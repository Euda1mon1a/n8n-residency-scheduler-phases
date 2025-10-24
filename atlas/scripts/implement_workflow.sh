#!/usr/bin/env bash
set -e
# Guard: ensure JSON exists
[ -f workflows/phase0+1.json ] || echo "{\"name\": \"Phase 0 placeholder\", \"nodes\": [], \"connections\": {}}" > workflows/phase0+1.json
mkdir -p .logs
cp workflows/phase0+1.json ".logs/phase0+1.$(date -u +%Y%m%dT%H%M%SZ).json"
echo "Ready for UI import: workflows/phase0+1.json"
