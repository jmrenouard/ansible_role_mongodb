# MongoDB Role Parameters

This document provides a comprehensive list of all variables available in the `ansible_role_mongodb` role. All variables are prefixed with `mongodb_` to ensure namespace safety.

## 1. Global & Installation Settings

| Variable | Default | Description |
| :--- | :--- | :--- |
| `mongodb_repo` | `true` | Whether to add the official MongoDB repository and GPG key. |
| `mongodb_version` | `5.0` | Major version of MongoDB to install. |
| `mongodb_edition` | `org` | Edition to install (`org` for Community, `enterprise` for Enterprise). |
| `mongodb_pymongo_version` | `4.7.2` | Version of the `pymongo` Python library to install on the host. |
| `mongodb_state` | `present` | State of the packages (`present`, `latest`). |

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

## 5. Replication & Clustering

| Variable | Default | Description |
| :--- | :--- | :--- |
| `mongodb_replication_role` | `''` | Role of the node in the cluster (`primary`, `secondary`, `arbiter`). |
| `mongodb_replication.replSetName` | `''` | Name of the replica set (required for clustering). |

## 6. Databases and Users

| Variable | Default | Description |
| :--- | :--- | :--- |
| `mongodb_user` | `[]` | List of custom databases and users to create (see README for schema). |

## 7. Backup Settings (mongodump)

| Variable | Default | Description |
| :--- | :--- | :--- |
| `mongodb_backup.enabled` | `true` | Enable automated backups via cron. |
| `mongodb_backup.dbs` | `[admin, config, local]` | List of databases to back up. |
| `mongodb_backup.user` | `backup` | Username for the backup user. |
| `mongodb_backup.pass` | `change_me` | Password for the backup user. |
| `mongodb_backup.path` | `/var/lib/mongodb_backups` | Target directory for backups. |
| `mongodb_backup.retention` | `46` | Retention period in hours. |

## 8. Service Management

| Variable | Default | Description |
| :--- | :--- | :--- |
| `mongodb_restart_config` | `true` | Restart MongoDB automatically after a configuration change. |
| `mongodb_restart_seconds` | `15` | Wait time between restarts in a cluster (rolling restart). |

## 9. Dynamic & Runtime Variables (Internal)

These variables are primarily used internally or set as facts by the role during execution:

- `host_count`: Number of hosts in the current play.
- `mongodb_primary`: Boolean fact set if `mongodb_replication_role` is `primary`.
- `mongodb_secondary`: Boolean fact set if `mongodb_replication_role` is `secondary`.
- `mongodb_arbiter`: Boolean fact set if `mongodb_replication_role` is `arbiter`.
- `mongodb_conf_set`: Registered variable tracking changes to the configuration file.
