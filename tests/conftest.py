"""
Pytest configuration and fixtures for N8N Workflow Generator tests
"""
import pytest
import os
import tempfile
import json
from pathlib import Path
from unittest.mock import Mock, patch

# Set test environment
os.environ['FLASK_ENV'] = 'testing'
os.environ['DEBUG'] = 'true'
os.environ['SECRET_KEY'] = 'test-secret-key-for-testing-only'
os.environ['GEMINI_API_KEY'] = 'test-gemini-key'

@pytest.fixture
def app():
    """Create Flask app for testing"""
    # Import after setting environment variables
    from app import app as flask_app
    
    flask_app.config.update({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'test-secret-key'
    })
    
    return flask_app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create test CLI runner"""
    return app.test_cli_runner()

@pytest.fixture
def sample_workflow_request():
    """Sample workflow generation request"""
    return {
        "description": "Send email when webhook receives customer data",
        "trigger": "webhook",
        "complexity": "simple"
    }

@pytest.fixture
def complex_workflow_request():
    """Complex workflow generation request"""
    return {
        "description": "Process incoming leads, validate data, enrich with external APIs, send to CRM, and notify sales team via Slack",
        "trigger": "webhook",
        "complexity": "complex"
    }

@pytest.fixture
def invalid_workflow_request():
    """Invalid workflow generation request"""
    return {
        "description": "",
        "trigger": "invalid_trigger",
        "complexity": "invalid_complexity"
    }

@pytest.fixture
def sample_workflow():
    """Sample n8n workflow structure"""
    return {
        "name": "Test Workflow",
        "nodes": [
            {
                "id": "webhook-1",
                "name": "Webhook",
                "type": "n8n-nodes-base.webhook",
                "position": [100, 200],
                "parameters": {
                    "httpMethod": "POST",
                    "path": "test-webhook"
                }
            },
            {
                "id": "email-1",
                "name": "Send Email",
                "type": "n8n-nodes-base.emailSend",
                "position": [300, 200],
                "parameters": {
                    "toEmail": "test@example.com",
                    "subject": "Test Email"
                }
            }
        ],
        "connections": {
            "Webhook": {
                "main": [[{"node": "Send Email", "type": "main", "index": 0}]]
            }
        },
        "active": True
    }

@pytest.fixture
def temp_config_file():
    """Create temporary configuration file"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config_data = {
            "DEBUG": True,
            "SECRET_KEY": "test-secret",
            "MAX_WORKFLOW_NODES": 10
        }
        json.dump(config_data, f)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    os.unlink(temp_path)

@pytest.fixture
def temp_env_file():
    """Create temporary .env file"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.env', delete=False) as f:
        f.write("DEBUG=true\n")
        f.write("SECRET_KEY=test-env-secret\n")
        f.write("MAX_WORKFLOW_NODES=15\n")
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    os.unlink(temp_path)

@pytest.fixture
def mock_gemini_api():
    """Mock Gemini API responses"""
    with patch('requests.post') as mock_post:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [{
                "content": {
                    "parts": [{
                        "text": json.dumps({
                            "name": "AI Generated Workflow",
                            "nodes": [
                                {
                                    "id": "webhook-1",
                                    "name": "Webhook",
                                    "type": "n8n-nodes-base.webhook",
                                    "position": [100, 200],
                                    "parameters": {}
                                }
                            ],
                            "connections": {},
                            "active": True
                        })
                    }]
                }
            }]
        }
        mock_post.return_value = mock_response
        yield mock_post

@pytest.fixture
def mock_redis():
    """Mock Redis for testing"""
    with patch('redis.Redis') as mock_redis_class:
        mock_redis_instance = Mock()
        mock_redis_instance.get.return_value = None
        mock_redis_instance.set.return_value = True
        mock_redis_instance.ping.return_value = True
        mock_redis_class.return_value = mock_redis_instance
        yield mock_redis_instance

@pytest.fixture(autouse=True)
def clean_environment():
    """Clean environment variables after each test"""
    yield
    
    # Clean up test environment variables
    test_vars = [
        'TEST_SECRET_KEY',
        'TEST_GEMINI_API_KEY',
        'TEST_DEBUG'
    ]
    
    for var in test_vars:
        if var in os.environ:
            del os.environ[var]

@pytest.fixture
def rate_limit_headers():
    """Headers for rate limiting tests"""
    return {
        'Content-Type': 'application/json',
        'X-Forwarded-For': '192.168.1.100'
    }

@pytest.fixture
def workflow_validation_data():
    """Data for workflow validation tests"""
    return {
        "valid_workflow": {
            "name": "Valid Workflow",
            "nodes": [
                {
                    "id": "1",
                    "name": "Start",
                    "type": "n8n-nodes-base.start",
                    "position": [100, 200],
                    "parameters": {}
                }
            ],
            "connections": {},
            "active": True
        },
        "invalid_workflow": {
            "name": "",
            "nodes": [],
            "connections": {},
            "active": False
        }
    }