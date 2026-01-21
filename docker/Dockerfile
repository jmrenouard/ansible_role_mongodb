FROM redhat/ubi8:8.10

# Environment variables
ENV TERM=xterm

# Install system utilities, SSH and Python 3.9 (Native on Rocky 9)
RUN dnf install -y --allowerasing \
  openssh-server \
  openssl \
  python3 \
  python3-pip \
  rsync \
  vim-enhanced \
  nano \
  net-tools \
  wget \
  curl \
  git \
  unzip \
  ca-certificates \
  procps-ng && \
  dnf clean all && \
  rm -rf /var/cache/dnf

# Install Supervisor via pip
RUN pip3 install --no-cache-dir supervisor

# Create mongod user and group
RUN groupadd -r mongod && useradd -r -g mongod mongod


# Configure SSH
RUN ssh-keygen -A && \
  echo 'root:rootpass' | chpasswd && \
  sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
  sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
  sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Create directories
RUN mkdir -p /var/run/sshd /var/log/supervisor /etc/supervisor/conf.d /datas

# Copy configuration files
COPY supervisord.conf /etc/supervisord.conf

# SSH Keys installation
RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh
COPY id_rsa.pub /root/.ssh/authorized_keys
COPY id_rsa.pub /root/.ssh/id_rsa.pub
COPY id_rsa /root/.ssh/id_rsa

RUN chmod 600 /root/.ssh/authorized_keys /root/.ssh/id_rsa && \
  chown -R root:root /root/.ssh

# Ports
EXPOSE 22 27017

# Volumes and Workdir
VOLUME ["/datas"]
WORKDIR /datas

# Start via Supervisor
CMD ["/usr/local/bin/supervisord", "-c", "/etc/supervisord.conf"]
