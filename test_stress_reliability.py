#!/usr/bin/env python3
"""Stress and Reliability Testing for N8n JSON Generator"""

import json
import sys
import os
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def test_high_volume_requests():
    """Test handling of high volume requests"""
    print("📈 Testing High Volume Request Handling")
    print("=" * 45)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    def make_request(request_id):
        start_time = time.time()
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': f'Create workflow {request_id} for high volume testing with data processing and notifications',
                                  'trigger_type': 'webhook',
                                  'complexity': 'medium'
                              }),
                              content_type='application/json')
        end_time = time.time()
        
        return {
            'id': request_id,
            'success': response.status_code == 200,
            'response_time': end_time - start_time,
            'status_code': response.status_code
        }
    
    # Test with 50 concurrent requests
    num_requests = 50
    print(f"🧪 Sending {num_requests} concurrent requests...")
    
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(make_request, i) for i in range(num_requests)]
        results = [future.result() for future in as_completed(futures)]
    
    end_time = time.time()
    total_time = end_time - start_time
    
    # Analyze results
    successful_requests = sum(1 for r in results if r['success'])
    failed_requests = num_requests - successful_requests
    avg_response_time = sum(r['response_time'] for r in results) / len(results)
    max_response_time = max(r['response_time'] for r in results)
    min_response_time = min(r['response_time'] for r in results)
    
    print(f"✅ Total time: {total_time:.2f}s")
    print(f"✅ Successful requests: {successful_requests}/{num_requests}")
    print(f"✅ Failed requests: {failed_requests}")
    print(f"✅ Average response time: {avg_response_time:.3f}s")
    print(f"✅ Min response time: {min_response_time:.3f}s")
    print(f"✅ Max response time: {max_response_time:.3f}s")
    print(f"✅ Requests per second: {num_requests/total_time:.2f}")
    
    # Success criteria: 90% success rate, average response time < 1s
    success_rate = (successful_requests / num_requests) * 100
    performance_good = avg_response_time < 1.0
    
    if success_rate >= 90 and performance_good:
        print("🎉 High volume test passed!")
        return True
    else:
        print("⚠️ High volume test needs attention!")
        return False

def test_memory_stability():
    """Test memory stability over repeated requests"""
    print("\n🧠 Testing Memory Stability")
    print("=" * 35)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    # Make 100 sequential requests to test for memory leaks
    num_requests = 100
    print(f"🧪 Making {num_requests} sequential requests...")
    
    successful_requests = 0
    response_times = []
    
    for i in range(num_requests):
        start_time = time.time()
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': f'Memory stability test workflow {i} with complex data processing and multiple integrations',
                                  'trigger_type': 'webhook',
                                  'complexity': 'complex'
                              }),
                              content_type='application/json')
        
        end_time = time.time()
        response_time = end_time - start_time
        response_times.append(response_time)
        
        if response.status_code == 200:
            successful_requests += 1
        
        # Print progress every 20 requests
        if (i + 1) % 20 == 0:
            avg_time = sum(response_times[-20:]) / 20
            print(f"   Progress: {i+1}/{num_requests}, Avg time (last 20): {avg_time:.3f}s")
    
    # Analyze stability
    first_quarter = response_times[:25]
    last_quarter = response_times[-25:]
    
    avg_first = sum(first_quarter) / len(first_quarter)
    avg_last = sum(last_quarter) / len(last_quarter)
    
    print(f"✅ Successful requests: {successful_requests}/{num_requests}")
    print(f"✅ Average response time (first 25): {avg_first:.3f}s")
    print(f"✅ Average response time (last 25): {avg_last:.3f}s")
    print(f"✅ Performance degradation: {((avg_last - avg_first) / avg_first * 100):.1f}%")
    
    # Success criteria: 95% success rate, less than 50% performance degradation
    success_rate = (successful_requests / num_requests) * 100
    degradation = ((avg_last - avg_first) / avg_first * 100) if avg_first > 0 else 0
    
    if success_rate >= 95 and degradation < 50:
        print("🎉 Memory stability test passed!")
        return True
    else:
        print("⚠️ Memory stability test needs attention!")
        return False

