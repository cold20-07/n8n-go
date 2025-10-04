#!/usr/bin/env python3
"""Integration Scenarios Testing for N8n JSON Generator"""

import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def test_popular_integrations():
    """Test workflows with popular service integrations"""
    print("🔗 Testing Popular Service Integrations")
    print("=" * 45)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    integration_scenarios = [
        {
            'name': 'Slack + Email Integration',
            'description': 'Create a workflow that sends notifications to Slack channels and email addresses when new leads are received',
            'expected_integrations': ['slack', 'email']
        },
        {
            'name': 'Database + Spreadsheet Sync',
            'description': 'Build a workflow that synchronizes data between MySQL database and Google Sheets for reporting',
            'expected_integrations': ['database', 'sheets']
        },
        {
            'name': 'API + Webhook Integration',
            'description': 'Design a workflow that receives webhook data and makes API calls to external services for data enrichment',
            'expected_integrations': ['webhook', 'api']
        },
        {
            'name': 'CRM + Marketing Automation',
            'description': 'Create a workflow that updates CRM records and triggers marketing automation campaigns based on customer behavior',
            'expected_integrations': ['crm', 'marketing']
        }
    ]
    
    passed_tests = 0
    
    for scenario in integration_scenarios:
        print(f"\n🧪 Testing: {scenario['name']}")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': scenario['description'],
                                  'trigger_type': 'webhook',
                                  'complexity': 'medium'
                              }),
                              content_type='application/json')
        
        if response.status_code == 200:
            try:
                data = json.loads(response.data)
                workflow = data.get('workflow', {})
                nodes = workflow.get('nodes', [])
                
                # Analyze node types for expected integrations
                node_types = [node.get('type', '').lower() for node in nodes]
                node_names = [node.get('name', '').lower() for node in nodes]
                
                print(f"   Generated {len(nodes)} nodes")
                print(f"   Node types: {node_types}")
                
                # Check for integration-related nodes
                integration_found = 0
                for integration in scenario['expected_integrations']:
                    found = any(integration in node_type or integration in node_name 
                              for node_type in node_types for node_name in node_names)
                    if found:
                        integration_found += 1
                        print(f"   ✅ Found {integration} integration")
                    else:
                        print(f"   ⚠️ Missing {integration} integration")
                
                if integration_found >= len(scenario['expected_integrations']) * 0.5:  # At least 50% of expected integrations
                    print("   ✅ Integration scenario successful")
                    passed_tests += 1
                else:
                    print("   ❌ Integration scenario incomplete")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Integration Results: {passed_tests}/{len(integration_scenarios)} passed")
    return passed_tests

def test_workflow_connection_patterns():
    """Test different workflow connection patterns"""
    print("\n🔀 Testing Workflow Connection Patterns")
    print("=" * 45)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    pattern_tests = [
        {
            'name': 'Linear Flow',
            'description': 'Create a simple linear workflow that processes data step by step from webhook to database',
            'expected_pattern': 'linear'
        },
        {
            'name': 'Conditional Branching',
            'description': 'Build a workflow with conditional logic that routes data to different paths based on validation results',
            'expected_pattern': 'branching'
        },
        {
            'name': 'Parallel Processing',
            'description': 'Design a workflow that processes data in parallel streams for email and Slack notifications',
            'expected_pattern': 'parallel'
        }
    ]
    
    passed_tests = 0
    
    for test in pattern_tests:
        print(f"\n🧪 Testing: {test['name']}")
        
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
                connections = workflow.get('connections', {})
                
                node_count = len(nodes)
                connection_count = len(connections)
                
                print(f"   Generated {node_count} nodes, {connection_count} connection groups")
                
                # Analyze connection pattern
                if connection_count > 0:
                    # Calculate connection complexity
                    total_connections = sum(len(conn_list) for conn_list in connections.values())
                    avg_connections_per_node = total_connections / max(node_count, 1)
                    
                    print(f"   Average connections per node: {avg_connections_per_node:.2f}")
                    
                    if test['expected_pattern'] == 'linear' and avg_connections_per_node <= 1.5:
                        print("   ✅ Linear pattern detected")
                        passed_tests += 1
                    elif test['expected_pattern'] == 'branching' and avg_connections_per_node > 1.5:
                        print("   ✅ Branching pattern detected")
                        passed_tests += 1
                    elif test['expected_pattern'] == 'parallel' and connection_count >= 2:
                        print("   ✅ Parallel pattern detected")
                        passed_tests += 1
                    else:
                        print(f"   ❌ Expected {test['expected_pattern']} pattern not clearly detected")
                else:
                    print("   ❌ No connections generated")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Connection Pattern Results: {passed_tests}/{len(pattern_tests)} passed")
    return passed_tests

