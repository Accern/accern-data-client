help:
	@echo "The following make targets are available:"
	@echo "install install all dependencies"
	@echo "lint-all	run all lint steps"
	@echo "lint-comment	run linter check over regular comments"
	@echo "lint-docstring	run linter check over docstring"
	@echo "lint-flake8	run flake8 checker to detect missing trailing comma"
	@echo "lint-forgottonformat	ensures format strings are used"
	@echo "lint-pycodestyle	run linter check using pycodestyle standard"
	@echo "lint-pycodestyle-debug	run linter in debug mode"
	@echo "lint-pylint	run linter check using pylint standard"
	@echo "lint-requirements	run requirements check"
	@echo "lint-stringformat	run string format check"
	@echo "lint-type-check	run type check"
	@echo "publish-pypi	publish the library on pypi"

ENV ?= venv

create-env:
	python3 -m venv $(ENV)
	. $(ENV)/bin/activate
	make install

install:
	python -m pip install --upgrade pip
	python -m pip install --progress-bar off --upgrade -r requirements.lint.txt

lint-comment:
	! find . \( -name '*.py' -o -name '*.pyi' \) -and -not -path './venv/*' \
	| xargs grep --color=always -nE \
	  '#.*(todo|xxx|fixme|n[oO][tT][eE]:|Note:|nopep8\s*$$)|.\"^s%'

lint-docstring:
	flake8 --verbose --select DAR --exclude venv --show-source ./

lint-flake8:
	flake8 --verbose --select C815 --exclude venv --show-source ./

lint-forgottenformat:
	! ./forgottenformat.sh

lint-pycodestyle:
	pycodestyle --exclude=venv --show-source packages/python

lint-pycodestyle-debug:
	pycodestyle --exclude=venv -v --show-source packages/python

lint-pylint:
	find packages/python \( -name '*.py' -o -name '*.pyi' \) -and -not -path './venv/*' \
	-and -not -path './stubs/*' \
	| sort
	find packages/python \( -name '*.py' -o -name '*.pyi' \) -and -not -path './venv/*' \
	-and -not -path './stubs/*' \
	| sort | xargs pylint -j 6

lint-requirements:
	sort -cf requirements.txt
	sort -cf requirements.lint.txt

lint-stringformat:
	! find . \( -name '*.py' -o -name '*.pyi' \) -and -not -path './venv/*' \
	| xargs grep --color=always -nE "%[^'\"]*\"\\s*%\\s*"

lint-type-check:
	mypy packages/python --config-file mypy.ini

lint-all: \
	lint-comment \
	lint-docstring \
	lint-forgottenformat \
	lint-requirements \
	lint-stringformat \
	lint-pycodestyle \
	lint-pylint \
	lint-type-check \
	lint-flake8

publish-pypi:
	rm -r dist build accern_xyme.egg-info || echo "no files to delete"
	python3 -m pip install -U setuptools twine wheel
	python3 setup.py sdist bdist_wheel
