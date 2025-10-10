"""
Tests for configuration management system
"""
import pytest
import os
import tempfile
import json
from pathlib import Path
from unittest.mock import patch, Mock

from config import Config, ConfigManager, validate_config, get_config_summary, reload_config


class TestConfigManager:
    """Test ConfigManager functionality"""
    
    def test_config_manager_initialization(self):
        """Test ConfigManager initializes correctly"""
        manager = ConfigManager()
        
        assert manager.sources_loaded == []
        assert manager.config_cache == {}
        assert len(manager.load_order) == 4
    
    def test_get_env_value_string(self):
        """Test getting string environment values"""
        manager = ConfigManager()
        
        # Test with existing environment variable
        os.environ['TEST_STRING'] = 'test_value'
        result = manager.get_env_value('TEST_STRING', 'default')
        assert result == 'test_value'
        
        # Test with default value
        result = manager.get_env_value('NON_EXISTENT', 'default')
        assert result == 'default'
        
        # Cleanup
        if 'TEST_STRING' in os.environ:
            del os.environ['TEST_STRING']
    
    def test_get_env_value_boolean(self):
        """Test getting boolean environment values"""
        manager = ConfigManager()
        
        # Test true values
        for true_val in ['true', 'True', '1', 'yes', 'on']:
            os.environ['TEST_BOOL'] = true_val
            result = manager.get_env_value('TEST_BOOL', False, bool)
            assert result is True
        
        # Test false values
        for false_val in ['false', 'False', '0', 'no', 'off']:
            os.environ['TEST_BOOL'] = false_val
            result = manager.get_env_value('TEST_BOOL', True, bool)
            assert result is False
        
        # Cleanup
        if 'TEST_BOOL' in os.environ:
            del os.environ['TEST_BOOL']
    
    def test_get_env_value_integer(self):
        """Test getting integer environment values"""
        manager = ConfigManager()
        
        # Test valid integer
        os.environ['TEST_INT'] = '42'
        result = manager.get_env_value('TEST_INT', 0, int)
        assert result == 42
        
        # Test invalid integer (should return default)
        os.environ['TEST_INT'] = 'not_a_number'
        result = manager.get_env_value('TEST_INT', 100, int)
        assert result == 100
        
        # Cleanup
        if 'TEST_INT' in os.environ:
            del os.environ['TEST_INT']
    
    def test_get_env_value_list(self):
        """Test getting list environment values"""
        manager = ConfigManager()
        
        # Test comma-separated list
        os.environ['TEST_LIST'] = 'item1,item2,item3'
        result = manager.get_env_value('TEST_LIST', [], list)
        assert result == ['item1', 'item2', 'item3']
        
        # Test list with spaces
        os.environ['TEST_LIST'] = 'item1, item2 , item3'
        result = manager.get_env_value('TEST_LIST', [], list)
        assert result == ['item1', 'item2', 'item3']
        
        # Cleanup
        if 'TEST_LIST' in os.environ:
            del os.environ['TEST_LIST']
    
    def test_load_from_env_file(self, temp_env_file):
        """Test loading configuration from .env file"""
        manager = ConfigManager()
        
        # Mock dotenv availability
        with patch('dotenv.load_dotenv') as mock_load_dotenv:
            result = manager.load_from_env_file(Path(temp_env_file))
            mock_load_dotenv.assert_called_once()
            assert 'env_file' in [source.value for source in manager.sources_loaded]
    
    def test_load_from_config_file(self, temp_config_file):
        """Test loading configuration from JSON file"""
        manager = ConfigManager()
        
        result = manager.load_from_config_file(Path(temp_config_file))
        assert isinstance(result, dict)
        assert 'config_file' in [source.value for source in manager.sources_loaded]


