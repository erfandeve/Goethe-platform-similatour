#!/usr/bin/env bash
# Copy the site's CONTENT from this machine's database to the server, then
# make it production-ready. Accounts, orders, attempts and other test activity
# stay behind; only what visitors see is copied.
#   SERVER=root@1.2.3.4 ADMIN_EMAIL=you@x.com ADMIN_PASSWORD='…' bash deploy/seed-db.sh
# Refuses to run if the server database already has users, so it can never
# overwrite a live site.
set -euo pipefail
: "${SERVER:?Set SERVER=user@host}"; : "${ADMIN_EMAIL:?}"; : "${ADMIN_PASSWORD:?}"
SRC_DB="${SRC_DB:-goteh}"
CONTENT="articles categories courses episodes exam_codes exams home_sections instructors lesson_videos parts plans podcasts reviews coupons"

if [ "$(ssh "$SERVER" "mongosh --quiet lexart --eval 'db.users.countDocuments()'")" != "0" ]; then
  echo "The server database already has users — refusing to overwrite a live site."; exit 1
fi

TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
for c in $CONTENT; do mongodump --quiet --db "$SRC_DB" --collection "$c" --out "$TMP"; done
tar -czf "$TMP/content.tgz" -C "$TMP" "$SRC_DB"
scp -q "$TMP/content.tgz" "$SERVER:/tmp/lexart-content.tgz"

ssh "$SERVER" "set -e
  cd /tmp && rm -rf lexart-content && mkdir lexart-content && tar -xzf lexart-content.tgz -C lexart-content
  mongorestore --quiet --drop --nsFrom '$SRC_DB.*' --nsTo 'lexart.*' lexart-content
  rm -rf lexart-content lexart-content.tgz
  cd /var/www/lexart/backend
  sudo -u www-data .venv/bin/python manage.py prepare_production \
    --admin-email '$ADMIN_EMAIL' --admin-password '$ADMIN_PASSWORD'"

# Uploaded media (covers, audio, lesson videos) that the content points at.
rsync -az --partial "$(dirname "$0")/../backend/media/" "$SERVER:/var/www/lexart/backend/media/"
ssh "$SERVER" "chown -R www-data:www-data /var/www/lexart/backend/media"
echo "Content copied and prepared for production."
