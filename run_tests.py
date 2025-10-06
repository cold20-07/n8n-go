#!/usr/bin/env python3
"""
Test runner for N8N Workflow Generator
"""
import sys
import os
import subprocess
import argparse
from pathlib import Path

def run_command(command, description):
    """Run a command and return success status"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        if e.stdout:
            print(f"stdout: {e.stdout}")
        if e.stderr:
            print(f"stderr: {e.stderr}")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print("📦 Checking test dependencies...")
    
    required_packages = ['pytest', 'flask']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package}")
    
    if missing_packages:
        print(f"\n❌ Missing required packages: {', '.join(missing_packages)}")
        print("Install with: pip install pytest flask")
        return False
    
    return True

def run_unit_tests():
    """Run unit tests"""
    print("\n🧪 Running Unit Tests")
    print("=" * 50)
    
    command = "python -m pytest tests/test_config.py tests/test_workflow_generation.py -v --tb=short"
    return run_command(command, "Unit tests")

def run_api_tests():
    """Run API tests"""
    print("\n🌐 Running API Tests")
    print("=" * 50)
    
    command = "python -m pytest tests/test_app.py tests/test_config_api.py -v --tb=short"
    return run_command(command, "API tests")

def run_rate_limiting_tests():
    """Run rate limiting tests"""
    print("\n🚦 Running Rate Limiting Tests")
    print("=" * 50)
    
    command = "python -m pytest tests/test_rate_limiting.py -v --tb=short"
    return run_command(command, "Rate limiting tests")

def run_integration_tests():
    """Run integration tests"""
    print("\n🔗 Running Integration Tests")
    print("=" * 50)
    
    command = "python -m pytest tests/test_integration.py -v --tb=short"
    return run_command(command, "Integration tests")

def run_all_tests():
    """Run all tests"""
    print("\n🚀 Running All Tests")
    print("=" * 50)
    
    command = "python -m pytest tests/ -v --tb=short"
    return run_command(command, "All tests")

def run_fast_tests():
    """Run fast tests only (excluding slow tests)"""
    print("\n⚡ Running Fast Tests")
    print("=" * 50)
    
    command = 'python -m pytest tests/ -v --tb=short -m "not slow"'
    return run_command(command, "Fast tests")

def run_coverage_tests():
    """Run tests with coverage"""
    print("\n📊 Running Tests with Coverage")
    print("=" * 50)
    
    # Check if pytest-cov is available
    try:
        import pytest_cov
        command = "python -m pytest tests/ --cov=. --cov-report=html --cov-report=term-missing"
        return run_command(command, "Coverage tests")
    except ImportError:
        print("⚠️ pytest-cov not installed. Install with: pip install pytest-cov")
        return run_all_tests()

def run_specific_test(test_path):
    """Run a specific test file or test function"""
    print(f"\n🎯 Running Specific Test: {test_path}")
    print("=" * 50)
    
    command = f"python -m pytest {test_path} -v --tb=short"
    return run_command(command, f"Test: {test_path}")

def generate_test_report():
    """Generate detailed test report"""
    print("\n📋 Generating Test Report")
    print("=" * 50)
    
    command = "python -m pytest tests/ --tb=short --junit-xml=test-results.xml"
    return run_command(command, "Test report generation")

def main():
    """Main test runner"""
    parser = argparse.ArgumentParser(description="Test runner for N8N Workflow Generator")
    parser.add_argument('--unit', action='store_true', help='Run unit tests only')
    parser.add_argument('--api', action='store_true', help='Run API tests only')
    parser.add_argument('--rate-limit', action='store_true', help='Run rate limiting tests only')
    parser.add_argument('--integration', action='store_true', help='Run integration tests only')
    parser.add_argument('--fast', action='store_true', help='Run fast tests only (exclude slow tests)')
    parser.add_argument('--coverage', action='store_true', help='Run tests with coverage')
    parser.add_argument('--report', action='store_true', help='Generate test report')
    parser.add_argument('--test', type=str, help='Run specific test file or function')
    parser.add_argument('--check-deps', action='store_true', help='Check dependencies only')
    
    args = parser.parse_args()
    
    print("🧪 N8N Workflow Generator Test Suite")
    print("=" * 60)
    
    # Check dependencies first
    if not check_dependencies():
        sys.exit(1)
    
    if args.check_deps:
        print("✅ All dependencies are available")
        return
    
    # Set test environment
    os.environ['FLASK_ENV'] = 'testing'
    os.environ['DEBUG'] = 'true'
    
    success = True
    
    try:
        if args.unit:
            success = run_unit_tests()
        elif args.api:
            success = run_api_tests()
        elif args.rate_limit:
            success = run_rate_limiting_tests()
        elif args.integration:
            success = run_integration_tests()
        elif args.fast:
            success = run_fast_tests()
        elif args.coverage:
            success = run_coverage_tests()
        elif args.report:
            success = generate_test_report()
        elif args.test:
            success = run_specific_test(args.test)
        else:
            success = run_all_tests()
        
        if args.report and success:
            generate_test_report()
        
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        success = False
    except Exception as e:
        print(f"\n❌ Test runner error: {e}")
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests completed successfully!")
        print("\n📋 Next steps:")
        print("   - Review test results above")
        print("   - Check coverage report (if generated)")
        print("   - Fix any failing tests")
    else:
        print("❌ Some tests failed or encountered errors")
        print("\n🔧 Troubleshooting:")
        print("   - Check error messages above")
        print("   - Ensure all dependencies are installed")
        print("   - Verify configuration is correct")
        print("   - Run specific test categories to isolate issues")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()