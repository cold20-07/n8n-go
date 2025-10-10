#!/usr/bin/env python3
"""
Test the Gemini fix with the correct model name
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def test_gemini_fix():
    """Test if the Gemini model fix works"""
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ No API key found")
        return
    
    print(f"🔑 Testing with API key: {api_key[:10]}...")
    
    # Test the exact configuration we're using
    model = "gemini-2.5-flash"
    base_url = "https://generativelanguage.googleapis.com/v1"
    url = f"{base_url}/models/{model}:generateContent?key={api_key}"
    
    print(f"🌐 Testing URL: {url}")
    
    payload = {
        "contents": [{
            "parts": [{"text": "Hello! Please respond with 'Gemini is working!' to confirm the connection."}]
        }],
        "generationConfig": {
            "temperature": 0.3,
            "topK": 40,
            "topP": 0.8,
            "maxOutputTokens": 100
        }
    }
    
    try:
        print("📡 Sending request...")
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=30)
        
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS! Gemini API is working!")
            
            if 'candidates' in data and data['candidates']:
                content = data['candidates'][0]['content']['parts'][0]['text']
                print(f"🤖 Gemini response: {content}")
            else:
                print("⚠️ Unexpected response format")
                print(f"Response: {json.dumps(data, indent=2)}")
        else:
            print(f"❌ FAILED! Status: {response.status_code}")
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_gemini_fix()