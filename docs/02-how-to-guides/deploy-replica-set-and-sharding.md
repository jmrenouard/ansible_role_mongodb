# Deploy a Replica Set or Sharded Cluster

Refer to the [Reference Tables](../03-reference/variables-playbooks-and-scenarios.md) before you run this procedure.

## Preconditions

1. Make sure that you have an odd number of target hosts for each replica set.
2. Make sure that TCP port `27017` is open between all target hosts.
3. Set new values for `mongodb_admin_pass`, `mongodb_adminuser_pass`, and `mongodb_backup.pass`.
4. Install the `community.mongodb` collection on the Ansible control host.

## Safety Instructions

**CAUTION:** Do not set `host_count` to an even number for a replica set. An even host count fails preflight checks and breaks election quorum.

## Procedure

### Deploy a Replica Set

1. Set `mongodb_replication.replSetName` and `mongodb_security.keyFile` in shared inventory variables.

2. Set `mongodb_replication_role` to `primary`, `secondary`, or `arbiter` on each host.

3. Check that one host uses `primary` and at most one host uses `arbiter`.

4. Start deployment with this command:

```bash
ansible-playbook -i inventory.ini playbooks/install_mongodb.yml
```

### Deploy a Sharded Cluster

1. Set `mongodb_sharding_role` to `configsvr`, `shardsvr`, or `mongos` for each node group.

2. Define `mongodb_sharding_config_members` on `configsvr` hosts and `mongodb_sharding_shard_members` on `shardsvr` hosts.

3. Define `mongodb_sharding.configDB` and `mongodb_sharding_shards` on `mongos` hosts.

4. Start `playbooks/install_mongodb.yml` against the inventory:

```bash
ansible-playbook -i sharding_inventory.ini playbooks/install_mongodb.yml
```

## Verification Check

1. Connect to the primary node with SSH.

2. Run `mongosh` to inspect the replica set status:

```bash
mongosh --port 27017 -u admin -p '<admin-password>' --authenticationDatabase admin --quiet --eval "rs.status().ok"
```

3. Make sure that the command returns `1`.

4. If `mongodb_sharding_role` includes `mongos`, run `sh.status()` on a router node and check shard names.

## Rollback Procedure

If an error occurs during deployment, do this procedure:

**WARNING:** Stop client connections before you run the reset playbook. `playbooks/reset.yml` deletes all data files in `mongodb_storage.dbPath` and removes MongoDB packages.

1. Run the reset playbook against the target hosts:

```bash
ansible-playbook -i inventory.ini playbooks/reset.yml
```

2. Examine `/etc/mongod.conf` and `/var/lib/mongo` to confirm removal.

## Related Documentation

- Reference: [Variables, Playbooks, and Scenarios](../03-reference/variables-playbooks-and-scenarios.md)
- Explanation: [Role Architecture and Quorum Design](../04-explanation/role-architecture-and-quorum-design.md)
