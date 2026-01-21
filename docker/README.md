# 🐳 UBI 8.10 Docker Fleet for Ansible Testing

This directory contains a containerized environment based on **Red Hat Universal Base Image 8.10**, designed to test the MongoDB Ansible role in a multi-node topology.

## 🚀 Quick Start

```bash
# Build image, create network, and start 3 nodes
make

# Manage the fleet
make build    # Build the UBI8 image
make network  # Create the internal bridge network (mongo-net)
make run      # Instantiate 3 containers
make stop     # Stop and remove containers
make clean    # Remove containers, network, and image
```

## ⚙️ Infrastructure Details

| Component | Description |
|-----------|-------------|
| **Base Image** | `registry.access.redhat.com/ubi8/ubi:8.10` |
| **Process Manager** | `supervisord` (managing `sshd`) |
| **Network** | `mongo-net` (bridge) |
| **SSH Access** | Root login enabled with `id_rsa` or `rootpass` |

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
