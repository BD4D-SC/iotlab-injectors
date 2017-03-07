The IoT-LAB injectors
=====================


Install
-------

	git clone git@github.com:iot-lab/iotlab-injectors.git
	cd iotlab-injectors

	mkvirtualenv embers
	pip install -r requirements.txt
	pip install .


Dev install
-----------

	mkvirtualenv embers-dev
	cd ../embers-datasets/ && pip install -e .
	cd ../meshblu-clients/ && pip install -e .
	pip install -r requirements.txt
	cd ../iotlab-injectors/
	pip install -e .


Testing it works
----------------

	pip install pytest
	pytest -v
