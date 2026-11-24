# Tutorial: Standalone Deployment and Local Docker Lab

> **Learning Goal:** Boot the 3-node UBI 9 Docker test lab, provision `roles/mongod`, and verify `mongod` runs under Supervisor inside containers.
>
> **Environment Warning:** Run this tutorial only against local Docker containers. Never apply preset lab credentials (`something_secure`, `change_me`) to shared infrastructure.

## Prerequisites

Prepare these tools on your workstation before starting:

- Docker Engine running locally with free ports `2221`-`2223` and `27017`-`27019`
- Python 3 with `ansible` and the `community.mongodb` Galaxy collection installed
- `ssh-keygen`, `make`, and `bash` available in your terminal

## Step 1: Generate SSH Keys and Start the Docker Fleet

Create the gitignored SSH key pair expected by `docker/Dockerfile`, build the image, and start the three lab containers:

```bash
cd docker
ssh-keygen -t rsa -N "" -f id_rsa
make build network run
```

Expected output:

```text
docker network create mongo-net
docker run -d --name mongodb-node-1 --network mongo-net -p 2221:22 -p 27017:27017 ...
docker run -d --name mongodb-node-2 --network mongo-net -p 2222:22 -p 27018:27017 ...
docker run -d --name mongodb-node-3 --network mongo-net -p 2223:22 -p 27019:27017 ...
```

## Step 2: Run the Provisioning Script

Deploy `roles/mongod` against `docker/inventory.yml` using `docker/run_install.sh` (pass a non-default backup secret so `assert.yml` passes even without `group_vars`):

```bash
./run_install.sh -e '{"mongodb_backup":{"pass":"lab_backup_secret"}}'
```

`run_install.sh` generates a temporary playbook referencing role `mongod` against `mongodb_cluster`, forwards CLI arguments via `"$@"`, runs `ansible-playbook -v -i inventory.yml`, and removes the temporary playbook when done.

## Step 3: Verify Container Process State

Confirm SSH access and verify that `mongod` started under `supervisord`:

```bash
ssh -i id_rsa -p 2221 -o StrictHostKeyChecking=no root@localhost "supervisorctl status"
```

Expected output:

```text
mongod                           RUNNING   pid 124, uptime 0:00:25
sshd                             RUNNING   pid 8, uptime 0:02:10
```

## Step 4: Inspect Single-Node Behavior with a One-Host Inventory

To test standalone mode (`host_count == 1`), return to the repository root, point `--private-key` at `docker/id_rsa`, limit execution to one host, and override `mongodb_replication_role`, `mongodb_security`, and `mongodb_backup`:

```bash
cd ..
ansible-playbook -i docker/inventory.yml --private-key docker/id_rsa playbooks/install_mongodb.yml \
  --limit mongodb-node-1 -e "mongodb_replication_role=''" -e "mongodb_security=''" \
  -e '{"mongodb_backup":{"pass":"lab_backup_secret"}}'
```

When `host_count | int == 1`, `roles/mongod/tasks/assert.yml` verifies `mongodb_replication_role == ''` and skips `cluster.yml` and `keyfile.yml`.

## Step 5: Clean Up the Lab

Stop containers and delete the temporary bridge network when finished:

```bash
cd docker
make stop clean
```

Expected output:

```text
mongodb-node-1
mongodb-node-2
mongodb-node-3
mongo-net
```

## Next Steps

- Guided cluster and TLS lab: [Three-Node Replica Set and Automated TLS](02-replica-set-and-tls.md)
- Day-2 SOPs in controlled English: [How-To Guides](../02-how-to-guides/index.md)
- Full variable table: [Variables, Playbooks, and Scenarios](../03-reference/variables-playbooks-and-scenarios.md)
- System internals: [Role Architecture and Quorum Design](../04-explanation/role-architecture-and-quorum-design.md)
