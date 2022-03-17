#!/usr/bin/env bash

set -e

ANY_DOUBLE="([^\\\\\"]|\\\\\")*"
ANY_SINGLE="([^\\\\']|\\\\')*"
IS_CURLY="([{][^{]|[^}][}])"
EAT_DOUBLE="\"${ANY_DOUBLE}\""
EAT_SINGLE="'${ANY_SINGLE}'"
EAT_STRINGS="^([^\"'#]|${EAT_DOUBLE}|${EAT_SINGLE})*"

INVALID_F_DOUBLE="f\"([^\\\\\"}{]|\\\\\")*\""
INVALID_F_SINGLE="f'([^\\\\'}{]|\\\\')*'"
INVALIDS="${INVALID_F_DOUBLE}|${INVALID_F_SINGLE}"
NO_F_DOUBLE="[^rf]\"${ANY_DOUBLE}${IS_CURLY}${ANY_DOUBLE}\""  # we also allow r
NO_F_SINGLE="'${ANY_SINGLE}${IS_CURLY}${ANY_SINGLE}'"  # we disallow any curls
NO_FS="${NO_F_DOUBLE}|${NO_F_SINGLE}"

MAIN_MATCH="(${NO_FS}|${INVALIDS})"
REGEX="${EAT_STRINGS}${MAIN_MATCH}"
echo ${REGEX}

! read -r -d '' PY_FILTER <<'EOF'
import sys

stdin = sys.stdin
stdout = sys.stdout
is_triple = False
while True:
    line = stdin.readline()
    if not line:
        break
    if line.count('"""') % 2 != 0:
        is_triple = not is_triple
        continue
    if not is_triple:
        stdout.write(line)
        stdout.flush()
EOF

find . \( -name '*.py' -o -name '*.pyi' \) -and -not -path './venv/*' \
    | xargs grep -nE "['\"]" \
    | python3 -c "${PY_FILTER}" \
    | grep -E "${REGEX}" \
    | grep --color=always -nE "${MAIN_MATCH}"
