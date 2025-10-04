#!/usr/bin/env python3
"""
Test Actual JSON Output
Generate the exact JSON that would be sent to the user and validate it
"""

import json
from enhanced_workflow_generator import EnhancedWorkflowGenerator

def test_actual_json_output():
    """Test the actual JSON output that gets sent to the user"""
    
    print("🔍 TESTING ACTUAL JSON OUTPUT")
    print("=" * 80)
    
    description = "Create a workflow that sends a Slack notification when a webhook is triggered"
    
    try:
        generator = EnhancedWorkflowGenerator()
        workflow = generator.generate_enhanced_workflow(description, 'webhook', 'simple')
        
        # Generate the exact JSON that would be sent
        json_output = json.dumps(workflow, indent=2)
        
        print(f"📄 COMPLETE JSON OUTPUT:")
        print(json_output)
        
        # Save it to a file for inspection
        with open('actual_output.json', 'w') as f:
            f.write(json_output)
        
        print(f"\n📁 Saved to: actual_output.json")
        
        # Parse it back to check for issues
        parsed = json.loads(json_output)
        
        print(f"\n🔍 VALIDATION CHECKS:")
        
        # Check nodes
        nodes = parsed.get('nodes', [])
        print(f"   Nodes: {len(nodes)}")
        for i, node in enumerate(nodes):
            print(f"      {i+1}. {node.get('name')} ({node.get('type')})")
            print(f"         ID: {node.get('id')}")
            print(f"         Position: {node.get('position')}")
        
        # Check connections
        connections = parsed.get('connections', {})
        print(f"   Connections: {len(connections)}")
        for source, conn_data in connections.items():
            targets = conn_data.get('main', [[]])[0]
            for target in targets:
                print(f"      {source} → {target.get('node')}")
        
        # Check for n8n compatibility issues
        print(f"\n🔧 N8N COMPATIBILITY CHECKS:")
        
        # Check if all nodes have required fields
        required_node_fields = ['id', 'name', 'type', 'typeVersion', 'position', 'parameters']
        for node in nodes:
            missing_fields = [field for field in required_node_fields if field not in node]
            if missing_fields:
                print(f"   ❌ Node '{node.get('name')}' missing: {missing_fields}")
            else:
                print(f"   ✅ Node '{node.get('name')}' has all required fields")
        
        # Check connection structure
        for source, conn_data in connections.items():
            if 'main' not in conn_data:
                print(f"   ❌ Connection from '{source}' missing 'main' field")
            else:
                main_conn = conn_data['main']
                if not isinstance(main_conn, list) or not main_conn:
                    print(f"   ❌ Connection from '{source}' has invalid 'main' structure")
                else:
                    for target_list in main_conn:
                        if not isinstance(target_list, list):
                            print(f"   ❌ Connection from '{source}' has invalid target list")
                        else:
                            for target in target_list:
                                required_target_fields = ['node', 'type', 'index']
                                missing_target_fields = [field for field in required_target_fields if field not in target]
                                if missing_target_fields:
                                    print(f"   ❌ Connection from '{source}' missing target fields: {missing_target_fields}")
                                else:
                                    print(f"   ✅ Connection '{source}' → '{target['node']}' properly structured")
        
        # Check workflow-level fields
        required_workflow_fields = ['id', 'name', 'nodes', 'connections', 'active']
        missing_workflow_fields = [field for field in required_workflow_fields if field not in parsed]
        if missing_workflow_fields:
            print(f"   ❌ Workflow missing fields: {missing_workflow_fields}")
        else:
            print(f"   ✅ Workflow has all required fields")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the actual JSON output test"""
    success = test_actual_json_output()
    
    if success:
        print(f"\n✅ JSON output looks correct - the issue might be elsewhere")
        print(f"📋 Check the actual_output.json file to see the exact structure")
    else:
        print(f"\n❌ Found issues in JSON output")

if __name__ == "__main__":
    main()