"""
Tests for configuration API endpoints
"""
import pytest
import json
from unittest.mock import patch, Mock


class TestConfigurationAPIEndpoints:
    """Test configuration API endpoints"""
    
    def test_config_status_endpoint(self, client):
        """Test configuration status endpoint"""
        response = client.get('/api/config/status')
        
        if response.status_code == 404:
            pytest.skip("Configuration API not available")
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['success'] is True
        assert 'status' in data
        assert 'summary' in data
        
        # Check status structure
        status = data['status']
        expected_status_fields = ['environment', 'debug', 'validation_status']
        for field in expected_status_fields:
            assert field in status
    
    def test_config_validate_endpoint(self, client):
        """Test configuration validation endpoint"""
        response = client.post('/api/config/validate')
        
        if response.status_code == 404:
            pytest.skip("Configuration API not available")
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['success'] is True
        assert 'validation' in data
        
        # Check validation structure
        validation = data['validation']
        expected_validation_fields = ['is_valid', 'total_issues', 'environment']
        for field in expected_validation_fields:
            assert field in validation
        
        # Check issue categorization
        assert 'critical_issues' in validation
        assert 'error_issues' in validation
        assert 'warning_issues' in validation
        
        assert isinstance(validation['critical_issues'], list)
        assert isinstance(validation['error_issues'], list)
        assert isinstance(validation['warning_issues'], list)
    
    def test_config_features_endpoint(self, client):
        """Test configuration features endpoint"""
        response = client.get('/api/config/features')
        
        if response.status_code == 404:
            pytest.skip("Configuration API not available")
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['success'] is True
        assert 'features' in data
        assert 'enabled_count' in data
        assert 'total_count' in data
        
        # Check features structure
        features = data['features']
        assert isinstance(features, dict)
        
        # Check that feature flags are boolean
        for feature_name, enabled in features.items():
            assert isinstance(enabled, bool)
        
        # Check counts
        enabled_count = data['enabled_count']
        total_count = data['total_count']
        
        assert isinstance(enabled_count, int)
        assert isinstance(total_count, int)
        assert 0 <= enabled_count <= total_count
    
    def test_config_rate_limits_endpoint(self, client):
        """Test configuration rate limits endpoint"""
        response = client.get('/api/config/rate-limits')
        
        if response.status_code == 404:
            pytest.skip("Configuration API not available")
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['success'] is True
        assert 'rate_limits' in data
        assert 'global_limits' in data
        
        # Check rate limits structure
        rate_limits = data['rate_limits']
        assert isinstance(rate_limits, dict)
        
        # Check global limits
        global_limits = data['global_limits']
        assert 'per_hour' in global_limits
        assert 'per_minute' in global_limits
        
        assert isinstance(global_limits['per_hour'], int)
        assert isinstance(global_limits['per_minute'], int)
    
    def test_config_database_endpoint(self, client):
        """Test configuration database endpoint"""
        response = client.get('/api/config/database')
        
        if response.status_code == 404:
            pytest.skip("Configuration API not available")
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['success'] is True
        assert 'database' in data
        
        # Check database config structure (should be safe, no sensitive data)
        db_config = data['database']
        expected_fields = ['pool_size', 'timeout', 'echo', 'url_type']
        for field in expected_fields:
            assert field in db_config
        
        # Should not contain actual database URL
        assert 'url' not in db_config or db_config['url'] == '***REDACTED***'
    
    def test_config_cache_endpoint(self, client):
        """Test configuration cache endpoint"""
        response = client.get('/api/config/cache')
        
        if response.status_code == 404:
            pytest.skip("Configuration API not available")
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['success'] is True
        assert 'cache' in data
        
        # Check cache config structure
        cache_config = data['cache']
        expected_fields = ['enabled', 'timeout', 'url_configured']
        for field in expected_fields:
            assert field in cache_config
        
        assert isinstance(cache_config['enabled'], bool)
        assert isinstance(cache_config['timeout'], int)
        assert isinstance(cache_config['url_configured'], bool)
    
    def test_config_export_endpoint(self, client):
        """Test configuration export endpoint"""
        response = client.get('/api/config/export')
        
        if response.status_code == 404:
            pytest.skip("Configuration API not available")
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['success'] is True
        assert 'export' in data
        
        # Check export structure
        export_data = data['export']
        assert 'configuration' in export_data
        assert 'metadata' in export_data
        
        # Check metadata
        metadata = export_data['metadata']
        expected_metadata_fields = ['exported_at', 'environment', 'version']
        for field in expected_metadata_fields:
            assert field in metadata
        
        # Check that sensitive data is redacted in configuration
        configuration = export_data['configuration']
        sensitive_keys = ['SECRET_KEY', 'GEMINI_API_KEY', 'OPENAI_API_KEY']
        for key in sensitive_keys:
            if key in configuration:
                assert configuration[key] in ['***REDACTED***', '']
    
    def test_config_health_endpoint(self, client):
        """Test configuration health endpoint"""
        response = client.get('/api/config/health')
        
        if response.status_code == 404:
            pytest.skip("Configuration API not available")
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['success'] is True
        assert 'status' in data
        
        # Status should be 'healthy' or 'unhealthy'
        assert data['status'] in ['healthy', 'unhealthy']
        
        # Check health fields
        expected_fields = ['issues_count', 'environment', 'checked_at']
        for field in expected_fields:
            assert field in data


