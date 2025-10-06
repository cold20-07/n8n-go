#!/usr/bin/env python3
"""
Start the Flask server with rate limiting enabled
"""
import os
import sys
from pathlib import Path

def setup_environment():
    """Setup environment for rate limiting"""
    
    # Create .env file if it doesn't exist
    if not Path('.env').exists():
        if Path('.env.example').exists():
            print("📝 Creating .env file from .env.example...")
            import shutil
            shutil.copy('.env.example', '.env')
            print("✅ .env file created")
        else:
            print("⚠️ No .env.example found")
    
    # Set default environment variables for rate limiting
    os.environ.setdefault('RATE_LIMIT_PER_HOUR', '100')
    os.environ.setdefault('RATE_LIMIT_PER_MINUTE', '10')
    os.environ.setdefault('FLASK_ENV', 'development')
    os.environ.setdefault('DEBUG', 'true')

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['flask', 'flask-limiter', 'flask-cors']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("   Install with: pip install -r requirements.txt")
        return False
    
    return True

def start_server():
    """Start the Flask server"""
    try:
        from app import app, config, logger
        
        print("🚀 Starting N8N Workflow Generator with Rate Limiting")
        print("=" * 60)
        print(f"📊 Rate Limits:")
        print(f"   Global: {config.RATE_LIMIT_PER_HOUR} requests per hour")
        print(f"   Generate: {config.RATE_LIMIT_PER_MINUTE} requests per minute")
        print(f"   Prompt Help: 20 requests per minute")
        print(f"   Validate: 30 requests per minute")
        print(f"   Preview: 50 requests per minute")
        print("=" * 60)
        print(f"🌐 Server starting on http://{config.HOST}:{config.PORT}")
        print("📋 Available endpoints:")
        print("   GET  /                 - Main interface")
        print("   POST /generate         - Generate workflow")
        print("   POST /prompt-help      - Get prompt assistance")
        print("   POST /validate         - Validate workflow")
        print("   POST /preview          - Generate preview")
        print("   GET  /health           - Health check")
        print("   GET  /api/rate-limits  - Rate limit info")
        print("   GET  /api/rate-limit-stats - Rate limit statistics")
        print("=" * 60)
        print("🧪 Test rate limiting with: python test_rate_limiting.py")
        print("=" * 60)
        
        # Start the server
        app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG,
            threaded=True
        )
        
    except ImportError as e:
        print(f"❌ Failed to import app: {e}")
        print("   Make sure all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Setting up environment...")
    setup_environment()
    
    print("📦 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print("✅ All dependencies available")
    
    # Start the server
    start_server()