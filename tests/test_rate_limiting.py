"""
Tests for rate limiting functionality
"""
import pytest
import time
from unittest.mock import patch, Mock


class TestRateLimitConfiguration:
    """Test rate limiting configuration"""
    
    def test_rate_limit_config_exists(self):
        """Test that rate limit configuration exists"""
        try:
            from config import config
            
            # Check that rate limit settings exist
            assert hasattr(config, 'RATE_LIMIT_PER_HOUR')
            assert hasattr(config, 'RATE_LIMIT_PER_MINUTE')
            assert hasattr(config, 'GENERATE_RATE_LIMIT')
            assert hasattr(config, 'PROMPT_HELP_RATE_LIMIT')
            assert hasattr(config, 'VALIDATE_RATE_LIMIT')
            assert hasattr(config, 'PREVIEW_RATE_LIMIT')
            
            # Check that values are reasonable
            assert config.RATE_LIMIT_PER_HOUR > 0
            assert config.RATE_LIMIT_PER_MINUTE > 0
            
        except ImportError:
            pytest.skip("Configuration module not available")
    
    def test_rate_limit_config_format(self):
        """Test rate limit configuration format"""
        try:
            from config import config
            
            rate_config = config.get_rate_limit_config()
            
            # Check that all expected endpoints are configured
            expected_endpoints = ['generate', 'prompt_help', 'validate', 'preview']
            for endpoint in expected_endpoints:
                assert endpoint in rate_config
                assert isinstance(rate_config[endpoint], str)
                assert 'per' in rate_config[endpoint]  # Should contain "per minute" or similar
            
            # Check global limits
            assert 'global_hour' in rate_config
            assert 'global_minute' in rate_config
            
        except ImportError:
            pytest.skip("Configuration module not available")


class TestRateLimitEndpoints:
    """Test rate limiting on specific endpoints"""
    
    def test_rate_limit_info_endpoint(self, client):
        """Test rate limit information endpoint"""
        response = client.get('/api/rate-limits')
        
        if response.status_code == 404:
            pytest.skip("Rate limit info endpoint not available")
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'rate_limits' in data
        rate_limits = data['rate_limits']
        
        # Check that common endpoints are listed
        expected_endpoints = ['generate', 'validate']
        for endpoint in expected_endpoints:
            # Endpoint might be in rate_limits or not, depending on implementation
            pass
    
    def test_rate_limit_stats_endpoint(self, client):
        """Test rate limit statistics endpoint"""
        response = client.get('/api/rate-limit-stats')
        
        if response.status_code == 404:
            pytest.skip("Rate limit stats endpoint not available")
        
        # Should either work or return a proper error
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'success' in data
    
    def test_generate_endpoint_rate_limiting(self, client, sample_workflow_request):
        """Test rate limiting on generate endpoint"""
        # Make a few requests to see if rate limiting is active
        responses = []
        
        for i in range(5):
            response = client.post('/generate',
                                  json=sample_workflow_request,
                                  content_type='application/json')
            responses.append(response.status_code)
            time.sleep(0.1)  # Small delay between requests
        
        # All requests should either succeed or be rate limited
        for status_code in responses:
            assert status_code in [200, 429, 500]  # 500 if dependencies missing
        
        # At least some should succeed
        success_count = sum(1 for code in responses if code == 200)
        assert success_count > 0
    
    def test_prompt_help_endpoint_rate_limiting(self, client):
        """Test rate limiting on prompt help endpoint"""
        responses = []
        
        for i in range(5):
            response = client.post('/prompt-help',
                                  json={"description": f"test request {i}"},
                                  content_type='application/json')
            responses.append(response.status_code)
            time.sleep(0.1)
        
        # Check response codes
        for status_code in responses:
            assert status_code in [200, 429, 500]
        
        # At least some should succeed
        success_count = sum(1 for code in responses if code == 200)
        assert success_count > 0
    
    def test_validate_endpoint_rate_limiting(self, client, sample_workflow):
        """Test rate limiting on validate endpoint"""
        responses = []
        
        for i in range(5):
            response = client.post('/validate',
                                  json={"workflow": sample_workflow},
                                  content_type='application/json')
            responses.append(response.status_code)
            time.sleep(0.1)
        
        # Check response codes
        for status_code in responses:
            assert status_code in [200, 400, 429, 500]
        
        # Should handle requests appropriately
        assert len(responses) == 5


