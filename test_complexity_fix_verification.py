#!/usr/bin/env python3
"""Complexity Fix Verification Test"""

import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def test_complex_scenario_node_generation():
    """Test that complex scenarios generate appropriate number of nodes"""
    print("🔧 Testing Complex Scenario Node Generation Fix")
    print("=" * 55)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    complex_scenarios = [
        {
            'name': 'Government Regulatory Compliance',
            'description': 'Create a regulatory compliance workflow with document review, approval processes, audit trails, validation checks, stakeholder notifications, and comprehensive reporting requirements',
            'trigger_type': 'manual',
            'complexity': 'complex',
            'expected_min_nodes': 5,
            'expected_max_nodes': 12
        },
        {
            'name': 'SaaS User Onboarding Pipeline',
            'description': 'Build a comprehensive user onboarding workflow for a SaaS platform with trial activation, feature tours, usage tracking, conversion optimization, email sequences, and analytics reporting',
            'trigger_type': 'webhook',
            'complexity': 'complex',
            'expected_min_nodes': 5,
            'expected_max_nodes': 12
        },
        {
            'name': 'Manufacturing Quality Control',
            'description': 'Design a quality control workflow with automated testing, defect tracking, corrective actions, compliance reporting, supplier notifications, and process optimization',
            'trigger_type': 'webhook',
            'complexity': 'complex',
            'expected_min_nodes': 5,
            'expected_max_nodes': 12
        },
        {
            'name': 'Enterprise Data Processing',
            'description': 'Create an enterprise data processing workflow with validation, transformation, enrichment, routing, storage, monitoring, error handling, and audit logging',
            'trigger_type': 'schedule',
            'complexity': 'complex',
            'expected_min_nodes': 6,
            'expected_max_nodes': 12
        }
    ]
    
    passed_tests = 0
    
    for scenario in complex_scenarios:
        print(f"\n🧪 Testing: {scenario['name']}")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': scenario['description'],
                                  'trigger_type': scenario['trigger_type'],
                                  'complexity': scenario['complexity']
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
                
                if scenario['expected_min_nodes'] <= node_count <= scenario['expected_max_nodes']:
                    print(f"✅ Appropriate complexity: {node_count} nodes")
                    
                    # Check for diverse node types
                    node_types = [node.get('type', '') for node in nodes]
                    unique_types = len(set(node_types))
                    
                    if unique_types >= 3:  # At least 3 different node types
                        print(f"✅ Good node diversity: {unique_types} unique types")
                        
                        # Check for proper connections
                        if connection_count >= node_count - 2:  # Most nodes should be connected
                            print("✅ Well-connected workflow")
                            passed_tests += 1
                        else:
                            print(f"⚠️ Limited connections: {connection_count}")
                            passed_tests += 0.5
                    else:
                        print(f"⚠️ Limited node diversity: {unique_types} types")
                        passed_tests += 0.5
                else:
                    print(f"❌ Wrong complexity: {node_count} nodes (expected {scenario['expected_min_nodes']}-{scenario['expected_max_nodes']})")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Complex Scenario Results: {passed_tests}/{len(complex_scenarios)} passed")
    return passed_tests

def test_content_complexity_analysis():
    """Test that content complexity is properly analyzed"""
    print("\n🔍 Testing Content Complexity Analysis")
    print("=" * 45)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    complexity_tests = [
        {
            'name': 'Simple Content',
            'description': 'Create a basic workflow to send email notifications',
            'complexity': 'simple',
            'expected_nodes': (2, 4)
        },
        {
            'name': 'Medium Content',
            'description': 'Build a workflow with validation, processing, and notification features',
            'complexity': 'medium',
            'expected_nodes': (3, 7)
        },
        {
            'name': 'Complex Content',
            'description': 'Design a comprehensive workflow with validation, transformation, routing, monitoring, error handling, reporting, and integration capabilities',
            'complexity': 'complex',
            'expected_nodes': (6, 12)
        }
    ]
    
    passed_tests = 0
    
    for test in complexity_tests:
        print(f"\n🧪 Testing: {test['name']}")
        
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
                
                node_count = len(nodes)
                min_expected, max_expected = test['expected_nodes']
                
                print(f"   Generated {node_count} nodes")
                print(f"   Expected range: {min_expected}-{max_expected}")
                
                if min_expected <= node_count <= max_expected:
                    print("✅ Content complexity properly analyzed")
                    passed_tests += 1
                else:
                    print("❌ Content complexity analysis needs improvement")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Content Analysis Results: {passed_tests}/{len(complexity_tests)} passed")
    return passed_tests

def test_industry_specific_complexity():
    """Test that industry-specific workflows get appropriate complexity"""
    print("\n🏭 Testing Industry-Specific Complexity")
    print("=" * 45)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    industry_tests = [
        {
            'name': 'Healthcare Workflow',
            'description': 'Create a patient management workflow with appointment scheduling, medical record updates, insurance verification, billing processing, and compliance reporting',
            'expected_min_nodes': 5
        },
        {
            'name': 'Financial Workflow',
            'description': 'Build a financial transaction workflow with fraud detection, compliance checking, risk assessment, approval routing, and audit logging',
            'expected_min_nodes': 5
        },
        {
            'name': 'Government Workflow',
            'description': 'Design a permit application workflow with document review, stakeholder notifications, approval processes, status tracking, and public records management',
            'expected_min_nodes': 5
        }
    ]
    
    passed_tests = 0
    
    for test in industry_tests:
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
                
                node_count = len(nodes)
                
                print(f"   Generated {node_count} nodes")
                
                if node_count >= test['expected_min_nodes']:
                    print(f"✅ Sufficient complexity for industry workflow")
                    passed_tests += 1
                else:
                    print(f"❌ Insufficient complexity: {node_count} < {test['expected_min_nodes']}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Industry Complexity Results: {passed_tests}/{len(industry_tests)} passed")
    return passed_tests

if __name__ == "__main__":
    try:
        print("🔧 COMPLEXITY FIX VERIFICATION")
        print("=" * 40)
        
        complex_passed = test_complex_scenario_node_generation()
        content_passed = test_content_complexity_analysis()
        industry_passed = test_industry_specific_complexity()
        
        total_tests = 4 + 3 + 3  # Total test cases
        total_passed = complex_passed + content_passed + industry_passed
        
        success_rate = (total_passed / total_tests) * 100
        
        print(f"\n🏆 COMPLEXITY FIX RESULTS")
        print("=" * 35)
        print(f"🔧 Complex Scenarios: {complex_passed}/4")
        print(f"🔍 Content Analysis: {content_passed}/3")
        print(f"🏭 Industry Specific: {industry_passed}/3")
        print(f"\n📊 OVERALL SCORE: {total_passed}/{total_tests} ({success_rate:.1f}%)")
        
        if success_rate >= 80:
            print("🎉 Complexity fix successful!")
            print("✅ Complex scenarios now generate appropriate node counts")
            print("🚀 Workflow generation permanently improved!")
            exit(0)
        else:
            print("⚠️ Complexity fix needs more work!")
            exit(1)
            
    except Exception as e:
        print(f"❌ Complexity fix verification failed: {e}")
        exit(1)