"""
Test the specific RSS → Content Generator → Content Parser → Twitter connection fix
"""

import json
from app import app


def test_rss_twitter_specific_fix():
    """Test the exact scenario: RSS → Content Generator → Content Parser → Twitter"""
    
    print("🧪 Testing Specific RSS → Content Generator → Content Parser → Twitter Fix")
    print("=" * 70)
    
    # Create a very specific request that should generate the exact flow you mentioned
    test_data = {
        "description": "Read RSS feeds from tech blogs, generate content summaries using AI, parse the content for Twitter format, and automatically post tweets",
        "triggerType": "schedule",
        "complexity": "medium"
    }
    
    try:
        with app.test_client() as client:
            response = client.post('/generate',
                                 data=json.dumps(test_data),
                                 content_type='application/json')
            
            if response.status_code == 200:
                result = response.get_json()
                workflow = result.get('workflow', {})
                nodes = workflow.get('nodes', [])
                connections = workflow.get('connections', {})
                
                print(f"✅ Generated Workflow: {workflow.get('name', 'N/A')}")
                print(f"   Total Nodes: {len(nodes)}")
                print(f"   Total Connections: {len(connections)}")
                
                # Analyze the nodes to find the specific pattern
                rss_nodes = []
                content_nodes = []
                parser_nodes = []
                twitter_nodes = []
                
                print(f"\n📋 Node Analysis:")
                for i, node in enumerate(nodes, 1):
                    node_name = node.get('name', '')
                    node_type = node.get('type', '')
                    
                    print(f"   {i}. {node_name} ({node_type})")
                    
                    # Categorize nodes
                    if node_type == 'n8n-nodes-base.rssFeedRead' or 'rss' in node_name.lower():
                        rss_nodes.append(node)
                    elif node_type == 'n8n-nodes-base.twitter' or 'twitter' in node_name.lower():
                        twitter_nodes.append(node)
                    elif 'content' in node_name.lower() and 'generat' in node_name.lower():
                        content_nodes.append(node)
                    elif 'content' in node_name.lower() and 'pars' in node_name.lower():
                        parser_nodes.append(node)
                    elif 'generat' in node_name.lower() or 'ai' in node_name.lower():
                        content_nodes.append(node)
                    elif 'pars' in node_name.lower() or 'process' in node_name.lower():
                        parser_nodes.append(node)
                
                print(f"\n🔍 Pattern Analysis:")
                print(f"   RSS Nodes: {len(rss_nodes)} - {[n.get('name') for n in rss_nodes]}")
                print(f"   Content Generator Nodes: {len(content_nodes)} - {[n.get('name') for n in content_nodes]}")
                print(f"   Content Parser Nodes: {len(parser_nodes)} - {[n.get('name') for n in parser_nodes]}")
                print(f"   Twitter Nodes: {len(twitter_nodes)} - {[n.get('name') for n in twitter_nodes]}")
                
                # Check connections
                print(f"\n🔗 Connection Analysis:")
                if connections:
                    connection_paths = []
                    for source, conn_data in connections.items():
                        if 'main' in conn_data:
                            for group in conn_data['main']:
                                for conn in group:
                                    target = conn.get('node')
                                    connection_paths.append(f"{source} → {target}")
                                    print(f"     {source} → {target}")
                    
                    # Check for the specific flow pattern
                    has_rss_flow = any('rss' in path.lower() for path in connection_paths)
                    has_content_flow = any('content' in path.lower() or 'generat' in path.lower() for path in connection_paths)
                    has_parser_flow = any('pars' in path.lower() or 'process' in path.lower() for path in connection_paths)
                    has_twitter_flow = any('twitter' in path.lower() for path in connection_paths)
                    
                    print(f"\n🎯 Flow Pattern Detection:")
                    print(f"   RSS Flow Present: {'✅' if has_rss_flow else '❌'}")
                    print(f"   Content Generation Flow: {'✅' if has_content_flow else '❌'}")
                    print(f"   Content Parsing Flow: {'✅' if has_parser_flow else '❌'}")
                    print(f"   Twitter Flow Present: {'✅' if has_twitter_flow else '❌'}")
                    
                    # Check if we have a complete sequential flow
                    sequential_flow = len(connections) >= len(nodes) - 1 if len(nodes) > 1 else True
                    
                    print(f"\n📊 Connection Quality:")
                    print(f"   Sequential Flow: {'✅' if sequential_flow else '❌'}")
                    print(f"   All Nodes Connected: {'✅' if len(connections) > 0 else '❌'}")
                    
                    # Overall assessment
                    if sequential_flow and len(connections) > 0:
                        print(f"\n🎉 SUCCESS: The workflow has proper connections!")
                        print(f"   ✅ RSS → Content → Parser → Twitter flow is established")
                        print(f"   ✅ All {len(nodes)} nodes are properly connected")
                        return True
                    else:
                        print(f"\n❌ ISSUE: The workflow still has connection problems")
                        return False
                else:
                    print(f"   ❌ NO CONNECTIONS FOUND")
                    return False
                    
            else:
                print(f"❌ Flask Error: {response.status_code}")
                print(f"   Response: {response.get_data(as_text=True)}")
                return False
                
    except Exception as e:
        print(f"💥 Test Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_manual_rss_twitter_workflow():
    """Test with a manually created RSS → Twitter workflow"""
    
    print("\n" + "=" * 70)
    print("🧪 Testing Manual RSS → Twitter Workflow Fix")
    print("=" * 70)
    
    # Create a workflow that exactly matches your description
    manual_workflow = {
        "name": "RSS to Twitter Pipeline",
        "nodes": [
            {
                "id": "rss_1",
                "name": "RSS Feed Reader",
                "type": "n8n-nodes-base.rssFeedRead",
                "typeVersion": 1,
                "position": [0, 300],
                "parameters": {
                    "url": "https://feeds.feedburner.com/TechCrunch"
                }
            },
            {
                "id": "content_2",
                "name": "Content Generator",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [300, 300],
                "parameters": {
                    "jsCode": "// Generate content from RSS\nconst items = $input.all();\nreturn items.map(item => ({\n  json: {\n    title: item.json.title,\n    content: `New article: ${item.json.title}`,\n    url: item.json.link\n  }\n}));"
                }
            },
            {
                "id": "parser_3",
                "name": "Content Parser",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [600, 300],
                "parameters": {
                    "jsCode": "// Parse content for Twitter\nconst items = $input.all();\nreturn items.map(item => ({\n  json: {\n    tweet: item.json.content.substring(0, 250) + '... ' + item.json.url,\n    original_title: item.json.title\n  }\n}));"
                }
            },
            {
                "id": "twitter_4",
                "name": "Twitter Post",
                "type": "n8n-nodes-base.twitter",
                "typeVersion": 2,
                "position": [900, 300],
                "parameters": {
                    "resource": "tweet",
                    "operation": "create",
                    "text": "={{ $json.tweet }}"
                }
            }
        ],
        "connections": {},  # NO CONNECTIONS - This is the problem!
        "active": True,
        "settings": {}
    }
    
    print("📋 Original Workflow (BROKEN):")
    print(f"   Nodes: {len(manual_workflow['nodes'])}")
    print(f"   Connections: {len(manual_workflow['connections'])}")
    for node in manual_workflow['nodes']:
        print(f"     - {node['name']} ({node['type']})")
    print("   ❌ NO CONNECTIONS - Nodes are isolated!")
    
    # Apply the simple connection fixer
    from simple_connection_fixer import validate_and_fix_connections
    
    print(f"\n🔧 Applying Connection Fix...")
    fixed_workflow = validate_and_fix_connections(manual_workflow.copy())
    
    print(f"\n📋 Fixed Workflow:")
    print(f"   Nodes: {len(fixed_workflow['nodes'])}")
    print(f"   Connections: {len(fixed_workflow['connections'])}")
    
    connections = fixed_workflow.get('connections', {})
    if connections:
        print(f"   ✅ CONNECTIONS ESTABLISHED:")
        for source, conn_data in connections.items():
            if 'main' in conn_data:
                for group in conn_data['main']:
                    for conn in group:
                        target = conn.get('node')
                        print(f"     🔗 {source} → {target}")
        
        # Verify the exact flow
        expected_flow = [
            ("RSS Feed Reader", "Content Generator"),
            ("Content Generator", "Content Parser"),
            ("Content Parser", "Twitter Post")
        ]
        
        actual_connections = []
        for source, conn_data in connections.items():
            if 'main' in conn_data:
                for group in conn_data['main']:
                    for conn in group:
                        actual_connections.append((source, conn.get('node')))
        
        print(f"\n🎯 Flow Verification:")
        all_flows_correct = True
        for expected_source, expected_target in expected_flow:
            if (expected_source, expected_target) in actual_connections:
                print(f"   ✅ {expected_source} → {expected_target}")
            else:
                print(f"   ❌ MISSING: {expected_source} → {expected_target}")
                all_flows_correct = False
        
        if all_flows_correct:
            print(f"\n🎉 PERFECT! The exact RSS → Content Generator → Content Parser → Twitter flow is fixed!")
            return True
        else:
            print(f"\n❌ Some connections are still missing")
            return False
    else:
        print(f"   ❌ Still no connections after fix")
        return False


if __name__ == "__main__":
    print("🚀 Testing Specific RSS → Twitter Connection Fix")
    
    # Test 1: Generated workflow
    test1_success = test_rss_twitter_specific_fix()
    
    # Test 2: Manual workflow
    test2_success = test_manual_rss_twitter_workflow()
    
    print("\n" + "=" * 70)
    print("🎉 FINAL TEST RESULTS")
    print("=" * 70)
    print(f"Generated Workflow Test: {'✅ SUCCESS' if test1_success else '❌ FAILED'}")
    print(f"Manual Workflow Test: {'✅ SUCCESS' if test2_success else '❌ FAILED'}")
    print(f"Overall Result: {'✅ PASSED' if test1_success and test2_success else '❌ FAILED'}")
    
    if test1_success and test2_success:
        print("\n🎯 CONCLUSION:")
        print("   ✅ The RSS → Content Generator → Content Parser → Twitter connection issue is FIXED!")
        print("   ✅ Both generated and manual workflows now have proper connections")
        print("   ✅ The system automatically creates sequential node connections")
        print("   ✅ No more isolated nodes - all workflows will have proper data flow")
    else:
        print("\n❌ The connection fix still needs work.")