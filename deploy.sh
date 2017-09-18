#!/bin/bash -e

source lib.sh


set_params() {
	NB_NODES=${1:-2}
	DURATION=${2:-5}
	IOTLAB_SITE=${3:-grenoble}

	BROKER=${BROKER:-meshblu.octoblu.com}
}

main() {
	_ start_experiment
	nodes=`get_nodes`

	_ wait_for_boot
	nodes=`get_booted_nodes`

	check_nb_nodes

	_ deploy_injectors
}

deploy_node() {
	ssh $node "
	git clone http://github.com/iot-lab/iotlab-injectors.git
	cd iotlab-injectors/
	pip install -r requirements.txt
	pip install -e .
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


log "=== starting ===="
init "$@"
main
log "=== complete ==="
