import json
import sys
from pathlib import Path

def fix_workflow(input_path, output_path):
    print(f"Reading {input_path}...")

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            workflow = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return

    if 'nodes' not in workflow:
        print("Error: Invalid workflow format (missing 'nodes' key)")
        return

    fixed_nodes = []
    node_names = set()

    print(f"Scanning {len(workflow['nodes'])} nodes...")

    for node in workflow['nodes']:
        # 1. Ensure parameters object exists
        if 'parameters' not in node or node['parameters'] is None:
            node['parameters'] = {}
            print(f"  - Fixed missing parameters for node: {node.get('name', 'Unknown')}")

        # 2. Fix Python Code Nodes (Beta compatibility)
        # Newer n8n requires 'language': 'python' if using pythonCode
        if node.get('type') == 'n8n-nodes-base.code':
            params = node['parameters']
            if 'pythonCode' in params and params.get('language') != 'python':
                params['language'] = 'python'
                print(f"  - Added language='python' to node: {node.get('name')}")
            # Ensure mode defaults if missing (common import error)
            if 'mode' not in params:
                params['mode'] = 'runOnceForEachItem'

        # 3. Ensure required string fields exist
        if 'type' not in node:
            print(f"  - WARNING: Node missing 'type': {node}")
            continue # Skip invalid nodes

        # 4. Sanitize position (ensure it's a list of 2 numbers)
        if 'position' not in node:
            node['position'] = [0, 0]

        fixed_nodes.append(node)
        node_names.add(node['name'])

    workflow['nodes'] = fixed_nodes

    # 5. Validate Connections
    # Remove connections that point to non-existent nodes
    if 'connections' in workflow:
        print("Validating connections...")
        clean_connections = {}

        for source_name, outputs in workflow['connections'].items():
            if source_name not in node_names:
                print(f"  - Removing connections from missing node: {source_name}")
                continue

            clean_outputs = {}
            for output_name, connections in outputs.items():
                valid_connections = []
                for conn in connections:
                    if isinstance(conn, list):
                        # Handle array of connections
                        valid_sub_conns = [c for c in conn if c['node'] in node_names]
                        if valid_sub_conns:
                            valid_connections.append(valid_sub_conns)
                    elif conn['node'] in node_names:
                        valid_connections.append(conn)
                    else:
                         print(f"  - Removed dead link to: {conn['node']}")

                if valid_connections:
                    clean_outputs[output_name] = valid_connections

            if clean_outputs:
                clean_connections[source_name] = clean_outputs

        workflow['connections'] = clean_connections

    # Write output
    print(f"Saving fixed workflow to {output_path}...")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(workflow, f, indent=2, ensure_ascii=False)

    print("Done! Try importing the fixed file.")

if __name__ == "__main__":
    input_file = "scheduler-master-consolidated-v1-cloud-ready.json"
    output_file = "scheduler-master-consolidated-v1-cloud-ready-fixed.json"
    fix_workflow(input_file, output_file)
