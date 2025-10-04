#!/usr/bin/env python3
"""Advanced Error Handling and Edge Cases Testing"""

import json
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def test_extreme_input_lengths():
    """Test handling of extremely long and short inputs"""
    print("📏 Testing Extreme Input Lengths")
    print("=" * 35)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    length_tests = [
        {
            'name': 'Extremely Short Description',
            'description': 'Hi',
            'trigger_type': 'webhook',
            'should_fail': True
        },
        {
            'name': 'Minimum Valid Description',
            'description': 'Create workflow',
            'trigger_type': 'webhook',
            'should_fail': False
        },
        {
            'name': 'Very Long Description',
            'description': 'Create a comprehensive enterprise-grade workflow system ' * 100,
            'trigger_type': 'webhook',
            'should_fail': False
        },
        {
            'name': 'Maximum Length Description',
            'description': 'Build an advanced workflow ' * 200 + ' with extensive features and capabilities',
            'trigger_type': 'webhook',
            'should_fail': True  # Should exceed length limit
        }
    ]
    
    passed_tests = 0
    
    for test in length_tests:
        print(f"\n🧪 Testing: {test['name']}")
        print(f"   Description length: {len(test['description'])} characters")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': test['description'],
                                  'trigger_type': test['trigger_type']
                              }),
                              content_type='application/json')
        
        success = response.status_code == 200
        
        if test['should_fail']:
            if not success:
                print(f"   ✅ Correctly rejected (status: {response.status_code})")
                passed_tests += 1
            else:
                print(f"   ❌ Should have been rejected but was accepted")
        else:
            if success:
                print(f"   ✅ Correctly accepted")
                passed_tests += 1
            else:
                print(f"   ❌ Should have been accepted but was rejected (status: {response.status_code})")
    
    print(f"\n📊 Length Test Results: {passed_tests}/{len(length_tests)} passed")
    return passed_tests

def test_malformed_json_variations():
    """Test various malformed JSON scenarios"""
    print("\n🔧 Testing Malformed JSON Variations")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    malformed_tests = [
        {
            'name': 'Missing Closing Brace',
            'data': '{"description": "test workflow", "trigger_type": "webhook"',
            'content_type': 'application/json'
        },
        {
            'name': 'Extra Comma',
            'data': '{"description": "test workflow",, "trigger_type": "webhook"}',
            'content_type': 'application/json'
        },
        {
            'name': 'Unquoted Keys',
            'data': '{description: "test workflow", trigger_type: "webhook"}',
            'content_type': 'application/json'
        },
        {
            'name': 'Single Quotes Instead of Double',
            'data': "{'description': 'test workflow', 'trigger_type': 'webhook'}",
            'content_type': 'application/json'
        },
        {
            'name': 'Trailing Comma',
            'data': '{"description": "test workflow", "trigger_type": "webhook",}',
            'content_type': 'application/json'
        },
        {
            'name': 'Nested JSON Error',
            'data': '{"description": "test", "trigger_type": "webhook", "nested": {"invalid": json}}',
            'content_type': 'application/json'
        }
    ]
    
    passed_tests = 0
    
    for test in malformed_tests:
        print(f"\n🧪 Testing: {test['name']}")
        
        response = client.post('/generate',
                              data=test['data'],
                              content_type=test['content_type'])
        
        # Should return error status (not 200)
        if response.status_code != 200:
            print(f"   ✅ Properly rejected malformed JSON (status: {response.status_code})")
            
            # Test recovery with valid request
            recovery_response = client.post('/generate',
                                          data=json.dumps({
                                              'description': 'Recovery test after malformed JSON',
                                              'trigger_type': 'webhook'
                                          }),
                                          content_type='application/json')
            
            if recovery_response.status_code == 200:
                print("   ✅ Successfully recovered after malformed JSON")
                passed_tests += 1
            else:
                print("   ❌ Failed to recover after malformed JSON")
        else:
            print("   ❌ Unexpectedly accepted malformed JSON")
    
    print(f"\n📊 Malformed JSON Results: {passed_tests}/{len(malformed_tests)} passed")
    return passed_tests

def test_concurrent_error_scenarios():
    """Test error handling under concurrent load"""
    print("\n🔀 Testing Concurrent Error Scenarios")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    def make_error_request(request_type, request_id):
        if request_type == 'valid':
            data = json.dumps({
                'description': f'Valid workflow request {request_id}',
                'trigger_type': 'webhook'
            })
            content_type = 'application/json'
        elif request_type == 'invalid_json':
            data = '{"description": "invalid json"'
            content_type = 'application/json'
        elif request_type == 'missing_field':
            data = json.dumps({'trigger_type': 'webhook'})
            content_type = 'application/json'
        elif request_type == 'wrong_content_type':
            data = json.dumps({
                'description': 'Wrong content type test',
                'trigger_type': 'webhook'
            })
            content_type = 'text/plain'
        
        response = client.post('/generate', data=data, content_type=content_type)
        return {
            'id': request_id,
            'type': request_type,
            'status': response.status_code,
            'success': response.status_code == 200 if request_type == 'valid' else response.status_code != 200
        }
    
    # Mix of valid and invalid requests
    request_types = ['valid', 'invalid_json', 'missing_field', 'wrong_content_type'] * 5  # 20 total requests
    
    print("🧪 Sending 20 concurrent mixed requests (valid and invalid)...")
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_error_request, req_type, i) 
                  for i, req_type in enumerate(request_types)]
        results = [future.result() for future in as_completed(futures)]
    
    # Analyze results
    valid_requests = [r for r in results if r['type'] == 'valid']
    error_requests = [r for r in results if r['type'] != 'valid']
    
    valid_success = sum(1 for r in valid_requests if r['success'])
    error_handled = sum(1 for r in error_requests if r['success'])
    
    print(f"   Valid requests handled: {valid_success}/{len(valid_requests)}")
    print(f"   Error requests handled: {error_handled}/{len(error_requests)}")
    
    # Success criteria: 90% of valid requests succeed, 90% of errors properly handled
    valid_rate = (valid_success / len(valid_requests)) * 100 if valid_requests else 100
    error_rate = (error_handled / len(error_requests)) * 100 if error_requests else 100
    
    if valid_rate >= 90 and error_rate >= 90:
        print("   ✅ Concurrent error handling successful")
        return True
    else:
        print(f"   ❌ Concurrent error handling issues (valid: {valid_rate:.1f}%, error: {error_rate:.1f}%)")
        return False

