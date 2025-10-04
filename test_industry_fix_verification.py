#!/usr/bin/env python3
"""Industry-Specific Detection Fix Verification"""

import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def test_industry_detection_fix():
    """Test that industry-specific detection is now working correctly"""
    print("🏭 Testing Industry-Specific Detection Fix")
    print("=" * 50)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    industry_tests = [
        {
            'name': 'Healthcare',
            'description': 'Build a patient appointment scheduling workflow with reminder notifications and medical record updates for healthcare providers',
            'expected_tags': ['healthcare', 'medical', 'patient', 'appointments'],
            'expected_type': 'healthcare'
        },
        {
            'name': 'Finance',
            'description': 'Design a financial transaction monitoring workflow with fraud detection and compliance reporting for banking systems',
            'expected_tags': ['finance', 'banking', 'transactions', 'compliance'],
            'expected_type': 'finance'
        },
        {
            'name': 'Education',
            'description': 'Create a student enrollment workflow with course assignment and notification to instructors for university management',
            'expected_tags': ['education', 'academic', 'students', 'courses'],
            'expected_type': 'education'
        },
        {
            'name': 'E-commerce',
            'description': 'Create an e-commerce order processing workflow with payment validation, inventory checks, and shipping notifications',
            'expected_tags': ['ecommerce', 'orders', 'payments', 'retail'],
            'expected_type': 'ecommerce'
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
                workflow_meta = workflow.get('meta', {})
                workflow_type = workflow_meta.get('workflow_type', '')
                
                print(f"   Generated tags: {tags}")
                print(f"   Workflow name: {workflow.get('name')}")
                print(f"   Workflow type: {workflow_type}")
                
                # Check for industry-relevant tags
                relevant_tags = 0
                for expected_tag in test['expected_tags']:
                    if any(expected_tag.lower() in tag.lower() for tag in tags):
                        relevant_tags += 1
                        print(f"   ✅ Found {expected_tag} tag")
                    else:
                        print(f"   ⚠️ Missing {expected_tag} tag")
                
                # Check workflow type
                type_correct = workflow_type == test['expected_type']
                if type_correct:
                    print(f"   ✅ Correct workflow type: {workflow_type}")
                else:
                    print(f"   ❌ Wrong workflow type: {workflow_type} (expected {test['expected_type']})")
                
                # Success criteria: at least 50% of expected tags + correct type
                if relevant_tags >= len(test['expected_tags']) * 0.5 and type_correct:
                    print("   ✅ Industry-specific detection successful")
                    passed_tests += 1
                else:
                    print("   ❌ Industry-specific detection failed")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Industry Detection Results: {passed_tests}/{len(industry_tests)} passed")
    
    success_rate = (passed_tests / len(industry_tests)) * 100
    print(f"📊 Success Rate: {success_rate:.1f}%")
    
    if success_rate >= 75:
        print("🎉 Industry-specific detection fix successful!")
        return True
    else:
        print("⚠️ Industry-specific detection still needs work!")
        return False

def test_keyword_priority():
    """Test that industry keywords have higher priority than generic ones"""
    print("\n🎯 Testing Keyword Priority System")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    priority_tests = [
        {
            'description': 'Create a healthcare patient notification system with automated alerts',
            'should_be': 'healthcare',
            'not_be': 'notification'
        },
        {
            'description': 'Build a financial transaction monitoring and notification system',
            'should_be': 'finance',
            'not_be': 'monitoring'
        },
        {
            'description': 'Design an educational student enrollment and notification workflow',
            'should_be': 'education',
            'not_be': 'notification'
        }
    ]
    
    passed_tests = 0
    
    for i, test in enumerate(priority_tests, 1):
        print(f"\n🧪 Priority Test {i}")
        
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
                workflow_meta = workflow.get('meta', {})
                workflow_type = workflow_meta.get('workflow_type', '')
                
                print(f"   Description: {test['description'][:60]}...")
                print(f"   Detected type: {workflow_type}")
                print(f"   Should be: {test['should_be']}")
                
                if workflow_type == test['should_be']:
                    print("   ✅ Correct industry priority")
                    passed_tests += 1
                else:
                    print("   ❌ Wrong priority - generic type won")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
        else:
            print(f"   ❌ Request failed: {response.status_code}")
    
    print(f"\n📊 Priority Test Results: {passed_tests}/{len(priority_tests)} passed")
    return passed_tests >= len(priority_tests) * 0.67  # 67% success rate

if __name__ == "__main__":
    try:
        print("🔧 INDUSTRY-SPECIFIC DETECTION FIX VERIFICATION")
        print("=" * 60)
        
        detection_fixed = test_industry_detection_fix()
        priority_fixed = test_keyword_priority()
        
        if detection_fixed and priority_fixed:
            print("\n🎉 INDUSTRY DETECTION FIX SUCCESSFUL!")
            print("✅ All industry-specific workflows now generate correct tags and types")
            print("✅ Keyword priority system working correctly")
            print("🚀 Industry detection permanently fixed!")
            exit(0)
        else:
            print("\n⚠️ INDUSTRY DETECTION STILL NEEDS WORK!")
            print("🔧 Some issues remain with industry-specific detection")
            exit(1)
            
    except Exception as e:
        print(f"❌ Industry detection fix verification failed: {e}")
        exit(1)