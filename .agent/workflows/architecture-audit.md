---
description: archi
---

# Architecture Audit Workflow

This workflow performs a structural audit of the Ansible role to identify inconsistencies, naming issues, and consolidation opportunities.

## When to use this workflow

- When the user types `/architecture-audit`.
- Before a major refactoring phase.
- To ensure compliance with `ARCHITECTURE.md`.

## Task

1. **Analyze Ansible Best Practices**:
   - Check if variables are prefixed with `mongodb_` in `defaults/`, `vars/`, and `tasks/`.
   - Verify usage of native Ansible modules over `shell` or `command`.
   - Identify inline service restarts that should be converted to `handlers`.
   - Audit task names for clarity and standard formatting.

2. **Idempotency & Robustness**:
   - Check `shell`/`command` tasks for `changed_when` or `failed_when`.
   - Verify that tasks are idempotent and don't perform redundant work.
   - Check if `meta/main.yml` is synchronized with `Changelog`.

3. **Molecule Compliance**:
   - Ensure all scenarios have a `verify.yml` and `prepare.yml`.
   - Identify gaps in scenario coverage (e.g., missing cluster tests for specific OS).

4. **Output Report**:
   - Generate a "Role Health Report" highlighting:
     - **Semantic Drift**: Inconsistent variable naming.
     - **Best Practice Gaps**: Missing handlers, raw shell usage.
     - **Test Gaps**: Scenarios not covered by Molecule.
     - **Refactoring Proposals**: Specific steps to improve role modularity.

## Constraints

- Respect the `$$IMMUTABLE$$` sections of `ARCHITECTURE.md`.
- Focus on Ansible logic as per `CONSTRAINTS.md`.
- Proposals must be purely technical and actionable.
