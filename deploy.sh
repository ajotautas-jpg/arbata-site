#!/bin/sh
# Sugeneruoja svetainę ir įstumia paruoštus failus į šaką "deploy" (iš jos Hostinger atsisiunčia).
set -e
cd "$(dirname "$0")"
python3 build.py
rm -rf /tmp/arbata-deploy && git worktree prune
git fetch origin deploy 2>/dev/null || true
if git show-ref --verify --quiet refs/remotes/origin/deploy; then git worktree add -B deploy /tmp/arbata-deploy origin/deploy; else git worktree add --detach /tmp/arbata-deploy && (cd /tmp/arbata-deploy && git checkout --orphan deploy && git rm -rf . >/dev/null 2>&1 || true); fi
find /tmp/arbata-deploy -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
cp -a dist/. /tmp/arbata-deploy/
cd /tmp/arbata-deploy && git add -A && git commit -m "Deploy $(date -u +%F\ %H:%M)" || echo "Nieko naujo"
git push origin deploy
