#!/bin/bash

# Cleanup script for merged branches
# Run this script to delete all merged remote branches

echo "This will delete the following merged branches from origin:"
echo ""
echo "Recent Claude branches (last 3 days):"
echo "  - claude/standardize-field-mapping-01GaskArxn6s7bQie2bMZRFc"
echo "  - claude/update-phase-field-ids-01VA11Pyv4XyxLtaRBEkaD8E"
echo "  - claude/investigate-merge-append-node-011u7heDpC1gK1unEKMJidPS"
echo "  - claude/fix-phase3-json-01EJr5jRrnjpYs6FA1yUFcNu"
echo "  - claude/review-phases-3-4-01AfT6r9yDjTVuf9RoT82VT5"
echo "  - claude/orchestrator-workflow-phases-018g1NnFH4mmsvhejuGnfhj2"
echo "  - claude/resolve-phase2-merge-019ywLveEmJC13kpL9XLiXSN"
echo "  - claude/fix-n8n-workflow-json-01XVDVVG3wN3PYd9poLWnAWP"
echo ""
echo "Older branches (4 weeks ago):"
echo "  - Euda1mon1a-patch-1"
echo "  - Euda1mon1a-patch-2"
echo "  - phase0-field-id-update"
echo "  - automation/github-cleanup"
echo "  - hardening-ci-logs"
echo "  - atlas-verify-scaffold"
echo "  - atlas-setup"
echo "  - codex-schema-update-2025-10-23"
echo "  - codex/config-2025-10-23"
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push origin --delete \
      claude/standardize-field-mapping-01GaskArxn6s7bQie2bMZRFc \
      claude/update-phase-field-ids-01VA11Pyv4XyxLtaRBEkaD8E \
      claude/investigate-merge-append-node-011u7heDpC1gK1unEKMJidPS \
      claude/fix-phase3-json-01EJr5jRrnjpYs6FA1yUFcNu \
      claude/review-phases-3-4-01AfT6r9yDjTVuf9RoT82VT5 \
      claude/orchestrator-workflow-phases-018g1NnFH4mmsvhejuGnfhj2 \
      claude/resolve-phase2-merge-019ywLveEmJC13kpL9XLiXSN \
      claude/fix-n8n-workflow-json-01XVDVVG3wN3PYd9poLWnAWP \
      Euda1mon1a-patch-1 \
      Euda1mon1a-patch-2 \
      phase0-field-id-update \
      automation/github-cleanup \
      hardening-ci-logs \
      atlas-verify-scaffold \
      atlas-setup \
      codex-schema-update-2025-10-23 \
      codex/config-2025-10-23

    echo ""
    echo "Cleanup complete! Pruning local references..."
    git fetch origin --prune
    echo "Done!"
else
    echo "Cleanup cancelled."
fi
