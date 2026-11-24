#!/bin/bash
# MongoDB Lab Aliases
# Source this file to get quick access to the nodes: source aliases.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

alias m1='ssh -i "${SCRIPT_DIR}/id_rsa" -p 2221 -o StrictHostKeyChecking=no root@localhost'
alias m2='ssh -i "${SCRIPT_DIR}/id_rsa" -p 2222 -o StrictHostKeyChecking=no root@localhost'
alias m3='ssh -i "${SCRIPT_DIR}/id_rsa" -p 2223 -o StrictHostKeyChecking=no root@localhost'
