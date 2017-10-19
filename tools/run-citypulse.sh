#!/bin/bash

host="strasbourg"
conf="tests/msg.test.embers.city"

log="citypulse.log"


run() {
	ssh $host.iot-lab.info "
	source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
	workon embers
	cd $conf
	(
	datasets --download --dataset citypulse --event traffic

	date +'%F %T == starting =='
	
	cat <<< '$(self_desc)' >> $log

	PYTHONUNBUFFERED=true \
	injectors --run \
		--dataset citypulse	\
		--event traffic	\
		--ev-per-h 12	\
		--nb-dev 449	\
		--proto https	\
		--duration $((3*60))

	date +'%F %T == complete =='
	) &>> $log < /dev/null &
	"
}

self_desc() {
	cat "$0" | sed '1,/PYTHONUN/ d; /complete/,$ d'
}


run
