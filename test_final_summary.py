#!/usr/bin/env python3
"""Final Summary Test - Complete N8n JSON Generator Testing"""

import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def comprehensive_test():
    """Run a comprehensive test of all functionality"""
    print("🎯 FINAL COMPREHENSIVE TEST")
    print("=" * 50)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    test_results = {
        'api_endpoint': False,
        'workflow_generation': False,
        'node_creation': False,
        'connection_creation': False,
        'trigger_types': {'webhook': False, 'schedule': False, 'manual': False},
        'response_format': False,
        'json_validity': False
    }
    
    # Test 1: API Endpoint
    print("1️⃣ Testing API Endpoint...")
    response = client.post('/generate',
                          data=json.dumps({
                              'description': 'Create a comprehensive workflow for testing',
                              'trigger_type': 'webhook'
                          }),
                          content_type='application/json')
    
    if response.status_code == 200:
        test_results['api_endpoint'] = True
        print("✅ API endpoint working")
    else:
        print(f"❌ API endpoint failed: {response.status_code}")
        return test_results
    
    # Test 2: Response Format
    print("2️⃣ Testing Response Format...")
    try:
        data = json.loads(response.data)
        required_keys = ['filename', 'formatted_json', 'success', 'workflow']
        
        if all(key in data for key in required_keys):
            test_results['response_format'] = True
            print("✅ Response format correct")
        else:
            print(f"❌ Missing keys: {set(required_keys) - set(data.keys())}")
    except:
        print("❌ Invalid JSON response")
        return test_results
    
    # Test 3: Workflow Generation
    print("3️⃣ Testing Workflow Generation...")
    workflow = data.get('workflow', {})
    
    if isinstance(workflow, dict) and 'nodes' in workflow:
        test_results['workflow_generation'] = True
        print("✅ Workflow structure present")
        
        # Test 4: Node Creation
        print("4️⃣ Testing Node Creation...")
        nodes = workflow.get('nodes', [])
        if len(nodes) > 0:
            test_results['node_creation'] = True
            print(f"✅ Generated {len(nodes)} nodes")
            
            # Show node details
            for i, node in enumerate(nodes[:3]):
                print(f"   Node {i+1}: {node.get('name', 'unnamed')} ({node.get('type', 'unknown')})")
        else:
            print("❌ No nodes generated")
        
        # Test 5: Connection Creation
        print("5️⃣ Testing Connection Creation...")
        connections = workflow.get('connections', {})
        if connections:
            test_results['connection_creation'] = True
            print(f"✅ Generated connections: {len(connections)} connection groups")
        else:
            print("❌ No connections generated")
    else:
        print("❌ Invalid workflow structure")
    
    # Test 6: JSON Validity
    print("6️⃣ Testing JSON Validity...")
    formatted_json = data.get('formatted_json', '')
    try:
        parsed_json = json.loads(formatted_json)
        if 'nodes' in parsed_json and len(parsed_json['nodes']) > 0:
            test_results['json_validity'] = True
            print("✅ Formatted JSON is valid and contains nodes")
        else:
            print("❌ Formatted JSON missing nodes")
    except:
        print("❌ Formatted JSON is invalid")
    
    # Test 7: All Trigger Types
    print("7️⃣ Testing All Trigger Types...")
    for trigger_type in ['webhook', 'schedule', 'manual']:
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': f'Create a {trigger_type} workflow for testing',
                                  'trigger_type': trigger_type
                              }),
                              content_type='application/json')
        
        if response.status_code == 200:
            try:
                data = json.loads(response.data)
                workflow = data.get('workflow', {})
                nodes = workflow.get('nodes', [])
                
                if len(nodes) > 0:
                    # Check if first node has correct trigger type
                    first_node_type = nodes[0].get('type', '')
                    expected_types = {
                        'webhook': 'n8n-nodes-base.webhook',
                        'schedule': 'n8n-nodes-base.scheduleTrigger',
                        'manual': 'n8n-nodes-base.manualTrigger'
                    }
                    
                    if first_node_type == expected_types[trigger_type]:
                        test_results['trigger_types'][trigger_type] = True
                        print(f"✅ {trigger_type} trigger working")
                    else:
                        print(f"❌ {trigger_type} trigger wrong type: {first_node_type}")
                else:
                    print(f"❌ {trigger_type} trigger no nodes")
            except:
                print(f"❌ {trigger_type} trigger invalid response")
        else:
            print(f"❌ {trigger_type} trigger failed")
    
    return test_results

def print_final_results(results):
    """Print final test results"""
    print("\n" + "="*60)
    print("🏆 FINAL TEST RESULTS")
    print("="*60)
    
    total_tests = 0
    passed_tests = 0
    
    # Core functionality
    core_tests = [
        ('API Endpoint', results['api_endpoint']),
        ('Response Format', results['response_format']),
        ('Workflow Generation', results['workflow_generation']),
        ('Node Creation', results['node_creation']),
        ('Connection Creation', results['connection_creation']),
        ('JSON Validity', results['json_validity'])
    ]
    
    print("\n🔧 Core Functionality:")
    for test_name, passed in core_tests:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name}: {status}")
        total_tests += 1
        if passed:
            passed_tests += 1
    
    # Trigger types
    print("\n🔄 Trigger Types:")
    for trigger_type, passed in results['trigger_types'].items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {trigger_type.capitalize()}: {status}")
        total_tests += 1
        if passed:
            passed_tests += 1
    
    # Overall score
    success_rate = (passed_tests / total_tests) * 100
    print(f"\n📊 OVERALL SCORE: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
    
    if success_rate >= 90:
        print("🎉 EXCELLENT! Your N8n JSON Generator is working perfectly!")
    elif success_rate >= 75:
        print("✅ GOOD! Your N8n JSON Generator is working well with minor issues.")
    elif success_rate >= 50:
        print("⚠️ FAIR! Your N8n JSON Generator has some functionality but needs improvement.")
    else:
        print("❌ POOR! Your N8n JSON Generator needs significant fixes.")
    
    print("\n🚀 Ready for production use!" if success_rate >= 75 else "\n🔧 Needs more work before production.")

if __name__ == "__main__":
    results = comprehensive_test()
    print_final_results(results)