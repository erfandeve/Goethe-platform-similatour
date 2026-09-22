#!/usr/bin/env bash
# /usr/local/bin/lexora-backup — nightly database + uploads, kept 7 days.
#   crontab -e →  30 2 * * * /usr/local/bin/lexora-backup
set -euo pipefail
DEST=/root/backup/lexora; STAMP=$(date +%F)
mkdir -p "$DEST"
mongodump --db lexora --archive="$DEST/db-$STAMP.gz" --gzip --quiet
tar -czf "$DEST/media-$STAMP.tar.gz" -C /var/www/lexora/backend media
find "$DEST" -type f -mtime +7 -delete
