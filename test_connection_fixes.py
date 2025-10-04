#!/usr/bin/env python3
"""
Test script to verify that node connections are working properly
"""

import sys
import os
import json

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_basic_workflow
except ImportError as e:
    print(f"❌ Failed to import app: {e}")
    sys.exit(1)

def test_webhook_connections():
    """Test webhook workflow connections"""
    print("🔗 Testing Webhook Workflow Connections")
    print("-" * 40)
    
    workflow = create_basic_workflow(
        'Create a webhook workflow that processes orders and sends confirmations',
        'webhook',
        'medium'
    )
    
    nodes = workflow['nodes']
    connections = workflow['connections']
    
    # Check basic structure
    print(f"✅ Generated {len(nodes)} nodes")
    print(f"✅ Generated {len(connections)} connections")
    
    # Verify webhook response node exists
    has_response = any('respond' in node['name'].lower() for node in nodes)
    if has_response:
        print("✅ Webhook response node present")
    else:
        print("❌ Missing webhook response node")
        return False
    
    # Verify all nodes are connected
    node_names = set(node['name'] for node in nodes)
    connected_sources = set(connections.keys())
    connected_targets = set()
    
    for targets in connections.values():
        for target_group in targets['main']:
            for target in target_group:
                connected_targets.add(target['node'])
    
    disconnected = node_names - connected_sources - connected_targets
    
    if len(disconnected) == 0:
        print("✅ All nodes properly connected")
    else:
        print(f"❌ Disconnected nodes: {disconnected}")
        return False
    
    # Verify connection chain integrity
    connection_chain = []
    current_node = nodes[0]['name']  # Start with first node
    
    while current_node in connections:
        next_connections = connections[current_node]['main'][0]
        if next_connections:
            next_node = next_connections[0]['node']
            connection_chain.append(f"{current_node} -> {next_node}")
            current_node = next_node
        else:
            break
    
    if len(connection_chain) == len(nodes) - 1:
        print("✅ Connection chain complete")
        for conn in connection_chain:
            print(f"   {conn}")
    else:
        print(f"❌ Incomplete connection chain: {len(connection_chain)} vs {len(nodes) - 1}")
        return False
    
    return True

def test_schedule_connections():
    """Test schedule workflow connections"""
    print("\n⏰ Testing Schedule Workflow Connections")
    print("-" * 40)
    
    workflow = create_basic_workflow(
        'Create a scheduled workflow that syncs data every hour',
        'schedule',
        'medium'
    )
    
    nodes = workflow['nodes']
    connections = workflow['connections']
    
    # Check basic structure
    print(f"✅ Generated {len(nodes)} nodes")
    print(f"✅ Generated {len(connections)} connections")
    
    # Verify no response node (not needed for schedule)
    has_response = any('respond' in node['name'].lower() for node in nodes)
    if not has_response:
        print("✅ No unnecessary response node")
    else:
        print("⚠️  Schedule workflow has response node (not needed but not wrong)")
    
    # Verify all nodes are connected
    node_names = set(node['name'] for node in nodes)
    connected_sources = set(connections.keys())
    connected_targets = set()
    
    for targets in connections.values():
        for target_group in targets['main']:
            for target in target_group:
                connected_targets.add(target['node'])
    
    disconnected = node_names - connected_sources - connected_targets
    
    if len(disconnected) == 0:
        print("✅ All nodes properly connected")
    else:
        print(f"❌ Disconnected nodes: {disconnected}")
        return False
    
    return True

def test_manual_connections():
    """Test manual workflow connections"""
    print("\n👤 Testing Manual Workflow Connections")
    print("-" * 40)
    
    workflow = create_basic_workflow(
        'Create a manual workflow for processing customer feedback',
        'manual',
        'simple'
    )
    
    nodes = workflow['nodes']
    connections = workflow['connections']
    
    # Check basic structure
    print(f"✅ Generated {len(nodes)} nodes")
    print(f"✅ Generated {len(connections)} connections")
    
    # Verify connections exist
    if len(connections) > 0:
        print("✅ Connections created")
    else:
        print("❌ No connections created")
        return False
    
    # Verify all nodes are connected
    node_names = set(node['name'] for node in nodes)
    connected_sources = set(connections.keys())
    connected_targets = set()
    
    for targets in connections.values():
        for target_group in targets['main']:
            for target in target_group:
                connected_targets.add(target['node'])
    
    disconnected = node_names - connected_sources - connected_targets
    
    if len(disconnected) == 0:
        print("✅ All nodes properly connected")
    else:
        print(f"❌ Disconnected nodes: {disconnected}")
        return False
    
    return True