class TestConfig:
    """Test Config class functionality"""
    
    def test_config_initialization(self):
        """Test Config initializes with default values"""
        # Set some test environment variables
        os.environ['TEST_DEBUG'] = 'true'
        os.environ['TEST_SECRET_KEY'] = 'test-secret'
        
        config = Config()
        
        # Test that config has expected attributes
        assert hasattr(config, 'DEBUG')
        assert hasattr(config, 'SECRET_KEY')
        assert hasattr(config, 'FLASK_ENV')
        assert hasattr(config, 'HOST')
        assert hasattr(config, 'PORT')
        
        # Cleanup
        if 'TEST_DEBUG' in os.environ:
            del os.environ['TEST_DEBUG']
        if 'TEST_SECRET_KEY' in os.environ:
            del os.environ['TEST_SECRET_KEY']
    
    def test_get_cors_origins(self):
        """Test CORS origins parsing"""
        config = Config()
        config.CORS_ORIGINS = 'http://localhost:3000,https://example.com,https://app.example.com'
        
        origins = config.get_cors_origins()
        expected = ['http://localhost:3000', 'https://example.com', 'https://app.example.com']
        assert origins == expected
    
    def test_get_trusted_proxies_string(self):
        """Test trusted proxies parsing from string"""
        config = Config()
        config.TRUSTED_PROXIES = '192.168.1.1,10.0.0.1,172.16.0.1'
        
        proxies = config.get_trusted_proxies()
        expected = ['192.168.1.1', '10.0.0.1', '172.16.0.1']
        assert proxies == expected
    
    def test_get_trusted_proxies_list(self):
        """Test trusted proxies parsing from list"""
        config = Config()
        config.TRUSTED_PROXIES = ['192.168.1.1', '10.0.0.1']
        
        proxies = config.get_trusted_proxies()
        assert proxies == ['192.168.1.1', '10.0.0.1']
    
    def test_environment_detection(self):
        """Test environment detection methods"""
        config = Config()
        
        # Test development
        config.FLASK_ENV = 'development'
        assert config.is_development() is True
        assert config.is_production() is False
        assert config.is_testing() is False
        
        # Test production
        config.FLASK_ENV = 'production'
        assert config.is_development() is False
        assert config.is_production() is True
        assert config.is_testing() is False
        
        # Test testing
        config.FLASK_ENV = 'testing'
        assert config.is_development() is False
        assert config.is_production() is False
        assert config.is_testing() is True
    
    def test_get_database_config(self):
        """Test database configuration generation"""
        config = Config()
        config.DATABASE_URL = 'sqlite:///test.db'
        config.DATABASE_POOL_SIZE = 5
        config.DATABASE_TIMEOUT = 30
        config.DEBUG = True
        
        db_config = config.get_database_config()
        
        assert db_config['url'] == 'sqlite:///test.db'
        assert db_config['pool_size'] == 5
        assert db_config['timeout'] == 30
        assert db_config['echo'] is True
    
    def test_get_redis_config(self):
        """Test Redis configuration generation"""
        config = Config()
        config.REDIS_URL = 'redis://localhost:6379'
        config.CACHE_TIMEOUT = 3600
        config.ENABLE_CACHING = True
        
        redis_config = config.get_redis_config()
        
        assert redis_config['url'] == 'redis://localhost:6379'
        assert redis_config['timeout'] == 3600
        assert redis_config['enabled'] is True
    
    def test_get_rate_limit_config(self):
        """Test rate limit configuration generation"""
        config = Config()
        config.GENERATE_RATE_LIMIT = '10 per minute'
        config.PROMPT_HELP_RATE_LIMIT = '20 per minute'
        config.VALIDATE_RATE_LIMIT = '30 per minute'
        config.PREVIEW_RATE_LIMIT = '50 per minute'
        config.RATE_LIMIT_PER_HOUR = 100
        config.RATE_LIMIT_PER_MINUTE = 10
        
        rate_config = config.get_rate_limit_config()
        
        assert rate_config['generate'] == '10 per minute'
        assert rate_config['prompt_help'] == '20 per minute'
        assert rate_config['validate'] == '30 per minute'
        assert rate_config['preview'] == '50 per minute'
        assert rate_config['global_hour'] == '100 per hour'
        assert rate_config['global_minute'] == '10 per minute'
    
    def test_get_feature_flags(self):
        """Test feature flags generation"""
        config = Config()
        config.ENABLE_AI_GENERATION = True
        config.ENABLE_CACHING = True
        config.ENABLE_CSRF = False
        config.ENABLE_METRICS = False
        config.ENABLE_EXPERIMENTAL_FEATURES = False
        config.ENABLE_WORKFLOW_TEMPLATES = True
        config.ENABLE_BATCH_PROCESSING = False
        
        features = config.get_feature_flags()
        
        assert features['ai_generation'] is True
        assert features['caching'] is True
        assert features['csrf'] is False
        assert features['metrics'] is False
        assert features['experimental'] is False
        assert features['templates'] is True
        assert features['batch_processing'] is False
    
    def test_to_dict_redacts_sensitive_data(self):
        """Test that to_dict redacts sensitive information"""
        config = Config()
        config.SECRET_KEY = 'super-secret-key'
        config.GEMINI_API_KEY = 'gemini-api-key'
        config.OPENAI_API_KEY = 'openai-api-key'
        config.DATABASE_URL = 'postgresql://user:pass@localhost/db'
        config.DEBUG = True
        
        config_dict = config.to_dict()
        
        # Sensitive data should be redacted
        assert config_dict['SECRET_KEY'] == '***REDACTED***'
        assert config_dict['GEMINI_API_KEY'] == '***REDACTED***'
        assert config_dict['OPENAI_API_KEY'] == '***REDACTED***'
        assert config_dict['DATABASE_URL'] == '***REDACTED***'
        
        # Non-sensitive data should be preserved
        assert config_dict['DEBUG'] is True


