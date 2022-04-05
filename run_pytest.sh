#!/usr/bin/env bash

set -e

FILE=$1

find * \( -name '*.py' -o -name '*.pyi' \) -and -not -path './venv/*' \
 -and -not -path './stubs/*' -exec python3 -m compileall -q -j 0 {} +

run_test() {
    python -m pytest -m "not local" -xvv $1
}
export -f run_test

if ! [ -z ${FILE} ]; then
    run_test ${FILE}
else
    for CUR in $(find 'tests' \( -name '*.py' -and -name 'test_*' \) \
            -and -not -path 'tests/data/*' \
            -and -not -path 'tests/__pycache__/*' |
            sort -sf); do
        run_test ${CUR}
    done
fi