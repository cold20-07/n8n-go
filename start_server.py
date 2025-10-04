#!/usr/bin/env python3
"""
Simple server launcher for n8n Workflow Generator
Handles both Flask app and static file serving
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def start_flask_server():
    """Start the Flask development server"""
    print("🚀 Starting Flask development server...")
    print("📍 Server will be available at: http://127.0.0.1:5000")
    print("📝 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Import and run Flask app
        from app import app
        app.run(host='127.0.0.1', port=5000, debug=True)
    except ImportError:
        print("❌ Flask app not found. Starting simple HTTP server instead...")
        start_simple_server()
    except Exception as e:
        print(f"❌ Error starting Flask server: {e}")
        print("🔄 Falling back to simple HTTP server...")
        start_simple_server()

def start_simple_server():
    """Start a simple HTTP server for static files"""
    print("🌐 Starting simple HTTP server...")
    print("📍 Server will be available at: http://127.0.0.1:8000")
    print("📝 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        # Use Python's built-in HTTP server with explicit IPv4 binding
        subprocess.run([
            sys.executable, '-m', 'http.server', '8000', 
            '--bind', '127.0.0.1'
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def open_browser(url, delay=2):
    """Open browser after a short delay"""
    def delayed_open():
        time.sleep(delay)
        try:
            webbrowser.open(url)
            print(f"🌐 Opened browser at {url}")
        except Exception as e:
            print(f"⚠️  Could not open browser: {e}")
            print(f"📍 Please manually open: {url}")
    
    import threading
    threading.Thread(target=delayed_open, daemon=True).start()

def main():
    """Main entry point"""
    print("🎯 n8n Workflow Generator Server Launcher")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path('app.py').exists():
        print("⚠️  app.py not found in current directory")
        print("📁 Please run this script from the project root directory")
        sys.exit(1)
    
    # Determine which server to start
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == 'simple':
            open_browser('http://127.0.0.1:8000')
            start_simple_server()
        elif mode == 'flask':
            open_browser('http://127.0.0.1:5000')
            start_flask_server()
        else:
            print(f"❌ Unknown mode: {mode}")
            print("💡 Usage: python start_server.py [flask|simple]")
            sys.exit(1)
    else:
        # Default: try Flask first, fallback to simple
        print("🔍 Auto-detecting best server option...")
        try:
            import flask
            print("✅ Flask available - starting Flask server")
            open_browser('http://127.0.0.1:5000')
            start_flask_server()
        except ImportError:
            print("ℹ️  Flask not available - starting simple HTTP server")
            open_browser('http://127.0.0.1:8000')
            start_simple_server()

if __name__ == '__main__':
    main()