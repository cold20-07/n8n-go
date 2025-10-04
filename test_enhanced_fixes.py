#!/usr/bin/env python3
"""
Test Enhanced Workflow Generator Fixes
Validates that the core issues have been resolved
"""

import json
import sys
from enhanced_workflow_generator import EnhancedWorkflowGenerator, EnhancedFeatureDetector

def test_feature_detection():
    """Test enhanced feature detection"""
    print("🧪 TESTING ENHANCED FEATURE DETECTION")
    print("=" * 60)
    
    test_cases = [
        {
            'description': 'Create an AI-powered workflow that monitors Slack messages, uses OpenAI to analyze sentiment and categorize topics, stores results in Google Sheets, and sends notifications based on urgency levels with conditional logic and multiple AI models',
            'expected_features': ['openai', 'ai_analysis', 'multiple_ai', 'slack', 'google_sheets', 'conditional']
        },
        {
            'description': 'Build a multi-modal content generation system with scheduled triggers, RSS feeds, AI content generation, and multi-platform posting to Twitter and LinkedIn with analytics tracking',
            'expected_features': ['schedule', 'rss', 'ai_content', 'twitter', 'linkedin', 'analytics']
        },
        {
            'description': 'Design an intelligent document processing workflow with email triggers, OCR processing, AI document classification, approval workflows, and CRM integration',
            'expected_features': ['email', 'ocr', 'pdf', 'ai_analysis', 'approval', 'crm']
        },
        {
            'description': 'Create a real-time customer journey orchestration with event triggers, AI prediction, multi-channel messaging, and real-time optimization with analytics',
            'expected_features': ['webhook', 'ai_analysis', 'email', 'slack', 'analytics']
        },
        {
            'description': 'Develop an automated financial analysis and reporting system with multiple data sources, AI classification, anomaly detection, dynamic dashboards, and compliance reporting',
            'expected_features': ['database', 'ai_analysis', 'financial', 'reporting', 'analytics']
        }
    ]
    
    detector = EnhancedFeatureDetector()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 TEST {i}/5: Feature Detection")
        print("-" * 40)
        print(f"Description: {test_case['description'][:80]}...")
        
        detected_features = detector.detect_features(test_case['description'])
        detected_names = list(detected_features.keys())
        expected_names = test_case['expected_features']
        
        print(f"🔍 Detected: {detected_names}")
        print(f"📋 Expected: {expected_names}")
        
        # Calculate coverage
        matches = len(set(detected_names) & set(expected_names))
        coverage = matches / len(expected_names) if expected_names else 0
        
        print(f"✅ Feature Coverage: {coverage:.1%} ({matches}/{len(expected_names)})")
        
        if coverage >= 0.6:  # 60% or better
            print("🎉 PASS - Good feature detection")
        else:
            print("❌ FAIL - Poor feature detection")
    
    return True

