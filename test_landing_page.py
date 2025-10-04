#!/usr/bin/env python3
"""
Test script to verify the new landing page works with the backend
"""

import sys
import os
import json
from flask import Flask
from werkzeug.test import Client
from werkzeug.wrappers import Response

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
except ImportError as e:
    print(f"❌ Failed to import app: {e}")
    sys.exit(1)

def test_landing_page():
    """Test that the landing page loads correctly"""
    print("Testing landing page...")
    
    with app.test_client() as client:
        # Test the main route
        response = client.get('/')
        
        if response.status_code == 200:
            print("✅ Landing page loads successfully")
            
            # Check if key elements are present in the HTML
            html_content = response.get_data(as_text=True)
            
            required_elements = [
                'workflowForm',
                'description',
                'triggerType',
                'complexity',
                'template',
                'generateBtn',
                'N8N Go'
            ]
            
            missing_elements = []
            for element in required_elements:
                if element not in html_content:
                    missing_elements.append(element)
            
            if missing_elements:
                print(f"⚠️  Missing elements: {missing_elements}")
            else:
                print("✅ All required form elements are present")
                
        else:
            print(f"❌ Landing page failed to load: {response.status_code}")
            return False
    
    return True

def test_workflow_generation():
    """Test that workflow generation endpoint works"""
    print("\nTesting workflow generation...")
    
    with app.test_client() as client:
        # Test data
        test_data = {
            'description': 'Create a simple webhook to database workflow for testing',
            'triggerType': 'webhook',
            'complexity': 'simple',
            'template': '',
            'advanced_options': {
                'include_error_handling': True,
                'include_validation': True
            }
        }
        
        # Make POST request to generate endpoint
        response = client.post('/generate', 
                             data=json.dumps(test_data),
                             content_type='application/json')
        
        if response.status_code == 200:
            print("✅ Workflow generation endpoint responds successfully")
            
            try:
                data = response.get_json()
                if data.get('success'):
                    workflow = data.get('workflow')
                    if workflow and 'nodes' in workflow and 'name' in workflow:
                        print(f"✅ Generated workflow: {workflow['name']}")
                        print(f"✅ Node count: {len(workflow['nodes'])}")
                        return True
                    else:
                        print("❌ Invalid workflow structure in response")
                        return False
                else:
                    print(f"❌ Generation failed: {data.get('error', 'Unknown error')}")
                    return False
            except Exception as e:
                print(f"❌ Failed to parse response: {e}")
                return False
        else:
            print(f"❌ Generation endpoint failed: {response.status_code}")
            try:
                error_data = response.get_json()
                print(f"Error details: {error_data}")
            except:
                print(f"Response text: {response.get_data(as_text=True)}")
            return False

def test_static_files():
    """Test that static files are accessible"""
    print("\nTesting static files...")
    
    with app.test_client() as client:
        # Test CSS file
        css_response = client.get('/static/css/style.css')
        if css_response.status_code == 200:
            print("✅ CSS file loads successfully")
        else:
            print(f"❌ CSS file failed to load: {css_response.status_code}")
            
        # Test JS file
        js_response = client.get('/static/js/script.js')
        if js_response.status_code == 200:
            print("✅ JavaScript file loads successfully")
        else:
            print(f"❌ JavaScript file failed to load: {js_response.status_code}")
            
        return css_response.status_code == 200 and js_response.status_code == 200

def test_form_elements():
    """Test that all form elements have proper IDs and names"""
    print("\nTesting form element compatibility...")
    
    with app.test_client() as client:
        response = client.get('/')
        html_content = response.get_data(as_text=True)
        
        # Check for form elements that JavaScript expects
        form_elements = {
            'workflowForm': 'id="workflowForm"',
            'description': 'id="description"',
            'triggerType': 'id="triggerType"',
            'complexity': 'id="complexity"',
            'template': 'id="template"',
            'generateBtn': 'id="generateBtn"',
            'advancedToggle': 'id="advancedToggle"',
            'copyBtn': 'id="copyBtn"',
            'downloadBtn': 'id="downloadBtn"',
            'regenerateBtn': 'id="regenerateBtn"',
            'workflowOutput': 'id="workflowOutput"',
            'validation': 'id="validation"'
        }
        
        missing_ids = []
        for element_name, id_pattern in form_elements.items():
            if id_pattern not in html_content:
                missing_ids.append(element_name)
        
        if missing_ids:
            print(f"❌ Missing form element IDs: {missing_ids}")
            return False
        else:
            print("✅ All required form element IDs are present")
            return True

def main():
    """Run all tests"""
    print("🧪 Testing New Landing Page Backend Compatibility")
    print("=" * 50)
    
    tests = [
        test_landing_page,
        test_static_files,
        test_form_elements,
        test_workflow_generation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The new landing page is fully compatible with the backend.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)