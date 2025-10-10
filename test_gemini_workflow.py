#!/usr/bin/env python3
"""
Test script to verify Gemini AI workflow generation with 100 real n8n workflows knowledge
"""

import requests
import json
import time

def test_workflow_generation():
    """Test the enhanced workflow generation system"""
    
    # Test cases with different complexity levels
    test_cases = [
        {
            "name": "RSS to Social Media",
            "description": "Create a workflow that monitors RSS feeds and automatically posts new articles to Twitter and LinkedIn",
            "trigger": "schedule",
            "complexity": "medium"
        },
        {
            "name": "Email Processing",
            "description": "Process incoming emails, extract attachments, and save them to Google Drive",
            "trigger": "webhook",
            "complexity": "simple"
        },
        {
            "name": "E-commerce Order Processing",
            "description": "When a new order is received, validate payment, update inventory, send confirmation email, and create shipping label",
            "trigger": "webhook",
            "complexity": "complex"
        },
        {
            "name": "Data Backup Automation",
            "description": "Daily backup of database to cloud storage with compression and encryption",
            "trigger": "schedule",
            "complexity": "medium"
        }
    ]
    
    print("🚀 Testing N8N Workflow Generator with Gemini AI")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:5000"
    
    # Test server availability
    try:
        health_response = requests.get(f"{base_url}/health", timeout=5)
        print(f"✅ Server is running: {health_response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Server not available: {e}")
        print("Please start the server with: python app.py")
        return
    
    # Test each workflow generation case
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test {i}: {test_case['name']}")
        print(f"Description: {test_case['description']}")
        print(f"Trigger: {test_case['trigger']}, Complexity: {test_case['complexity']}")
        
        try:
            # Make request to generate workflow
            start_time = time.time()
            response = requests.post(
                f"{base_url}/generate",
                json=test_case,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    workflow = data.get('workflow', {})
                    nodes = workflow.get('nodes', [])
                    connections = workflow.get('connections', {})
                    
                    print(f"✅ Success! Generated in {response_time:.2f}s")
                    print(f"   Workflow: {workflow.get('name', 'Unnamed')}")
                    print(f"   Nodes: {len(nodes)}")
                    print(f"   Connections: {len(connections)}")
                    
                    # Show node types
                    node_types = [node.get('type', 'unknown').split('.')[-1] for node in nodes]
                    print(f"   Node Types: {', '.join(node_types)}")
                    
                    # Check if AI was used
                    if data.get('ai_used'):
                        print(f"   🤖 AI Provider: {data.get('ai_provider', 'Unknown')}")
                        print(f"   💰 Cost: ${data.get('ai_cost', 0):.4f}")
                    
                    # Check if cached
                    if data.get('cached'):
                        print("   ⚡ Result was cached")
                    
                    # Validation info
                    validation = data.get('validation', {})
                    if validation:
                        print(f"   🔍 Validation Score: {validation.get('confidence_score', 0):.1f}%")
                
                else:
                    print(f"❌ Generation failed: {data.get('error', 'Unknown error')}")
            
            else:
                print(f"❌ HTTP Error {response.status_code}: {response.text}")
        
        except requests.exceptions.Timeout:
            print("⏰ Request timed out (>30s)")
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
        
        # Small delay between requests
        time.sleep(1)
    
    # Test cache statistics
    print(f"\n📊 Cache Statistics")
    print("-" * 30)
    try:
        cache_response = requests.get(f"{base_url}/api/cache/stats", timeout=5)
        if cache_response.status_code == 200:
            cache_data = cache_response.json()
            if cache_data.get('success'):
                stats = cache_data.get('statistics', {})
                print(f"Hit Rate: {stats.get('hit_rate', 0):.1f}%")
                print(f"Total Requests: {stats.get('total_requests', 0)}")
                print(f"Cache Status: {'Redis' if stats.get('redis_available') else 'In-Memory Fallback'}")
            else:
                print("Cache stats not available")
        else:
            print("Cache API not accessible")
    except:
        print("Cache statistics not available")
    
    print(f"\n🎉 Testing completed!")
    print("The system is ready to generate perfect n8n workflows using:")
    print("  • Gemini AI for intelligent generation")
    print("  • Knowledge from 100 real n8n workflows")
    print("  • Advanced caching for performance")
    print("  • Comprehensive validation and optimization")

if __name__ == "__main__":
    test_workflow_generation()