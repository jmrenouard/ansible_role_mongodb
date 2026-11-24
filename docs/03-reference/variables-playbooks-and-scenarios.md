# Variables, Playbooks, and Scenarios

Reference tables for `roles/mongod/defaults/main.yml`, `playbooks/`, `Makefile` targets, and `roles/mongod/molecule/`.

## Role Defaults (`roles/mongod/defaults/main.yml`)

### Installation, OS Tuning, and Credentials

| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `mongodb_repo` | `true` | Configure official MongoDB RPM repo and GPG key |
| `mongodb_version` | `6.0` | Target MongoDB version |
| `mongodb_edition` | `org` | Package edition (`org` or `enterprise`) |
| `mongodb_pymongo_version` | `4.7.2` | `pymongo` Python package version installed via `pip3` |
| `mongodb_thp` | `true` | Disable Transparent Huge Pages on non-container hosts |
| `mongodb_numa` | `true` | Enable NUMA memory interleaving and `vm.zone_reclaim_mode` |
| `mongodb_admin_pass` | `"change_me"` | Password for `admin` (`root` role); must be changed |
| `mongodb_adminuser_name` | `adminuser` | Name of the user-management admin account |
| `mongodb_adminuser_pass` | `"change_me"` | Password for `mongodb_adminuser_name`; must be changed |

### Configuration, Replication, Sharding, and TLS

| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `mongodb_net` | `{bindIp: 0.0.0.0, port: 27017}` | Network bind IP and TCP port in `mongod.conf` |
| `mongodb_systemlog` | `{destination: file, logAppend: true, path: /var/log/mongodb/mongod.log}` | `systemLog` dictionary in `mongod.conf` |
| `mongodb_storage` | `{dbPath: /var/lib/mongo, journal: {enabled: true}}` | `storage` dictionary (`journal` stripped above 6.0) |
| `mongodb_processmanagement` | `{fork: true, pidFilePath: /var/run/mongodb/mongod.pid, timeZoneInfo: /usr/share/zoneinfo}` | `processManagement` settings |
| `mongodb_security` | `""` | Security dictionary (`authorization`, `keyFile`, KMIP) |
| `mongodb_operationprofiling` | `""` | Optional `operationProfiling` dictionary |
| `mongodb_replication` | `""` | Replication settings (`replSetName`) |
| `mongodb_replication_role` | `""` | Node role: `primary`, `secondary`, or `arbiter` |
| `mongodb_sharding` | `""` | Optional `sharding` dictionary in `mongod.conf` |
| `mongodb_sharding_role` | `""` | Sharding component: `configsvr`, `shardsvr`, or `mongos` |
| `mongodb_sharding_config_members` | `[]` | Member dicts for `configsvr` initialization |
| `mongodb_sharding_shard_members` | `[]` | Member dicts for `shardsvr` initialization |
| `mongodb_sharding_shards` | `[]` | `{shard, address}` entries registered on `mongos` |
| `mongodb_auditlog` | `""` | Enterprise `auditLog` dictionary |
| `mongodb_snmp` | `""` | Enterprise `snmp` dictionary |
| `mongodb_custom_cnf` | `""` | Custom top-level keys appended to `mongod.conf` |
| `mongodb_tls_generate_certs` | `false` | Generate self-signed CA and signed node certificates |
| `mongodb_tls_dir` | `/etc/ssl/mongodb` | Directory storing generated TLS assets |
| `mongodb_tls_ca_cert` | `{{ mongodb_tls_dir }}/mongodb-ca.crt` | CA certificate path |
| `mongodb_tls_ca_key` | `{{ mongodb_tls_dir }}/mongodb-ca.key` | CA private key path |
| `mongodb_tls_node_cert` | `{{ mongodb_tls_dir }}/mongodb.pem` | Combined node certificate and private key PEM path |
| `mongodb_tls_node_key` | `{{ mongodb_tls_dir }}/mongodb.key` | Node private key path |
| `mongodb_tls_ca_dn` | `/C=FR/ST=Paris/L=Paris/O=MongoDB/CN=MongoDB-CA` | CA certificate distinguished name metadata |
| `mongodb_tls_server_dn` | `/C=FR/ST=Paris/L=Paris/O=MongoDB/CN={{ ansible_fqdn }}` | Node certificate distinguished name metadata |

### Users, Backups, and Service Controls

| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `mongodb_user` | `[]` | Custom database users created by `tasks/user.yml` |
| `mongodb_backup.enabled` | `true` | Enable daily `mongodump` cron on standalone or first secondary |
| `mongodb_backup.dbs` | `[admin, config, local]` | Databases dumped by cron |
| `mongodb_backup.user` | `backup` | Backup account username |
| `mongodb_backup.pass` | `change_me` | Backup account password (must be changed) |
| `mongodb_backup.path` | `/var/lib/mongodb_backups` | Backup destination directory |
| `mongodb_backup.owner` | `mongod` | Directory owner |
| `mongodb_backup.group` | `mongod` | Directory group |
| `mongodb_backup.mode` | `"0660"` | Directory permissions |
| `mongodb_backup.hour` | `2` | Cron hour |
| `mongodb_backup.minute` | `5` | Cron minute |
| `mongodb_backup.day` | `"*"` | Cron day-of-month |
| `mongodb_backup.retention` | `46` | Retention period in hours |
| `mongodb_restart_config` | `true` | Restart `mongod` when `/etc/mongod.conf` changes |
| `mongodb_restart_seconds` | `15` | Configured interval variable between restarts |

