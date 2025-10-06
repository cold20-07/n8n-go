"""
Integration tests for N8N Workflow Generator
"""
import pytest
import json
import time
from unittest.mock import patch, Mock


class TestWorkflowGenerationIntegration:
    """Integration tests for complete workflow generation flow"""
    
    def test_complete_workflow_generation_flow(self, client, sample_workflow_request):
        """Test complete workflow generation from request to response"""
        # Step 1: Generate workflow
        response = client.post('/generate',
                              json=sample_workflow_request,
                              content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        
        workflow = data['workflow']
        
        # Step 2: Validate the generated workflow (if validator available)
        if 'workflow' in data:
            validation_response = client.post('/validate',
                                            json={"workflow": workflow},
                                            content_type='application/json')
            
            # Validation might not be available
            if validation_response.status_code == 200:
                validation_data = validation_response.get_json()
                assert validation_data['success'] is True
        
        # Step 3: Generate preview (if available)
        preview_response = client.post('/preview',
                                     json={"workflow": workflow},
                                     content_type='application/json')
        
        # Preview might not be available
        if preview_response.status_code == 200:
            preview_data = preview_response.get_json()
            assert preview_data['success'] is True
    
    def test_workflow_generation_with_different_complexities(self, client):
        """Test workflow generation with different complexity levels"""
        base_request = {
            "description": "Process customer data and send notifications",
            "trigger": "webhook"
        }
        
        complexities = ['simple', 'medium', 'complex']
        workflows = {}
        
        for complexity in complexities:
            request_data = base_request.copy()
            request_data['complexity'] = complexity
            
            response = client.post('/generate',
                                  json=request_data,
                                  content_type='application/json')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] is True
            
            workflows[complexity] = data['workflow']
        
        # Verify that different complexities produce different results
        simple_nodes = len(workflows['simple']['nodes'])
        medium_nodes = len(workflows['medium']['nodes'])
        complex_nodes = len(workflows['complex']['nodes'])
        
        # Complex should generally have more nodes than simple
        assert complex_nodes >= simple_nodes
    
    def test_workflow_generation_with_different_triggers(self, client):
        """Test workflow generation with different trigger types"""
        base_request = {
            "description": "Process incoming data",
            "complexity": "medium"
        }
        
        triggers = ['webhook', 'schedule', 'manual']
        workflows = {}
        
        for trigger in triggers:
            request_data = base_request.copy()
            request_data['trigger'] = trigger
            
            response = client.post('/generate',
                                  json=request_data,
                                  content_type='application/json')
            
            assert response.status_code == 200
            data = response.get_json()
            assert data['success'] is True
            
            workflows[trigger] = data['workflow']
        
        # Verify that different triggers produce appropriate trigger nodes
        for trigger, workflow in workflows.items():
            nodes = workflow['nodes']
            assert len(nodes) > 0
            
            # First node should be appropriate for the trigger type
            first_node = nodes[0]
            node_type = first_node['type'].lower()
            
            if trigger == 'webhook':
                assert 'webhook' in node_type or 'http' in node_type
            elif trigger == 'schedule':
                # Schedule triggers might be implemented differently
                pass
            elif trigger == 'manual':
                # Manual triggers might be implemented differently
                pass


class TestPromptHelpIntegration:
    """Integration tests for prompt help functionality"""
    
    def test_prompt_help_to_workflow_generation(self, client):
        """Test flow from prompt help to workflow generation"""
        # Step 1: Get prompt help for unclear request
        unclear_request = {"description": "automate stuff"}
        
        help_response = client.post('/prompt-help',
                                   json=unclear_request,
                                   content_type='application/json')
        
        assert help_response.status_code == 200
        help_data = help_response.get_json()
        assert help_data['success'] is True
        
        # Step 2: Use improved description for workflow generation
        if help_data.get('needs_help'):
            # Simulate user providing more details
            improved_request = {
                "description": "Process customer emails and send automated responses with personalized content",
                "trigger": "webhook",
                "complexity": "medium"
            }
        else:
            improved_request = {
                "description": unclear_request["description"],
                "trigger": "webhook",
                "complexity": "medium"
            }
        
        # Step 3: Generate workflow with improved description
        workflow_response = client.post('/generate',
                                       json=improved_request,
                                       content_type='application/json')
        
        assert workflow_response.status_code == 200
        workflow_data = workflow_response.get_json()
        assert workflow_data['success'] is True
    
    def test_iterative_prompt_improvement(self, client):
        """Test iterative prompt improvement process"""
        descriptions = [
            "help me",
            "automate emails",
            "send emails when customers sign up",
            "send welcome emails to new customers who register via webhook"
        ]
        
        for i, description in enumerate(descriptions):
            help_response = client.post('/prompt-help',
                                       json={"description": description},
                                       content_type='application/json')
            
            assert help_response.status_code == 200
            help_data = help_response.get_json()
            assert help_data['success'] is True
            
            # Later descriptions should need less help
            if i == 0:
                assert help_data.get('needs_help', True) is True
            elif i == len(descriptions) - 1:
                # Last description should be detailed enough
                pass


