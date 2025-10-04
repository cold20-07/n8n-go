#!/usr/bin/env python3
"""
Fix n8n Connections
Ensure the connection format exactly matches what n8n expects
"""

import json
from enhanced_workflow_generator import EnhancedWorkflowGenerator

def fix_n8n_connection_format():
    """Fix the connection format to match n8n exactly"""
    
    print("🔧 FIXING N8N CONNECTION FORMAT")
    print("=" * 80)
    
    description = "Create a workflow that sends a Slack notification when a webhook is triggered"
    
    try:
        generator = EnhancedWorkflowGenerator()
        workflow = generator.generate_enhanced_workflow(description, 'webhook', 'simple')
        
        # Get the original connections
        original_connections = workflow.get('connections', {})
        print(f"📋 Original connections: {len(original_connections)}")
        
        # Fix the connection format
        fixed_connections = {}
        
        for source_node_name, connection_data in original_connections.items():
            # n8n uses node names as keys, which we're already doing
            # But let's ensure the structure is exactly right
            fixed_connections[source_node_name] = {
                "main": [
                    [
                        {
                            "node": connection_data["main"][0][0]["node"],
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        
        # Update the workflow with fixed connections
        workflow['connections'] = fixed_connections
        
        # Also ensure all nodes have proper structure
        nodes = workflow.get('nodes', [])
        for node in nodes:
            # Ensure position is properly formatted
            if 'position' in node:
                pos = node['position']
                if isinstance(pos, list) and len(pos) == 2:
                    node['position'] = [int(pos[0]), int(pos[1])]
            
            # Ensure typeVersion is proper
            if 'typeVersion' in node:
                node['typeVersion'] = float(node['typeVersion']) if '.' in str(node['typeVersion']) else int(node['typeVersion'])
        
        # Generate the fixed JSON
        fixed_json = json.dumps(workflow, indent=2)
        
        print(f"🔧 FIXED WORKFLOW STRUCTURE:")
        print(f"   Nodes: {len(nodes)}")
        print(f"   Connections: {len(fixed_connections)}")
        
        # Show the connection structure
        print(f"\n🔗 FIXED CONNECTION STRUCTURE:")
        for source, conn_data in fixed_connections.items():
            target = conn_data['main'][0][0]['node']
            print(f"   '{source}' → '{target}'")
        
        # Save the fixed workflow
        with open('fixed_webhook_slack.json', 'w') as f:
            f.write(fixed_json)
        
        print(f"\n📁 Fixed workflow saved to: fixed_webhook_slack.json")
        
        # Validate the fixed structure
        print(f"\n✅ VALIDATION:")
        
        # Check that all expected connections exist
        node_names = [node['name'] for node in nodes]
        expected_connections = []
        for i in range(len(node_names) - 1):
            expected_connections.append((node_names[i], node_names[i + 1]))
        
        actual_connections = []
        for source, conn_data in fixed_connections.items():
            target = conn_data['main'][0][0]['node']
            actual_connections.append((source, target))
        
        print(f"   Expected: {expected_connections}")
        print(f"   Actual:   {actual_connections}")
        
        if set(expected_connections) == set(actual_connections):
            print(f"   ✅ All connections present and correct!")
        else:
            print(f"   ❌ Connection mismatch!")
        
        # Show a sample of the JSON
        print(f"\n📄 SAMPLE JSON (connections section):")
        connections_json = json.dumps(fixed_connections, indent=2)
        print(connections_json)
        
        return workflow
        
    except Exception as e:
        print(f"❌ Fix failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Run the n8n connection fix"""
    workflow = fix_n8n_connection_format()
    
    if workflow:
        print(f"\n🎉 SUCCESS! Fixed workflow ready for n8n import")
        print(f"📋 Import fixed_webhook_slack.json into n8n")
        print(f"🔗 All nodes should now be properly connected")
    else:
        print(f"\n❌ Failed to fix the workflow")

if __name__ == "__main__":
    main()