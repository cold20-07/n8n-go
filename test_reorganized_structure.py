#!/usr/bin/env python3
"""
Test script to verify the reorganized project structure works correctly
"""
import sys
import os
from pathlib import Path

def test_imports():
    """Test that all modules can be imported with new structure"""
    print("🧪 Testing reorganized project structure...")
    
    # Test configuration
    try:
        from config import config
        print("✅ Configuration module imported successfully")
    except ImportError as e:
        print(f"❌ Configuration import failed: {e}")
        return False
    
    # Test logging
    try:
        from logger import setup_app_logging
        logger = setup_app_logging(debug=False)
        print("✅ Logging module imported successfully")
    except ImportError as e:
        print(f"❌ Logging import failed: {e}")
        return False
    
    # Test exceptions
    try:
        from exceptions import WorkflowGeneratorError, ValidationError
        print("✅ Exception classes imported successfully")
    except ImportError as e:
        print(f"❌ Exception import failed: {e}")
        return False
    
    # Test core modules
    modules_to_test = [
        ('src.core.validators.enhanced_input_validation', 'Enhanced input validation'),
        ('src.utils.prompt_helper', 'Prompt helper'),
        ('src.core.generators.trained_workflow_generator', 'Trained workflow generator'),
        ('src.core.generators.feature_aware_workflow_generator', 'Feature-aware generator'),
        ('src.core.generators.enhanced_workflow_generator', 'Enhanced workflow generator'),
        ('src.core.validators.simple_connection_fixer', 'Simple connection fixer'),
    ]
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {description} imported successfully")
        except ImportError as e:
            print(f"⚠️ {description} import failed: {e}")
    
    # Test main app
    try:
        import app
        print("✅ Main app imported successfully")
    except ImportError as e:
        print(f"❌ Main app import failed: {e}")
        return False
    
    return True

def test_directory_structure():
    """Test that the directory structure is correct"""
    print("\n📁 Testing directory structure...")
    
    expected_dirs = [
        'src',
        'src/core',
        'src/core/generators',
        'src/core/validators',
        'src/core/models',
        'src/utils',
        'src/api',
        'src/api/routes',
        'tests',
        'tests/unit',
        'tests/integration',
        'scripts',
        'config',
        'docs'
    ]
    
    all_exist = True
    for directory in expected_dirs:
        if Path(directory).exists():
            print(f"✅ {directory}")
        else:
            print(f"❌ {directory} - missing")
            all_exist = False
    
    return all_exist

def test_file_locations():
    """Test that files are in the correct locations"""
    print("\n📄 Testing file locations...")
    
    expected_files = {
        'src/core/generators': [
            'enhanced_workflow_generator.py',
            'feature_aware_workflow_generator.py',
            'trained_workflow_generator.py'
        ],
        'src/core/validators': [
            'connection_validator.py',
            'enhanced_input_validation.py',
            'simple_connection_fixer.py'
        ],
        'src/utils': [
            'prompt_helper.py',
            'prompt_assistance_system.py'
        ],
        'scripts': [
            'cleanup_debug_files.py',
            'regenerate_models.py'
        ]
    }
    
    all_exist = True
    for directory, files in expected_files.items():
        print(f"\n📂 {directory}:")
        for file in files:
            file_path = Path(directory) / file
            if file_path.exists():
                print(f"  ✅ {file}")
            else:
                print(f"  ❌ {file} - missing")
                all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("🚀 Testing N8N Workflow Generator Reorganized Structure\n")
    
    # Test directory structure
    structure_ok = test_directory_structure()
    
    # Test file locations
    files_ok = test_file_locations()
    
    # Test imports
    imports_ok = test_imports()
    
    print("\n" + "="*50)
    print("📊 Test Results:")
    print(f"   Directory Structure: {'✅ PASS' if structure_ok else '❌ FAIL'}")
    print(f"   File Locations: {'✅ PASS' if files_ok else '❌ FAIL'}")
    print(f"   Module Imports: {'✅ PASS' if imports_ok else '❌ FAIL'}")
    
    if structure_ok and files_ok and imports_ok:
        print("\n🎉 All tests passed! Project reorganization successful!")
        return True
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)