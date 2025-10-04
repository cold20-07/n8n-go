#!/usr/bin/env python3
"""Performance Testing for N8n JSON Generator"""

import time
import json
import sys
import os
from concurrent.futures import ThreadPoolExecutor

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def test_response_times():
    """Test response times for different workflow complexities"""
    print("🚀 Testing Response Times")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    test_cases = [
        ("Simple workflow", "Create a basic webhook to email workflow"),
        ("Medium workflow", "Build a lead processing system with CRM integration and email notifications"),
        ("Complex workflow", "Design a comprehensive e-commerce order processing system with payment validation, inventory checks, customer notifications, and analytics tracking")
    ]
    
    for name, description in test_cases:
        start_time = time.time()
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': description,
                                  'trigger_type': 'webhook'
                              }),
                              content_type='application/json')
        end_time = time.time()
        
        response_time = end_time - start_time
        print(f"✅ {name}: {response_time:.3f}s")
        
        if response.status_code == 200:
            data = json.loads(response.data)
            print(f"   Nodes: {len(data.get('nodes', []))}")
        
    print()

def test_concurrent_load():
    """Test concurrent request handling"""
    print("🔄 Testing Concurrent Load")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    def make_request(i):
        start_time = time.time()
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': f'Create workflow {i} for data processing',
                                  'trigger_type': 'webhook'
                              }),
                              content_type='application/json')
        end_time = time.time()
        return {
            'id': i,
            'time': end_time - start_time,
            'success': response.status_code == 200
        }
    
    # Test with 5 concurrent requests
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request, i) for i in range(5)]
        results = [f.result() for f in futures]
    
    successful = sum(1 for r in results if r['success'])
    avg_time = sum(r['time'] for r in results) / len(results)
    
    print(f"✅ Concurrent requests: {successful}/5 successful")
    print(f"✅ Average response time: {avg_time:.3f}s")
    print()

if __name__ == "__main__":
    try:
        test_response_times()
        test_concurrent_load()
        print("🎉 Performance tests completed!")
        exit(0)  # Success
    except Exception as e:
        print(f"❌ Performance tests failed: {e}")
        exit(1)  # Failure