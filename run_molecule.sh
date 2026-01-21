#!/bin/bash
set -e
mkdir -p logs
LOGFILE="logs/molecule_full_run_$(date +%Y%m%d_%H%M%S).log"
echo "Starting Molecule tests at $(date)" | tee "$LOGFILE"
source ./venv/bin/activate
cd roles/mongod
molecule test --all --destroy=always -- -v >> "../../$LOGFILE" 2>&1
echo "Molecule tests finished at $(date) with exit code $?" | tee -a "$LOGFILE"
deactivate
