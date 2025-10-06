#!/usr/bin/env python3
"""
Test script to verify rate limiting functionality
"""
import requests
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

def test_rate_limiting():
    """Test rate limiting on various endpoints"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Rate Limiting Implementation")
    print("=" * 50)
    
    # Test data
    test_payload = {
        "description": "Test workflow for rate limiting",
        "trigger": "webhook",
        "complexity": "simple"
    }
    
    # Test endpoints with their limits
    endpoints = [
        {
            'path': '/generate',
            'method': 'POST',
            'data': test_payload,
            'limit': 10,
            'name': 'Workflow Generation'
        },
        {
            'path': '/prompt-help',
            'method': 'POST', 
            'data': {"description": "test"},
            'limit': 20,
            'name': 'Prompt Help'
        },
        {
            'path': '/validate',
            'method': 'POST',
            'data': {"workflow": {"nodes": [], "connections": {}}},
            'limit': 30,
            'name': 'Workflow Validation'
        },
        {
            'path': '/health',
            'method': 'GET',
            'data': None,
            'limit': None,
            'name': 'Health Check'
        }
    ]
    
    for endpoint in endpoints:
        print(f"\n📡 Testing {endpoint['name']} ({endpoint['path']})")
        
        if endpoint['limit'] is None:
            print("   ℹ️ No rate limit - testing basic functionality")
            test_basic_functionality(base_url, endpoint)
        else:
            print(f"   📊 Rate limit: {endpoint['limit']} per minute")
            test_endpoint_rate_limit(base_url, endpoint)
    
    # Test rate limit info endpoint
    print(f"\n📋 Testing Rate Limit Info")
    test_rate_limit_info(base_url)
    
    print(f"\n✅ Rate limiting tests completed!")

def test_basic_functionality(base_url, endpoint):
    """Test basic functionality of an endpoint"""
    try:
        url = f"{base_url}{endpoint['path']}"
        
        if endpoint['method'] == 'GET':
            response = requests.get(url, timeout=5)
        else:
            response = requests.post(url, json=endpoint['data'], timeout=5)
        
        if response.status_code == 200:
            print(f"   ✅ Basic functionality works")
        else:
            print(f"   ⚠️ Response: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request failed: {e}")

def test_endpoint_rate_limit(base_url, endpoint):
    """Test rate limiting for a specific endpoint"""
    url = f"{base_url}{endpoint['path']}"
    limit = endpoint['limit']
    
    # Test normal usage (should work)
    print(f"   🔄 Testing normal usage (5 requests)...")
    success_count = 0
    
    for i in range(5):
        try:
            if endpoint['method'] == 'GET':
                response = requests.get(url, timeout=5)
            else:
                response = requests.post(url, json=endpoint['data'], timeout=5)
            
            if response.status_code == 200:
                success_count += 1
            elif response.status_code == 429:
                print(f"   ⚠️ Rate limited on request {i+1}")
                break
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request {i+1} failed: {e}")
            break
        
        time.sleep(0.1)  # Small delay between requests
    
    print(f"   ✅ {success_count}/5 requests succeeded")
    
    # Test rapid requests (should trigger rate limit)
    print(f"   🚀 Testing rapid requests (should trigger rate limit)...")
    
    def make_request():
        try:
            if endpoint['method'] == 'GET':
                response = requests.get(url, timeout=2)
            else:
                response = requests.post(url, json=endpoint['data'], timeout=2)
            return response.status_code
        except:
            return 0
    
    # Make many concurrent requests
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(make_request) for _ in range(limit + 5)]
        results = [future.result() for future in as_completed(futures)]
    
    success_responses = sum(1 for r in results if r == 200)
    rate_limited = sum(1 for r in results if r == 429)
    
    print(f"   📊 Results: {success_responses} successful, {rate_limited} rate limited")
    
    if rate_limited > 0:
        print(f"   ✅ Rate limiting is working!")
    else:
        print(f"   ⚠️ Rate limiting may not be active")

def test_rate_limit_info(base_url):
    """Test rate limit info endpoint"""
    try:
        response = requests.get(f"{base_url}/api/rate-limits", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Rate limit info available")
            print(f"   📋 Limits: {json.dumps(data.get('rate_limits', {}), indent=6)}")
        else:
            print(f"   ⚠️ Rate limit info not available: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Failed to get rate limit info: {e}")

def check_server_running():
    """Check if the Flask server is running"""
    try:
        response = requests.get("http://localhost:5000/health", timeout=5)
        return response.status_code == 200
    except:
        return False

if __name__ == "__main__":
    print("🚀 Rate Limiting Test Suite")
    print("=" * 50)
    
    if not check_server_running():
        print("❌ Flask server is not running!")
        print("   Please start the server with: python app.py")
        exit(1)
    
    print("✅ Flask server is running")
    test_rate_limiting()