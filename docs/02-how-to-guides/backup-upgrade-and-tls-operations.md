# Operate Backups, Staged Upgrades, and TLS

Refer to the [Reference Tables](../03-reference/variables-playbooks-and-scenarios.md) before you run this procedure.

## Preconditions

1. Make sure that you have root SSH access to all cluster hosts.
2. Make sure that `mongodb_admin_pass` and `mongodb_backup.pass` are correct in inventory variables.
3. Make sure that `mongodb_net.port` is reachable from the control host and between cluster nodes.

## Safety Instructions

**WARNING:** Back up cluster data and pause client writes before you start `playbooks/update.yml`. Active writes during node restarts can cause data loss.

## Procedure

### Enable and Check Backups

1. Set `mongodb_backup.enabled` to `true` and set a strong `mongodb_backup.pass` value.

2. Run `playbooks/install_mongodb.yml` to install the cron job on the first secondary node.

3. Connect to the first secondary host and list cron jobs:

```bash
crontab -l
```

4. Examine `/var/lib/mongodb_backups/latest` to confirm the backup directory link exists.

### Run a Staged Patch Upgrade

1. Set `mongodb_version` and `mongodb_edition` in inventory variables.

2. Verify that `mongodb_replication_role` is set for `primary`, `secondary`, and `arbiter` hosts.

3. Start the staged update playbook:

```bash
ansible-playbook -i inventory.ini playbooks/update.yml
```

4. Monitor playbook output as nodes upgrade in order: arbiter, secondaries, then primary.

### Enable Generated TLS Certificates

1. Set `mongodb_tls_generate_certs` to `true` in shared variables.

2. Do not set a duplicate `mongodb_net.tls` block when `mongodb_tls_generate_certs` is `true`.

3. Run `playbooks/install_mongodb.yml` to create `/etc/ssl/mongodb/mongodb-ca.crt` and `/etc/ssl/mongodb/mongodb.pem`.

**NOTE:** The template `mongod.conf.j2` writes a `tls` section automatically when `mongodb_tls_generate_certs` is `true`.

## Verification Check

1. Check cluster health with `mongosh`:

```bash
mongosh --port 27017 -u admin -p '<admin-password>' --authenticationDatabase admin --quiet --eval "db.hello().isWritablePrimary"
```

2. Make sure that the command returns `true` on the primary host.

3. If TLS is active, test connection with `--tls` and `--tlsCAFile /etc/ssl/mongodb/mongodb-ca.crt`.

## Rollback Procedure

If an upgrade or TLS change fails, do this procedure:

1. Restore the previous package version on the failed node with `dnf downgrade`.

2. Restore the previous `/etc/mongod.conf` file from your configuration backup.

3. Restart `mongod` on the host:

```bash
systemctl restart mongod
```

4. Examine `/var/log/mongodb/mongod.log` and confirm `db.hello()` passes on the primary node.

## Related Documentation

- Reference: [Variables, Playbooks, and Scenarios](../03-reference/variables-playbooks-and-scenarios.md)
- Explanation: [Role Architecture and Quorum Design](../04-explanation/role-architecture-and-quorum-design.md)
