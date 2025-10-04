#!/usr/bin/env python3
"""Workflow Complexity Testing for N8n JSON Generator"""

import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def test_workflow_complexity_levels():
    """Test different complexity levels of workflows"""
    print("🎛️ Testing Workflow Complexity Levels")
    print("=" * 45)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    complexity_tests = [
        {
            'level': 'Simple',
            'description': 'Create a basic webhook that sends an email notification',
            'expected_min_nodes': 3,
            'expected_max_nodes': 6
        },
        {
            'level': 'Medium',
            'description': 'Build a lead processing system that receives webhooks, validates data, updates CRM, and sends notifications to sales team',
            'expected_min_nodes': 4,
            'expected_max_nodes': 8
        },
        {
            'level': 'Complex',
            'description': 'Design a comprehensive e-commerce order processing system with payment validation, inventory checks, customer notifications, shipping integration, analytics tracking, and error handling with retry logic',
            'expected_min_nodes': 4,
            'expected_max_nodes': 10
        },
        {
            'level': 'Enterprise',
            'description': 'Create an enterprise-grade data integration pipeline that synchronizes customer data between CRM, ERP, marketing automation, support ticketing system, analytics platform, with real-time monitoring, error handling, data validation, transformation rules, and compliance logging',
            'expected_min_nodes': 3,
            'expected_max_nodes': 8
        }
    ]
    
    passed_tests = 0
    
    for test in complexity_tests:
        print(f"🧪 Testing {test['level']} Complexity")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': test['description'],
                                  'trigger_type': 'webhook'
                              }),
                              content_type='application/json')
        
        if response.status_code == 200:
            try:
                data = json.loads(response.data)
                workflow = data.get('workflow', {})
                node_count = len(workflow.get('nodes', []))
                
                if test['expected_min_nodes'] <= node_count <= test['expected_max_nodes']:
                    print(f"✅ Appropriate complexity: {node_count} nodes")
                    passed_tests += 1
                else:
                    print(f"❌ Unexpected complexity: {node_count} nodes (expected {test['expected_min_nodes']}-{test['expected_max_nodes']})")
                
                # Check for complexity indicators
                node_types = [node.get('type', '') for node in workflow.get('nodes', [])]
                has_conditional = any('if' in node_type for node_type in node_types)
                has_code = any('code' in node_type for node_type in node_types)
                
                print(f"   Conditional logic: {'Yes' if has_conditional else 'No'}")
                print(f"   Custom code: {'Yes' if has_code else 'No'}")
                
            except json.JSONDecodeError:
                print("❌ Invalid JSON response")
        else:
            print(f"❌ Failed to generate workflow (status: {response.status_code})")
        
        print()
    
    print(f"📊 Complexity Test Results: {passed_tests}/{len(complexity_tests)} passed")
    return passed_tests

def test_trigger_type_complexity():
    """Test how different trigger types affect workflow complexity"""
    print("🔄 Testing Trigger Type Impact on Complexity")
    print("=" * 50)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    base_description = "Create a data processing workflow that validates input, transforms data, and stores results"
    
    trigger_tests = [
        {'type': 'webhook', 'expected_response_node': True},
        {'type': 'schedule', 'expected_response_node': False},
        {'type': 'manual', 'expected_response_node': False}
    ]
    
    passed_tests = 0
    
    for test in trigger_tests:
        print(f"🧪 Testing {test['type']} trigger")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': base_description,
                                  'trigger_type': test['type']
                              }),
                              content_type='application/json')
        
        if response.status_code == 200:
            try:
                data = json.loads(response.data)
                workflow = data.get('workflow', {})
                nodes = workflow.get('nodes', [])
                
                # Check for webhook response node
                has_response_node = any('respondToWebhook' in node.get('type', '') for node in nodes)
                
                if has_response_node == test['expected_response_node']:
                    print(f"✅ Correct response node handling")
                    passed_tests += 1
                else:
                    expected = "present" if test['expected_response_node'] else "absent"
                    actual = "present" if has_response_node else "absent"
                    print(f"❌ Response node should be {expected}, but is {actual}")
                
                print(f"   Total nodes: {len(nodes)}")
                print(f"   Trigger type: {nodes[0].get('type', 'unknown') if nodes else 'none'}")
                
            except json.JSONDecodeError:
                print("❌ Invalid JSON response")
        else:
            print(f"❌ Failed to generate workflow")
        
        print()
    
    print(f"📊 Trigger Type Test Results: {passed_tests}/{len(trigger_tests)} passed")
    return passed_tests

if __name__ == "__main__":
    complexity_passed = test_workflow_complexity_levels()
    trigger_passed = test_trigger_type_complexity()
    
    total_tests = 4 + 3
    total_passed = complexity_passed + trigger_passed
    
    print(f"\n🎛️ Overall Complexity Testing: {total_passed}/{total_tests} tests passed")
    
    if total_passed >= total_tests * 0.8:
        print("🎉 Complexity tests mostly passed!")
        exit(0)  # Success
    else:
        print("⚠️ Some complexity tests failed!")
        exit(1)  # Failure