"""
Simple Connection Fixer for n8n Workflows
Specifically fixes RSS → Content Generator → Content Parser → Twitter connection issues
"""

def fix_workflow_connections_simple(workflow):
    """
    Simple function to fix workflow connections
    Ensures all nodes are connected in sequence
    """
    if not workflow or 'nodes' not in workflow:
        return workflow
    
    nodes = workflow.get('nodes', [])
    if len(nodes) < 2:
        return workflow
    
    print(f"Connection Fix: Fixing connections for {len(nodes)} nodes...")
    
    # Create sequential connections
    connections = {}
    
    for i in range(len(nodes) - 1):
        current_node = nodes[i]
        next_node = nodes[i + 1]
        
        current_name = current_node.get('name')
        next_name = next_node.get('name')
        
        if current_name and next_name:
            connections[current_name] = {
                'main': [[{
                    'node': next_name,
                    'type': 'main',
                    'index': 0
                }]]
            }
            print(f"   [CONNECT] Connected: {current_name} -> {next_name}")
    
    workflow['connections'] = connections
    print(f"[OK] Created {len(connections)} connections")
    
    return workflow


def ensure_proper_node_flow(workflow):
    """
    Ensure proper node flow for RSS → Content → Parser → Twitter
    """
    if not workflow or 'nodes' not in workflow:
        return workflow
    
    nodes = workflow.get('nodes', [])
    if len(nodes) < 2:
        return workflow
    
    # Find specific node types
    rss_nodes = []
    content_nodes = []
    parser_nodes = []
    twitter_nodes = []
    other_nodes = []
    
    for node in nodes:
        node_type = node.get('type', '')
        node_name = node.get('name', '').lower()
        
        if node_type == 'n8n-nodes-base.rssFeedRead':
            rss_nodes.append(node)
        elif node_type == 'n8n-nodes-base.twitter':
            twitter_nodes.append(node)
        elif 'content' in node_name or 'generate' in node_name:
            content_nodes.append(node)
        elif 'parse' in node_name or 'process' in node_name:
            parser_nodes.append(node)
        else:
            other_nodes.append(node)
    
    # Reorder nodes for proper flow
    ordered_nodes = []
    
    # Add RSS nodes first
    ordered_nodes.extend(rss_nodes)
    
    # Add content generation nodes
    ordered_nodes.extend(content_nodes)
    
    # Add parser nodes
    ordered_nodes.extend(parser_nodes)
    
    # Add other processing nodes
    ordered_nodes.extend(other_nodes)
    
    # Add Twitter nodes last
    ordered_nodes.extend(twitter_nodes)
    
    # If we have the expected pattern, use ordered nodes
    if rss_nodes and twitter_nodes:
        workflow['nodes'] = ordered_nodes
        print(f"🔄 Reordered nodes for RSS → Twitter flow")
        
        # Log the new order
        for i, node in enumerate(ordered_nodes):
            print(f"   {i+1}. {node.get('name')} ({node.get('type')})")
    
    return workflow


def validate_and_fix_connections(workflow):
    """
    Main function to validate and fix workflow connections
    """
    if not workflow:
        return workflow
    
    print("Validation: Validating workflow connections...")
    
    # Step 1: Ensure proper node flow
    workflow = ensure_proper_node_flow(workflow)
    
    # Step 2: Fix connections
    workflow = fix_workflow_connections_simple(workflow)
    
    # Step 3: Validate the result
    nodes = workflow.get('nodes', [])
    connections = workflow.get('connections', {})
    
    print(f"Validation: Results:")
    print(f"   Nodes: {len(nodes)}")
    print(f"   Connections: {len(connections)}")
    
    # Check if all non-trigger nodes have inputs
    trigger_types = [
        'n8n-nodes-base.webhook',
        'n8n-nodes-base.scheduleTrigger', 
        'n8n-nodes-base.manualTrigger',
        'n8n-nodes-base.rssFeedRead'
    ]
    
    connected_nodes = set()
    for source, conn_data in connections.items():
        connected_nodes.add(source)
        if 'main' in conn_data:
            for group in conn_data['main']:
                for conn in group:
                    connected_nodes.add(conn.get('node'))
    
    unconnected_count = 0
    for node in nodes:
        node_name = node.get('name')
        node_type = node.get('type')
        
        if node_type not in trigger_types and node_name not in connected_nodes:
            print(f"   ⚠️ Unconnected node: {node_name}")
            unconnected_count += 1
    
    if unconnected_count == 0:
        print("   [OK] All nodes properly connected")
    else:
        print(f"   [ERROR] {unconnected_count} nodes still unconnected")
    
    return workflow


# Test the simple fixer
if __name__ == "__main__":
    # Test with a simple workflow
    test_workflow = {
        "name": "RSS to Twitter Test",
        "nodes": [
            {
                "id": "1",
                "name": "RSS Feed Reader",
                "type": "n8n-nodes-base.rssFeedRead",
                "typeVersion": 1,
                "position": [0, 300],
                "parameters": {"url": "https://example.com/feed.xml"}
            },
            {
                "id": "2",
                "name": "Content Generator",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [300, 300],
                "parameters": {"jsCode": "return $input.all();"}
            },
            {
                "id": "3",
                "name": "Content Parser",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [600, 300],
                "parameters": {"jsCode": "return $input.all();"}
            },
            {
                "id": "4",
                "name": "Twitter Post",
                "type": "n8n-nodes-base.twitter",
                "typeVersion": 2,
                "position": [900, 300],
                "parameters": {"resource": "tweet", "operation": "create"}
            }
        ],
        "connections": {},
        "active": True,
        "settings": {}
    }
    
    print("🧪 Testing Simple Connection Fixer")
    print("=" * 50)
    
    print("Before:")
    print(f"  Nodes: {len(test_workflow['nodes'])}")
    print(f"  Connections: {len(test_workflow['connections'])}")
    
    fixed_workflow = validate_and_fix_connections(test_workflow)
    
    print("\nAfter:")
    print(f"  Nodes: {len(fixed_workflow['nodes'])}")
    print(f"  Connections: {len(fixed_workflow['connections'])}")
    
    print("\nConnections created:")
    for source, conn_data in fixed_workflow['connections'].items():
        for group in conn_data['main']:
            for conn in group:
                print(f"  {source} → {conn['node']}")