---
trigger: explicit_call
description: Automated audit to enforce project constitution rules
category: governance
---
# Compliance Sentinel (Ansible)

## 🧠 Rationale

High-density development requires automated guardrails to ensure that all changes adhere to the project's architecture, naming conventions, and quality standards.

## 🛠️ Implementation

### 1. Core Check: Variable Prefixing

Ensure all variables in `defaults/`, `vars/`, and `tasks/` are prefixed with `mongodb_`.

```bash
grep -r "[[:space:]]" roles/mongod/{defaults,vars,tasks} | grep -v "mongodb_"
```

### 2. Core Check: Linting Excellence

Verify that the project passes both `ansible-lint` and `yamllint`.

```bash
make lint
```

### 3. Core Check: Idempotency & Robustness

Verify that all `shell` or `command` tasks have `changed_when` or `failed_when` defined, and use native modules where possible.

```bash
grep -rE "shell:|command:" roles/mongod/tasks | xargs grep -L "changed_when:"
```

### 4. Structural Audit (Architecture)

- Verify usage of native Ansible modules over `shell`.
- Identify inline service restarts that should be `handlers`.
- Ensure `meta/main.yml` version matches `Changelog`.

### 5. Changelog Compliance

Verify the format and consistency of the latest Changelog entries.

```bash
head -n 20 Changelog
```

## ✅ Verification

Run `/compliance-sentinel` before any major commit or release.
