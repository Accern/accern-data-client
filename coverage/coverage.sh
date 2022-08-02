#!/usr/bin/env bash

set -e
export IS_TEST=1
RESULT_FNAME=$1;shift
FILES=($@)
coverage erase

find * \( -name '*.py' -o -name '*.pyi' \) -and -not -path './venv/*' \
 -and -not -path './stubs/*' -exec python3 -m compileall -q -j 0 {} +


run_coverage() {
    python -m pytest -xvv --full-trace --junitxml="test-results/parts/result${2}.xml" $1 --cov --cov-append
    coverage report
}
export -f run_coverage

if ! [ -z ${FILES} ]; then
    IDX=0
    for CUR_TEST in ${FILES[@]}; do
        run_coverage $CUR_TEST $IDX
        IDX=$((IDX+1))
    done
else
    IDX=0
    for CUR in $(find 'tests' \( -name '*.py' -and -name 'test_*' \) \
            -and -not -path 'tests/data/*' \
            -and -not -path 'tests/data_mini/*' \
            -and -not -path 'tests/__pycache__/*' |
            sort -sf); do
    run_coverage ${CUR} $CUR_TEST $IDX
    IDX=$((IDX+1))
    done
fi
python3 -m tests merge_results --dir test-results --out-fname ${RESULT_FNAME}
echo "${RESULT_FNAME} generated"
rm -r test-results/parts

coverage xml -o coverage/reports/xml_report.xml
coverage html -d coverage/reports/html_report
