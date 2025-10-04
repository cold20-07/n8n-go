#!/usr/bin/env python3
"""
Perfection Verification Test - 100% Comprehensive Testing
Tests all fixes and ensures 100% functionality
"""

import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def test_trigger_type_fixes():
    """Test that all trigger types work correctly"""
    print("🔧 Testing Trigger Type Fixes")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    trigger_tests = [
        {
            'name': 'Webhook Trigger',
            'trigger_type': 'webhook',
            'expected_type': 'n8n-nodes-base.webhook'
        },
        {
            'name': 'Schedule Trigger',
            'trigger_type': 'schedule',
            'expected_type': 'n8n-nodes-base.scheduleTrigger'
        },
        {
            'name': 'Manual Trigger',
            'trigger_type': 'manual',
            'expected_type': 'n8n-nodes-base.manualTrigger'
        }
    ]
    
    passed = 0
    
    for test in trigger_tests:
        print(f"🧪 Testing {test['name']}...")
        
        # Test with both parameter formats
        for param_format in ['triggerType', 'trigger_type']:
            response = client.post('/generate',
                                  data=json.dumps({
                                      'description': f'Create a comprehensive {test["trigger_type"]} workflow for testing',
                                      param_format: test['trigger_type']
                                  }),
                                  content_type='application/json')
            
            if response.status_code == 200:
                try:
                    data = json.loads(response.data)
                    workflow = data.get('workflow', {})
                    nodes = workflow.get('nodes', [])
                    
                    if len(nodes) > 0:
                        trigger_node = nodes[0]
                        actual_type = trigger_node.get('type')
                        
                        if actual_type == test['expected_type']:
                            print(f"✅ {param_format}: Correct type {actual_type}")
                            passed += 1
                        else:
                            print(f"❌ {param_format}: Wrong type {actual_type} (expected {test['expected_type']})")
                    else:
                        print(f"❌ {param_format}: No nodes generated")
                except:
                    print(f"❌ {param_format}: Invalid response")
            else:
                print(f"❌ {param_format}: Request failed ({response.status_code})")
        
        print()
    
    print(f"📊 Trigger Type Results: {passed}/6 tests passed")
    return passed

def test_security_fixes():
    """Test security sanitization"""
    print("🛡️ Testing Security Fixes")
    print("=" * 30)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    security_tests = [
        {
            'name': 'Script Injection',
            'description': 'Create workflow <script>alert("xss")</script> with malicious content',
            'should_be_sanitized': True
        },
        {
            'name': 'SQL Injection',
            'description': "Create workflow'; DROP TABLE users; -- with SQL injection",
            'should_be_sanitized': True
        },
        {
            'name': 'Command Injection',
            'description': 'Create workflow; rm -rf / with command injection',
            'should_be_sanitized': True
        },
        {
            'name': 'Path Traversal',
            'description': 'Create workflow ../../etc/passwd with path traversal',
            'should_be_sanitized': True
        },
        {
            'name': 'Normal Content',
            'description': 'Create a normal workflow for processing customer data safely',
            'should_be_sanitized': False
        }
    ]
    
    passed = 0
    
    for test in security_tests:
        print(f"🧪 Testing {test['name']}...")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': test['description'],
                                  'trigger_type': 'webhook'
                              }),
                              content_type='application/json')
        
        if response.status_code == 200:
            try:
                data = json.loads(response.data)
                response_str = json.dumps(data)
                
                dangerous_patterns = ['<script>', 'DROP TABLE', 'rm -rf', '../../']
                has_dangerous = any(pattern in response_str for pattern in dangerous_patterns)
                
                if test['should_be_sanitized']:
                    if not has_dangerous:
                        print("✅ Malicious content properly sanitized")
                        passed += 1
                    else:
                        print("❌ Dangerous content still present")
                else:
                    if not has_dangerous:
                        print("✅ Normal content preserved")
                        passed += 1
                    else:
                        print("❌ Normal content incorrectly flagged")
                        
            except:
                print("❌ Invalid response format")
        else:
            print(f"❌ Request failed ({response.status_code})")
        
        print()
    
    print(f"📊 Security Results: {passed}/5 tests passed")
    return passed

