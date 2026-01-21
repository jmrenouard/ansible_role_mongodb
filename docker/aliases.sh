#!/bin/bash
# MongoDB Lab Aliases
# Source this file to get quick access to the nodes: source aliases.sh

alias m1='ssh -i /home/jmren/GIT_REPOS/ansible_role_mongodb/docker/id_rsa -p 2221 -o StrictHostKeyChecking=no root@localhost'
alias m2='ssh -i /home/jmren/GIT_REPOS/ansible_role_mongodb/docker/id_rsa -p 2222 -o StrictHostKeyChecking=no root@localhost'
alias m3='ssh -i /home/jmren/GIT_REPOS/ansible_role_mongodb/docker/id_rsa -p 2223 -o StrictHostKeyChecking=no root@localhost'
