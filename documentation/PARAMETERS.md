# MongoDB Role Parameters

This document provides a list of variables available in `roles/mongod`. All variables are prefixed with `mongodb_` to ensure namespace safety.

## 1. Global & Installation Settings

| Variable | Default | Description |
| :--- | :--- | :--- |
| `mongodb_repo` | `true` | Whether to add the official MongoDB repository and GPG key. |
| `mongodb_version` | `6.0` | Version of MongoDB to configure (fallback when `mongodb_major_version` is unset). |
| `mongodb_major_version` | `mongodb_version` | Optional major version override for MongoDB repo/GPG key paths. |
| `mongodb_edition` | `org` | Edition to install (`org` for Community, `enterprise` for Enterprise). |
| `mongodb_pymongo_version` | `4.7.2` | Version of the `pymongo` Python library to install on the host. |
| `mongodb_manage_service` | `true` | Manage `mongod`/`mongos` service start and restart tasks (`false` for bare test containers). |
| `mongodb_is_systemd` | Auto-detected | Override systemd detection (`false` activates Supervisor fallback). |

## 2. OS Optimization (Performance)

| Variable | Default | Description |
| :--- | :--- | :--- |
| `mongodb_thp` | `true` | Disable Transparent Huge Pages (THP) as per production notes. |
| `mongodb_numa` | `true` | Enable NUMA support via `numactl` in the systemd service. |

## 3. Authentication (Internal Users)

The role automatically creates three administrative users:

| Variable | Default | Description |
| :--- | :--- | :--- |
| `mongodb_admin_pass` | `change_me` | Password for the `admin` user (root role). |
| `mongodb_adminuser_name` | `adminuser` | Username for the user administrator. |
| `mongodb_adminuser_pass` | `change_me` | Password for the `adminuser` (userAdminAnyDatabase role). |

## 4. MongoDB Configuration (`mongod.conf`)

These variables map directly to the keys in `/etc/mongod.conf`. If set to an empty string (`''`), the section is commented out.

| Variable | Default | Mapping in `mongod.conf` |
| :--- | :--- | :--- |
| `mongodb_net` | `{bindIp: 0.0.0.0, port: 27017}` | `net` |
| `mongodb_systemlog` | `{destination: file, ...}` | `systemLog` |
| `mongodb_storage` | `{dbPath: /var/lib/mongo, ...}` | `storage` |
| `mongodb_processmanagement` | `{fork: true, ...}` | `processManagement` |
| `mongodb_security` | `''` | `security` |
| `mongodb_operationprofiling` | `''` | `operationProfiling` |
| `mongodb_replication` | `''` | `replication` |
| `mongodb_sharding` | `''` | `sharding` |
| `mongodb_auditlog` | `''` | `auditLog` (Enterprise only) |
| `mongodb_snmp` | `''` | `snmp` (Enterprise only) |
| `mongodb_custom_cnf` | `''` | Inject custom top-level keys and values. |

## 5. Replication, Sharding & Clustering

| Variable | Default | Description |
| :--- | :--- | :--- |
| `mongodb_replication_role` | `''` | Role of the node in the cluster (`primary`, `secondary`, `arbiter`). |
| `mongodb_replication.replSetName` | `''` | Name of the replica set (required when `host_count > 1`). |
| `mongodb_priority` | `3`/`2`/`1` | Optional replica set member election priority override per host. |
| `mongodb_sharding_role` | `''` | Sharding component role (`configsvr`, `shardsvr`, `mongos`). |
| `mongodb_sharding_config_members` | `[]` | Replica set member list when `mongodb_sharding_role` is `configsvr`. |
| `mongodb_sharding_shard_members` | `[]` | Replica set member list when `mongodb_sharding_role` is `shardsvr`. |
| `mongodb_sharding_shards` | `[]` | Shards (`{shard, address}`) added by `mongos` router. |

## 6. TLS/SSL Settings

| Variable | Default | Description |
| :--- | :--- | :--- |
| `mongodb_tls_generate_certs` | `false` | Generate a self-signed CA and sign node certificates (`tasks/tls.yml`). |
| `mongodb_tls_dir` | `/etc/ssl/mongodb` | Directory for TLS certificates and keys. |
| `mongodb_tls_ca_cert` | `{{ mongodb_tls_dir }}/mongodb-ca.crt` | CA certificate path. |
| `mongodb_tls_ca_key` | `{{ mongodb_tls_dir }}/mongodb-ca.key` | CA private key path. |
| `mongodb_tls_node_cert` | `{{ mongodb_tls_dir }}/mongodb.pem` | Combined node certificate and private key PEM path. |
| `mongodb_tls_node_key` | `{{ mongodb_tls_dir }}/mongodb.key` | Node private key path. |
| `mongodb_tls_ca_dn` | `/C=FR/ST=Paris/L=Paris/O=MongoDB/CN=MongoDB-CA` | Subject DN metadata reference for the CA certificate. |
| `mongodb_tls_server_dn` | `/C=FR/ST=Paris/L=Paris/O=MongoDB/CN={{ ansible_fqdn }}` | Subject DN metadata reference for server certificates. |
| `mongodb_primary_node` | First play host | Delegate host used for CA signing when generating TLS certs. |
| `mongodb_tls_allow_no_cert` | `true` | Value for `net.tls.allowConnectionsWithoutCertificates`. |

## 7. Databases and Users

| Variable | Default | Description |
| :--- | :--- | :--- |
| `mongodb_user` | `[]` | List of custom databases and users to create (see README for schema). |

## 8. Backup Settings (mongodump)

| Variable | Default | Description |
| :--- | :--- | :--- |
| `mongodb_backup.enabled` | `true` | Enable automated backups via cron. |
| `mongodb_backup.dbs` | `[admin, config, local]` | List of databases to back up. |
| `mongodb_backup.user` | `backup` | Username for the backup user. |
| `mongodb_backup.pass` | `change_me` | Password for the backup user (must be changed from `change_me`). |
| `mongodb_backup.path` | `/var/lib/mongodb_backups` | Target directory for backups. |
| `mongodb_backup.owner` | `mongod` | Owner of `mongodb_backup.path`. |
| `mongodb_backup.group` | `mongod` | Group of `mongodb_backup.path`. |
| `mongodb_backup.mode` | `'0660'` | Permissions mode of `mongodb_backup.path`. |
| `mongodb_backup.hour` | `2` | Cron hour for `mongodump`. |
| `mongodb_backup.minute` | `5` | Cron minute for `mongodump`. |
| `mongodb_backup.day` | `'*'` | Cron day-of-month expression. |
| `mongodb_backup.retention` | `46` | Retention period in hours. |

## 9. Service Management

| Variable | Default | Description |
| :--- | :--- | :--- |
| `mongodb_restart_config` | `true` | Restart MongoDB automatically after a configuration change. |
| `mongodb_restart_seconds` | `15` | Configured wait interval variable (seconds). |

## 10. Dynamic & Runtime Variables (Internal)

These variables are primarily used internally or set as facts by the role during execution:

- `host_count`: Number of hosts in the current play.
- `mongodb_primary`: Boolean fact set if `mongodb_replication_role` is `primary`.
- `mongodb_secondary`: Boolean fact set if `mongodb_replication_role` is `secondary`.
- `mongodb_arbiter`: Boolean fact set if `mongodb_replication_role` is `arbiter`.
- `mongodb_conf_set`: Registered variable tracking changes to the configuration file.
