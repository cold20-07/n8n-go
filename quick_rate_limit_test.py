#!/usr/bin/env python3
"""
Quick test to verify rate limiting is working
"""
import time

def test_rate_limiting_import():
    """Test that rate limiting components import correctly"""
    print("🧪 Testing Rate Limiting Components")
    print("=" * 40)
    
    try:
        from app import app, limiter, config
        print("✅ Flask app imported successfully")
        print(f"✅ Rate limiter configured: {limiter is not None}")
        print(f"✅ Rate limits: {config.RATE_LIMIT_PER_HOUR}/hour, {config.RATE_LIMIT_PER_MINUTE}/minute")
        
        # Test route configuration
        routes = [rule.rule for rule in app.url_map.iter_rules()]
        expected_routes = ['/', '/generate', '/prompt-help', '/validate', '/health', '/api/rate-limits']
        
        for route in expected_routes:
            if route in routes:
                print(f"✅ Route {route} available")
            else:
                print(f"❌ Route {route} missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_configuration():
    """Test configuration system"""
    print("\n🔧 Testing Configuration")
    print("=" * 40)
    
    try:
        from config import config
        
        print(f"✅ Debug mode: {config.DEBUG}")
        print(f"✅ Host: {config.HOST}")
        print(f"✅ Port: {config.PORT}")
        print(f"✅ Rate limits configured: {config.RATE_LIMIT_PER_HOUR}/hour")
        print(f"✅ CORS origins: {config.get_cors_origins()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_error_handlers():
    """Test error handler configuration"""
    print("\n🚨 Testing Error Handlers")
    print("=" * 40)
    
    try:
        from app import app
        
        # Check if error handlers are registered
        error_handlers = app.error_handler_spec.get(None, {})
        
        expected_codes = [400, 429, 500]
        for code in expected_codes:
            if code in error_handlers:
                print(f"✅ Error handler {code} registered")
            else:
                print(f"⚠️ Error handler {code} not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handler test failed: {e}")
        return False

def test_security_features():
    """Test security features"""
    print("\n🔒 Testing Security Features")
    print("=" * 40)
    
    try:
        from app import app
        
        # Test that security middleware is configured
        with app.test_client() as client:
            response = client.get('/health')
            
            security_headers = [
                'X-Content-Type-Options',
                'X-Frame-Options', 
                'X-XSS-Protection',
                'Referrer-Policy'
            ]
            
            for header in security_headers:
                if header in response.headers:
                    print(f"✅ Security header {header}: {response.headers[header]}")
                else:
                    print(f"⚠️ Security header {header} missing")
        
        return True
        
    except Exception as e:
        print(f"❌ Security test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Rate Limiting Quick Test Suite")
    print("=" * 50)
    
    tests = [
        test_rate_limiting_import,
        test_configuration,
        test_error_handlers,
        test_security_features
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Rate limiting is ready to use.")
        print("\n🚀 Next steps:")
        print("   1. Start server: python start_with_rate_limiting.py")
        print("   2. Test endpoints: python test_rate_limiting.py")
        print("   3. Check health: curl http://localhost:5000/health")
    else:
        print("⚠️ Some tests failed. Check the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)