def test_complex_workflow_connections():
    """Test complex workflow with conditional logic"""
    print("\n🔀 Testing Complex Workflow Connections")
    print("-" * 40)
    
    workflow = create_basic_workflow(
        'Create a complex lead processing workflow with conditional routing and error handling',
        'webhook',
        'complex'
    )
    
    nodes = workflow['nodes']
    connections = workflow['connections']
    
    # Check basic structure
    print(f"✅ Generated {len(nodes)} nodes")
    print(f"✅ Generated {len(connections)} connections")
    
    # Look for conditional nodes
    has_conditional = any(node['type'] == 'n8n-nodes-base.if' for node in nodes)
    if has_conditional:
        print("✅ Conditional logic node present")
    else:
        print("ℹ️  No conditional nodes (may be normal)")
    
    # Verify all nodes are connected
    node_names = set(node['name'] for node in nodes)
    connected_sources = set(connections.keys())
    connected_targets = set()
    
    for targets in connections.values():
        for target_group in targets['main']:
            for target in target_group:
                connected_targets.add(target['node'])
    
    disconnected = node_names - connected_sources - connected_targets
    
    if len(disconnected) == 0:
        print("✅ All nodes properly connected")
    else:
        print(f"❌ Disconnected nodes: {disconnected}")
        return False
    
    return True

def test_connection_validation():
    """Test connection validation logic"""
    print("\n🔍 Testing Connection Validation")
    print("-" * 40)
    
    workflow = create_basic_workflow(
        'Test workflow for connection validation',
        'webhook',
        'medium'
    )
    
    connections = workflow['connections']
    nodes = workflow['nodes']
    
    # Validate connection structure
    validation_errors = []
    
    for source_name, connection_data in connections.items():
        # Check if source node exists
        source_exists = any(node['name'] == source_name for node in nodes)
        if not source_exists:
            validation_errors.append(f"Source node '{source_name}' does not exist")
        
        # Check connection structure
        if 'main' not in connection_data:
            validation_errors.append(f"Connection from '{source_name}' missing 'main' key")
            continue
        
        for target_group in connection_data['main']:
            for target in target_group:
                # Check target node exists
                target_name = target.get('node')
                if not target_name:
                    validation_errors.append(f"Connection from '{source_name}' missing target node name")
                    continue
                
                target_exists = any(node['name'] == target_name for node in nodes)
                if not target_exists:
                    validation_errors.append(f"Target node '{target_name}' does not exist")
                
                # Check connection properties
                if target.get('type') != 'main':
                    validation_errors.append(f"Invalid connection type: {target.get('type')}")
                
                if target.get('index') != 0:
                    validation_errors.append(f"Invalid connection index: {target.get('index')}")
    
    if len(validation_errors) == 0:
        print("✅ All connections are valid")
    else:
        print(f"❌ Connection validation errors:")
        for error in validation_errors:
            print(f"   - {error}")
        return False
    
    return True

def main():
    """Run all connection tests"""
    print("🔗 Testing Node Connection Fixes")
    print("=" * 50)
    
    tests = [
        test_webhook_connections,
        test_schedule_connections,
        test_manual_connections,
        test_complex_workflow_connections,
        test_connection_validation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Connection Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All node connections are working perfectly!")
        print("\n✅ Key Fixes Applied:")
        print("   - Fixed incomplete connection creation")
        print("   - Added proper webhook response nodes")
        print("   - Ensured all nodes are connected in proper chains")
        print("   - Validated connection structure integrity")
        print("   - Removed corrupted code from connection function")
        return True
    else:
        print("⚠️  Some connection tests failed. Please review the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)