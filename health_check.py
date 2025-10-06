#!/usr/bin/env python3
"""
Health check for N8N Workflow Generator
"""
import requests
import threading
import time
import sys
from app import app

def run_server():
    """Run the Flask server"""
    app.run(port=5001, debug=False, use_reloader=False)

def main():
    """Run health check"""
    print("🏥 Starting Health Check...")
    
    # Start server in background
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    try:
        # Test health endpoint
        print("🔍 Testing /health endpoint...")
        response = requests.get('http://localhost:5001/health', timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check PASSED")
            print(f"   Status: {data.get('status')}")
            print(f"   Services: {len(data.get('services', {}))}")
            
            # Show service status
            services = data.get('services', {})
            for service, status in services.items():
                status_icon = "✅" if status else "❌"
                print(f"   {status_icon} {service}: {'Available' if status else 'Unavailable'}")
            
            return True
        else:
            print(f"❌ Health check FAILED: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check FAILED: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)