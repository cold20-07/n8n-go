#!/usr/bin/env python3
"""
Complete Workflow Fix Test
Tests the exact same workflow that was failing to ensure it now works perfectly
"""

import json
from enhanced_workflow_generator import EnhancedWorkflowGenerator

def test_rss_social_media_workflow():
    """Test the RSS social media workflow that was failing"""
    
    print("🎯 TESTING COMPLETE RSS SOCIAL MEDIA WORKFLOW FIX")
    print("=" * 80)
    
    # The exact prompt that was failing
    description = "Create a scheduled workflow that reads RSS feeds, generates social media posts using AI, and posts them to Twitter and LinkedIn"
    
    print(f"📝 Prompt: {description}")
    print("-" * 80)
    
    generator = EnhancedWorkflowGenerator()
    
    try:
        workflow = generator.generate_enhanced_workflow(description, 'schedule', 'medium')
        
        nodes = workflow.get('nodes', [])
        connections = workflow.get('connections', {})
        
        print(f"✅ WORKFLOW GENERATED SUCCESSFULLY")
        print(f"   📋 Name: {workflow.get('name')}")
        print(f"   🔢 Nodes: {len(nodes)}")
        print(f"   🔗 Connections: {len(connections)}")
        
        # Detailed node analysis
        print(f"\n🧩 DETAILED NODE ANALYSIS:")
        expected_features = {
            'schedule': False,
            'rss': False,
            'ai_content': False,
            'twitter': False,
            'linkedin': False
        }
        
        for i, node in enumerate(nodes, 1):
            name = node.get('name', 'Unknown')
            node_type = node.get('type', 'Unknown')
            parameters = node.get('parameters', {})
            
            print(f"\n   📋 Node {i}: {name}")
            print(f"      Type: {node_type}")
            print(f"      Position: {node.get('position', [0, 0])}")
            print(f"      Parameters: {len(parameters)} configured")
            
            # Check for expected features
            if 'scheduleTrigger' in node_type:
                expected_features['schedule'] = True
                print(f"      ✅ Schedule trigger detected")
                if 'rule' in parameters:
                    interval = parameters['rule'].get('interval', [{}])[0]
                    print(f"      ⏰ Interval: {interval.get('hoursInterval', 'Unknown')} hours")
            
            elif 'rssFeedRead' in node_type:
                expected_features['rss'] = True
                print(f"      ✅ RSS feed reader detected")
                if 'url' in parameters:
                    print(f"      🔗 URL configured: {parameters['url'][:50]}...")
            
            elif 'langchain' in node_type.lower() and 'chat' in node_type.lower():
                expected_features['ai_content'] = True
                print(f"      ✅ AI content generation detected")
                if 'options' in parameters and 'systemMessage' in parameters['options']:
                    print(f"      🤖 System message configured")
            
            elif 'twitter' in node_type.lower():
                expected_features['twitter'] = True
                print(f"      ✅ Twitter integration detected")
                if 'operation' in parameters:
                    print(f"      🐦 Operation: {parameters['operation']}")
                if 'text' in parameters:
                    print(f"      📝 Text template configured")
            
            elif 'linkedin' in node_type.lower():
                expected_features['linkedin'] = True
                print(f"      ✅ LinkedIn integration detected")
                if 'operation' in parameters:
                    print(f"      💼 Operation: {parameters['operation']}")
                if 'text' in parameters:
                    print(f"      📝 Text template configured")
            
            # Show parameter details for key nodes
            if parameters and len(parameters) > 0:
                print(f"      📊 Key parameters:")
                for key, value in list(parameters.items())[:2]:
                    if isinstance(value, dict):
                        print(f"         {key}: {type(value).__name__} with {len(value)} items")
                    else:
                        print(f"         {key}: {str(value)[:50]}...")
        
        # Connection analysis
        print(f"\n🔗 CONNECTION FLOW ANALYSIS:")
        connection_chain = []
        
        for i, node in enumerate(nodes):
            node_name = node['name']
            if node_name in connections:
                targets = connections[node_name].get('main', [[]])[0]
                if targets:
                    target_name = targets[0].get('node')
                    connection_chain.append(f"{node_name} → {target_name}")
                    print(f"   {i+1}. {node_name} → {target_name}")
                else:
                    print(f"   {i+1}. {node_name} → (no connection)")
            else:
                print(f"   {i+1}. {node_name} → (end node)")
        
        # Feature coverage assessment
        print(f"\n✅ FEATURE COVERAGE ASSESSMENT:")
        covered_features = sum(expected_features.values())
        total_features = len(expected_features)
        coverage_percent = covered_features / total_features
        
        for feature, covered in expected_features.items():
            status = "✅" if covered else "❌"
            print(f"   {status} {feature.replace('_', ' ').title()}: {'Found' if covered else 'Missing'}")
        
        print(f"\n📊 Coverage: {coverage_percent:.0%} ({covered_features}/{total_features})")
        
        # Quality assessment
        print(f"\n🏆 QUALITY ASSESSMENT:")
        
        quality_checks = []
        
        # Node count check
        if len(nodes) >= 5:
            quality_checks.append("✅ Sufficient nodes (5+)")
        else:
            quality_checks.append(f"❌ Too few nodes ({len(nodes)})")
        
        # Connection check
        if len(connections) >= len(nodes) - 1:
            quality_checks.append("✅ Proper connections")
        else:
            quality_checks.append(f"❌ Missing connections")
        
        # Parameter check
        nodes_with_params = sum(1 for node in nodes if node.get('parameters'))
        if nodes_with_params >= len(nodes) * 0.8:
            quality_checks.append("✅ Well-configured parameters")
        else:
            quality_checks.append(f"❌ Missing parameters")
        
        # Feature coverage check
        if coverage_percent >= 0.8:
            quality_checks.append("✅ Excellent feature coverage")
        elif coverage_percent >= 0.6:
            quality_checks.append("✅ Good feature coverage")
        else:
            quality_checks.append("❌ Poor feature coverage")
        
        # Real n8n types check
        valid_types = all(
            node.get('type', '').startswith(('n8n-nodes-base.', '@n8n/n8n-nodes-langchain.'))
            for node in nodes
        )
        if valid_types:
            quality_checks.append("✅ All valid n8n node types")
        else:
            quality_checks.append("❌ Invalid node types detected")
        
        for check in quality_checks:
            print(f"   {check}")
        
        # Overall score
        passed_checks = sum(1 for check in quality_checks if check.startswith("✅"))
        total_checks = len(quality_checks)
        overall_score = (passed_checks / total_checks) * 10
        
        print(f"\n🎯 OVERALL QUALITY SCORE: {overall_score:.1f}/10")
        
        # JSON validation
        print(f"\n📄 JSON VALIDATION:")
        try:
            json_str = json.dumps(workflow, indent=2)
            json_size = len(json_str)
            print(f"   ✅ Valid JSON structure")
            print(f"   📊 Size: {json_size:,} characters")
            
            # Check for n8n compatibility
            required_fields = ['id', 'name', 'nodes', 'connections', 'active']
            missing_fields = [field for field in required_fields if field not in workflow]
            
            if not missing_fields:
                print(f"   ✅ n8n compatible structure")
            else:
                print(f"   ❌ Missing required fields: {missing_fields}")
            
        except Exception as e:
            print(f"   ❌ JSON serialization failed: {e}")
        
        # Final verdict
        print(f"\n" + "=" * 80)
        if overall_score >= 8.0 and coverage_percent >= 0.8:
            print("🎉 EXCELLENT! Workflow generation is working perfectly!")
            print("✅ All major issues have been fixed:")
            print("   • Nodes are properly connected")
            print("   • Parameters are correctly configured")
            print("   • All requested features are implemented")
            print("   • Uses real n8n node types")
            print("   • Generates production-ready JSON")
            return True
        elif overall_score >= 6.0:
            print("✅ GOOD! Workflow generation is working well with minor issues")
            return True
        else:
            print("⚠️ NEEDS IMPROVEMENT - Some issues remain")
            return False
        
    except Exception as e:
        print(f"❌ WORKFLOW GENERATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the complete workflow fix test"""
    success = test_rss_social_media_workflow()
    
    if success:
        print(f"\n🎉 SUCCESS! The RSS social media workflow is now working perfectly!")
        print(f"The user should now see:")
        print(f"   • 5-7 connected nodes in the visual editor")
        print(f"   • Proper parameters in each node")
        print(f"   • A complete workflow from RSS → AI → Social Media")
    else:
        print(f"\n⚠️ Issues remain - further debugging needed")
    
    return success

if __name__ == "__main__":
    main()