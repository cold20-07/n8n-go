#!/usr/bin/env python3
"""
Test Flask App Directly
Test the actual Flask app endpoint to see what JSON is being returned
"""

import json
import requests
import time
import threading
import subprocess
import sys

def start_flask_app():
    """Start the Flask app in background"""
    try:
        # Start Flask app
        process = subprocess.Popen([sys.executable, 'app.py'], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE)
        
        # Wait a moment for it to start
        time.sleep(3)
        
        return process
    except Exception as e:
        print(f"Failed to start Flask app: {e}")
        return None

def test_flask_endpoint():
    """Test the Flask app endpoint directly"""
    
    print("🔍 TESTING FLASK APP ENDPOINT DIRECTLY")
    print("=" * 80)
    
    # Test data
    test_data = {
        "description": "Create a workflow that sends a Slack notification when a webhook is triggered",
        "trigger_type": "webhook",
        "complexity": "simple"
    }
    
    print(f"📝 Test request:")
    print(f"   Description: {test_data['description']}")
    print(f"   Trigger: {test_data['trigger_type']}")
    print(f"   Complexity: {test_data['complexity']}")
    
    try:
        # Make request to Flask app
        response = requests.post(
            'http://localhost:5000/generate',
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"\n📡 Response:")
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            
            print(f"\n✅ SUCCESS! Response received:")
            print(f"   Success: {result.get('success')}")
            print(f"   Workflow name: {result.get('workflow_name')}")
            print(f"   Node count: {result.get('node_count')}")
            print(f"   Workflow type: {result.get('workflow_type')}")
            
            # Get the actual workflow
            workflow = result.get('workflow', {})
            nodes = workflow.get('nodes', [])
            connections = workflow.get('connections', {})
            
            print(f"\n📊 WORKFLOW ANALYSIS:")
            print(f"   Total nodes: {len(nodes)}")
            print(f"   Total connections: {len(connections)}")
            
            print(f"\n📋 NODES:")
            for i, node in enumerate(nodes, 1):
                print(f"   {i}. {node.get('name')} ({node.get('type')})")
                print(f"      ID: {node.get('id')}")
                print(f"      Position: {node.get('position')}")
            
            print(f"\n🔗 CONNECTIONS:")
            if connections:
                for source, conn_data in connections.items():
                    targets = conn_data.get('main', [[]])[0]
                    for target in targets:
                        target_name = target.get('node')
                        print(f"   {source} → {target_name}")
            else:
                print("   ❌ NO CONNECTIONS FOUND!")
            
            # Save the complete response
            with open('flask_response.json', 'w') as f:
                json.dump(result, f, indent=2)
            
            print(f"\n📁 Complete response saved to: flask_response.json")
            
            # Check for disconnected nodes
            node_names = [node.get('name') for node in nodes]
            connected_sources = set(connections.keys())
            connected_targets = set()
            
            for conn_data in connections.values():
                targets = conn_data.get('main', [[]])[0]
                for target in targets:
                    connected_targets.add(target.get('node'))
            
            all_connected = connected_sources | connected_targets
            disconnected = set(node_names) - all_connected
            
            if disconnected:
                print(f"\n🚨 DISCONNECTED NODES FOUND: {list(disconnected)}")
                print("   These nodes are not connected to anything!")
            else:
                print(f"\n✅ ALL NODES ARE CONNECTED")
            
            return len(nodes), len(connections), list(disconnected) if disconnected else []
            
        else:
            print(f"\n❌ ERROR Response:")
            print(f"   Status: {response.status_code}")
            print(f"   Text: {response.text}")
            return 0, 0, []
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Could not connect to Flask app")
        print("   Make sure the Flask app is running on http://localhost:5000")
        return 0, 0, []
    except Exception as e:
        print(f"\n❌ Request failed: {e}")
        return 0, 0, []

def test_without_flask():
    """Test the generation logic without Flask"""
    
    print(f"\n🧪 TESTING WITHOUT FLASK (Direct Generator)")
    print("=" * 60)
    
    try:
        from enhanced_workflow_generator import generate_enhanced_workflow
        
        workflow = generate_enhanced_workflow(
            "Create a workflow that sends a Slack notification when a webhook is triggered",
            'webhook',
            'simple'
        )
        
        nodes = workflow.get('nodes', [])
        connections = workflow.get('connections', {})
        
        print(f"   Direct generator result:")
        print(f"   Nodes: {len(nodes)}")
        print(f"   Connections: {len(connections)}")
        
        for i, node in enumerate(nodes, 1):
            print(f"      {i}. {node.get('name')}")
        
        for source, conn_data in connections.items():
            target = conn_data['main'][0][0]['node']
            print(f"      {source} → {target}")
        
        return len(nodes), len(connections)
        
    except Exception as e:
        print(f"   ❌ Direct generator failed: {e}")
        return 0, 0

def main():
    """Test both Flask app and direct generator"""
    
    print("🔍 COMPREHENSIVE CONNECTION TEST")
    print("=" * 80)
    print("Testing both Flask app and direct generator to find connection issues")
    print("=" * 80)
    
    # Test direct generator first
    direct_nodes, direct_connections = test_without_flask()
    
    # Test Flask app
    print(f"\n🌐 TESTING FLASK APP")
    print("=" * 60)
    print("Starting Flask app... (this may take a moment)")
    
    flask_process = start_flask_app()
    
    if flask_process:
        try:
            flask_nodes, flask_connections, disconnected = test_flask_endpoint()
            
            print(f"\n📊 COMPARISON:")
            print(f"   Direct generator: {direct_nodes} nodes, {direct_connections} connections")
            print(f"   Flask app: {flask_nodes} nodes, {flask_connections} connections")
            
            if disconnected:
                print(f"   🚨 Flask app has disconnected nodes: {disconnected}")
            
            if direct_nodes == flask_nodes and direct_connections == flask_connections and not disconnected:
                print(f"\n✅ BOTH WORK PERFECTLY!")
                print("   The issue might be in the frontend display")
            elif disconnected:
                print(f"\n🚨 FLASK APP HAS CONNECTION ISSUES!")
                print("   The Flask app is creating disconnected nodes")
            else:
                print(f"\n⚠️ RESULTS DIFFER - NEED INVESTIGATION")
            
        finally:
            # Clean up Flask process
            flask_process.terminate()
            flask_process.wait()
    else:
        print("❌ Could not start Flask app for testing")

if __name__ == "__main__":
    main()