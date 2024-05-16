.PHONY: clean clean-test clean-pyc clean-build docs

## remove all build, test, coverage and Python artifacts
clean: clean-build clean-pyc clean-test docs-clean

## remove build artifacts
clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg' -exec rm -f {} +

## remove Python file artifacts
clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	rm -rf .mypy_cache/
	rm -rf .ruff_cache

## remove test and coverage artifacts
clean-test:
	rm -fr .tox/
	rm -f .coverage*
	rm -fr htmlcov/
	rm -rf mypy_report/
	rm -rf *.html
	rm -fr .cache/
	rm -fr .pytest_cache
	rm -f coverage.xml

## remove sms artifacts
clean-sms:
	find inbox -name '*.json' -exec rm -f {} +
	find outbox -name '*.json' -exec rm -f {} +

## fix with ruff
format:
	poetry run ruff check --select I . --fix
	poetry run ruff format .

## check style with ruff, mypy
lint:
	poetry run ruff check . --exit-zero --fix
	poetry run mypy .

## run tests
test:
	poetry run pytest

## run tests with coverage report
coverage:
	poetry run coverage run -m pytest
	poetry run coverage combine
	poetry run coverage report

## check code coverage and test report with the default Python
test-reports:
	poetry run coverage run -m pytest --html=test_report.html --self-contained-html
	poetry run coverage combine
	poetry run coverage html
	poetry run mypy --html-report=mypy_report --install-types --non-interactive src tests

	@echo "Open reports htmlcov/index.html, test_report.html, mypy_report/index.html in your browser"

## run typer to build the cli markdown docs
cli-docs:
	poetry run typer sms_simulator.cli utils docs --name sms  > docs/docs/CLI.md

## generate Mkdocs HTML documentation
docs: docs-clean cli-docs
	cd docs/; poetry run mkdocs build

## serve docs locally
serve-docs: docs-clean cli-docs
	cd docs/; poetry run mkdocs serve --watch ../src/sms_simulator

## remove previously build docs
docs-clean:
	cd docs/; rm -rf site/;

## builds source and wheel package
dist: clean
	poetry build

## install the package and all development dependencies to the poetry virtualenv
install-all: clean
	poetry install

## start ray head node
start-ray:
	poetry run ray start --head

## stop ray head node
stop-ray:
	poetry run ray stop

##############################################################################
# Self Documenting Commands                                                  #
##############################################################################
.DEFAULT_GOAL := show-help
# See <https://gist.github.com/klmr/575726c7e05d8780505a> for explanation.
.PHONY: show-help
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)";echo;sed -ne"/^## /{h;s/.*//;:d" -e"H;n;s/^## //;td" -e"s/:.*//;G;s/\\n## /---/;s/\\n/ /g;p;}" ${MAKEFILE_LIST}|LC_ALL='C' sort -f|awk -F --- -v n=$$(tput cols) -v i=19 -v a="$$(tput setaf 6)" -v z="$$(tput sgr0)" '{printf"%s%*s%s ",a,-i,$$1,z;m=split($$2,w," ");l=n-i;for(j=1;j<=m;j++){l-=length(w[j])+1;if(l<= 0){l=n-i-length(w[j])-1;printf"\n%*s ",-i," ";}printf"%s ",w[j];}printf"\n";}'
