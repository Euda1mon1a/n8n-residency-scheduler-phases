# n8n Cloud Import Guide

## ✅ Ready for Import

**File to upload:** `scheduler-master-consolidated-v1-FINAL-CLOUD-READY.json` ⭐ **USE THIS ONE**

Previous versions (deprecated):
- ~~`scheduler-master-consolidated-v1-cloud-ready-fixed.json`~~ (old)
- ~~`scheduler-master-consolidated-v1-cloud-ready.json`~~ (old)
- ~~`scheduler-master-consolidated-v1.json`~~ (has credentials)

## What Was Fixed

The original consolidation had several issues that prevented n8n cloud import:

### Issue 1: Hardcoded Credential IDs ❌
```json
"credentials": {
  "airtableTokenApi": {
    "id": "jaswG7byACjIoa6L",
    "name": "Airtable Personal Access Token account 2"
  }
}
```
**Fix:** Removed all credential references. n8n cloud will prompt you to add them after import.

### Issue 2: Invalid Workflow Structure ❌
The consolidated workflow had fields that don't appear in standard n8n exports:
- Top-level `active` field
- Node-level `disabled` field

**Fix:** Restructured to match standard n8n workflow format:
```json
{
  "name": "...",
  "version": 1,
  "description": "...",
  "nodes": [...],
  "connections": {...},
  "settings": {...},
  "staticData": {},
  "meta": {...}
}
```

### Issue 3: Missing `mode` Parameter on Code Nodes ❌ **ROOT CAUSE**
All 28 Code nodes were missing the required `mode` parameter, causing the `toLowerCase` error during import.

**Fix:** Added `"mode": "runOnceForEachItem"` to all Code node parameters:
```json
{
  "type": "n8n-nodes-base.code",
  "parameters": {
    "jsCode": "...",
    "mode": "runOnceForEachItem"  // ← ADDED THIS
  }
}
```

## Import Steps

1. **Open n8n Cloud**
   - Go to your n8n cloud instance
   - Navigate to Workflows

2. **Import Workflow**
   - Click "⋮" menu → "Import from File"
   - Select: `scheduler-master-consolidated-v1-FINAL-CLOUD-READY.json`
   - Click "Import"

3. **Configure Credentials** (After Import)
   n8n will show a credential setup screen for:
   - **Airtable** (30 nodes need this)

   Steps:
   - Click "Create New Credential"
   - Select "Airtable Personal Access Token"
   - Enter your Airtable PAT
   - Save
   - Select this credential for all 30 Airtable nodes

4. **Verify Import**
   - Check that all 100 nodes are present
   - Use the minimap to navigate between phases
   - Each phase is separated by 2000px horizontally

## Workflow Structure

After import, you'll see:

```
ORCHESTRATOR (0px) → PHASE 0 (2000px) → PHASE 1 (4000px) → PHASE 2 (6000px)
    ↓                     ↓                  ↓                  ↓
PHASE 3 (8000px) → PHASE 4 (10000px) → PHASE 6 (12000px) → PHASE 7 (14000px)
    ↓                     ↓
PHASE 8 (16000px) → PHASE 9 (18000px)
```

**Total Canvas Width:** 19,200px
**Nodes:** 100
**Connections:** 111

## Troubleshooting

### If import still fails:

1. **Check n8n cloud version**
   - Ensure you're on the latest version
   - Some older versions may have import bugs

2. **Try the minimal test**
   ```bash
   # Use the minimal test workflow first
   test-minimal.json
   ```
   If this imports successfully, the issue is with the consolidated workflow structure.

3. **Check browser console**
   - Open Developer Tools (F12)
   - Check Console tab for specific error messages
   - Share any error details for further debugging

4. **Alternative: Copy/Paste Method**
   - Open the JSON file
   - Copy entire contents
   - In n8n cloud: ⋮ → "Import from URL or String"
   - Paste and import

## File Versions

| File | Purpose | Status |
|------|---------|--------|
| `scheduler-master-consolidated-v1-FINAL-CLOUD-READY.json` | **Latest - regenerated with all fixes** | ✅ **USE THIS** |
| `scheduler-master-consolidated-v1.json` | Original with local credentials | ❌ Deprecated |
| `scheduler-master-consolidated-v1-cloud-ready.json` | Old - missing mode params | ❌ Deprecated |
| `scheduler-master-consolidated-v1-cloud-ready-fixed.json` | Old - outdated source files | ❌ Deprecated |
| `test-minimal.json` | Minimal test workflow (2 nodes) | ✅ For testing |

## Next Steps After Successful Import

1. **Test the workflow**
   - Click the manual trigger on the orchestrator
   - Check execution logs

2. **Configure Execute Workflow nodes**
   - The 9 "Execute Workflow" nodes reference `{{ $workflow.id }}`
   - This means they'll try to execute the same workflow (recursive)
   - You may want to split these into separate workflows or update the IDs

3. **Update Airtable references**
   - Check that table IDs match your Airtable base
   - Update if necessary

## Support

If you continue to have issues:
1. Share the exact error message from n8n cloud
2. Check browser developer console for JavaScript errors
3. Try importing one of the individual phase files first to isolate the issue
