#!/usr/bin/env sh
# Container entrypoint. A fresh database seeds itself so a new deployment is
# browsable without opening a shell; an already-seeded one is left alone.
set -e

python manage.py bootstrap --if-empty || echo "Seeding skipped (database not reachable yet)."

exec gunicorn config.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers "${WEB_CONCURRENCY:-2}" \
  --timeout 180
