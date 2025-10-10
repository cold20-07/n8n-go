#!/usr/bin/env python3
"""
Test Gemini with a simple workflow generation request
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def test_simple_workflow():
    """Test Gemini with a simple workflow request"""
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ No API key found")
        return
    
    model = "gemini-2.5-flash"
    base_url = "https://generativelanguage.googleapis.com/v1"
    url = f"{base_url}/models/{model}:generateContent?key={api_key}"
    
    # Simple, short prompt
    prompt = """Create a simple n8n workflow JSON for: "Send email notifications"

Return only valid JSON with this structure:
{
  "name": "Email Notification Workflow",
  "nodes": [
    {
      "id": "trigger",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [100, 100],
      "parameters": {}
    }
  ],
  "connections": {},
  "active": true
}"""
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": 1024
        }
    }
    
    try:
        print("📡 Testing simple workflow generation...")
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=10)
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS! Gemini generated workflow!")
            
            print(f"Raw response: {json.dumps(data, indent=2)}")
            
            if 'candidates' in data and data['candidates']:
                candidate = data['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    content = candidate['content']['parts'][0]['text']
                    print(f"🤖 Generated workflow:")
                    print(content[:500] + "..." if len(content) > 500 else content)
                else:
                    print("⚠️ Unexpected response structure")
                    return
                
                # Try to parse as JSON
                try:
                    # Clean the response
                    clean_content = content.strip()
                    if clean_content.startswith('```json'):
                        clean_content = clean_content[7:]
                    if clean_content.endswith('```'):
                        clean_content = clean_content[:-3]
                    
                    workflow = json.loads(clean_content)
                    print("✅ Valid JSON workflow generated!")
                    print(f"   Name: {workflow.get('name', 'N/A')}")
                    print(f"   Nodes: {len(workflow.get('nodes', []))}")
                    
                except json.JSONDecodeError as e:
                    print(f"⚠️ JSON parsing failed: {e}")
                    
        else:
            print(f"❌ FAILED! Status: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_simple_workflow()