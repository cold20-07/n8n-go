"""
Advanced Configuration Management for N8N Workflow Generator
"""
import os
import json
import yaml
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from pathlib import Path
from enum import Enum
import logging

# Configuration loading utilities
class ConfigSource(Enum):
    """Configuration source types"""
    ENV_FILE = "env_file"
    ENVIRONMENT = "environment"
    CONFIG_FILE = "config_file"
    DEFAULT = "default"

class ConfigManager:
    """Advanced configuration manager with multiple sources and validation"""
    
    def __init__(self):
        self.sources_loaded = []
        self.config_cache = {}
        self.load_order = [
            ConfigSource.DEFAULT,
            ConfigSource.CONFIG_FILE,
            ConfigSource.ENV_FILE,
            ConfigSource.ENVIRONMENT
        ]
    
    def load_from_env_file(self, env_path: Path = None) -> Dict[str, str]:
        """Load configuration from .env file"""
        if env_path is None:
            env_path = Path('.env')
        
        config = {}
        if env_path.exists():
            try:
                from dotenv import load_dotenv
                load_dotenv(env_path)
                self.sources_loaded.append(ConfigSource.ENV_FILE)
                print(f"✅ Loaded configuration from {env_path}")
            except ImportError:
                print("⚠️ python-dotenv not installed, skipping .env file")
        
        return config
    
    def load_from_config_file(self, config_path: Path = None) -> Dict[str, Any]:
        """Load configuration from YAML or JSON config file"""
        if config_path is None:
            # Try multiple config file locations
            possible_paths = [
                Path('config.yaml'),
                Path('config.yml'),
                Path('config.json'),
                Path('config/app.yaml'),
                Path('config/app.yml'),
                Path('config/app.json')
            ]
            config_path = next((p for p in possible_paths if p.exists()), None)
        
        if config_path and config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    if config_path.suffix in ['.yaml', '.yml']:
                        config = yaml.safe_load(f)
                    else:
                        config = json.load(f)
                
                self.sources_loaded.append(ConfigSource.CONFIG_FILE)
                print(f"✅ Loaded configuration from {config_path}")
                return config
            except Exception as e:
                print(f"⚠️ Failed to load config file {config_path}: {e}")
        
        return {}
    
    def get_env_value(self, key: str, default: Any = None, cast_type: type = str) -> Any:
        """Get environment variable with type casting and validation"""
        value = os.getenv(key, default)
        
        if value is None:
            return default
        
        # Type casting
        try:
            if cast_type == bool:
                return str(value).lower() in ('true', '1', 'yes', 'on')
            elif cast_type == int:
                return int(value)
            elif cast_type == float:
                return float(value)
            elif cast_type == list:
                return [item.strip() for item in str(value).split(',') if item.strip()]
            else:
                return cast_type(value)
        except (ValueError, TypeError) as e:
            print(f"⚠️ Failed to cast {key}={value} to {cast_type.__name__}: {e}")
            return default

# Initialize configuration manager
config_manager = ConfigManager()

# Load configuration from all sources
config_manager.load_from_env_file()
config_file_config = config_manager.load_from_config_file()