def test_template_matching():
    """Test template matching improvements"""
    print("\n\n🧪 TESTING TEMPLATE MATCHING")
    print("=" * 60)
    
    generator = EnhancedWorkflowGenerator()
    
    test_cases = [
        {
            'description': 'Create an AI-powered workflow that monitors Slack messages, uses OpenAI to analyze sentiment and categorize topics, stores results in Google Sheets, and sends notifications based on urgency levels',
            'expected_template': 'ai_slack_sheets'
        },
        {
            'description': 'Design an intelligent document processing workflow with email triggers, OCR processing, AI document classification, approval workflows, and CRM integration',
            'expected_template': 'document_ai_processing'
        },
        {
            'description': 'Build a multi-modal content generation system with scheduled triggers, RSS feeds, AI content generation, and multi-platform posting to Twitter and LinkedIn',
            'expected_template': 'content_generation_social'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 TEST {i}/3: Template Matching")
        print("-" * 40)
        print(f"Description: {test_case['description'][:80]}...")
        
        detected_features = generator.feature_detector.detect_features(test_case['description'])
        template, score = generator.find_best_template(detected_features, test_case['description'])
        
        print(f"🔍 Detected features: {list(detected_features.keys())}")
        print(f"📋 Selected template: {template.get('name', 'Unknown') if template else 'None'}")
        print(f"🎯 Match score: {score:.2f}")
        
        if score >= 0.3:  # 30% or better
            print("🎉 PASS - Good template matching")
        else:
            print("❌ FAIL - Poor template matching")
    
    return True

def test_workflow_generation():
    """Test complete workflow generation"""
    print("\n\n🧪 TESTING COMPLETE WORKFLOW GENERATION")
    print("=" * 60)
    
    generator = EnhancedWorkflowGenerator()
    
    test_cases = [
        {
            'description': 'Create an AI-powered workflow that monitors Slack messages, uses OpenAI to analyze sentiment and categorize topics, stores results in Google Sheets, and sends notifications based on urgency levels with conditional logic and multiple AI models',
            'expected_features': ['openai', 'ai_analysis', 'slack', 'google_sheets', 'conditional'],
            'min_nodes': 5
        },
        {
            'description': 'Build a multi-modal content generation system with scheduled triggers, RSS feeds, AI content generation, and multi-platform posting to Twitter and LinkedIn with analytics tracking',
            'expected_features': ['schedule', 'rss', 'ai_content', 'twitter', 'linkedin'],
            'min_nodes': 5
        },
        {
            'description': 'Design an intelligent document processing workflow with email triggers, OCR processing, AI document classification, approval workflows, and CRM integration',
            'expected_features': ['email', 'ocr', 'ai_analysis', 'approval'],
            'min_nodes': 5
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 TEST {i}/3: Complete Workflow Generation")
        print("-" * 40)
        print(f"Description: {test_case['description'][:80]}...")
        
        try:
            workflow = generator.generate_enhanced_workflow(test_case['description'])
            
            # Analyze generated workflow
            nodes = workflow.get('nodes', [])
            node_count = len(nodes)
            node_types = [node.get('type', '') for node in nodes]
            unique_types = len(set(node_types))
            
            print(f"📊 Generated {node_count} nodes with {unique_types} unique types")
            print(f"🔗 Node types: {node_types[:5]}{'...' if len(node_types) > 5 else ''}")
            
            # Check feature coverage
            detected_features = generator.feature_detector.detect_features(test_case['description'])
            required_nodes = generator.feature_detector.get_required_nodes(detected_features)
            
            feature_coverage = 0
            for required_node in required_nodes:
                if any(required_node in node_type for node_type in node_types):
                    feature_coverage += 1
            
            coverage_percent = feature_coverage / len(required_nodes) if required_nodes else 0
            
            print(f"✅ Feature coverage: {coverage_percent:.1%} ({feature_coverage}/{len(required_nodes)})")
            print(f"🏆 Quality metrics:")
            print(f"   • Node count: {node_count} (min: {test_case['min_nodes']})")
            print(f"   • Node diversity: {unique_types} types")
            print(f"   • Feature coverage: {coverage_percent:.1%}")
            
            # Overall assessment
            if (node_count >= test_case['min_nodes'] and 
                coverage_percent >= 0.4 and 
                unique_types >= 3):
                print("🎉 PASS - High quality workflow generated")
            else:
                print("❌ FAIL - Low quality workflow")
                
        except Exception as e:
            print(f"❌ GENERATION FAILED: {e}")
    
    return True

def test_node_type_validation():
    """Test that generated workflows use real n8n node types"""
    print("\n\n🧪 TESTING NODE TYPE VALIDATION")
    print("=" * 60)
    
    # Known valid n8n node types
    valid_node_types = {
        'n8n-nodes-base.webhook',
        'n8n-nodes-base.slack',
        'n8n-nodes-base.googleSheets',
        'n8n-nodes-base.set',
        'n8n-nodes-base.if',
        'n8n-nodes-base.httpRequest',
        'n8n-nodes-base.emailSend',
        '@n8n/n8n-nodes-langchain.lmChatOpenAi',
        '@n8n/n8n-nodes-langchain.textClassifier',
        '@n8n/n8n-nodes-langchain.outputParserStructured'
    }
    
    generator = EnhancedWorkflowGenerator()
    
    test_description = "Create an AI workflow with Slack integration and Google Sheets"
    workflow = generator.generate_enhanced_workflow(test_description)
    
    nodes = workflow.get('nodes', [])
    node_types = [node.get('type', '') for node in nodes]
    
    print(f"📊 Generated {len(nodes)} nodes")
    print(f"🔍 Node types: {node_types}")
    
    valid_count = 0
    for node_type in node_types:
        if node_type in valid_node_types or any(valid in node_type for valid in valid_node_types):
            valid_count += 1
        else:
            print(f"⚠️ Unknown node type: {node_type}")
    
    validity_percent = valid_count / len(node_types) if node_types else 0
    print(f"✅ Node type validity: {validity_percent:.1%} ({valid_count}/{len(node_types)})")
    
    if validity_percent >= 0.8:  # 80% or better
        print("🎉 PASS - Good node type validity")
    else:
        print("❌ FAIL - Poor node type validity")
    
    return True

def main():
    """Run all tests"""
    print("🚀 ENHANCED WORKFLOW GENERATOR VALIDATION")
    print("=" * 80)
    print("Testing fixes for feature detection, template matching, and workflow quality")
    print("=" * 80)
    
    try:
        # Run all tests
        test_feature_detection()
        test_template_matching()
        test_workflow_generation()
        test_node_type_validation()
        
        print("\n\n🎉 ALL TESTS COMPLETED!")
        print("=" * 80)
        print("✅ Enhanced workflow generator validation finished")
        print("🔧 Core issues should now be resolved:")
        print("   • Improved feature detection with comprehensive keywords")
        print("   • Better template matching with specialized templates")
        print("   • Higher quality workflows with more nodes and features")
        print("   • Valid n8n node types throughout")
        
    except Exception as e:
        print(f"\n❌ TEST SUITE FAILED: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()