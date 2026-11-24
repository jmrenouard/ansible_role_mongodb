# 🧪 TEST SPECIFICATIONS & ROADMAP

This document outlines the roadmap for expanding the Molecule testing suite to ensure high-density, production-ready MongoDB orchestration.

## Tier 1: Cluster Orchestration (High Priority)

### [IMPLEMENTED] `sharding-ubi9`

**Status**: Implemented in `roles/mongod/molecule/sharding-ubi9/`.

- **Components**: 3 Config Servers (`configsvr`), 6 Shard Nodes (`shardA`, `shardB`), 1 Query Router (`mongos`).
- **Verification**: Verifies `mongod`/`mongos` processes and `sh.status()` shard registration (`shardARS`, `shardBRS`).

### [IMPLEMENTED - CERT CHECKS] `tls-ubi9`

**Status**: Implemented in `roles/mongod/molecule/tls-ubi9/` (generates CA and node certs; live `mongosh --tls` probe is skipped when `mongodb_manage_service: false`).

### [NEW] `rolling-upgrade-ubi9`

**Rationale**: Validate zero-downtime path from MongoDB 5.0 to 6.0.

- **Scenario**: Deploy 5.0 cluster, update `mongodb_version` to 6.0, re-run converge.
- **Verification**: Check feature compatibility version (FCV) and data integrity.
- **Complexity**: Medium
- **Impact**: Operational Continuity

---

## 🔐 Tier 2: Security & Compliance

### 🛂 [NEW] `auth-ldap-enterprise`

**Rationale**: Enterprise environments often require external authentication.

- **Scenario**: Integration with a mock LDAP/OpenLDAP container.
- **Verification**: Validated login with external credentials.
- **Complexity**: High
- **Impact**: Enterprise Compliance

### 💎 [NEW] `encryption-at-rest`

**Rationale**: Security best practice for sensitive data.

- **Scenario**: Enable `security.enableEncryption` with local keyfile or KMIP.
- **Verification**: Check `mongod` logs for encryption activation.
- **Complexity**: Medium
- **Impact**: Data Protection

---

## 📊 Tier 3: Performance & Observability

### 📉 [NEW] `performance-baseline`

**Rationale**: Measure the overhead of TLS and security features.

- **Scenario**: Run `sysbench-mongodb` or similar against the provisioned host.
- **Verification**: Automatic report generation of IOPS/Latency.
- **Complexity**: Low
- **Impact**: Stability

### 🕵️ [NEW] `audit-logging`

**Rationale**: Critical for highly regulated environments.

- **Scenario**: Enable `auditLog` destination to console/file.
- **Verification**: Verify audit events are captured in the specified path.
- **Complexity**: Low
- **Impact**: Compliance

---

## 🛠️ Implementation Strategy

Scenarios will be implemented sequentially following this priority (High -> Low). Each scenario must pass `ansible-lint` and `yamllint`.
