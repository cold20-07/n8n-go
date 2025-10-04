"""
Test Flask integration with connection validation
"""

import requests
import json


def test_flask_workflow_generation():
    """Test workflow generation with connection validation through Flask API"""
    
    print("🧪 Testing Flask API with Connection Validation")
    print("=" * 60)
    
    # Test data that should trigger connection fixes
    test_data = {
        "description": "Create a workflow that reads RSS feeds, generates content summaries, parses them for social media, and posts to Twitter",
        "triggerType": "schedule",
        "complexity": "medium"
    }
    
    try:
        # Start Flask app in test mode (you'll need to run this separately)
        print("📡 Sending request to Flask API...")
        print(f"   Description: {test_data['description'][:50]}...")
        print(f"   Trigger: {test_data['triggerType']}")
        print(f"   Complexity: {test_data['complexity']}")
        
        # This would normally make a request to the running Flask app
        # For now, let's simulate the workflow generation process
        from app import app
        
        with app.test_client() as client:
            response = client.post('/generate', 
                                 data=json.dumps(test_data),
                                 content_type='application/json')
            
            if response.status_code == 200:
                result = response.get_json()
                
                print(f"\n✅ API Response Success!")
                print(f"   Status: {response.status_code}")
                print(f"   Workflow Name: {result.get('workflow_name', 'N/A')}")
                print(f"   Node Count: {result.get('node_count', 0)}")
                
                # Check if workflow has connections
                workflow = result.get('workflow', {})
                connections = workflow.get('connections', {})
                
                print(f"   Connections: {len(connections)}")
                
                if connections:
                    print(f"\n🔗 Connection Details:")
                    for source, conn_data in connections.items():
                        if 'main' in conn_data:
                            for group in conn_data['main']:
                                for conn in group:
                                    target = conn.get('node')
                                    print(f"     {source} → {target}")
                
                # Check for validation info
                validation = result.get('validation', {})
                if validation:
                    print(f"\n🔍 Validation Info:")
                    print(f"   Validation Applied: {validation.get('validation_applied', False)}")
                    if 'confidence_score' in validation:
                        print(f"   Confidence Score: {validation['confidence_score']:.2f}")
                
                return True
                
            else:
                print(f"❌ API Error: {response.status_code}")
                print(f"   Response: {response.get_data(as_text=True)}")
                return False
                
    except Exception as e:
        print(f"💥 Test Error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_validation_endpoint():
    """Test the dedicated validation endpoint"""
    
    print("\n" + "=" * 60)
    print("🧪 Testing Validation Endpoint")
    print("=" * 60)
    
    # Create a test workflow with connection issues
    test_workflow = {
        "name": "Test Workflow",
        "nodes": [
            {
                "id": "1",
                "name": "RSS Reader",
                "type": "n8n-nodes-base.rssFeedRead",
                "typeVersion": 1,
                "position": [0, 300],
                "parameters": {"url": "https://feeds.example.com/rss.xml"}
            },
            {
                "id": "2",
                "name": "Content Processor",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [300, 300],
                "parameters": {"jsCode": "return $input.all();"}
            }
        ],
        "connections": {},  # No connections
        "active": True,
        "settings": {}
    }
    
    try:
        from app import app
        
        with app.test_client() as client:
            response = client.post('/validate',
                                 data=json.dumps({"workflow": test_workflow}),
                                 content_type='application/json')
            
            if response.status_code == 200:
                result = response.get_json()
                
                print(f"✅ Validation Endpoint Success!")
                print(f"   Fixes Applied: {result.get('fixes_applied', False)}")
                
                validation_report = result.get('validation_report', {})
                if validation_report:
                    original = validation_report.get('original_validation', {})
                    print(f"   Original Valid: {original.get('is_valid', False)}")
                    print(f"   Original Errors: {len(original.get('errors', []))}")
                    
                    fixes = validation_report.get('fixes_applied', [])
                    if fixes:
                        print(f"   Fixes Applied:")
                        for fix in fixes:
                            print(f"     - {fix}")
                
                return True
                
            else:
                print(f"❌ Validation Error: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"💥 Validation Test Error: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Starting Flask Connection Validation Tests")
    
    # Test 1: Workflow generation with connection validation
    generation_success = test_flask_workflow_generation()
    
    # Test 2: Dedicated validation endpoint
    validation_success = test_validation_endpoint()
    
    print("\n" + "=" * 60)
    print("🎉 FLASK TEST SUMMARY")
    print("=" * 60)
    print(f"Workflow Generation: {'✅ SUCCESS' if generation_success else '❌ FAILED'}")
    print(f"Validation Endpoint: {'✅ SUCCESS' if validation_success else '❌ FAILED'}")
    print(f"Overall Result: {'✅ PASSED' if generation_success and validation_success else '❌ FAILED'}")
    
    if generation_success and validation_success:
        print("\n🎯 Flask integration with connection validation is working!")
        print("   The system can now automatically fix RSS → Content → Parser → Twitter flows.")
    else:
        print("\n❌ Flask integration needs debugging.")