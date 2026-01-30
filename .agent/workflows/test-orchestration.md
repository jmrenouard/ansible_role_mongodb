---
trigger: explicit_call
description: Unified orchestration for Molecule tests and project validation
category: tool
---

# Test Orchestration

This workflow centralizes test execution for the Ansible role. It supports both full sweeps and specific scenario validation.

## 🧠 Rationale

Redundant test scripts lead to fragmentation. Using a unified orchestration layer via the root `Makefile` ensures consistent environment setup and cleanup.

## 🛠️ Implementation

### 1. Scenario Discovery

List all available Molecule scenarios to identify the target.

```bash
make molecule MOLECULE_OPTS="list"
```

### 2. Full Validation Sweep

Run linting followed by all Molecule scenarios.

```bash
make test
```

### 3. Target Specific Scenario

Run a specific scenario (e.g., `default`, `replicaset-psa-ubi9`) with auto-cleanup.

```bash
make molecule MOLECULE_OPTS="test -s default --destroy=always"
```

## ✅ Verification

- Ensure all `molecule` commands are executed within the project virtual environment.
- Verify that `make lint` passes before starting long-running `molecule` tests.
- Check that Docker containers are removed after completion.
