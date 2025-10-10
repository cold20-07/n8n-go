#!/usr/bin/env python3
"""
Redis Caching System for N8N Workflow Generator
Provides intelligent caching for workflows, AI responses, and validation results
"""

import json
import hashlib
import pickle
import logging
from typing import Any, Optional, Dict, List, Union
from datetime import datetime, timedelta
from functools import wraps
import redis
from flask import current_app

logger = logging.getLogger(__name__)

class CacheManager:
    """Advanced Redis cache manager with intelligent key management and fallbacks"""
    
    def __init__(self, redis_url: str = None, default_ttl: int = 3600):
        """
        Initialize cache manager
        
        Args:
            redis_url: Redis connection URL
            default_ttl: Default time-to-live in seconds (1 hour)
        """
        self.default_ttl = default_ttl
        self.redis_client = None
        self.fallback_cache = {}  # In-memory fallback
        self.cache_stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'errors': 0
        }
        
        # Initialize Redis connection
        self._init_redis(redis_url)
    
    def _init_redis(self, redis_url: str = None):
        """Initialize Redis connection with fallback handling"""
        try:
            if redis_url:
                self.redis_client = redis.from_url(redis_url, decode_responses=False)
            else:
                # Try default Redis connection
                self.redis_client = redis.Redis(
                    host='localhost',
                    port=6379,
                    db=0,
                    decode_responses=False,
                    socket_connect_timeout=5,
                    socket_timeout=5
                )
            
            # Test connection
            self.redis_client.ping()
            logger.info("✅ Redis cache initialized successfully")
            
        except Exception as e:
            logger.warning(f"⚠️ Redis not available, using in-memory fallback: {e}")
            self.redis_client = None
    
    def _generate_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate a consistent cache key from arguments"""
        # Create a string representation of all arguments
        key_data = {
            'args': args,
            'kwargs': sorted(kwargs.items()) if kwargs else {}
        }
        
        # Create hash of the data
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        key_hash = hashlib.md5(key_string.encode()).hexdigest()[:12]
        
        return f"n8n_cache:{prefix}:{key_hash}"
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache with fallback handling"""
        try:
            if self.redis_client:
                # Try Redis first
                value = self.redis_client.get(key)
                if value is not None:
                    self.cache_stats['hits'] += 1
                    return pickle.loads(value)
            
            # Fallback to in-memory cache
            if key in self.fallback_cache:
                entry = self.fallback_cache[key]
                if entry['expires'] > datetime.now():
                    self.cache_stats['hits'] += 1
                    return entry['value']
                else:
                    # Expired entry
                    del self.fallback_cache[key]
            
            self.cache_stats['misses'] += 1
            return None
            
        except Exception as e:
            logger.error(f"Cache get error for key {key}: {e}")
            self.cache_stats['errors'] += 1
            return None
    
    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set value in cache with fallback handling"""
        if ttl is None:
            ttl = self.default_ttl
        
        try:
            if self.redis_client:
                # Try Redis first
                serialized_value = pickle.dumps(value)
                success = self.redis_client.setex(key, ttl, serialized_value)
                if success:
                    self.cache_stats['sets'] += 1
                    return True
            
            # Fallback to in-memory cache
            self.fallback_cache[key] = {
                'value': value,
                'expires': datetime.now() + timedelta(seconds=ttl)
            }
            self.cache_stats['sets'] += 1
            
            # Clean up expired entries periodically
            self._cleanup_fallback_cache()
            return True
            
        except Exception as e:
            logger.error(f"Cache set error for key {key}: {e}")
            self.cache_stats['errors'] += 1
            return False
    
    def delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            deleted = False
            
            if self.redis_client:
                deleted = bool(self.redis_client.delete(key))
            
            if key in self.fallback_cache:
                del self.fallback_cache[key]
                deleted = True
            
            return deleted
            
        except Exception as e:
            logger.error(f"Cache delete error for key {key}: {e}")
            return False
    
    def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching a pattern"""
        try:
            deleted_count = 0
            
            if self.redis_client:
                keys = self.redis_client.keys(pattern)
                if keys:
                    deleted_count = self.redis_client.delete(*keys)
            
            # Clear from fallback cache
            keys_to_delete = [k for k in self.fallback_cache.keys() if pattern.replace('*', '') in k]
            for key in keys_to_delete:
                del self.fallback_cache[key]
                deleted_count += 1
            
            logger.info(f"Cleared {deleted_count} cache entries matching pattern: {pattern}")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Cache clear pattern error: {e}")
            return 0
    
    def _cleanup_fallback_cache(self):
        """Clean up expired entries from fallback cache"""
        if len(self.fallback_cache) > 1000:  # Only cleanup when cache gets large
            now = datetime.now()
            expired_keys = [
                key for key, entry in self.fallback_cache.items()
                if entry['expires'] <= now
            ]
            for key in expired_keys:
                del self.fallback_cache[key]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self.cache_stats['hits'] + self.cache_stats['misses']
        hit_rate = (self.cache_stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        stats = {
            **self.cache_stats,
            'hit_rate': round(hit_rate, 2),
            'total_requests': total_requests,
            'redis_available': self.redis_client is not None,
            'fallback_cache_size': len(self.fallback_cache)
        }
        
        if self.redis_client:
            try:
                redis_info = self.redis_client.info()
                stats['redis_memory_used'] = redis_info.get('used_memory_human', 'Unknown')
                stats['redis_connected_clients'] = redis_info.get('connected_clients', 0)
            except Exception:
                pass
        
        return stats

# Global cache instance
cache_manager = None

def init_cache(redis_url: str = None, default_ttl: int = 3600):
    """Initialize global cache manager"""
    global cache_manager
    cache_manager = CacheManager(redis_url, default_ttl)
    return cache_manager

def get_cache() -> CacheManager:
    """Get global cache manager instance"""
    global cache_manager
    if cache_manager is None:
        cache_manager = CacheManager()
    return cache_manager

# Decorators for easy caching

def cache_result(prefix: str, ttl: int = None):
    """
    Decorator to cache function results
    
    Args:
        prefix: Cache key prefix
        ttl: Time-to-live in seconds
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache = get_cache()
            
            # Generate cache key
            cache_key = cache._generate_key(prefix, *args, **kwargs)
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            logger.debug(f"Cached result for {func.__name__}")
            
            return result
    return decorator

def cache_workflow_generation(ttl: int = 1800):  # 30 minutes
    """Decorator specifically for workflow generation caching"""
    return cache_result("workflow_gen", ttl)

def cache_ai_response(ttl: int = 3600):  # 1 hour
    """Decorator specifically for AI response caching"""
    return cache_result("ai_response", ttl)

def cache_validation_result(ttl: int = 900):  # 15 minutes
    """Decorator specifically for validation result caching"""
    return cache_result("validation", ttl)

def cache_template_data(ttl: int = 7200):  # 2 hours
    """Decorator specifically for template data caching"""
    return cache_result("template", ttl)

# Cache warming functions

def warm_template_cache():
    """Pre-load commonly used templates into cache"""
    try:
        from src.templates.workflow_templates import get_all_templates
        from dataclasses import asdict
        templates = get_all_templates()
        cache = get_cache()
        
        # templates is a list of WorkflowTemplate objects
        for template in templates:
            cache_key = cache._generate_key("template", template.id)
            # Convert dataclass to dict
            template_dict = asdict(template)
            cache.set(cache_key, template_dict, 7200)  # 2 hours
        
        logger.info(f"Warmed cache with {len(templates)} templates")
        
    except Exception as e:
        logger.error(f"Failed to warm template cache: {e}")

def warm_validation_cache():
    """Pre-load common validation patterns"""
    try:
        # This could be expanded to pre-cache common validation scenarios
        logger.info("Validation cache warming completed")
        
    except Exception as e:
        logger.error(f"Failed to warm validation cache: {e}")

# Cache management utilities

def clear_all_cache():
    """Clear all cache entries"""
    cache = get_cache()
    return cache.clear_pattern("n8n_cache:*")

def clear_workflow_cache():
    """Clear workflow generation cache"""
    cache = get_cache()
    return cache.clear_pattern("n8n_cache:workflow_gen:*")

def clear_ai_cache():
    """Clear AI response cache"""
    cache = get_cache()
    return cache.clear_pattern("n8n_cache:ai_response:*")

def get_cache_info():
    """Get comprehensive cache information"""
    cache = get_cache()
    return cache.get_stats()