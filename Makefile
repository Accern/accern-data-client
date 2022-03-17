help:
	@echo "The following make targets are available:"
	@echo "install install all dependencies"
	@echo "lint-all	run all lint steps"
	@echo "lint-comment	run linter check over regular comments"
	@echo "lint-emptyinit	main inits must be empty"
	@echo "lint-flake8	run flake8 checker to deteck missing trailing comma"
	@echo "lint-forgottenformat	ensures format strings are used"
	@echo "lint-indent	run indent format check"
	@echo "lint-pycodestyle	run linter check using pycodestyle standard"
	@echo "lint-pycodestyle-debug	run linter in debug mode"
	@echo "lint-pyi	Ensure no regular python files exist in stubs"
	@echo "lint-pylint	run linter check using pylint standard"
	@echo "lint-requirements	run requirements check"
	@echo "lint-stringformat	run string format check"
	@echo "lint-type-check	run type check"
	@echo "pre-commit 	sort python package imports using isort"
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

lint-emptyinit:
	[ ! -s app/__init__.py ]

lint-pyi:
	./pyi.sh

lint-stringformat:
	! find . \( -name '*.py' -o -name '*.pyi' \) -and -not -path './venv/*' \
	| xargs grep --color=always -nE "%[^'\"]*\"\\s*%\\s*"

lint-indent:
	# FIXME add pyi at one point
	! find . -name '*.py' -and -not -path './venv/*' \
	| xargs grep --color=always -nE "^(\s{4})*\s{1,3}\S.*$$"

lint-forgottenformat:
	! ./forgottenformat.sh

lint-requirements:
	locale
	cat requirements.lint.txt
	sort -ufc requirements.lint.txt
	cat requirements.txt
	sort -ufc requirements.txt

lint-pycodestyle:
	pycodestyle --exclude=venv --show-source packages/python

lint-pycodestyle-debug:
	pycodestyle --exclude=venv,.git,.mypy_cache -v --show-source packages/python

lint-pylint:
	find packages/python \( -name '*.py' -o -name '*.pyi' \) -and -not -path './venv/*' \
	-and -not -path './stubs/*' \
	| sort
	find packages/python \( -name '*.py' -o -name '*.pyi' \) -and -not -path './venv/*' \
	-and -not -path './stubs/*' \
	| sort | xargs pylint -j 6

lint-type-check:
	mypy packages/python --config-file mypy.ini

lint-flake8:
	flake8 --verbose --select C815,I001,I002,I003,I004,I005 --exclude \
	venv --show-source ./

lint-all: \
	lint-comment \
	lint-emptyinit \
	lint-pyi \
	lint-stringformat \
	lint-indent \
	lint-forgottenformat \
	lint-requirements \
	lint-pycodestyle \
	lint-pylint \
	lint-type-check \
	lint-flake8

pre-commit:
	pre-commit install
	isort .

publish-pypi:
	rm -r dist build accern_xyme.egg-info || echo "no files to delete"
	python3 -m pip install -U setuptools twine wheel
	python3 setup.py sdist bdist_wheel
