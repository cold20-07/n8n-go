#!/usr/bin/env python3
"""Workflow Validation Testing for N8n JSON Generator"""

import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def validate_workflow_structure(workflow):
    """Validate the structure of generated workflow"""
    required_fields = ['name', 'nodes', 'connections', 'tags']
    
    for field in required_fields:
        if field not in workflow:
            return False, f"Missing required field: {field}"
    
    # Validate nodes
    if not isinstance(workflow['nodes'], list) or len(workflow['nodes']) == 0:
        return False, "Nodes must be a non-empty list"
    
    # Validate each node
    for i, node in enumerate(workflow['nodes']):
        node_required = ['id', 'name', 'type', 'position', 'parameters']
        for field in node_required:
            if field not in node:
                return False, f"Node {i} missing field: {field}"
    
    # Validate connections
    if not isinstance(workflow['connections'], dict):
        return False, "Connections must be a dictionary"
    
    return True, "Valid workflow structure"

def test_workflow_schemas():
    """Test different workflow generation scenarios"""
    print("📋 Testing Workflow Schema Validation")
    print("=" * 50)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    test_scenarios = [
        {
            'name': 'E-commerce Order Processing',
            'description': 'Create an order processing workflow with payment validation and inventory management',
            'trigger_type': 'webhook'
        },
        {
            'name': 'Data Synchronization',
            'description': 'Build a data sync workflow between CRM and marketing automation platform',
            'trigger_type': 'schedule'
        },
        {
            'name': 'Customer Support Automation',
            'description': 'Design a support ticket routing system with priority classification',
            'trigger_type': 'manual'
        },
        {
            'name': 'Social Media Monitoring',
            'description': 'Create a social media monitoring workflow with sentiment analysis and response automation',
            'trigger_type': 'webhook'
        }
    ]
    
    passed_tests = 0
    
    for scenario in test_scenarios:
        print(f"🧪 Testing: {scenario['name']}")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': scenario['description'],
                                  'trigger_type': scenario['trigger_type']
                              }),
                              content_type='application/json')
        
        if response.status_code != 200:
            print(f"❌ Failed to generate workflow")
            continue
        
        try:
            data = json.loads(response.data)
            # Get the actual workflow from the response structure
            workflow = data.get('workflow', {})
            is_valid, message = validate_workflow_structure(workflow)
            
            if is_valid:
                print(f"✅ Valid workflow generated")
                print(f"   Nodes: {len(workflow['nodes'])}")
                print(f"   Connections: {len(workflow.get('connections', {}))}")
                print(f"   Tags: {len(workflow.get('tags', []))}")
                passed_tests += 1
            else:
                print(f"❌ Invalid workflow: {message}")
                
        except json.JSONDecodeError:
            print(f"❌ Invalid JSON response")
        
        print()
    
    print(f"📊 Schema Validation Results: {passed_tests}/{len(test_scenarios)} passed")
    return passed_tests == len(test_scenarios)

def test_node_type_validation():
    """Test that generated nodes use valid N8n node types"""
    print("🔧 Testing Node Type Validation")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    valid_node_types = [
        'n8n-nodes-base.webhook',
        'n8n-nodes-base.scheduleTrigger',
        'n8n-nodes-base.manualTrigger',
        'n8n-nodes-base.code',
        'n8n-nodes-base.if',
        'n8n-nodes-base.emailSend',
        'n8n-nodes-base.slack',
        'n8n-nodes-base.mysql',
        'n8n-nodes-base.googleSheets',
        'n8n-nodes-base.respondToWebhook'
    ]
    
    response = client.post('/generate',
                          data=json.dumps({
                              'description': 'Create a comprehensive workflow with multiple node types',
                              'trigger_type': 'webhook'
                          }),
                          content_type='application/json')
    
    if response.status_code == 200:
        data = json.loads(response.data)
        workflow = data.get('workflow', {})
        invalid_nodes = []
        
        for node in workflow.get('nodes', []):
            if node.get('type') not in valid_node_types:
                invalid_nodes.append(node.get('type'))
        
        if not invalid_nodes:
            print("✅ All node types are valid")
            return True
        else:
            print(f"❌ Invalid node types found: {invalid_nodes}")
            return False
    else:
        print("❌ Failed to generate workflow for validation")
        return False

if __name__ == "__main__":
    schema_passed = test_workflow_schemas()
    node_types_passed = test_node_type_validation()
    
    if schema_passed and node_types_passed:
        print("🎉 All validation tests passed!")
        exit(0)  # Success
    else:
        print("⚠️ Some validation tests failed!")
        exit(1)  # Failure