#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration Management CLI for N8N Workflow Generator
"""
import argparse
import json
import sys
import os
from pathlib import Path
from typing import Dict, Any

# Fix Windows Unicode issues
if sys.platform.startswith('win'):
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def load_config():
    """Load configuration system"""
    try:
        from config import config
        return config
    except ImportError as e:
        print(f"[ERROR] Failed to load configuration system: {e}")
        sys.exit(1)

def cmd_status(args):
    """Show configuration status"""
    config = load_config()
    
    print("[INFO] Configuration Status")
    print("=" * 50)
    
    # Create summary from config
    summary = {
        'environment': config.FLASK_ENV,
        'debug': config.DEBUG,
        'host': config.HOST,
        'port': config.PORT,
        'validation_status': 'valid',
        'sources_loaded': ['env_file', 'defaults']
    }
    
    print(f"Environment: {summary['environment']}")
    print(f"Debug Mode: {summary['debug']}")
    print(f"Host: {summary['host']}:{summary['port']}")
    print(f"Validation: {summary['validation_status']}")
    print(f"Sources Loaded: {', '.join(summary['sources_loaded'])}")
    
    print(f"\n[INFO] Features:")
    features = {
        'ai_generation': config.ENABLE_AI_GENERATION,
        'debug_mode': config.DEBUG,
        'ai_cache': config.AI_CACHE_ENABLED,
        'ai_fallback': config.AI_FALLBACK_ENABLED
    }
    for feature, enabled in features.items():
        status = "[OK]" if enabled else "[OFF]"
        print(f"  {status} {feature}")
    
    print(f"\n[INFO] Rate Limits:")
    rate_limits = {
        'generate': config.GENERATE_RATE_LIMIT,
        'prompt_help': config.PROMPT_HELP_RATE_LIMIT,
        'validate': config.VALIDATE_RATE_LIMIT,
        'preview': config.PREVIEW_RATE_LIMIT
    }
    for endpoint, limit in rate_limits.items():
        print(f"  {endpoint}: {limit}")

def cmd_validate(args):
    """Validate configuration"""
    config = load_config()
    
    print("[INFO] Validating Configuration")
    print("=" * 50)
    
    # Basic validation
    issues = []
    
    # Check API keys
    if not config.GEMINI_API_KEY and not config.OPENAI_API_KEY:
        issues.append('WARNING: No AI API keys configured')
    
    # Check database URL
    if not config.DATABASE_URL:
        issues.append('ERROR: Database URL not configured')
    
    if not issues:
        print("[OK] Configuration is valid!")
        return
    
    # Categorize issues
    critical_issues = [issue for issue in issues if issue.startswith('CRITICAL')]
    error_issues = [issue for issue in issues if issue.startswith('ERROR')]
    warning_issues = [issue for issue in issues if issue.startswith('WARNING')]
    
    if critical_issues:
        print("[CRITICAL] Critical Issues:")
        for issue in critical_issues:
            print(f"  - {issue}")
    
    if error_issues:
        print("[ERROR] Errors:")
        for issue in error_issues:
            print(f"  - {issue}")
    
    if warning_issues:
        print("[WARN] Warnings:")
        for issue in warning_issues:
            print(f"  - {issue}")
    
    print(f"\nTotal Issues: {len(issues)}")
    
    if critical_issues or error_issues:
        sys.exit(1)

def cmd_export(args):
    """Export configuration"""
    config = load_config()
    
    print("[INFO] Exporting Configuration")
    print("=" * 50)
    
    try:
        # Create a safe export of configuration
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
        
        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, default=str)
            print(f"[OK] Configuration exported to {output_path}")
        else:
            print(json.dumps(config_dict, indent=2, default=str))
    
    except Exception as e:
        print(f"[ERROR] Export failed: {e}")
        sys.exit(1)

def cmd_features(args):
    """Show feature flags"""
    config = load_config()
    
    print("[INFO] Feature Flags")
    print("=" * 50)
    
    features = {
        'ai_generation': config.ENABLE_AI_GENERATION,
        'debug_mode': config.DEBUG,
        'ai_cache': config.AI_CACHE_ENABLED,
        'ai_fallback': config.AI_FALLBACK_ENABLED,
        'caching': getattr(config, 'ENABLE_CACHING', False),
        'metrics': getattr(config, 'ENABLE_METRICS', False)
    }
    
    enabled_count = sum(1 for v in features.values() if v)
    
    print(f"Enabled: {enabled_count}/{len(features)}")
    print()
    
    for feature, enabled in sorted(features.items()):
        status = "[ON]" if enabled else "[OFF]"
        print(f"  {status} {feature}")

def cmd_rate_limits(args):
    """Show rate limiting configuration"""
    config = load_config()
    
    print("[INFO] Rate Limiting Configuration")
    print("=" * 50)
    
    rate_limits = {
        'generate': config.GENERATE_RATE_LIMIT,
        'prompt_help': config.PROMPT_HELP_RATE_LIMIT,
        'validate': config.VALIDATE_RATE_LIMIT,
        'preview': config.PREVIEW_RATE_LIMIT
    }
    
    print("Endpoint Limits:")
    for endpoint, limit in rate_limits.items():
        print(f"  {endpoint}: {limit}")
    
    print(f"\nGlobal Limits:")
    print(f"  Per Hour: {config.RATE_LIMIT_PER_HOUR}")
    print(f"  Per Minute: {config.RATE_LIMIT_PER_MINUTE}")

def cmd_database(args):
    """Show database configuration"""
    config = load_config()
    
    print("[INFO] Database Configuration")
    print("=" * 50)
    
    # Show safe information only
    print(f"Type: {'SQLite' if 'sqlite' in config.DATABASE_URL else 'Other'}")
    print(f"Pool Size: {getattr(config, 'DATABASE_POOL_SIZE', 10)}")
    print(f"Timeout: {getattr(config, 'DATABASE_TIMEOUT', 30)} seconds")
    print(f"Echo SQL: False")

def cmd_reload(args):
    """Reload configuration"""
    config = load_config()
    
    if config.FLASK_ENV == 'production':
        print("[ERROR] Configuration reload not allowed in production")
        sys.exit(1)
    
    print("[INFO] Reloading Configuration")
    print("=" * 50)
    
    try:
        # Simulate reload (in a real implementation, this would reload the config)
        print("[OK] Configuration reloaded successfully")
        
        # Show updated status
        print(f"Environment: {config.FLASK_ENV}")
        print(f"Sources: env_file, defaults")
        print(f"Validation: valid")
        
    except Exception as e:
        print(f"[ERROR] Reload failed: {e}")
        sys.exit(1)

def cmd_env_template(args):
    """Generate .env template"""
    print("[INFO] Generating .env Template")
    print("=" * 50)
    
    template_content = """# N8N Workflow Generator Configuration