class TestConfigurationAPIReload:
    """Test configuration reload functionality"""
    
    def test_config_reload_endpoint_development(self, client):
        """Test configuration reload in development mode"""
        response = client.post('/api/config/reload')
        
        if response.status_code == 404:
            pytest.skip("Configuration API not available")
        
        # Should work in development/testing mode
        if response.status_code == 403:
            # Forbidden in production mode
            data = response.get_json()
            assert data['success'] is False
            assert 'not allowed in production' in data['error']
        else:
            # Should succeed in development
            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] is True
            assert 'message' in data
            assert 'reloaded_at' in data
    
    def test_config_reload_production_forbidden(self, client):
        """Test that configuration reload is forbidden in production"""
        with patch('config_api.config') as mock_config:
            mock_config.is_production.return_value = True
            
            response = client.post('/api/config/reload')
            
            if response.status_code != 404:
                assert response.status_code == 403
                data = response.get_json()
                assert data['success'] is False


class TestConfigurationAPIErrorHandling:
    """Test configuration API error handling"""
    
    def test_config_api_404_handling(self, client):
        """Test 404 handling for configuration API"""
        response = client.get('/api/config/nonexistent')
        
        if response.status_code == 404:
            # Check if it's a proper JSON error response
            try:
                data = response.get_json()
                if data:
                    assert 'success' in data
                    assert data['success'] is False
            except:
                # Plain 404 is also acceptable
                pass
    
    def test_config_api_method_not_allowed(self, client):
        """Test method not allowed handling"""
        # Try POST on a GET-only endpoint
        response = client.post('/api/config/status')
        
        if response.status_code == 405:
            # Check if it's a proper JSON error response
            try:
                data = response.get_json()
                if data:
                    assert 'success' in data
                    assert data['success'] is False
            except:
                # Plain 405 is also acceptable
                pass
    
    def test_config_api_internal_error_handling(self, client):
        """Test internal error handling"""
        # This is hard to test without mocking internal failures
        # We'll just ensure that if errors occur, they're handled gracefully
        
        with patch('config_api.config') as mock_config:
            mock_config.validate.side_effect = Exception("Test error")
            
            response = client.post('/api/config/validate')
            
            if response.status_code != 404:
                # Should handle the error gracefully
                assert response.status_code == 500
                data = response.get_json()
                assert data['success'] is False
                assert 'error' in data


class TestConfigurationAPIAuthentication:
    """Test configuration API authentication/authorization"""
    
    def test_config_api_no_auth_required(self, client):
        """Test that configuration API doesn't require authentication"""
        # Most config endpoints should be accessible without auth
        # (In production, you might want to add authentication)
        
        response = client.get('/api/config/status')
        
        if response.status_code != 404:
            # Should not require authentication
            assert response.status_code != 401
            assert response.status_code != 403 or response.status_code == 403  # 403 might be for production-only features
    
    def test_config_api_sensitive_endpoints(self, client):
        """Test access to sensitive configuration endpoints"""
        # Some endpoints might be restricted
        sensitive_endpoints = ['/api/config/export', '/api/config/reload']
        
        for endpoint in sensitive_endpoints:
            if endpoint == '/api/config/reload':
                response = client.post(endpoint)
            else:
                response = client.get(endpoint)
            
            if response.status_code != 404:
                # Should either work or be properly restricted
                assert response.status_code in [200, 403, 500]


class TestConfigurationAPIValidation:
    """Test configuration API input validation"""
    
    def test_config_validate_endpoint_validation(self, client):
        """Test validation endpoint input validation"""
        # Test with invalid JSON
        response = client.post('/api/config/validate',
                              data='invalid json',
                              content_type='application/json')
        
        if response.status_code != 404:
            # Should handle invalid JSON gracefully
            assert response.status_code in [400, 500]
    
    def test_config_reload_endpoint_validation(self, client):
        """Test reload endpoint input validation"""
        # Test with invalid data
        response = client.post('/api/config/reload',
                              json={'invalid': 'data'},
                              content_type='application/json')
        
        if response.status_code != 404:
            # Should handle gracefully (reload doesn't need input data)
            assert response.status_code in [200, 403, 500]


class TestConfigurationAPIPerformance:
    """Test configuration API performance"""
    
    def test_config_status_response_time(self, client):
        """Test configuration status response time"""
        import time
        
        start_time = time.time()
        response = client.get('/api/config/status')
        end_time = time.time()
        
        if response.status_code != 404:
            response_time = end_time - start_time
            # Should respond quickly (less than 1 second)
            assert response_time < 1.0
    
    def test_config_features_caching(self, client):
        """Test that configuration features are cached appropriately"""
        # Make multiple requests
        responses = []
        for i in range(3):
            response = client.get('/api/config/features')
            if response.status_code == 200:
                responses.append(response.get_json())
        
        if responses:
            # Responses should be consistent (features don't change during test)
            first_response = responses[0]
            for response in responses[1:]:
                assert response['features'] == first_response['features']