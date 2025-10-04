#!/usr/bin/env python3
"""
Test Connection Formats
Test both node name and node ID based connections to see which n8n expects
"""

import json
from enhanced_workflow_generator import EnhancedWorkflowGenerator

def test_both_connection_formats():
    """Test both node name and node ID based connections"""
    
    print("🔍 TESTING BOTH CONNECTION FORMATS")
    print("=" * 80)
    
    description = "Create a workflow that sends a Slack notification when a webhook is triggered"
    
    try:
        generator = EnhancedWorkflowGenerator()
        workflow = generator.generate_enhanced_workflow(description, 'webhook', 'simple')
        
        nodes = workflow.get('nodes', [])
        
        print(f"📋 NODES:")
        for i, node in enumerate(nodes):
            print(f"   {i+1}. Name: '{node['name']}', ID: '{node['id']}'")
        
        # Create connections using node names (current approach)
        name_based_connections = {}
        for i in range(len(nodes) - 1):
            current_node = nodes[i]
            next_node = nodes[i + 1]
            
            name_based_connections[current_node['name']] = {
                'main': [[{
                    'node': next_node['name'],
                    'type': 'main',
                    'index': 0
                }]]
            }
        
        # Create connections using node IDs (alternative approach)
        id_based_connections = {}
        for i in range(len(nodes) - 1):
            current_node = nodes[i]
            next_node = nodes[i + 1]
            
            id_based_connections[current_node['name']] = {  # Key is still name
                'main': [[{
                    'node': next_node['name'],  # But target could be ID
                    'type': 'main',
                    'index': 0
                }]]
            }
        
        print(f"\n🔗 NAME-BASED CONNECTIONS:")
        for source, conn_data in name_based_connections.items():
            target = conn_data['main'][0][0]['node']
            print(f"   '{source}' → '{target}'")
        
        print(f"\n🆔 ID-BASED CONNECTIONS:")
        for source, conn_data in id_based_connections.items():
            target = conn_data['main'][0][0]['node']
            print(f"   '{source}' → '{target}'")
        
        # Create both versions of the workflow
        workflow_name_based = workflow.copy()
        workflow_name_based['connections'] = name_based_connections
        
        workflow_id_based = workflow.copy()
        workflow_id_based['connections'] = id_based_connections
        
        # Save both versions
        with open('workflow_name_based.json', 'w') as f:
            json.dump(workflow_name_based, f, indent=2)
        
        with open('workflow_id_based.json', 'w') as f:
            json.dump(workflow_id_based, f, indent=2)
        
        print(f"\n📁 SAVED BOTH VERSIONS:")
        print(f"   workflow_name_based.json - Uses node names")
        print(f"   workflow_id_based.json - Uses node IDs")
        
        # Show the JSON structure for both
        print(f"\n📄 NAME-BASED CONNECTION JSON:")
        print(json.dumps(name_based_connections, indent=2))
        
        print(f"\n📄 ID-BASED CONNECTION JSON:")
        print(json.dumps(id_based_connections, indent=2))
        
        # Check if there are any differences
        if name_based_connections == id_based_connections:
            print(f"\n⚠️ Both formats are identical - the issue is elsewhere")
        else:
            print(f"\n🔍 Formats differ - try both in n8n to see which works")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the connection format test"""
    success = test_both_connection_formats()
    
    if success:
        print(f"\n✅ Generated both connection formats for testing")
        print(f"🧪 Try importing both JSON files into n8n to see which works")
    else:
        print(f"\n❌ Failed to generate test formats")

if __name__ == "__main__":
    main()