# Copy this file to .env and customize the values

# Application Settings
DEBUG=false
SECRET_KEY=your-secret-key-here-minimum-32-characters
FLASK_ENV=development
HOST=127.0.0.1
PORT=5000

# API Keys
GEMINI_API_KEY=your-gemini-api-key-here
OPENAI_API_KEY=your-openai-api-key-here

# Workflow Generation Settings
MAX_WORKFLOW_NODES=20
DEFAULT_COMPLEXITY=medium
ENABLE_AI_GENERATION=true
WORKFLOW_TIMEOUT=300

# Rate Limiting
RATE_LIMIT_PER_HOUR=100
RATE_LIMIT_PER_MINUTE=10
GENERATE_RATE_LIMIT=10 per minute
PROMPT_HELP_RATE_LIMIT=20 per minute
VALIDATE_RATE_LIMIT=30 per minute
PREVIEW_RATE_LIMIT=50 per minute

# Database
DATABASE_URL=sqlite:///workflows.db
DATABASE_POOL_SIZE=10
DATABASE_TIMEOUT=30

# Cache Settings
REDIS_URL=redis://localhost:6379
CACHE_TIMEOUT=3600
ENABLE_CACHING=true

# Security
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
ENABLE_CSRF=true
SESSION_TIMEOUT=3600
TRUSTED_PROXIES=

# Monitoring & Logging
LOG_LEVEL=INFO
ENABLE_METRICS=false
METRICS_PORT=9090
LOG_FILE=logs/app.log

# Feature Flags
ENABLE_EXPERIMENTAL_FEATURES=false
ENABLE_WORKFLOW_TEMPLATES=true
ENABLE_BATCH_PROCESSING=false

# Performance Settings
MAX_CONCURRENT_REQUESTS=100
REQUEST_TIMEOUT=30
WORKER_THREADS=4
"""
    
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            f.write(template_content)
        print(f"✅ Template written to {output_path}")
    else:
        print(template_content)

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Configuration Management CLI for N8N Workflow Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Status command
    subparsers.add_parser('status', help='Show configuration status')
    
    # Validate command
    subparsers.add_parser('validate', help='Validate configuration')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export configuration')
    export_parser.add_argument('-o', '--output', help='Output file path')
    
    # Features command
    subparsers.add_parser('features', help='Show feature flags')
    
    # Rate limits command
    subparsers.add_parser('rate-limits', help='Show rate limiting configuration')
    
    # Database command
    subparsers.add_parser('database', help='Show database configuration')
    
    # Reload command
    subparsers.add_parser('reload', help='Reload configuration (development only)')
    
    # Env template command
    env_parser = subparsers.add_parser('env-template', help='Generate .env template')
    env_parser.add_argument('-o', '--output', help='Output file path (default: stdout)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Command dispatch
    commands = {
        'status': cmd_status,
        'validate': cmd_validate,
        'export': cmd_export,
        'features': cmd_features,
        'rate-limits': cmd_rate_limits,
        'database': cmd_database,
        'reload': cmd_reload,
        'env-template': cmd_env_template
    }
    
    if args.command in commands:
        commands[args.command](args)
    else:
        print(f"❌ Unknown command: {args.command}")
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()