#!/bin/bash

SCRIPT_ROOT=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
CORE_ROOT=$(cd $SCRIPT_ROOT/.. && pwd)
CORE_TOP=$(cd $CORE_ROOT/.. && pwd)

cat <<EOF
CORE_ROOT: $CORE_ROOT
CORE_TOP: $CORE_TOP
EOF