def test_resource_exhaustion_scenarios():
    """Test behavior under resource exhaustion scenarios"""
    print("\n💾 Testing Resource Exhaustion Scenarios")
    print("=" * 45)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    exhaustion_tests = [
        {
            'name': 'Rapid Sequential Requests',
            'test_func': lambda: test_rapid_requests(client)
        },
        {
            'name': 'Large Payload Processing',
            'test_func': lambda: test_large_payload(client)
        },
        {
            'name': 'Complex Description Processing',
            'test_func': lambda: test_complex_description(client)
        }
    ]
    
    passed_tests = 0
    
    for test in exhaustion_tests:
        print(f"\n🧪 Testing: {test['name']}")
        
        try:
            result = test['test_func']()
            if result:
                print("   ✅ Resource exhaustion handled gracefully")
                passed_tests += 1
            else:
                print("   ❌ Resource exhaustion caused issues")
        except Exception as e:
            print(f"   ❌ Resource exhaustion test failed: {e}")
    
    print(f"\n📊 Resource Exhaustion Results: {passed_tests}/{len(exhaustion_tests)} passed")
    return passed_tests

def test_rapid_requests(client):
    """Test rapid sequential requests"""
    success_count = 0
    for i in range(20):
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': f'Rapid request {i} for resource testing',
                                  'trigger_type': 'webhook'
                              }),
                              content_type='application/json')
        if response.status_code == 200:
            success_count += 1
    
    return success_count >= 18  # 90% success rate

def test_large_payload(client):
    """Test large payload handling"""
    large_description = "Create a comprehensive workflow " * 50  # Large but within limits
    
    response = client.post('/generate',
                          data=json.dumps({
                              'description': large_description,
                              'trigger_type': 'webhook',
                              'complexity': 'complex'
                          }),
                          content_type='application/json')
    
    return response.status_code == 200

def test_complex_description(client):
    """Test complex description processing"""
    complex_description = """
    Create an enterprise-grade multi-tenant SaaS workflow system with the following requirements:
    1. User authentication and authorization with RBAC
    2. Multi-database support with automatic sharding
    3. Real-time event processing with message queues
    4. Microservices architecture with service discovery
    5. API gateway with rate limiting and caching
    6. Monitoring and alerting with custom metrics
    7. Automated deployment with blue-green strategies
    8. Data encryption at rest and in transit
    9. Compliance with SOC2, GDPR, and HIPAA
    10. Multi-region deployment with disaster recovery
    """
    
    response = client.post('/generate',
                          data=json.dumps({
                              'description': complex_description,
                              'trigger_type': 'webhook',
                              'complexity': 'complex'
                          }),
                          content_type='application/json')
    
    return response.status_code == 200

if __name__ == "__main__":
    try:
        print("🛡️ ADVANCED ERROR HANDLING AND EDGE CASES TESTING")
        print("=" * 65)
        
        length_passed = test_extreme_input_lengths()
        malformed_passed = test_malformed_json_variations()
        concurrent_passed = test_concurrent_error_scenarios()
        exhaustion_passed = test_resource_exhaustion_scenarios()
        
        total_tests = 4 + 6 + 1 + 3  # Total test cases
        total_passed = length_passed + malformed_passed + (1 if concurrent_passed else 0) + exhaustion_passed
        
        success_rate = (total_passed / total_tests) * 100
        
        print(f"\n🏆 ADVANCED ERROR HANDLING TEST RESULTS")
        print("=" * 55)
        print(f"📏 Extreme Lengths: {length_passed}/4")
        print(f"🔧 Malformed JSON: {malformed_passed}/6")
        print(f"🔀 Concurrent Errors: {'1/1' if concurrent_passed else '0/1'}")
        print(f"💾 Resource Exhaustion: {exhaustion_passed}/3")
        print(f"\n📊 OVERALL SCORE: {total_passed}/{total_tests} ({success_rate:.1f}%)")
        
        if success_rate >= 80:
            print("🎉 Advanced error handling tests passed!")
            exit(0)
        else:
            print("⚠️ Some advanced error handling tests need attention!")
            exit(1)
            
    except Exception as e:
        print(f"❌ Advanced error handling tests failed: {e}")
        exit(1)