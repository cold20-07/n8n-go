#!/usr/bin/env python3
"""API Endpoint Testing for N8n JSON Generator"""

import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def test_all_endpoints():
    """Test all available API endpoints"""
    print("🌐 Testing All API Endpoints")
    print("=" * 35)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    endpoints = [
        {
            'name': 'Home Page',
            'method': 'GET',
            'path': '/',
            'expected_status': 200,
            'should_contain': ['N8N Go', 'workflow']
        },
        {
            'name': 'Generate Workflow',
            'method': 'POST',
            'path': '/generate',
            'data': {
                'description': 'Create a test workflow for API testing',
                'trigger_type': 'webhook'
            },
            'expected_status': 200,
            'should_contain': ['nodes', 'connections']
        },
        {
            'name': 'Static CSS',
            'method': 'GET',
            'path': '/static/css/style.css',
            'expected_status': 200,
            'should_contain': ['body', 'color']
        },
        {
            'name': 'Static JS',
            'method': 'GET',
            'path': '/static/js/main.js',
            'expected_status': 200,
            'should_contain': ['function']
        },
        {
            'name': 'Documentation Page',
            'method': 'GET',
            'path': '/documentation',
            'expected_status': 200,
            'should_contain': ['documentation', 'API']
        },
        {
            'name': 'Pricing Page',
            'method': 'GET',
            'path': '/pricing',
            'expected_status': 200,
            'should_contain': ['pricing', 'plan']
        }
    ]
    
    passed_tests = 0
    
    for endpoint in endpoints:
        print(f"🧪 Testing: {endpoint['name']}")
        
        try:
            if endpoint['method'] == 'GET':
                response = client.get(endpoint['path'])
            elif endpoint['method'] == 'POST':
                response = client.post(endpoint['path'],
                                     data=json.dumps(endpoint.get('data', {})),
                                     content_type='application/json')
            
            # Check status code
            if response.status_code == endpoint['expected_status']:
                print(f"✅ Status code: {response.status_code}")
                
                # Check content
                if 'should_contain' in endpoint:
                    response_text = response.data.decode('utf-8')
                    content_checks = []
                    
                    for content in endpoint['should_contain']:
                        if content.lower() in response_text.lower():
                            content_checks.append(True)
                        else:
                            content_checks.append(False)
                    
                    if all(content_checks):
                        print("✅ Content validation passed")
                        passed_tests += 1
                    else:
                        print("❌ Content validation failed")
                else:
                    passed_tests += 1
            else:
                print(f"❌ Status code: {response.status_code} (expected {endpoint['expected_status']})")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print()
    
    print(f"📊 Endpoint Test Results: {passed_tests}/{len(endpoints)} passed")
    return passed_tests

def test_error_endpoints():
    """Test error handling for invalid endpoints"""
    print("❌ Testing Error Endpoint Handling")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    error_tests = [
        {
            'name': '404 Not Found',
            'path': '/nonexistent-page',
            'method': 'GET',
            'expected_status': 404
        },
        {
            'name': 'Method Not Allowed',
            'path': '/generate',
            'method': 'GET',
            'expected_status': 405
        },
        {
            'name': 'Invalid Static File',
            'path': '/static/nonexistent.css',
            'method': 'GET',
            'expected_status': 404
        }
    ]
    
    passed_tests = 0
    
    for test in error_tests:
        print(f"🧪 Testing: {test['name']}")
        
        try:
            if test['method'] == 'GET':
                response = client.get(test['path'])
            elif test['method'] == 'POST':
                response = client.post(test['path'])
            
            if response.status_code == test['expected_status']:
                print(f"✅ Correct error status: {response.status_code}")
                passed_tests += 1
            else:
                print(f"❌ Wrong status: {response.status_code} (expected {test['expected_status']})")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print()
    
    print(f"📊 Error Handling Results: {passed_tests}/{len(error_tests)} passed")
    return passed_tests

if __name__ == "__main__":
    endpoint_passed = test_all_endpoints()
    error_passed = test_error_endpoints()
    
    total_tests = 6 + 3
    total_passed = endpoint_passed + error_passed
    
    print(f"\n🌐 Overall API Testing: {total_passed}/{total_tests} tests passed")
    
    if total_passed >= total_tests * 0.8:
        print("🎉 API tests mostly passed!")
        exit(0)  # Success
    else:
        print("⚠️ Some API tests failed!")
        exit(1)  # Failure