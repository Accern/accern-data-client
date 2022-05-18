help:
	@echo "The following make targets are available:"
	@echo "git-check	run git check"
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
	@echo "version-sync	check package versions are same"

ENV ?= venv
VERSION=`echo "from packages.python.accern_data import __version__;import sys;out = sys.stdout;out.write(__version__);out.flush();" | python3 2>/dev/null`
TS_VERSION=`echo "import json;fin=open('package.json', 'r');version=json.loads(fin.read())['version'];fin.close();print(version)" | python3 2>/dev/null`

coverage-report:
	./coverage/coverage.sh

create-env:
	python3 -m venv $(ENV)
	. $(ENV)/bin/activate
	make install

git-check:
	@git diff --exit-code 2>&1 >/dev/null && git diff --cached --exit-code 2>&1 >/dev/null || (echo "working copy is not clean" && exit 1)
	@test -z `git ls-files --other --exclude-standard --directory` || (echo "there are untracked files" && exit 1)
	@test `git rev-parse --abbrev-ref HEAD` = "main" || (grep -q -E "a|b|rc" <<< "$(VERSION)") || (echo "not on main" && exit 1)

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
	make git-check
	make version-sync
	rm -r dist build accern_data.egg-info || echo "no files to delete"
	python3 -m pip install -U setuptools twine wheel
	python3 setup.py sdist bdist_wheel
	python3 -m twine upload dist/accern_data-$(VERSION)-py3-none-any.whl dist/accern_data-$(VERSION).tar.gz
	git tag "v$(VERSION)"
	git push origin "v$(VERSION)"
	@echo "succesfully deployed $(VERSION)"

pytest:
	./run_pytest.sh $(FILE)

version-sync:
	@test "${VERSION}" = "$(TS_VERSION)" || (echo "version not matching. VERSION=$(VERSION), TS_VERSION=$(TS_VERSION)" && exit 1)
