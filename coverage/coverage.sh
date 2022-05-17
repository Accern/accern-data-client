#!/usr/bin/env bash

set -e
export IS_TEST=1

coverage erase

find * \( -name '*.py' -o -name '*.pyi' \) -and -not -path './venv/*' \
 -and -not -path './stubs/*' -exec python3 -m compileall -q -j 0 {} +


run_coverage() {
    echo $@
    python -m pytest -xvv $@ --cov --cov-append
    coverage report
    coverage xml -o coverage/directory/xml_report.xml
    coverage html -d coverage/directory/html_report
    coverage erase
}
export -f run_coverage

ALL=$(find 'tests' \( -name '*.py' -and -name 'test_*' \) \
            -and -not -path 'tests/data/*' \
            -and -not -path 'tests/__pycache__/*' |
            sort -sf)
# for CUR in $(find 'tests' \( -name '*.py' -and -name 'test_*' \) \
#             -and -not -path 'tests/data/*' \
#             -and -not -path 'tests/__pycache__/*' |
#             sort -sf); do
#     ALL="${ALL} ${CUR}"
# done
run_coverage ${ALL[@]}
