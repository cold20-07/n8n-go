#!/usr/bin/env python3
"""
Verification test for all the fixes applied to the N8N Workflow Generator
"""
import sys
import json
import requests
import threading
import time
from pathlib import Path

def test_rate_limiting_fix():
    """Test that rate limiting has been increased"""
    print("🚦 Testing Rate Limiting Fix...")
    
    try:
        from config import config
        
        # Check that rate limits have been increased
        assert config.RATE_LIMIT_PER_HOUR == 1000, f"Expected 1000, got {config.RATE_LIMIT_PER_HOUR}"
        assert config.RATE_LIMIT_PER_MINUTE == 100, f"Expected 100, got {config.RATE_LIMIT_PER_MINUTE}"
        assert config.GENERATE_RATE_LIMIT == "100 per minute", f"Expected '100 per minute', got {config.GENERATE_RATE_LIMIT}"
        
        print("   ✅ Rate limits increased successfully")
        print(f"   📊 Per hour: {config.RATE_LIMIT_PER_HOUR}")
        print(f"   📊 Per minute: {config.RATE_LIMIT_PER_MINUTE}")
        print(f"   📊 Generate endpoint: {config.GENERATE_RATE_LIMIT}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Rate limiting test failed: {e}")
        return False

def test_validate_endpoint():
    """Test that the /validate endpoint is working"""
    print("🔍 Testing /validate Endpoint...")
    
    try:
        from app import app
        
        # Start test server
        def run_server():
            app.run(port=5002, debug=False, use_reloader=False)
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        time.sleep(2)
        
        # Test the validate endpoint
        test_workflow = {
            "workflow": {
                "nodes": [
                    {
                        "id": "test1",
                        "name": "Test Node",
                        "type": "n8n-nodes-base.webhook",
                        "parameters": {}
                    }
                ],
                "connections": {}
            }
        }
        
        response = requests.post(
            'http://localhost:5002/validate',
            json=test_workflow,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ /validate endpoint working")
            print(f"   📊 Response: {data.get('success', False)}")
            print(f"   📊 Valid: {data.get('valid', False)}")
            return True
        else:
            print(f"   ❌ /validate endpoint failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"   ❌ Validate endpoint test failed: {e}")
        return False

def test_config_api_endpoints():
    """Test that configuration API endpoints are working"""
    print("⚙️ Testing Configuration API Endpoints...")
    
    try:
        from app import app
        
        # Start test server
        def run_server():
            app.run(port=5003, debug=False, use_reloader=False)
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        time.sleep(2)
        
        # Test config status endpoint
        response = requests.get('http://localhost:5003/api/config/status', timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("   ✅ /api/config/status working")
            print(f"   📊 Success: {data.get('success', False)}")
            print(f"   📊 Environment: {data.get('status', {}).get('environment', 'unknown')}")
            return True
        else:
            print(f"   ❌ Config API failed: {response.status_code}")
            print(f"   📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Config API test failed: {e}")
        return False

def test_cli_unicode_fix():
    """Test that CLI tools work without Unicode errors"""
    print("🖥️ Testing CLI Unicode Fix...")
    
    try:
        import subprocess
        
        # Test config CLI status command
        result = subprocess.run(
            [sys.executable, 'config_cli.py', 'status'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=30
        )
        
        if result.returncode == 0:
            print("   ✅ CLI Unicode issues fixed")
            print("   📊 CLI status command works")
            
            # Check that output contains expected content
            if "[INFO] Configuration Status" in result.stdout:
                print("   ✅ CLI output format correct")
                return True
            else:
                print("   ⚠️ CLI output format unexpected")
                return False
        else:
            print(f"   ❌ CLI failed with return code: {result.returncode}")
            print(f"   📄 Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"   ❌ CLI Unicode test failed: {e}")
        return False

def test_workflow_generation_still_works():
    """Test that workflow generation still works after fixes"""
    print("🚀 Testing Workflow Generation Still Works...")
    
    try:
        from src.core.generators.market_leading_workflow_generator import generate_market_leading_workflow
        
        # Generate a test workflow
        workflow = generate_market_leading_workflow(
            "Test workflow for verification",
            "webhook",
            "medium"
        )
        
        # Validate workflow structure
        required_fields = ['id', 'name', 'nodes', 'connections']
        missing_fields = [field for field in required_fields if field not in workflow]
        
        if missing_fields:
            print(f"   ❌ Missing workflow fields: {missing_fields}")
            return False
        
        nodes = workflow.get('nodes', [])
        connections = workflow.get('connections', {})
        
        print("   ✅ Workflow generation working")
        print(f"   📊 Nodes: {len(nodes)}")
        print(f"   📊 Connections: {len(connections)}")
        print(f"   📊 Workflow: {workflow.get('name')}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Workflow generation test failed: {e}")
        return False

def main():
    """Run all verification tests"""
    print("🔧 N8N Workflow Generator - Fixes Verification")
    print("=" * 60)
    
    tests = [
        ("Rate Limiting Fix", test_rate_limiting_fix),
        ("Validate Endpoint", test_validate_endpoint),
        ("Config API Endpoints", test_config_api_endpoints),
        ("CLI Unicode Fix", test_cli_unicode_fix),
        ("Workflow Generation", test_workflow_generation_still_works)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            print()
        except Exception as e:
            print(f"   ❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
            print()
    
    # Summary
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print("=" * 60)
    print(f"📊 Verification Results: {passed}/{total} tests passed")
    print()
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {status} {test_name}")
    
    if passed == total:
        print("\n🎉 All fixes verified successfully!")
        print("✅ The N8N Workflow Generator is ready for production!")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Some issues may remain.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)