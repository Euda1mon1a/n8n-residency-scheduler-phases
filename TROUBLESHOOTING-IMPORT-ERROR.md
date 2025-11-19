# Troubleshooting n8n Cloud Import Error

## Error: "Cannot read properties of undefined (reading 'toLowerCase')"

### Current Status

**File being uploaded:** `scheduler-master-consolidated-v1-cloud-ready-fixed.json`

**Validation Results:**
- ✅ Valid JSON syntax
- ✅ 100 nodes, all with required fields
- ✅ 28 Code nodes (all JavaScript with `mode` parameter)
- ✅ 0 Python nodes
- ✅ No hardcoded credentials
- ✅ All connections valid
- ✅ Proper n8n workflow structure

### Possible Causes & Solutions

#### 1. Browser Cache Issue
**Try:**
```bash
# Clear browser cache or use incognito/private mode
# Hard refresh: Ctrl+Shift+R (Windows/Linux) or Cmd+Shift+R (Mac)
```

#### 2. n8n Cloud Version Compatibility
Some node type versions might not be compatible with your n8n cloud version.

**Try:**
- Check your n8n cloud version (Settings → About)
- Compare with required node versions in the workflow

#### 3. File Upload Method
**Try alternative import methods:**

**Method A: Copy/Paste**
1. Open `scheduler-master-consolidated-v1-cloud-ready-fixed.json`
2. Copy entire contents (Ctrl+A, Ctrl+C)
3. In n8n cloud: Click "⋮" → "Import from URL or String"
4. Paste and import

**Method B: Upload Minimal Test First**
1. Try uploading `test-minimal.json` first (2 nodes only)
2. If that works, the issue is specific to the consolidated workflow
3. If that fails, there's an n8n cloud configuration issue

#### 4. Specific Node Type Issues
The error might be from a specific node type. Let's test with a simplified version.

**Create a version without Airtable nodes:**

```bash
python3 << 'EOF'
import json

with open('scheduler-master-consolidated-v1-cloud-ready-fixed.json') as f:
    workflow = json.load(f)

# Remove Airtable nodes temporarily
workflow['nodes'] = [n for n in workflow['nodes'] if n['type'] != 'n8n-nodes-base.airtable']

# Also remove their connections
valid_node_names = {n['name'] for n in workflow['nodes']}
clean_connections = {}
for source, conns in workflow['connections'].items():
    if source in valid_node_names:
        clean_conns = {}
        for conn_type, conn_arrays in conns.items():
            valid = []
            for arr in conn_arrays:
                filtered = [c for c in arr if c['node'] in valid_node_names]
                if filtered:
                    valid.append(filtered)
            if valid:
                clean_conns[conn_type] = valid
        if clean_conns:
            clean_connections[source] = clean_conns

workflow['connections'] = clean_connections

with open('test-without-airtable.json', 'w', encoding='utf-8') as f:
    json.dump(workflow, f, indent=2, ensure_ascii=False)

print(f"Created test-without-airtable.json with {len(workflow['nodes'])} nodes")
EOF
```

Then try uploading `test-without-airtable.json`.

#### 5. Check Browser Developer Console
**Critical debugging step:**

1. Open browser Developer Tools (F12)
2. Go to Console tab
3. Try importing the workflow
4. Look for the FULL error message

**What to look for:**
- The exact line that mentions `toLowerCase`
- Any stack trace showing which node or property is causing the issue
- Network tab errors (if the upload is failing)

**Share the full error output** - it will show exactly which field is undefined.

#### 6. Direct n8n API Import (Advanced)
If the UI fails, try using n8n's API directly:

```bash
# Get your n8n cloud API key from: Settings → API
export N8N_API_KEY="your-api-key"
export N8N_URL="https://your-instance.app.n8n.cloud"

curl -X POST "$N8N_URL/api/v1/workflows" \
  -H "X-N8N-API-KEY: $N8N_API_KEY" \
  -H "Content-Type: application/json" \
  -d @scheduler-master-consolidated-v1-cloud-ready-fixed.json
```

### Next Steps

Please try the following in order:

1. **Clear browser cache** and try import again
2. **Upload `test-minimal.json`** to verify basic import works
3. **Check browser console** for the full error message
4. **Try copy/paste method** instead of file upload
5. **Share the browser console output** - this will pinpoint the exact issue

### Alternative: Test Individual Phases

If the consolidated workflow continues to fail, try importing individual phase workflows first:

- `phase0-absence-loader.json`
- `phase1-smart-block-pairing.json`
- `phase2-smart-resident-association.json`
- etc.

If individual phases import successfully, the issue is specific to the consolidation process.

### Contact Information

If none of these solutions work, please provide:
1. Full error message from browser console
2. n8n cloud version (Settings → About)
3. Which troubleshooting steps you tried
4. Whether `test-minimal.json` imports successfully
