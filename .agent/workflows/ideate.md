---
description: ideate
---

# Ideation Workflow

This workflow analyzes the Ansible role structure, Molecule test results, and objectives to suggest actionable improvements and new features for MongoDB orchestration.

## When to use this workflow

- When the user types `/ideate`.
- When the project reaches a milestone and needs fresh directions.

## Task

1. **Analyze Current Role State**:
   - Review `OBJECTIVES.md` and `ARCHITECTURE.md`.
   - Check `defaults/main.yml` for missing MongoDB configuration parameters (e.g., storage engine tuning, audit logs).
   - Scan `molecule/` for scenarios not yet implemented (e.g., Sharding, specific TLS configurations).

2. **Generate 3 to 4 technical evolution paths**:
   - One focusing on **Cluster Management** (e.g., Zero-downtime rolling upgrades, Sharded cluster orchestration).
   - One focusing on **Security & Compliance** (e.g., LDAP/Active Directory integration, advanced encryption at rest).
   - One focusing on **Testing & CI/CD** (e.g., Chaos testing for replica sets, GitHub Actions optimization for multi-scenario runs).
   - One focusing on **Observability** (e.g., MongoDB Exporter integration, custom health check tasks).

3. **Present ideas with**:
   - **Title**: A clear name for the feature.
   - **Rationale**: Why it matters for a high-quality MongoDB role.
   - **Complexity**: Low/Medium/High.
   - **Impact**: Expected benefit (Performance, Scalability, Security).

## Constraints

- Suggestions must respect `CONSTRAINTS.md` (Ansible-native focus, MongoDB-centric).
- Avoid generic advice; link to specific tasks or variables in the repo.
