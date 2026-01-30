---
trigger: explicit_call
description: Periodic project maintenance, cleanup, and dependency updates
category: governance
---

# Maintenance Workflow

This workflow performs routine cleanup, linting, and health checks on the Ansible role development environment.

## When to use this workflow

- When the user types `/maintenance`.
- Before starting a new feature or after finishing tests.
- To troubleshoot environment issues.

## Task

// turbo

1. Clean up Molecule temporary instances and files.

   ```bash
   molecule cleanup
   molecule destroy --all
   ```

2. Run Ansible-Lint to ensure compliance with best practices.

   ```bash
   ansible-lint .
   ```

3. Verify Molecule scenarios availability and status.

   ```bash
   molecule list
   ```

4. Check for unhandled virtual environment directories (should be ignored by git).

   ```bash
   ls -d venv/ .venv/ 2>/dev/null || echo "No local venv detected in root"
   ```

## Constraints

- If `molecule list` shows any "Created" instances, remind the user to destroy them if not needed.
- Report any linting errors that violate `CONSTRAINTS.md`.