def test_error_recovery():
    """Test error recovery and resilience"""
    print("\n🛡️ Testing Error Recovery and Resilience")
    print("=" * 45)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    # Test various error scenarios and recovery
    error_scenarios = [
        {
            'name': 'Invalid JSON Recovery',
            'data': '{invalid json}',
            'content_type': 'application/json',
            'should_recover': True
        },
        {
            'name': 'Missing Content Type Recovery',
            'data': json.dumps({'description': 'Test workflow', 'trigger_type': 'webhook'}),
            'content_type': None,
            'should_recover': True
        },
        {
            'name': 'Empty Request Recovery',
            'data': '',
            'content_type': 'application/json',
            'should_recover': True
        }
    ]
    
    recovery_tests_passed = 0
    
    for scenario in error_scenarios:
        print(f"\n🧪 Testing: {scenario['name']}")
        
        # Send error request
        kwargs = {'data': scenario['data']}
        if scenario['content_type']:
            kwargs['content_type'] = scenario['content_type']
        
        error_response = client.post('/generate', **kwargs)
        print(f"   Error response: {error_response.status_code}")
        
        # Test recovery with valid request immediately after
        recovery_response = client.post('/generate',
                                      data=json.dumps({
                                          'description': 'Recovery test workflow after error scenario',
                                          'trigger_type': 'webhook'
                                      }),
                                      content_type='application/json')
        
        if recovery_response.status_code == 200:
            print("   ✅ Successfully recovered after error")
            recovery_tests_passed += 1
        else:
            print("   ❌ Failed to recover after error")
    
    print(f"\n📊 Error Recovery Results: {recovery_tests_passed}/{len(error_scenarios)} passed")
    
    return recovery_tests_passed >= len(error_scenarios) * 0.8  # 80% recovery rate

def test_concurrent_different_requests():
    """Test concurrent requests with different parameters"""
    print("\n🔀 Testing Concurrent Different Request Types")
    print("=" * 50)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    # Different request types
    request_types = [
        {'description': 'Simple webhook workflow', 'trigger_type': 'webhook', 'complexity': 'simple'},
        {'description': 'Complex schedule workflow with multiple integrations', 'trigger_type': 'schedule', 'complexity': 'complex'},
        {'description': 'Medium manual workflow for data processing', 'trigger_type': 'manual', 'complexity': 'medium'},
        {'description': 'E-commerce order processing workflow', 'trigger_type': 'webhook', 'complexity': 'complex'},
        {'description': 'Customer support automation system', 'trigger_type': 'schedule', 'complexity': 'medium'}
    ]
    
    def make_diverse_request(request_type, request_id):
        start_time = time.time()
        response = client.post('/generate',
                              data=json.dumps(request_type),
                              content_type='application/json')
        end_time = time.time()
        
        return {
            'id': request_id,
            'type': request_type['trigger_type'],
            'complexity': request_type['complexity'],
            'success': response.status_code == 200,
            'response_time': end_time - start_time
        }
    
    # Send 25 concurrent requests (5 of each type)
    print("🧪 Sending 25 concurrent diverse requests...")
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        for i in range(25):
            request_type = request_types[i % len(request_types)]
            futures.append(executor.submit(make_diverse_request, request_type, i))
        
        results = [future.result() for future in as_completed(futures)]
    
    # Analyze results by type
    webhook_results = [r for r in results if r['type'] == 'webhook']
    schedule_results = [r for r in results if r['type'] == 'schedule']
    manual_results = [r for r in results if r['type'] == 'manual']
    
    webhook_success = sum(1 for r in webhook_results if r['success'])
    schedule_success = sum(1 for r in schedule_results if r['success'])
    manual_success = sum(1 for r in manual_results if r['success'])
    
    print(f"✅ Webhook requests: {webhook_success}/{len(webhook_results)} successful")
    print(f"✅ Schedule requests: {schedule_success}/{len(schedule_results)} successful")
    print(f"✅ Manual requests: {manual_success}/{len(manual_results)} successful")
    
    total_success = sum(1 for r in results if r['success'])
    success_rate = (total_success / len(results)) * 100
    
    print(f"✅ Overall success rate: {total_success}/{len(results)} ({success_rate:.1f}%)")
    
    return success_rate >= 90

if __name__ == "__main__":
    try:
        print("🚀 STRESS AND RELIABILITY TESTING")
        print("=" * 50)
        
        volume_passed = test_high_volume_requests()
        memory_passed = test_memory_stability()
        recovery_passed = test_error_recovery()
        concurrent_passed = test_concurrent_different_requests()
        
        tests_passed = sum([volume_passed, memory_passed, recovery_passed, concurrent_passed])
        total_tests = 4
        
        success_rate = (tests_passed / total_tests) * 100
        
        print(f"\n🏆 STRESS AND RELIABILITY TEST RESULTS")
        print("=" * 50)
        print(f"📈 High Volume: {'✅ PASS' if volume_passed else '❌ FAIL'}")
        print(f"🧠 Memory Stability: {'✅ PASS' if memory_passed else '❌ FAIL'}")
        print(f"🛡️ Error Recovery: {'✅ PASS' if recovery_passed else '❌ FAIL'}")
        print(f"🔀 Concurrent Diversity: {'✅ PASS' if concurrent_passed else '❌ FAIL'}")
        print(f"\n📊 OVERALL SCORE: {tests_passed}/{total_tests} ({success_rate:.1f}%)")
        
        if success_rate >= 75:
            print("🎉 Stress and reliability tests passed!")
            exit(0)
        else:
            print("⚠️ Some stress tests need attention!")
            exit(1)
            
    except Exception as e:
        print(f"❌ Stress and reliability tests failed: {e}")
        exit(1)