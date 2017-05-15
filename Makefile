# This file is based on v0.0.12 of the Makefile template for Counsyl
# automation library repos from https://github.counsyl.com/automation/boilerplate/
#
# Before editing this file, consider updating the template instead, or removing
# this comment to prevent future template updates from being propagated here.
#

PACKAGE_NAME?=counsyl_pyads
TEST_OUTPUT_DIR?=test-output
TEST_OUTPUT_XML?=nosetests.xml
COVERAGE_DIR?=htmlcov
COVERAGE_DATA?=.coverage

VENV_DIR?=.venv
ifneq ($(VIRTUAL_ENV),)
	VENV_DIR=$(VIRTUAL_ENV)
endif
VENV_ACTIVATE=$(VENV_DIR)/bin/activate
WITH_VENV=. $(VENV_ACTIVATE);

$(VENV_ACTIVATE): requirements.txt requirements-dev.txt
	test -f $@ || virtualenv --python=python2.7 $(VENV_DIR)
	$(WITH_VENV) pip install --no-deps -r requirements.txt
	$(WITH_VENV) pip install --no-deps -r requirements-dev.txt
	touch $@

default:
	python setup.py check build

.PHONY: venv
venv: $(VENV_ACTIVATE)

.PHONY: setup
setup: venv

.PHONY: develop
develop: venv
	$(WITH_VENV) python setup.py develop

.PHONY: clean
clean:
	python setup.py clean
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg*/
	rm -rf __pycache__/
	rm -f MANIFEST
	rm -rf $(TEST_OUTPUT_DIR)
	rm -rf $(COVERAGE_DIR)
	rm -f $(COVERAGE_DATA)
	find $(PACKAGE_NAME) -type f -name '*.pyc' -delete

.PHONY: teardown
teardown:
	rm -rf $(VENV_DIR)/

.PHONY: lint
lint: venv
	$(WITH_VENV) flake8 -v $(PACKAGE_NAME)/ $(LINT_ARGS)

.PHONY: quality
quality: venv
	$(WITH_VENV) radon cc -s $(PACKAGE_NAME)/
	$(WITH_VENV) radon mi $(PACKAGE_NAME)/

.PHONY: test
test: develop
	$(WITH_VENV) py.test -v \
	--doctest-modules \
	--ignore=setup.py \
	--ignore=$(VENV_DIR) \
	--junit-xml=$(TEST_OUTPUT_DIR)/$(TEST_OUTPUT_XML) \
	--cov=${PACKAGE_NAME} \
	--cov-report=html $(TEST_ARGS)

.PHONY: sdist
sdist:
	python setup.py sdist


# End of boilerplate template. Automatic updates will leave lines below intact.
# Repo specific make targets can be added here.

