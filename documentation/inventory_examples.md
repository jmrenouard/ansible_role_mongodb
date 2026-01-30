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

## Replica Set PSS + Arbiter

A 4-node configuration (3 data nodes + 1 arbiter) or similar custom topologies.

```ini
[mongodb_primary]
mongo-01.example.com

[mongodb_secondary]
mongo-02.example.com
mongo-03.example.com

[mongodb_arbiter]
mongo-04.example.com

[mongodb_primary:vars]
mongodb_replication_role=primary

[mongodb_secondary:vars]
mongodb_replication_role=secondary

[mongodb_arbiter:vars]
mongodb_replication_role=arbiter
```ini
[mongodb_primary]
mongo-04.example.com
 
[mongodb_secondary]
mongo-05.example.com
mongo-06.example.com
 
[mongodb_arbiter]
mongo-07.example.com
 
[mongodb_primary:vars]
mongodb_replication_role=primary
 
[mongodb_secondary:vars]
mongodb_replication_role=secondary
 
[mongodb_arbiter:vars]
mongodb_replication_role=arbiter
```

---

## Sharded Cluster

Example configuration for a sharded cluster with Config Servers, Shards, and mongos.

```ini
[configsvr]
cs-01.example.com mongodb_sharding_role=configsvr
cs-02.example.com mongodb_sharding_role=configsvr
cs-03.example.com mongodb_sharding_role=configsvr
 
[shardA]
sa-01.example.com mongodb_sharding_role=shardsvr
sa-02.example.com mongodb_sharding_role=shardsvr
sa-03.example.com mongodb_sharding_role=shardsvr
 
[mongos]
router-01.example.com mongodb_sharding_role=mongos
```
