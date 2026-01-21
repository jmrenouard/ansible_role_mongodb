---
description: Run Ansible and YAML linting
---

# Lint Workflow

This workflow ensures code quality by running `ansible-lint` and `yamllint`.

## When to use this workflow

- When the user types `/lint`.
- Before every commit.

## Task

// turbo

1. Run `ansible-lint` on the role.

   ```bash
   ansible-lint
   ```

2. Run `yamllint` on all YAML files.

   ```bash
   yamllint .
   ```

## Constraints

- Must return 0 errors for the workflow to be considered successful.
- Follow rules defined in `.ansible-lint`.
