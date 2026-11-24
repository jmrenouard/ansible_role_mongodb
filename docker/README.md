# UBI 9 Docker Fleet for Ansible Testing

This directory contains a containerized lab based on **Red Hat Universal Base Image 9 (`redhat/ubi9:9.4`)** to test the `roles/mongod` Ansible role in a 3-node topology.

## Prerequisites

SSH keys (`docker/id_rsa` and `docker/id_rsa.pub`) are gitignored. Generate a local lab key pair in `docker/` before running `make build`:

```bash
ssh-keygen -t rsa -N "" -f id_rsa
```

## Quick Start

```bash
# Build image, create network, and start 3 nodes
make

# Manage the fleet
make build    # Build the container image (tagged in Makefile as IMAGE)
make network  # Create the internal bridge network (mongo-net)
make run      # Instantiate 3 containers
make stop     # Stop and remove containers
make clean    # Remove containers, network, and image
```

## Infrastructure Details

| Component | Description |
|-----------|-------------|
| **Base Image** | `redhat/ubi9:9.4` (defined in `docker/Dockerfile`) |
| **Process Manager** | `supervisord` (managing `sshd`) |
| **Network** | `mongo-net` (bridge) |
| **SSH Access** | Root login enabled with generated `id_rsa` or preset `rootpass` |

## 🌐 Port Mapping

| Node | SSH Port (Host) | MongoDB Port (Host) |
|------|-----------------|---------------------|
| `mongodb-node-1` | `2221` | `27017` |
| `mongodb-node-2` | `2222` | `27018` |
| `mongodb-node-3` | `2223` | `27019` |

## 🔐 SSH Connectivity

The environment is pre-configured with a pair of SSH keys. To connect to a node:

```bash
ssh -i id_rsa -p 2221 root@localhost
```

> [!IMPORTANT]
> This environment is intended for **DEVELOPMENT** and **TESTING** only. It uses a preset root password (`rootpass`) and embedded SSH keys.
