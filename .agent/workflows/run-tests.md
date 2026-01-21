---
description: run-tests
---

# Run Tests Workflow

This workflow automates the execution of Ansible role tests using Molecule.

## When to use this workflow

- When the user types `/run-tests`.
- When changes are made to tasks, templates, or defaults.
- Before a release or after major refactoring.

## Task

// turbo

1. Execute all molecule scenarios.

   ```bash
   molecule test --all
   ```

2. If tests pass, verify idempotency for the default scenario.

   ```bash
   molecule idempotence -s default
   ```

## Constraints

- Stop if any molecule stage fails and report the logs.
- Ensure Docker is available on the host.
