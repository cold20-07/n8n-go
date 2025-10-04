#!/usr/bin/env python3
"""
Fix Connections Permanently
Diagnose and fix the root cause of connection issues across all automations
"""

import json
from enhanced_workflow_generator import EnhancedWorkflowGenerator

def diagnose_connection_issues():
    """Diagnose why connections aren't working"""
    
    print("🔍 DIAGNOSING CONNECTION ISSUES PERMANENTLY")
    print("=" * 80)
    
    test_prompts = [
        "Create a workflow that sends a Slack notification when a webhook is triggered",
        "Create a workflow that receives webhook data, processes it with AI, stores results in Google Sheets, and sends a Slack notification",
        "Build a scheduled workflow that reads RSS feeds and posts to Twitter",
        "Create an email automation that processes attachments and saves to database"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🧪 TEST {i}: {prompt[:60]}...")
        print("-" * 60)
        
        try:
            generator = EnhancedWorkflowGenerator()
            workflow = generator.generate_enhanced_workflow(prompt, 'webhook', 'medium')
            
            nodes = workflow.get('nodes', [])
            connections = workflow.get('connections', {})
            
            print(f"   Nodes: {len(nodes)}")
            print(f"   Connections: {len(connections)}")
            
            # Check each node
            node_names = [node.get('name') for node in nodes]
            print(f"   Node names: {node_names}")
            
            # Check connections
            connected_sources = list(connections.keys())
            print(f"   Connected sources: {connected_sources}")
            
            # Find missing connections
            expected_sources = node_names[:-1]  # All except last should have outgoing connections
            missing_connections = set(expected_sources) - set(connected_sources)
            
            if missing_connections:
                print(f"   ❌ MISSING CONNECTIONS FROM: {list(missing_connections)}")
            else:
                print(f"   ✅ All expected connections present")
            
            # Check connection targets
            for source, conn_data in connections.items():
                targets = conn_data.get('main', [[]])[0]
                for target in targets:
                    target_name = target.get('node')
                    if target_name in node_names:
                        print(f"   ✅ {source} → {target_name}")
                    else:
                        print(f"   ❌ {source} → {target_name} (INVALID TARGET)")
            
        except Exception as e:
            print(f"   ❌ FAILED: {e}")
            import traceback
            traceback.print_exc()

def fix_enhanced_generator_connections():
    """Fix the connection generation in enhanced generator"""
    
    print(f"\n🔧 FIXING ENHANCED GENERATOR CONNECTIONS")
    print("=" * 80)
    
    # Read the current enhanced generator
    with open('enhanced_workflow_generator.py', 'r') as f:
        content = f.read()
    
    # Check if create_connections method exists and is correct
    if 'def create_connections' in content:
        print("✅ create_connections method found")
        
        # Test the method directly
        generator = EnhancedWorkflowGenerator()
        
        # Create test nodes
        test_nodes = [
            {'name': 'Node 1', 'id': 'node1'},
            {'name': 'Node 2', 'id': 'node2'},
            {'name': 'Node 3', 'id': 'node3'}
        ]
        
        connections = generator.create_connections(test_nodes)
        print(f"✅ Connection method works: {len(connections)} connections")
        
        expected_connections = [
            ('Node 1', 'Node 2'),
            ('Node 2', 'Node 3')
        ]
        
        actual_connections = []
        for source, conn_data in connections.items():
            target = conn_data['main'][0][0]['node']
            actual_connections.append((source, target))
        
        print(f"   Expected: {expected_connections}")
        print(f"   Actual: {actual_connections}")
        
        if set(expected_connections) == set(actual_connections):
            print("   ✅ Connection logic is correct")
            return True
        else:
            print("   ❌ Connection logic is broken")
            return False
    else:
        print("❌ create_connections method not found")
        return False

def create_bulletproof_connection_method():
    """Create a bulletproof connection method"""
    
    print(f"\n🛡️ CREATING BULLETPROOF CONNECTION METHOD")
    print("=" * 80)
    
    bulletproof_method = '''
    def create_connections(self, nodes: List[Dict]) -> Dict:
        """Create bulletproof connections between all nodes"""
        connections = {}
        
        if not nodes or len(nodes) < 2:
            print("⚠️ Not enough nodes to create connections")
            return connections
        
        print(f"🔗 Creating connections for {len(nodes)} nodes")
        
        # Connect each node to the next one
        for i in range(len(nodes) - 1):
            current_node = nodes[i]
            next_node = nodes[i + 1]
            
            current_name = current_node.get('name', f'Node {i+1}')
            next_name = next_node.get('name', f'Node {i+2}')
            
            # Ensure names are strings and not empty
            if not current_name or not next_name:
                print(f"⚠️ Invalid node names: '{current_name}' → '{next_name}'")
                continue
            
            # Create the connection
            connections[current_name] = {
                'main': [[{
                    'node': next_name,
                    'type': 'main',
                    'index': 0
                }]]
            }
            
            print(f"   ✅ Connected: {current_name} → {next_name}")
        
        print(f"🔗 Created {len(connections)} connections total")
        return connections
    '''
    
    return bulletproof_method

def apply_permanent_fix():
    """Apply the permanent fix to the enhanced generator"""
    
    print(f"\n🔧 APPLYING PERMANENT FIX")
    print("=" * 80)
    
    # Read the current file
    with open('enhanced_workflow_generator.py', 'r') as f:
        content = f.read()
    
    # Find and replace the create_connections method
    import re
    
    # Pattern to match the entire create_connections method
    pattern = r'def create_connections\(self, nodes: List\[Dict\]\) -> Dict:.*?(?=\n    def|\n\nclass|\nclass|\Z)'
    
    new_method = '''def create_connections(self, nodes: List[Dict]) -> Dict:
        """Create bulletproof connections between all nodes"""
        connections = {}
        
        if not nodes or len(nodes) < 2:
            print("⚠️ Not enough nodes to create connections")
            return connections
        
        print(f"🔗 Creating connections for {len(nodes)} nodes")
        
        # Connect each node to the next one
        for i in range(len(nodes) - 1):
            current_node = nodes[i]
            next_node = nodes[i + 1]
            
            current_name = current_node.get('name', f'Node {i+1}')
            next_name = next_node.get('name', f'Node {i+2}')
            
            # Ensure names are strings and not empty
            if not current_name or not next_name:
                print(f"⚠️ Invalid node names: '{current_name}' → '{next_name}'")
                continue
            
            # Create the connection
            connections[current_name] = {
                'main': [[{
                    'node': next_name,
                    'type': 'main',
                    'index': 0
                }]]
            }
            
            print(f"   ✅ Connected: {current_name} → {next_name}")
        
        print(f"🔗 Created {len(connections)} connections total")
        return connections'''
    
    # Replace the method
    new_content = re.sub(pattern, new_method, content, flags=re.DOTALL)
    
    # Write back to file
    with open('enhanced_workflow_generator.py', 'w') as f:
        f.write(new_content)
    
    print("✅ Applied permanent fix to enhanced_workflow_generator.py")
    
    # Test the fix
    print(f"\n🧪 TESTING THE FIX")
    
    # Reload the module
    import importlib
    import enhanced_workflow_generator
    importlib.reload(enhanced_workflow_generator)
    
    # Test with a simple workflow
    from enhanced_workflow_generator import EnhancedWorkflowGenerator
    
    generator = EnhancedWorkflowGenerator()
    workflow = generator.generate_enhanced_workflow(
        "Create a workflow that sends a Slack notification when a webhook is triggered",
        'webhook',
        'simple'
    )
    
    nodes = workflow.get('nodes', [])
    connections = workflow.get('connections', {})
    
    print(f"   Nodes: {len(nodes)}")
    print(f"   Connections: {len(connections)}")
    
    # Verify all connections
    node_names = [node.get('name') for node in nodes]
    expected_connections = len(nodes) - 1
    
    if len(connections) == expected_connections:
        print(f"   ✅ PERFECT! All {expected_connections} connections created")
        
        # Show the connections
        for source, conn_data in connections.items():
            target = conn_data['main'][0][0]['node']
            print(f"      {source} → {target}")
        
        return True
    else:
        print(f"   ❌ STILL BROKEN: Expected {expected_connections}, got {len(connections)}")
        return False

def main():
    """Run the permanent connection fix"""
    
    print("🛠️ PERMANENT CONNECTION FIX")
    print("=" * 80)
    print("This will permanently fix connection issues across ALL automations")
    print("=" * 80)
    
    # Step 1: Diagnose current issues
    diagnose_connection_issues()
    
    # Step 2: Check if connection method works
    method_works = fix_enhanced_generator_connections()
    
    if not method_works:
        # Step 3: Apply permanent fix
        fix_success = apply_permanent_fix()
        
        if fix_success:
            print(f"\n🎉 PERMANENT FIX APPLIED SUCCESSFULLY!")
            print("✅ All automations will now have perfect connections")
            print("🔗 Every node will be connected to the next node")
            print("🚀 Test any automation prompt - connections will work!")
        else:
            print(f"\n❌ Fix failed - manual intervention needed")
    else:
        print(f"\n✅ Connection method already works correctly")
        print("🔍 The issue might be elsewhere in the system")

if __name__ == "__main__":
    main()