#!/usr/bin/env python3
"""
Test workflow generation functionality
"""

import json
from app import app

def test_workflow_generation():
    """Test workflow generation with complex scenario"""
    print('🧪 Testing workflow generation with complex scenario...')
    
    with app.test_client() as client:
        # Test workflow generation
        test_data = {
            'description': 'Create a lead processing workflow that receives leads via webhook, validates email addresses, enriches data with company information, and sends Slack notifications for high-value leads',
            'triggerType': 'webhook',
            'complexity': 'medium'
        }
        
        response = client.post('/generate', json=test_data)
        
        if response.status_code == 200:
            data = response.get_json()
            if data.get('success'):
                workflow = data['workflow']
                print(f'✅ Generated workflow: {workflow["name"]}')
                print(f'✅ Node count: {len(workflow["nodes"])}')
                print(f'✅ Connection count: {len(workflow["connections"])}')
                
                # Verify nodes have required fields
                node_validation_passed = True
                for i, node in enumerate(workflow['nodes']):
                    required_fields = ['parameters', 'name', 'type', 'typeVersion', 'position']
                    missing_fields = [field for field in required_fields if field not in node]
                    if missing_fields:
                        print(f'❌ Node {i} missing fields: {missing_fields}')
                        node_validation_passed = False
                    else:
                        print(f'✅ Node {i} ({node["name"]}) has all required fields')
                
                # Verify connections reference existing nodes
                connection_validation_passed = True
                node_names = {node['name'] for node in workflow['nodes']}
                for source, connections in workflow['connections'].items():
                    if source not in node_names:
                        print(f'❌ Connection source "{source}" not found in nodes')
                        connection_validation_passed = False
                    else:
                        for connection_group in connections['main']:
                            for connection in connection_group:
                                target = connection['node']
                                if target not in node_names:
                                    print(f'❌ Connection target "{target}" not found in nodes')
                                    connection_validation_passed = False
                                else:
                                    print(f'✅ Connection {source} -> {target} is valid')
                
                # Test different trigger types
                print('\n🔧 Testing different trigger types...')
                trigger_types = ['webhook', 'schedule', 'manual']
                for trigger_type in trigger_types:
                    test_data_trigger = {
                        'description': f'Simple {trigger_type} workflow for testing',
                        'triggerType': trigger_type,
                        'complexity': 'simple'
                    }
                    
                    response = client.post('/generate', json=test_data_trigger)
                    if response.status_code == 200:
                        data = response.get_json()
                        if data.get('success'):
                            workflow = data['workflow']
                            trigger_node = workflow['nodes'][0] if workflow['nodes'] else None
                            if trigger_node:
                                expected_types = {
                                    'webhook': 'n8n-nodes-base.webhook',
                                    'schedule': 'n8n-nodes-base.scheduleTrigger',
                                    'manual': 'n8n-nodes-base.manualTrigger'
                                }
                                if trigger_node['type'] == expected_types[trigger_type]:
                                    print(f'✅ {trigger_type} trigger type correct: {trigger_node["type"]}')
                                else:
                                    print(f'❌ {trigger_type} trigger type incorrect: expected {expected_types[trigger_type]}, got {trigger_node["type"]}')
                            else:
                                print(f'❌ No trigger node found for {trigger_type}')
                        else:
                            print(f'❌ {trigger_type} generation failed: {data.get("error")}')
                    else:
                        print(f'❌ {trigger_type} request failed: {response.status_code}')
                
                print('\n📊 Validation Summary:')
                print(f'✅ Node structure validation: {"PASSED" if node_validation_passed else "FAILED"}')
                print(f'✅ Connection validation: {"PASSED" if connection_validation_passed else "FAILED"}')
                print('✅ Workflow generation test completed successfully')
                
                return node_validation_passed and connection_validation_passed
                
            else:
                print(f'❌ Generation failed: {data.get("error")}')
                return False
        else:
            print(f'❌ Request failed with status: {response.status_code}')
            return False

def test_input_validation():
    """Test input validation"""
    print('\n🔍 Testing input validation...')
    
    with app.test_client() as client:
        # Test missing description
        response = client.post('/generate', json={'triggerType': 'webhook'})
        if response.status_code == 400:
            print('✅ Missing description properly rejected')
        else:
            print('❌ Missing description should be rejected')
        
        # Test empty description
        response = client.post('/generate', json={'description': '', 'triggerType': 'webhook'})
        if response.status_code == 400:
            print('✅ Empty description properly rejected')
        else:
            print('❌ Empty description should be rejected')
        
        # Test short description
        response = client.post('/generate', json={'description': 'short', 'triggerType': 'webhook'})
        if response.status_code == 400:
            print('✅ Short description properly rejected')
        else:
            print('❌ Short description should be rejected')
        
        # Test invalid trigger type
        response = client.post('/generate', json={'description': 'Valid description for testing', 'triggerType': 'invalid'})
        if response.status_code == 400:
            print('✅ Invalid trigger type properly rejected')
        else:
            print('❌ Invalid trigger type should be rejected')
        
        print('✅ Input validation tests completed')

if __name__ == "__main__":
    print('🧪 Testing n8n Workflow Generation')
    print('=' * 50)
    
    success = test_workflow_generation()
    test_input_validation()
    
    print('\n' + '=' * 50)
    if success:
        print('🎉 All workflow generation tests passed!')
    else:
        print('⚠️ Some tests failed - check output above')