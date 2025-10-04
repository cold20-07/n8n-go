"""
Test the simple connection fix in Flask
"""

import json
from app import app


def test_simple_connection_fix():
    """Test that the simple connection fix works in Flask"""
    
    print("🧪 Testing Simple Connection Fix in Flask")
    print("=" * 50)
    
    test_data = {
        "description": "Read RSS feeds, generate content, parse it, and post to Twitter",
        "triggerType": "schedule",
        "complexity": "medium"
    }
    
    try:
        with app.test_client() as client:
            response = client.post('/generate',
                                 data=json.dumps(test_data),
                                 content_type='application/json')
            
            if response.status_code == 200:
                result = response.get_json()
                workflow = result.get('workflow', {})
                connections = workflow.get('connections', {})
                nodes = workflow.get('nodes', [])
                
                print(f"✅ Flask Response Success!")
                print(f"   Workflow: {workflow.get('name', 'N/A')}")
                print(f"   Nodes: {len(nodes)}")
                print(f"   Connections: {len(connections)}")
                
                if connections:
                    print(f"\n🔗 Connections Found:")
                    connection_count = 0
                    for source, conn_data in connections.items():
                        if 'main' in conn_data:
                            for group in conn_data['main']:
                                for conn in group:
                                    target = conn.get('node')
                                    print(f"     {source} → {target}")
                                    connection_count += 1
                    
                    print(f"\n📊 Connection Analysis:")
                    print(f"   Total connections: {connection_count}")
                    print(f"   Expected connections: {max(0, len(nodes) - 1)}")
                    
                    if connection_count >= max(0, len(nodes) - 1):
                        print(f"   Status: ✅ PROPERLY CONNECTED")
                        return True
                    else:
                        print(f"   Status: ❌ MISSING CONNECTIONS")
                        return False
                else:
                    print(f"   Status: ❌ NO CONNECTIONS FOUND")
                    return False
                    
            else:
                print(f"❌ Flask Error: {response.status_code}")
                print(f"   Response: {response.get_data(as_text=True)}")
                return False
                
    except Exception as e:
        print(f"💥 Test Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_simple_connection_fix()
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Result: {'✅ SUCCESS' if success else '❌ FAILED'}")
    
    if success:
        print("   The simple connection fix is working in Flask!")
        print("   RSS → Content → Parser → Twitter flows should now be connected.")
    else:
        print("   The connection fix needs more work.")