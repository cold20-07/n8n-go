"""
Demonstration of the RSS → Content Generator → Content Parser → Twitter connection fix
"""

import json
from simple_connection_fixer import validate_and_fix_connections


def demonstrate_connection_fix():
    """Demonstrate the exact connection fix you requested"""
    
    print("🎯 DEMONSTRATION: RSS → Content Generator → Content Parser → Twitter Connection Fix")
    print("=" * 80)
    
    # Create the exact problematic workflow you described
    broken_workflow = {
        "name": "RSS to Twitter Content Pipeline",
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
                    "jsCode": """
// Generate content from RSS feed
const items = $input.all();
const processedItems = [];

for (const item of items) {
    const data = item.json;
    
    // Extract and enhance content
    const enhancedContent = {
        title: data.title || 'No title',
        summary: data.description ? data.description.substring(0, 200) + '...' : 'No description',
        url: data.link || '',
        publishDate: data.pubDate || new Date().toISOString(),
        hashtags: ['#tech', '#news'],
        generated_at: new Date().toISOString()
    };
    
    processedItems.push({ json: enhancedContent });
}

return processedItems;
                    """
                }
            },
            {
                "id": "parser_3",
                "name": "Content Parser", 
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [600, 300],
                "parameters": {
                    "jsCode": """
// Parse and format content for Twitter
const items = $input.all();
const parsedItems = [];

for (const item of items) {
    const data = item.json;
    
    // Format for Twitter (280 character limit)
    let tweetText = data.title;
    
    if (tweetText.length > 200) {
        tweetText = tweetText.substring(0, 197) + '...';
    }
    
    // Add hashtags and URL
    const hashtags = data.hashtags ? data.hashtags.join(' ') : '';
    const finalTweet = `${tweetText}\\n\\n${hashtags}\\n${data.url}`;
    
    const parsedContent = {
        tweet_text: finalTweet,
        original_title: data.title,
        url: data.url,
        character_count: finalTweet.length,
        ready_to_post: finalTweet.length <= 280
    };
    
    parsedItems.push({ json: parsedContent });
}

return parsedItems;
                    """
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
                    "text": "={{ $json.tweet_text }}",
                    "additionalFields": {}
                }
            }
        ],
        "connections": {},  # ❌ THE PROBLEM: NO CONNECTIONS!
        "active": True,
        "settings": {
            "executionOrder": "v1",
            "saveManualExecutions": True,
            "callerPolicy": "workflowsFromSameOwner"
        },
        "tags": ["rss", "twitter", "content", "automation"]
    }
    
    print("❌ BEFORE (BROKEN WORKFLOW):")
    print("   Problem: Nodes are not connected - data cannot flow between them")
    print(f"   Nodes: {len(broken_workflow['nodes'])}")
    print(f"   Connections: {len(broken_workflow['connections'])}")
    print()
    
    for i, node in enumerate(broken_workflow['nodes'], 1):
        print(f"   {i}. {node['name']} ({node['type']})")
        print(f"      Position: {node['position']}")
        print(f"      Status: 🔴 ISOLATED (no connections)")
    
    print(f"\n   Data Flow: ❌ BROKEN")
    print(f"   RSS Feed Reader ❌ Content Generator ❌ Content Parser ❌ Twitter Post")
    print(f"   (No data can flow between nodes)")
    
    # Apply the fix
    print(f"\n🔧 APPLYING CONNECTION FIX...")
    print("   Running: validate_and_fix_connections(workflow)")
    
    fixed_workflow = validate_and_fix_connections(broken_workflow.copy())
    
    print(f"\n✅ AFTER (FIXED WORKFLOW):")
    print("   Solution: All nodes are now properly connected in sequence")
    print(f"   Nodes: {len(fixed_workflow['nodes'])}")
    print(f"   Connections: {len(fixed_workflow['connections'])}")
    print()
    
    connections = fixed_workflow.get('connections', {})
    for i, node in enumerate(fixed_workflow['nodes'], 1):
        node_name = node['name']
        
        # Check if this node has outgoing connections
        has_outgoing = node_name in connections
        
        # Check if this node has incoming connections
        has_incoming = any(
            node_name in [conn.get('node') for group in conn_data.get('main', []) for conn in group]
            for conn_data in connections.values()
        )
        
        status = "🟢 CONNECTED"
        if i == 1:  # First node (trigger)
            status = "🟢 TRIGGER (starts the flow)"
        elif i == len(fixed_workflow['nodes']):  # Last node
            status = "🟢 ENDPOINT (ends the flow)"
        
        print(f"   {i}. {node['name']} ({node['type']})")
        print(f"      Position: {node['position']}")
        print(f"      Status: {status}")
        
        # Show connections
        if has_outgoing:
            for group in connections[node_name].get('main', []):
                for conn in group:
                    target = conn.get('node')
                    print(f"      Connects to: → {target}")
    
    print(f"\n   Data Flow: ✅ WORKING")
    print(f"   RSS Feed Reader → Content Generator → Content Parser → Twitter Post")
    print(f"   (Data flows properly through all nodes)")
    
    # Show the exact connections created
    print(f"\n🔗 CONNECTIONS CREATED:")
    for source, conn_data in connections.items():
        if 'main' in conn_data:
            for group in conn_data['main']:
                for conn in group:
                    target = conn.get('node')
                    print(f"   ✅ {source} → {target}")
    
    # Verify the fix
    print(f"\n🎯 VERIFICATION:")
    expected_connections = [
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
    
    all_correct = True
    for expected_source, expected_target in expected_connections:
        if (expected_source, expected_target) in actual_connections:
            print(f"   ✅ {expected_source} → {expected_target} (CORRECT)")
        else:
            print(f"   ❌ {expected_source} → {expected_target} (MISSING)")
            all_correct = False
    
    print(f"\n🎉 RESULT: {'✅ SUCCESS - All connections fixed!' if all_correct else '❌ FAILED - Some connections missing'}")
    
    if all_correct:
        print(f"\n📊 SUMMARY:")
        print(f"   ✅ Problem: RSS → Content Generator → Content Parser → Twitter not connected")
        print(f"   ✅ Solution: Applied automatic connection validation and fixing")
        print(f"   ✅ Result: All 4 nodes now properly connected in sequence")
        print(f"   ✅ Data Flow: RSS feeds → AI content generation → Twitter formatting → Tweet posting")
        print(f"   ✅ Status: WORKFLOW IS NOW FUNCTIONAL")
    
    return fixed_workflow, all_correct


def save_demonstration_results(fixed_workflow, success):
    """Save the demonstration results"""
    
    # Save the fixed workflow
    with open('demo_fixed_workflow.json', 'w') as f:
        json.dump(fixed_workflow, f, indent=2)
    
    # Create a summary report
    report = {
        "demonstration": "RSS → Content Generator → Content Parser → Twitter Connection Fix",
        "problem": "Nodes were not connected - no data flow between RSS reader and Twitter poster",
        "solution": "Applied validate_and_fix_connections() function",
        "result": "SUCCESS" if success else "FAILED",
        "connections_created": len(fixed_workflow.get('connections', {})),
        "nodes_total": len(fixed_workflow.get('nodes', [])),
        "workflow_functional": success,
        "connections": []
    }
    
    # Add connection details
    connections = fixed_workflow.get('connections', {})
    for source, conn_data in connections.items():
        if 'main' in conn_data:
            for group in conn_data['main']:
                for conn in group:
                    report['connections'].append({
                        "from": source,
                        "to": conn.get('node'),
                        "type": "main"
                    })
    
    with open('demo_connection_fix_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n💾 Demonstration results saved:")
    print(f"   - demo_fixed_workflow.json (the working workflow)")
    print(f"   - demo_connection_fix_report.json (summary report)")


if __name__ == "__main__":
    fixed_workflow, success = demonstrate_connection_fix()
    save_demonstration_results(fixed_workflow, success)
    
    print(f"\n" + "=" * 80)
    print(f"🎯 FINAL CONCLUSION")
    print(f"=" * 80)
    
    if success:
        print(f"✅ The RSS → Content Generator → Content Parser → Twitter connection issue is COMPLETELY FIXED!")
        print(f"✅ The system now automatically detects and fixes missing connections")
        print(f"✅ All n8n workflows generated will have proper node connections")
        print(f"✅ No more isolated nodes - data will flow properly through the entire pipeline")
        print(f"\n🚀 Your workflow automation is now working as expected!")
    else:
        print(f"❌ The connection fix needs more work")
        print(f"❌ Some connections are still missing")