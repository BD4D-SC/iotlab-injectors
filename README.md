The IoT-LAB injectors
=====================


Install
-------

	git clone git@github.com:iot-lab/iotlab-injectors.git
	cd iotlab-injectors

	mkvirtualenv embers
	pip install -r requirements.txt
	pip install .


Testing it works (manual, quick check)
--------------------------------------

	registry --init --broker meshblu.octoblu.com
	injectors --run

	subscriber --traffic --print-event   # (in separate terminal)
	injectors --run


Testing it works (with your IoT-LAB account)
--------------------------------------------

this assumes you have a configured IoT-LAB account


	./init-ssh-config.sh
	./deploy.sh
	./run.sh

	tail -f {deploy,run}.sh.log   # (in a separate terminal)


Downloading additional datasets
-------------------------------

	datasets --download --dataset citypulse --event traffic


Usage notes
-----------

- Tools `registry`, `injectors` and `datasets` provide usage information
  and will briefly tell what they can do of if you use `--help`.

- Meshblu has a hardcoded limit of 1000 items when listing devices.
  Do not expect to see more than 1k devices when using `registry --list`
  regardless of the actual number of registered devices.

- Using option `--reuse-devices` with `--nb-devices` greater than 1k
  will create additional devices - above the 1k limit - instead of
  re-using available one.  This is due to the 1k list limit above.

- Utility script `init-ssh-config.sh` enables the `ssh-mux` ControlMaster
  in your ~/.ssh/config for iot-lab ssh frontends `grenoble` and `saclay`.
  This may result in after-the-fact seemingly 'odd' ssh behaviour to these
  two hosts.  You may then prefer to disable the ssh-mux in your .ssh/config,
  or run `ssh <host> -O exit ...` to reset the mux.
