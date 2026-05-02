#!/bin/bash
# git-sync.sh — CAS auto-commit & push
# Uso: ./tools/git-sync.sh "mensaje del commit"
# Si no se pasa mensaje, usa uno genérico con timestamp.

cd /data/workspace

MSG="${1:-"chore: auto-sync $(date -u '+%Y-%m-%d %H:%M UTC')"}"

git add -A
git diff --cached --quiet && echo "Nada que commitear." && exit 0
git commit -m "$MSG"
git push origin HEAD
