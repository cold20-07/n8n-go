"""
Test script for connection validation system
Tests the RSS → Content Generator → Content Parser → Twitter connection fix
"""

import json
from connection_validator import ConnectionValidator
from workflow_accuracy_validator import WorkflowAccuracyValidator


def test_rss_to_twitter_workflow():
    """Test the specific RSS to Twitter workflow connection issue"""
    
    print("🧪 Testing RSS → Content Generator → Content Parser → Twitter Connection Fix")
    print("=" * 70)
    
    # Create test workflow with the exact issue mentioned
    test_workflow = {
        "name": "RSS to Twitter Content Pipeline",
        "nodes": [
            {
                "id": "rss_reader_1",
                "name": "RSS Feed Reader",
                "type": "n8n-nodes-base.rssFeedRead",
                "typeVersion": 1,
                "position": [0, 300],
                "parameters": {
                    "url": "https://feeds.feedburner.com/TechCrunch"
                }
            },
            {
                "id": "content_gen_2",
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
                "id": "content_parser_3",
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
                "id": "twitter_post_4",
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
        "connections": {},  # This is the problem - no connections!
        "active": True,
        "settings": {
            "executionOrder": "v1",
            "saveManualExecutions": True,
            "callerPolicy": "workflowsFromSameOwner"
        },
        "tags": ["rss", "twitter", "content", "automation"]
    }
    
    print("📋 Original Workflow:")
    print(f"   Nodes: {len(test_workflow['nodes'])}")
    print(f"   Connections: {len(test_workflow['connections'])}")
    
    for node in test_workflow['nodes']:
        print(f"   - {node['name']} ({node['type']})")
    
    print(f"\n❌ Problem: No connections between nodes!")
    print("   Expected flow: RSS Feed Reader → Content Generator → Content Parser → Twitter Post")
    
    # Test the validator
    validator = ConnectionValidator()
    
    print("\n🔧 Applying Connection Validation and Fixes...")
    fixed_workflow, validation_report = validator.validate_and_fix_connections(test_workflow)
    
    print("\n📊 Validation Report:")
    print(f"   Original valid: {validation_report['original_validation']['is_valid']}")
    print(f"   Original errors: {len(validation_report['original_validation']['errors'])}")
    
    if validation_report['original_validation']['errors']:
        print("   Original errors:")
        for error in validation_report['original_validation']['errors'][:5]:
            print(f"     - {error}")
    
    print(f"\n✅ Fixes Applied: {len(validation_report.get('fixes_applied', []))}")
    for fix in validation_report.get('fixes_applied', []):
        print(f"   - {fix}")
    
    print(f"\n🚀 Improvements: {len(validation_report.get('connection_improvements', []))}")
    for improvement in validation_report.get('connection_improvements', []):
        print(f"   - {improvement}")
    
    print(f"\n🔗 Fixed Connections:")
    connections = fixed_workflow.get('connections', {})
    connection_count = 0
    
    for source, conn_data in connections.items():
        if 'main' in conn_data:
            for group in conn_data['main']:
                for conn in group:
                    target = conn['node']
                    print(f"   {source} → {target}")
                    connection_count += 1
    
    print(f"\n📈 Results:")
    print(f"   Total connections created: {connection_count}")
    print(f"   Expected connections: {len(test_workflow['nodes']) - 1}")
    print(f"   Connection success: {'✅ YES' if connection_count >= len(test_workflow['nodes']) - 1 else '❌ NO'}")
    
    # Validate the fixed workflow
    if 'post_fix_validation' in validation_report:
        post_fix_valid = validation_report['post_fix_validation']['is_valid']
        post_fix_errors = validation_report['post_fix_validation']['errors']
        print(f"   Post-fix validation: {'✅ VALID' if post_fix_valid else '❌ INVALID'}")
        
        if post_fix_errors:
            print(f"   Remaining errors: {len(post_fix_errors)}")
            for error in post_fix_errors[:3]:
                print(f"     - {error}")
    
    # Test specific flow pattern
    print(f"\n🔍 Flow Pattern Analysis:")
    rss_to_content = check_connection_exists(connections, "RSS Feed Reader", "Content Generator")
    content_to_parser = check_connection_exists(connections, "Content Generator", "Content Parser")
    parser_to_twitter = check_connection_exists(connections, "Content Parser", "Twitter Post")
    
    print(f"   RSS Feed Reader → Content Generator: {'✅' if rss_to_content else '❌'}")
    print(f"   Content Generator → Content Parser: {'✅' if content_to_parser else '❌'}")
    print(f"   Content Parser → Twitter Post: {'✅' if parser_to_twitter else '❌'}")
    
    complete_flow = rss_to_content and content_to_parser and parser_to_twitter
    print(f"   Complete RSS→Twitter flow: {'✅ ESTABLISHED' if complete_flow else '❌ INCOMPLETE'}")
    
    return fixed_workflow, validation_report, complete_flow


def check_connection_exists(connections, source_name, target_name):
    """Check if a specific connection exists"""
    if source_name not in connections:
        return False
    
    conn_data = connections[source_name]
    if 'main' not in conn_data:
        return False
    
    for group in conn_data['main']:
        for conn in group:
            if conn.get('node') == target_name:
                return True
    
    return False


def test_accuracy_validation():
    """Test the accuracy validation system"""
    print("\n" + "=" * 70)
    print("🧪 Testing Workflow Accuracy Validation")
    print("=" * 70)
    
    validator = WorkflowAccuracyValidator()
    
    # Test workflow with accuracy issues
    test_workflow = {
        "name": "Test Workflow",
        "nodes": [
            {
                "id": "1",
                "name": "Bad RSS Reader",
                "type": "n8n-nodes-base.rssFeedRead",
                "typeVersion": 1,
                "position": [0, 300],
                "parameters": {
                    "url": "https://example.com/feed.xml"  # Placeholder URL - should be flagged
                }
            },
            {
                "id": "2",
                "name": "Invalid Node",
                "type": "invalid-node-type",  # Invalid node type - should be flagged
                "typeVersion": 1,
                "position": [300, 300],
                "parameters": {}
            }
        ],
        "connections": {},
        "active": True,
        "settings": {}
    }
    
    result = validator.validate_complete_workflow(test_workflow)
    
    print(f"📊 Accuracy Validation Results:")
    print(f"   Workflow valid: {result.is_valid}")
    print(f"   Errors found: {len(result.errors)}")
    print(f"   Warnings: {len(result.warnings)}")
    print(f"   Suggestions: {len(result.suggestions)}")
    
    if result.errors:
        print(f"\n❌ Errors:")
        for error in result.errors:
            print(f"   - {error}")
    
    if result.warnings:
        print(f"\n⚠️ Warnings:")
        for warning in result.warnings:
            print(f"   - {warning}")
    
    if result.suggestions:
        print(f"\n💡 Suggestions:")
        for suggestion in result.suggestions:
            print(f"   - {suggestion}")
    
    return result


def save_test_results(fixed_workflow, validation_report, complete_flow):
    """Save test results to files"""
    
    # Save fixed workflow
    with open('test_fixed_workflow.json', 'w') as f:
        json.dump(fixed_workflow, f, indent=2)
    
    # Save validation report
    with open('test_validation_report.json', 'w') as f:
        json.dump(validation_report, f, indent=2)
    
    # Save test summary
    summary = {
        "test_name": "RSS to Twitter Connection Fix Test",
        "timestamp": "2024-01-01T00:00:00Z",
        "results": {
            "complete_flow_established": complete_flow,
            "connections_created": len(fixed_workflow.get('connections', {})),
            "nodes_count": len(fixed_workflow.get('nodes', [])),
            "fixes_applied": len(validation_report.get('fixes_applied', [])),
            "improvements_made": len(validation_report.get('connection_improvements', []))
        },
        "success": complete_flow
    }
    
    with open('test_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n💾 Test results saved:")
    print(f"   - test_fixed_workflow.json")
    print(f"   - test_validation_report.json") 
    print(f"   - test_summary.json")


if __name__ == "__main__":
    print("🚀 Starting Connection Validation Tests")
    print("=" * 70)
    
    try:
        # Test 1: RSS to Twitter connection fix
        fixed_workflow, validation_report, complete_flow = test_rss_to_twitter_workflow()
        
        # Test 2: Accuracy validation
        accuracy_result = test_accuracy_validation()
        
        # Save results
        save_test_results(fixed_workflow, validation_report, complete_flow)
        
        print("\n" + "=" * 70)
        print("🎉 TEST SUMMARY")
        print("=" * 70)
        print(f"RSS→Twitter Flow Fix: {'✅ SUCCESS' if complete_flow else '❌ FAILED'}")
        print(f"Accuracy Validation: {'✅ WORKING' if len(accuracy_result.errors) > 0 else '❌ NOT DETECTING ISSUES'}")
        print(f"Overall Test Result: {'✅ PASSED' if complete_flow else '❌ FAILED'}")
        
        if complete_flow:
            print("\n🎯 The connection validation system successfully fixed the")
            print("   RSS → Content Generator → Content Parser → Twitter flow!")
        else:
            print("\n❌ The connection validation system needs improvement.")
        
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
        import traceback
        traceback.print_exc()