@dataclass
class Config:
    """Advanced application configuration with validation and multiple sources"""
    
    # Application Settings
    DEBUG: bool = field(default_factory=lambda: config_manager.get_env_value('DEBUG', False, bool))
    SECRET_KEY: str = field(default_factory=lambda: config_manager.get_env_value('SECRET_KEY', 'dev-key-change-in-production'))
    FLASK_ENV: str = field(default_factory=lambda: config_manager.get_env_value('FLASK_ENV', 'development'))
    HOST: str = field(default_factory=lambda: config_manager.get_env_value('HOST', '127.0.0.1'))
    PORT: int = field(default_factory=lambda: config_manager.get_env_value('PORT', 5000, int))
    
    # API Keys
    GEMINI_API_KEY: str = field(default_factory=lambda: config_manager.get_env_value('GEMINI_API_KEY', ''))
    OPENAI_API_KEY: str = field(default_factory=lambda: config_manager.get_env_value('OPENAI_API_KEY', ''))
    CLAUDE_API_KEY: str = field(default_factory=lambda: config_manager.get_env_value('CLAUDE_API_KEY', ''))
    
    # AI Provider Settings
    AI_PROVIDER_PRIORITY: List[str] = field(default_factory=lambda: config_manager.get_env_value('AI_PROVIDER_PRIORITY', ['gemini', 'openai', 'claude'], list))
    AI_COST_THRESHOLD: float = field(default_factory=lambda: config_manager.get_env_value('AI_COST_THRESHOLD', 1.0, float))
    AI_CACHE_ENABLED: bool = field(default_factory=lambda: config_manager.get_env_value('AI_CACHE_ENABLED', True, bool))
    AI_FALLBACK_ENABLED: bool = field(default_factory=lambda: config_manager.get_env_value('AI_FALLBACK_ENABLED', True, bool))
    
    # Workflow Generation Settings
    MAX_WORKFLOW_NODES: int = field(default_factory=lambda: config_manager.get_env_value('MAX_WORKFLOW_NODES', 20, int))
    DEFAULT_COMPLEXITY: str = field(default_factory=lambda: config_manager.get_env_value('DEFAULT_COMPLEXITY', 'medium'))
    ENABLE_AI_GENERATION: bool = field(default_factory=lambda: config_manager.get_env_value('ENABLE_AI_GENERATION', True, bool))
    WORKFLOW_TIMEOUT: int = field(default_factory=lambda: config_manager.get_env_value('WORKFLOW_TIMEOUT', 300, int))
    
    # Rate Limiting - Increased for better testing and production use
    RATE_LIMIT_PER_HOUR: int = field(default_factory=lambda: config_manager.get_env_value('RATE_LIMIT_PER_HOUR', 1000, int))
    RATE_LIMIT_PER_MINUTE: int = field(default_factory=lambda: config_manager.get_env_value('RATE_LIMIT_PER_MINUTE', 100, int))
    GENERATE_RATE_LIMIT: str = field(default_factory=lambda: config_manager.get_env_value('GENERATE_RATE_LIMIT', '100 per minute'))
    PROMPT_HELP_RATE_LIMIT: str = field(default_factory=lambda: config_manager.get_env_value('PROMPT_HELP_RATE_LIMIT', '200 per minute'))
    VALIDATE_RATE_LIMIT: str = field(default_factory=lambda: config_manager.get_env_value('VALIDATE_RATE_LIMIT', '300 per minute'))
    PREVIEW_RATE_LIMIT: str = field(default_factory=lambda: config_manager.get_env_value('PREVIEW_RATE_LIMIT', '500 per minute'))
    
    # Database
    DATABASE_URL: str = field(default_factory=lambda: config_manager.get_env_value('DATABASE_URL', 'sqlite:///workflows.db'))
    DATABASE_POOL_SIZE: int = field(default_factory=lambda: config_manager.get_env_value('DATABASE_POOL_SIZE', 10, int))
    DATABASE_TIMEOUT: int = field(default_factory=lambda: config_manager.get_env_value('DATABASE_TIMEOUT', 30, int))
    
    # Cache Settings
    REDIS_URL: str = field(default_factory=lambda: config_manager.get_env_value('REDIS_URL', 'redis://localhost:6379'))
    CACHE_TIMEOUT: int = field(default_factory=lambda: config_manager.get_env_value('CACHE_TIMEOUT', 3600, int))
    ENABLE_CACHING: bool = field(default_factory=lambda: config_manager.get_env_value('ENABLE_CACHING', True, bool))
    
    # Security
    CORS_ORIGINS: str = field(default_factory=lambda: config_manager.get_env_value('CORS_ORIGINS', 'http://localhost:3000'))
    ENABLE_CSRF: bool = field(default_factory=lambda: config_manager.get_env_value('ENABLE_CSRF', True, bool))
    SESSION_TIMEOUT: int = field(default_factory=lambda: config_manager.get_env_value('SESSION_TIMEOUT', 3600, int))
    TRUSTED_PROXIES: List[str] = field(default_factory=lambda: config_manager.get_env_value('TRUSTED_PROXIES', [], list))
    
    # Monitoring & Logging
    LOG_LEVEL: str = field(default_factory=lambda: config_manager.get_env_value('LOG_LEVEL', 'INFO'))
    ENABLE_METRICS: bool = field(default_factory=lambda: config_manager.get_env_value('ENABLE_METRICS', False, bool))
    METRICS_PORT: int = field(default_factory=lambda: config_manager.get_env_value('METRICS_PORT', 9090, int))
    LOG_FILE: str = field(default_factory=lambda: config_manager.get_env_value('LOG_FILE', 'logs/app.log'))
    
    # Feature Flags
    ENABLE_EXPERIMENTAL_FEATURES: bool = field(default_factory=lambda: config_manager.get_env_value('ENABLE_EXPERIMENTAL_FEATURES', False, bool))
    ENABLE_WORKFLOW_TEMPLATES: bool = field(default_factory=lambda: config_manager.get_env_value('ENABLE_WORKFLOW_TEMPLATES', True, bool))
    ENABLE_BATCH_PROCESSING: bool = field(default_factory=lambda: config_manager.get_env_value('ENABLE_BATCH_PROCESSING', False, bool))
    
    # Performance Settings
    MAX_CONCURRENT_REQUESTS: int = field(default_factory=lambda: config_manager.get_env_value('MAX_CONCURRENT_REQUESTS', 100, int))
    REQUEST_TIMEOUT: int = field(default_factory=lambda: config_manager.get_env_value('REQUEST_TIMEOUT', 30, int))
    WORKER_THREADS: int = field(default_factory=lambda: config_manager.get_env_value('WORKER_THREADS', 4, int))
    
    def get_cors_origins(self) -> List[str]:
        """Get CORS origins as a list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(',') if origin.strip()]
    
    def get_trusted_proxies(self) -> List[str]:
        """Get trusted proxy IPs as a list"""
        if isinstance(self.TRUSTED_PROXIES, str):
            return [ip.strip() for ip in self.TRUSTED_PROXIES.split(',') if ip.strip()]
        return self.TRUSTED_PROXIES
    
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.FLASK_ENV.lower() == 'production'
    
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.FLASK_ENV.lower() == 'development'
    
    def is_testing(self) -> bool:
        """Check if running in testing mode"""
        return self.FLASK_ENV.lower() == 'testing'
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration dictionary"""
        return {
            'url': self.DATABASE_URL,
            'pool_size': self.DATABASE_POOL_SIZE,
            'timeout': self.DATABASE_TIMEOUT,
            'echo': self.DEBUG
        }
    
    def get_redis_config(self) -> Dict[str, Any]:
        """Get Redis configuration dictionary"""
        return {
            'url': self.REDIS_URL,
            'timeout': self.CACHE_TIMEOUT,
            'enabled': self.ENABLE_CACHING
        }
    
    def get_rate_limit_config(self) -> Dict[str, str]:
        """Get rate limiting configuration"""
        return {
            'generate': self.GENERATE_RATE_LIMIT,
            'prompt_help': self.PROMPT_HELP_RATE_LIMIT,
            'validate': self.VALIDATE_RATE_LIMIT,
            'preview': self.PREVIEW_RATE_LIMIT,
            'global_hour': f"{self.RATE_LIMIT_PER_HOUR} per hour",
            'global_minute': f"{self.RATE_LIMIT_PER_MINUTE} per minute"
        }
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get logging configuration"""
        return {
            'level': self.LOG_LEVEL,
            'file': self.LOG_FILE,
            'debug': self.DEBUG
        }
    
    def get_feature_flags(self) -> Dict[str, bool]:
        """Get all feature flags"""
        return {
            'ai_generation': self.ENABLE_AI_GENERATION,
            'caching': self.ENABLE_CACHING,
            'csrf': self.ENABLE_CSRF,
            'metrics': self.ENABLE_METRICS,
            'experimental': self.ENABLE_EXPERIMENTAL_FEATURES,
            'templates': self.ENABLE_WORKFLOW_TEMPLATES,
            'batch_processing': self.ENABLE_BATCH_PROCESSING
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary (excluding sensitive data)"""
        config_dict = {}
        sensitive_keys = ['SECRET_KEY', 'GEMINI_API_KEY', 'OPENAI_API_KEY', 'DATABASE_URL']
        
        for key, value in self.__dict__.items():
            if key not in sensitive_keys:
                config_dict[key] = value
            else:
                config_dict[key] = '***REDACTED***' if value else ''
        
        return config_dict
    
    def validate(self) -> List[str]:
        """Validate configuration and return list of issues"""
        issues = []
        
        # Critical security checks
        if self.SECRET_KEY == 'dev-key-change-in-production' and self.is_production():
            issues.append("CRITICAL: SECRET_KEY must be changed in production")
        
        if len(self.SECRET_KEY) < 32 and self.is_production():
            issues.append("CRITICAL: SECRET_KEY should be at least 32 characters in production")
        
        # API key validation
        if self.ENABLE_AI_GENERATION and not self.GEMINI_API_KEY and not self.OPENAI_API_KEY:
            issues.append("WARNING: AI generation enabled but no API keys provided")
        
        # Workflow settings validation
        if self.MAX_WORKFLOW_NODES < 2:
            issues.append("ERROR: MAX_WORKFLOW_NODES must be at least 2")
        
        if self.MAX_WORKFLOW_NODES > 100:
            issues.append("WARNING: MAX_WORKFLOW_NODES > 100 may cause performance issues")
        
        if self.DEFAULT_COMPLEXITY not in ['simple', 'medium', 'complex']:
            issues.append("ERROR: DEFAULT_COMPLEXITY must be 'simple', 'medium', or 'complex'")
        
        # Rate limiting validation
        if self.RATE_LIMIT_PER_HOUR < 1:
            issues.append("ERROR: RATE_LIMIT_PER_HOUR must be at least 1")
        
        if self.RATE_LIMIT_PER_MINUTE < 1:
            issues.append("ERROR: RATE_LIMIT_PER_MINUTE must be at least 1")
        
        # Performance validation
        if self.MAX_CONCURRENT_REQUESTS > 1000:
            issues.append("WARNING: MAX_CONCURRENT_REQUESTS > 1000 may cause resource exhaustion")
        
        if self.WORKER_THREADS > 20:
            issues.append("WARNING: WORKER_THREADS > 20 may cause context switching overhead")
        
        # Network validation
        if self.PORT < 1024 and not self.is_development():
            issues.append("WARNING: PORT < 1024 requires root privileges")
        
        if self.PORT > 65535:
            issues.append("ERROR: PORT must be between 1 and 65535")
        
        # Timeout validation
        if self.REQUEST_TIMEOUT > 300:
            issues.append("WARNING: REQUEST_TIMEOUT > 300 seconds may cause client timeouts")
        
        if self.WORKFLOW_TIMEOUT > 600:
            issues.append("WARNING: WORKFLOW_TIMEOUT > 600 seconds may cause resource issues")
        
        # Log level validation
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.LOG_LEVEL.upper() not in valid_log_levels:
            issues.append(f"ERROR: LOG_LEVEL must be one of {valid_log_levels}")
        
        return issues
    
    def reload(self):
        """Reload configuration from all sources"""
        global config_manager
        config_manager = ConfigManager()
        config_manager.load_from_env_file()
        config_manager.load_from_config_file()
        
        # Re-initialize all fields
        self.__post_init__()

