#!/usr/bin/env python3
"""
Quick test of core N8N Workflow Generator functionality
"""
import sys
import json
from pathlib import Path

def test_market_leading_generator():
    """Test the market-leading workflow generator"""
    print("🧪 Testing Market-Leading Workflow Generator...")
    
    try:
        # Import the generator
        sys.path.append('src/core/generators')
        from market_leading_workflow_generator import generate_market_leading_workflow
        
        # Test basic workflow generation
        description = "Process customer orders and send notifications"
        trigger_type = "webhook"
        complexity = "medium"
        
        print(f"   📝 Description: {description}")
        print(f"   🔗 Trigger: {trigger_type}")
        print(f"   ⚙️  Complexity: {complexity}")
        
        # Generate workflow
        workflow = generate_market_leading_workflow(description, trigger_type, complexity)
        
        # Validate workflow structure
        required_fields = ['id', 'name', 'nodes', 'connections']
        missing_fields = [field for field in required_fields if field not in workflow]
        
        if missing_fields:
            print(f"   ❌ Missing required fields: {missing_fields}")
            return False
        
        nodes = workflow.get('nodes', [])
        connections = workflow.get('connections', {})
        
        print(f"   ✅ Generated workflow: {workflow.get('name')}")
        print(f"   📊 Nodes: {len(nodes)}")
        print(f"   🔗 Connections: {len(connections)}")
        
        # Validate nodes
        for i, node in enumerate(nodes, 1):
            node_name = node.get('name', f'Node {i}')
            node_type = node.get('type', 'unknown')
            print(f"      {i}. {node_name} ({node_type})")
        
        # Validate connections
        connection_count = 0
        for source, conn_data in connections.items():
            if 'main' in conn_data and conn_data['main']:
                for group in conn_data['main']:
                    if isinstance(group, list):
                        for conn in group:
                            if isinstance(conn, dict):
                                target = conn.get('node', 'unknown')
                                print(f"      🔗 {source} → {target}")
                                connection_count += 1
        
        print(f"   📈 Total connections: {connection_count}")
        
        # Check for production features
        production_features = []
        
        # Check for error handling
        if any('error' in node.get('name', '').lower() for node in nodes):
            production_features.append("Error Handling")
        
        # Check for validation
        if any('validation' in node.get('name', '').lower() for node in nodes):
            production_features.append("Input Validation")
        
        # Check for monitoring
        if any('monitor' in node.get('name', '').lower() for node in nodes):
            production_features.append("Performance Monitoring")
        
        # Check for retry settings
        retry_nodes = [node for node in nodes if node.get('retryOnFail')]
        if retry_nodes:
            production_features.append(f"Retry Logic ({len(retry_nodes)} nodes)")
        
        print(f"   🚀 Production features: {', '.join(production_features) if production_features else 'Basic'}")
        
        # Validate JSON structure
        try:
            json_str = json.dumps(workflow, indent=2)
            print(f"   ✅ Valid JSON structure ({len(json_str)} chars)")
        except Exception as e:
            print(f"   ❌ Invalid JSON structure: {e}")
            return False
        
        print("   ✅ Market-Leading Generator: PASSED")
        return True
        
    except Exception as e:
        print(f"   ❌ Market-Leading Generator failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_app_import():
    """Test basic app import"""
    print("🧪 Testing Basic App Import...")
    
    try:
        from app import app
        print("   ✅ App import: PASSED")
        return True
    except Exception as e:
        print(f"   ❌ App import failed: {e}")
        return False

def test_training_data():
    """Test training data availability"""
    print("🧪 Testing Training Data...")
    
    try:
        dataset_path = Path('training_data/comprehensive_n8n_dataset.json')
        if dataset_path.exists():
            with open(dataset_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"   ✅ Training dataset loaded")
            print(f"   📊 Workflow patterns: {len(data.get('workflow_patterns', []))}")
            print(f"   🔧 Node types: {len(data.get('node_types', []))}")
            print(f"   📋 Best practices: {len(data.get('best_practices', []))}")
            print(f"   🌍 Real examples: {len(data.get('real_world_examples', []))}")
            return True
        else:
            print(f"   ⚠️  Training dataset not found at {dataset_path}")
            return False
            
    except Exception as e:
        print(f"   ❌ Training data test failed: {e}")
        return False

def main():
    """Run all core functionality tests"""
    print("🚀 N8N Workflow Generator - Core Functionality Test")
    print("=" * 60)
    
    tests = [
        test_basic_app_import,
        test_training_data,
        test_market_leading_generator
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
            print()
        except Exception as e:
            print(f"   ❌ Test failed with exception: {e}")
            results.append(False)
            print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("=" * 60)
    print(f"📊 Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("🎉 All core functionality tests PASSED!")
        print("✅ The N8N Workflow Generator is working correctly!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)