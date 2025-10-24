#!/usr/bin/env bash
set -euo pipefail

echo "[1/5] Update main"
git fetch origin main || true
git checkout main || true
git pull --ff-only || true

echo "[2/5] Ensure scripts are executable"
chmod +x atlas/scripts/*.sh 2>/dev/null || true

echo "[3/5] Fix Codex config and validate"
if command -v codex >/dev/null 2>&1; then
  ./atlas/scripts/fix_codex_config.sh
else
  echo "codex not installed; running fix script without validation"
  bash ./atlas/scripts/fix_codex_config.sh || true
fi

echo "[4/5] Prepare workflow"
./atlas/scripts/implement_workflow.sh

echo "verify_scaffold complete" > .logs/verify_scaffold.ok || true

echo "[5/5] Commit quick report"
git add -A
git commit -m "Atlas: verify scaffold run" || true
git push || true

echo "Done. Next: import workflows/phase0+1.json in n8n and Run once."
