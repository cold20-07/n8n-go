#!/usr/bin/env python3
"""
Test Updated Simple Workflow
Test the updated 2-node webhook-to-Slack workflow
"""

import json
from enhanced_workflow_generator import EnhancedWorkflowGenerator

def test_updated_simple_workflow():
    """Test the updated simple webhook-to-Slack workflow"""
    
    print("🎯 TESTING UPDATED SIMPLE WORKFLOW")
    print("=" * 80)
    
    description = "Create a workflow that sends a Slack notification when a webhook is triggered"
    
    try:
        generator = EnhancedWorkflowGenerator()
        workflow = generator.generate_enhanced_workflow(description, 'webhook', 'simple')
        
        nodes = workflow.get('nodes', [])
        connections = workflow.get('connections', {})
        
        print(f"✅ WORKFLOW GENERATED:")
        print(f"   Name: {workflow['name']}")
        print(f"   Nodes: {len(nodes)}")
        print(f"   Connections: {len(connections)}")
        
        # Show the structure
        print(f"\n📋 NODE STRUCTURE:")
        for i, node in enumerate(nodes, 1):
            print(f"   {i}. {node['name']} ({node['type']})")
            print(f"      ID: {node['id']}")
            print(f"      Position: {node['position']}")
            print(f"      Parameters: {len(node.get('parameters', {}))}")
        
        print(f"\n🔗 CONNECTION STRUCTURE:")
        for source, conn_data in connections.items():
            target = conn_data['main'][0][0]['node']
            print(f"   {source} → {target}")
        
        # Generate and save JSON
        json_output = json.dumps(workflow, indent=2)
        
        with open('updated_simple_workflow.json', 'w') as f:
            f.write(json_output)
        
        print(f"\n📁 Saved to: updated_simple_workflow.json")
        print(f"📊 JSON size: {len(json_output):,} characters")
        
        # Validate the structure
        print(f"\n✅ VALIDATION:")
        
        # Check node count
        if len(nodes) == 2:
            print(f"   ✅ Correct node count (2)")
        else:
            print(f"   ❌ Wrong node count ({len(nodes)}, expected 2)")
        
        # Check connection count
        if len(connections) == 1:
            print(f"   ✅ Correct connection count (1)")
        else:
            print(f"   ❌ Wrong connection count ({len(connections)}, expected 1)")
        
        # Check node types
        expected_types = ['n8n-nodes-base.webhook', 'n8n-nodes-base.slack']
        actual_types = [node['type'] for node in nodes]
        
        if actual_types == expected_types:
            print(f"   ✅ Correct node types")
        else:
            print(f"   ❌ Wrong node types: {actual_types}")
        
        # Check connection
        if connections:
            source_node = nodes[0]['name']
            target_node = nodes[1]['name']
            
            if source_node in connections:
                actual_target = connections[source_node]['main'][0][0]['node']
                if actual_target == target_node:
                    print(f"   ✅ Correct connection: {source_node} → {target_node}")
                else:
                    print(f"   ❌ Wrong connection target: {actual_target}")
            else:
                print(f"   ❌ Missing connection from {source_node}")
        
        return len(nodes) == 2 and len(connections) == 1
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the updated simple workflow test"""
    success = test_updated_simple_workflow()
    
    if success:
        print(f"\n🎉 SUCCESS! Updated simple workflow is perfect!")
        print(f"📋 This 2-node workflow should definitely work in n8n")
        print(f"🔗 Import updated_simple_workflow.json to test")
    else:
        print(f"\n❌ Issues found with the updated workflow")

if __name__ == "__main__":
    main()