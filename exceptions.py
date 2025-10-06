"""
Custom exceptions for N8N Workflow Generator
"""

class WorkflowGeneratorError(Exception):
    """Base exception for workflow generation errors"""
    
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or 'WORKFLOW_ERROR'
        self.details = details or {}
    
    def to_dict(self) -> dict:
        """Convert exception to dictionary for API responses"""
        return {
            'error': self.error_code,
            'message': self.message,
            'details': self.details
        }

class ValidationError(WorkflowGeneratorError):
    """Raised when workflow validation fails"""
    
    def __init__(self, message: str, field: str = None, value=None):
        super().__init__(message, 'VALIDATION_ERROR')
        if field:
            self.details['field'] = field
        if value is not None:
            self.details['invalid_value'] = str(value)

class GenerationError(WorkflowGeneratorError):
    """Raised when workflow generation fails"""
    
    def __init__(self, message: str, generator_type: str = None):
        super().__init__(message, 'GENERATION_ERROR')
        if generator_type:
            self.details['generator'] = generator_type

class APIError(WorkflowGeneratorError):
    """Raised when external API calls fail"""
    
    def __init__(self, message: str, api_name: str = None, status_code: int = None):
        super().__init__(message, 'API_ERROR')
        if api_name:
            self.details['api'] = api_name
        if status_code:
            self.details['status_code'] = status_code

class ConnectionError(WorkflowGeneratorError):
    """Raised when workflow connection validation fails"""
    
    def __init__(self, message: str, node_name: str = None):
        super().__init__(message, 'CONNECTION_ERROR')
        if node_name:
            self.details['node'] = node_name

class ConfigurationError(WorkflowGeneratorError):
    """Raised when configuration is invalid"""
    
    def __init__(self, message: str, config_key: str = None):
        super().__init__(message, 'CONFIG_ERROR')
        if config_key:
            self.details['config_key'] = config_key

class RateLimitError(WorkflowGeneratorError):
    """Raised when rate limit is exceeded"""
    
    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = None):
        super().__init__(message, 'RATE_LIMIT_ERROR')
        if retry_after:
            self.details['retry_after'] = retry_after