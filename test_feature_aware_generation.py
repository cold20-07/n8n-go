#!/usr/bin/env python3
"""
Test Feature-Aware Workflow Generation
Tests the enhanced system with comprehensive feature detection
"""

import requests
import json
import time
from threading import Thread
from app import app

def run_test_server():
    """Run the Flask app for testing"""
    app.run(port=5004, debug=False, use_reloader=False)

def test_feature_detection():
    """Test comprehensive feature detection"""
    print("🎯 TESTING FEATURE-AWARE WORKFLOW GENERATION")
    print("=" * 80)
    
    # Start server
    server_thread = Thread(target=run_test_server, daemon=True)
    server_thread.start()
    time.sleep(3)
    
    base_url = "http://localhost:5004"
    
    # Test cases with specific features
    test_cases = [
        {
            'name': 'AI + Slack + Google Sheets Integration',
            'description': 'Use OpenAI to analyze customer feedback from Slack, categorize issues, and update Google Sheets with insights',
            'expected_features': {
                'AI': ['OpenAI', 'LangChain'],
                'Communication': ['Slack'],
                'Data': ['Google Sheets'],
                'Processing': ['Conditional logic']
            }
        },
        {
            'name': 'Multi-Channel Content Publishing',
            'description': 'Create blog posts with AI, publish to WordPress, share on Twitter and LinkedIn, track analytics',
            'expected_features': {
                'AI': ['Content generation'],
                'CMS': ['WordPress'],
                'Social': ['Twitter', 'LinkedIn'],
                'Analytics': ['Tracking']
            }
        },
        {
            'name': 'Document Processing Pipeline',
            'description': 'Process PDF documents with OCR, extract data with AI, validate information, send email notifications',
            'expected_features': {
                'Document': ['PDF processing', 'OCR'],
                'AI': ['Data extraction'],
                'Communication': ['Email'],
                'Processing': ['Validation']
            }
        },
        {
            'name': 'E-commerce Order Processing',
            'description': 'Monitor webhook for new orders, update inventory in database, send confirmation emails, create invoices',
            'expected_features': {
                'Triggers': ['Webhook'],
                'Data': ['Database'],
                'Communication': ['Email'],
                'Processing': ['Conditional logic']
            }
        },
        {
            'name': 'Customer Support Automation',
            'description': 'Analyze support tickets with AI, route to appropriate teams via Slack, update CRM records, generate reports',
            'expected_features': {
                'AI': ['Text analysis'],
                'Communication': ['Slack'],
                'CRM': ['Customer records'],
                'Processing': ['Routing logic']
            }
        }
    ]
    
    print("🚀 Testing Feature Detection and Workflow Generation...")
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 TEST {i}/5: {test_case['name']}")
        print("=" * 60)
        print(f"Description: {test_case['description']}")
        print(f"Expected Features: {list(test_case['expected_features'].keys())}")
        print("-" * 60)
        
        try:
            response = requests.post(f"{base_url}/generate",
                json={
                    'description': test_case['description'],
                    'triggerType': 'webhook',
                    'complexity': 'medium'
                },
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success'):
                    workflow = result.get('workflow', {})
                    nodes = workflow.get('nodes', [])
                    
                    print(f"✅ GENERATION SUCCESSFUL")
                    print(f"   📋 Workflow Name: {result.get('workflow_name', 'N/A')}")
                    print(f"   🔢 Node Count: {len(nodes)} nodes")
                    print(f"   🎯 Generation Type: {result.get('workflow_type', 'unknown')}")
                    
                    # Analyze detected features
                    detected_features = analyze_workflow_features(workflow)
                    print(f"\n   🔍 DETECTED FEATURES:")
                    
                    for category, features in detected_features.items():
                        if features:
                            print(f"      {category}: {', '.join(features)}")
                    
                    # Validate expected features
                    print(f"\n   ✅ FEATURE VALIDATION:")
                    validation_score = validate_expected_features(detected_features, test_case['expected_features'])
                    
                    for expected_category, expected_items in test_case['expected_features'].items():
                        detected_items = detected_features.get(expected_category, [])
                        if detected_items:
                            print(f"      ✅ {expected_category}: {', '.join(detected_items)}")
                        else:
                            print(f"      ❌ {expected_category}: Not detected")
                    
                    print(f"   📊 Feature Detection Score: {validation_score:.0f}%")
                    
                    # Show node type diversity
                    node_types = [node.get('type', 'unknown') for node in nodes]
                    unique_types = set(node_types)
                    
                    print(f"\n   🧩 NODE TYPE ANALYSIS:")
                    print(f"      Total Nodes: {len(nodes)}")
                    print(f"      Unique Types: {len(unique_types)}")
                    
                    # Categorize node types
                    ai_nodes = [nt for nt in unique_types if any(ai in nt.lower() for ai in ['openai', 'langchain', 'ai', 'gpt'])]
                    service_nodes = [nt for nt in unique_types if any(svc in nt.lower() for svc in ['slack', 'sheets', 'email', 'twitter', 'wordpress'])]
                    
                    if ai_nodes:
                        print(f"      🤖 AI Nodes: {len(ai_nodes)}")
                        for node in ai_nodes[:2]:
                            short_name = node.split('.')[-1] if '.' in node else node
                            print(f"         • {short_name}")
                    
                    if service_nodes:
                        print(f"      🔗 Service Nodes: {len(service_nodes)}")
                        for node in service_nodes[:3]:
                            short_name = node.split('.')[-1] if '.' in node else node
                            print(f"         • {short_name}")
                    
                    # Overall quality assessment
                    quality_score = assess_workflow_quality(workflow, test_case)
                    print(f"\n   🏆 Overall Quality Score: {quality_score:.1f}/10")
                    
                else:
                    print(f"❌ GENERATION FAILED: {result.get('error', 'Unknown error')}")
                    
            else:
                print(f"❌ HTTP ERROR: {response.status_code}")
                
        except Exception as e:
            print(f"❌ REQUEST FAILED: {e}")
        
        print("=" * 80)
    
    print("\n🎉 FEATURE-AWARE TESTING COMPLETED!")

def analyze_workflow_features(workflow: dict) -> dict:
    """Analyze what features are present in the generated workflow"""
    nodes = workflow.get('nodes', [])
    node_types = [node.get('type', '').lower() for node in nodes]
    
    detected_features = {
        'AI': [],
        'Communication': [],
        'Data': [],
        'CMS': [],
        'Social': [],
        'Document': [],
        'Analytics': [],
        'Processing': [],
        'Triggers': []
    }
    
    # AI features
    if any('openai' in nt for nt in node_types):
        detected_features['AI'].append('OpenAI')
    if any('langchain' in nt for nt in node_types):
        detected_features['AI'].append('LangChain')
    if any('claude' in nt for nt in node_types):
        detected_features['AI'].append('Claude')
    
    # Communication features
    if any('slack' in nt for nt in node_types):
        detected_features['Communication'].append('Slack')
    if any('email' in nt or 'gmail' in nt for nt in node_types):
        detected_features['Communication'].append('Email')
    if any('telegram' in nt for nt in node_types):
        detected_features['Communication'].append('Telegram')
    
    # Data features
    if any('sheets' in nt for nt in node_types):
        detected_features['Data'].append('Google Sheets')
    if any('database' in nt or 'postgres' in nt or 'mysql' in nt for nt in node_types):
        detected_features['Data'].append('Database')
    
    # CMS features
    if any('wordpress' in nt for nt in node_types):
        detected_features['CMS'].append('WordPress')
    
    # Social features
    if any('twitter' in nt for nt in node_types):
        detected_features['Social'].append('Twitter')
    if any('linkedin' in nt for nt in node_types):
        detected_features['Social'].append('LinkedIn')
    
    # Processing features
    if any('if' in nt or 'switch' in nt for nt in node_types):
        detected_features['Processing'].append('Conditional Logic')
    if any('code' in nt for nt in node_types):
        detected_features['Processing'].append('Custom Code')
    
    # Triggers
    if any('webhook' in nt for nt in node_types):
        detected_features['Triggers'].append('Webhook')
    if any('schedule' in nt for nt in node_types):
        detected_features['Triggers'].append('Schedule')
    
    return detected_features

def validate_expected_features(detected: dict, expected: dict) -> float:
    """Calculate percentage of expected features that were detected"""
    total_expected = sum(len(items) for items in expected.values())
    if total_expected == 0:
        return 100.0
    
    detected_count = 0
    for category, expected_items in expected.items():
        detected_items = detected.get(category, [])
        for expected_item in expected_items:
            if any(expected_item.lower() in detected_item.lower() for detected_item in detected_items):
                detected_count += 1
    
    return (detected_count / total_expected) * 100

def assess_workflow_quality(workflow: dict, test_case: dict) -> float:
    """Assess overall workflow quality"""
    score = 0.0
    nodes = workflow.get('nodes', [])
    
    # Basic structure (2 points)
    if workflow.get('name') and len(nodes) > 0:
        score += 2.0
    
    # Appropriate complexity (2 points)
    if len(nodes) >= 5:
        score += 2.0
    elif len(nodes) >= 3:
        score += 1.0
    
    # Real n8n node types (2 points)
    node_types = [node.get('type', '') for node in nodes]
    real_types = sum(1 for nt in node_types if 'n8n-nodes-base.' in nt or '@n8n/' in nt)
    if real_types >= len(nodes) * 0.8:
        score += 2.0
    elif real_types >= len(nodes) * 0.5:
        score += 1.0
    
    # Feature detection (2 points)
    detected_features = analyze_workflow_features(workflow)
    expected_features = test_case['expected_features']
    feature_score = validate_expected_features(detected_features, expected_features)
    score += (feature_score / 100) * 2.0
    
    # Connections (1 point)
    connections = workflow.get('connections', {})
    if connections:
        score += 1.0
    
    # Parameters (1 point)
    has_params = any(node.get('parameters') for node in nodes)
    if has_params:
        score += 1.0
    
    return min(score, 10.0)

def main():
    """Run feature-aware testing"""
    print("🎯 FEATURE-AWARE WORKFLOW GENERATION TESTING")
    print("Testing comprehensive feature detection and workflow generation")
    print("=" * 80)
    
    test_feature_detection()

if __name__ == "__main__":
    main()