#!/usr/bin/env python3
"""
Test Complex Prompts with Trained Workflow Generation
Tests the most complex prompts to demonstrate the quality of trained generation
"""

import requests
import json
import time
from threading import Thread
from app import app

def run_test_server():
    """Run the Flask app for testing"""
    app.run(port=5003, debug=False, use_reloader=False)

def test_complex_prompts():
    """Test complex prompts with the trained workflow generator"""
    print("🎯 TESTING COMPLEX PROMPTS WITH TRAINED WORKFLOW GENERATION")
    print("=" * 80)
    
    # Start server
    server_thread = Thread(target=run_test_server, daemon=True)
    server_thread.start()
    time.sleep(3)
    
    base_url = "http://localhost:5003"
    
    # Complex test prompts
    complex_prompts = [
        {
            'name': 'Advanced AI-Powered Data Pipeline',
            'description': '''Create an advanced workflow that monitors a webhook for incoming customer support tickets, uses OpenAI GPT-4 to analyze sentiment and categorize the issue type, extracts key entities like product names and customer details, checks against a knowledge base using vector search, generates personalized responses with different AI models based on urgency level, sends notifications to appropriate Slack channels with different formatting for high/low priority, updates a Google Sheet with ticket analytics, and triggers follow-up workflows for escalated cases while maintaining conversation context throughout the entire process.''',
            'complexity': 'complex',
            'expected_features': ['AI analysis', 'Slack integration', 'Google Sheets', 'Conditional logic', 'Multiple AI models']
        },
        {
            'name': 'Multi-Modal Content Generation System',
            'description': '''Build a sophisticated content automation workflow that starts with a scheduled trigger every morning, pulls trending topics from multiple RSS feeds and social media APIs, uses AI to analyze content relevance and engagement potential, generates blog post outlines with SEO optimization, creates multiple content variations using different AI writing styles, generates accompanying images using DALL-E based on the content themes, optimizes the content for different platforms (WordPress, LinkedIn, Twitter), schedules posts across multiple social channels with platform-specific formatting, tracks engagement metrics, and automatically adjusts future content strategy based on performance analytics while maintaining brand voice consistency.''',
            'complexity': 'complex',
            'expected_features': ['Scheduled trigger', 'RSS feeds', 'AI content generation', 'Multi-platform posting', 'Analytics']
        },
        {
            'name': 'Intelligent Document Processing & Workflow',
            'description': '''Design a comprehensive document processing system that receives PDF documents via email attachments, extracts text and images using OCR and AI vision models, classifies document types (invoices, contracts, reports) using machine learning, validates extracted data against business rules, routes documents to appropriate approval workflows based on content and value thresholds, sends notifications to stakeholders with document summaries and action items, integrates with CRM and ERP systems to update relevant records, generates compliance reports, handles exceptions with human-in-the-loop review processes, and maintains audit trails with version control while ensuring data privacy and security throughout the entire pipeline.''',
            'complexity': 'complex',
            'expected_features': ['Email processing', 'OCR/AI vision', 'Document classification', 'Approval workflows', 'CRM integration']
        },
        {
            'name': 'Real-Time Customer Journey Orchestration',
            'description': '''Create an intelligent customer journey workflow that triggers on website events and user behavior, analyzes customer data from multiple touchpoints using AI to predict intent and likelihood to convert, personalizes communication strategies based on customer segment and behavior patterns, sends targeted messages across email, SMS, and push notifications with dynamic content generation, tracks engagement and adjusts messaging frequency and channels in real-time, integrates with marketing automation platforms and CRM systems, handles customer responses and routes them to appropriate teams, escalates high-value prospects to sales with enriched context, measures campaign effectiveness with advanced analytics, and continuously optimizes the journey using machine learning feedback loops while maintaining GDPR compliance and customer preferences.''',
            'complexity': 'complex',
            'expected_features': ['Event triggers', 'AI prediction', 'Multi-channel messaging', 'Real-time optimization', 'Analytics']
        },
        {
            'name': 'Automated Financial Analysis & Reporting',
            'description': '''Develop a complex financial workflow that connects to multiple data sources including bank APIs, accounting software, and market data feeds, performs real-time data validation and anomaly detection using statistical models, categorizes transactions using AI-powered classification, generates automated reconciliation reports with discrepancy highlighting, calculates key financial metrics and KPIs with trend analysis, creates dynamic dashboards with interactive visualizations, sends personalized financial insights to different stakeholder groups via email and Slack with role-based access control, triggers alerts for unusual patterns or threshold breaches, integrates with compliance systems for regulatory reporting, schedules automated backups and data archiving, and provides predictive analytics for cash flow forecasting while maintaining strict security and audit requirements.''',
            'complexity': 'complex',
            'expected_features': ['Multiple data sources', 'AI classification', 'Anomaly detection', 'Dynamic dashboards', 'Compliance reporting']
        }
    ]
    
    print("🚀 Testing Complex Workflow Generation...")
    print("Each test will show the quality and complexity of generated workflows\n")
    
    for i, prompt in enumerate(complex_prompts, 1):
        print(f"📝 TEST {i}/5: {prompt['name']}")
        print("=" * 60)
        print(f"Description Length: {len(prompt['description'])} characters")
        print(f"Expected Features: {', '.join(prompt['expected_features'])}")
        print(f"Complexity: {prompt['complexity']}")
        print("-" * 60)
        
        try:
            # Make request to generate workflow
            response = requests.post(f"{base_url}/generate",
                json={
                    'description': prompt['description'],
                    'triggerType': 'webhook',
                    'complexity': prompt['complexity']
                },
                headers={'Content-Type': 'application/json'},
                timeout=45  # Longer timeout for complex generation
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success'):
                    workflow = result.get('workflow', {})
                    nodes = workflow.get('nodes', [])
                    connections = workflow.get('connections', {})
                    
                    print(f"✅ GENERATION SUCCESSFUL")
                    print(f"   📋 Workflow Name: {result.get('workflow_name', 'N/A')}")
                    print(f"   🔢 Node Count: {len(nodes)} nodes")
                    print(f"   🔗 Connections: {len(connections)} node connections")
                    print(f"   🎯 Generation Type: {result.get('workflow_type', 'unknown')}")
                    print(f"   📊 Complexity Level: {result.get('complexity', 'N/A')}")
                    
                    # Analyze node types in detail
                    node_types = [node.get('type', 'unknown') for node in nodes]
                    unique_types = list(set(node_types))
                    
                    print(f"\n   🧩 NODE ANALYSIS ({len(unique_types)} unique types):")
                    
                    # Categorize node types
                    ai_nodes = [nt for nt in unique_types if any(ai in nt.lower() for ai in ['openai', 'langchain', 'ai', 'gpt', 'claude'])]
                    integration_nodes = [nt for nt in unique_types if any(svc in nt.lower() for svc in ['slack', 'sheets', 'email', 'webhook', 'http'])]
                    processing_nodes = [nt for nt in unique_types if any(proc in nt.lower() for proc in ['set', 'code', 'if', 'merge', 'split'])]
                    
                    if ai_nodes:
                        print(f"      🤖 AI Nodes ({len(ai_nodes)}):")
                        for node in ai_nodes[:3]:  # Show first 3
                            short_name = node.split('.')[-1] if '.' in node else node
                            count = node_types.count(node)
                            print(f"         • {short_name} ({count}x)")
                    
                    if integration_nodes:
                        print(f"      🔗 Integration Nodes ({len(integration_nodes)}):")
                        for node in integration_nodes[:3]:  # Show first 3
                            short_name = node.split('.')[-1] if '.' in node else node
                            count = node_types.count(node)
                            print(f"         • {short_name} ({count}x)")
                    
                    if processing_nodes:
                        print(f"      ⚙️ Processing Nodes ({len(processing_nodes)}):")
                        for node in processing_nodes[:3]:  # Show first 3
                            short_name = node.split('.')[-1] if '.' in node else node
                            count = node_types.count(node)
                            print(f"         • {short_name} ({count}x)")
                    
                    # Check for expected features
                    print(f"\n   ✅ FEATURE VALIDATION:")
                    features_found = 0
                    for feature in prompt['expected_features']:
                        found = check_feature_in_workflow(workflow, feature)
                        status = "✅" if found else "❌"
                        print(f"      {status} {feature}: {'Found' if found else 'Not detected'}")
                        if found:
                            features_found += 1
                    
                    feature_score = (features_found / len(prompt['expected_features'])) * 100
                    print(f"   📊 Feature Coverage: {feature_score:.0f}% ({features_found}/{len(prompt['expected_features'])})")
                    
                    # Calculate overall quality score
                    quality_score = calculate_workflow_quality(workflow, prompt)
                    print(f"   🏆 Overall Quality Score: {quality_score:.1f}/10")
                    
                    # Show sample node for inspection
                    if nodes:
                        sample_node = nodes[1] if len(nodes) > 1 else nodes[0]  # Skip trigger, show processing node
                        print(f"\n   🔍 SAMPLE NODE INSPECTION:")
                        print(f"      Name: {sample_node.get('name', 'N/A')}")
                        print(f"      Type: {sample_node.get('type', 'N/A')}")
                        print(f"      Parameters: {len(sample_node.get('parameters', {}))} configured")
                        if sample_node.get('parameters'):
                            param_keys = list(sample_node['parameters'].keys())[:3]
                            print(f"      Sample Params: {', '.join(param_keys)}")
                    
                    print(f"\n   📄 JSON SIZE: {len(result.get('formatted_json', '{}'))} characters")
                    
                else:
                    print(f"❌ GENERATION FAILED")
                    print(f"   Error: {result.get('error', 'Unknown error')}")
                    if result.get('needs_prompt_help'):
                        print(f"   Helper Message: {result.get('helper_message', '')[:100]}...")
                    
            else:
                print(f"❌ HTTP ERROR: {response.status_code}")
                print(f"   Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ REQUEST FAILED: {e}")
        
        print("\n" + "=" * 80 + "\n")
        
        # Small delay between tests
        time.sleep(2)
    
    print("🎉 COMPLEX PROMPT TESTING COMPLETED!")
    print("=" * 80)

def check_feature_in_workflow(workflow: dict, feature: str) -> bool:
    """Check if a specific feature is present in the workflow"""
    nodes = workflow.get('nodes', [])
    node_types = [node.get('type', '').lower() for node in nodes]
    node_names = [node.get('name', '').lower() for node in nodes]
    
    feature_lower = feature.lower()
    
    # Feature detection logic
    if 'ai' in feature_lower:
        return any('openai' in nt or 'langchain' in nt or 'ai' in nt for nt in node_types)
    elif 'slack' in feature_lower:
        return any('slack' in nt for nt in node_types)
    elif 'google sheets' in feature_lower or 'sheets' in feature_lower:
        return any('sheets' in nt or 'googlesheets' in nt for nt in node_types)
    elif 'email' in feature_lower:
        return any('email' in nt or 'gmail' in nt for nt in node_types)
    elif 'schedule' in feature_lower:
        return any('schedule' in nt or 'cron' in nt for nt in node_types)
    elif 'webhook' in feature_lower:
        return any('webhook' in nt for nt in node_types)
    elif 'conditional' in feature_lower or 'logic' in feature_lower:
        return any('if' in nt or 'switch' in nt for nt in node_types)
    elif 'rss' in feature_lower:
        return any('rss' in nt for nt in node_types)
    elif 'analytics' in feature_lower:
        return any('analytics' in nt or 'tracking' in nt for nt in node_types)
    else:
        # Generic check
        return any(feature_lower in nt or feature_lower in nn for nt in node_types for nn in node_names)

def calculate_workflow_quality(workflow: dict, prompt: dict) -> float:
    """Calculate overall workflow quality score"""
    score = 0.0
    
    nodes = workflow.get('nodes', [])
    connections = workflow.get('connections', {})
    
    # Basic structure (2 points)
    if workflow.get('id') and workflow.get('name'):
        score += 2.0
    
    # Node count appropriate for complexity (2 points)
    node_count = len(nodes)
    if prompt['complexity'] == 'complex':
        if node_count >= 8:
            score += 2.0
        elif node_count >= 5:
            score += 1.0
    else:
        if node_count >= 4:
            score += 2.0
    
    # Real n8n node types (2 points)
    node_types = [node.get('type', '') for node in nodes]
    has_real_types = any('n8n-nodes-base.' in nt or '@n8n/' in nt for nt in node_types)
    if has_real_types:
        score += 2.0
    
    # AI integration when expected (2 points)
    description = prompt['description'].lower()
    if 'ai' in description or 'openai' in description:
        has_ai = any('openai' in nt.lower() or 'langchain' in nt.lower() for nt in node_types)
        if has_ai:
            score += 2.0
    else:
        score += 2.0  # No AI expected, so full points
    
    # Connections (1 point)
    if connections:
        score += 1.0
    
    # Parameters configured (1 point)
    has_params = any(node.get('parameters') for node in nodes)
    if has_params:
        score += 1.0
    
    return min(score, 10.0)

def main():
    """Run complex prompt testing"""
    print("🎯 COMPLEX PROMPT TESTING WITH TRAINED WORKFLOW GENERATION")
    print("Testing the most sophisticated prompts to demonstrate system capabilities")
    print("=" * 80)
    
    test_complex_prompts()

if __name__ == "__main__":
    main()