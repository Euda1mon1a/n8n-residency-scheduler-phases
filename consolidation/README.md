# n8n Workflow Consolidation Resources

This directory contains resources for creating and deploying a consolidated version of all scheduler phases as a single n8n workflow.

## Contents

### Consolidated Workflow
- **scheduler-master-consolidated-v1-FINAL-CLOUD-READY.json** - A single n8n workflow file that combines all phases (0-9) into one importable workflow, ready for n8n Cloud deployment.

### Documentation
- **N8N-CLOUD-IMPORT-GUIDE.md** - Step-by-step guide for importing workflows into n8n Cloud
- **TROUBLESHOOTING-IMPORT-ERROR.md** - Common import errors and their solutions
- **CONSOLIDATION-README.md** - Detailed explanation of the consolidation approach
- **CONSOLIDATION-SUMMARY.txt** - Summary of the consolidation process

### Python Utilities
- **consolidate_workflows.py** - Script to merge multiple phase workflows into a single consolidated workflow
- **prepare_for_cloud.py** - Prepares workflows for n8n Cloud by removing credentials and fixing compatibility issues
- **fix_python_nodes.py** - Adds `language='python'` parameter to Python Code nodes for cloud compatibility
- **fix_workflow_json.py** - General workflow JSON structure fixes

## Use Cases

### Option 1: Use the Pre-built Consolidated Workflow
If you want to deploy all phases as a single workflow:
1. Import `scheduler-master-consolidated-v1-FINAL-CLOUD-READY.json` into your n8n instance
2. Follow the `N8N-CLOUD-IMPORT-GUIDE.md` for cloud-specific steps
3. Configure your Airtable credentials

### Option 2: Create Your Own Consolidated Workflow
If you want to customize or rebuild the consolidation:
1. Use `consolidate_workflows.py` to merge individual phase workflows
2. Run `prepare_for_cloud.py` to make it cloud-ready
3. Use `fix_python_nodes.py` and `fix_workflow_json.py` as needed

## When to Use Consolidated vs. Modular

**Use Consolidated Workflow When:**
- Deploying to n8n Cloud (easier management)
- You want a single workflow to import/export
- Simpler deployment and backup strategy

**Use Modular Phase Workflows When:**
- Running on self-hosted n8n
- You need to test/debug individual phases
- You want to update phases independently
- The orchestrator pattern is preferred for your use case

## Notes

- The consolidated workflow was extracted from the `claude/consolidate-n8n-workflows-01YUderKwjuaqoTX5ZHqU4n2` branch
- This approach is an alternative to the modular orchestrator pattern used in the main repository
- Both approaches are valid - choose based on your deployment needs

## Source Branch

These files were extracted from branch: `claude/consolidate-n8n-workflows-01YUderKwjuaqoTX5ZHqU4n2`

Created: December 2025
