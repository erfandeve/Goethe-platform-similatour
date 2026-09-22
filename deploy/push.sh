#!/usr/bin/env bash
# Upload the built site and the API code, then restart both services.
#   SERVER=root@1.2.3.4 bash deploy/push.sh
# Retries on its own: links to Iranian servers drop mid-transfer.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
: "${SERVER:?Set SERVER=user@host}"
[ -d "$ROOT/deploy/out/web" ] || { echo "Run deploy/build.sh first"; exit 1; }

sync() {
  for attempt in 1 2 3 4 5; do
    rsync -az --partial --delete "$@" && return 0
    echo "rsync failed (attempt $attempt), retrying…"; sleep 5
  done
  return 1
}

ssh "$SERVER" 'mkdir -p /var/www/lexart/web /var/www/lexart/backend /var/www/lexart/deploy'
sync "$ROOT/deploy/out/web/" "$SERVER:/var/www/lexart/web/"
sync --exclude out --exclude frontend.env "$ROOT/deploy/" "$SERVER:/var/www/lexart/deploy/"
sync --exclude .venv --exclude media --exclude .env --exclude .cache --exclude __pycache__ \
  "$ROOT/backend/" "$SERVER:/var/www/lexart/backend/"

ssh "$SERVER" 'set -e
  cd /var/www/lexart/backend
  .venv/bin/pip install -q -r requirements.txt
  mkdir -p media
  chown -R www-data:www-data /var/www/lexart
  if ! systemctl list-unit-files lexart-api.service >/dev/null 2>&1; then
    echo "Uploaded. Services are not installed yet — continue with DEPLOY.md step 4."
    exit 0
  fi
  systemctl restart lexart-api lexart-web
  sleep 4
  curl -fsS http://127.0.0.1:8010/api/health/ >/dev/null && echo "API ok"
  curl -fsS -o /dev/null http://127.0.0.1:3000/fa && echo "Web ok"'
