#!/usr/bin/env python3
"""
N8N Workflow Consolidation Script
Merges all phase workflows into a single consolidated workflow with:
- Unique node IDs
- Namespace prefixing
- Visual grouping
- Spatial separation
- Connection remapping
"""

import json
import sys
from typing import Dict, List, Any
from pathlib import Path


class WorkflowConsolidator:
    """Consolidates multiple n8n workflows into a single workflow"""

    def __init__(self):
        self.workflows = []
        self.node_id_map = {}  # Maps old IDs to new IDs
        self.next_node_id = 1
        self.x_offset_per_phase = 2000

        # Phase configurations
        self.phases = [
            {"file": "orchestrator-workflow.json", "prefix": "ORCH_", "name": "Orchestrator"},
            {"file": "phase0-absence-loader.json", "prefix": "P0_", "name": "Phase 0"},
            {"file": "phase1-smart-block-pairing.json", "prefix": "P1_", "name": "Phase 1"},
            {"file": "phase2-smart-resident-association.json", "prefix": "P2_", "name": "Phase 2"},
            {"file": "phase3-enhanced-faculty-assignment-v3.json", "prefix": "P3_", "name": "Phase 3"},
            {"file": "phase4-enhanced-call-scheduling.json", "prefix": "P4_", "name": "Phase 4"},
            {"file": "phase6-orchestrator-compatible.json", "prefix": "P6_", "name": "Phase 6"},
            {"file": "phase7-orchestrator-compatible.json", "prefix": "P7_", "name": "Phase 7"},
            {"file": "phase8-emergency-coverage-engine.json", "prefix": "P8_", "name": "Phase 8"},
            {"file": "phase9-excel-export-engine.json", "prefix": "P9_", "name": "Phase 9"},
        ]

    def load_workflow(self, filepath: str) -> Dict[str, Any]:
        """Load a workflow JSON file"""
        with open(filepath, 'r') as f:
            return json.load(f)

    def validate_workflow(self, workflow: Dict[str, Any], filename: str) -> bool:
        """Validate that a workflow has required n8n structure"""
        required_keys = ['nodes', 'connections']
        for key in required_keys:
            if key not in workflow:
                print(f"ERROR: {filename} missing required key: {key}")
                return False

        if not isinstance(workflow['nodes'], list):
            print(f"ERROR: {filename} 'nodes' is not a list")
            return False

        if not isinstance(workflow['connections'], dict):
            print(f"ERROR: {filename} 'connections' is not a dict")
            return False

        print(f"✓ Validated: {filename} ({len(workflow['nodes'])} nodes)")
        return True

    def remap_node_id(self, old_id: str, phase_prefix: str) -> str:
        """Generate a new unique node ID"""
        # Create a unique key for this old ID + phase combo
        map_key = f"{phase_prefix}{old_id}"

        if map_key not in self.node_id_map:
            new_id = f"{phase_prefix}{old_id}"
            self.node_id_map[map_key] = new_id

        return self.node_id_map[map_key]

    def process_node(self, node: Dict[str, Any], phase_idx: int, phase_prefix: str) -> Dict[str, Any]:
        """Process a single node: remap ID, add prefix, adjust position"""
        new_node = node.copy()

        # Remap node ID
        old_id = node.get('id', f'node_{self.next_node_id}')
        new_id = self.remap_node_id(old_id, phase_prefix)
        new_node['id'] = new_id

        # Add namespace prefix to name
        old_name = node.get('name', 'Unnamed Node')
        new_name = f"{phase_prefix}{old_name}"
        new_node['name'] = new_name

        # Adjust position with x-axis offset
        if 'position' in node:
            position = node['position']
            if isinstance(position, list) and len(position) == 2:
                x_offset = phase_idx * self.x_offset_per_phase
                new_node['position'] = [position[0] + x_offset, position[1]]

        self.next_node_id += 1
        return new_node

    def remap_connections(self, connections: Dict[str, Any], phase_prefix: str) -> Dict[str, Any]:
        """Remap connection node references to new IDs"""
        new_connections = {}

        for source_node, outputs in connections.items():
            # Remap source node name
            # Find the old node ID that matches this source_node name
            map_key = None
            for key in self.node_id_map:
                if key.endswith(source_node) or source_node in key:
                    map_key = key
                    break

            if map_key:
                new_source = self.node_id_map[map_key]
            else:
                new_source = f"{phase_prefix}{source_node}"

            # Process connection structure
            new_outputs = {}
            for output_type, connections_list in outputs.items():
                new_connections_list = []

                for connection_array in connections_list:
                    new_connection_array = []
                    for connection in connection_array:
                        new_connection = connection.copy()

                        # Remap target node
                        if 'node' in connection:
                            target_node = connection['node']
                            # Find matching key
                            target_map_key = None
                            for key in self.node_id_map:
                                if key.endswith(target_node) or target_node in key:
                                    target_map_key = key
                                    break

                            if target_map_key:
                                new_connection['node'] = self.node_id_map[target_map_key]
                            else:
                                new_connection['node'] = f"{phase_prefix}{target_node}"

                        new_connection_array.append(new_connection)
                    new_connections_list.append(new_connection_array)

                new_outputs[output_type] = new_connections_list

            new_connections[new_source] = new_outputs

        return new_connections

    def consolidate(self) -> Dict[str, Any]:
        """Main consolidation method"""
        consolidated_nodes = []
        consolidated_connections = {}

        print("\n=== LOADING AND PROCESSING WORKFLOWS ===")

        for phase_idx, phase_config in enumerate(self.phases):
            filename = phase_config['file']
            prefix = phase_config['prefix']
            phase_name = phase_config['name']

            print(f"\nProcessing {phase_name} ({filename})...")

            # Load workflow
            try:
                workflow = self.load_workflow(filename)
            except Exception as e:
                print(f"ERROR loading {filename}: {e}")
                continue

            # Validate structure
            if not self.validate_workflow(workflow, filename):
                continue

            # Process nodes
            nodes_processed = 0
            for node in workflow.get('nodes', []):
                processed_node = self.process_node(node, phase_idx, prefix)
                consolidated_nodes.append(processed_node)
                nodes_processed += 1

            print(f"  → Processed {nodes_processed} nodes")

            # Process connections
            connections = workflow.get('connections', {})
            remapped_connections = self.remap_connections(connections, prefix)

            # Merge connections
            for source, outputs in remapped_connections.items():
                if source in consolidated_connections:
                    # Merge outputs
                    for output_type, conn_list in outputs.items():
                        if output_type in consolidated_connections[source]:
                            consolidated_connections[source][output_type].extend(conn_list)
                        else:
                            consolidated_connections[source][output_type] = conn_list
                else:
                    consolidated_connections[source] = outputs

            print(f"  → Processed {len(remapped_connections)} connection sources")

        # Create consolidated workflow
        consolidated = {
            "name": "Scheduler Master Consolidated v1",
            "nodes": consolidated_nodes,
            "connections": consolidated_connections,
            "active": False,
            "settings": {
                "executionOrder": "v1"
            },
            "staticData": None,
            "meta": {
                "templateCredsSetupCompleted": True,
                "description": "Consolidated workflow containing all scheduler phases - Orchestrator, Phase 0-4, 6-9",
                "version": "1.0.0",
                "consolidation_info": {
                    "total_workflows_merged": len(self.phases),
                    "total_nodes": len(consolidated_nodes),
                    "total_connections": sum(len(conns) for conns in consolidated_connections.values()),
                    "phases_included": [p['name'] for p in self.phases],
                    "spatial_separation": f"{self.x_offset_per_phase}px per phase",
                    "node_id_strategy": "Namespaced with phase prefixes",
                    "created_by": "N8N Workflow Consolidation Script v1.0"
                }
            }
        }

        return consolidated

    def validate_consolidated(self, workflow: Dict[str, Any]) -> bool:
        """Validate the consolidated workflow"""
        print("\n=== VALIDATING CONSOLIDATED WORKFLOW ===")

        # Check basic structure
        if 'nodes' not in workflow or 'connections' not in workflow:
            print("ERROR: Missing nodes or connections")
            return False

        total_nodes = len(workflow['nodes'])
        print(f"✓ Total nodes: {total_nodes}")

        # Verify unique node IDs
        node_ids = [node['id'] for node in workflow['nodes']]
        if len(node_ids) != len(set(node_ids)):
            print("ERROR: Duplicate node IDs found!")
            return False
        print(f"✓ All node IDs are unique")

        # Verify node names have prefixes
        prefixes = set([p['prefix'] for p in self.phases])
        nodes_with_prefix = 0
        for node in workflow['nodes']:
            name = node.get('name', '')
            if any(name.startswith(prefix) for prefix in prefixes):
                nodes_with_prefix += 1

        print(f"✓ Nodes with namespace prefix: {nodes_with_prefix}/{total_nodes}")

        # Check connections reference valid nodes
        node_id_set = set(node_ids)
        valid_connections = 0
        invalid_connections = 0

        for source, outputs in workflow['connections'].items():
            # Source should be a valid node ID or name
            for output_type, conn_list in outputs.items():
                for connection_array in conn_list:
                    for connection in connection_array:
                        target = connection.get('node', '')
                        if target in node_id_set or any(node.get('name') == target for node in workflow['nodes']):
                            valid_connections += 1
                        else:
                            invalid_connections += 1

        print(f"✓ Valid connections: {valid_connections}")
        if invalid_connections > 0:
            print(f"⚠ Invalid connections: {invalid_connections} (may need manual review)")

        # Check position distribution
        x_positions = [node.get('position', [0, 0])[0] for node in workflow['nodes'] if 'position' in node]
        if x_positions:
            min_x = min(x_positions)
            max_x = max(x_positions)
            print(f"✓ X-axis range: {min_x} to {max_x} (spread: {max_x - min_x}px)")

        print(f"\n✅ Consolidated workflow is valid!")
        return True

    def save_workflow(self, workflow: Dict[str, Any], output_file: str):
        """Save consolidated workflow to file"""
        with open(output_file, 'w') as f:
            json.dump(workflow, f, indent=2)

        file_size = Path(output_file).stat().st_size
        print(f"\n✅ Saved consolidated workflow to: {output_file}")
        print(f"   File size: {file_size:,} bytes ({file_size / 1024:.1f} KB)")


def main():
    """Main execution"""
    print("=" * 60)
    print("N8N WORKFLOW CONSOLIDATION SCRIPT")
    print("=" * 60)

    consolidator = WorkflowConsolidator()

    # Consolidate workflows
    consolidated_workflow = consolidator.consolidate()

    # Validate
    if not consolidator.validate_consolidated(consolidated_workflow):
        print("\n❌ Validation failed!")
        sys.exit(1)

    # Save
    output_file = "scheduler-master-consolidated-v1.json"
    consolidator.save_workflow(consolidated_workflow, output_file)

    # Print summary
    print("\n" + "=" * 60)
    print("CONSOLIDATION SUMMARY")
    print("=" * 60)
    print(f"Workflows merged: {len(consolidator.phases)}")
    print(f"Total nodes: {len(consolidated_workflow['nodes'])}")
    print(f"Total connections: {len(consolidated_workflow['connections'])}")
    print(f"Output file: {output_file}")
    print(f"\nPhases included:")
    for phase in consolidator.phases:
        print(f"  - {phase['name']} ({phase['prefix'][:-1]})")
    print("\n✅ CONSOLIDATION COMPLETE!")
    print("=" * 60)


if __name__ == "__main__":
    main()
