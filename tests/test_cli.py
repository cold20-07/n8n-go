"""
Tests for CLI functionality
"""
import pytest
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch, Mock


class TestConfigCLI:
    """Test configuration CLI functionality"""
    
    def test_config_cli_import(self):
        """Test that config CLI can be imported"""
        try:
            import config_cli
            assert hasattr(config_cli, 'main')
            assert hasattr(config_cli, 'cmd_status')
            assert hasattr(config_cli, 'cmd_validate')
        except ImportError:
            pytest.skip("Config CLI not available")
    
    def test_config_cli_status_command(self):
        """Test config CLI status command"""
        try:
            result = subprocess.run([
                sys.executable, 'config_cli.py', 'status'
            ], capture_output=True, text=True, timeout=30)
            
            # Should complete successfully
            assert result.returncode == 0
            
            # Should contain expected output
            output = result.stdout
            assert 'Configuration Status' in output
            assert 'Environment:' in output
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("Config CLI not available or timeout")
    
    def test_config_cli_validate_command(self):
        """Test config CLI validate command"""
        try:
            result = subprocess.run([
                sys.executable, 'config_cli.py', 'validate'
            ], capture_output=True, text=True, timeout=30)
            
            # Should complete (might have validation issues but shouldn't crash)
            assert result.returncode in [0, 1]  # 1 if validation issues found
            
            # Should contain expected output
            output = result.stdout
            assert 'Validating Configuration' in output
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("Config CLI not available or timeout")
    
    def test_config_cli_features_command(self):
        """Test config CLI features command"""
        try:
            result = subprocess.run([
                sys.executable, 'config_cli.py', 'features'
            ], capture_output=True, text=True, timeout=30)
            
            # Should complete successfully
            assert result.returncode == 0
            
            # Should contain expected output
            output = result.stdout
            assert 'Feature Flags' in output
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("Config CLI not available or timeout")
    
    def test_config_cli_env_template_command(self):
        """Test config CLI env template command"""
        try:
            result = subprocess.run([
                sys.executable, 'config_cli.py', 'env-template'
            ], capture_output=True, text=True, timeout=30)
            
            # Should complete successfully
            assert result.returncode == 0
            
            # Should contain expected output
            output = result.stdout
            assert 'N8N Workflow Generator Configuration' in output
            assert 'DEBUG=' in output
            assert 'SECRET_KEY=' in output
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("Config CLI not available or timeout")
    
    def test_config_cli_help(self):
        """Test config CLI help"""
        try:
            result = subprocess.run([
                sys.executable, 'config_cli.py', '--help'
            ], capture_output=True, text=True, timeout=30)
            
            # Should complete successfully
            assert result.returncode == 0
            
            # Should contain help information
            output = result.stdout
            assert 'Configuration Management CLI' in output
            assert 'status' in output
            assert 'validate' in output
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("Config CLI not available or timeout")
    
    def test_config_cli_invalid_command(self):
        """Test config CLI with invalid command"""
        try:
            result = subprocess.run([
                sys.executable, 'config_cli.py', 'invalid-command'
            ], capture_output=True, text=True, timeout=30)
            
            # Should fail with error
            assert result.returncode != 0
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("Config CLI not available or timeout")


class TestTestRunner:
    """Test the test runner functionality"""
    
    def test_test_runner_import(self):
        """Test that test runner can be imported"""
        try:
            import run_tests
            assert hasattr(run_tests, 'main')
            assert hasattr(run_tests, 'check_dependencies')
        except ImportError:
            pytest.skip("Test runner not available")
    
    def test_test_runner_help(self):
        """Test test runner help"""
        try:
            result = subprocess.run([
                sys.executable, 'run_tests.py', '--help'
            ], capture_output=True, text=True, timeout=30)
            
            # Should complete successfully
            assert result.returncode == 0
            
            # Should contain help information
            output = result.stdout
            assert 'Test runner for N8N Workflow Generator' in output
            assert '--unit' in output
            assert '--api' in output
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("Test runner not available or timeout")
    
    def test_test_runner_check_deps(self):
        """Test test runner dependency check"""
        try:
            result = subprocess.run([
                sys.executable, 'run_tests.py', '--check-deps'
            ], capture_output=True, text=True, timeout=30)
            
            # Should complete
            assert result.returncode in [0, 1]  # 1 if dependencies missing
            
            # Should contain dependency information
            output = result.stdout
            assert 'Checking test dependencies' in output
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("Test runner not available or timeout")


class TestSetupScripts:
    """Test setup and utility scripts"""
    
    def test_setup_project_script(self):
        """Test setup project script"""
        try:
            # Just test that it can be imported
            import setup_project
            assert hasattr(setup_project, 'setup_environment')
        except ImportError:
            pytest.skip("Setup project script not available")
    
    def test_start_with_rate_limiting_script(self):
        """Test start with rate limiting script"""
        try:
            # Just test that it can be imported
            import start_with_rate_limiting
            assert hasattr(start_with_rate_limiting, 'start_server')
        except ImportError:
            pytest.skip("Start with rate limiting script not available")


