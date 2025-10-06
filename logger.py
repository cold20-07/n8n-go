"""
Logging configuration for N8N Workflow Generator
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

def setup_logger(
    name: str, 
    level: str = "INFO", 
    log_file: Optional[str] = None,
    format_string: Optional[str] = None
) -> logging.Logger:
    """
    Setup logger with console and optional file output
    
    Args:
        name: Logger name
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output
        format_string: Custom format string
    
    Returns:
        Configured logger instance
    """
    
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Default format
    if not format_string:
        format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    formatter = logging.Formatter(format_string)
    
    # Console handler with encoding fix for Windows
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Fix encoding issues on Windows
    if hasattr(console_handler.stream, 'reconfigure'):
        try:
            console_handler.stream.reconfigure(encoding='utf-8')
        except:
            pass  # Fallback to default encoding
    
    logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        # Create logs directory if it doesn't exist
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def setup_app_logging(debug: bool = False) -> logging.Logger:
    """
    Setup application-wide logging configuration
    
    Args:
        debug: Enable debug logging
    
    Returns:
        Main application logger
    """
    
    level = "DEBUG" if debug else "INFO"
    
    # Create logs directory
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    log_file = logs_dir / f"n8n_generator_{timestamp}.log"
    
    # Setup main logger
    logger = setup_logger(
        "n8n_generator", 
        level=level,
        log_file=str(log_file)
    )
    
    # Setup component loggers
    setup_logger("n8n_generator.api", level=level)
    setup_logger("n8n_generator.generator", level=level)
    setup_logger("n8n_generator.validator", level=level)
    
    logger.info(f"Logging initialized - Level: {level}, File: {log_file}")
    
    return logger

class LoggerMixin:
    """Mixin class to add logging capability to any class"""
    
    @property
    def logger(self) -> logging.Logger:
        """Get logger for this class"""
        class_name = self.__class__.__name__
        return logging.getLogger(f"n8n_generator.{class_name.lower()}")

# Performance logging decorator
def log_performance(func):
    """Decorator to log function execution time"""
    import time
    from functools import wraps
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger("n8n_generator.performance")
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"{func.__name__} executed in {execution_time:.3f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"{func.__name__} failed after {execution_time:.3f}s: {e}")
            raise
    
    return wrapper

# Request logging for Flask
def log_request(request, response_status: int, execution_time: float):
    """Log HTTP request details"""
    logger = logging.getLogger("n8n_generator.api")
    
    log_data = {
        'method': request.method,
        'path': request.path,
        'status': response_status,
        'time': f"{execution_time:.3f}s",
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', 'Unknown')[:100]
    }
    
    if response_status >= 400:
        logger.warning(f"Request failed: {log_data}")
    else:
        logger.info(f"Request completed: {log_data}")

if __name__ == "__main__":
    # Test logging setup
    logger = setup_app_logging(debug=True)
    logger.info("Logging system test successful")
    logger.debug("Debug message test")
    logger.warning("Warning message test")
    logger.error("Error message test")