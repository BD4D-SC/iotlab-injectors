#!/bin/bash
#set -x

NB_NODES=${1:-2}
DURATION=${2:-5}

BROKER=${BROKER:-DEFINE_MESHBLU.broker.fqdn}

IOTLAB_SITE=${3:-grenoble}
LOCAL_OVERRIDES="deploy.local.sh"

LOG=${LOG:-$0.log}


main() {
	startup

	_ start_experiment
	nodes=`get_nodes`

	_ wait_for_boot
	nodes=`get_booted_nodes`

	check_nb_nodes

	_ deploy_injectors
	_ run_injectors

	finish
}

start_experiment() {
	exp_id=$(experiment-cli submit -d $DURATION \
		-l $NB_NODES,archi=a8:at86rf231+site=$IOTLAB_SITE \
		| awk '/"id":/ {print $2}'
	)
	experiment-cli wait -i $exp_id &>/dev/null
}

get_nodes() {
	experiment-cli get -i $exp_id -r \
	| awk '/network_address/ {print $2}' \
	| tr -d '",'
}

wait_for_boot() {
	for node in $nodes; do
		(while ! check_ssh_access; do
			[ $[nb_fail++] -gt 25 ] && exit 1
			sleep 1
		 done) &
	done
	wait
}

get_booted_nodes() {
	for node in $nodes; do
		(check_ssh_access && echo $node) &
	done
	wait
}

deploy_node() {
	ssh $node "
	git clone http://github.com/iot-lab/iotlab-injectors.git
	cd iotlab-injectors/
	pip install -r requirements.txt
	pip install .
	"
}

configure_node() {
	ssh $node "
	registry --init --broker $BROKER
	"
}

deploy_injectors() {
	# nodes nfs-share [most of] their filesystem
	# deploy on first node
	node=`head -1 <<<"$nodes"`
	deploy_node &> /dev/null
	configure_node
}

run_injectors() {
	for node in $nodes; do
		ssh $node injectors --run &
	done
	wait
}

check_ssh_access() {
	ssh $node -o ConnectTimeout=2 id &>/dev/null
}

animated_wait() {
	while true; do
		for c in . o O 0 O o; do
			printf "\r%-30s   %c  " $func $c
			sleep .3
		done
	 done
}

_() {
	func=$1
	animated_wait & _pid=$!
	disown $_pid
	date_stamp "=== $func"
	$func &>> $LOG
	kill $_pid
	printf "\r%-30s [%s]\n" $func "done"
}

date_stamp() {
	date +"%F %T $*" >> $LOG
}

check_nb_nodes() {
	nb_nodes=`wc -w <<< $nodes`
	[ $nb_nodes = $NB_NODES ] && return

	msg="!!! deploying on $nb_nodes nodes"
	date_stamp "$msg"
	echo "$msg"
}

startup() {
	cat /dev/null > $LOG

	date_stamp "=== starting" \
	"[$NB_NODES nodes @ $IOTLAB_SITE / $DURATION min]"
}

finish() {
	date_stamp "=== complete ==="
}

[ -f $LOCAL_OVERRIDES ] && source $LOCAL_OVERRIDES

main
