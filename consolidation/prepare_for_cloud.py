#!/usr/bin/env python3
"""Prepare consolidated workflow for n8n cloud import by removing credential IDs."""
import json
from pathlib import Path

def remove_credential_ids(workflow_data):
    """Remove credential IDs from all nodes to allow n8n cloud to prompt for setup."""
    modified = False

    for node in workflow_data.get('nodes', []):
        if 'credentials' in node:
            # Remove the credentials entirely - n8n will prompt to add them
            del node['credentials']
            modified = True

    return workflow_data, modified

def main():
    input_file = Path('scheduler-master-consolidated-v1.json')
    output_file = Path('scheduler-master-consolidated-v1-cloud-ready.json')

    print('=== PREPARING WORKFLOW FOR N8N CLOUD ===\n')

    # Load workflow
    print(f'Loading: {input_file}')
    with open(input_file, 'r', encoding='utf-8') as f:
        workflow = json.load(f)

    original_node_count = len(workflow.get('nodes', []))
    cred_count = sum(1 for node in workflow['nodes'] if 'credentials' in node)

    print(f'Original workflow: {original_node_count} nodes, {cred_count} with credentials')

    # Remove credential IDs
    workflow, modified = remove_credential_ids(workflow)

    if modified:
        print(f'✅ Removed credentials from {cred_count} nodes')
        print('   (n8n cloud will prompt you to configure them after import)')

    # Save cloud-ready version
    print(f'\nSaving cloud-ready version: {output_file}')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)
        f.write('\n')

    # Validate
    with open(output_file, 'r', encoding='utf-8') as f:
        test = json.load(f)

    remaining_creds = sum(1 for node in test['nodes'] if 'credentials' in node)

    print(f'\n=== VALIDATION ===')
    print(f'✅ Valid JSON: {len(test["nodes"])} nodes')
    print(f'✅ Credentials remaining: {remaining_creds}')
    print(f'✅ File size: {output_file.stat().st_size:,} bytes')

    print(f'\n🎉 SUCCESS!')
    print(f'\n📤 Upload this file to n8n cloud:')
    print(f'   {output_file}')
    print(f'\n💡 After import, n8n will ask you to configure:')
    print(f'   - Airtable credentials (for {cred_count} nodes)')

if __name__ == '__main__':
    main()
