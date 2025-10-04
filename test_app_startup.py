#!/usr/bin/env python3
"""
Test Flask app startup and basic functionality
"""

import sys
import os
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

def test_app_startup():
    """Test that the Flask app starts up correctly"""
    print("🚀 Testing Flask app startup...")
    
    # Create a test server
    server = make_server('127.0.0.1', 5555, app, threaded=True)
    
    # Start server in a separate thread
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    # Give the server time to start
    time.sleep(2)
    
    try:
        # Test the main page
        response = requests.get('http://127.0.0.1:5555/', timeout=10)
        
        if response.status_code == 200:
            print("✅ Flask app starts successfully")
            print("✅ Landing page is accessible")
            
            # Check if the page contains expected content
            if 'N8N Go' in response.text:
                print("✅ Landing page contains correct branding")
            else:
                print("⚠️  Landing page missing expected branding")
                
            if 'workflowForm' in response.text:
                print("✅ Workflow form is present")
            else:
                print("❌ Workflow form is missing")
                return False
                
            return True
        else:
            print(f"❌ Landing page returned status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to connect to Flask app: {e}")
        return False
    finally:
        # Shutdown the server
        server.shutdown()
        
def test_api_endpoint():
    """Test the API endpoint"""
    print("\n🔌 Testing API endpoint...")
    
    # Create a test server
    server = make_server('127.0.0.1', 5556, app, threaded=True)
    
    # Start server in a separate thread
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    # Give the server time to start
    time.sleep(2)
    
    try:
        # Test the generate endpoint
        test_data = {
            'description': 'Create a simple test workflow',
            'triggerType': 'webhook',
            'complexity': 'simple'
        }
        
        response = requests.post(
            'http://127.0.0.1:5556/generate',
            json=test_data,
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Generate endpoint responds successfully")
            
            try:
                data = response.json()
                if data.get('success'):
                    print("✅ Workflow generation works correctly")
                    return True
                else:
                    print(f"❌ Generation failed: {data.get('error')}")
                    return False
            except Exception as e:
                print(f"❌ Failed to parse JSON response: {e}")
                return False
        else:
            print(f"❌ Generate endpoint returned status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to connect to API endpoint: {e}")
        return False
    finally:
        # Shutdown the server
        server.shutdown()

def main():
    """Run startup tests"""
    print("🧪 Testing Flask App Startup and Backend Integration")
    print("=" * 60)
    
    tests = [
        test_app_startup,
        test_api_endpoint
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Startup Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 Flask app and backend are working perfectly with the new landing page!")
        print("\n🚀 You can now run the app with: python app.py")
        return True
    else:
        print("⚠️  Some startup tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)