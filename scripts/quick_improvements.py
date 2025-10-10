#!/usr/bin/env python3
"""
Quick Improvements Implementation
Implements the most impactful improvements that can be done immediately
"""

import os
import shutil
from pathlib import Path

def implement_quick_improvements():
    """Implement immediate improvements to project structure"""
    
    print("🚀 Implementing quick improvements...")
    
    # 1. Create better project structure
    directories = [
        "src/core/generators",
        "src/core/validators", 
        "src/core/utils",
        "src/api/routes",
        "src/config",
        "tests/unit",
        "tests/integration",
        "docs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # 2. Move files to better locations
    file_moves = [
        # Generators
        ("trained_workflow_generator.py", "src/core/generators/"),
        ("enhanced_workflow_generator.py", "src/core/generators/"),
        ("feature_aware_workflow_generator.py", "src/core/generators/"),
        
        # Validators
        ("connection_validator.py", "src/core/validators/"),
        ("workflow_accuracy_validator.py", "src/core/validators/"),
        ("enhanced_input_validation.py", "src/core/validators/"),
        
        # Utils
        ("prompt_helper.py", "src/core/utils/"),
        ("enhance_workflow_output.py", "src/core/utils/"),
        
        # Tests
        ("test_app_startup.py", "tests/unit/"),
        ("test_workflow_generation.py", "tests/unit/"),
        ("test_final_system.py", "tests/integration/"),
    ]
    
    for source, dest_dir in file_moves:
        if Path(source).exists():
            dest_path = Path(dest_dir) / source
            shutil.move(source, dest_path)
            print(f"📦 Moved {source} → {dest_path}")
    
    # 3. Create configuration file
    create_config_file()
    
    # 4. Create improved requirements files
    create_requirements_files()
    
    # 5. Create basic test configuration
    create_test_config()
    
    # 6. Create development scripts
    create_dev_scripts()
    
    print("✅ Quick improvements implemented!")
    print("\n📋 Next steps:")
    print("   1. Update import statements in moved files")
    print("   2. Run: python -m pytest tests/")
    print("   3. Run: python scripts/dev_server.py")

def create_config_file():
    """Create configuration management"""
    config_content = '''"""
Configuration management for n8n workflow generator
"""
import os
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    """Application configuration"""
    
    # Flask settings
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    HOST: str = os.getenv('HOST', '127.0.0.1')
    PORT: int = int(os.getenv('PORT', '5000'))
    
    # API settings
    GEMINI_API_KEY: Optional[str] = os.getenv('GEMINI_API_KEY')
    MAX_WORKFLOW_NODES: int = int(os.getenv('MAX_WORKFLOW_NODES', '20'))
    REQUEST_TIMEOUT: int = int(os.getenv('REQUEST_TIMEOUT', '30'))
    
    # Rate limiting
    RATE_LIMIT: str = os.getenv('RATE_LIMIT', '100/hour')
    RATE_LIMIT_PER_MINUTE: str = os.getenv('RATE_LIMIT_PER_MINUTE', '10/minute')
    
    # Caching
    CACHE_TYPE: str = os.getenv('CACHE_TYPE', 'simple')
    CACHE_DEFAULT_TIMEOUT: int = int(os.getenv('CACHE_DEFAULT_TIMEOUT', '300'))
    
    # Logging
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE: Optional[str] = os.getenv('LOG_FILE')
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Create config from environment variables"""
        return cls()

# Global config instance
config = Config.from_env()
'''
    
    Path("src/config/settings.py").write_text(config_content)
    Path("src/config/__init__.py").write_text("")
    print("⚙️ Created configuration system")

def create_requirements_files():
    """Create improved requirements files"""
    
    # Production requirements
    prod_requirements = '''# Production dependencies
Flask==2.3.3
Werkzeug==2.3.7
Jinja2==3.1.2
requests==2.31.0
python-dotenv==1.0.0
gunicorn==21.2.0

# Validation and serialization
pydantic==2.4.2

# Caching and rate limiting
Flask-Caching==2.1.0
Flask-Limiter==3.5.0

# Security
Flask-CORS==4.0.0

# Monitoring
psutil==5.9.6
'''
    
    # Development requirements
    dev_requirements = '''# Development dependencies
-r requirements.txt

# Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-mock==3.12.0

# Code quality
black==23.9.1
isort==5.12.0
flake8==6.1.0
mypy==1.6.1

# Documentation
sphinx==7.2.6
sphinx-rtd-theme==1.3.0

# Development tools
watchdog==3.0.0
'''
    
    Path("requirements.txt").write_text(prod_requirements)
    Path("requirements-dev.txt").write_text(dev_requirements)
    print("📦 Created improved requirements files")

def create_test_config():
    """Create test configuration"""
    
    # pytest configuration
    pytest_ini = '''[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --tb=short
    --cov=src
    --cov-report=html
    --cov-report=term-missing
'''
    
    # Test fixtures
    conftest_content = '''"""
Test configuration and fixtures
"""
import pytest
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

@pytest.fixture
def app():
    """Create test Flask app"""
    from app import app
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def sample_workflow_request():
    """Sample workflow request for testing"""
    return {
        "description": "Send email notification when webhook is received",
        "trigger": "webhook",
        "complexity": "simple"
    }
'''
    
    Path("pytest.ini").write_text(pytest_ini)
    Path("tests/conftest.py").write_text(conftest_content)
    Path("tests/__init__.py").write_text("")
    Path("tests/unit/__init__.py").write_text("")
    Path("tests/integration/__init__.py").write_text("")
    print("🧪 Created test configuration")

def create_dev_scripts():
    """Create development scripts"""
    
    # Development server script
    dev_server = '''#!/usr/bin/env python3
"""
Development server with auto-reload and debugging
"""
import os
import sys
from pathlib import Path

# Add src to Python path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app
from src.config.settings import config

if __name__ == "__main__":
    print("🚀 Starting development server...")
    print(f"📍 Running on http://{config.HOST}:{config.PORT}")
    print("🔄 Auto-reload enabled")
    print("🐛 Debug mode enabled")
    
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=True,
        use_reloader=True
    )
'''
    
    # Setup script
    setup_script = '''#!/usr/bin/env python3
"""
Development environment setup script
"""
import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False

def setup_development():
    """Setup development environment"""
    print("🚀 Setting up development environment...")
    
    # Install dependencies
    if not run_command("pip install -r requirements-dev.txt", "Installing dependencies"):
        return False
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        env_content = """DEBUG=true
SECRET_KEY=dev-secret-key
GEMINI_API_KEY=your-api-key-here
LOG_LEVEL=DEBUG
"""
        env_file.write_text(env_content)
        print("📝 Created .env file")
    
    # Run tests
    if not run_command("python -m pytest tests/ -v", "Running tests"):
        print("⚠️ Some tests failed, but setup continues")
    
    # Check code quality
    run_command("black --check .", "Checking code formatting")
    run_command("isort --check-only .", "Checking import sorting")
    
    print("\\n✅ Development environment ready!")
    print("\\n📋 Next steps:")
    print("   1. Update GEMINI_API_KEY in .env file")
    print("   2. Run: python scripts/dev_server.py")
    print("   3. Visit: http://localhost:5000")

if __name__ == "__main__":
    setup_development()
'''
    
    # Create scripts directory
    Path("scripts").mkdir(exist_ok=True)
    Path("scripts/dev_server.py").write_text(dev_server)
    Path("scripts/setup_dev.py").write_text(setup_script)
    
    # Make scripts executable on Unix systems
    if os.name != 'nt':
        os.chmod("scripts/dev_server.py", 0o755)
        os.chmod("scripts/setup_dev.py", 0o755)
    
    print("🛠️ Created development scripts")

if __name__ == "__main__":
    implement_quick_improvements()