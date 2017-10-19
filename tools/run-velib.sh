#!/bin/bash

host="strasbourg"
conf="tests/msg.test.embers.city"

log="velib.log"


run() {
	ssh $host.iot-lab.info "
	source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
	workon embers
	cd $conf
	(
	date +'%F %T == starting =='
	
	cat <<< '$(self_desc)' >> $log

	PYTHONUNBUFFERED=true \
	injectors --run \
		--dataset paris	\
		--event parking	\
		--ev-per-h 60	\
		--nb-dev 1226	\
		--proto https	\
		--fiware	\
		--duration $((24*60))

	date +'%F %T == complete =='
	) &>> $log < /dev/null &
	"
}

self_desc() {
	cat "$0" | sed '1,/PYTHONUN/ d; /complete/,$ d'
}


run
