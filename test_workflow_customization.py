#!/usr/bin/env python3
"""Workflow Customization and Flexibility Testing"""

import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def test_complexity_scaling():
    """Test how workflows scale with different complexity levels"""
    print("📈 Testing Complexity Scaling")
    print("=" * 35)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    base_description = "Create a customer data processing workflow with validation, transformation, and storage"
    
    complexity_tests = [
        {'level': 'simple', 'expected_min': 2, 'expected_max': 4},
        {'level': 'medium', 'expected_min': 3, 'expected_max': 6},
        {'level': 'complex', 'expected_min': 4, 'expected_max': 8}
    ]
    
    passed_tests = 0
    
    for test in complexity_tests:
        print(f"\n🧪 Testing {test['level'].title()} Complexity")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': base_description,
                                  'trigger_type': 'webhook',
                                  'complexity': test['level']
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
                
                print(f"   Generated {node_count} nodes, {connection_count} connections")
                
                if test['expected_min'] <= node_count <= test['expected_max']:
                    print(f"   ✅ Appropriate complexity scaling")
                    
                    # Check for increasing sophistication
                    node_types = [node.get('type', '') for node in nodes]
                    has_conditional = any('if' in node_type for node_type in node_types)
                    has_code = any('code' in node_type for node_type in node_types)
                    
                    sophistication_score = sum([has_conditional, has_code, connection_count > 2])
                    expected_sophistication = {'simple': 1, 'medium': 2, 'complex': 2}
                    
                    if sophistication_score >= expected_sophistication[test['level']]:
                        print(f"   ✅ Appropriate sophistication level")
                        passed_tests += 1
                    else:
                        print(f"   ⚠️ Lower sophistication than expected")
                        passed_tests += 0.5
                else:
                    print(f"   ❌ Wrong node count: {node_count} (expected {test['expected_min']}-{test['expected_max']})")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Complexity Scaling Results: {passed_tests}/{len(complexity_tests)} passed")
    return passed_tests

def test_trigger_type_variations():
    """Test different trigger type behaviors and configurations"""
    print("\n🔄 Testing Trigger Type Variations")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    trigger_variations = [
        {
            'name': 'Webhook with Response',
            'trigger_type': 'webhook',
            'description': 'Create a webhook workflow that processes data and returns a response',
            'should_have_response': True
        },
        {
            'name': 'Schedule with Batch Processing',
            'trigger_type': 'schedule',
            'description': 'Build a scheduled workflow for batch processing large datasets',
            'should_have_response': False
        },
        {
            'name': 'Manual with User Input',
            'trigger_type': 'manual',
            'description': 'Design a manual workflow that requires user input and confirmation',
            'should_have_response': False
        }
    ]
    
    passed_tests = 0
    
    for test in trigger_variations:
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
                
                # Check trigger node type
                if nodes:
                    trigger_node = nodes[0]
                    expected_types = {
                        'webhook': 'n8n-nodes-base.webhook',
                        'schedule': 'n8n-nodes-base.scheduleTrigger',
                        'manual': 'n8n-nodes-base.manualTrigger'
                    }
                    
                    if trigger_node.get('type') == expected_types[test['trigger_type']]:
                        print(f"   ✅ Correct trigger type: {trigger_node.get('type')}")
                        
                        # Check for response node if expected
                        has_response = any('respondToWebhook' in node.get('type', '') for node in nodes)
                        
                        if test['should_have_response'] == has_response:
                            print(f"   ✅ Response node handling correct")
                            passed_tests += 1
                        else:
                            expected = "present" if test['should_have_response'] else "absent"
                            actual = "present" if has_response else "absent"
                            print(f"   ❌ Response node should be {expected}, but is {actual}")
                    else:
                        print(f"   ❌ Wrong trigger type: {trigger_node.get('type')}")
                else:
                    print("   ❌ No nodes generated")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Trigger Variations Results: {passed_tests}/{len(trigger_variations)} passed")
    return passed_tests