def test_industry_specific_workflows():
    """Test industry-specific workflow generation"""
    print("\n🏭 Testing Industry-Specific Workflows")
    print("=" * 45)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    industry_tests = [
        {
            'name': 'E-commerce',
            'description': 'Create an e-commerce order processing workflow with payment validation, inventory checks, and shipping notifications',
            'expected_tags': ['ecommerce', 'orders', 'payments']
        },
        {
            'name': 'Healthcare',
            'description': 'Build a patient appointment scheduling workflow with reminder notifications and medical record updates',
            'expected_tags': ['healthcare', 'appointments', 'notifications']
        },
        {
            'name': 'Finance',
            'description': 'Design a financial transaction monitoring workflow with fraud detection and compliance reporting',
            'expected_tags': ['finance', 'monitoring', 'compliance']
        },
        {
            'name': 'Education',
            'description': 'Create a student enrollment workflow with course assignment and notification to instructors',
            'expected_tags': ['education', 'enrollment', 'notifications']
        }
    ]
    
    passed_tests = 0
    
    for test in industry_tests:
        print(f"\n🧪 Testing: {test['name']} Industry")
        
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
                tags = workflow.get('tags', [])
                workflow_name = workflow.get('name', '').lower()
                
                print(f"   Generated tags: {tags}")
                print(f"   Workflow name: {workflow.get('name')}")
                
                # Check for industry-relevant tags or naming
                relevant_elements = 0
                for expected_tag in test['expected_tags']:
                    if (any(expected_tag in tag.lower() for tag in tags) or 
                        expected_tag in workflow_name):
                        relevant_elements += 1
                        print(f"   ✅ Found {expected_tag} relevance")
                
                if relevant_elements >= len(test['expected_tags']) * 0.5:  # At least 50% relevance
                    print("   ✅ Industry-specific workflow generated")
                    passed_tests += 1
                else:
                    print("   ❌ Insufficient industry relevance")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Industry-Specific Results: {passed_tests}/{len(industry_tests)} passed")
    return passed_tests

if __name__ == "__main__":
    try:
        integration_passed = test_popular_integrations()
        pattern_passed = test_workflow_connection_patterns()
        industry_passed = test_industry_specific_workflows()
        
        total_tests = 4 + 3 + 4  # Total test cases
        total_passed = integration_passed + pattern_passed + industry_passed
        
        success_rate = (total_passed / total_tests) * 100
        
        print(f"\n🏆 INTEGRATION SCENARIOS TEST RESULTS")
        print("=" * 50)
        print(f"🔗 Popular Integrations: {integration_passed}/4")
        print(f"🔀 Connection Patterns: {pattern_passed}/3")
        print(f"🏭 Industry-Specific: {industry_passed}/4")
        print(f"\n📊 OVERALL SCORE: {total_passed}/{total_tests} ({success_rate:.1f}%)")
        
        if success_rate >= 80:
            print("🎉 Integration scenario tests passed!")
            exit(0)
        else:
            print("⚠️ Some integration tests need attention!")
            exit(1)
            
    except Exception as e:
        print(f"❌ Integration scenario tests failed: {e}")
        exit(1)