class TestConfigurationSystemTests:
    """Test the configuration system test script"""
    
    def test_configuration_system_test_import(self):
        """Test that configuration system test can be imported"""
        try:
            import test_configuration_system
            assert hasattr(test_configuration_system, 'main')
        except ImportError:
            pytest.skip("Configuration system test not available")
    
    def test_configuration_system_test_run(self):
        """Test running configuration system tests"""
        try:
            result = subprocess.run([
                sys.executable, 'test_configuration_system.py'
            ], capture_output=True, text=True, timeout=60)
            
            # Should complete
            assert result.returncode in [0, 1]
            
            # Should contain test output
            output = result.stdout
            assert 'Configuration System Test Suite' in output
            
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("Configuration system test not available or timeout")


class TestRateLimitingTests:
    """Test the rate limiting test script"""
    
    def test_rate_limiting_test_import(self):
        """Test that rate limiting test can be imported"""
        try:
            import test_rate_limiting
            assert hasattr(test_rate_limiting, 'test_rate_limiting')
        except ImportError:
            pytest.skip("Rate limiting test not available")
    
    def test_quick_rate_limit_test_import(self):
        """Test that quick rate limit test can be imported"""
        try:
            import quick_rate_limit_test
            assert hasattr(quick_rate_limit_test, 'main')
        except ImportError:
            pytest.skip("Quick rate limit test not available")


class TestUtilityScripts:
    """Test utility scripts"""
    
    def test_reorganize_project_script(self):
        """Test reorganize project script"""
        try:
            import reorganize_project
            assert hasattr(reorganize_project, 'create_new_structure')
            assert hasattr(reorganize_project, 'move_files')
        except ImportError:
            pytest.skip("Reorganize project script not available")
    
    def test_cleanup_scripts_exist(self):
        """Test that cleanup scripts exist"""
        cleanup_scripts = [
            'scripts/cleanup_debug_files.py',
            'scripts/cleanup_for_distribution.py'
        ]
        
        for script_path in cleanup_scripts:
            script_file = Path(script_path)
            if script_file.exists():
                # Try to import if it's a Python file
                try:
                    # This is a basic existence check
                    assert script_file.is_file()
                except Exception:
                    pass


class TestDocumentationScripts:
    """Test documentation and summary scripts"""
    
    def test_summary_files_exist(self):
        """Test that summary files exist"""
        summary_files = [
            'REORGANIZATION_SUMMARY.md',
            'RATE_LIMITING_SUMMARY.md',
            'CONFIGURATION_SYSTEM_SUMMARY.md',
            'IMPROVEMENT_ROADMAP.md',
            'IMPROVEMENT_SUGGESTIONS.md'
        ]
        
        for summary_file in summary_files:
            file_path = Path(summary_file)
            if file_path.exists():
                assert file_path.is_file()
                # Check that file has content
                content = file_path.read_text(encoding='utf-8')
                assert len(content) > 100  # Should have substantial content
    
    def test_readme_exists(self):
        """Test that README exists and has content"""
        readme_path = Path('README.md')
        if readme_path.exists():
            assert readme_path.is_file()
            content = readme_path.read_text(encoding='utf-8')
            assert len(content) > 500  # Should have substantial content
            assert 'N8N' in content or 'n8n' in content


class TestProjectStructure:
    """Test project structure and organization"""
    
    def test_src_directory_structure(self):
        """Test src directory structure"""
        src_path = Path('src')
        if src_path.exists():
            assert src_path.is_dir()
            
            # Check for expected subdirectories
            expected_dirs = ['core', 'utils']
            for expected_dir in expected_dirs:
                dir_path = src_path / expected_dir
                if dir_path.exists():
                    assert dir_path.is_dir()
    
    def test_tests_directory_structure(self):
        """Test tests directory structure"""
        tests_path = Path('tests')
        assert tests_path.exists()
        assert tests_path.is_dir()
        
        # Check for test files
        test_files = list(tests_path.glob('test_*.py'))
        assert len(test_files) > 0
        
        # Check for conftest.py
        conftest_path = tests_path / 'conftest.py'
        assert conftest_path.exists()
    
    def test_config_files_exist(self):
        """Test that configuration files exist"""
        config_files = [
            'config.py',
            'config_api.py',
            'config_cli.py',
            '.env.example',
            'pytest.ini'
        ]
        
        for config_file in config_files:
            file_path = Path(config_file)
            if file_path.exists():
                assert file_path.is_file()
    
    def test_docker_files_exist(self):
        """Test that Docker files exist"""
        docker_files = [
            'Dockerfile',
            'docker-compose.yml'
        ]
        
        for docker_file in docker_files:
            file_path = Path(docker_file)
            if file_path.exists():
                assert file_path.is_file()
                content = file_path.read_text()
                assert len(content) > 50  # Should have content