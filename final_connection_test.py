#!/usr/bin/env python3
"""
Final Connection Test
Test the updated Flask app with enhanced logging and validation
"""

import json

def test_updated_flask_app():
    """Test the updated Flask app logic"""
    
    print("🎯 FINAL CONNECTION TEST - UPDATED FLASK APP")
    print("=" * 80)
    
    # Test multiple prompts to ensure all work
    test_prompts = [
        "Create a workflow that sends a Slack notification when a webhook is triggered",
        "Create a workflow that receives webhook data, processes it with AI, stores results in Google Sheets, and sends a Slack notification",
        "Build a scheduled workflow that reads RSS feeds and posts to Twitter"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🧪 TEST {i}: {prompt[:60]}...")
        print("-" * 60)
        
        # Simulate the updated Flask logic
        try:
            from enhanced_workflow_generator import generate_enhanced_workflow
            
            workflow = generate_enhanced_workflow(prompt, 'webhook', 'medium')
            
            nodes = workflow.get('nodes', [])
            connections = workflow.get('connections', {})
            
            print(f"✅ Generation successful:")
            print(f"   Nodes: {len(nodes)}")
            print(f"   Connections: {len(connections)}")
            
            # Detailed analysis
            node_names = [node.get('name') for node in nodes]
            print(f"   Node names: {node_names}")
            
            # Check connections
            connection_pairs = []
            for source, conn_data in connections.items():
                target = conn_data['main'][0][0]['node']
                connection_pairs.append((source, target))
                print(f"   🔗 {source} → {target}")
            
            # Validate completeness
            expected_connections = len(nodes) - 1 if len(nodes) > 1 else 0
            
            if len(connections) == expected_connections:
                print(f"   ✅ Perfect: {expected_connections} connections as expected")
            else:
                print(f"   ❌ Issue: Expected {expected_connections}, got {len(connections)}")
            
            # Check for disconnected nodes
            connected_sources = set(connections.keys())
            connected_targets = set(target for _, target in connection_pairs)
            all_connected = connected_sources | connected_targets
            disconnected = set(node_names) - all_connected
            
            if disconnected:
                print(f"   🚨 DISCONNECTED: {list(disconnected)}")
            else:
                print(f"   ✅ ALL NODES CONNECTED")
            
            # Save this test result
            with open(f'test_{i}_result.json', 'w') as f:
                json.dump(workflow, f, indent=2)
            
            print(f"   📁 Saved to: test_{i}_result.json")
            
        except Exception as e:
            print(f"   ❌ FAILED: {e}")
            import traceback
            traceback.print_exc()

def create_perfect_simple_workflow():
    """Create a guaranteed perfect simple workflow"""
    
    print(f"\n🎯 CREATING GUARANTEED PERFECT WORKFLOW")
    print("=" * 60)
    
    # Create the simplest possible perfect workflow
    perfect_workflow = {
        "id": "perfect_workflow_123",
        "name": "Perfect Webhook to Slack",
        "nodes": [
            {
                "id": "webhook_node",
                "name": "Webhook",
                "type": "n8n-nodes-base.webhook",
                "typeVersion": 1,
                "position": [200, 300],
                "parameters": {
                    "httpMethod": "POST",
                    "path": "perfect-webhook"
                }
            },
            {
                "id": "slack_node", 
                "name": "Slack",
                "type": "n8n-nodes-base.slack",
                "typeVersion": 1,
                "position": [400, 300],
                "parameters": {
                    "operation": "post",
                    "channel": "#general",
                    "text": "🎉 Perfect workflow executed!"
                }
            }
        ],
        "connections": {
            "Webhook": {
                "main": [
                    [
                        {
                            "node": "Slack",
                            "type": "main",
                            "index": 0
                        }
                    ]
                ]
            }
        },
        "active": True,
        "settings": {},
        "staticData": None,
        "tags": ["perfect"],
        "triggerCount": 1,
        "updatedAt": "2025-01-01T00:00:00.000Z",
        "versionId": "1"
    }
    
    # Save the perfect workflow
    with open('perfect_workflow.json', 'w') as f:
        json.dump(perfect_workflow, f, indent=2)
    
    print(f"✅ Perfect workflow created:")
    print(f"   Nodes: {len(perfect_workflow['nodes'])}")
    print(f"   Connections: {len(perfect_workflow['connections'])}")
    print(f"   Connection: Webhook → Slack")
    print(f"   📁 Saved to: perfect_workflow.json")
    
    return perfect_workflow

def main():
    """Run the final connection test"""
    
    # Test the updated Flask app logic
    test_updated_flask_app()
    
    # Create a guaranteed perfect workflow
    perfect_workflow = create_perfect_simple_workflow()
    
    print(f"\n" + "=" * 80)
    print("🎉 FINAL CONNECTION TEST COMPLETE!")
    print("=" * 80)
    print("✅ If the tests above show perfect connections, the issue is:")
    print("   1. Frontend display problem")
    print("   2. n8n import issue") 
    print("   3. Browser cache")
    print("")
    print("🔧 SOLUTIONS:")
    print("   1. Try importing perfect_workflow.json directly into n8n")
    print("   2. Clear browser cache and refresh")
    print("   3. Check n8n version compatibility")
    print("   4. Restart the Flask app")

if __name__ == "__main__":
    main()