## Playbooks (`playbooks/`)

| Playbook | Target Hosts | Purpose |
| :--- | :--- | :--- |
| `playbooks/install_mongodb.yml` | `all` | Execute `roles/mongod` for standalone or replica set deployment |
| `playbooks/update.yml` | `one_host`, `mongodb_arbiter`, `mongodb_primary`, `mongodb_secondary` | Rolling patch upgrade (`dnf state: latest`, arbiter -> secondary -> primary step-down) |
| `playbooks/reset.yml` | `all` | Remove MongoDB packages, keys, `/etc/mongod.conf`, `/var/lib/mongo`, `/var/log/mongodb`, cron jobs |
| `playbooks/scale.yml` | `all` | Experimental debug placeholder documenting planned scaling flow |

## Makefile Targets

### Root `Makefile`

| Target | Command Behavior |
| :--- | :--- |
| `make help` | Print available targets |
| `make lint` | Run `$(BIN)/ansible-lint roles/mongod playbooks/*.yml` and `$(BIN)/yamllint .` |
| `make molecule` | Run `cd roles/mongod && ../../$(BIN)/molecule $(MOLECULE_OPTS)` (`MOLECULE_OPTS?=test --all`) |
| `make test` | Run `lint` followed by `molecule` |
| `make clean` | Delete `venv/`, `.molecule/`, `*.pyc`, and `__pycache__/` |

### Docker Lab `docker/Makefile`

| Target | Command Behavior |
| :--- | :--- |
| `make all` | Execute `build`, `network`, and `run` |
| `make build` | Build image from `docker/Dockerfile` (`redhat/ubi9:9.4`) |
| `make network` | Create Docker bridge network `mongo-net` |
| `make run` | Start `mongodb-node-1` (`2221`/`27017`), `mongodb-node-2` (`2222`/`27018`), `mongodb-node-3` (`2223`/`27019`) |
| `make provision` | Execute `./run_install.sh` against `docker/inventory.yml` |
| `make deploy` | Run `all` followed by `provision` |
| `make stop` | Stop and remove all three lab containers |
| `make clean` | Run `stop`, then remove `mongo-net` and image |
| `make rebuild` | Run `clean`, `ssh-clean`, and `all` |
| `make scratch` | Run `clean`, `all`, and `provision` |
| `make ssh-clean` | Remove cached localhost ports `2221`-`2223` from `~/.ssh/known_hosts` |
| `make logs` | Follow container logs on `mongodb-node-1` |

## Molecule Scenarios (`roles/mongod/molecule/`)

| Scenario | Image Base | Instances | Service Mode | Verification Scope |
| :--- | :--- | :--- | :--- | :--- |
| `default` | `ubi9/ubi-init:latest` | `1` (`test-multi-01`) | `mongodb_manage_service: false`, `mongodb_is_systemd: false` | Process, port `27017`, `/etc/mongod.conf`, `/var/lib/mongo`, `ping` |
| `default-ubi8` | `ubi8/ubi:latest` | `1` (`test-ubi8-01-v2`) | `/usr/sbin/init` (`systemd`) | Stub (`assert: that: true`) |
| `replicaset-psa-ubi8` | `ubi8/ubi:latest` + `docker-ubi8-ansible` | `3` (`test-ubi8-01-v2`..`03-v2`) | `/usr/sbin/init` (`systemd`) | Stub (`assert: that: true`) |
| `replicaset-psa-ubi9` | `ubi9/ubi:latest` | `3` (`test-multi-01`..`03`) | No systemd (`tail -f /dev/null`) | Stub (`assert: that: true`) |
| `replicaset-pss-ubi8` | `ubi8/ubi:latest` + `docker-ubi8-ansible` | `5` (`replica-ubi8-01`..`05`) | `/usr/sbin/init` (`systemd`) | Stub (`assert: that: true`) |
| `replicaset-pss-ubi9` | `ubi9/ubi:latest` | `5` (`replica-ubi9-01`..`05`) | No systemd (`tail -f /dev/null`) | Stub (`assert: that: true`) |
| `sharding-ubi9` | `ubi9/ubi:latest` | `10` (`cs-1..3`, `sA-1..3`, `sB-1..3`, `router-1`) | `mongodb_manage_service: false` | Process check and `mongosh --eval 'sh.status()'` |
| `tls-ubi9` | `ubi9/ubi:latest` | `1` (`test-tls-01`) | `mongodb_manage_service: false`, `mongodb_is_systemd: true` | Cert files exist; `mongosh --tls` gated by `mongodb_manage_service` |
