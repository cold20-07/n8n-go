#!/usr/bin/env python3
"""
Run script for the n8n Workflow Generator
"""

import os
import sys
from app import app

def main():
    """Main entry point for the application"""
    
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    # Get host from environment or use default
    host = os.environ.get('HOST', '127.0.0.1')
    
    # Get debug mode from environment
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    print(f"Starting n8n Workflow Generator on {host}:{port}")
    print(f"Debug mode: {debug}")
    
    try:
        app.run(
            host=host,
            port=port,
            debug=debug
        )
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"Error starting application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()