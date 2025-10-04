#!/usr/bin/env python3
"""Debug Response Structure"""

import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app import app

def debug_response():
    """Debug the actual response structure"""
    print("🔍 Debugging Response Structure")
    print("=" * 40)
    
    app.config['TESTING'] = True
    client = app.test_client()
    
    response = client.post('/generate',
                          data=json.dumps({
                              'description': 'Create a simple webhook workflow',
                              'trigger_type': 'webhook'
                          }),
                          content_type='application/json')
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data = json.loads(response.data)
            print(f"Response Keys: {list(data.keys())}")
            
            # Check each key
            for key, value in data.items():
                print(f"\n{key}:")
                if isinstance(value, dict):
                    print(f"  Type: dict with keys: {list(value.keys())}")
                    if key == 'workflow' and 'nodes' in value:
                        print(f"  Nodes count: {len(value['nodes'])}")
                        if len(value['nodes']) > 0:
                            print(f"  First node: {value['nodes'][0].get('name', 'unnamed')}")
                elif isinstance(value, str):
                    print(f"  Type: string (length: {len(value)})")
                    if key == 'formatted_json':
                        try:
                            parsed = json.loads(value)
                            print(f"  Parsed JSON keys: {list(parsed.keys())}")
                            if 'nodes' in parsed:
                                print(f"  Nodes in formatted_json: {len(parsed['nodes'])}")
                        except:
                            print("  Cannot parse as JSON")
                else:
                    print(f"  Type: {type(value)}, Value: {value}")
            
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            print(f"Raw response: {response.data.decode('utf-8')}")

if __name__ == "__main__":
    debug_response()