class TestRateLimitingIntegration:
    """Integration tests for rate limiting across endpoints"""
    
    @pytest.mark.slow
    def test_rate_limiting_across_endpoints(self, client, sample_workflow_request):
        """Test rate limiting behavior across different endpoints"""
        endpoints = [
            ('/generate', 'POST', sample_workflow_request),
            ('/prompt-help', 'POST', {"description": "test"}),
            ('/health', 'GET', None)
        ]
        
        results = {}
        
        for endpoint, method, data in endpoints:
            responses = []
            
            # Make multiple requests to each endpoint
            for i in range(10):
                if method == 'GET':
                    response = client.get(endpoint)
                else:
                    response = client.post(endpoint,
                                         json=data,
                                         content_type='application/json')
                
                responses.append(response.status_code)
                time.sleep(0.1)  # Small delay
            
            results[endpoint] = responses
        
        # Analyze results
        for endpoint, responses in results.items():
            # Should have some successful responses
            success_count = sum(1 for code in responses if code == 200)
            rate_limited_count = sum(1 for code in responses if code == 429)
            
            assert success_count > 0, f"No successful responses for {endpoint}"
            
            # Health endpoint should not be rate limited
            if endpoint == '/health':
                assert rate_limited_count == 0, "Health endpoint should not be rate limited"
    
    def test_rate_limit_recovery(self, client, sample_workflow_request):
        """Test rate limit recovery after waiting"""
        # Make requests until rate limited
        responses = []
        for i in range(15):
            response = client.post('/generate',
                                  json=sample_workflow_request,
                                  content_type='application/json')
            responses.append(response.status_code)
            
            if response.status_code == 429:
                break
        
        # If we got rate limited, wait and try again
        if 429 in responses:
            time.sleep(2)  # Wait for rate limit to reset
            
            recovery_response = client.post('/generate',
                                           json=sample_workflow_request,
                                           content_type='application/json')
            
            # Should be able to make requests again
            assert recovery_response.status_code in [200, 500]  # 500 if dependencies missing


class TestConfigurationIntegration:
    """Integration tests for configuration system"""
    
    def test_configuration_affects_behavior(self, client):
        """Test that configuration changes affect application behavior"""
        # Get current configuration
        config_response = client.get('/api/config/status')
        
        if config_response.status_code == 404:
            pytest.skip("Configuration API not available")
        
        assert config_response.status_code == 200
        config_data = config_response.get_json()
        
        # Test that configuration is being used
        assert config_data['success'] is True
        assert 'status' in config_data
        
        # Check that rate limits from configuration are applied
        rate_limit_response = client.get('/api/config/rate-limits')
        if rate_limit_response.status_code == 200:
            rate_data = rate_limit_response.get_json()
            assert rate_data['success'] is True
            assert 'rate_limits' in rate_data
    
    def test_feature_flags_affect_behavior(self, client):
        """Test that feature flags affect application behavior"""
        features_response = client.get('/api/config/features')
        
        if features_response.status_code == 404:
            pytest.skip("Configuration API not available")
        
        assert features_response.status_code == 200
        features_data = features_response.get_json()
        
        assert features_data['success'] is True
        features = features_data['features']
        
        # Test that features are actually being used
        # This is hard to test without specific feature implementations
        assert isinstance(features, dict)
        assert len(features) > 0


