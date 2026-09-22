#!/usr/bin/env bash
# /usr/local/bin/lexart-backup — nightly database + uploads, kept 7 days.
#   crontab:  30 2 * * * /usr/local/bin/lexart-backup
# Lesson videos are left out: they are large, they don't change once
# uploaded, and seven nightly copies of them would fill a 40 GB disk. Keep the
# originals on your own computer (or a download host) instead.
set -euo pipefail
DEST=/root/backup/lexart; STAMP=$(date +%F)
mkdir -p "$DEST"
mongodump --db lexart --archive="$DEST/db-$STAMP.gz" --gzip --quiet
tar -czf "$DEST/media-$STAMP.tar.gz" -C /var/www/lexart/backend \
  --exclude='media/courses/*/videos' media
find "$DEST" -type f -mtime +7 -delete
# Warn in the journal when the disk is getting full.
USED=$(df --output=pcent / | tail -1 | tr -dc '0-9')
[ "$USED" -lt 85 ] || logger -t lexart-backup "Disk ${USED}% full — check /root/backup and uploaded videos"
