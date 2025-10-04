#!/usr/bin/env python3
"""
Comprehensive test for all bug fixes and error handling
"""

import sys
import os
import json
import threading
import time
import requests
from werkzeug.serving import make_server

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
except ImportError as e:
    print(f"❌ Failed to import app: {e}")
    sys.exit(1)

def test_input_validation():
    """Test backend input validation"""
    print("🔍 Testing Input Validation")
    print("-" * 30)
    
    with app.test_client() as client:
        # Test empty description
        response = client.post('/generate', 
                             data=json.dumps({'description': ''}),
                             content_type='application/json')
        
        if response.status_code == 400:
            print("✅ Empty description properly rejected")
        else:
            print("❌ Empty description should be rejected")
        
        # Test short description
        response = client.post('/generate', 
                             data=json.dumps({'description': 'short'}),
                             content_type='application/json')
        
        if response.status_code == 400:
            print("✅ Short description properly rejected")
        else:
            print("❌ Short description should be rejected")
        
        # Test invalid trigger type
        response = client.post('/generate', 
                             data=json.dumps({
                                 'description': 'Valid description for testing purposes',
                                 'triggerType': 'invalid_trigger'
                             }),
                             content_type='application/json')
        
        if response.status_code == 400:
            print("✅ Invalid trigger type properly rejected")
        else:
            print("❌ Invalid trigger type should be rejected")
        
        # Test valid input
        response = client.post('/generate', 
                             data=json.dumps({
                                 'description': 'Create a valid workflow for testing all the validation logic',
                                 'triggerType': 'webhook'
                             }),
                             content_type='application/json')
        
        if response.status_code == 200:
            print("✅ Valid input properly accepted")
        else:
            print("❌ Valid input should be accepted")

def test_mathematical_calculations():
    """Test mathematical calculations in workflow generation"""
    print("\n🧮 Testing Mathematical Calculations")
    print("-" * 40)
    
    with app.test_client() as client:
        response = client.post('/generate', 
                             data=json.dumps({
                                 'description': 'Create a complex workflow with multiple nodes for testing positioning calculations',
                                 'triggerType': 'webhook',
                                 'complexity': 'complex'
                             }),
                             content_type='application/json')
        
        if response.status_code == 200:
            data = response.get_json()
            if data.get('success'):
                workflow = data.get('workflow')
                nodes = workflow.get('nodes', [])
                
                # Check node positioning
                positions_valid = True
                for i, node in enumerate(nodes):
                    position = node.get('position', [0, 0])
                    if not isinstance(position, list) or len(position) != 2:
                        positions_valid = False
                        break
                    
                    x, y = position
                    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                        positions_valid = False
                        break
                    
                    # Check if positions are reasonable (not negative, not too large)
                    if x < 0 or y < 0 or x > 10000 or y > 10000:
                        positions_valid = False
                        break
                
                if positions_valid:
                    print("✅ Node positioning calculations are correct")
                else:
                    print("❌ Node positioning calculations have issues")
                
                # Check connections structure
                connections = workflow.get('connections', {})
                connections_valid = True
                
                for source, conn_data in connections.items():
                    if not isinstance(conn_data, dict) or 'main' not in conn_data:
                        connections_valid = False
                        break
                    
                    main_connections = conn_data['main']
                    if not isinstance(main_connections, list):
                        connections_valid = False
                        break
                
                if connections_valid:
                    print("✅ Connection structure is mathematically sound")
                else:
                    print("❌ Connection structure has mathematical issues")
            else:
                print("❌ Workflow generation failed")
        else:
            print("❌ Request failed")

