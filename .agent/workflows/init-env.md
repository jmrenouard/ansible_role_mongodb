---
trigger: explicit_call
description: Python virtual environment and dependency initialization
category: tool
---

# Initialize Environment Workflow

This workflow sets up a Python virtual environment and installs all necessary dependencies for Ansible development and Molecule testing.

## When to use this workflow

- When the user types `/init-env`.
- After cloning the repository.
- When requirements change.

## Task

// turbo

1. Create a virtual environment if it doesn't exist.

   ```bash
   python3 -m venv venv
   ```

2. Activate the virtual environment and install dependencies.

   ```bash
   source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
   ```

3. (Optional) Initialize Ansible Galaxy dependencies.

   ```bash
   source venv/bin/activate && ansible-galaxy collection install -r molecule/default/requirements.yml || true
   ```

## Constraints

- Ensure `python3` and `pip` are installed on the host.
- The workflow should be idempotent (safe to run multiple times).
