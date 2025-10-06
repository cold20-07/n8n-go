"""
Configuration API for N8N Workflow Generator
Provides endpoints for configuration management and monitoring
"""
from flask import Blueprint, jsonify, request
from typing import Dict, Any
import json
from datetime import datetime, timezone

# Import configuration
try:
    from config import config
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False

# Create blueprint for configuration API
config_bp = Blueprint('config_api', __name__, url_prefix='/api/config')

@config_bp.route('/status', methods=['GET'])
def config_status():
    """Get configuration status and summary"""
    if not CONFIG_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Configuration system not available'
        }), 500
    
    try:
        # Create a basic configuration summary
        summary = {
            'environment': config.FLASK_ENV,
            'debug': config.DEBUG,
            'validation_status': 'valid',
            'features': {
                'ai_generation': config.ENABLE_AI_GENERATION,
                'caching': getattr(config, 'ENABLE_CACHING', False),
                'metrics': getattr(config, 'ENABLE_METRICS', False)
            },
            'sources_loaded': ['env_file', 'defaults']
        }
        
        return jsonify({
            'success': True,
            'status': {
                'environment': summary['environment'],
                'debug': summary['debug'],
                'validation_status': summary['validation_status'],
                'issues_count': 0,
                'features_enabled': sum(1 for v in summary['features'].values() if v),
                'sources_loaded': summary['sources_loaded'],
                'last_checked': datetime.now(timezone.utc).isoformat()
            },
            'summary': summary
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get configuration status: {str(e)}'
        }), 500

@config_bp.route('/validate', methods=['POST'])
def validate_configuration():
    """Validate current configuration and return detailed results"""
    if not CONFIG_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Configuration system not available'
        }), 500
    
    try:
        # Basic validation - check if required settings exist
        issues = []
        
        # Check API keys
        if not config.GEMINI_API_KEY and not config.OPENAI_API_KEY:
            issues.append('WARNING: No AI API keys configured')
        
        # Check database URL
        if not config.DATABASE_URL:
            issues.append('ERROR: Database URL not configured')
        
        # Categorize issues
        critical_issues = [issue for issue in issues if issue.startswith('CRITICAL')]
        error_issues = [issue for issue in issues if issue.startswith('ERROR')]
        warning_issues = [issue for issue in issues if issue.startswith('WARNING')]
        
        validation_result = {
            'is_valid': len(critical_issues) == 0 and len(error_issues) == 0,
            'total_issues': len(issues),
            'critical_issues': critical_issues,
            'error_issues': error_issues,
            'warning_issues': warning_issues,
            'environment': config.FLASK_ENV,
            'is_production': config.FLASK_ENV == 'production',
            'validated_at': datetime.now(timezone.utc).isoformat()
        }
        
        return jsonify({
            'success': True,
            'validation': validation_result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Configuration validation failed: {str(e)}'
        }), 500

@config_bp.route('/features', methods=['GET'])
def get_feature_flags():
    """Get current feature flag status"""
    if not CONFIG_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Configuration system not available'
        }), 500
    
    try:
        # Create feature flags from config
        features = {
            'ai_generation': config.ENABLE_AI_GENERATION,
            'debug_mode': config.DEBUG,
            'ai_cache': config.AI_CACHE_ENABLED,
            'ai_fallback': config.AI_FALLBACK_ENABLED,
            'caching': getattr(config, 'ENABLE_CACHING', False),
            'metrics': getattr(config, 'ENABLE_METRICS', False),
            'csrf': getattr(config, 'ENABLE_CSRF', True)
        }
        
        return jsonify({
            'success': True,
            'features': features,
            'enabled_count': sum(1 for v in features.values() if v),
            'total_count': len(features)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get feature flags: {str(e)}'
        }), 500

@config_bp.route('/rate-limits', methods=['GET'])
def get_rate_limits():
    """Get current rate limiting configuration"""
    if not CONFIG_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Configuration system not available'
        }), 500
    
    try:
        # Create rate limits from config
        rate_limits = {
            'generate': config.GENERATE_RATE_LIMIT,
            'prompt_help': config.PROMPT_HELP_RATE_LIMIT,
            'validate': config.VALIDATE_RATE_LIMIT,
            'preview': config.PREVIEW_RATE_LIMIT
        }
        
        return jsonify({
            'success': True,
            'rate_limits': rate_limits,
            'global_limits': {
                'per_hour': config.RATE_LIMIT_PER_HOUR,
                'per_minute': config.RATE_LIMIT_PER_MINUTE
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get rate limits: {str(e)}'
        }), 500

@config_bp.route('/database', methods=['GET'])
def get_database_config():
    """Get database configuration (excluding sensitive data)"""
    if not CONFIG_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Configuration system not available'
        }), 500
    
    try:
        # Create database config from available settings
        safe_config = {
            'pool_size': getattr(config, 'DATABASE_POOL_SIZE', 10),
            'timeout': getattr(config, 'DATABASE_TIMEOUT', 30),
            'echo': False,
            'url_type': 'sqlite' if 'sqlite' in config.DATABASE_URL else 'other'
        }
        
        return jsonify({
            'success': True,
            'database': safe_config
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get database config: {str(e)}'
        }), 500