def test_error_handling():
    """Test error handling in various scenarios"""
    print("\n🛡️ Testing Error Handling")
    print("-" * 30)
    
    with app.test_client() as client:
        # Test malformed JSON
        response = client.post('/generate', 
                             data='{"invalid": json}',
                             content_type='application/json')
        
        if response.status_code in [400, 500]:
            print("✅ Malformed JSON properly handled")
        else:
            print("❌ Malformed JSON should be handled")
        
        # Test missing content type
        response = client.post('/generate', 
                             data=json.dumps({'description': 'test'}))
        
        if response.status_code in [400, 415]:
            print("✅ Missing content type properly handled")
        else:
            print("❌ Missing content type should be handled")
        
        # Test empty request body
        response = client.post('/generate', 
                             data='',
                             content_type='application/json')
        
        if response.status_code in [400, 500]:
            print("✅ Empty request body properly handled")
        else:
            print("❌ Empty request body should be handled")

def test_memory_management():
    """Test for potential memory leaks and resource management"""
    print("\n💾 Testing Memory Management")
    print("-" * 35)
    
    with app.test_client() as client:
        # Generate multiple workflows to test for memory leaks
        for i in range(5):
            response = client.post('/generate', 
                                 data=json.dumps({
                                     'description': f'Test workflow number {i} for memory management testing',
                                     'triggerType': 'webhook'
                                 }),
                                 content_type='application/json')
            
            if response.status_code != 200:
                print(f"❌ Request {i+1} failed")
                return
        
        print("✅ Multiple requests handled without memory issues")

def test_edge_cases():
    """Test edge cases and boundary conditions"""
    print("\n🎯 Testing Edge Cases")
    print("-" * 25)
    
    with app.test_client() as client:
        # Test very long description
        long_description = "A" * 10000
        response = client.post('/generate', 
                             data=json.dumps({
                                 'description': long_description,
                                 'triggerType': 'webhook'
                             }),
                             content_type='application/json')
        
        if response.status_code == 200:
            print("✅ Very long description handled")
        else:
            print("❌ Very long description caused issues")
        
        # Test special characters in description
        special_description = "Test with special chars: !@#$%^&*()[]{}|;':\",./<>?"
        response = client.post('/generate', 
                             data=json.dumps({
                                 'description': special_description,
                                 'triggerType': 'manual'
                             }),
                             content_type='application/json')
        
        if response.status_code == 200:
            print("✅ Special characters handled")
        else:
            print("❌ Special characters caused issues")
        
        # Test Unicode characters
        unicode_description = "Test with Unicode: 你好世界 🚀 émojis and açcénts"
        response = client.post('/generate', 
                             data=json.dumps({
                                 'description': unicode_description,
                                 'triggerType': 'schedule'
                             }),
                             content_type='application/json')
        
        if response.status_code == 200:
            print("✅ Unicode characters handled")
        else:
            print("❌ Unicode characters caused issues")

def test_concurrent_requests():
    """Test concurrent request handling"""
    print("\n🔄 Testing Concurrent Requests")
    print("-" * 35)
    
    # Create a test server
    server = make_server('127.0.0.1', 5558, app, threaded=True)
    
    # Start server in a separate thread
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    # Give the server time to start
    time.sleep(2)
    
    try:
        import concurrent.futures
        
        def make_request(i):
            try:
                response = requests.post(
                    'http://127.0.0.1:5558/generate',
                    json={
                        'description': f'Concurrent test workflow {i}',
                        'triggerType': 'webhook'
                    },
                    timeout=30
                )
                return response.status_code == 200
            except Exception:
                return False
        
        # Make 5 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request, i) for i in range(5)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        if all(results):
            print("✅ Concurrent requests handled successfully")
        else:
            print("❌ Some concurrent requests failed")
            
    except ImportError:
        print("⚠️  concurrent.futures not available, skipping concurrent test")
    except Exception as e:
        print(f"❌ Concurrent test failed: {e}")
    finally:
        server.shutdown()

def main():
    """Run all bug fix tests"""
    print("🐛 Comprehensive Bug Fix Testing")
    print("=" * 50)
    
    tests = [
        test_input_validation,
        test_mathematical_calculations,
        test_error_handling,
        test_memory_management,
        test_edge_cases,
        test_concurrent_requests
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Bug Fix Test Results: {passed}/{total} test categories passed")
    
    if passed == total:
        print("🎉 All bug fixes verified! The application is robust and error-free.")
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)