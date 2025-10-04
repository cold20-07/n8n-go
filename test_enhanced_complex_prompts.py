#!/usr/bin/env python3
"""
Test Enhanced Complex Prompts
Tests the same complex prompts that were failing before to validate fixes
"""

import json
import requests
import time
from enhanced_workflow_generator import EnhancedWorkflowGenerator

def test_complex_prompts_enhanced():
    """Test the same complex prompts with enhanced generator"""
    
    print("🎯 TESTING COMPLEX PROMPTS WITH ENHANCED WORKFLOW GENERATION")
    print("=" * 80)
    print("Testing the exact same prompts that were failing before")
    print("=" * 80)
    
    # The exact same test cases that were failing
    test_cases = [
        {
            'name': 'Advanced AI-Powered Data Pipeline',
            'description': 'Create an AI-powered workflow that monitors Slack messages, uses OpenAI to analyze sentiment and categorize topics, stores results in Google Sheets, and sends notifications based on urgency levels with conditional logic and multiple AI models',
            'expected_features': ['AI analysis', 'Slack integration', 'Google Sheets', 'Conditional logic', 'Multiple AI models'],
            'complexity': 'complex'
        },
        {
            'name': 'Multi-Modal Content Generation System',
            'description': 'Build a multi-modal content generation system with scheduled triggers, RSS feeds, AI content generation, and multi-platform posting to Twitter and LinkedIn with analytics tracking',
            'expected_features': ['Scheduled trigger', 'RSS feeds', 'AI content generation', 'Multi-platform posting', 'Analytics'],
            'complexity': 'complex'
        },
        {
            'name': 'Intelligent Document Processing & Workflow',
            'description': 'Design an intelligent document processing workflow with email triggers, OCR processing, AI document classification, approval workflows, and CRM integration',
            'expected_features': ['Email processing', 'OCR/AI vision', 'Document classification', 'Approval workflows', 'CRM integration'],
            'complexity': 'complex'
        },
        {
            'name': 'Real-Time Customer Journey Orchestration',
            'description': 'Create a real-time customer journey orchestration with event triggers, AI prediction, multi-channel messaging, real-time optimization, and analytics',
            'expected_features': ['Event triggers', 'AI prediction', 'Multi-channel messaging', 'Real-time optimization', 'Analytics'],
            'complexity': 'complex'
        },
        {
            'name': 'Automated Financial Analysis & Reporting',
            'description': 'Develop an automated financial analysis and reporting system with multiple data sources, AI classification, anomaly detection, dynamic dashboards, and compliance reporting',
            'expected_features': ['Multiple data sources', 'AI classification', 'Anomaly detection', 'Dynamic dashboards', 'Compliance reporting'],
            'complexity': 'complex'
        }
    ]
    
    generator = EnhancedWorkflowGenerator()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 TEST {i}/5: {test_case['name']}")
        print("=" * 60)
        print(f"Description Length: {len(test_case['description'])} characters")
        print(f"Expected Features: {', '.join(test_case['expected_features'])}")
        print(f"Complexity: {test_case['complexity']}")
        print("-" * 60)
        
        try:
            # Generate workflow using enhanced generator
            workflow = generator.generate_enhanced_workflow(
                test_case['description'], 
                'webhook', 
                test_case['complexity']
            )
            
            # Analyze the generated workflow
            nodes = workflow.get('nodes', [])
            connections = workflow.get('connections', {})
            
            print("✅ GENERATION SUCCESSFUL")
            print(f"   📋 Workflow Name: {workflow.get('name', 'Unknown')}")
            print(f"   🔢 Node Count: {len(nodes)} nodes")
            print(f"   🔗 Connections: {len(connections)} node connections")
            print(f"   🎯 Generation Type: enhanced_model")
            print(f"   📊 Complexity Level: {test_case['complexity']}")
            
            # Analyze node types
            node_types = {}
            ai_nodes = []
            integration_nodes = []
            processing_nodes = []
            
            for node in nodes:
                node_type = node.get('type', 'unknown')
                node_name = node.get('name', 'Unknown')
                
                if node_type in node_types:
                    node_types[node_type] += 1
                else:
                    node_types[node_type] = 1
                
                # Categorize nodes
                if any(ai_term in node_type.lower() for ai_term in ['openai', 'langchain', 'ai', 'gpt', 'classifier']):
                    ai_nodes.append(f"{node_type} (1x)")
                elif any(int_term in node_type.lower() for int_term in ['slack', 'email', 'webhook', 'sheets', 'twitter', 'linkedin', 'rss']):
                    integration_nodes.append(f"{node_type} (1x)")
                else:
                    processing_nodes.append(f"{node_type} (1x)")
            
            print(f"   🧩 NODE ANALYSIS ({len(node_types)} unique types):")
            
            if ai_nodes:
                print(f"      🤖 AI Nodes ({len(ai_nodes)}):")
                for node in ai_nodes[:3]:  # Show first 3
                    print(f"         • {node}")
            
            if integration_nodes:
                print(f"      🔗 Integration Nodes ({len(integration_nodes)}):")
                for node in integration_nodes[:3]:  # Show first 3
                    print(f"         • {node}")
            
            if processing_nodes:
                print(f"      ⚙️ Processing Nodes ({len(processing_nodes)}):")
                for node in processing_nodes[:3]:  # Show first 3
                    print(f"         • {node}")
            
            # Feature validation
            print("   ✅ FEATURE VALIDATION:")
            detected_features = generator.feature_detector.detect_features(test_case['description'])
            feature_coverage = 0
            
            for expected_feature in test_case['expected_features']:
                found = False
                
                # Check if feature is represented in the workflow
                if 'AI' in expected_feature and ai_nodes:
                    found = True
                elif 'Slack' in expected_feature and any('slack' in node.lower() for node in [n.get('type', '') for n in nodes]):
                    found = True
                elif 'Google Sheets' in expected_feature and any('sheets' in node.lower() for node in [n.get('type', '') for n in nodes]):
                    found = True
                elif 'Conditional' in expected_feature and any('if' in node.lower() for node in [n.get('type', '') for n in nodes]):
                    found = True
                elif 'Email' in expected_feature and any('email' in node.lower() for node in [n.get('type', '') for n in nodes]):
                    found = True
                elif 'OCR' in expected_feature and any('ocr' in node.lower() for node in [n.get('type', '') for n in nodes]):
                    found = True
                elif 'Schedule' in expected_feature and any('schedule' in node.lower() for node in [n.get('type', '') for n in nodes]):
                    found = True
                elif 'RSS' in expected_feature and any('rss' in node.lower() for node in [n.get('type', '') for n in nodes]):
                    found = True
                elif 'Twitter' in expected_feature and any('twitter' in node.lower() for node in [n.get('type', '') for n in nodes]):
                    found = True
                elif 'LinkedIn' in expected_feature and any('linkedin' in node.lower() for node in [n.get('type', '') for n in nodes]):
                    found = True
                elif 'Analytics' in expected_feature and any('analytics' in node.lower() for node in [n.get('type', '') for n in nodes]):
                    found = True
                
                if found:
                    print(f"      ✅ {expected_feature}: Found")
                    feature_coverage += 1
                else:
                    print(f"      ❌ {expected_feature}: Not detected")
            
            coverage_percent = feature_coverage / len(test_case['expected_features'])
            print(f"   📊 Feature Coverage: {coverage_percent:.0%} ({feature_coverage}/{len(test_case['expected_features'])})")
            
            # Quality score calculation
            quality_score = 0.0
            
            # Node count (30%)
            if len(nodes) >= 7:
                quality_score += 3.0
            elif len(nodes) >= 5:
                quality_score += 2.0
            elif len(nodes) >= 3:
                quality_score += 1.0
            
            # Node diversity (25%)
            if len(node_types) >= 6:
                quality_score += 2.5
            elif len(node_types) >= 4:
                quality_score += 2.0
            elif len(node_types) >= 2:
                quality_score += 1.0
            
            # Feature coverage (35%)
            quality_score += coverage_percent * 3.5
            
            # AI integration (10%)
            if ai_nodes:
                quality_score += 1.0
            
            print(f"   🏆 Overall Quality Score: {quality_score:.1f}/10")
            
            # Sample node inspection
            if nodes:
                sample_node = nodes[0]
                print(f"   🔍 SAMPLE NODE INSPECTION:")
                print(f"      Name: {sample_node.get('name', 'Unknown')}")
                print(f"      Type: {sample_node.get('type', 'Unknown')}")
                print(f"      Parameters: {len(sample_node.get('parameters', {}))} configured")
                if sample_node.get('parameters'):
                    param_keys = list(sample_node['parameters'].keys())[:2]
                    print(f"      Sample Params: {', '.join(param_keys)}")
            
            # JSON size
            json_size = len(json.dumps(workflow))
            print(f"   📄 JSON SIZE: {json_size} characters")
            
        except Exception as e:
            print(f"❌ GENERATION FAILED: {e}")
            continue
    
    print("\n" + "=" * 80)
    print("🎉 ENHANCED COMPLEX PROMPT TESTING COMPLETED!")
    print("=" * 80)

def main():
    """Run the enhanced complex prompt tests"""
    test_complex_prompts_enhanced()

if __name__ == "__main__":
    main()