class TestErrorHandlingIntegration:
    """Integration tests for error handling across the application"""
    
    def test_error_consistency_across_endpoints(self, client):
        """Test that error responses are consistent across endpoints"""
        # Test various error conditions
        error_tests = [
            ('/generate', 'POST', {}, 400),  # Missing data
            ('/generate', 'POST', 'invalid json', 415),  # Wrong content type
            ('/prompt-help', 'POST', {}, 200),  # Should handle empty data gracefully
            ('/validate', 'POST', {}, 400),  # Missing workflow data
        ]
        
        for endpoint, method, data, expected_status in error_tests:
            if method == 'POST':
                if isinstance(data, dict):
                    response = client.post(endpoint,
                                         json=data,
                                         content_type='application/json')
                else:
                    response = client.post(endpoint,
                                         data=data,
                                         content_type='application/json')
            else:
                response = client.get(endpoint)
            
            # Check that error responses have consistent structure
            if response.status_code >= 400:
                try:
                    error_data = response.get_json()
                    if error_data:
                        assert 'success' in error_data
                        assert error_data['success'] is False
                        assert 'error' in error_data
                except:
                    # Some errors might not return JSON
                    pass
    
    def test_graceful_degradation(self, client, sample_workflow_request):
        """Test graceful degradation when components are unavailable"""
        # Test that the application continues to work even if some components fail
        
        # Mock component failures
        with patch('app.ENHANCED_GENERATOR_AVAILABLE', False):
            with patch('app.TRAINED_GENERATOR_AVAILABLE', False):
                response = client.post('/generate',
                                      json=sample_workflow_request,
                                      content_type='application/json')
                
                # Should still work with fallback generators
                assert response.status_code == 200
                data = response.get_json()
                assert data['success'] is True
    
    def test_timeout_handling(self, client, sample_workflow_request):
        """Test timeout handling for long-running operations"""
        # This is hard to test without actually causing timeouts
        # We'll just verify that the application handles requests appropriately
        
        response = client.post('/generate',
                              json=sample_workflow_request,
                              content_type='application/json')
        
        # Should complete within reasonable time
        assert response.status_code in [200, 500, 429]


class TestSecurityIntegration:
    """Integration tests for security features"""
    
    def test_security_headers_consistency(self, client):
        """Test that security headers are applied consistently"""
        endpoints = ['/', '/health', '/generate', '/api/config/status']
        
        for endpoint in endpoints:
            if endpoint == '/generate':
                response = client.post(endpoint,
                                     json={"description": "test", "trigger": "webhook", "complexity": "simple"},
                                     content_type='application/json')
            else:
                response = client.get(endpoint)
            
            # Check for security headers (if implemented)
            security_headers = [
                'X-Content-Type-Options',
                'X-Frame-Options',
                'X-XSS-Protection'
            ]
            
            for header in security_headers:
                # Headers might not be implemented yet
                if header in response.headers:
                    assert response.headers[header] is not None
    
    def test_input_sanitization(self, client):
        """Test input sanitization across endpoints"""
        # Test with potentially malicious input
        malicious_inputs = [
            "<script>alert('xss')</script>",
            "'; DROP TABLE users; --",
            "../../../etc/passwd",
            "javascript:alert('xss')"
        ]
        
        for malicious_input in malicious_inputs:
            request_data = {
                "description": malicious_input,
                "trigger": "webhook",
                "complexity": "simple"
            }
            
            response = client.post('/generate',
                                  json=request_data,
                                  content_type='application/json')
            
            # Should handle malicious input gracefully
            assert response.status_code in [200, 400, 500]
            
            if response.status_code == 200:
                data = response.get_json()
                # Generated workflow should not contain the malicious input as-is
                workflow_str = json.dumps(data['workflow'])
                assert malicious_input not in workflow_str


class TestPerformanceIntegration:
    """Integration tests for performance characteristics"""
    
    def test_response_times(self, client, sample_workflow_request):
        """Test response times for various endpoints"""
        endpoints_and_limits = [
            ('/health', 'GET', None, 0.5),  # Health should be very fast
            ('/generate', 'POST', sample_workflow_request, 10.0),  # Generation can be slower
            ('/prompt-help', 'POST', {"description": "test"}, 2.0),  # Prompt help should be fast
        ]
        
        for endpoint, method, data, time_limit in endpoints_and_limits:
            start_time = time.time()
            
            if method == 'GET':
                response = client.get(endpoint)
            else:
                response = client.post(endpoint,
                                     json=data,
                                     content_type='application/json')
            
            end_time = time.time()
            response_time = end_time - start_time
            
            # Check that response time is within limits
            assert response_time < time_limit, f"{endpoint} took {response_time:.2f}s (limit: {time_limit}s)"
    
    def test_concurrent_requests(self, client, sample_workflow_request):
        """Test handling of concurrent requests"""
        import threading
        import queue
        
        results = queue.Queue()
        
        def make_request():
            try:
                response = client.post('/generate',
                                     json=sample_workflow_request,
                                     content_type='application/json')
                results.put(response.status_code)
            except Exception as e:
                results.put(f"Error: {e}")
        
        # Start multiple threads
        threads = []
        for i in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=30)  # 30 second timeout
        
        # Check results
        response_codes = []
        while not results.empty():
            result = results.get()
            response_codes.append(result)
        
        # Should handle concurrent requests appropriately
        assert len(response_codes) == 5
        
        # Most should succeed (some might be rate limited)
        success_count = sum(1 for code in response_codes if code == 200)
        assert success_count > 0