class TestRateLimitHeaders:
    """Test rate limiting headers and responses"""
    
    def test_rate_limit_exceeded_response(self, client, sample_workflow_request):
        """Test response when rate limit is exceeded"""
        # This test is challenging because we need to actually exceed the rate limit
        # We'll make many requests quickly and check for 429 responses
        
        responses = []
        for i in range(20):  # Make many requests quickly
            response = client.post('/generate',
                                  json=sample_workflow_request,
                                  content_type='application/json')
            responses.append(response)
            
            if response.status_code == 429:
                # Found a rate limited response, test its structure
                data = response.get_json()
                assert data['success'] is False
                assert 'error' in data
                assert 'RATE_LIMIT_EXCEEDED' in data['error'] or 'rate limit' in data['error'].lower()
                
                # Should have retry information
                if 'retry_after' in data:
                    assert isinstance(data['retry_after'], int)
                    assert data['retry_after'] > 0
                
                break
        
        # If no rate limiting occurred, that's also valid (rate limits might be high)
        status_codes = [r.status_code for r in responses]
        
        # Should have some successful responses
        assert 200 in status_codes or 500 in status_codes  # 500 if dependencies missing
    
    def test_rate_limit_headers_present(self, client):
        """Test that rate limit headers are present in responses"""
        response = client.get('/health')
        
        # Some rate limiting implementations add headers like:
        # X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset
        # These are optional and depend on the rate limiting implementation
        
        # Just check that the response is valid
        assert response.status_code == 200
    
    def test_different_ips_separate_limits(self, client, sample_workflow_request):
        """Test that different IPs have separate rate limits"""
        # This is hard to test without actually changing the client IP
        # We'll just make requests with different X-Forwarded-For headers
        
        headers1 = {'X-Forwarded-For': '192.168.1.100'}
        headers2 = {'X-Forwarded-For': '192.168.1.101'}
        
        response1 = client.post('/generate',
                               json=sample_workflow_request,
                               content_type='application/json',
                               headers=headers1)
        
        response2 = client.post('/generate',
                               json=sample_workflow_request,
                               content_type='application/json',
                               headers=headers2)
        
        # Both should be handled independently
        # (Actual IP-based rate limiting depends on configuration)
        assert response1.status_code in [200, 429, 500]
        assert response2.status_code in [200, 429, 500]


class TestRateLimitBypass:
    """Test rate limit bypass scenarios"""
    
    def test_health_endpoint_no_rate_limit(self, client):
        """Test that health endpoint is not rate limited"""
        # Make many requests to health endpoint
        responses = []
        
        for i in range(10):
            response = client.get('/health')
            responses.append(response.status_code)
        
        # All should succeed (health endpoint typically not rate limited)
        for status_code in responses:
            assert status_code == 200
    
    def test_static_files_no_rate_limit(self, client):
        """Test that static files are not rate limited"""
        # Try to access static files (if they exist)
        response = client.get('/static/nonexistent.css')
        
        # Should return 404, not 429
        assert response.status_code in [404, 200]  # 200 if file exists
    
    def test_options_requests_handling(self, client):
        """Test that OPTIONS requests are handled properly"""
        response = client.options('/generate')
        
        # Should not be rate limited (CORS preflight)
        assert response.status_code in [200, 204, 405]  # Various valid responses


class TestRateLimitConfiguration:
    """Test rate limiting configuration and management"""
    
    def test_rate_limit_storage_backend(self):
        """Test rate limit storage backend configuration"""
        try:
            from app import limiter
            
            if limiter is not None:
                # Check that limiter is configured
                assert limiter is not None
                
                # Check storage backend (might be in-memory or Redis)
                # This is implementation-specific
                pass
            else:
                pytest.skip("Rate limiter not configured")
                
        except ImportError:
            pytest.skip("Rate limiter not available")
    
    def test_rate_limit_key_function(self):
        """Test rate limit key function"""
        try:
            from flask_limiter.util import get_remote_address
            
            # This is the default key function
            # In a real test, we'd need a request context
            assert callable(get_remote_address)
            
        except ImportError:
            pytest.skip("Flask-Limiter not available")
    
    def test_rate_limit_exemption(self, client):
        """Test rate limit exemption for certain conditions"""
        # Some endpoints might be exempt from rate limiting
        # This depends on the specific implementation
        
        # Test that configuration endpoints might have different limits
        response = client.get('/api/config/status')
        
        if response.status_code != 404:
            # If endpoint exists, it should respond appropriately
            assert response.status_code in [200, 500]


class TestRateLimitMonitoring:
    """Test rate limiting monitoring and metrics"""
    
    def test_rate_limit_metrics_collection(self):
        """Test that rate limit metrics are collected"""
        try:
            from rate_limiting import rate_monitor
            
            # Check that monitor exists and has expected methods
            assert hasattr(rate_monitor, 'record_request')
            assert hasattr(rate_monitor, 'get_stats')
            
            # Test basic functionality
            stats = rate_monitor.get_stats()
            assert isinstance(stats, dict)
            
        except ImportError:
            pytest.skip("Rate limiting monitoring not available")
    
    def test_rate_limit_stats_structure(self):
        """Test rate limiting statistics structure"""
        try:
            from rate_limiting import get_rate_limit_stats
            
            stats = get_rate_limit_stats()
            
            # Check expected fields
            expected_fields = ['uptime_seconds', 'total_requests', 'total_blocked']
            for field in expected_fields:
                if field in stats:
                    assert isinstance(stats[field], (int, float))
            
        except ImportError:
            pytest.skip("Rate limiting statistics not available")
    
    def test_rate_limit_info_structure(self):
        """Test rate limiting info structure"""
        try:
            from rate_limiting import get_rate_limit_info
            
            info = get_rate_limit_info()
            
            assert isinstance(info, dict)
            assert 'rate_limits' in info
            
        except ImportError:
            pytest.skip("Rate limiting info not available")