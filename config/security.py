"""
Security configuration for n8n Workflow Generator
"""

import os
from typing import Dict, List

class SecurityConfig:
    """Security configuration settings"""
    
    # CORS Settings
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://localhost:5000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5000"
    ]
    
    # Content Security Policy
    CSP_DIRECTIVES = {
        'default-src': ["'self'"],
        'script-src': [
            "'self'",
            "'unsafe-inline'",  # Required for inline scripts
            "https://cdn.jsdelivr.net",
            "https://unpkg.com"
        ],
        'style-src': [
            "'self'",
            "'unsafe-inline'",  # Required for inline styles
            "https://fonts.googleapis.com",
            "https://cdn.jsdelivr.net"
        ],
        'font-src': [
            "'self'",
            "https://fonts.gstatic.com"
        ],
        'img-src': [
            "'self'",
            "data:",
            "https:"
        ],
        'connect-src': [
            "'self'",
            "https://api.gemini.com",
            "https://api.openai.com",
            "https://api.anthropic.com"
        ]
    }
    
    # Rate Limiting
    RATE_LIMITS = {
        'default': '100 per hour',
        'generate': '50 per hour',
        'validate': '200 per hour',
        'templates': '500 per hour'
    }
    
    # Input Validation
    MAX_DESCRIPTION_LENGTH = 1000
    MIN_DESCRIPTION_LENGTH = 10
    ALLOWED_TRIGGER_TYPES = ['webhook', 'schedule', 'manual', 'email']
    ALLOWED_COMPLEXITY_LEVELS = ['simple', 'medium', 'complex']
    
    # File Upload (if implemented)
    MAX_FILE_SIZE = 1024 * 1024  # 1MB
    ALLOWED_EXTENSIONS = {'.json', '.txt'}
    
    # API Security
    API_KEY_LENGTH = 32
    SESSION_TIMEOUT = 3600  # 1 hour
    
    # Headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Referrer-Policy': 'strict-origin-when-cross-origin'
    }
    
    @classmethod
    def get_cors_origins(cls) -> List[str]:
        """Get CORS origins from environment or defaults"""
        env_origins = os.getenv('CORS_ORIGINS')
        if env_origins:
            return env_origins.split(',')
        return cls.CORS_ORIGINS
    
    @classmethod
    def is_production(cls) -> bool:
        """Check if running in production"""
        return os.getenv('FLASK_ENV') == 'production'
    
    @classmethod
    def get_rate_limit(cls, endpoint: str) -> str:
        """Get rate limit for specific endpoint"""
        return cls.RATE_LIMITS.get(endpoint, cls.RATE_LIMITS['default'])

# Input sanitization patterns
DANGEROUS_PATTERNS = [
    r'<script[^>]*>.*?</script>',
    r'javascript:',
    r'vbscript:',
    r'onload\s*=',
    r'onerror\s*=',
    r'onclick\s*=',
    r'eval\s*\(',
    r'setTimeout\s*\(',
    r'setInterval\s*\('
]

# Allowed HTML tags for rich text (if implemented)
ALLOWED_HTML_TAGS = {
    'b', 'i', 'u', 'strong', 'em', 'p', 'br', 'ul', 'ol', 'li'
}

# API endpoint security configurations
ENDPOINT_SECURITY = {
    '/api/generate': {
        'rate_limit': '50 per hour',
        'require_validation': True,
        'max_payload_size': 10240  # 10KB
    },
    '/api/validate': {
        'rate_limit': '200 per hour',
        'require_validation': True,
        'max_payload_size': 51200  # 50KB
    },
    '/api/templates': {
        'rate_limit': '500 per hour',
        'require_validation': False,
        'max_payload_size': 1024  # 1KB
    }
}