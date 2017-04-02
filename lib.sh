# sourced by main scripts

LOG=${LOG:-$0.log}


set_params() {
	NB_NODES=${1:-2}
	DURATION=${2:-5}
	IOTLAB_SITE=${3:-grenoble}
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
	time_start=`date +%s`
	while true; do
		nb_booted=`get_booted_nodes | wc -l`
		time_diff=$[`date +%s` - time_start]
		[ $nb_booted = $NB_NODES ] && break
		[ $time_diff -gt 80 ] && break
		#echo "nb_booted=$nb_booted time_diff=$time_diff"
		sleep 1
	done
}

get_booted_nodes() {
	for node in $nodes; do
		(check_ssh_access && echo $node) &
	done
	wait
}

check_ssh_access() {
	ssh $node -o ConnectTimeout=2 id &>/dev/null
}

get_running_exp_ids() {
	experiment-cli get -l --state Running \
	| awk '/"id":/ {print $2}' | tr -d ,
}

check_exp_id() {
	running_exp_ids=`get_running_exp_ids`
	[ "$running_exp_ids" ] || {
		echo "no running experiment" && exit 1
	} >&2
	[ "$exp_id" ] && {
		[ grep -qF "$exp_id" <<< "$running_exp_ids" ] && return 0
		echo "no such running experiment: $exp_id" && exit 1
	} >&2
	exp_id=`head -1 <<< "$running_exp_ids"`
	[ "$exp_id" == "$running_exp_ids" ] || {
		echo "more than one experiment running"
		echo "use e.g. 'exp_id=<id> $0 ...'"
		echo "select <id> in:" $running_exp_ids && exit 1
	} >&2
}

init_nodes() {
	check_exp_id
	nodes=`get_nodes`
	nodes=`get_booted_nodes`
	[ "$nodes" ] || {
		echo "no booted nodes in experiment $exp_id" && exit 1
	} >&2

	nb_nodes=`wc -l <<< "$nodes"`
	IOTLAB_SITE=`head -1 <<<"$nodes" | awk -F . '{print $2}'`
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
	log "=== $func"
	$func &>> $LOG
	kill $_pid && _pid=
	printf "\r%-30s [%s]\n" $func "done"
}

on_error() {
	[ $_pid ] && kill $_pid
	echo "ERROR"
	echo
	echo "last line in $LOG:"
	tail -1 $LOG
	exit 1
}

init_exit_trap() {
	exec 3>&2
	trap '[ $? = 0 ] || on_error >&3' EXIT
}

log() {
	date +"%F %T $*" >> $LOG
}

check_nb_nodes() {
	nb_nodes=`wc -w <<< $nodes`
	[ $nb_nodes = $NB_NODES ] && return

	msg="!!! deploying on $nb_nodes nodes"
	log  "$msg"
	echo "$msg"
}

log_trace() {
	set -x
	$* &>> $LOG
	set +x
} &>/dev/null

init_ssh_mux() {
	ssh $IOTLAB_SITE.iot-lab.info -O exit &>/dev/null || true
	ssh $IOTLAB_SITE.iot-lab.info id &>/dev/null || {
		fatal "failed to connect to $IOTLAB_SITE.iot-lab.info"
	}
}

sanity_check_params() {
	[ "$IOTLAB_SITE" ] || fatal "IOTLAB_SITE is not defined"
	[ "$NB_NODES" ] || fatal "NB_NODES is not defined"
	[ "$DURATION" ] || fatal "DURATION is not defined"
}

fatal() {
	echo "FATAL: $*" | tee -a $LOG >&2
	exit 1
}

init() {
	log_trace set_params $@
	sanity_check_params
	init_ssh_mux
	init_exit_trap
}
