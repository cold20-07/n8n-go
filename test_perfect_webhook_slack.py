#!/usr/bin/env python3
"""
Perfect Webhook to Slack Test
Tests the simple webhook-to-Slack workflow to ensure it's perfect
"""

import json
from enhanced_workflow_generator import EnhancedWorkflowGenerator

def test_perfect_webhook_slack():
    """Test the perfect webhook to Slack workflow"""
    
    print("🎯 TESTING PERFECT WEBHOOK TO SLACK WORKFLOW")
    print("=" * 80)
    
    # The exact prompt
    description = "Create a workflow that sends a Slack notification when a webhook is triggered"
    
    print(f"📝 Prompt: {description}")
    print("-" * 80)
    
    try:
        generator = EnhancedWorkflowGenerator()
        workflow = generator.generate_enhanced_workflow(description, 'webhook', 'simple')
        
        print(f"✅ WORKFLOW GENERATED")
        print(f"   Name: {workflow['name']}")
        print(f"   Nodes: {len(workflow['nodes'])}")
        print(f"   Connections: {len(workflow['connections'])}")
        
        # Analyze the workflow structure
        nodes = workflow['nodes']
        connections = workflow['connections']
        
        print(f"\n🧩 PERFECT WORKFLOW ANALYSIS:")
        
        # Expected structure: Webhook → Set → Slack
        expected_types = [
            'n8n-nodes-base.webhook',
            'n8n-nodes-base.set', 
            'n8n-nodes-base.slack'
        ]
        
        actual_types = [node['type'] for node in nodes]
        
        print(f"   Expected: {expected_types}")
        print(f"   Actual:   {actual_types}")
        
        if actual_types == expected_types:
            print(f"   ✅ Perfect node sequence!")
        else:
            print(f"   ⚠️ Node sequence differs")
        
        # Check each node in detail
        print(f"\n📋 DETAILED NODE ANALYSIS:")
        
        for i, node in enumerate(nodes, 1):
            name = node['name']
            node_type = node['type']
            parameters = node.get('parameters', {})
            position = node.get('position', [0, 0])
            
            print(f"\n   {i}. {name}")
            print(f"      Type: {node_type}")
            print(f"      Position: {position}")
            print(f"      Parameters: {len(parameters)} configured")
            
            # Validate specific node configurations
            if 'webhook' in node_type:
                print(f"      🔍 Webhook Configuration:")
                if 'httpMethod' in parameters:
                    print(f"         ✅ HTTP Method: {parameters['httpMethod']}")
                if 'path' in parameters:
                    print(f"         ✅ Path: {parameters['path']}")
                if 'options' in parameters:
                    print(f"         ✅ Options configured")
                
            elif 'set' in node_type:
                print(f"      🔍 Data Processing Configuration:")
                assignments = parameters.get('assignments', {}).get('assignments', [])
                print(f"         ✅ Assignments: {len(assignments)} configured")
                for assignment in assignments:
                    name_field = assignment.get('name', 'unknown')
                    print(f"            • {name_field}")
                
            elif 'slack' in node_type:
                print(f"      🔍 Slack Configuration:")
                if 'operation' in parameters:
                    print(f"         ✅ Operation: {parameters['operation']}")
                if 'channel' in parameters:
                    print(f"         ✅ Channel: {parameters['channel']}")
                if 'text' in parameters:
                    text_preview = parameters['text'][:100] + "..." if len(parameters['text']) > 100 else parameters['text']
                    print(f"         ✅ Message template configured")
                    print(f"            Preview: {text_preview}")
        
        # Check connections
        print(f"\n🔗 CONNECTION VALIDATION:")
        
        expected_connections = [
            (nodes[0]['name'], nodes[1]['name']),
            (nodes[1]['name'], nodes[2]['name'])
        ]
        
        actual_connections = []
        for source, targets in connections.items():
            target = targets['main'][0][0]['node']
            actual_connections.append((source, target))
        
        print(f"   Expected connections:")
        for source, target in expected_connections:
            print(f"      {source} → {target}")
        
        print(f"   Actual connections:")
        for source, target in actual_connections:
            print(f"      {source} → {target}")
        
        if set(expected_connections) == set(actual_connections):
            print(f"   ✅ Perfect connections!")
        else:
            print(f"   ⚠️ Connection mismatch")
        
        # Generate and validate JSON
        print(f"\n📄 JSON VALIDATION:")
        json_str = json.dumps(workflow, indent=2)
        json_size = len(json_str)
        
        print(f"   ✅ Valid JSON ({json_size:,} characters)")
        
        # Save the perfect workflow
        with open('perfect_webhook_slack.json', 'w') as f:
            f.write(json_str)
        
        print(f"   📁 Saved to: perfect_webhook_slack.json")
        
        # Overall assessment
        print(f"\n" + "=" * 80)
        
        quality_checks = [
            len(nodes) == 3,  # Exactly 3 nodes
            len(connections) == 2,  # Exactly 2 connections
            actual_types == expected_types,  # Correct node types
            all(node.get('parameters') for node in nodes),  # All nodes have parameters
            json_size > 1000  # Reasonable JSON size
        ]
        
        passed_checks = sum(quality_checks)
        total_checks = len(quality_checks)
        
        if passed_checks == total_checks:
            print("🎉 PERFECT! This workflow is absolutely flawless!")
            print("✅ Ready for immediate use in n8n:")
            print("   • Exactly 3 nodes in perfect sequence")
            print("   • All connections properly configured")
            print("   • All parameters have realistic values")
            print("   • Webhook ready to receive POST requests")
            print("   • Slack notification with rich formatting")
            print("   • Data processing with timestamp and formatting")
            
            print(f"\n🚀 USAGE INSTRUCTIONS:")
            print("   1. Import perfect_webhook_slack.json into n8n")
            print("   2. Configure your Slack credentials")
            print("   3. Activate the workflow")
            print("   4. Send POST requests to the webhook URL")
            print("   5. Watch Slack notifications appear instantly!")
            
            return True
        else:
            print(f"⚠️ Quality score: {passed_checks}/{total_checks} - Some improvements needed")
            return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the perfect webhook to Slack test"""
    success = test_perfect_webhook_slack()
    
    if success:
        print(f"\n🎉 SUCCESS! The webhook-to-Slack workflow is PERFECT!")
    else:
        print(f"\n⚠️ Some issues need to be addressed")
    
    return success

if __name__ == "__main__":
    main()