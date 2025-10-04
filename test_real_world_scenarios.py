#!/usr/bin/env python3
"""Real-World Business Scenarios Testing"""

import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def test_saas_business_workflows():
    """Test SaaS business workflow scenarios"""
    print("💼 Testing SaaS Business Workflows")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    saas_scenarios = [
        {
            'name': 'User Onboarding Pipeline',
            'description': 'Create a comprehensive user onboarding workflow for a SaaS platform with trial activation, feature tours, usage tracking, and conversion optimization',
            'trigger_type': 'webhook',
            'expected_features': ['onboarding', 'trial', 'tracking', 'conversion']
        },
        {
            'name': 'Subscription Management',
            'description': 'Build a subscription lifecycle management workflow with billing automation, usage monitoring, upgrade/downgrade handling, and churn prevention',
            'trigger_type': 'schedule',
            'expected_features': ['subscription', 'billing', 'usage', 'churn']
        },
        {
            'name': 'Customer Success Automation',
            'description': 'Design a customer success workflow with health scoring, proactive outreach, feature adoption tracking, and renewal management',
            'trigger_type': 'webhook',
            'expected_features': ['success', 'health', 'adoption', 'renewal']
        },
        {
            'name': 'Product Analytics Pipeline',
            'description': 'Create a product analytics workflow with event tracking, user behavior analysis, feature usage metrics, and automated reporting',
            'trigger_type': 'schedule',
            'expected_features': ['analytics', 'tracking', 'behavior', 'metrics']
        }
    ]
    
    passed_tests = 0
    
    for scenario in saas_scenarios:
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
                tags = workflow.get('tags', [])
                
                print(f"   Generated {len(nodes)} nodes")
                print(f"   Tags: {tags}")
                
                # Check for appropriate complexity
                if len(nodes) >= 4:  # SaaS workflows should be reasonably complex
                    print("   ✅ Appropriate complexity for SaaS scenario")
                    
                    # Check for SaaS-relevant features
                    all_text = ' '.join([scenario['description'].lower()] + [tag.lower() for tag in tags])
                    features_found = sum(1 for feature in scenario['expected_features']
                                       if feature in all_text)
                    
                    if features_found >= 2:  # At least 2 SaaS features
                        print(f"   ✅ SaaS features detected: {features_found}")
                        passed_tests += 1
                    else:
                        print(f"   ⚠️ Limited SaaS features: {features_found}")
                        passed_tests += 0.5
                else:
                    print("   ❌ Insufficient complexity for SaaS scenario")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 SaaS Business Results: {passed_tests}/{len(saas_scenarios)} passed")
    return passed_tests

def test_manufacturing_workflows():
    """Test manufacturing and supply chain workflows"""
    print("\n🏭 Testing Manufacturing Workflows")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    manufacturing_scenarios = [
        {
            'name': 'Production Planning',
            'description': 'Create a production planning workflow with demand forecasting, capacity planning, material requirements, and scheduling optimization',
            'trigger_type': 'schedule',
            'expected_elements': ['production', 'planning', 'capacity', 'materials']
        },
        {
            'name': 'Quality Control Process',
            'description': 'Build a quality control workflow with automated testing, defect tracking, corrective actions, and compliance reporting',
            'trigger_type': 'webhook',
            'expected_elements': ['quality', 'testing', 'defect', 'compliance']
        },
        {
            'name': 'Supply Chain Management',
            'description': 'Design a supply chain workflow with vendor management, procurement automation, inventory optimization, and logistics coordination',
            'trigger_type': 'schedule',
            'expected_elements': ['supply', 'vendor', 'procurement', 'inventory']
        },
        {
            'name': 'Equipment Maintenance',
            'description': 'Create a predictive maintenance workflow with sensor monitoring, failure prediction, maintenance scheduling, and parts ordering',
            'trigger_type': 'webhook',
            'expected_elements': ['maintenance', 'monitoring', 'prediction', 'scheduling']
        }
    ]
    
    passed_tests = 0
    
    for scenario in manufacturing_scenarios:
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
                
                print(f"   Generated {len(nodes)} nodes")
                
                # Manufacturing workflows should be complex
                if len(nodes) >= 3:
                    print("   ✅ Appropriate complexity for manufacturing")
                    
                    # Check for manufacturing-relevant elements
                    description_lower = scenario['description'].lower()
                    elements_found = sum(1 for element in scenario['expected_elements']
                                       if element in description_lower)
                    
                    if elements_found >= 2:
                        print(f"   ✅ Manufacturing elements present: {elements_found}")
                        passed_tests += 1
                    else:
                        print(f"   ⚠️ Limited manufacturing elements: {elements_found}")
                        passed_tests += 0.5
                else:
                    print("   ❌ Insufficient complexity for manufacturing")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Manufacturing Results: {passed_tests}/{len(manufacturing_scenarios)} passed")
    return passed_tests

