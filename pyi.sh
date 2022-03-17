#!/usr/bin/env bash

PY_FILES=$(find stubs -type f -name '*.py')
echo "${PY_FILES}"
[ -z ${PY_FILES} ]
