#!/bin/sh
# Sugeneruoja svetainę ir įstumia paruoštus failus į šaką "deploy" (iš jos Hostinger atsisiunčia).
set -e
cd "$(dirname "$0")"
# apsauga: diegti tik tai, kas jau yra šakoje main (kitaip galima nutrinti kito lango darbą)
if [ -z "$SKIP_CHECK" ]; then
  git fetch -q origin main 2>/dev/null || true
  if [ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main 2>/dev/null || echo none)" ]; then echo 'STOP: vietinis HEAD nelygus origin/main. Pirma git pull --rebase ir git push origin HEAD:main.'; exit 1; fi
  if [ -n "$(git status --porcelain | grep -v '^?? dist/' )" ]; then echo 'STOP: yra neįrašytų pakeitimų (git status). Pirma commit ir push į main.'; exit 1; fi
fi
python3 build.py
[ -n "$SKIP_CHECK" ] || python3 check.py || { echo 'Patikra nepavyko: diegimas sustabdytas (SKIP_CHECK=1 apeiti)'; exit 1; }
rm -rf /tmp/arbata-deploy && git worktree prune
git fetch origin deploy 2>/dev/null || true
if git show-ref --verify --quiet refs/remotes/origin/deploy; then git worktree add -B deploy /tmp/arbata-deploy origin/deploy; else git worktree add --detach /tmp/arbata-deploy && (cd /tmp/arbata-deploy && git checkout --orphan deploy && git rm -rf . >/dev/null 2>&1 || true); fi
find /tmp/arbata-deploy -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
cp -a dist/. /tmp/arbata-deploy/
date -u +"%F %H:%M UTC" > /tmp/arbata-deploy/version.txt
cd /tmp/arbata-deploy && git add -A && git commit -m "Deploy $(date -u +%F\ %H:%M)" || echo "Nieko naujo"
git push origin deploy
