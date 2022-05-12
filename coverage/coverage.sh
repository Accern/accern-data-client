#!/usr/bin/env bash

set -e
export IS_TEST=1

coverage erase

find * \( -name '*.py' -o -name '*.pyi' \) -and -not -path './venv/*' \
 -and -not -path './stubs/*' -exec python3 -m compileall -q -j 0 {} +


run_coverage() {
    python -m pytest -xvv $1 --cov --cov-append
}
export -f run_coverage

for CUR in $(find 'tests' \( -name '*.py' -and -name 'test_*' \) \
            -and -not -path 'tests/data/*' \
            -and -not -path 'tests/__pycache__/*' |
            sort -sf); do
    run_coverage ${CUR}
done

coverage report
coverage html
coverage erase
