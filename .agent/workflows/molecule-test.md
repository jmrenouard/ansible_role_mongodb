---
description: Run Molecule tests for specific scenarios
---

# Molecule Test Workflow

This workflow allows running specific Molecule scenarios or all scenarios.

## When to use this workflow

- When the user types `/molecule-test`.
- To validate a specific setup (e.g., `cluster`).

## Task

// turbo

1. List available scenarios.

   ```bash
   molecule list
   ```

2. Execute the requested scenario (defaulting to all if not specified).

   ```bash
   molecule test --all
   ```

## Constraints

- Use `--destroy=always` to ensure environment cleanup after tests.
- Report any failure in the `verify` or `side_effect` stages.
