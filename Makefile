.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

define BROWSER_PYSCRIPT
import os, webbrowser, sys

from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

BROWSER := python -c "$$BROWSER_PYSCRIPT"


help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	-rm -f .coverage
	-rm -fr htmlcov/
	-rm -fr .pytest_cache
	-rm test_app/pactfiles/TestConsumer-TestProvider-pact.json

lint: ## check style with flake8
	flake8 pact_testgen tests

format: ## Run Black formatter
	black .

test-client: ## Run test_app client tests to generate a sample Pact file
	cd test_app && pytest client_tests.py

test-provider: ## Run test_app provider test suite
	cd test_app/provider && python manage.py test

testgen: test-client  ## Run pact-testgen on test app contract to regenerate test files
	cd test_app && ./run_pact_testgen

test: ## run tests quickly with the default Python
	pytest

test-integration: test-provider test  ## Run sample app + pact-testgen tests

test-debug: clean-test test-client  ## Run tests, drop to debugger on failure
	pytest --pdb

test-all: clean-test test-client testgen test-provider  ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run --source pact_testgen -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

docs: ## generate Sphinx HTML documentation, including API docs
	rm -f docs/pact_testgen.rst
	rm -f docs/modules.rst
	sphinx-apidoc -o docs/ pact_testgen
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

servedocs: docs ## compile the docs watching for changes
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python setup.py install


# Pact broker
# Install from https://github.com/pact-foundation/pact-ruby-standalone/releases

broker-publish:  ## Publish test app pact contract to the pact broker
	pact-broker publish \
	test_app/pactfiles/TestConsumer-TestProvider-pact.json \
	--consumer-app-version=`git rev-parse --short HEAD` \
	--tag=DEV
