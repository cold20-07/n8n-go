#!/usr/bin/env python3
"""Final Trigger Type Verification"""

import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def test_all_trigger_combinations():
    """Test all trigger type combinations thoroughly"""
    print("🎯 FINAL TRIGGER TYPE VERIFICATION")
    print("=" * 50)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    # Test all combinations of parameters and trigger types
    test_cases = [
        # Webhook tests
        {'param': 'triggerType', 'value': 'webhook', 'expected': 'n8n-nodes-base.webhook'},
        {'param': 'trigger_type', 'value': 'webhook', 'expected': 'n8n-nodes-base.webhook'},
        
        # Schedule tests  
        {'param': 'triggerType', 'value': 'schedule', 'expected': 'n8n-nodes-base.scheduleTrigger'},
        {'param': 'trigger_type', 'value': 'schedule', 'expected': 'n8n-nodes-base.scheduleTrigger'},
        
        # Manual tests
        {'param': 'triggerType', 'value': 'manual', 'expected': 'n8n-nodes-base.manualTrigger'},
        {'param': 'trigger_type', 'value': 'manual', 'expected': 'n8n-nodes-base.manualTrigger'},
    ]
    
    passed = 0
    total = len(test_cases)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}/{total}: {test['param']}='{test['value']}'")
        
        response = client.post('/generate',
                              data=json.dumps({
                                  'description': f'Create a comprehensive {test["value"]} workflow for final verification testing',
                                  test['param']: test['value']
                              }),
                              content_type='application/json')
        
        if response.status_code == 200:
            try:
                data = json.loads(response.data)
                workflow = data.get('workflow', {})
                nodes = workflow.get('nodes', [])
                
                if len(nodes) > 0:
                    first_node = nodes[0]
                    actual_type = first_node.get('type')
                    expected_type = test['expected']
                    
                    print(f"   Expected: {expected_type}")
                    print(f"   Actual:   {actual_type}")
                    
                    if actual_type == expected_type:
                        print("   ✅ PERFECT MATCH")
                        passed += 1
                    else:
                        print("   ❌ TYPE MISMATCH")
                        print(f"   Node name: {first_node.get('name')}")
                        print(f"   Node params: {first_node.get('parameters', {})}")
                else:
                    print("   ❌ NO NODES GENERATED")
                    
            except Exception as e:
                print(f"   ❌ ERROR: {e}")
        else:
            print(f"   ❌ REQUEST FAILED: {response.status_code}")
            try:
                error_data = json.loads(response.data)
                print(f"   Error: {error_data.get('error', 'Unknown')}")
            except:
                pass
    
    success_rate = (passed / total) * 100
    
    print(f"\n🏆 FINAL TRIGGER VERIFICATION RESULTS")
    print("=" * 50)
    print(f"✅ Passed: {passed}/{total}")
    print(f"📊 Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("🎉 PERFECT! All trigger types working flawlessly!")
        print("🚀 Trigger type handling is 100% correct!")
    else:
        print("⚠️ Some trigger types need attention!")
    
    return success_rate == 100

if __name__ == "__main__":
    is_perfect = test_all_trigger_combinations()
    exit(0 if is_perfect else 1)