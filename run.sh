#!/bin/bash -e

source lib.sh


set_params() {
	NB_DEVICES=${1:-1}
	DURATION=${2:-.1}
	EV_PER_HOUR=${3:-3600}
	PROTOCOL="http"
	EVENTS="traffic"

	NB_NODES=$nb_nodes
}

main() {
	_ run_injectors
}

run_injectors() {
	for node in $nodes; do
		ssh $node injectors --run \
		--nb-devices $NB_DEVICES \
		--duration $DURATION \
		--events $EVENTS \
		--ev-per-hour $EV_PER_HOUR \
		--protocol $PROTOCOL \
		&
	done
	for pid in `jobs -p`; do
		wait $pid
	done
}

init_nodes

log "=== starting ===="
init "$@"
main
log "=== complete ==="