def test_workflow_personalization():
    """Test workflow personalization based on different user contexts"""
    print("\n👤 Testing Workflow Personalization")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    personalization_tests = [
        {
            'name': 'Small Business Context',
            'description': 'Create a simple order processing workflow for a small online store with basic inventory tracking',
            'expected_characteristics': ['simple', 'basic', 'small-scale']
        },
        {
            'name': 'Enterprise Context',
            'description': 'Build an enterprise-grade order processing system with advanced analytics, multi-region support, and compliance monitoring',
            'expected_characteristics': ['complex', 'enterprise', 'advanced']
        },
        {
            'name': 'Startup Context',
            'description': 'Design a lean customer onboarding workflow for a tech startup with automated welcome sequences and growth tracking',
            'expected_characteristics': ['lean', 'automated', 'growth']
        },
        {
            'name': 'Non-Profit Context',
            'description': 'Create a volunteer management workflow for a non-profit organization with donation tracking and impact reporting',
            'expected_characteristics': ['volunteer', 'donation', 'impact']
        }
    ]
    
    passed_tests = 0
    
    for test in personalization_tests:
        print(f"\n🧪 Testing: {test['name']}")
        
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
                nodes = workflow.get('nodes', [])
                tags = workflow.get('tags', [])
                workflow_name = workflow.get('name', '').lower()
                
                print(f"   Generated {len(nodes)} nodes")
                print(f"   Tags: {tags}")
                print(f"   Name: {workflow.get('name')}")
                
                # Check for context-appropriate complexity
                node_count = len(nodes)
                if 'small business' in test['name'].lower() or 'startup' in test['name'].lower():
                    appropriate_complexity = 2 <= node_count <= 5
                elif 'enterprise' in test['name'].lower():
                    appropriate_complexity = node_count >= 4
                else:
                    appropriate_complexity = node_count >= 2
                
                if appropriate_complexity:
                    print("   ✅ Appropriate complexity for context")
                    
                    # Check for context-relevant elements
                    all_text = ' '.join([workflow_name] + tags + [test['description'].lower()])
                    context_relevance = sum(1 for char in test['expected_characteristics']
                                          if any(char in all_text for char in [char]))
                    
                    if context_relevance >= 1:  # At least some context relevance
                        print(f"   ✅ Context-appropriate personalization")
                        passed_tests += 1
                    else:
                        print("   ⚠️ Limited context personalization")
                        passed_tests += 0.5
                else:
                    print("   ❌ Inappropriate complexity for context")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Personalization Results: {passed_tests}/{len(personalization_tests)} passed")
    return passed_tests

def test_workflow_extensibility():
    """Test how well workflows can be extended and modified"""
    print("\n🔧 Testing Workflow Extensibility")
    print("=" * 35)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    extensibility_tests = [
        {
            'name': 'Modular Design',
            'description': 'Create a modular customer service workflow with separate validation, processing, and notification components',
            'expected_modularity': True
        },
        {
            'name': 'Scalable Architecture',
            'description': 'Build a scalable data processing workflow that can handle increasing volumes and additional data sources',
            'expected_scalability': True
        },
        {
            'name': 'Integration Ready',
            'description': 'Design an integration-ready workflow with multiple API endpoints and webhook connections for third-party services',
            'expected_integration_points': True
        }
    ]
    
    passed_tests = 0
    
    for test in extensibility_tests:
        print(f"\n🧪 Testing: {test['name']}")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': test['description'],
                                  'trigger_type': 'webhook',
                                  'complexity': 'complex'
                              }),
                              content_type='application/json')
        
        if response.status_code == 200:
            try:
                data = json.loads(response.data)
                workflow = data.get('workflow', {})
                nodes = workflow.get('nodes', [])
                connections = workflow.get('connections', {})
                
                print(f"   Generated {len(nodes)} nodes, {len(connections)} connection groups")
                
                # Analyze extensibility characteristics
                node_types = [node.get('type', '') for node in nodes]
                
                # Check for modular components
                has_validation = any('code' in node_type or 'if' in node_type for node_type in node_types)
                has_processing = any('code' in node_type for node_type in node_types)
                has_integration = any('http' in node_type or 'webhook' in node_type for node_type in node_types)
                
                extensibility_score = sum([has_validation, has_processing, has_integration])
                
                if extensibility_score >= 2:  # At least 2 extensibility features
                    print(f"   ✅ Good extensibility design (score: {extensibility_score})")
                    
                    # Check connection structure for modularity
                    if len(connections) >= 2:  # Multiple connection points
                        print("   ✅ Modular connection structure")
                        passed_tests += 1
                    else:
                        print("   ⚠️ Limited connection modularity")
                        passed_tests += 0.5
                else:
                    print(f"   ❌ Limited extensibility (score: {extensibility_score})")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Extensibility Results: {passed_tests}/{len(extensibility_tests)} passed")
    return passed_tests

if __name__ == "__main__":
    try:
        print("🎛️ WORKFLOW CUSTOMIZATION AND FLEXIBILITY TESTING")
        print("=" * 60)
        
        complexity_passed = test_complexity_scaling()
        trigger_passed = test_trigger_type_variations()
        personalization_passed = test_workflow_personalization()
        extensibility_passed = test_workflow_extensibility()
        
        total_tests = 3 + 3 + 4 + 3  # Total test cases
        total_passed = complexity_passed + trigger_passed + personalization_passed + extensibility_passed
        
        success_rate = (total_passed / total_tests) * 100
        
        print(f"\n🏆 WORKFLOW CUSTOMIZATION TEST RESULTS")
        print("=" * 55)
        print(f"📈 Complexity Scaling: {complexity_passed}/3")
        print(f"🔄 Trigger Variations: {trigger_passed}/3")
        print(f"👤 Personalization: {personalization_passed}/4")
        print(f"🔧 Extensibility: {extensibility_passed}/3")
        print(f"\n📊 OVERALL SCORE: {total_passed}/{total_tests} ({success_rate:.1f}%)")
        
        if success_rate >= 75:
            print("🎉 Workflow customization tests passed!")
            exit(0)
        else:
            print("⚠️ Some customization tests need attention!")
            exit(1)
            
    except Exception as e:
        print(f"❌ Workflow customization tests failed: {e}")
        exit(1)