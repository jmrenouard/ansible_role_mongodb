#!/bin/bash
set -euo pipefail

# Path to the inventory
INVENTORY="inventory.yml"

# Source virtual environment if exists
if [ -d "../venv" ]; then
    # shellcheck disable=SC1091
    source ../venv/bin/activate
fi

# Run the playbook using the local role
# Configuration is handled via ansible.cfg in this directory

cat <<EOF > install_playbook.yml
---
- name: Deploy MongoDB Cluster
  hosts: mongodb_cluster
  roles:
    - mongod
EOF

ansible-playbook -v -i "$INVENTORY" install_playbook.yml "$@"

# Cleanup temporary playbook
rm install_playbook.yml
