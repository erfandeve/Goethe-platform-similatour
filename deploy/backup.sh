#!/usr/bin/env bash
# /usr/local/bin/lexart-backup — nightly database + uploads, kept 7 days.
#   crontab -e →  30 2 * * * /usr/local/bin/lexart-backup
set -euo pipefail
DEST=/root/backup/lexart; STAMP=$(date +%F)
mkdir -p "$DEST"
mongodump --db lexart --archive="$DEST/db-$STAMP.gz" --gzip --quiet
tar -czf "$DEST/media-$STAMP.tar.gz" -C /var/www/lexart/backend media
find "$DEST" -type f -mtime +7 -delete
