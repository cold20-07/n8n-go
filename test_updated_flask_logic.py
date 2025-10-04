#!/usr/bin/env python3
"""
Test Updated Flask Logic
Test the updated Flask app logic with error handling
"""

import json

def test_updated_flask_logic():
    """Test the updated Flask app logic"""
    
    print("🔍 TESTING UPDATED FLASK APP LOGIC")
    print("=" * 80)
    
    description = "Create a workflow that sends a Slack notification when a webhook is triggered"
    trigger_type = "webhook"
    complexity = "simple"
    
    print(f"📝 Input:")
    print(f"   Description: {description}")
    print(f"   Trigger: {trigger_type}")
    print(f"   Complexity: {complexity}")
    
    # Test generator availability
    try:
        from enhanced_workflow_generator import generate_enhanced_workflow
        ENHANCED_GENERATOR_AVAILABLE = True
        print(f"✅ Enhanced generator available")
    except ImportError:
        ENHANCED_GENERATOR_AVAILABLE = False
        print(f"❌ Enhanced generator not available")
    
    try:
        from feature_aware_workflow_generator import generate_feature_aware_workflow
        FEATURE_AWARE_GENERATOR_AVAILABLE = True
        print(f"✅ Feature-aware generator available")
    except ImportError:
        FEATURE_AWARE_GENERATOR_AVAILABLE = False
        print(f"❌ Feature-aware generator not available")
    
    try:
        from trained_workflow_generator import generate_trained_workflow
        TRAINED_GENERATOR_AVAILABLE = True
        print(f"✅ Trained generator available")
    except ImportError:
        TRAINED_GENERATOR_AVAILABLE = False
        print(f"❌ Trained generator not available")
    
    # Simulate the updated generation logic
    print(f"\n🎯 UPDATED GENERATION LOGIC:")
    
    workflow = None
    generation_error = None
    generator_used = None
    
    if ENHANCED_GENERATOR_AVAILABLE:
        try:
            print("🎯 Using enhanced workflow generator")
            workflow = generate_enhanced_workflow(description, trigger_type, complexity)
            print(f"✅ Enhanced generator succeeded: {len(workflow.get('nodes', []))} nodes")
            generator_used = "enhanced"
        except Exception as e:
            print(f"❌ Enhanced generator failed: {e}")
            generation_error = str(e)
            workflow = None
    
    if not workflow and FEATURE_AWARE_GENERATOR_AVAILABLE:
        try:
            print("🎯 Using feature-aware workflow generator")
            workflow = generate_feature_aware_workflow(description, trigger_type, complexity)
            print(f"✅ Feature-aware generator succeeded: {len(workflow.get('nodes', []))} nodes")
            generator_used = "feature_aware"
        except Exception as e:
            print(f"❌ Feature-aware generator failed: {e}")
            generation_error = str(e)
            workflow = None
    
    if not workflow and TRAINED_GENERATOR_AVAILABLE:
        try:
            print("🎯 Using trained workflow generator")
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
        
        import sys
        sys.path.append('.')
        from app import create_basic_workflow
        workflow = create_basic_workflow(description, trigger_type, complexity, '', {})
        print(f"✅ Basic generator succeeded: {len(workflow.get('nodes', []))} nodes")
        generator_used = "basic"
    
    # Analyze the result
    if workflow:
        nodes = workflow.get('nodes', [])
        connections = workflow.get('connections', {})
        
        print(f"\n✅ FINAL RESULT:")
        print(f"   Generator used: {generator_used}")
        print(f"   Total nodes: {len(nodes)}")
        print(f"   Total connections: {len(connections)}")
        
        print(f"\n📋 ALL NODES:")
        for i, node in enumerate(nodes, 1):
            print(f"   {i}. {node.get('name')} ({node.get('type')})")
        
        print(f"\n🔗 ALL CONNECTIONS:")
        for source, conn_data in connections.items():
            targets = conn_data.get('main', [[]])[0]
            for target in targets:
                print(f"   {source} → {target.get('node')}")
        
        # Save result
        json_output = json.dumps(workflow, indent=2)
        with open('updated_flask_test_result.json', 'w') as f:
            f.write(json_output)
        
        print(f"\n📁 Saved to: updated_flask_test_result.json")
        
        return len(nodes), generator_used
    
    return 0, "none"

def main():
    """Run the updated Flask logic test"""
    node_count, generator_used = test_updated_flask_logic()
    
    print(f"\n" + "=" * 80)
    if node_count == 2 and generator_used == "enhanced":
        print("🎉 PERFECT! Enhanced generator working correctly")
        print("✅ You should now see exactly 2 connected nodes")
    elif generator_used == "basic":
        print("🚨 ISSUE: Falling back to basic generator")
        print("❌ This explains the 4 nodes you're seeing")
        print("🔧 Check the error messages above to see why enhanced generator failed")
    else:
        print(f"⚠️ Unexpected result: {node_count} nodes from {generator_used} generator")

if __name__ == "__main__":
    main()