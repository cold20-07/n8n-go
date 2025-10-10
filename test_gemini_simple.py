#!/usr/bin/env python3
"""
Simple test to check if Gemini API is working
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def test_gemini_simple():
    """Test basic Gemini API functionality"""
    
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ No Gemini API key found")
        return
    
    print(f"🧪 Testing basic Gemini API functionality")
    print(f"🔑 API Key: {api_key[:10]}...")
    
    # Simple test prompt
    simple_prompt = """Create a simple n8n workflow JSON for monitoring RSS feeds.

Requirements:
- Use webhook trigger
- Include RSS feed reader
- Add data processing
- Return only valid JSON

Example format:
{
  "name": "RSS Monitor",
  "nodes": [...],
  "connections": {...}
}"""
    
    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": simple_prompt}]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "topK": 40,
            "topP": 0.8,
            "maxOutputTokens": 2048
        }
    }
    
    try:
        print("📡 Making API request...")
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=30)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            content = data["candidates"][0]["content"]["parts"][0]["text"]
            print(f"✅ API call successful!")
            print(f"📝 Response length: {len(content)} characters")
            print(f"🔍 Response preview: {content[:200]}...")
            
            # Try to parse as JSON
            try:
                # Clean the response
                content = content.strip()
                if content.startswith('```json'):
                    content = content[7:]
                if content.endswith('```'):
                    content = content[:-3]
                
                workflow = json.loads(content)
                print(f"✅ Valid JSON returned!")
                print(f"📝 Workflow name: {workflow.get('name', 'Unnamed')}")
                print(f"🔗 Nodes: {len(workflow.get('nodes', []))}")
                
            except json.JSONDecodeError as e:
                print(f"⚠️ Response is not valid JSON: {e}")
                print(f"Raw content: {content}")
        
        else:
            print(f"❌ API call failed: {response.status_code}")
            print(f"Error: {response.text}")
            
            # Check common error causes
            if response.status_code == 400:
                print("\n🔍 Possible causes for 400 error:")
                print("   - Invalid API key format")
                print("   - Request payload too large")
                print("   - Invalid request structure")
                
            elif response.status_code == 403:
                print("\n🔍 Possible causes for 403 error:")
                print("   - API key not authorized")
                print("   - Quota exceeded")
                print("   - Geographic restrictions")
    
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_gemini_simple()