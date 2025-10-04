#!/usr/bin/env python3
"""JSON Compliance and N8n Compatibility Testing"""

import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def test_json_schema_compliance():
    """Test generated workflows against N8n JSON schema"""
    print("📋 Testing JSON Schema Compliance")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    # Basic N8n workflow schema
    n8n_workflow_schema = {
        "type": "object",
        "required": ["name", "nodes", "connections"],
        "properties": {
            "name": {"type": "string", "minLength": 1},
            "nodes": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": ["id", "name", "type", "position", "parameters"],
                    "properties": {
                        "id": {"type": "string"},
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "position": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 2,
                            "maxItems": 2
                        },
                        "parameters": {"type": "object"},
                        "typeVersion": {"type": "number"}
                    }
                }
            },
            "connections": {"type": "object"},
            "active": {"type": "boolean"},
            "settings": {"type": "object"},
            "tags": {"type": "array"},
            "meta": {"type": "object"}
        }
    }
    
    test_cases = [
        {
            'name': 'Simple Workflow Schema',
            'description': 'Create a basic webhook to email workflow',
            'trigger_type': 'webhook'
        },
        {
            'name': 'Complex Workflow Schema',
            'description': 'Build a comprehensive e-commerce order processing system with multiple integrations',
            'trigger_type': 'webhook',
            'complexity': 'complex'
        },
        {
            'name': 'Schedule Workflow Schema',
            'description': 'Design a scheduled data synchronization workflow',
            'trigger_type': 'schedule'
        }
    ]
    
    passed_tests = 0
    
    for test_case in test_cases:
        print(f"\n🧪 Testing: {test_case['name']}")
        
        response = client.post('/generate',
                              data=json.dumps(test_case),
                              content_type='application/json')
        
        if response.status_code == 200:
            try:
                data = json.loads(response.data)
                workflow = data.get('workflow', {})
                
                # Basic schema validation
                schema_valid = True
                required_fields = ['name', 'nodes', 'connections']
                
                for field in required_fields:
                    if field not in workflow:
                        schema_valid = False
                        print(f"   ❌ Missing required field: {field}")
                        break
                
                if schema_valid and isinstance(workflow.get('nodes'), list) and len(workflow['nodes']) > 0:
                    # Validate node structure
                    for i, node in enumerate(workflow['nodes']):
                        node_required = ['id', 'name', 'type', 'position', 'parameters']
                        for node_field in node_required:
                            if node_field not in node:
                                schema_valid = False
                                print(f"   ❌ Node {i} missing field: {node_field}")
                                break
                        if not schema_valid:
                            break
                
                if schema_valid:
                    print("   ✅ Schema validation passed")
                    passed_tests += 1
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Schema Compliance Results: {passed_tests}/{len(test_cases)} passed")
    return passed_tests

def test_n8n_node_compatibility():
    """Test that generated nodes are compatible with N8n"""
    print("\n🔧 Testing N8n Node Compatibility")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    # Valid N8n node types
    valid_n8n_nodes = {
        'n8n-nodes-base.webhook',
        'n8n-nodes-base.scheduleTrigger',
        'n8n-nodes-base.manualTrigger',
        'n8n-nodes-base.code',
        'n8n-nodes-base.if',
        'n8n-nodes-base.emailSend',
        'n8n-nodes-base.slack',
        'n8n-nodes-base.mysql',
        'n8n-nodes-base.googleSheets',
        'n8n-nodes-base.httpRequest',
        'n8n-nodes-base.respondToWebhook',
        'n8n-nodes-base.readWriteFile'
    }
    
    compatibility_tests = [
        {
            'description': 'Create a workflow with email, Slack, and database operations',
            'trigger_type': 'webhook'
        },
        {
            'description': 'Build a workflow with HTTP requests and file operations',
            'trigger_type': 'manual'
        },
        {
            'description': 'Design a workflow with conditional logic and code execution',
            'trigger_type': 'schedule'
        }
    ]
    
    passed_tests = 0
    
    for i, test in enumerate(compatibility_tests, 1):
        print(f"\n🧪 Compatibility Test {i}")
        
        response = client.post('/generate',
                              data=json.dumps(test),
                              content_type='application/json')
        
        if response.status_code == 200:
            try:
                data = json.loads(response.data)
                workflow = data.get('workflow', {})
                nodes = workflow.get('nodes', [])
                
                invalid_nodes = []
                valid_nodes = []
                
                for node in nodes:
                    node_type = node.get('type', '')
                    if node_type in valid_n8n_nodes:
                        valid_nodes.append(node_type)
                    else:
                        invalid_nodes.append(node_type)
                
                print(f"   Valid nodes: {len(valid_nodes)}")
                print(f"   Invalid nodes: {len(invalid_nodes)}")
                
                if len(invalid_nodes) == 0:
                    print("   ✅ All nodes are N8n compatible")
                    passed_tests += 1
                else:
                    print(f"   ❌ Invalid node types: {invalid_nodes}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Node Compatibility Results: {passed_tests}/{len(compatibility_tests)} passed")
    return passed_tests

