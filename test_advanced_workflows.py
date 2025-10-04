#!/usr/bin/env python3
"""Advanced Workflow Testing for N8n JSON Generator"""

import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def test_complex_workflow_scenarios():
    """Test complex real-world workflow scenarios"""
    print("🔧 Testing Complex Workflow Scenarios")
    print("=" * 45)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    complex_scenarios = [
        {
            'name': 'Multi-Step E-commerce Pipeline',
            'description': 'Create a comprehensive e-commerce workflow that receives orders via webhook, validates payment information, checks inventory levels, processes payment through Stripe, updates inventory in database, sends confirmation email to customer, creates shipping label, notifies warehouse team via Slack, and tracks the order status',
            'trigger_type': 'webhook',
            'expected_min_nodes': 4,
            'expected_max_nodes': 10
        },
        {
            'name': 'Customer Support Automation',
            'description': 'Build an intelligent customer support system that monitors support emails, categorizes tickets by urgency and type, assigns to appropriate team members, sends auto-responses, escalates high-priority issues, tracks response times, and generates daily reports',
            'trigger_type': 'schedule',
            'expected_min_nodes': 3,
            'expected_max_nodes': 8
        },
        {
            'name': 'Data Analytics Pipeline',
            'description': 'Design a data processing workflow that extracts data from multiple APIs, transforms and cleans the data, performs calculations and aggregations, stores results in data warehouse, generates visualizations, and sends automated reports to stakeholders',
            'trigger_type': 'manual',
            'expected_min_nodes': 3,
            'expected_max_nodes': 9
        },
        {
            'name': 'Social Media Management',
            'description': 'Create a social media automation workflow that monitors brand mentions across platforms, analyzes sentiment, responds to customer inquiries, schedules posts, tracks engagement metrics, and alerts marketing team of trending topics',
            'trigger_type': 'webhook',
            'expected_min_nodes': 4,
            'expected_max_nodes': 8
        }
    ]
    
    passed_tests = 0
    
    for scenario in complex_scenarios:
        print(f"\n🧪 Testing: {scenario['name']}")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': scenario['description'],
                                  'trigger_type': scenario['trigger_type'],
                                  'complexity': 'complex'
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
                
                # Validate node count
                if scenario['expected_min_nodes'] <= node_count <= scenario['expected_max_nodes']:
                    print("   ✅ Appropriate complexity level")
                    
                    # Validate workflow structure
                    has_name = bool(workflow.get('name'))
                    has_tags = bool(workflow.get('tags'))
                    has_meta = bool(workflow.get('meta'))
                    
                    if has_name and has_tags and has_meta:
                        print("   ✅ Complete workflow metadata")
                        
                        # Validate trigger node
                        if nodes:
                            trigger_node = nodes[0]
                            expected_triggers = {
                                'webhook': 'n8n-nodes-base.webhook',
                                'schedule': 'n8n-nodes-base.scheduleTrigger',
                                'manual': 'n8n-nodes-base.manualTrigger'
                            }
                            
                            if trigger_node.get('type') == expected_triggers[scenario['trigger_type']]:
                                print("   ✅ Correct trigger type")
                                passed_tests += 1
                            else:
                                print(f"   ❌ Wrong trigger type: {trigger_node.get('type')}")
                        else:
                            print("   ❌ No nodes generated")
                    else:
                        print("   ❌ Missing workflow metadata")
                else:
                    print(f"   ❌ Wrong complexity: {node_count} nodes (expected {scenario['expected_min_nodes']}-{scenario['expected_max_nodes']})")
                    
            except Exception as e:
                print(f"   ❌ Error parsing response: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Complex Workflow Results: {passed_tests}/{len(complex_scenarios)} passed")
    return passed_tests

