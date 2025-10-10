#!/usr/bin/env python3
"""
Check available Gemini models
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

def check_available_models():
    """Check what Gemini models are available"""
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        print("❌ No Gemini API key found")
        return
    
    print(f"🔑 Using API key: {api_key[:10]}...")
    
    # Try different API versions and endpoints
    endpoints = [
        "https://generativelanguage.googleapis.com/v1/models",
        "https://generativelanguage.googleapis.com/v1beta/models"
    ]
    
    for endpoint in endpoints:
        print(f"\n🌐 Checking endpoint: {endpoint}")
        
        try:
            response = requests.get(f"{endpoint}?key={api_key}", timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                models = data.get('models', [])
                print(f"   Found {len(models)} models:")
                
                for model in models[:10]:  # Show first 10
                    name = model.get('name', 'Unknown')
                    display_name = model.get('displayName', 'Unknown')
                    supported_methods = model.get('supportedGenerationMethods', [])
                    
                    if 'generateContent' in supported_methods:
                        print(f"   ✅ {name} ({display_name}) - Supports generateContent")
                    else:
                        print(f"   ⚠️ {name} ({display_name}) - Methods: {supported_methods}")
                
                if len(models) > 10:
                    print(f"   ... and {len(models) - 10} more models")
                    
            else:
                print(f"   Error: {response.text[:200]}")
                
        except Exception as e:
            print(f"   Exception: {e}")

def test_specific_models():
    """Test specific model names"""
    api_key = os.getenv('GEMINI_API_KEY')
    
    if not api_key:
        return
    
    # Common model names to try
    models_to_test = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-latest", 
        "gemini-1.5-pro",
        "gemini-1.5-pro-latest",
        "gemini-pro",
        "models/gemini-1.5-flash",
        "models/gemini-1.5-flash-latest",
        "models/gemini-1.5-pro",
        "models/gemini-1.5-pro-latest"
    ]
    
    base_urls = [
        "https://generativelanguage.googleapis.com/v1",
        "https://generativelanguage.googleapis.com/v1beta"
    ]
    
    print(f"\n🧪 Testing specific model names...")
    
    for base_url in base_urls:
        print(f"\n📡 Testing with {base_url}:")
        
        for model in models_to_test:
            url = f"{base_url}/models/{model}:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": "Hello, just testing if this model works. Please respond with 'OK'."}]
                }]
            }
            
            try:
                response = requests.post(url, json=payload, timeout=10)
                
                if response.status_code == 200:
                    print(f"   ✅ {model} - WORKS!")
                    data = response.json()
                    if 'candidates' in data and data['candidates']:
                        content = data['candidates'][0]['content']['parts'][0]['text']
                        print(f"      Response: {content[:50]}...")
                    break  # Found working model
                else:
                    print(f"   ❌ {model} - {response.status_code}: {response.text[:100]}...")
                    
            except Exception as e:
                print(f"   ❌ {model} - Exception: {str(e)[:100]}...")

if __name__ == "__main__":
    check_available_models()
    test_specific_models()