def test_input_validation_fixes():
    """Test improved input validation"""
    print("🔍 Testing Input Validation Fixes")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    validation_tests = [
        {
            'name': 'Empty Description',
            'data': {'description': '', 'trigger_type': 'webhook'},
            'should_reject': True
        },
        {
            'name': 'Short Description',
            'data': {'description': 'short', 'trigger_type': 'webhook'},
            'should_reject': True
        },
        {
            'name': 'Too Long Description',
            'data': {'description': 'A' * 6000, 'trigger_type': 'webhook'},
            'should_reject': True
        },
        {
            'name': 'Invalid Trigger Type',
            'data': {'description': 'Create a valid workflow', 'trigger_type': 'invalid'},
            'should_reject': True
        },
        {
            'name': 'Valid Input',
            'data': {'description': 'Create a comprehensive workflow for processing data', 'trigger_type': 'webhook'},
            'should_reject': False
        }
    ]
    
    passed = 0
    
    for test in validation_tests:
        print(f"🧪 Testing {test['name']}...")
        
        response = client.post('/generate',
                              data=json.dumps(test['data']),
                              content_type='application/json')
        
        is_rejected = response.status_code != 200
        
        if test['should_reject'] and is_rejected:
            print("✅ Properly rejected invalid input")
            passed += 1
        elif not test['should_reject'] and not is_rejected:
            print("✅ Properly accepted valid input")
            passed += 1
        else:
            expected = "rejected" if test['should_reject'] else "accepted"
            actual = "rejected" if is_rejected else "accepted"
            print(f"❌ Expected {expected}, got {actual}")
        
        print()
    
    print(f"📊 Validation Results: {passed}/5 tests passed")
    return passed

def test_workflow_generation_quality():
    """Test workflow generation quality"""
    print("⚙️ Testing Workflow Generation Quality")
    print("=" * 45)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    quality_tests = [
        {
            'name': 'Simple Workflow',
            'description': 'Create a basic webhook to email notification workflow',
            'complexity': 'simple',
            'min_nodes': 2,
            'max_nodes': 4
        },
        {
            'name': 'Medium Workflow',
            'description': 'Build a lead processing system with validation, CRM integration, and notifications',
            'complexity': 'medium',
            'min_nodes': 3,
            'max_nodes': 6
        },
        {
            'name': 'Complex Workflow',
            'description': 'Design a comprehensive e-commerce order processing system with payment validation, inventory checks, customer notifications, and analytics',
            'complexity': 'complex',
            'min_nodes': 4,
            'max_nodes': 8
        }
    ]
    
    passed = 0
    
    for test in quality_tests:
        print(f"🧪 Testing {test['name']}...")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': test['description'],
                                  'trigger_type': 'webhook',
                                  'complexity': test['complexity']
                              }),
                              content_type='application/json')
        
        if response.status_code == 200:
            try:
                data = json.loads(response.data)
                workflow = data.get('workflow', {})
                nodes = workflow.get('nodes', [])
                connections = workflow.get('connections', {})
                
                node_count = len(nodes)
                connection_count = len(connections)
                
                print(f"   Generated {node_count} nodes with complexity '{test['complexity']}'")
                
                if test['min_nodes'] <= node_count <= test['max_nodes']:
                    print(f"✅ Appropriate node count: {node_count}")
                    
                    if connection_count > 0:
                        print(f"✅ Has connections: {connection_count}")
                        
                        # Check for required fields
                        has_name = bool(workflow.get('name'))
                        has_tags = bool(workflow.get('tags'))
                        
                        if has_name and has_tags:
                            print("✅ Complete workflow structure")
                            passed += 1
                        else:
                            print("❌ Missing workflow metadata")
                    else:
                        print("❌ No connections generated")
                else:
                    print(f"❌ Wrong node count: {node_count} (expected {test['min_nodes']}-{test['max_nodes']})")
                    
            except:
                print("❌ Invalid response format")
        else:
            print(f"❌ Request failed ({response.status_code})")
        
        print()
    
    print(f"📊 Quality Results: {passed}/3 tests passed")
    return passed

def run_perfection_test():
    """Run complete perfection verification"""
    print("🎯 PERFECTION VERIFICATION TEST")
    print("=" * 50)
    
    trigger_passed = test_trigger_type_fixes()
    security_passed = test_security_fixes()
    validation_passed = test_input_validation_fixes()
    quality_passed = test_workflow_generation_quality()
    
    total_tests = 6 + 5 + 5 + 3  # Total from all test categories
    total_passed = trigger_passed + security_passed + validation_passed + quality_passed
    
    success_rate = (total_passed / total_tests) * 100
    
    print(f"\n🏆 PERFECTION TEST RESULTS")
    print("=" * 40)
    print(f"🔧 Trigger Types: {trigger_passed}/6")
    print(f"🛡️ Security: {security_passed}/5")
    print(f"🔍 Validation: {validation_passed}/5")
    print(f"⚙️ Quality: {quality_passed}/3")
    print(f"\n📊 OVERALL SCORE: {total_passed}/{total_tests} ({success_rate:.1f}%)")
    
    if success_rate == 100:
        print("🎉 PERFECT! 100% SUCCESS ACHIEVED!")
        print("🚀 Your N8n JSON Generator is now flawless!")
    elif success_rate >= 95:
        print("🌟 EXCELLENT! Near-perfect performance!")
        print("🚀 Ready for production with minimal issues!")
    elif success_rate >= 90:
        print("✅ VERY GOOD! Minor improvements needed!")
    else:
        print("⚠️ NEEDS MORE WORK! Significant issues remain!")
    
    return success_rate == 100

if __name__ == "__main__":
    is_perfect = run_perfection_test()
    exit(0 if is_perfect else 1)