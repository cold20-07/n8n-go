#!/usr/bin/env python3
"""Edge Case Testing for N8n JSON Generator"""

import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def test_extreme_inputs():
    """Test with extreme input scenarios"""
    print("🎯 Testing Extreme Input Cases")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    test_cases = [
        {
            'name': 'Very Long Description',
            'description': 'Create a workflow ' + 'with many details ' * 50,
            'trigger_type': 'webhook',
            'should_pass': True
        },
        {
            'name': 'Minimal Description',
            'description': 'Short',  # Only 5 characters - should fail
            'trigger_type': 'webhook',
            'should_pass': False  # Too short
        },
        {
            'name': 'Special Characters',
            'description': 'Create workflow with special chars: @#$%^&*()[]{}|\\:";\'<>?,./`~',
            'trigger_type': 'webhook',
            'should_pass': True
        },
        {
            'name': 'Unicode Characters',
            'description': 'Create workflow with émojis 🚀 and ünïcödé characters',
            'trigger_type': 'webhook',
            'should_pass': True
        },
        {
            'name': 'Numbers Only',
            'description': '123456789 workflow automation system',
            'trigger_type': 'webhook',
            'should_pass': True
        }
    ]
    
    passed = 0
    
    for case in test_cases:
        print(f"🧪 Testing: {case['name']}")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': case['description'],
                                  'trigger_type': case['trigger_type']
                              }),
                              content_type='application/json')
        
        success = response.status_code == 200
        
        if success == case['should_pass']:
            print(f"✅ Expected result: {'Success' if success else 'Failure'}")
            passed += 1
        else:
            print(f"❌ Unexpected result: {'Success' if success else 'Failure'}")
        
        print()
    
    print(f"📊 Edge Case Results: {passed}/{len(test_cases)} passed")
    return passed

def test_malformed_requests():
    """Test handling of malformed requests"""
    print("🔧 Testing Malformed Request Handling")
    print("=" * 45)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    malformed_cases = [
        {
            'name': 'Invalid JSON',
            'data': '{invalid json}',
            'content_type': 'application/json'
        },
        {
            'name': 'Missing Content-Type',
            'data': json.dumps({'description': 'test', 'trigger_type': 'webhook'}),
            'content_type': None
        },
        {
            'name': 'Empty Body',
            'data': '',
            'content_type': 'application/json'
        },
        {
            'name': 'Wrong Content-Type',
            'data': json.dumps({'description': 'test', 'trigger_type': 'webhook'}),
            'content_type': 'text/plain'
        }
    ]
    
    passed = 0
    
    for case in malformed_cases:
        print(f"🧪 Testing: {case['name']}")
        
        kwargs = {'data': case['data']}
        if case['content_type']:
            kwargs['content_type'] = case['content_type']
        
        response = client.post('/generate', **kwargs)
        
        # Should return error status (not 200)
        if response.status_code != 200:
            print(f"✅ Properly rejected with status {response.status_code}")
            passed += 1
        else:
            print(f"❌ Unexpectedly accepted malformed request")
        
        print()
    
    print(f"📊 Malformed Request Results: {passed}/{len(malformed_cases)} passed")
    return passed

def test_boundary_conditions():
    """Test boundary conditions"""
    print("📏 Testing Boundary Conditions")
    print("=" * 35)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    # Test minimum valid description length
    min_desc = "Create a basic workflow for data processing tasks"
    response = client.post('/generate',
                          data=json.dumps({
                              'description': min_desc,
                              'trigger_type': 'webhook'
                          }),
                          content_type='application/json')
    
    min_length_pass = response.status_code == 200
    print(f"✅ Minimum length description: {'Passed' if min_length_pass else 'Failed'}")
    
    # Test all trigger types
    trigger_types = ['webhook', 'schedule', 'manual']
    trigger_pass = 0
    
    for trigger in trigger_types:
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': 'Create a workflow for testing trigger types',
                                  'trigger_type': trigger
                              }),
                              content_type='application/json')
        
        if response.status_code == 200:
            trigger_pass += 1
            print(f"✅ Trigger type '{trigger}': Passed")
        else:
            print(f"❌ Trigger type '{trigger}': Failed")
    
    print(f"📊 Boundary Condition Results: {trigger_pass + (1 if min_length_pass else 0)}/{len(trigger_types) + 1} passed")
    return trigger_pass + (1 if min_length_pass else 0)

if __name__ == "__main__":
    extreme_passed = test_extreme_inputs()
    malformed_passed = test_malformed_requests()
    boundary_passed = test_boundary_conditions()
    
    total_tests = 5 + 4 + 4  # Total test cases across all functions
    total_passed = extreme_passed + malformed_passed + boundary_passed
    
    print(f"\n🎯 Overall Edge Case Testing: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("🎉 All edge case tests passed!")
        exit(0)  # Success
    else:
        print("⚠️ Some edge case tests failed!")
        exit(1)  # Failure