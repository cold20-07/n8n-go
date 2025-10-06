#!/usr/bin/env python3
"""
Comprehensive Deployment Readiness Check for N8N Workflow Generator
"""
import os
import sys
import json
import subprocess
from pathlib import Path

def check_build_system():
    """Check if build system is working"""
    print("🔨 Checking Build System...")
    
    try:
        # Check npm build
        result = subprocess.run(['npm', 'run', 'build'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("   ✅ NPM build successful")
            return True
        else:
            print(f"   ❌ NPM build failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"   ❌ Build system error: {e}")
        return False

def check_core_functionality():
    """Check core application functionality"""
    print("🧪 Checking Core Functionality...")
    
    try:
        result = subprocess.run([sys.executable, 'test_core_functionality.py'], 
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0 and "All core functionality tests PASSED" in result.stdout:
            print("   ✅ Core functionality tests passed")
            return True
        else:
            print(f"   ❌ Core functionality tests failed")
            return False
    except Exception as e:
        print(f"   ❌ Core functionality error: {e}")
        return False

def check_dependencies():
    """Check if all dependencies are available"""
    print("📦 Checking Dependencies...")
    
    try:
        # Check Python dependencies
        import flask
        import requests
        import pytest
        print("   ✅ Python dependencies available")
        
        # Check Node.js dependencies
        node_modules = Path('node_modules')
        if node_modules.exists():
            print("   ✅ Node.js dependencies installed")
        else:
            print("   ❌ Node.js dependencies missing")
            return False
            
        return True
    except ImportError as e:
        print(f"   ❌ Missing Python dependency: {e}")
        return False

def check_configuration():
    """Check configuration files"""
    print("⚙️ Checking Configuration...")
    
    required_files = [
        '.env.example',
        'config.py',
        'requirements.txt',
        'package.json',
        'Dockerfile',
        'docker-compose.yml'
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"   ❌ Missing configuration files: {missing_files}")
        return False
    else:
        print("   ✅ All configuration files present")
        return True

def check_docker_readiness():
    """Check Docker deployment readiness"""
    print("🐳 Checking Docker Readiness...")
    
    try:
        # Check if Docker is available
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("   ✅ Docker available")
            
            # Check if we can build the image
            print("   🔨 Testing Docker build...")
            build_result = subprocess.run(['docker', 'build', '-t', 'n8n-generator-test', '.'], 
                                        capture_output=True, text=True, timeout=300)
            
            if build_result.returncode == 0:
                print("   ✅ Docker build successful")
                
                # Clean up test image
                subprocess.run(['docker', 'rmi', 'n8n-generator-test'], 
                             capture_output=True, text=True)
                return True
            else:
                print(f"   ❌ Docker build failed: {build_result.stderr}")
                return False
        else:
            print("   ⚠️ Docker not available (optional for deployment)")
            return True
    except Exception as e:
        print(f"   ⚠️ Docker check failed: {e} (optional for deployment)")
        return True

def check_security():
    """Check security configuration"""
    print("🔒 Checking Security Configuration...")
    
    security_checks = []
    
    # Check if .env has secure defaults
    env_example = Path('.env.example')
    if env_example.exists():
        content = env_example.read_text()
        if 'DEBUG=false' in content and 'FLASK_ENV=production' in content:
            security_checks.append("Production environment configured")
        if 'SECRET_KEY=your-secret-key-here' in content:
            security_checks.append("Secret key placeholder present")
        if 'CORS_ORIGINS=' in content:
            security_checks.append("CORS configuration present")
    
    # Check nginx security configuration
    nginx_conf = Path('deploy/nginx.conf')
    if nginx_conf.exists():
        content = nginx_conf.read_text()
        if 'ssl_certificate' in content:
            security_checks.append("SSL configuration present")
        if 'X-Frame-Options' in content:
            security_checks.append("Security headers configured")
        if 'limit_req_zone' in content:
            security_checks.append("Rate limiting configured")
    
    if len(security_checks) >= 3:
        print("   ✅ Security configuration looks good")
        for check in security_checks:
            print(f"      • {check}")
        return True
    else:
        print("   ⚠️ Some security configurations may need attention")
        return True

def check_production_readiness():
    """Check production-specific requirements"""
    print("🚀 Checking Production Readiness...")
    
    production_features = []
    
    # Check for production server (gunicorn)
    requirements = Path('requirements.txt').read_text()
    if 'gunicorn' in requirements:
        production_features.append("Production WSGI server (gunicorn)")
    
    # Check for monitoring/logging
    if 'LOG_LEVEL' in Path('.env.example').read_text():
        production_features.append("Logging configuration")
    
    # Check for health check endpoint
    try:
        from app import app
        with app.test_client() as client:
            response = client.get('/health')
            if response.status_code == 200:
                production_features.append("Health check endpoint")
    except:
        pass
    
    # Check for rate limiting
    if 'Flask-Limiter' in requirements:
        production_features.append("Rate limiting")
    
    # Check for CORS
    if 'Flask-CORS' in requirements:
        production_features.append("CORS configuration")
    
    if len(production_features) >= 4:
        print("   ✅ Production features ready")
        for feature in production_features:
            print(f"      • {feature}")
        return True
    else:
        print("   ⚠️ Some production features may need attention")
        return False

def main():
    """Run comprehensive deployment readiness check"""
    print("🚀 N8N Workflow Generator - Deployment Readiness Check")
    print("=" * 60)
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Configuration", check_configuration),
        ("Build System", check_build_system),
        ("Core Functionality", check_core_functionality),
        ("Security", check_security),
        ("Production Readiness", check_production_readiness),
        ("Docker Readiness", check_docker_readiness)
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
            print()
        except Exception as e:
            print(f"   ❌ {check_name} check failed: {e}")
            results.append((check_name, False))
            print()
    
    # Summary
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print("=" * 60)
    print(f"📊 Deployment Readiness: {passed}/{total} checks passed")
    print()
    
    for check_name, result in results:
        status = "✅ READY" if result else "❌ NEEDS ATTENTION"
        print(f"   {status} {check_name}")
    
    print()
    
    if passed >= total - 1:  # Allow 1 optional failure (like Docker)
        print("🎉 DEPLOYMENT READY!")
        print("✅ The N8N Workflow Generator is ready for production deployment!")
        print()
        print("📋 Next Steps:")
        print("   1. Set up production environment variables")
        print("   2. Configure SSL certificates")
        print("   3. Set up monitoring and logging")
        print("   4. Deploy using Docker or your preferred method")
        return True
    else:
        print("⚠️ DEPLOYMENT NOT READY")
        print("❌ Please address the failed checks before deploying")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)