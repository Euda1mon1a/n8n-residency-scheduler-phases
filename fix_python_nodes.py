import json

input_file = "scheduler-master-consolidated-v1-cloud-ready-fixed.json"
output_file = "scheduler-master-consolidated-v1-cloud-ready-fixed-v2.json"

print(f"Reading {input_file}...")

with open(input_file, 'r', encoding='utf-8') as f:
    workflow = json.load(f)

nodes_fixed = 0

for node in workflow['nodes']:
    # Check if it's a code node
    if node.get('type') == 'n8n-nodes-base.code':
        params = node.get('parameters', {})

        # If it has pythonCode but missing language parameter, fix it
        if 'pythonCode' in params:
            if params.get('language') != 'python':
                params['language'] = 'python'
                nodes_fixed += 1
                print(f"Fixed node: {node.get('name')} (Added language='python')")

print(f"\nTotal nodes fixed: {nodes_fixed}")

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(workflow, f, indent=2, ensure_ascii=False)

print(f"Saved fixed workflow to {output_file}")