# Global configuration instance
config = Config()

def validate_config() -> None:
    """Validate configuration and handle issues appropriately"""
    issues = config.validate()
    
    if not issues:
        print("✅ Configuration validation passed")
        return
    
    # Categorize issues
    critical_issues = [issue for issue in issues if issue.startswith('CRITICAL')]
    error_issues = [issue for issue in issues if issue.startswith('ERROR')]
    warning_issues = [issue for issue in issues if issue.startswith('WARNING')]
    
    if critical_issues or error_issues:
        print("❌ Configuration Issues Found:")
        for issue in critical_issues + error_issues:
            print(f"   - {issue}")
        
        if config.is_production():
            print("💥 Critical configuration issues in production mode - exiting")
            exit(1)
        else:
            print("⚠️ Configuration issues detected but continuing in development mode")
    
    if warning_issues:
        print("⚠️ Configuration Warnings:")
        for issue in warning_issues:
            print(f"   - {issue}")

def get_config_summary() -> Dict[str, Any]:
    """Get a summary of current configuration"""
    return {
        'environment': config.FLASK_ENV,
        'debug': config.DEBUG,
        'host': config.HOST,
        'port': config.PORT,
        'features': config.get_feature_flags(),
        'rate_limits': config.get_rate_limit_config(),
        'sources_loaded': config_manager.sources_loaded,
        'validation_status': 'passed' if not config.validate() else 'issues_found'
    }

def reload_config():
    """Reload configuration from all sources"""
    config.reload()
    validate_config()
    print("🔄 Configuration reloaded")

if __name__ == "__main__":
    validate_config()
    summary = get_config_summary()
    print(f"\n📋 Configuration Summary:")
    print(f"   Environment: {summary['environment']}")
    print(f"   Debug: {summary['debug']}")
    print(f"   Host: {summary['host']}:{summary['port']}")
    print(f"   Features: {summary['features']}")
    print(f"   Sources: {summary['sources_loaded']}")
    print(f"   Status: {summary['validation_status']}")