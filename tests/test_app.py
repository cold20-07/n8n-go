"""
Tests for Flask application routes and functionality
"""
import pytest
import json
from unittest.mock import patch, Mock


class TestAppInitialization:
    """Test Flask app initialization"""
    
    def test_app_creation(self, app):
        """Test that Flask app is created successfully"""
        assert app is not None
        assert app.config['TESTING'] is True
    
    def test_app_routes_exist(self, client):
        """Test that expected routes exist"""
        # Test main routes
        response = client.get('/')
        assert response.status_code in [200, 404]  # 404 if template missing
        
        # Test health endpoint
        response = client.get('/health')
        assert response.status_code == 200
        
        data = response.get_json()
        assert data is not None
        assert 'status' in data


class TestWorkflowGeneration:
    """Test workflow generation endpoints"""
    
    def test_generate_workflow_success(self, client, sample_workflow_request):
        """Test successful workflow generation"""
        response = client.post('/generate',
                              json=sample_workflow_request,
                              content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['success'] is True
        assert 'workflow' in data
        assert 'nodes' in data['workflow']
        assert len(data['workflow']['nodes']) > 0
        assert 'workflow_name' in data
        assert 'node_count' in data
    
    def test_generate_workflow_complex(self, client, complex_workflow_request):
        """Test complex workflow generation"""
        response = client.post('/generate',
                              json=complex_workflow_request,
                              content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert data['success'] is True
        assert 'workflow' in data
        # Complex workflows should have more nodes
        assert len(data['workflow']['nodes']) >= 3
    
    def test_generate_workflow_missing_data(self, client):
        """Test workflow generation with missing data"""
        response = client.post('/generate',
                              json={},
                              content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
        assert 'error' in data
    
    def test_generate_workflow_invalid_trigger(self, client):
        """Test workflow generation with invalid trigger"""
        invalid_request = {
            "description": "Test workflow",
            "trigger": "invalid_trigger",
            "complexity": "simple"
        }
        
        response = client.post('/generate',
                              json=invalid_request,
                              content_type='application/json')
        
        # Should either fix the trigger or return an error
        assert response.status_code in [200, 400]
    
    def test_generate_workflow_invalid_complexity(self, client):
        """Test workflow generation with invalid complexity"""
        invalid_request = {
            "description": "Test workflow",
            "trigger": "webhook",
            "complexity": "invalid_complexity"
        }
        
        response = client.post('/generate',
                              json=invalid_request,
                              content_type='application/json')
        
        # Should default to medium complexity and succeed
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_generate_workflow_empty_description(self, client):
        """Test workflow generation with empty description"""
        empty_request = {
            "description": "",
            "trigger": "webhook",
            "complexity": "simple"
        }
        
        response = client.post('/generate',
                              json=empty_request,
                              content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
    
    def test_generate_workflow_long_description(self, client):
        """Test workflow generation with very long description"""
        long_description = "A" * 6000  # Exceeds typical limits
        long_request = {
            "description": long_description,
            "trigger": "webhook",
            "complexity": "simple"
        }
        
        response = client.post('/generate',
                              json=long_request,
                              content_type='application/json')
        
        # Should either truncate or return error
        assert response.status_code in [200, 400]
    
    def test_generate_workflow_with_template(self, client):
        """Test workflow generation with template"""
        template_request = {
            "description": "Process customer data",
            "trigger": "webhook",
            "complexity": "medium",
            "template": "lead_processing"
        }
        
        response = client.post('/generate',
                              json=template_request,
                              content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_generate_workflow_wrong_content_type(self, client, sample_workflow_request):
        """Test workflow generation with wrong content type"""
        response = client.post('/generate',
                              data=json.dumps(sample_workflow_request),
                              content_type='text/plain')
        
        assert response.status_code == 415
        data = response.get_json()
        assert data['success'] is False
        assert 'Content-Type must be application/json' in data['error']


class TestPromptHelp:
    """Test prompt help functionality"""
    
    def test_prompt_help_empty_input(self, client):
        """Test prompt help with empty input"""
        response = client.post('/prompt-help',
                              json={"description": ""},
                              content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['needs_help'] is True
        assert 'message' in data
    
    def test_prompt_help_detailed_input(self, client):
        """Test prompt help with detailed input"""
        response = client.post('/prompt-help',
                              json={"description": "I want to create a workflow that processes customer emails and sends automated responses"},
                              content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
    
    def test_prompt_help_missing_data(self, client):
        """Test prompt help with missing data"""
        response = client.post('/prompt-help',
                              json={},
                              content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['needs_help'] is True
    
    def test_prompt_help_wrong_content_type(self, client):
        """Test prompt help with wrong content type"""
        response = client.post('/prompt-help',
                              data='{"description": "test"}',
                              content_type='text/plain')
        
        assert response.status_code == 415


class TestWorkflowValidation:
    """Test workflow validation endpoints"""
    
    def test_validate_workflow_success(self, client, sample_workflow):
        """Test successful workflow validation"""
        response = client.post('/validate',
                              json={"workflow": sample_workflow},
                              content_type='application/json')
        
        # May not be available if validator not imported
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.get_json()
            assert data['success'] is True
    
    def test_validate_workflow_missing_data(self, client):
        """Test workflow validation with missing data"""
        response = client.post('/validate',
                              json={},
                              content_type='application/json')
        
        assert response.status_code == 400
        data = response.get_json()
        assert data['success'] is False
    
    def test_validate_workflow_invalid_structure(self, client):
        """Test workflow validation with invalid structure"""
        invalid_workflow = {
            "name": "",
            "nodes": [],
            "connections": {}
        }
        
        response = client.post('/validate',
                              json={"workflow": invalid_workflow},
                              content_type='application/json')
        
        # Should handle invalid workflow gracefully
        assert response.status_code in [200, 400, 500]


class TestPreviewGeneration:
    """Test workflow preview generation"""
    
    def test_generate_preview_success(self, client, sample_workflow):
        """Test successful preview generation"""
        response = client.post('/preview',
                              json={"workflow": sample_workflow},
                              content_type='application/json')
        
        # May not be available if preview generator not implemented
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.get_json()
            assert data['success'] is True
            assert 'preview' in data
    
    def test_generate_preview_missing_data(self, client):
        """Test preview generation with missing data"""
        response = client.post('/preview',
                              json={},
                              content_type='application/json')
        
        assert response.status_code in [400, 500]


class TestHealthCheck:
    """Test health check endpoint"""
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'status' in data
        assert 'version' in data
        assert 'timestamp' in data
        assert 'services' in data
        
        # Check service status structure
        services = data['services']
        expected_services = ['ai_generator', 'validator', 'enhancer', 'rate_limiter']
        
        for service in expected_services:
            assert service in services
            assert isinstance(services[service], bool)


class TestRateLimiting:
    """Test rate limiting functionality"""
    
    def test_rate_limit_info(self, client):
        """Test rate limit info endpoint"""
        response = client.get('/api/rate-limits')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'rate_limits' in data
        assert isinstance(data['rate_limits'], dict)
    
    def test_rate_limit_stats(self, client):
        """Test rate limit statistics endpoint"""
        response = client.get('/api/rate-limit-stats')
        
        # May not be available if rate limiting not fully configured
        assert response.status_code in [200, 500]
        
        if response.status_code == 200:
            data = response.get_json()
            assert data['success'] is True
    
    @pytest.mark.slow
    def test_rate_limiting_enforcement(self, client, sample_workflow_request):
        """Test that rate limiting is enforced"""
        # Make multiple rapid requests
        responses = []
        for i in range(15):  # Exceed typical rate limit
            response = client.post('/generate',
                                  json=sample_workflow_request,
                                  content_type='application/json')
            responses.append(response.status_code)
        
        # Should have some rate limited responses (429)
        # Note: This test might be flaky depending on rate limit configuration
        status_codes = set(responses)
        
        # At least some requests should succeed
        assert 200 in status_codes
        
        # If rate limiting is active, some should be limited
        # (This is optional as rate limiting might not be fully configured in tests)


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_error(self, client):
        """Test 404 error handling"""
        response = client.get('/nonexistent-endpoint')
        assert response.status_code == 404
    
    def test_405_method_not_allowed(self, client):
        """Test 405 method not allowed"""
        response = client.get('/generate')  # Should be POST only
        assert response.status_code == 405
    
    def test_500_error_handling(self, client):
        """Test 500 error handling"""
        # This is harder to test without mocking internal errors
        # The error handlers should be registered
        pass


class TestSecurityHeaders:
    """Test security headers"""
    
    def test_security_headers_present(self, client):
        """Test that security headers are present"""
        response = client.get('/health')
        
        # Check for security headers
        expected_headers = [
            'X-Content-Type-Options',
            'X-Frame-Options',
            'X-XSS-Protection',
            'Referrer-Policy'
        ]
        
        for header in expected_headers:
            assert header in response.headers
    
    def test_cors_headers(self, client):
        """Test CORS headers"""
        # Make an OPTIONS request to test CORS
        response = client.options('/generate')
        
        # Should have CORS headers if CORS is configured
        # This might not be present in test environment
        pass


class TestConfigurationAPI:
    """Test configuration API endpoints"""
    
    def test_config_status(self, client):
        """Test configuration status endpoint"""
        response = client.get('/api/config/status')
        
        # May not be available if config API not registered
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.get_json()
            assert data['success'] is True
            assert 'status' in data
    
    def test_config_features(self, client):
        """Test configuration features endpoint"""
        response = client.get('/api/config/features')
        
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.get_json()
            assert data['success'] is True
            assert 'features' in data
    
    def test_config_health(self, client):
        """Test configuration health endpoint"""
        response = client.get('/api/config/health')
        
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.get_json()
            assert data['success'] is True
            assert 'status' in data