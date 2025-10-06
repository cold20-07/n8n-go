#!/usr/bin/env python3
"""
Setup Script for n8n Workflow Generator
Handles initial setup and dependency installation
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def setup_project():
    """Complete project setup"""
    print("🚀 Setting up n8n Workflow Generator...")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install Python dependencies
    if Path("requirements.txt").exists():
        if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
            print("⚠️ Python dependencies installation failed, but app may still work")
    
    # Install Node.js dependencies if package.json exists
    if Path("package.json").exists():
        if not run_command("npm install", "Installing Node.js dependencies"):
            print("⚠️ Node.js dependencies installation failed")
    
    # Create necessary directories
    directories = ["trained_models", "improved_models", "final_models", "static/temp"]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {directory}")
    
    # Optional: Regenerate models
    print("\n🤖 Would you like to regenerate AI models? (y/n)")
    print("   Note: This may take several minutes but improves AI features")
    
    choice = input().lower().strip()
    if choice in ['y', 'yes']:
        run_command("python regenerate_models.py", "Regenerating AI models")
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("   1. Open index.html in your browser for the web interface")
    print("   2. Or run 'python app.py' for the Flask server")
    print("   3. Configure your Gemini API key in script.js (optional)")
    
    return True

if __name__ == "__main__":
    setup_project()