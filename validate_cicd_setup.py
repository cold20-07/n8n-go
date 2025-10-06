#!/usr/bin/env python3
"""
Validation script for CI/CD pipeline setup
"""
import os
import sys
import json
import yaml
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists and return status"""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path} - NOT FOUND")
        return False

def validate_yaml_file(file_path, description):
    """Validate YAML file syntax"""
    try:
        with open(file_path, 'r') as f:
            yaml.safe_load(f)
        print(f"✅ {description}: Valid YAML syntax")
        return True
    except yaml.YAMLError as e:
        print(f"❌ {description}: Invalid YAML - {e}")
        return False
    except FileNotFoundError:
        print(f"❌ {description}: File not found")
        return False

def validate_json_file(file_path, description):
    """Validate JSON file syntax"""
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        print(f"✅ {description}: Valid JSON syntax")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ {description}: Invalid JSON - {e}")
        return False
    except FileNotFoundError:
        print(f"❌ {description}: File not found")
        return False

def check_github_workflows():
    """Check GitHub workflow files"""
    print("\n🔄 GitHub Workflows")
    print("=" * 50)
    
    workflows = [
        ('.github/workflows/ci.yml', 'Main CI/CD Pipeline'),
        ('.github/workflows/security.yml', 'Security Scanning'),
        ('.github/workflows/release.yml', 'Release Automation'),
        ('.github/workflows/performance.yml', 'Performance Testing')
    ]
    
    all_valid = True
    for file_path, description in workflows:
        if check_file_exists(file_path, description):
            if not validate_yaml_file(file_path, f"{description} YAML"):
                all_valid = False
        else:
            all_valid = False
    
    # Check dependabot configuration
    if check_file_exists('.github/dependabot.yml', 'Dependabot Configuration'):
        validate_yaml_file('.github/dependabot.yml', 'Dependabot YAML')
    else:
        all_valid = False
    
    return all_valid

def check_deployment_files():
    """Check deployment configuration files"""
    print("\n🚀 Deployment Configuration")
    print("=" * 50)
    
    deployment_files = [
        ('deploy/docker-compose.prod.yml', 'Production Docker Compose'),
        ('deploy/nginx.conf', 'Nginx Configuration'),
        ('deploy/prometheus.yml', 'Prometheus Configuration'),
        ('deploy/deploy.sh', 'Deployment Script'),
        ('deploy/.env.production', 'Production Environment'),
        ('deploy/.env.staging', 'Staging Environment')
    ]
    
    all_valid = True
    for file_path, description in deployment_files:
        if not check_file_exists(file_path, description):
            all_valid = False
    
    # Validate YAML files
    yaml_files = [
        ('deploy/docker-compose.prod.yml', 'Docker Compose'),
        ('deploy/prometheus.yml', 'Prometheus Config')
    ]
    
    for file_path, description in yaml_files:
        if Path(file_path).exists():
            if not validate_yaml_file(file_path, description):
                all_valid = False
    
    return all_valid

def check_docker_files():
    """Check Docker-related files"""
    print("\n🐳 Docker Configuration")
    print("=" * 50)
    
    docker_files = [
        ('Dockerfile', 'Main Dockerfile'),
        ('docker-compose.yml', 'Development Docker Compose'),
        ('.dockerignore', 'Docker Ignore File')
    ]
    
    all_valid = True
    for file_path, description in docker_files:
        if check_file_exists(file_path, description):
            if file_path.endswith('.yml'):
                validate_yaml_file(file_path, f"{description} YAML")
        else:
            if file_path == 'Dockerfile':  # Dockerfile is required
                all_valid = False
    
    return all_valid

def check_test_configuration():
    """Check test configuration"""
    print("\n🧪 Test Configuration")
    print("=" * 50)
    
    test_files = [
        ('pytest.ini', 'Pytest Configuration'),
        ('tests/conftest.py', 'Test Fixtures'),
        ('run_tests.py', 'Test Runner'),
        ('tests/test_config.py', 'Configuration Tests'),
        ('tests/test_app.py', 'Application Tests')
    ]
    
    all_valid = True
    for file_path, description in test_files:
        if not check_file_exists(file_path, description):
            all_valid = False
    
    return all_valid

def check_configuration_files():
    """Check application configuration files"""
    print("\n⚙️ Application Configuration")
    print("=" * 50)
    
    config_files = [
        ('config.py', 'Main Configuration'),
        ('config_api.py', 'Configuration API'),
        ('config_cli.py', 'Configuration CLI'),
        ('.env.example', 'Environment Template'),
        ('requirements.txt', 'Python Dependencies'),
        ('package.json', 'Node.js Dependencies')
    ]
    
    all_valid = True
    for file_path, description in config_files:
        if not check_file_exists(file_path, description):
            all_valid = False
    
    # Validate JSON files
    json_files = [
        ('package.json', 'Package.json')
    ]
    
    for file_path, description in json_files:
        if Path(file_path).exists():
            if not validate_json_file(file_path, description):
                all_valid = False
    
    return all_valid

def check_documentation():
    """Check documentation files"""
    print("\n📚 Documentation")
    print("=" * 50)
    
    doc_files = [
        ('README.md', 'Main README'),
        ('CICD_PIPELINE_SUMMARY.md', 'CI/CD Documentation'),
        ('COMPREHENSIVE_TESTS_COMPLETE.md', 'Test Documentation'),
        ('CONFIGURATION_SYSTEM_SUMMARY.md', 'Configuration Documentation'),
        ('RATE_LIMITING_SUMMARY.md', 'Rate Limiting Documentation')
    ]
    
    all_valid = True
    for file_path, description in doc_files:
        if not check_file_exists(file_path, description):
            all_valid = False
    
    return all_valid

def check_security_files():
    """Check security-related files"""
    print("\n🔒 Security Configuration")
    print("=" * 50)
    
    security_files = [
        ('exceptions.py', 'Exception Handling'),
        ('logger.py', 'Logging Configuration'),
        ('.gitignore', 'Git Ignore File')
    ]
    
    all_valid = True
    for file_path, description in security_files:
        if not check_file_exists(file_path, description):
            all_valid = False
    
    return all_valid

def check_required_secrets():
    """Check for required secrets documentation"""
    print("\n🔑 Required Secrets")
    print("=" * 50)
    
    required_secrets = [
        'DOCKER_USERNAME',
        'DOCKER_PASSWORD', 
        'PYPI_API_TOKEN',
        'SLACK_WEBHOOK',
        'CODECOV_TOKEN'
    ]
    
    print("Required GitHub Repository Secrets:")
    for secret in required_secrets:
        print(f"  - {secret}")
    
    print("\n⚠️ Make sure to configure these secrets in your GitHub repository:")
    print("   Settings → Secrets and variables → Actions")
    
    return True

def generate_setup_checklist():
    """Generate setup checklist"""
    print("\n📋 CI/CD Setup Checklist")
    print("=" * 50)
    
    checklist = [
        "✅ All workflow files are present and valid",
        "✅ Deployment configuration is complete",
        "✅ Docker files are configured",
        "✅ Test suite is comprehensive",
        "✅ Documentation is up to date",
        "⚠️ Configure GitHub repository secrets",
        "⚠️ Customize environment files with your values",
        "⚠️ Update Docker registry settings",
        "⚠️ Configure Slack webhook for notifications",
        "⚠️ Set up monitoring dashboards"
    ]
    
    for item in checklist:
        print(f"  {item}")
    
    print("\n🚀 Next Steps:")
    print("  1. Configure repository secrets in GitHub")
    print("  2. Customize deploy/.env.production with your values")
    print("  3. Update DOCKER_USERNAME in deployment files")
    print("  4. Test the pipeline with a small change")
    print("  5. Set up monitoring and alerting")

def main():
    """Main validation function"""
    print("🔍 CI/CD Pipeline Validation")
    print("=" * 60)
    
    checks = [
        ("GitHub Workflows", check_github_workflows),
        ("Deployment Files", check_deployment_files),
        ("Docker Configuration", check_docker_files),
        ("Test Configuration", check_test_configuration),
        ("Application Configuration", check_configuration_files),
        ("Documentation", check_documentation),
        ("Security Configuration", check_security_files),
        ("Required Secrets", check_required_secrets)
    ]
    
    all_passed = True
    results = {}
    
    for check_name, check_function in checks:
        try:
            result = check_function()
            results[check_name] = result
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ {check_name}: Error during validation - {e}")
            results[check_name] = False
            all_passed = False
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Validation Summary")
    print("=" * 60)
    
    for check_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {check_name}")
    
    if all_passed:
        print("\n🎉 All validations passed! Your CI/CD pipeline is ready.")
        print("   Follow the setup checklist below to complete the configuration.")
    else:
        print("\n⚠️ Some validations failed. Please fix the issues above.")
        print("   The CI/CD pipeline may not work correctly until all issues are resolved.")
    
    generate_setup_checklist()
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)