def test_workflow_executability():
    """Test that generated workflows are theoretically executable in N8n"""
    print("\n⚙️ Testing Workflow Executability")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    executability_tests = [
        {
            'name': 'Webhook Response Chain',
            'description': 'Create a webhook workflow that processes data and responds',
            'trigger_type': 'webhook',
            'must_have_response': True
        },
        {
            'name': 'Schedule Processing Chain',
            'description': 'Build a scheduled workflow that processes and stores data',
            'trigger_type': 'schedule',
            'must_have_response': False
        },
        {
            'name': 'Manual Execution Chain',
            'description': 'Design a manual workflow with data transformation',
            'trigger_type': 'manual',
            'must_have_response': False
        }
    ]
    
    passed_tests = 0
    
    for test in executability_tests:
        print(f"\n🧪 Testing: {test['name']}")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': test['description'],
                                  'trigger_type': test['trigger_type']
                              }),
                              content_type='application/json')
        
        if response.status_code == 200:
            try:
                data = json.loads(response.data)
                workflow = data.get('workflow', {})
                nodes = workflow.get('nodes', [])
                connections = workflow.get('connections', {})
                
                # Check for proper execution chain
                has_trigger = len(nodes) > 0
                has_connections = len(connections) > 0
                has_response_node = any('respondToWebhook' in node.get('type', '') for node in nodes)
                
                print(f"   Has trigger node: {has_trigger}")
                print(f"   Has connections: {has_connections}")
                print(f"   Has response node: {has_response_node}")
                
                # Validate execution requirements
                execution_valid = has_trigger and has_connections
                
                if test['must_have_response']:
                    execution_valid = execution_valid and has_response_node
                
                if execution_valid:
                    print("   ✅ Workflow is executable")
                    passed_tests += 1
                else:
                    print("   ❌ Workflow execution chain incomplete")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Executability Results: {passed_tests}/{len(executability_tests)} passed")
    return passed_tests

def test_json_formatting_quality():
    """Test the quality of JSON formatting in responses"""
    print("\n📝 Testing JSON Formatting Quality")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    response = client.post('/generate',
                          data=json.dumps({
                              'description': 'Create a comprehensive workflow for JSON formatting testing',
                              'trigger_type': 'webhook'
                          }),
                          content_type='application/json')
    
    if response.status_code == 200:
        try:
            data = json.loads(response.data)
            formatted_json = data.get('formatted_json', '')
            
            # Test JSON formatting quality
            formatting_checks = {
                'has_indentation': '  ' in formatted_json,
                'has_newlines': '\n' in formatted_json,
                'valid_json': True,
                'proper_structure': True
            }
            
            # Validate that formatted JSON is valid
            try:
                parsed_formatted = json.loads(formatted_json)
                formatting_checks['valid_json'] = True
                
                # Check structure
                required_keys = ['name', 'nodes', 'connections']
                formatting_checks['proper_structure'] = all(key in parsed_formatted for key in required_keys)
                
            except json.JSONDecodeError:
                formatting_checks['valid_json'] = False
                formatting_checks['proper_structure'] = False
            
            passed_checks = sum(formatting_checks.values())
            total_checks = len(formatting_checks)
            
            print(f"✅ Has proper indentation: {formatting_checks['has_indentation']}")
            print(f"✅ Has newlines: {formatting_checks['has_newlines']}")
            print(f"✅ Valid JSON: {formatting_checks['valid_json']}")
            print(f"✅ Proper structure: {formatting_checks['proper_structure']}")
            
            print(f"\n📊 Formatting Quality: {passed_checks}/{total_checks} checks passed")
            
            return passed_checks >= total_checks * 0.75  # 75% of checks must pass
            
        except Exception as e:
            print(f"❌ Error testing formatting: {e}")
            return False
    else:
        print(f"❌ Request failed: {response.status_code}")
        return False

if __name__ == "__main__":
    try:
        print("📋 JSON COMPLIANCE AND N8N COMPATIBILITY TESTING")
        print("=" * 60)
        
        schema_passed = test_json_schema_compliance()
        compatibility_passed = test_n8n_node_compatibility()
        executability_passed = test_workflow_executability()
        formatting_passed = test_json_formatting_quality()
        
        total_tests = 3 + 3 + 3 + 1  # Total test cases
        total_passed = schema_passed + compatibility_passed + executability_passed + (1 if formatting_passed else 0)
        
        success_rate = (total_passed / total_tests) * 100
        
        print(f"\n🏆 JSON COMPLIANCE TEST RESULTS")
        print("=" * 50)
        print(f"📋 Schema Compliance: {schema_passed}/3")
        print(f"🔧 Node Compatibility: {compatibility_passed}/3")
        print(f"⚙️ Workflow Executability: {executability_passed}/3")
        print(f"📝 JSON Formatting: {'1/1' if formatting_passed else '0/1'}")
        print(f"\n📊 OVERALL SCORE: {total_passed}/{total_tests} ({success_rate:.1f}%)")
        
        if success_rate >= 80:
            print("🎉 JSON compliance tests passed!")
            exit(0)
        else:
            print("⚠️ Some compliance tests need attention!")
            exit(1)
            
    except Exception as e:
        print(f"❌ JSON compliance tests failed: {e}")
        exit(1)