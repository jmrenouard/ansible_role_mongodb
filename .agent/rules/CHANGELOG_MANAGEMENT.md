# 📜 STATE MEMORY & HISTORY

## Contextual Consistency Protocols

1. **History Update:** Add new entries to the top of `Changelog` if the action is correct and tested.

2. **Versioning & Sync:**
   - **Mandatory Sync:** The version at the top of `Changelog` MUST match the `version` field in `meta/main.yml`.
   - Increment `meta/main.yml` version after successful action and testing.
   - Use `X.X.Y` format:
     - Increment `Y` for minor actions.
     - Increment `Z` (X.Z.X) for major functions and missing features.

## History Entry Example

1.0 2026-01-21

- Description of the change/fix.
- feat: add parameter to tasks/main.yml
- fix: error solved for deployment on RockyLinux 8.
