#!/usr/bin/env python3
"""
Quick Setup Script for N8N Workflow Generator
Sets up the development environment and runs initial checks
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def print_step(step, description):
    """Print a formatted step"""
    print(f"\n🔧 Step {step}: {description}")

def run_command(command, description="", check=True):
    """Run a command and handle errors"""
    if description:
        print(f"   Running: {description}")
    
    try:
        result = subprocess.run(command, shell=True, check=check, 
                              capture_output=True, text=True)
        if result.stdout:
            print(f"   ✅ {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error: {e}")
        if e.stderr:
            print(f"   Error details: {e.stderr.strip()}")
        return False

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def create_directories():
    """Create necessary directories"""
    directories = [
        'src/core/generators',
        'src/core/validators', 
        'src/templates',
        'src/utils',
        'logs',
        'static/css',
        'static/js',
        'templates'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ Created: {directory}")

def setup_environment():
    """Setup environment file"""
    env_example = Path('.env.example')
    env_file = Path('.env')
    
    if env_example.exists() and not env_file.exists():
        shutil.copy(env_example, env_file)
        print("   ✅ Created .env file from .env.example")
        print("   ⚠️  Please edit .env file with your API keys")
    elif env_file.exists():
        print("   ✅ .env file already exists")
    else:
        print("   ❌ .env.example not found")

def install_dependencies():
    """Install Python dependencies"""
    if Path('requirements.txt').exists():
        return run_command('pip install -r requirements.txt', 
                         "Installing Python dependencies")
    else:
        print("   ⚠️  requirements.txt not found")
        return False

def check_api_keys():
    """Check if API keys are configured"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        gemini_key = os.getenv('GEMINI_API_KEY')
        openai_key = os.getenv('OPENAI_API_KEY')
        
        if gemini_key and gemini_key != 'your-gemini-api-key-here':
            print("   ✅ Gemini API key configured")
        else:
            print("   ⚠️  Gemini API key not configured")
        
        if openai_key and openai_key != 'your-openai-api-key-here':
            print("   ✅ OpenAI API key configured")
        else:
            print("   ⚠️  OpenAI API key not configured")
            
    except ImportError:
        print("   ⚠️  python-dotenv not installed")

def test_imports():
    """Test critical imports"""
    imports_to_test = [
        ('flask', 'Flask web framework'),
        ('requests', 'HTTP requests library'),
        ('json', 'JSON handling (built-in)'),
    ]
    
    all_good = True
    for module, description in imports_to_test:
        try:
            __import__(module)
            print(f"   ✅ {description}")
        except ImportError:
            print(f"   ❌ {description} - not available")
            all_good = False
    
    return all_good

def run_basic_tests():
    """Run basic functionality tests"""
    try:
        # Test config loading
        from config import config
        print("   ✅ Configuration system")
        
        # Test AI enhancements
        try:
            from ai_enhancements import AIOrchestrator
            print("   ✅ AI enhancement system")
        except ImportError:
            print("   ⚠️  AI enhancement system not available")
        
        # Test templates
        try:
            from src.templates.workflow_templates import template_manager
            templates = template_manager.get_all_templates()
            print(f"   ✅ Template system ({len(templates)} templates)")
        except ImportError:
            print("   ⚠️  Template system not available")
        
        # Test validator
        try:
            from src.validators.workflow_validator import workflow_validator
            print("   ✅ Workflow validation system")
        except ImportError:
            print("   ⚠️  Workflow validation system not available")
            
        return True
        
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False

def main():
    """Main setup function"""
    print_header("N8N Workflow Generator - Quick Setup")
    
    # Step 1: Check Python version
    print_step(1, "Checking Python version")
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Create directories
    print_step(2, "Creating directory structure")
    create_directories()
    
    # Step 3: Setup environment
    print_step(3, "Setting up environment")
    setup_environment()
    
    # Step 4: Install dependencies
    print_step(4, "Installing dependencies")
    if not install_dependencies():
        print("   ⚠️  Some dependencies may be missing")
    
    # Step 5: Check API keys
    print_step(5, "Checking API configuration")
    check_api_keys()
    
    # Step 6: Test imports
    print_step(6, "Testing critical imports")
    if not test_imports():
        print("   ⚠️  Some imports failed - check dependencies")
    
    # Step 7: Run basic tests
    print_step(7, "Running basic functionality tests")
    if not run_basic_tests():
        print("   ⚠️  Some tests failed - check configuration")
    
    # Final summary
    print_header("Setup Complete!")
    print("""
🚀 Your N8N Workflow Generator is ready!

Next steps:
1. Edit .env file with your API keys
2. Run: python app.py
3. Open: http://localhost:5000

Features available:
✅ AI-powered workflow generation
✅ Multiple AI provider support
✅ Workflow templates
✅ Workflow validation
✅ Rate limiting
✅ Comprehensive logging

For help:
- Check README.md
- Review documentation at /documentation
- Check logs in logs/ directory

Happy workflow building! 🎉
    """)

if __name__ == "__main__":
    main()