def test_workflow_node_diversity():
    """Test that workflows generate diverse node types"""
    print("\n🎨 Testing Workflow Node Diversity")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    diversity_tests = [
        {
            'description': 'Create a workflow with email notifications, Slack messages, database operations, and API calls',
            'expected_node_types': ['email', 'slack', 'database', 'api']
        },
        {
            'description': 'Build a workflow with data validation, transformation, conditional logic, and file operations',
            'expected_node_types': ['validation', 'transformation', 'conditional', 'file']
        },
        {
            'description': 'Design a workflow with webhook triggers, HTTP requests, spreadsheet updates, and notifications',
            'expected_node_types': ['webhook', 'http', 'spreadsheet', 'notification']
        }
    ]
    
    passed_tests = 0
    
    for i, test in enumerate(diversity_tests, 1):
        print(f"\n🧪 Diversity Test {i}")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': test['description'],
                                  'trigger_type': 'webhook',
                                  'complexity': 'medium'
                              }),
                              content_type='application/json')
        
        if response.status_code == 200:
            try:
                data = json.loads(response.data)
                workflow = data.get('workflow', {})
                nodes = workflow.get('nodes', [])
                
                node_types = [node.get('type', '') for node in nodes]
                print(f"   Generated node types: {node_types}")
                
                # Check for diversity in node types
                unique_types = len(set(node_types))
                if unique_types >= 3:  # At least 3 different node types
                    print(f"   ✅ Good diversity: {unique_types} unique node types")
                    passed_tests += 1
                else:
                    print(f"   ❌ Low diversity: {unique_types} unique node types")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Node Diversity Results: {passed_tests}/{len(diversity_tests)} passed")
    return passed_tests

def test_workflow_naming_intelligence():
    """Test intelligent workflow naming based on description"""
    print("\n🏷️ Testing Intelligent Workflow Naming")
    print("=" * 45)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    naming_tests = [
        {
            'description': 'Create a lead processing workflow for sales automation',
            'expected_keywords': ['lead', 'process', 'workflow']
        },
        {
            'description': 'Build an order fulfillment system with inventory management',
            'expected_keywords': ['order', 'fulfillment', 'workflow']
        },
        {
            'description': 'Design a customer notification system for support tickets',
            'expected_keywords': ['customer', 'notification', 'workflow']
        }
    ]
    
    passed_tests = 0
    
    for i, test in enumerate(naming_tests, 1):
        print(f"\n🧪 Naming Test {i}")
        
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
                workflow_name = workflow.get('name', '').lower()
                
                print(f"   Generated name: {workflow.get('name')}")
                
                # Check if name contains relevant keywords
                keyword_matches = sum(1 for keyword in test['expected_keywords'] 
                                    if keyword in workflow_name)
                
                if keyword_matches >= 2:  # At least 2 relevant keywords
                    print(f"   ✅ Intelligent naming: {keyword_matches} relevant keywords")
                    passed_tests += 1
                else:
                    print(f"   ❌ Poor naming: {keyword_matches} relevant keywords")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Naming Intelligence Results: {passed_tests}/{len(naming_tests)} passed")
    return passed_tests

if __name__ == "__main__":
    try:
        complex_passed = test_complex_workflow_scenarios()
        diversity_passed = test_workflow_node_diversity()
        naming_passed = test_workflow_naming_intelligence()
        
        total_tests = 4 + 3 + 3  # Total test cases
        total_passed = complex_passed + diversity_passed + naming_passed
        
        success_rate = (total_passed / total_tests) * 100
        
        print(f"\n🏆 ADVANCED WORKFLOW TEST RESULTS")
        print("=" * 50)
        print(f"🔧 Complex Scenarios: {complex_passed}/4")
        print(f"🎨 Node Diversity: {diversity_passed}/3")
        print(f"🏷️ Naming Intelligence: {naming_passed}/3")
        print(f"\n📊 OVERALL SCORE: {total_passed}/{total_tests} ({success_rate:.1f}%)")
        
        if success_rate >= 90:
            print("🎉 Advanced workflow tests passed!")
            exit(0)
        else:
            print("⚠️ Some advanced tests need attention!")
            exit(1)
            
    except Exception as e:
        print(f"❌ Advanced workflow tests failed: {e}")
        exit(1)