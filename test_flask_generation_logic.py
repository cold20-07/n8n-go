#!/usr/bin/env python3
"""
Test Flask Generation Logic
Simulate the exact Flask generation logic to find where it's failing
"""

import json

def simulate_flask_generation():
    """Simulate the exact Flask generation process"""
    
    print("🔍 SIMULATING FLASK GENERATION LOGIC")
    print("=" * 80)
    
    # Simulate the exact request data that Flask receives
    data = {
        "description": "Create a workflow that sends a Slack notification when a webhook is triggered",
        "trigger_type": "webhook", 
        "complexity": "simple"
    }
    
    print(f"📝 Request data: {data}")
    
    # Step 1: Import generators (like Flask does)
    try:
        from enhanced_workflow_generator import generate_enhanced_workflow
        ENHANCED_GENERATOR_AVAILABLE = True
        print("✅ Enhanced generator imported successfully")
    except ImportError as e:
        ENHANCED_GENERATOR_AVAILABLE = False
        print(f"❌ Enhanced generator import failed: {e}")
    
    try:
        from feature_aware_workflow_generator import generate_feature_aware_workflow
        FEATURE_AWARE_GENERATOR_AVAILABLE = True
        print("✅ Feature-aware generator imported successfully")
    except ImportError as e:
        FEATURE_AWARE_GENERATOR_AVAILABLE = False
        print(f"❌ Feature-aware generator import failed: {e}")
    
    try:
        from trained_workflow_generator import generate_trained_workflow
        TRAINED_GENERATOR_AVAILABLE = True
        print("✅ Trained generator imported successfully")
    except ImportError as e:
        TRAINED_GENERATOR_AVAILABLE = False
        print(f"❌ Trained generator import failed: {e}")
    
    # Step 2: Extract parameters (like Flask does)
    description = data.get('description', '').strip()
    trigger_type = data.get('trigger_type', 'webhook')
    complexity = data.get('complexity', 'medium')
    
    print(f"\n📋 Extracted parameters:")
    print(f"   Description: {description}")
    print(f"   Trigger: {trigger_type}")
    print(f"   Complexity: {complexity}")
    
    # Step 3: Generation logic (exactly like Flask)
    print(f"\n🎯 GENERATION PROCESS:")
    
    workflow = None
    generation_error = None
    generator_used = None
    
    if ENHANCED_GENERATOR_AVAILABLE:
        try:
            print("🎯 Attempting enhanced workflow generator...")
            workflow = generate_enhanced_workflow(description, trigger_type, complexity)
            print(f"✅ Enhanced generator succeeded: {len(workflow.get('nodes', []))} nodes")
            generator_used = "enhanced"
        except Exception as e:
            print(f"❌ Enhanced generator failed: {e}")
            import traceback
            traceback.print_exc()
            generation_error = str(e)
            workflow = None
    
    if not workflow and FEATURE_AWARE_GENERATOR_AVAILABLE:
        try:
            print("🎯 Attempting feature-aware workflow generator...")
            workflow = generate_feature_aware_workflow(description, trigger_type, complexity)
            print(f"✅ Feature-aware generator succeeded: {len(workflow.get('nodes', []))} nodes")
            generator_used = "feature_aware"
        except Exception as e:
            print(f"❌ Feature-aware generator failed: {e}")
            generation_error = str(e)
            workflow = None
    
    if not workflow and TRAINED_GENERATOR_AVAILABLE:
        try:
            print("🎯 Attempting trained workflow generator...")
            workflow = generate_trained_workflow(description, trigger_type, complexity)
            print(f"✅ Trained generator succeeded: {len(workflow.get('nodes', []))} nodes")
            generator_used = "trained"
        except Exception as e:
            print(f"❌ Trained generator failed: {e}")
            generation_error = str(e)
            workflow = None
    
    if not workflow:
        print("⚠️ All advanced generators failed, falling back to basic workflow generation")
        if generation_error:
            print(f"   Last error: {generation_error}")
        
        # Import basic generator
        from app import create_basic_workflow
        workflow = create_basic_workflow(description, trigger_type, complexity, '', {})
        print(f"✅ Basic generator succeeded: {len(workflow.get('nodes', []))} nodes")
        generator_used = "basic"
    
    # Step 4: Analyze result
    if workflow:
        nodes = workflow.get('nodes', [])
        connections = workflow.get('connections', {})
        
        print(f"\n📊 FINAL RESULT:")
        print(f"   Generator used: {generator_used}")
        print(f"   Total nodes: {len(nodes)}")
        print(f"   Total connections: {len(connections)}")
        
        print(f"\n📋 NODES:")
        for i, node in enumerate(nodes, 1):
            print(f"   {i}. {node.get('name', 'Unknown')} ({node.get('type', 'Unknown')})")
        
        print(f"\n🔗 CONNECTIONS:")
        if connections:
            for source, conn_data in connections.items():
                targets = conn_data.get('main', [[]])[0]
                for target in targets:
                    target_name = target.get('node', 'Unknown')
                    print(f"   {source} → {target_name}")
        else:
            print("   ❌ NO CONNECTIONS!")
        
        # Check for disconnected nodes
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
            print(f"\n🚨 DISCONNECTED NODES: {list(disconnected)}")
        else:
            print(f"\n✅ ALL NODES CONNECTED")
        
        # Save result
        with open('flask_simulation_result.json', 'w') as f:
            json.dump(workflow, f, indent=2)
        
        print(f"\n📁 Saved to: flask_simulation_result.json")
        
        return generator_used, len(nodes), len(connections), list(disconnected) if disconnected else []
    
    return "none", 0, 0, []

def main():
    """Run the Flask simulation"""
    generator, nodes, connections, disconnected = simulate_flask_generation()
    
    print(f"\n" + "=" * 80)
    print("🎯 ANALYSIS:")
    
    if generator == "enhanced" and nodes == 2 and connections == 1 and not disconnected:
        print("🎉 PERFECT! Enhanced generator working in Flask simulation")
        print("✅ The issue is NOT in the generation logic")
        print("🔍 Check the frontend or n8n import process")
    elif generator == "basic":
        print("🚨 PROBLEM: Flask is falling back to basic generator!")
        print("❌ This explains the disconnected nodes you're seeing")
        print("🔧 The enhanced generator is failing in Flask context")
    elif disconnected:
        print(f"🚨 PROBLEM: {len(disconnected)} nodes are disconnected!")
        print(f"   Disconnected: {disconnected}")
        print("🔧 Connection logic needs fixing")
    else:
        print(f"⚠️ Unexpected result: {generator} generator, {nodes} nodes, {connections} connections")

if __name__ == "__main__":
    main()