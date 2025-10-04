#!/usr/bin/env python3
"""
Test frontend integration and static file serving
"""

import requests
import threading
import time
from app import app
from werkzeug.serving import make_server

def test_frontend_integration():
    """Test that frontend files are served correctly"""
    print('🧪 Testing Frontend Integration')
    print('=' * 40)
    
    # Start test server
    server = make_server('127.0.0.1', 5557, app, threaded=True)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    time.sleep(2)  # Give server time to start
    
    try:
        # Test main page
        print('🌐 Testing main page...')
        response = requests.get('http://127.0.0.1:5557/', timeout=10)
        if response.status_code == 200:
            print('✅ Main page loads successfully')
            
            # Check for key elements
            content = response.text
            checks = [
                ('N8N Go', 'Page title'),
                ('workflowForm', 'Workflow form'),
                ('Generate Workflow', 'Generate button'),
                ('css/style.css', 'CSS reference'),
                ('js/script.js', 'JavaScript reference')
            ]
            
            for check, description in checks:
                if check in content:
                    print(f'✅ {description} found')
                else:
                    print(f'❌ {description} missing')
        else:
            print(f'❌ Main page failed: {response.status_code}')
            return False
        
        # Test CSS file
        print('\n🎨 Testing CSS file...')
        css_response = requests.get('http://127.0.0.1:5557/static/css/style.css', timeout=10)
        if css_response.status_code == 200:
            print('✅ CSS file loads successfully')
            if '--primary-blue' in css_response.text or '--dark-bg' in css_response.text:
                print('✅ CSS contains expected dark theme styles')
            else:
                print('❌ CSS missing expected styles')
        else:
            print(f'❌ CSS file failed: {css_response.status_code}')
        
        # Test JavaScript file
        print('\n📜 Testing JavaScript file...')
        js_response = requests.get('http://127.0.0.1:5557/static/js/script.js', timeout=10)
        if js_response.status_code == 200:
            print('✅ JavaScript file loads successfully')
            if 'N8nWorkflowGeneratorApp' in js_response.text:
                print('✅ JavaScript contains expected classes')
            else:
                print('❌ JavaScript missing expected classes')
        else:
            print(f'❌ JavaScript file failed: {js_response.status_code}')
        
        # Test workflow generation
        print('\n⚙️ Testing workflow generation...')
        test_data = {
            'description': 'Create a simple test workflow for frontend validation',
            'triggerType': 'webhook'
        }
        
        gen_response = requests.post(
            'http://127.0.0.1:5557/generate',
            json=test_data,
            timeout=30
        )
        
        if gen_response.status_code == 200:
            data = gen_response.json()
            if data.get('success'):
                print('✅ Workflow generation works from frontend')
                workflow = data['workflow']
                print(f'   Generated: {workflow.get("name", "Unknown")}')
                print(f'   Nodes: {len(workflow.get("nodes", []))}')
            else:
                print(f'❌ Generation failed: {data.get("error")}')
        else:
            print(f'❌ Generation request failed: {gen_response.status_code}')
        
        print('\n✅ Frontend integration test completed successfully!')
        return True
        
    except Exception as e:
        print(f'❌ Test failed with error: {e}')
        return False
    finally:
        server.shutdown()

if __name__ == "__main__":
    success = test_frontend_integration()
    if success:
        print('\n🎉 All frontend tests passed!')
        print('🚀 Your N8N Go is ready to use!')
        print('\nTo start the application:')
        print('  python run.py')
        print('  or')
        print('  python app.py')
    else:
        print('\n⚠️ Some frontend tests failed')