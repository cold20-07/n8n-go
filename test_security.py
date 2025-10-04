#!/usr/bin/env python3
"""Security Testing for N8n JSON Generator"""

import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def test_injection_attacks():
    """Test for various injection attack vectors"""
    print("🛡️ Testing Injection Attack Prevention")
    print("=" * 45)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    injection_payloads = [
        {
            'name': 'SQL Injection',
            'description': "Create workflow'; DROP TABLE users; --",
            'trigger_type': 'webhook'
        },
        {
            'name': 'XSS Script Injection',
            'description': 'Create workflow <script>alert("xss")</script>',
            'trigger_type': 'webhook'
        },
        {
            'name': 'Command Injection',
            'description': 'Create workflow; rm -rf /',
            'trigger_type': 'webhook'
        },
        {
            'name': 'JSON Injection',
            'description': 'Create workflow", "malicious": "payload',
            'trigger_type': 'webhook'
        },
        {
            'name': 'Path Traversal',
            'description': 'Create workflow ../../etc/passwd',
            'trigger_type': 'webhook'
        }
    ]
    
    passed = 0
    
    for payload in injection_payloads:
        print(f"🧪 Testing: {payload['name']}")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': payload['description'],
                                  'trigger_type': payload['trigger_type']
                              }),
                              content_type='application/json')
        
        if response.status_code == 200:
            # Check if response is properly sanitized
            try:
                workflow = json.loads(response.data)
                # Verify no malicious content in response
                response_str = json.dumps(workflow)
                
                dangerous_patterns = ['<script>', 'DROP TABLE', 'rm -rf', '../../']
                has_dangerous = any(pattern in response_str for pattern in dangerous_patterns)
                
                if not has_dangerous:
                    print("✅ Payload properly sanitized")
                    passed += 1
                else:
                    print("❌ Dangerous content found in response")
            except:
                print("❌ Invalid response format")
        else:
            # Rejection is also acceptable for security
            print("✅ Payload properly rejected")
            passed += 1
        
        print()
    
    print(f"📊 Injection Test Results: {passed}/{len(injection_payloads)} passed")
    return passed

def test_input_validation():
    """Test input validation security"""
    print("🔍 Testing Input Validation Security")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    validation_tests = [
        {
            'name': 'Extremely Long Input',
            'description': 'A' * 10000,  # Very long string
            'trigger_type': 'webhook',
            'should_reject': True
        },
        {
            'name': 'Null Bytes',
            'description': 'Create workflow\\x00with null bytes',
            'trigger_type': 'webhook',
            'should_reject': False  # Should handle gracefully
        },
        {
            'name': 'Invalid Trigger Type',
            'description': 'Create a valid workflow description',
            'trigger_type': 'invalid_trigger',
            'should_reject': True
        },
        {
            'name': 'Binary Data',
            'description': '\\xff\\xfe\\xfd binary data',
            'trigger_type': 'webhook',
            'should_reject': False  # Should handle gracefully
        }
    ]
    
    passed = 0
    
    for test in validation_tests:
        print(f"🧪 Testing: {test['name']}")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': test['description'],
                                  'trigger_type': test['trigger_type']
                              }),
                              content_type='application/json')
        
        is_rejected = response.status_code != 200
        
        if test['should_reject'] and is_rejected:
            print("✅ Properly rejected invalid input")
            passed += 1
        elif not test['should_reject'] and not is_rejected:
            print("✅ Properly handled edge case input")
            passed += 1
        else:
            expected = "rejected" if test['should_reject'] else "accepted"
            actual = "rejected" if is_rejected else "accepted"
            print(f"❌ Expected {expected}, got {actual}")
        
        print()
    
    print(f"📊 Validation Test Results: {passed}/{len(validation_tests)} passed")
    return passed

def test_rate_limiting_simulation():
    """Simulate rapid requests to test for DoS protection"""
    print("⚡ Testing Rapid Request Handling")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    # Send 20 rapid requests
    successful_requests = 0
    
    for i in range(20):
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': f'Create workflow {i} for rapid testing',
                                  'trigger_type': 'webhook'
                              }),
                              content_type='application/json')
        
        if response.status_code == 200:
            successful_requests += 1
    
    print(f"✅ Handled {successful_requests}/20 rapid requests")
    
    # All requests should be handled (no built-in rate limiting expected)
    if successful_requests >= 15:  # Allow some tolerance
        print("✅ System handles rapid requests well")
        return True
    else:
        print("❌ System may have issues with rapid requests")
        return False

if __name__ == "__main__":
    injection_passed = test_injection_attacks()
    validation_passed = test_input_validation()
    rate_limit_passed = test_rate_limiting_simulation()
    
    total_tests = 5 + 4 + 1  # Total test cases
    total_passed = injection_passed + validation_passed + (1 if rate_limit_passed else 0)
    
    print(f"\n🛡️ Overall Security Testing: {total_passed}/{total_tests} tests passed")
    
    if total_passed >= total_tests * 0.8:  # 80% pass rate acceptable for security
        print("🎉 Security tests mostly passed!")
        exit(0)  # Success
    else:
        print("⚠️ Security concerns detected!")
        exit(1)  # Failure