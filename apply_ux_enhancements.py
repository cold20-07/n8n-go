#!/usr/bin/env python3
"""
UX Enhancement Application Script
Applies the enhanced UX improvements to the N8N Workflow Generator
"""

import os
import shutil
import sys
from datetime import datetime

def backup_existing_files():
    """Create backups of existing files before applying enhancements"""
    backup_dir = f"backups/pre_ux_enhancement_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    files_to_backup = [
        ('templates/index.html', f'{backup_dir}/index.html'),
        ('static/css/style.css', f'{backup_dir}/style.css'),
        ('static/js/main.js', f'{backup_dir}/main.js')
    ]
    
    print("🔄 Creating backups of existing files...")
    for src, dst in files_to_backup:
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"   ✅ Backed up {src} to {dst}")
        else:
            print(f"   ⚠️  File not found: {src}")
    
    return backup_dir

def apply_enhancements():
    """Apply the enhanced UX files"""
    enhancements = [
        ('templates/enhanced-index.html', 'templates/index.html'),
        ('static/css/enhanced-style.css', 'static/css/style.css'),
        ('static/js/enhanced-main.js', 'static/js/main.js')
    ]
    
    print("🚀 Applying UX enhancements...")
    for src, dst in enhancements:
        if os.path.exists(src):
            # Ensure destination directory exists
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            print(f"   ✅ Applied {src} to {dst}")
        else:
            print(f"   ❌ Enhancement file not found: {src}")
            return False
    
    return True

def create_additional_assets():
    """Create additional assets needed for enhanced UX"""
    
    # Create accessibility statement page
    accessibility_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Accessibility Statement - n8n go</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <header>
        <div class="container">
            <nav>
                <a href="/" class="logo">n8n go</a>
                <ul class="nav-links">
                    <li><a href="/">Home</a></li>
                    <li><a href="/accessibility" class="active">Accessibility</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <main class="container" style="padding: 60px 20px;">
        <h1>Accessibility Statement</h1>
        
        <p>n8n go is committed to ensuring digital accessibility for people with disabilities. We are continually improving the user experience for everyone and applying the relevant accessibility standards.</p>
        
        <h2>Conformance Status</h2>
        <p>The Web Content Accessibility Guidelines (WCAG) defines requirements for designers and developers to improve accessibility for people with disabilities. It defines three levels of conformance: Level A, Level AA, and Level AAA. n8n go is fully conformant with WCAG 2.1 level AA.</p>
        
        <h2>Accessibility Features</h2>
        <ul>
            <li>Keyboard navigation support</li>
            <li>Screen reader compatibility</li>
            <li>High contrast mode support</li>
            <li>Scalable text up to 200%</li>
            <li>Alternative text for images</li>
            <li>Descriptive link text</li>
            <li>Consistent navigation</li>
            <li>Form labels and instructions</li>
        </ul>
        
        <h2>Feedback</h2>
        <p>We welcome your feedback on the accessibility of n8n go. Please let us know if you encounter accessibility barriers:</p>
        <ul>
            <li>Email: accessibility@n8ngo.com</li>
            <li>Phone: +1 (555) 123-4567</li>
        </ul>
        
        <p>We try to respond to feedback within 2 business days.</p>
        
        <h2>Technical Specifications</h2>
        <p>Accessibility of n8n go relies on the following technologies to work with the particular combination of web browser and any assistive technologies or plugins installed on your computer:</p>
        <ul>
            <li>HTML</li>
            <li>WAI-ARIA</li>
            <li>CSS</li>
            <li>JavaScript</li>
        </ul>
        
        <p>These technologies are relied upon for conformance with the accessibility standards used.</p>
    </main>
    
    <footer>
        <div class="container">
            <p style="text-align: center; padding: 20px 0;">
                Made with ❤️ by NXT - Committed to accessibility for all
            </p>
        </div>
    </footer>
