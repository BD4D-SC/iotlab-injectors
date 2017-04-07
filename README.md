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

	subscriber --traffic --print-event yes   # (in separate terminal)
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
