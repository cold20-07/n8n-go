#!/usr/bin/env python3
"""Debug Trigger Type Issues"""

import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def debug_trigger_types():
    """Debug trigger type generation"""
    print("🔍 Debugging Trigger Type Issues")
    print("=" * 45)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    trigger_types = ['webhook', 'schedule', 'manual']
    expected_types = {
        'webhook': 'n8n-nodes-base.webhook',
        'schedule': 'n8n-nodes-base.scheduleTrigger',
        'manual': 'n8n-nodes-base.manualTrigger'
    }
    
    for trigger_type in trigger_types:
        print(f"\n🧪 Testing {trigger_type} trigger...")
        
        # Test with both parameter formats
        for param_name in ['triggerType', 'trigger_type']:
            print(f"  Using parameter: {param_name}")
            
            response = client.post('/generate',
                                  data=json.dumps({
                                      'description': f'Create a {trigger_type} workflow for testing trigger types',
                                      param_name: trigger_type
                                  }),
                                  content_type='application/json')
            
            print(f"  Response status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = json.loads(response.data)
                    workflow = data.get('workflow', {})
                    nodes = workflow.get('nodes', [])
                    
                    print(f"  Generated {len(nodes)} nodes")
                    
                    if len(nodes) > 0:
                        first_node = nodes[0]
                        actual_type = first_node.get('type')
                        expected_type = expected_types[trigger_type]
                        
                        print(f"  First node name: {first_node.get('name')}")
                        print(f"  Expected type: {expected_type}")
                        print(f"  Actual type: {actual_type}")
                        
                        if actual_type == expected_type:
                            print(f"  ✅ CORRECT")
                        else:
                            print(f"  ❌ WRONG - Expected {expected_type}, got {actual_type}")
                            
                            # Debug the trigger node creation
                            print(f"  Debug info:")
                            print(f"    Node parameters: {first_node.get('parameters', {})}")
                            print(f"    Node position: {first_node.get('position', [])}")
                    else:
                        print("  ❌ No nodes generated")
                        
                except Exception as e:
                    print(f"  ❌ Error parsing response: {e}")
            else:
                print(f"  ❌ Request failed with status {response.status_code}")
                try:
                    error_data = json.loads(response.data)
                    print(f"  Error: {error_data.get('error', 'Unknown error')}")
                except:
                    print(f"  Raw response: {response.data}")

if __name__ == "__main__":
    debug_trigger_types()