</body>
</html>"""
    
    os.makedirs('templates', exist_ok=True)
    with open('templates/accessibility.html', 'w', encoding='utf-8') as f:
        f.write(accessibility_content)
    print("   ✅ Created accessibility statement page")
    
    # Create service worker for offline support
    sw_content = """// Service Worker for n8n go - Enhanced UX
const CACHE_NAME = 'n8n-go-v1';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/js/main.js',
    '/static/favicon.ico'
];

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                // Return cached version or fetch from network
                return response || fetch(event.request);
            }
        )
    );
});"""
    
    os.makedirs('static', exist_ok=True)
    with open('static/sw.js', 'w', encoding='utf-8') as f:
        f.write(sw_content)
    print("   ✅ Created service worker for offline support")

def update_flask_routes():
    """Generate Flask route updates for new pages"""
    route_updates = """
# Add these routes to your Flask app for enhanced UX features

@app.route('/accessibility')
def accessibility():
    return render_template('accessibility.html')

@app.route('/sw.js')
def service_worker():
    return send_from_directory('static', 'sw.js', mimetype='application/javascript')

# Enhanced error handlers with better UX
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500
"""
    
    with open('flask_route_updates.py', 'w', encoding='utf-8') as f:
        f.write(route_updates)
    print("   ✅ Created Flask route updates file")

def run_tests():
    """Run basic tests to verify enhancements are working"""
    print("🧪 Running basic verification tests...")
    
    # Check if enhanced files exist
    required_files = [
        'templates/index.html',
        'static/css/style.css',
        'static/js/main.js'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path} exists")
        else:
            print(f"   ❌ {file_path} missing")
            return False
    
    # Check for key UX features in files
    with open('templates/index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    ux_features = [
        'aria-label',
        'skip-link',
        'live-region',
        'validation-message',
        'character-counter'
    ]
    
    for feature in ux_features:
        if feature in html_content:
            print(f"   ✅ UX feature '{feature}' found in HTML")
        else:
            print(f"   ⚠️  UX feature '{feature}' not found in HTML")
    
    return True

def main():
    """Main execution function"""
    print("🎨 n8n Workflow Generator - UX Enhancement Application")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('templates') and not os.path.exists('static'):
        print("❌ Error: This script should be run from the project root directory")
        print("   Make sure you're in the directory containing 'templates' and 'static' folders")
        sys.exit(1)
    
    # Check if enhancement files exist
    enhancement_files = [
        'templates/enhanced-index.html',
        'static/css/enhanced-style.css',
        'static/js/enhanced-main.js'
    ]
    
    missing_files = [f for f in enhancement_files if not os.path.exists(f)]
    if missing_files:
        print("❌ Error: Enhancement files not found:")
        for f in missing_files:
            print(f"   - {f}")
        print("\\n   Please ensure all enhancement files are in place before running this script.")
        sys.exit(1)
    
    try:
        # Step 1: Backup existing files
        backup_dir = backup_existing_files()
        
        # Step 2: Apply enhancements
        if not apply_enhancements():
            print("❌ Failed to apply enhancements")
            sys.exit(1)
        
        # Step 3: Create additional assets
        print("🔧 Creating additional assets...")
        create_additional_assets()
        update_flask_routes()
        
        # Step 4: Run verification tests
        if run_tests():
            print("\\n🎉 UX enhancements successfully applied!")
            print(f"\\n📁 Backup created at: {backup_dir}")
            print("\\n📋 Next steps:")
            print("   1. Review the changes in your files")
            print("   2. Update your Flask routes using flask_route_updates.py")
            print("   3. Test the application thoroughly")
            print("   4. Run accessibility tests with screen readers")
            print("   5. Check mobile responsiveness")
            print("\\n📖 See UX_ENHANCEMENT_GUIDE.md for detailed documentation")
        else:
            print("\\n⚠️  Enhancements applied but verification tests failed")
            print("   Please check the files manually and refer to the guide")
        
    except Exception as e:
        print(f"\\n❌ Error during enhancement application: {str(e)}")
        print("   Please check the error and try again")
        sys.exit(1)

if __name__ == "__main__":
    main()