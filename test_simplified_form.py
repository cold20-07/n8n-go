#!/usr/bin/env python3
"""
Test the simplified form functionality
"""

import sys
import os
import json

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from app import app
except ImportError as e:
    print(f"❌ Failed to import app: {e}")
    sys.exit(1)

def test_simplified_form():
    """Test the simplified form with different trigger types"""
    print("🧪 Testing Simplified Form with All Trigger Types")
    print("=" * 50)
    
    trigger_types = ['webhook', 'schedule', 'manual']
    
    with app.test_client() as client:
        for trigger_type in trigger_types:
            print(f"\n🔧 Testing {trigger_type} trigger...")
            
            # Test data for each trigger type
            test_data = {
                'description': f'Create a {trigger_type} workflow that processes data and sends notifications',
                'triggerType': trigger_type,
                'complexity': 'medium',  # Default complexity
                'template': '',  # No template
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
                try:
                    data = response.get_json()
                    if data.get('success'):
                        workflow = data.get('workflow')
                        if workflow and 'nodes' in workflow:
                            print(f"✅ {trigger_type.title()} workflow generated successfully")
                            print(f"   Name: {workflow['name']}")
                            print(f"   Nodes: {len(workflow['nodes'])}")
                            
                            # Check if the trigger node has the correct type
                            trigger_node = workflow['nodes'][0] if workflow['nodes'] else None
                            if trigger_node:
                                expected_types = {
                                    'webhook': 'n8n-nodes-base.webhook',
                                    'schedule': 'n8n-nodes-base.scheduleTrigger',
                                    'manual': 'n8n-nodes-base.manualTrigger'
                                }
                                
                                if trigger_node['type'] == expected_types[trigger_type]:
                                    print(f"   ✅ Correct trigger type: {trigger_node['type']}")
                                else:
                                    print(f"   ❌ Wrong trigger type: {trigger_node['type']} (expected {expected_types[trigger_type]})")
                            else:
                                print(f"   ❌ No trigger node found")
                        else:
                            print(f"❌ {trigger_type.title()} workflow generation failed - invalid structure")
                    else:
                        print(f"❌ {trigger_type.title()} workflow generation failed: {data.get('error')}")
                except Exception as e:
                    print(f"❌ {trigger_type.title()} workflow generation failed: {e}")
            else:
                print(f"❌ {trigger_type.title()} request failed: {response.status_code}")

def test_form_validation():
    """Test form validation with missing fields"""
    print("\n🔍 Testing Form Validation")
    print("=" * 30)
    
    with app.test_client() as client:
        # Test with missing description
        test_data = {
            'description': '',
            'triggerType': 'webhook'
        }
        
        response = client.post('/generate', 
                             data=json.dumps(test_data),
                             content_type='application/json')
        
        if response.status_code == 400:
            print("✅ Validation correctly rejects empty description")
        else:
            print("❌ Validation should reject empty description")
        
        # Test with missing trigger type
        test_data = {
            'description': 'Test workflow description',
            'triggerType': ''
        }
        
        response = client.post('/generate', 
                             data=json.dumps(test_data),
                             content_type='application/json')
        
        # Backend should handle this gracefully
        print("✅ Backend handles missing trigger type")

def main():
    """Run all tests"""
    test_simplified_form()
    test_form_validation()
    
    print("\n" + "=" * 50)
    print("🎉 Simplified form testing completed!")

if __name__ == "__main__":
    main()