#!/usr/bin/env bash
# Build the site for production on THIS machine and stage it in deploy/out/.
#   1. cp deploy/frontend.env.example deploy/frontend.env   (fill in the domain)
#   2. bash deploy/build.sh
# The server never builds: a Next build needs more memory than a small VPS has.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENV_FILE="$ROOT/deploy/frontend.env"
[ -f "$ENV_FILE" ] || { echo "Missing deploy/frontend.env (copy frontend.env.example)"; exit 1; }

set -a; source "$ENV_FILE"; set +a
case "${NEXT_PUBLIC_SITE_URL:-}" in
  https://*) ;;
  *) echo "NEXT_PUBLIC_SITE_URL must be the real https:// domain (it is baked into every canonical link)."; exit 1 ;;
esac

cd "$ROOT/frontend"
# .env.local points at the local backend and would win over the values above.
if [ -f .env.local ]; then mv .env.local .env.local.deploy-bak; trap 'mv .env.local.deploy-bak .env.local' EXIT; fi

npm ci --no-audit --no-fund
npx next build

OUT="$ROOT/deploy/out/web"
rm -rf "$OUT"; mkdir -p "$OUT/.next"
cp -R .next/standalone/. "$OUT/"
cp -R .next/static "$OUT/.next/static"
cp -R public "$OUT/public"

# The browser must never be sent to the local development API.
if grep -rqs "localhost:8010" "$OUT/.next/static"; then
  echo "WARNING: localhost:8010 found in the client bundle — check deploy/frontend.env"
fi
echo "Built for $NEXT_PUBLIC_SITE_URL → deploy/out/web ($(du -sh "$OUT" | cut -f1))"
