#!/usr/bin/env python3
"""
Setup script for N8N Workflow Generator
"""
import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"   stdout: {e.stdout}")
        if e.stderr:
            print(f"   stderr: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def setup_environment():
    """Setup development environment"""
    print("🚀 Setting up N8N Workflow Generator development environment")
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create .env file if it doesn't exist
    if not Path('.env').exists():
        if Path('.env.example').exists():
            print("📝 Creating .env file from .env.example")
            import shutil
            shutil.copy('.env.example', '.env')
            print("⚠️ Please edit .env file with your actual configuration")
        else:
            print("⚠️ No .env.example found, please create .env manually")
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    # Install Node.js dependencies if package.json exists
    if Path('package.json').exists():
        if not run_command("npm install", "Installing Node.js dependencies"):
            print("⚠️ Node.js dependencies failed, but continuing...")
    
    # Create necessary directories
    directories = ['logs', 'tests', 'static/uploads', 'training_data']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # Run cleanup if available
    if Path('cleanup_debug_files.py').exists():
        run_command("python cleanup_debug_files.py", "Cleaning up debug files")
    
    # Validate configuration
    if Path('config.py').exists():
        run_command("python config.py", "Validating configuration")
    
    # Run basic tests
    if Path('tests').exists():
        run_command("python -m pytest tests/ -v --tb=short", "Running basic tests")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Edit .env file with your API keys")
    print("   2. Run: python app.py")
    print("   3. Open: http://localhost:5000")
    
    return True

def setup_production():
    """Setup for production deployment"""
    print("🏭 Setting up for production deployment")
    
    # Check required environment variables
    required_vars = ['SECRET_KEY', 'FLASK_ENV']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    # Install production dependencies
    if not run_command("pip install gunicorn", "Installing production server"):
        return False
    
    # Create production directories
    prod_dirs = ['logs', 'static', 'instance']
    for directory in prod_dirs:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Production setup completed")
    print("   Run with: gunicorn --bind 0.0.0.0:5000 app:app")
    
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "production":
        setup_production()
    else:
        setup_environment()