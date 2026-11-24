# Inventory Examples

This document provides several inventory configurations for different MongoDB topologies.

## Single Instance

### Community Edition

```ini
[mongodb_primary]
mongo-01.example.com mongodb_edition=org mongodb_version=6.0
```

### Enterprise Edition

```ini
[mongodb_primary]
mongo-01.example.com mongodb_edition=enterprise mongodb_version=6.0
```

---

## Replica Set PSA (Primary, Secondary, Arbiter)

A 3-node architecture with one arbiter to ensure quorum without storing a full copy of the data.

```ini
[mongodb_primary]
mongo-01.example.com

[mongodb_secondary]
mongo-02.example.com

[mongodb_arbiter]
mongo-03.example.com

[mongodb_primary:vars]
mongodb_replication_role=primary

[mongodb_secondary:vars]
mongodb_replication_role=secondary

[mongodb_arbiter:vars]
mongodb_replication_role=arbiter
```

---

## Replica Set PSS (Primary, Secondary, Secondary)

### 3-Node Cluster

Standard 3-node cluster with full data replication on all nodes.

```ini
[mongodb_primary]
mongo-01.example.com

[mongodb_secondary]
mongo-02.example.com
mongo-03.example.com

[mongodb_primary:vars]
mongodb_replication_role=primary

[mongodb_secondary:vars]
mongodb_replication_role=secondary
```

### 5-Node Cluster

Highly available 5-node cluster with 4 secondary nodes.

```ini
[mongodb_primary]
mongo-01.example.com

[mongodb_secondary]
mongo-02.example.com
mongo-03.example.com
mongo-04.example.com
mongo-05.example.com

[mongodb_primary:vars]
mongodb_replication_role=primary

[mongodb_secondary:vars]
mongodb_replication_role=secondary
```

---

## Odd-Node Quorum Requirement & Custom 5-Node PSA Topology

> [!IMPORTANT]
> `roles/mongod/tasks/assert.yml` enforces `host_count | int % 2 != 0` when deploying a replica set. Even-numbered plays (such as 2 or 4 hosts) fail assertion checks to preserve election quorum.

Example 5-node PSA cluster (1 primary, 3 data secondaries, 1 arbiter):

```ini
[mongodb_primary]
mongo-01.example.com

[mongodb_secondary]
mongo-02.example.com
mongo-03.example.com
mongo-04.example.com

[mongodb_arbiter]
mongo-05.example.com

[mongodb_primary:vars]
mongodb_replication_role=primary

[mongodb_secondary:vars]
mongodb_replication_role=secondary

[mongodb_arbiter:vars]
mongodb_replication_role=arbiter
```

---

## Sharded Cluster

Example configuration for a sharded cluster with Config Servers, Shards, and `mongos` (matching `roles/mongod/molecule/sharding-ubi9/`):

```ini
[configsvr]
cs-01.example.com mongodb_sharding_role=configsvr mongodb_replication_role=primary
cs-02.example.com mongodb_sharding_role=configsvr mongodb_replication_role=secondary
cs-03.example.com mongodb_sharding_role=configsvr mongodb_replication_role=secondary

[shardA]
sa-01.example.com mongodb_sharding_role=shardsvr mongodb_replication_role=primary
sa-02.example.com mongodb_sharding_role=shardsvr mongodb_replication_role=secondary
sa-03.example.com mongodb_sharding_role=shardsvr mongodb_replication_role=secondary

[mongos]
router-01.example.com mongodb_sharding_role=mongos
```
