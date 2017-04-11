The IoT-LAB injectors
=====================


Dev install
-----------

	git clone git@github.com:iot-lab/iotlab-injectors.git
	git clone git@github.com:iot-lab/embers-datasets.git
	git clone git@github.com:iot-lab/meshblu-clients.git

	mkvirtualenv embers-dev
	(cd embers-datasets/ && pip install -e .)
	(cd meshblu-clients/ && pip install -e .)

	cd iotlab-injectors
	pip install -r requirements.txt
	pip install -e .


Installing a local instance of Meshblu
--------------------------------------

	git clone git@github.com:iot-lab/meshblu.git

	meshblu/install.sh docker
	# logout/login or reboot as needed

	meshblu/install.sh docker-compose meshblu
	meshblu/install.sh start


Checking it works (local, manual, quick check)
----------------------------------------------

	registry --init
	injectors --run

	subscriber --pollution --print-event yes  # (in separate terminal)
	injectors --run --event pollution


Testing it works (against local Meshblu instance)
-------------------------------------------------

	pip install pytest
	pytest -v


Testing it works (with your IoT-LAB account)
--------------------------------------------

	./init-ssh-config.sh
	./deploy.sh
	./run.sh

	tail -f {deploy,run}.sh.log   # (in separate terminal)


Downloading additional datasets
-------------------------------

	datasets --list
	datasets --download --dataset citypulse --event traffic
