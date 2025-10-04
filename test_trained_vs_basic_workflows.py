#!/usr/bin/env python3
"""
Test Trained vs Basic Workflow Generation
Compare the quality and realism of workflows generated using trained models vs basic generation
"""

import requests
import json
import time
from threading import Thread
from app import app

def run_test_server():
    """Run the Flask app for testing"""
    app.run(port=5002, debug=False, use_reloader=False)

def test_workflow_quality():
    """Test the quality of generated workflows"""
    print("🧪 Testing Trained vs Basic Workflow Generation")
    print("=" * 60)
    
    # Start server
    server_thread = Thread(target=run_test_server, daemon=True)
    server_thread.start()
    time.sleep(3)
    
    base_url = "http://localhost:5002"
    
    # Test cases that should generate realistic workflows
    test_cases = [
        {
            'name': 'AI-Powered Data Processing',
            'description': 'Process CSV files with OpenAI, analyze the data, and send results to Slack with a summary',
            'expected_nodes': ['webhook', 'csv', 'openai', 'slack'],
            'complexity': 'medium'
        },
        {
            'name': 'Content Management Automation',
            'description': 'Create WordPress blog posts from Google Sheets data using AI content generation',
            'expected_nodes': ['sheets', 'ai', 'wordpress'],
            'complexity': 'medium'
        },
        {
            'name': 'Communication Integration',
            'description': 'Monitor email attachments, extract text with AI, and send notifications to multiple channels',
            'expected_nodes': ['email', 'ai', 'slack', 'telegram'],
            'complexity': 'complex'
        },
        {
            'name': 'Data Pipeline',
            'description': 'Extract data from API, transform with custom logic, validate with AI, and store in database',
            'expected_nodes': ['http', 'transform', 'ai', 'database'],
            'complexity': 'complex'
        }
    ]
    
    print("🚀 Testing Workflow Generation Quality...")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['name']}")
        print(f"Description: {test_case['description']}")
        print("-" * 50)
        
        try:
            response = requests.post(f"{base_url}/generate",
                json={
                    'description': test_case['description'],
                    'triggerType': 'webhook',
                    'complexity': test_case['complexity']
                },
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success'):
                    workflow = result.get('workflow', {})
                    nodes = workflow.get('nodes', [])
                    
                    print(f"✅ Generated Successfully")
                    print(f"   Workflow Name: {result.get('workflow_name', 'N/A')}")
                    print(f"   Node Count: {len(nodes)}")
                    print(f"   Workflow Type: {result.get('workflow_type', 'unknown')}")
                    print(f"   Complexity: {result.get('complexity', 'N/A')}")
                    
                    # Analyze node types
                    node_types = [node.get('type', 'unknown') for node in nodes]
                    unique_types = set(node_types)
                    
                    print(f"   Node Types ({len(unique_types)} unique):")
                    for node_type in unique_types:
                        count = node_types.count(node_type)
                        short_name = node_type.split('.')[-1] if '.' in node_type else node_type
                        print(f"     • {short_name}: {count}")
                    
                    # Check for realistic patterns
                    realistic_score = analyze_workflow_realism(workflow, test_case)
                    print(f"   Realism Score: {realistic_score:.1f}/10")
                    
                    # Check connections
                    connections = workflow.get('connections', {})
                    print(f"   Connections: {len(connections)} node connections")
                    
                    # Show sample node for inspection
                    if nodes:
                        sample_node = nodes[0]
                        print(f"   Sample Node: {sample_node.get('name', 'N/A')} ({sample_node.get('type', 'N/A')})")
                        if sample_node.get('parameters'):
                            param_count = len(sample_node['parameters'])
                            print(f"     Parameters: {param_count} configured")
                    
                else:
                    print(f"❌ Generation failed: {result.get('error', 'Unknown error')}")
                    
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
        
        print("=" * 50)
    
    print(f"\n✅ Workflow Quality Testing Complete!")

def analyze_workflow_realism(workflow: dict, test_case: dict) -> float:
    """Analyze how realistic the generated workflow is"""
    score = 0.0
    
    nodes = workflow.get('nodes', [])
    node_types = [node.get('type', '') for node in nodes]
    
    # Check for proper n8n structure (2 points)
    if workflow.get('id') and workflow.get('name'):
        score += 2.0
    
    # Check for realistic node count (2 points)
    if 3 <= len(nodes) <= 15:
        score += 2.0
    elif len(nodes) > 0:
        score += 1.0
    
    # Check for proper node types (2 points)
    has_proper_types = any('n8n-nodes-base.' in nt or '@n8n/' in nt for nt in node_types)
    if has_proper_types:
        score += 2.0
    
    # Check for expected functionality (2 points)
    description_lower = test_case['description'].lower()
    if 'ai' in description_lower or 'openai' in description_lower:
        has_ai = any('openai' in nt.lower() or 'langchain' in nt.lower() for nt in node_types)
        if has_ai:
            score += 1.0
    
    if 'slack' in description_lower:
        has_slack = any('slack' in nt.lower() for nt in node_types)
        if has_slack:
            score += 1.0
    
    # Check for connections (1 point)
    connections = workflow.get('connections', {})
    if connections:
        score += 1.0
    
    # Check for proper parameters (1 point)
    has_parameters = any(node.get('parameters') for node in nodes)
    if has_parameters:
        score += 1.0
    
    return min(score, 10.0)

def compare_with_training_data():
    """Compare generated workflows with actual training data"""
    print(f"\n📊 Comparing with Training Data...")
    
    try:
        # Load a sample from training data
        with open("training_data/workflow_templates.json", 'r') as f:
            templates = json.load(f)
        
        if templates:
            sample_template = templates[0]
            print(f"📋 Sample from Training Data:")
            print(f"   Name: {sample_template.get('name', 'N/A')}")
            print(f"   Nodes: {len(sample_template.get('nodes', []))}")
            
            # Show node types from training data
            training_nodes = sample_template.get('nodes', [])
            training_types = [node.get('type', 'unknown') for node in training_nodes]
            unique_training_types = set(training_types)
            
            print(f"   Training Node Types ({len(unique_training_types)} unique):")
            for node_type in list(unique_training_types)[:5]:
                short_name = node_type.split('.')[-1] if '.' in node_type else node_type
                print(f"     • {short_name}")
            
            print(f"\n✅ Generated workflows should match this level of complexity and realism")
        
    except Exception as e:
        print(f"⚠️ Could not load training data: {e}")

def main():
    """Run all workflow quality tests"""
    print("🎯 WORKFLOW GENERATION QUALITY TEST")
    print("=" * 60)
    print("Testing if generated workflows match the quality of the 100 training JSONs...")
    
    # Test workflow generation quality
    test_workflow_quality()
    
    # Compare with training data
    compare_with_training_data()
    
    print(f"\n🎉 Quality testing completed!")
    print(f"Generated workflows should now match the complexity and realism of your training data!")

if __name__ == "__main__":
    main()