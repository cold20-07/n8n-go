#!/usr/bin/env python3
"""
Test Prompt Assistance System
Tests the interactive prompt helper functionality
"""

import requests
import json
import time
from threading import Thread
from app import app

def run_test_server():
    """Run the Flask app for testing"""
    app.run(port=5001, debug=False, use_reloader=False)

def test_prompt_assistance():
    """Test the prompt assistance functionality"""
    print("🧪 Testing Prompt Assistance System")
    print("=" * 50)
    
    # Start server
    server_thread = Thread(target=run_test_server, daemon=True)
    server_thread.start()
    time.sleep(2)
    
    base_url = "http://localhost:5001"
    
    # Test cases for prompt assistance
    test_cases = [
        {
            'name': 'Empty Input',
            'input': '',
            'should_need_help': True
        },
        {
            'name': 'Very Short Input',
            'input': 'help',
            'should_need_help': True
        },
        {
            'name': 'Vague Request',
            'input': 'automate something',
            'should_need_help': True
        },
        {
            'name': 'Clear Request',
            'input': 'Process CSV files and send email notifications with the results',
            'should_need_help': False
        },
        {
            'name': 'Integration Request',
            'input': 'Connect Slack to Google Sheets for daily reports',
            'should_need_help': False
        }
    ]
    
    print("🔍 Testing Prompt Help Endpoint...")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test_case['name']}")
        print(f"Input: '{test_case['input']}'")
        
        try:
            response = requests.post(f"{base_url}/prompt-help", 
                json={'description': test_case['input']},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result['success']:
                    needs_help = result.get('needs_help', False)
                    message = result.get('message', '')
                    
                    print(f"✅ Response received")
                    print(f"   Needs help: {needs_help}")
                    print(f"   Expected: {test_case['should_need_help']}")
                    
                    if needs_help == test_case['should_need_help']:
                        print(f"✅ Correct assessment")
                    else:
                        print(f"❌ Incorrect assessment")
                    
                    # Show first 100 chars of message
                    print(f"   Message: {message[:100]}...")
                    
                    if 'suggestions' in result and result['suggestions']:
                        print(f"   Suggestions: {len(result['suggestions'])} provided")
                    
                else:
                    print(f"❌ API returned error: {result.get('error', 'Unknown error')}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
        
        print("-" * 30)
    
    # Test workflow generation with prompt assistance
    print(f"\n🚀 Testing Workflow Generation with Prompt Assistance...")
    
    generation_tests = [
        {
            'name': 'Too Short - Should Trigger Help',
            'input': 'help me',
            'should_trigger_help': True
        },
        {
            'name': 'Good Input - Should Generate',
            'input': 'Create a workflow that processes incoming webhook data, validates email addresses, and sends notifications to Slack',
            'should_trigger_help': False
        }
    ]
    
    for i, test_case in enumerate(generation_tests, 1):
        print(f"\n📝 Generation Test {i}: {test_case['name']}")
        print(f"Input: '{test_case['input']}'")
        
        try:
            response = requests.post(f"{base_url}/generate",
                json={
                    'description': test_case['input'],
                    'triggerType': 'webhook',
                    'complexity': 'medium'
                },
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('needs_prompt_help'):
                    print(f"✅ Triggered prompt assistance")
                    print(f"   Helper message: {result.get('helper_message', '')[:100]}...")
                    
                    if test_case['should_trigger_help']:
                        print(f"✅ Correctly triggered help")
                    else:
                        print(f"❌ Unexpectedly triggered help")
                        
                elif result.get('success'):
                    print(f"✅ Generated workflow successfully")
                    print(f"   Workflow name: {result.get('workflow_name', 'N/A')}")
                    
                    if not test_case['should_trigger_help']:
                        print(f"✅ Correctly generated workflow")
                    else:
                        print(f"❌ Should have triggered help instead")
                        
                else:
                    print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
                    
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    print(f"\n✅ Prompt Assistance Testing Complete!")

def test_prompt_helper_module():
    """Test the prompt helper module directly"""
    print(f"\n🔧 Testing Prompt Helper Module...")
    
    try:
        from prompt_helper import PromptHelper, enhance_workflow_generation
        
        helper = PromptHelper()
        
        # Test analysis
        test_inputs = [
            "process csv files",
            "automate daily reports", 
            "connect slack to sheets",
            "help"
        ]
        
        for input_text in test_inputs:
            print(f"\n📝 Testing: '{input_text}'")
            
            # Test analysis
            pattern = helper.analyze_request(input_text)
            print(f"   Detected pattern: {pattern}")
            
            # Test enhancement
            result = enhance_workflow_generation(input_text)
            print(f"   Needs clarification: {result['needs_clarification']}")
            print(f"   Response length: {len(result['helper_response'])} chars")
        
        print(f"✅ Prompt Helper Module working correctly")
        
    except Exception as e:
        print(f"❌ Prompt Helper Module error: {e}")

def main():
    """Run all prompt assistance tests"""
    print("🤖 PROMPT ASSISTANCE SYSTEM TESTS")
    print("=" * 60)
    
    # Test the module directly
    test_prompt_helper_module()
    
    # Test the web endpoints
    test_prompt_assistance()
    
    print(f"\n🎉 All tests completed!")

if __name__ == "__main__":
    main()