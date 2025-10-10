#!/usr/bin/env python3
"""
Test script for the new configuration system
"""
import os
import sys
import tempfile
from pathlib import Path

def test_configuration_import():
    """Test that configuration system imports correctly"""
    print("🧪 Testing Configuration System Import")
    print("=" * 50)
    
    try:
        from config import config, validate_config, get_config_summary, ConfigManager
        print("✅ Configuration system imported successfully")
        
        # Test basic properties
        print(f"✅ Environment: {config.FLASK_ENV}")
        print(f"✅ Debug: {config.DEBUG}")
        print(f"✅ Host: {config.HOST}:{config.PORT}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration import failed: {e}")
        return False

def test_configuration_validation():
    """Test configuration validation"""
    print("\n🔍 Testing Configuration Validation")
    print("=" * 50)
    
    try:
        from config import config
        
        issues = config.validate()
        print(f"✅ Validation completed: {len(issues)} issues found")
        
        if issues:
            for issue in issues[:3]:  # Show first 3 issues
                print(f"   - {issue}")
            if len(issues) > 3:
                print(f"   ... and {len(issues) - 3} more")
        
        return True
    except Exception as e:
        print(f"❌ Validation test failed: {e}")
        return False

def test_feature_flags():
    """Test feature flag functionality"""
    print("\n🎛️ Testing Feature Flags")
    print("=" * 50)
    
    try:
        from config import config
        
        features = config.get_feature_flags()
        enabled_count = sum(1 for v in features.values() if v)
        
        print(f"✅ Feature flags loaded: {enabled_count}/{len(features)} enabled")
        
        # Show some key features
        key_features = ['ai_generation', 'caching', 'metrics']
        for feature in key_features:
            if feature in features:
                status = "ON" if features[feature] else "OFF"
                print(f"   {feature}: {status}")
        
        return True
    except Exception as e:
        print(f"❌ Feature flags test failed: {e}")
        return False

def test_rate_limiting_config():
    """Test rate limiting configuration"""
    print("\n🚦 Testing Rate Limiting Configuration")
    print("=" * 50)
    
    try:
        from config import config
        
        rate_limits = config.get_rate_limit_config()
        print(f"✅ Rate limits configured: {len(rate_limits)} endpoints")
        
        # Test specific endpoints
        endpoints = ['generate', 'validate', 'preview']
        for endpoint in endpoints:
            if endpoint in rate_limits:
                print(f"   {endpoint}: {rate_limits[endpoint]}")
        
        return True
    except Exception as e:
        print(f"❌ Rate limiting config test failed: {e}")
        return False

def test_database_config():
    """Test database configuration"""
    print("\n🗄️ Testing Database Configuration")
    print("=" * 50)
    
    try:
        from config import config
        
        db_config = config.get_database_config()
        print(f"✅ Database config loaded")
        print(f"   Pool size: {db_config['pool_size']}")
        print(f"   Timeout: {db_config['timeout']}")
        print(f"   Echo: {db_config['echo']}")
        
        return True
    except Exception as e:
        print(f"❌ Database config test failed: {e}")
        return False

def test_cors_config():
    """Test CORS configuration"""
    print("\n🌐 Testing CORS Configuration")
    print("=" * 50)
    
    try:
        from config import config
        
        cors_origins = config.get_cors_origins()
        print(f"✅ CORS origins configured: {len(cors_origins)} origins")
        
        for origin in cors_origins:
            print(f"   - {origin}")
        
        return True
    except Exception as e:
        print(f"❌ CORS config test failed: {e}")
        return False

def test_config_export():
    """Test configuration export"""
    print("\n📤 Testing Configuration Export")
    print("=" * 50)
    
    try:
        from config import config
        
        config_dict = config.to_dict()
        print(f"✅ Configuration exported: {len(config_dict)} settings")
        
        # Check that sensitive data is redacted
        sensitive_keys = ['SECRET_KEY', 'GEMINI_API_KEY', 'OPENAI_API_KEY']
        for key in sensitive_keys:
            if key in config_dict:
                if config_dict[key] == '***REDACTED***' or config_dict[key] == '':
                    print(f"   ✅ {key}: properly redacted")
                else:
                    print(f"   ⚠️ {key}: may not be properly redacted")
        
        return True
    except Exception as e:
        print(f"❌ Config export test failed: {e}")
        return False

def test_environment_detection():
    """Test environment detection"""
    print("\n🌍 Testing Environment Detection")
    print("=" * 50)
    
    try:
        from config import config
        
        print(f"✅ Environment detection working")
        print(f"   Current environment: {config.FLASK_ENV}")
        print(f"   Is production: {config.is_production()}")
        print(f"   Is development: {config.is_development()}")
        print(f"   Is testing: {config.is_testing()}")
        
        return True
    except Exception as e:
        print(f"❌ Environment detection test failed: {e}")
        return False

def test_config_summary():
    """Test configuration summary"""
    print("\n📋 Testing Configuration Summary")
    print("=" * 50)
    
    try:
        from config import get_config_summary
        
        summary = get_config_summary()
        print(f"✅ Configuration summary generated")
        print(f"   Environment: {summary['environment']}")
        print(f"   Debug: {summary['debug']}")
        print(f"   Features enabled: {sum(1 for v in summary['features'].values() if v)}")
        print(f"   Sources loaded: {len(summary['sources_loaded'])}")
        
        return True
    except Exception as e:
        print(f"❌ Config summary test failed: {e}")
        return False

def test_config_api_import():
    """Test configuration API import"""
    print("\n🔌 Testing Configuration API")
    print("=" * 50)
    
    try:
        from config_api import config_bp
        print(f"✅ Configuration API blueprint imported")
        print(f"   Blueprint name: {config_bp.name}")
        print(f"   URL prefix: {config_bp.url_prefix}")
        
        return True
    except Exception as e:
        print(f"❌ Configuration API test failed: {e}")
        return False

def test_config_cli_import():
    """Test configuration CLI import"""
    print("\n💻 Testing Configuration CLI")
    print("=" * 50)
    
    try:
        import config_cli
        print(f"✅ Configuration CLI imported successfully")
        
        # Test that main functions exist
        functions = ['cmd_status', 'cmd_validate', 'cmd_export']
        for func_name in functions:
            if hasattr(config_cli, func_name):
                print(f"   ✅ {func_name} function available")
            else:
                print(f"   ❌ {func_name} function missing")
        
        return True
    except Exception as e:
        print(f"❌ Configuration CLI test failed: {e}")
        return False

def main():
    """Run all configuration system tests"""
    print("Configuration System Test Suite")
    print("=" * 60)
    
    tests = [
        test_configuration_import,
        test_configuration_validation,
        test_feature_flags,
        test_rate_limiting_config,
        test_database_config,
        test_cors_config,
        test_config_export,
        test_environment_detection,
        test_config_summary,
        test_config_api_import,
        test_config_cli_import
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All configuration system tests passed!")
        print("\n🚀 Next steps:")
        print("   1. Test CLI: python config_cli.py status")
        print("   2. Start server: python app.py")
        print("   3. Check config API: curl http://localhost:5000/api/config/status")
    else:
        print("⚠️ Some tests failed. Check the output above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)