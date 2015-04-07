#! /usr/bin/make

PACKAGE_NAME=counsyl_pyads
TEST_OUTPUT?=nosetests.xml

VENV_DIR?=.venv
VENV_ACTIVATE=$(VENV_DIR)/bin/activate
WITH_VENV=. $(VENV_ACTIVATE);

default:
	python setup.py check build

.PHONY: venv setup clean teardown lint test package

$(VENV_ACTIVATE): requirements.txt requirements-dev.txt
	test -f $@ || virtualenv --python=python2.7 $(VENV_DIR)
	$(WITH_VENV) pip install -r requirements.txt
	$(WITH_VENV) pip install -r requirements-dev.txt
	touch $@

venv: $(VENV_ACTIVATE)

setup: venv

clean:
	python setup.py clean
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg*/
	rm -rf __pycache__/
	rm -f MANIFEST
	rm -f $(TEST_OUTPUT)
	find $(PACKAGE_NAME) -type f -name '*.pyc' -delete

teardown:
	rm -rf $(VENV_DIR)/

lint: venv
	$(WITH_VENV) flake8 $(PACKAGE_NAME)/

test: venv
	$(WITH_VENV) py.test --junitxml=$(TEST_OUTPUT)

package:
	python setup.py sdist