class TestConfigValidation:
    """Test configuration validation"""
    
    def test_validate_production_secret_key(self):
        """Test validation of SECRET_KEY in production"""
        config = Config()
        config.SECRET_KEY = 'dev-key-change-in-production'
        config.FLASK_ENV = 'production'
        
        issues = config.validate()
        
        critical_issues = [issue for issue in issues if issue.startswith('CRITICAL')]
        assert len(critical_issues) > 0
        assert any('SECRET_KEY must be changed' in issue for issue in critical_issues)
    
    def test_validate_secret_key_length(self):
        """Test validation of SECRET_KEY length in production"""
        config = Config()
        config.SECRET_KEY = 'short'  # Less than 32 characters
        config.FLASK_ENV = 'production'
        
        issues = config.validate()
        
        critical_issues = [issue for issue in issues if issue.startswith('CRITICAL')]
        assert any('at least 32 characters' in issue for issue in critical_issues)
    
    def test_validate_api_keys(self):
        """Test validation of API keys when AI generation is enabled"""
        config = Config()
        config.ENABLE_AI_GENERATION = True
        config.GEMINI_API_KEY = ''
        config.OPENAI_API_KEY = ''
        
        issues = config.validate()
        
        warning_issues = [issue for issue in issues if issue.startswith('WARNING')]
        assert any('no API keys provided' in issue for issue in warning_issues)
    
    def test_validate_workflow_nodes(self):
        """Test validation of workflow node limits"""
        config = Config()
        
        # Test minimum nodes
        config.MAX_WORKFLOW_NODES = 1
        issues = config.validate()
        error_issues = [issue for issue in issues if issue.startswith('ERROR')]
        assert any('must be at least 2' in issue for issue in error_issues)
        
        # Test maximum nodes warning
        config.MAX_WORKFLOW_NODES = 150
        issues = config.validate()
        warning_issues = [issue for issue in issues if issue.startswith('WARNING')]
        assert any('may cause performance issues' in issue for issue in warning_issues)
    
    def test_validate_complexity(self):
        """Test validation of default complexity"""
        config = Config()
        config.DEFAULT_COMPLEXITY = 'invalid'
        
        issues = config.validate()
        
        error_issues = [issue for issue in issues if issue.startswith('ERROR')]
        assert any('must be \'simple\', \'medium\', or \'complex\'' in issue for issue in error_issues)
    
    def test_validate_rate_limits(self):
        """Test validation of rate limits"""
        config = Config()
        
        # Test minimum rate limits
        config.RATE_LIMIT_PER_HOUR = 0
        config.RATE_LIMIT_PER_MINUTE = 0
        
        issues = config.validate()
        
        error_issues = [issue for issue in issues if issue.startswith('ERROR')]
        assert any('RATE_LIMIT_PER_HOUR must be at least 1' in issue for issue in error_issues)
        assert any('RATE_LIMIT_PER_MINUTE must be at least 1' in issue for issue in error_issues)
    
    def test_validate_port_range(self):
        """Test validation of port range"""
        config = Config()
        
        # Test port too high
        config.PORT = 70000
        issues = config.validate()
        error_issues = [issue for issue in issues if issue.startswith('ERROR')]
        assert any('must be between 1 and 65535' in issue for issue in error_issues)
    
    def test_validate_log_level(self):
        """Test validation of log level"""
        config = Config()
        config.LOG_LEVEL = 'INVALID'
        
        issues = config.validate()
        
        error_issues = [issue for issue in issues if issue.startswith('ERROR')]
        assert any('LOG_LEVEL must be one of' in issue for issue in error_issues)


class TestConfigFunctions:
    """Test configuration utility functions"""
    
    def test_validate_config_no_issues(self):
        """Test validate_config with no issues"""
        with patch('config.config') as mock_config:
            mock_config.validate.return_value = []
            mock_config.is_production.return_value = False
            
            # Should not raise any exceptions
            validate_config()
    
    def test_validate_config_with_warnings(self):
        """Test validate_config with warnings"""
        with patch('config.config') as mock_config:
            mock_config.validate.return_value = ['WARNING: Test warning']
            mock_config.is_production.return_value = False
            
            # Should not raise any exceptions
            validate_config()
    
    def test_get_config_summary(self):
        """Test get_config_summary function"""
        with patch('config.config') as mock_config:
            mock_config.FLASK_ENV = 'testing'
            mock_config.DEBUG = True
            mock_config.HOST = '127.0.0.1'
            mock_config.PORT = 5000
            mock_config.get_feature_flags.return_value = {'test': True}
            mock_config.get_rate_limit_config.return_value = {'test': '10 per minute'}
            mock_config.validate.return_value = []
            
            with patch('config.config_manager') as mock_manager:
                mock_manager.sources_loaded = ['env_file']
                
                summary = get_config_summary()
                
                assert summary['environment'] == 'testing'
                assert summary['debug'] is True
                assert summary['host'] == '127.0.0.1'
                assert summary['port'] == 5000
                assert summary['features'] == {'test': True}
                assert summary['rate_limits'] == {'test': '10 per minute'}
                assert summary['sources_loaded'] == ['env_file']
                assert summary['validation_status'] == 'passed'
    
    def test_reload_config(self):
        """Test reload_config function"""
        with patch('config.config') as mock_config:
            mock_config.reload = Mock()
            
            with patch('config.validate_config') as mock_validate:
                reload_config()
                
                mock_config.reload.assert_called_once()
                mock_validate.assert_called_once()