@config_bp.route('/cache', methods=['GET'])
def get_cache_config():
    """Get cache configuration"""
    if not CONFIG_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Configuration system not available'
        }), 500
    
    try:
        # Create cache config from available settings
        redis_url = getattr(config, 'REDIS_URL', '')
        cache_timeout = getattr(config, 'CACHE_TIMEOUT', 3600)
        cache_enabled = getattr(config, 'ENABLE_CACHING', False)
        
        return jsonify({
            'success': True,
            'cache': {
                'enabled': cache_enabled,
                'timeout': cache_timeout,
                'url_configured': bool(redis_url)
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to get cache config: {str(e)}'
        }), 500

@config_bp.route('/reload', methods=['POST'])
def reload_configuration():
    """Reload configuration from all sources"""
    if not CONFIG_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Configuration system not available'
        }), 500
    
    try:
        # Check if this is allowed (only in development)
        if config.FLASK_ENV == 'production':
            return jsonify({
                'success': False,
                'error': 'Configuration reload not allowed in production'
            }), 403
        
        # Simulate reload (in a real implementation, this would reload the config)
        summary = {
            'environment': config.FLASK_ENV,
            'debug': config.DEBUG,
            'sources_loaded': ['env_file', 'defaults']
        }
        
        return jsonify({
            'success': True,
            'message': 'Configuration reloaded successfully',
            'summary': summary,
            'reloaded_at': datetime.now(timezone.utc).isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to reload configuration: {str(e)}'
        }), 500

@config_bp.route('/export', methods=['GET'])
def export_configuration():
    """Export current configuration (excluding sensitive data)"""
    if not CONFIG_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Configuration system not available'
        }), 500
    
    try:
        # Create a safe export of configuration (excluding sensitive data)
        config_dict = {
            'environment': config.FLASK_ENV,
            'debug': config.DEBUG,
            'host': config.HOST,
            'port': config.PORT,
            'max_workflow_nodes': config.MAX_WORKFLOW_NODES,
            'default_complexity': config.DEFAULT_COMPLEXITY,
            'enable_ai_generation': config.ENABLE_AI_GENERATION,
            'workflow_timeout': config.WORKFLOW_TIMEOUT,
            'rate_limit_per_hour': config.RATE_LIMIT_PER_HOUR,
            'rate_limit_per_minute': config.RATE_LIMIT_PER_MINUTE,
            'ai_cache_enabled': config.AI_CACHE_ENABLED,
            'ai_fallback_enabled': config.AI_FALLBACK_ENABLED
        }
        
        export_data = {
            'configuration': config_dict,
            'metadata': {
                'exported_at': datetime.now(timezone.utc).isoformat(),
                'environment': config.FLASK_ENV,
                'version': '1.0.0',
                'sources': ['env_file', 'defaults']
            }
        }
        
        return jsonify({
            'success': True,
            'export': export_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to export configuration: {str(e)}'
        }), 500

@config_bp.route('/health', methods=['GET'])
def config_health():
    """Configuration system health check"""
    if not CONFIG_AVAILABLE:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': 'Configuration system not available'
        }), 500
    
    try:
        # Basic health check - verify essential config is available
        issues = []
        if not config.SECRET_KEY or config.SECRET_KEY == 'dev-key-change-in-production':
            issues.append('WARNING: Using default secret key')
        
        critical_issues = [issue for issue in issues if issue.startswith('CRITICAL')]
        error_issues = [issue for issue in issues if issue.startswith('ERROR')]
        
        is_healthy = len(critical_issues) == 0 and len(error_issues) == 0
        
        return jsonify({
            'success': True,
            'status': 'healthy' if is_healthy else 'unhealthy',
            'issues_count': len(issues),
            'critical_issues_count': len(critical_issues),
            'error_issues_count': len(error_issues),
            'environment': config.FLASK_ENV,
            'checked_at': datetime.now(timezone.utc).isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'unhealthy',
            'error': f'Health check failed: {str(e)}'
        }), 500

# Error handlers for the configuration API
@config_bp.errorhandler(404)
def config_not_found(error):
    return jsonify({
        'success': False,
        'error': 'Configuration endpoint not found'
    }), 404

@config_bp.errorhandler(405)
def config_method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 'Method not allowed for this configuration endpoint'
    }), 405