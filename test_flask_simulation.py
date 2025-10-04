#!/usr/bin/env python3
"""
Test Flask App Simulation
Simulate exactly what the Flask app does to find where extra nodes come from
"""

import json

def test_flask_simulation():
    """Simulate the exact Flask app workflow generation process"""
    
    print("🔍 SIMULATING FLASK APP WORKFLOW GENERATION")
    print("=" * 80)
    
    # Simulate the exact request data
    description = "Create a workflow that sends a Slack notification when a webhook is triggered"
    trigger_type = "webhook"
    complexity = "simple"
    
    print(f"📝 Input:")
    print(f"   Description: {description}")
    print(f"   Trigger: {trigger_type}")
    print(f"   Complexity: {complexity}")
    
    # Test enhanced generator availability
    try:
        from enhanced_workflow_generator import generate_enhanced_workflow
        ENHANCED_GENERATOR_AVAILABLE = True
        print(f"✅ Enhanced generator available")
    except ImportError as e:
        ENHANCED_GENERATOR_AVAILABLE = False
        print(f"❌ Enhanced generator not available: {e}")
    
    # Test feature-aware generator availability
    try:
        from feature_aware_workflow_generator import generate_feature_aware_workflow
        FEATURE_AWARE_GENERATOR_AVAILABLE = True
        print(f"✅ Feature-aware generator available")
    except ImportError as e:
        FEATURE_AWARE_GENERATOR_AVAILABLE = False
        print(f"❌ Feature-aware generator not available: {e}")
    
    # Test trained generator availability
    try:
        from trained_workflow_generator import generate_trained_workflow
        TRAINED_GENERATOR_AVAILABLE = True
        print(f"✅ Trained generator available")
    except ImportError as e:
        TRAINED_GENERATOR_AVAILABLE = False
        print(f"❌ Trained generator not available: {e}")
    
    # Simulate the exact generation logic from app.py
    print(f"\n🎯 GENERATION LOGIC:")
    
    workflow = None
    generator_used = None
    
    if ENHANCED_GENERATOR_AVAILABLE:
        print("🎯 Using enhanced workflow generator")
        workflow = generate_enhanced_workflow(description, trigger_type, complexity)
        generator_used = "enhanced"
    elif FEATURE_AWARE_GENERATOR_AVAILABLE:
        print("🎯 Using feature-aware workflow generator")
        workflow = generate_feature_aware_workflow(description, trigger_type, complexity)
        generator_used = "feature_aware"
    elif TRAINED_GENERATOR_AVAILABLE:
        print("🎯 Using trained workflow generator")
        workflow = generate_trained_workflow(description, trigger_type, complexity)
        generator_used = "trained"
    else:
        print("⚠️ Falling back to basic workflow generation")
        # Import the basic workflow function from app.py
        import sys
        sys.path.append('.')
        from app import create_basic_workflow
        workflow = create_basic_workflow(description, trigger_type, complexity, '', {})
        generator_used = "basic"
    
    if workflow:
        nodes = workflow.get('nodes', [])
        connections = workflow.get('connections', {})
        
        print(f"\n✅ WORKFLOW GENERATED:")
        print(f"   Generator used: {generator_used}")
        print(f"   Name: {workflow.get('name', 'Unknown')}")
        print(f"   Total nodes: {len(nodes)}")
        print(f"   Total connections: {len(connections)}")
        
        # Show all nodes
        print(f"\n📋 ALL NODES:")
        for i, node in enumerate(nodes, 1):
            print(f"   {i}. {node.get('name', 'Unknown')} ({node.get('type', 'Unknown')})")
            print(f"      ID: {node.get('id', 'Unknown')}")
            print(f"      Position: {node.get('position', 'Unknown')}")
        
        # Show all connections
        print(f"\n🔗 ALL CONNECTIONS:")
        if connections:
            for source, conn_data in connections.items():
                targets = conn_data.get('main', [[]])[0]
                if targets:
                    for target in targets:
                        target_name = target.get('node', 'Unknown')
                        print(f"   {source} → {target_name}")
                else:
                    print(f"   {source} → (no target)")
        else:
            print("   ❌ NO CONNECTIONS FOUND!")
        
        # Find disconnected nodes
        print(f"\n🚨 DISCONNECTED NODE ANALYSIS:")
        node_names = [node.get('name') for node in nodes]
        connected_sources = set(connections.keys())
        connected_targets = set()
        
        for conn_data in connections.values():
            targets = conn_data.get('main', [[]])[0]
            for target in targets:
                connected_targets.add(target.get('node'))
        
        all_connected = connected_sources | connected_targets
        disconnected = set(node_names) - all_connected
        
        if disconnected:
            print(f"   ❌ DISCONNECTED NODES: {list(disconnected)}")
            print(f"   🔍 These nodes are not connected to anything!")
        else:
            print(f"   ✅ All nodes are connected")
        
        # Save the workflow for inspection
        json_output = json.dumps(workflow, indent=2)
        with open('flask_simulation_output.json', 'w') as f:
            f.write(json_output)
        
        print(f"\n📁 Saved to: flask_simulation_output.json")
        
        return len(nodes), len(connections), list(disconnected) if disconnected else []
    
    else:
        print(f"❌ No workflow generated!")
        return 0, 0, []

def main():
    """Run the Flask simulation test"""
    node_count, connection_count, disconnected = test_flask_simulation()
    
    print(f"\n" + "=" * 80)
    if node_count == 2 and connection_count == 1 and not disconnected:
        print("🎉 PERFECT! Workflow matches expected structure")
    elif disconnected:
        print(f"🚨 PROBLEM FOUND: {len(disconnected)} disconnected nodes!")
        print(f"   Disconnected: {disconnected}")
        print(f"   This explains why you see unconnected nodes!")
    else:
        print(f"⚠️ Unexpected structure: {node_count} nodes, {connection_count} connections")

if __name__ == "__main__":
    main()