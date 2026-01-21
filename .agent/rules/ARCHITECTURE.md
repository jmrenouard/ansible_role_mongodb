---
trigger: always_on
---

# ⚙️ EXECUTION RULES & CONSTRAINTS

## 1. Formal Prohibitions (Hard Constraints)

1. **NON-REGRESSION:** Deleting existing code is **prohibited** without relocation or commenting out.
2. **IDEMPOTENCY:** All Ansible tasks MUST be idempotent. Use `changed_when` or `failed_when` for `shell`/`command` modules.
3. **OPERATIONAL SILENCE:** Textual explanations/pedagogy are **proscribed** in the response. Only code blocks, commands, and technical results.
4. **NATIVE MODULES:** Use native Ansible modules over `shell` or `command` whenever possible.

## 2. Output & Restitution Format

1. **NO CHATTER:** No intro or conclusion sentences.
2. **CODE ONLY:** Use Search_block / replace_block format for files > 50 lines.
3. **MANDATORY PROSPECTIVE:** Each intervention must conclude with **3 technical evolution paths** to improve robustness/performance.
4. **MEMORY UPDATE:** Include the JSON MEMORY_UPDATE_PROTOCOL block at the very end.

## 3. Ansible Best Practices

* **Variable Prefixing:** All variables must be prefixed with `mongodb_`.
* **Linting:** `ansible-lint` and `yamllint` must pass before any commit.
* **Handlers:** Use handlers for service restarts instead of inline tasks.

## 4. Test and requirements

* Update `requirements.txt` / `molecule/default/requirements.yml` as needed.
* All changes must be verified via `molecule test`.
* Multi-node scenarios (e.g., `cluster`) must be validated if MongoDB topology is affected.

## 5. Changelog maintenance

* All changes MUST be traced and documented inside @Changelog