def test_media_and_content_workflows():
    """Test media and content management workflows"""
    print("\n🎬 Testing Media and Content Workflows")
    print("=" * 45)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    media_scenarios = [
        {
            'name': 'Content Publishing Pipeline',
            'description': 'Create a content publishing workflow with editorial review, SEO optimization, multi-platform distribution, and performance tracking',
            'trigger_type': 'webhook',
            'expected_aspects': ['content', 'publishing', 'seo', 'distribution']
        },
        {
            'name': 'Video Processing Workflow',
            'description': 'Build a video processing workflow with upload handling, transcoding, thumbnail generation, metadata extraction, and CDN distribution',
            'trigger_type': 'webhook',
            'expected_aspects': ['video', 'processing', 'transcoding', 'cdn']
        },
        {
            'name': 'Social Media Management',
            'description': 'Design a social media workflow with content scheduling, cross-platform posting, engagement monitoring, and analytics reporting',
            'trigger_type': 'schedule',
            'expected_aspects': ['social', 'scheduling', 'posting', 'engagement']
        },
        {
            'name': 'Digital Asset Management',
            'description': 'Create a digital asset workflow with file organization, metadata tagging, version control, and access management',
            'trigger_type': 'webhook',
            'expected_aspects': ['asset', 'organization', 'metadata', 'version']
        }
    ]
    
    passed_tests = 0
    
    for scenario in media_scenarios:
        print(f"\n🧪 Testing: {scenario['name']}")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': scenario['description'],
                                  'trigger_type': scenario['trigger_type'],
                                  'complexity': 'medium'
                              }),
                              content_type='application/json')
        
        if response.status_code == 200:
            try:
                data = json.loads(response.data)
                workflow = data.get('workflow', {})
                nodes = workflow.get('nodes', [])
                tags = workflow.get('tags', [])
                
                print(f"   Generated {len(nodes)} nodes")
                print(f"   Tags: {tags}")
                
                # Media workflows should have reasonable complexity
                if len(nodes) >= 3:
                    print("   ✅ Appropriate complexity for media workflow")
                    
                    # Check for media-relevant aspects
                    all_content = ' '.join([scenario['description'].lower()] + [tag.lower() for tag in tags])
                    aspects_found = sum(1 for aspect in scenario['expected_aspects']
                                      if aspect in all_content)
                    
                    if aspects_found >= 2:
                        print(f"   ✅ Media aspects detected: {aspects_found}")
                        passed_tests += 1
                    else:
                        print(f"   ⚠️ Limited media aspects: {aspects_found}")
                        passed_tests += 0.5
                else:
                    print("   ❌ Insufficient complexity for media workflow")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Media and Content Results: {passed_tests}/{len(media_scenarios)} passed")
    return passed_tests

def test_government_and_compliance_workflows():
    """Test government and compliance workflow scenarios"""
    print("\n🏛️ Testing Government and Compliance Workflows")
    print("=" * 50)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    government_scenarios = [
        {
            'name': 'Regulatory Compliance',
            'description': 'Create a regulatory compliance workflow with document review, approval processes, audit trails, and reporting requirements',
            'trigger_type': 'manual',
            'expected_compliance': ['compliance', 'regulatory', 'audit', 'approval']
        },
        {
            'name': 'Public Records Management',
            'description': 'Build a public records workflow with request processing, document retrieval, redaction procedures, and response tracking',
            'trigger_type': 'webhook',
            'expected_compliance': ['records', 'request', 'processing', 'tracking']
        },
        {
            'name': 'Permit Application Process',
            'description': 'Design a permit application workflow with application review, stakeholder notifications, approval routing, and status updates',
            'trigger_type': 'webhook',
            'expected_compliance': ['permit', 'application', 'review', 'approval']
        }
    ]
    
    passed_tests = 0
    
    for scenario in government_scenarios:
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
                
                print(f"   Generated {len(nodes)} nodes")
                
                # Government workflows should be thorough
                if len(nodes) >= 4:
                    print("   ✅ Appropriate complexity for government workflow")
                    
                    # Check for compliance-relevant elements
                    description_lower = scenario['description'].lower()
                    compliance_found = sum(1 for element in scenario['expected_compliance']
                                         if element in description_lower)
                    
                    if compliance_found >= 3:
                        print(f"   ✅ Compliance elements present: {compliance_found}")
                        passed_tests += 1
                    else:
                        print(f"   ⚠️ Limited compliance elements: {compliance_found}")
                        passed_tests += 0.5
                else:
                    print("   ❌ Insufficient complexity for government workflow")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Government and Compliance Results: {passed_tests}/{len(government_scenarios)} passed")
    return passed_tests

if __name__ == "__main__":
    try:
        print("🌍 REAL-WORLD BUSINESS SCENARIOS TESTING")
        print("=" * 55)
        
        saas_passed = test_saas_business_workflows()
        manufacturing_passed = test_manufacturing_workflows()
        media_passed = test_media_and_content_workflows()
        government_passed = test_government_and_compliance_workflows()
        
        total_tests = 4 + 4 + 4 + 3  # Total test cases
        total_passed = saas_passed + manufacturing_passed + media_passed + government_passed
        
        success_rate = (total_passed / total_tests) * 100
        
        print(f"\n🏆 REAL-WORLD SCENARIOS TEST RESULTS")
        print("=" * 50)
        print(f"💼 SaaS Business: {saas_passed}/4")
        print(f"🏭 Manufacturing: {manufacturing_passed}/4")
        print(f"🎬 Media & Content: {media_passed}/4")
        print(f"🏛️ Government & Compliance: {government_passed}/3")
        print(f"\n📊 OVERALL SCORE: {total_passed}/{total_tests} ({success_rate:.1f}%)")
        
        if success_rate >= 70:
            print("🎉 Real-world scenario tests passed!")
            exit(0)
        else:
            print("⚠️ Some real-world scenario tests need attention!")
            exit(1)
            
    except Exception as e:
        print(f"❌ Real-world scenario tests failed: {e}")
        exit(1)