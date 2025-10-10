#!/usr/bin/env python3
"""
Cache Management API for N8N Workflow Generator
Provides endpoints for cache monitoring and management
"""

from flask import Blueprint, jsonify, request
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

# Create blueprint for cache API
cache_bp = Blueprint('cache_api', __name__, url_prefix='/api/cache')

@cache_bp.route('/status', methods=['GET'])
def cache_status():
    """Get cache system status and statistics"""
    try:
        from src.core.cache import get_cache
        cache = get_cache()
        stats = cache.get_stats()
        
        return jsonify({
            'success': True,
            'cache_status': 'active' if stats['redis_available'] else 'fallback',
            'statistics': stats,
            'message': 'Cache system is operational'
        })
        
    except Exception as e:
        logger.error(f"Cache status error: {e}")
        return jsonify({
            'success': False,
            'error': 'Cache system unavailable',
            'details': str(e)
        }), 500

@cache_bp.route('/stats', methods=['GET'])
def cache_stats():
    """Get detailed cache statistics"""
    try:
        from src.core.cache import get_cache
        cache = get_cache()
        stats = cache.get_stats()
        
        # Add additional metrics
        detailed_stats = {
            **stats,
            'cache_efficiency': {
                'hit_rate_category': 'excellent' if stats['hit_rate'] > 80 else 'good' if stats['hit_rate'] > 60 else 'needs_improvement',
                'total_operations': stats['hits'] + stats['misses'] + stats['sets'],
                'error_rate': (stats['errors'] / max(stats['total_requests'], 1)) * 100
            }
        }
        
        return jsonify({
            'success': True,
            'statistics': detailed_stats
        })
        
    except Exception as e:
        logger.error(f"Cache stats error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve cache statistics'
        }), 500

@cache_bp.route('/clear', methods=['POST'])
def clear_cache():
    """Clear cache entries based on pattern or clear all"""
    try:
        data = request.get_json() or {}
        pattern = data.get('pattern', 'n8n_cache:*')
        
        from src.core.cache import get_cache
        cache = get_cache()
        
        if pattern == 'all':
            pattern = 'n8n_cache:*'
        
        cleared_count = cache.clear_pattern(pattern)
        
        return jsonify({
            'success': True,
            'message': f'Cleared {cleared_count} cache entries',
            'pattern': pattern,
            'cleared_count': cleared_count
        })
        
    except Exception as e:
        logger.error(f"Cache clear error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to clear cache'
        }), 500

@cache_bp.route('/clear/workflows', methods=['POST'])
def clear_workflow_cache():
    """Clear workflow generation cache"""
    try:
        from src.core.cache import clear_workflow_cache
        cleared_count = clear_workflow_cache()
        
        return jsonify({
            'success': True,
            'message': f'Cleared {cleared_count} workflow cache entries',
            'cache_type': 'workflow_generation'
        })
        
    except Exception as e:
        logger.error(f"Workflow cache clear error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to clear workflow cache'
        }), 500

@cache_bp.route('/clear/ai', methods=['POST'])
def clear_ai_cache():
    """Clear AI response cache"""
    try:
        from src.core.cache import clear_ai_cache
        cleared_count = clear_ai_cache()
        
        return jsonify({
            'success': True,
            'message': f'Cleared {cleared_count} AI cache entries',
            'cache_type': 'ai_responses'
        })
        
    except Exception as e:
        logger.error(f"AI cache clear error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to clear AI cache'
        }), 500

@cache_bp.route('/warm', methods=['POST'])
def warm_cache():
    """Warm cache with commonly used data"""
    try:
        data = request.get_json() or {}
        cache_types = data.get('types', ['templates'])
        
        results = {}
        
        if 'templates' in cache_types:
            try:
                from src.core.cache import warm_template_cache
                warm_template_cache()
                results['templates'] = 'success'
            except Exception as e:
                results['templates'] = f'failed: {str(e)}'
        
        if 'validation' in cache_types:
            try:
                from src.core.cache import warm_validation_cache
                warm_validation_cache()
                results['validation'] = 'success'
            except Exception as e:
                results['validation'] = f'failed: {str(e)}'
        
        return jsonify({
            'success': True,
            'message': 'Cache warming completed',
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Cache warming error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to warm cache'
        }), 500

@cache_bp.route('/health', methods=['GET'])
def cache_health():
    """Get cache system health check"""
    try:
        from src.core.cache import get_cache
        cache = get_cache()
        stats = cache.get_stats()
        
        # Determine health status
        health_status = 'healthy'
        issues = []
        
        if not stats['redis_available']:
            health_status = 'degraded'
            issues.append('Redis unavailable, using fallback cache')
        
        if stats['error_rate'] > 10:  # More than 10% error rate
            health_status = 'unhealthy'
            issues.append(f"High error rate: {stats['error_rate']:.1f}%")
        
        if stats['hit_rate'] < 30:  # Less than 30% hit rate
            health_status = 'degraded'
            issues.append(f"Low cache hit rate: {stats['hit_rate']:.1f}%")
        
        return jsonify({
            'success': True,
            'health_status': health_status,
            'issues': issues,
            'statistics': {
                'hit_rate': stats['hit_rate'],
                'total_requests': stats['total_requests'],
                'redis_available': stats['redis_available'],
                'fallback_cache_size': stats['fallback_cache_size']
            }
        })
        
    except Exception as e:
        logger.error(f"Cache health check error: {e}")
        return jsonify({
            'success': False,
            'health_status': 'unhealthy',
            'error': 'Cache health check failed'
        }), 500

@cache_bp.route('/keys', methods=['GET'])
def cache_keys():
    """Get cache keys (limited for security)"""
    try:
        pattern = request.args.get('pattern', 'n8n_cache:*')
        limit = min(int(request.args.get('limit', 100)), 1000)  # Max 1000 keys
        
        from src.core.cache import get_cache
        cache = get_cache()
        
        keys = []
        if cache.redis_client:
            try:
                redis_keys = cache.redis_client.keys(pattern)
                keys.extend([key.decode() if isinstance(key, bytes) else key for key in redis_keys[:limit]])
            except Exception as e:
                logger.warning(f"Failed to get Redis keys: {e}")
        
        # Add fallback cache keys
        fallback_keys = [k for k in cache.fallback_cache.keys() if pattern.replace('*', '') in k]
        keys.extend(fallback_keys[:limit - len(keys)])
        
        return jsonify({
            'success': True,
            'keys': keys[:limit],
            'total_found': len(keys),
            'limit_applied': limit
        })
        
    except Exception as e:
        logger.error(f"Cache keys error: {e}")
        return jsonify({
            'success': False,
            'error': 'Failed to retrieve cache keys'
        }), 500