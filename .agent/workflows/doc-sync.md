---
description: doc-sync
---

# Doc Sync

You are a specialized agent for synchronizing documentation with the Ansible role code.

## When to use this workflow

- When the user types `/doc-sync`.
- When they ask to update the documentation after code changes.

## Context

- The project root contains the `roles/mongod` directory.
- Source files are in `roles/mongod/tasks/`, `roles/mongod/defaults/`, `roles/mongod/vars/`, `roles/mongod/handlers/`, and `roles/mongod/templates/`.
- Documentation is primarily in `README.md`.
- Versioning is in `roles/mongod/meta/main.yml`.

## Task

1. **Identify Modified Assets**:
   - Check for changes in `defaults/main.yml` (new variables).
   - Check for changes in `tasks/` (new features or logic behavior).
2. **Update README.md**:
   - Synchronize the "Role Variables" section with `defaults/main.yml`.
   - Ensure all new features are described in the features section.
   - Update examples if task behavior changed.
3. **Version Sync**:
   - Verify that the version in `meta/main.yml` matches the latest entry in `Changelog`.
   - Update `meta/main.yml` if a new version was declared in `Changelog`.
4. **Propose and Apply**:
   - Present a clear diff of the `README.md` or `meta/main.yml` changes.
   - Wait for validation before writing unless the change is trivial and safe.

## Constraints

- Never delete documentation sections without explicit confirmation.
- Respect the existing style (headings, lists, examples).
- Ensure all variables mentioned in `README.md` use the required prefix (`mongodb_`).
