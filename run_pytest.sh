#!/usr/bin/env bash

set -e
export IS_TEST=1
FILES=($@)

find * \( -name '*.py' -o -name '*.pyi' \) -and -not -path './venv/*' \
 -and -not -path './stubs/*' -exec python3 -m compileall -q -j 0 {} +

run_test() {
    python -m pytest -xvv --full-trace --junitxml="test-results/parts/result${2}.xml" $1
}
export -f run_test

if ! [ -z ${FILES} ]; then
    IDX=0
    for CUR_TEST in ${FILES[@]}; do
        run_test $CUR_TEST $IDX
        IDX=$((IDX+1))
    done
else
    IDX=0
    for CUR in $(find 'tests' \( -name '*.py' -and -name 'test_*' \) \
            -and -not -path 'tests/data/*' \
            -and -not -path 'tests/data_mini/*' \
            -and -not -path 'tests/__pycache__/*' |
            sort -sf); do
        run_test ${CUR} $CUR_TEST $IDX
        IDX=$((IDX+1))
    done
fi
python3 -c "from tests.utils import merge_results; merge_results('./test-results')"
rm -r test-results/parts
