SHELL := /bin/bash

JOB_ID ?= ""
RESULT_EXPORT_PATH ?= results/$(JOB_ID).png
RANDOM ?= 0

load:
	python3 -m venv simons-env
	source simons-env/bin/activate

.PHONY: install
install:
	if [ -n "$$SIMONS_ENV" ]; then make load; fi
	python -m ensurepip --upgrade
	pip install qiskit
	pip install qiskit-ibm-runtime
	pip install qiskit[visualization]
	pip install git+https://github.com/qiskit-community/qiskit-textbook.git#subdirectory=qiskit-textbook-src
	pip install matplotlib
	pip install tweedledum
	pip install python-dotenv

quantum:
	python quantum.py $(RANDOM)

result:
	python result.py $(JOB_ID) $(RESULT_EXPORT_PATH)
