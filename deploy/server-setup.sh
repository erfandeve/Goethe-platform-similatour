#!/usr/bin/env bash
# One-time (and safe to re-run) preparation of a fresh Ubuntu server for LexArt.
#   scp deploy/server-setup.sh root@SERVER:/root/ && ssh root@SERVER bash /root/server-setup.sh
# Installs nginx, Node, MongoDB, Python, the firewall and fail2ban, adds swap,
# and lays out /var/www/lexart. It does not touch the site's code or data —
# push.sh uploads the code, seed-db.sh the content.
set -euo pipefail
export DEBIAN_FRONTEND=noninteractive
log() { printf '\n\033[1;36m== %s\033[0m\n' "$*"; }

. /etc/os-release
log "Ubuntu $VERSION_ID ($VERSION_CODENAME), $(nproc) CPU, $(free -m | awk '/Mem/{print $2}') MB RAM"

log "Swap (2 GB) — the API, the site and MongoDB share 2 GB of RAM"
if ! swapon --show | grep -q /swapfile; then
  fallocate -l 2G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile
  grep -q /swapfile /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
  sysctl -w vm.swappiness=10 >/dev/null && echo 'vm.swappiness=10' > /etc/sysctl.d/99-lexart.conf
fi

log "Base packages"
apt-get update -q
apt-get install -y -q nginx certbot python3-certbot-nginx rsync curl gnupg ufw fail2ban \
  python3 python3-venv python3-pip ca-certificates

log "Node.js 20"
if ! command -v node >/dev/null || [ "$(node -p 'process.versions.node.split(".")[0]')" -lt 20 ]; then
  curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && apt-get install -y -q nodejs
fi
node --version

log "MongoDB 7 (listening on 127.0.0.1 only)"
if ! command -v mongod >/dev/null; then
  curl -fsSL https://www.mongodb.org/static/pgp/server-7.0.asc | gpg --dearmor --yes -o /usr/share/keyrings/mongodb-7.gpg
  echo "deb [signed-by=/usr/share/keyrings/mongodb-7.gpg] https://repo.mongodb.org/apt/ubuntu ${VERSION_CODENAME}/mongodb-org/7.0 multiverse" \
    > /etc/apt/sources.list.d/mongodb-org-7.list
  apt-get update -q && apt-get install -y -q mongodb-org || {
    echo "!! MongoDB repository unreachable from this server. Upload the .deb packages and dpkg -i them."; exit 1; }
fi
sed -i 's/^\(\s*bindIp:\).*/\1 127.0.0.1/' /etc/mongod.conf
systemctl enable --now mongod

log "Python for the API"
PY=python3
if ! python3 -c 'import sys; sys.exit(sys.version_info < (3, 11))'; then
  # Older Ubuntu: a standalone 3.13 in a path the service user can read.
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export UV_PYTHON_INSTALL_DIR=/opt/uv-python
  ~/.local/bin/uv python install 3.13 && chmod -R a+rX /opt/uv-python
  PY="$(~/.local/bin/uv python find 3.13)"
fi
mkdir -p /var/www/lexart/{backend,web,deploy}
[ -x /var/www/lexart/backend/.venv/bin/python ] || "$PY" -m venv /var/www/lexart/backend/.venv
/var/www/lexart/backend/.venv/bin/python --version

log "Firewall: SSH, HTTP, HTTPS only (MongoDB and the API stay private)"
ufw allow OpenSSH >/dev/null && ufw allow 'Nginx Full' >/dev/null && ufw --force enable

log "fail2ban for SSH"
cat > /etc/fail2ban/jail.d/lexart.conf <<'EOF'
[sshd]
enabled = true
maxretry = 5
bantime = 1h
EOF
systemctl enable --now fail2ban && systemctl restart fail2ban

log "nginx"
sed -i 's/^\s*#\?\s*server_tokens.*/\tserver_tokens off;/' /etc/nginx/nginx.conf
rm -f /etc/nginx/sites-enabled/default

log "Done. Next: push.sh (code), seed-db.sh (content), then install-services (see DEPLOY.md)."
