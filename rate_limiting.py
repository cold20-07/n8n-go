"""
Rate limiting configuration and utilities for N8N Workflow Generator
"""
import time
from collections import defaultdict, deque
from typing import Dict, Optional
from flask import request, jsonify
from functools import wraps

class RateLimitMonitor:
    """Monitor and track rate limiting statistics"""
    
    def __init__(self):
        self.request_counts = defaultdict(int)
        self.blocked_requests = defaultdict(int)
        self.request_history = defaultdict(lambda: deque(maxlen=1000))
        self.start_time = time.time()
    
    def record_request(self, ip: str, endpoint: str, blocked: bool = False):
        """Record a request for monitoring"""
        timestamp = time.time()
        key = f"{ip}:{endpoint}"
        
        self.request_counts[key] += 1
        if blocked:
            self.blocked_requests[key] += 1
        
        self.request_history[key].append({
            'timestamp': timestamp,
            'blocked': blocked
        })
    
    def get_stats(self) -> Dict:
        """Get rate limiting statistics"""
        total_requests = sum(self.request_counts.values())
        total_blocked = sum(self.blocked_requests.values())
        uptime = time.time() - self.start_time
        
        return {
            'uptime_seconds': uptime,
            'total_requests': total_requests,
            'total_blocked': total_blocked,
            'block_rate': (total_blocked / total_requests * 100) if total_requests > 0 else 0,
            'requests_per_minute': (total_requests / uptime * 60) if uptime > 0 else 0,
            'top_ips': self._get_top_ips(),
            'top_endpoints': self._get_top_endpoints()
        }
    
    def _get_top_ips(self, limit: int = 10) -> list:
        """Get top IPs by request count"""
        ip_counts = defaultdict(int)
        for key, count in self.request_counts.items():
            ip = key.split(':')[0]
            ip_counts[ip] += count
        
        return sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:limit]
    
    def _get_top_endpoints(self, limit: int = 10) -> list:
        """Get top endpoints by request count"""
        endpoint_counts = defaultdict(int)
        for key, count in self.request_counts.items():
            endpoint = key.split(':', 1)[1]
            endpoint_counts[endpoint] += count
        
        return sorted(endpoint_counts.items(), key=lambda x: x[1], reverse=True)[:limit]

# Global rate limit monitor
rate_monitor = RateLimitMonitor()

def custom_rate_limit(limit: str, per: str = "minute", key_func=None):
    """
    Custom rate limiting decorator with monitoring
    
    Args:
        limit: Number of requests (e.g., "10")
        per: Time period ("minute", "hour", "day")
        key_func: Function to generate rate limit key
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Get client identifier
            if key_func:
                client_key = key_func()
            else:
                client_key = request.remote_addr or 'unknown'
            
            endpoint = request.endpoint or 'unknown'
            
            # Record the request
            rate_monitor.record_request(client_key, endpoint, blocked=False)
            
            # Execute the original function
            return f(*args, **kwargs)
        
        return wrapper
    return decorator

def get_client_id() -> str:
    """Get client identifier for rate limiting"""
    # Try to get real IP from headers (for reverse proxy setups)
    real_ip = request.headers.get('X-Real-IP')
    forwarded_for = request.headers.get('X-Forwarded-For')
    
    if real_ip:
        return real_ip
    elif forwarded_for:
        # Get first IP from X-Forwarded-For
        return forwarded_for.split(',')[0].strip()
    else:
        return request.remote_addr or 'unknown'

def rate_limit_exceeded_handler(retry_after: Optional[int] = None):
    """Handle rate limit exceeded with custom response"""
    client_id = get_client_id()
    endpoint = request.endpoint or 'unknown'
    
    # Record blocked request
    rate_monitor.record_request(client_id, endpoint, blocked=True)
    
    response_data = {
        'success': False,
        'error': 'RATE_LIMIT_EXCEEDED',
        'message': 'Too many requests. Please slow down.',
        'retry_after': retry_after or 60,
        'client_id': client_id[:8] + '...' if len(client_id) > 8 else client_id  # Partial ID for debugging
    }
    
    return jsonify(response_data), 429

def get_rate_limit_stats():
    """Get rate limiting statistics for monitoring"""
    return rate_monitor.get_stats()

# Rate limiting configuration based on endpoint sensitivity
RATE_LIMITS = {
    'generate': {
        'limit': '10 per minute',
        'description': 'Workflow generation (resource intensive)'
    },
    'prompt-help': {
        'limit': '20 per minute', 
        'description': 'Prompt assistance (moderate usage)'
    },
    'validate': {
        'limit': '30 per minute',
        'description': 'Workflow validation (light processing)'
    },
    'preview': {
        'limit': '50 per minute',
        'description': 'Preview generation (lightweight)'
    },
    'health': {
        'limit': None,
        'description': 'Health check (no limit)'
    }
}

def get_rate_limit_info():
    """Get information about rate limits for documentation"""
    return {
        'rate_limits': RATE_LIMITS,
        'global_limit': '100 per hour',
        'note': 'Rate limits are per IP address and reset automatically'
    }