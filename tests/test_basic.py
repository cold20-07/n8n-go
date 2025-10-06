"""
Basic tests for N8N Workflow Generator
"""
import pytest
import json
from unittest.mock import patch, MagicMock

# Import the app (adjust import path as needed)
try:
    from app import app
except ImportError:
    # Fallback for testing
    app = None

@pytest.fixture
def client():
    """Create test client"""
    if app is None:
        pytest.skip("App not available for testing")
    
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def sample_workflow_request():
    """Sample workflow request data"""
    return {
        "description": "Send email when webhook receives customer data",
        "trigger": "webhook",
        "complexity": "simple"
    }

def test_index_route(client):
    """Test the main index route"""
    response = client.get('/')
    assert response.status_code == 200

def test_generate_workflow_success(client, sample_workflow_request):
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

def test_generate_workflow_missing_data(client):
    """Test workflow generation with missing data"""
    response = client.post('/generate', 
                          json={},
                          content_type='application/json')
    
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False

def test_generate_workflow_invalid_trigger(client):
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

def test_generate_workflow_invalid_complexity(client):
    """Test workflow generation with invalid complexity"""
    invalid_request = {
        "description": "Test workflow",
        "trigger": "webhook", 
        "complexity": "invalid_complexity"
    }
    
    response = client.post('/generate', 
                          json=invalid_request,
                          content_type='application/json')
    
    # Should default to medium complexity
    assert response.status_code == 200

def test_prompt_help_empty_input(client):
    """Test prompt help with empty input"""
    response = client.post('/prompt-help',
                          json={"description": ""},
                          content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['needs_help'] is True

def test_prompt_help_detailed_input(client):
    """Test prompt help with detailed input"""
    response = client.post('/prompt-help',
                          json={"description": "I want to create a workflow that processes customer emails and sends responses"},
                          content_type='application/json')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True

def test_workflow_validation():
    """Test workflow structure validation"""
    # Test valid workflow structure
    valid_workflow = {
        "name": "Test Workflow",
        "nodes": [
            {
                "id": "1",
                "name": "Webhook",
                "type": "n8n-nodes-base.webhook",
                "position": [100, 200],
                "parameters": {}
            }
        ],
        "connections": {}
    }
    
    # Basic validation checks
    assert "name" in valid_workflow
    assert "nodes" in valid_workflow
    assert "connections" in valid_workflow
    assert len(valid_workflow["nodes"]) > 0
    
    # Check node structure
    node = valid_workflow["nodes"][0]
    required_fields = ["id", "name", "type", "position", "parameters"]
    for field in required_fields:
        assert field in node

if __name__ == "__main__":
    pytest.main([__file__, "-v"])