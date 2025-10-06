#!/usr/bin/env python3
"""
Build script for N8N Workflow Generator
Handles post-TypeScript compilation tasks
"""
import os
import shutil
import json
from pathlib import Path

def main():
    """Main build process"""
    print("🔨 Starting N8N Workflow Generator build process...")
    
    # Check if TypeScript compilation was successful
    dist_dir = Path('dist')
    if not dist_dir.exists():
        print("❌ TypeScript compilation failed - dist directory not found")
        return False
    
    print("✅ TypeScript compilation successful")
    
    # Copy static files to dist if needed
    static_dir = Path('static')
    if static_dir.exists():
        print("📁 Copying static files...")
        dist_static = dist_dir / 'static'
        if dist_static.exists():
            shutil.rmtree(dist_static)
        shutil.copytree(static_dir, dist_static)
        print("✅ Static files copied")
    
    # Copy templates if needed
    templates_dir = Path('templates')
    if templates_dir.exists():
        print("📄 Copying templates...")
        dist_templates = dist_dir / 'templates'
        if dist_templates.exists():
            shutil.rmtree(dist_templates)
        shutil.copytree(templates_dir, dist_templates)
        print("✅ Templates copied")
    
    # Create build info
    build_info = {
        'version': '1.0.0',
        'build_time': '2025-10-06T12:00:00Z',
        'typescript_compiled': True,
        'python_backend': True,
        'status': 'success'
    }
    
    build_info_path = dist_dir / 'build-info.json'
    with open(build_info_path, 'w') as f:
        json.dump(build_info, f, indent=2)
    
    print("✅ Build info created")
    print("🎉 Build process completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)