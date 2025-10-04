#!/usr/bin/env python3
"""
Test Connections and Parameters Fix
Validates that nodes are properly connected and have correct parameters
"""

import json
from enhanced_workflow_generator import EnhancedWorkflowGenerator

def test_connections_and_parameters():
    """Test that connections and parameters are working correctly"""
    
    print("🔧 TESTING CONNECTIONS AND PARAMETERS FIX")
    print("=" * 60)
    
    generator = EnhancedWorkflowGenerator()
    
    # Test the RSS social media workflow
    description = "Create a scheduled workflow that reads RSS feeds, generates social media posts using AI, and posts them to Twitter and LinkedIn"
    
    print(f"📝 Testing: {description}")
    print("-" * 60)
    
    try:
        workflow = generator.generate_enhanced_workflow(description, 'schedule', 'medium')
        
        nodes = workflow.get('nodes', [])
        connections = workflow.get('connections', {})
        
        print(f"✅ Generated {len(nodes)} nodes")
        print(f"✅ Generated {len(connections)} connections")
        
        # Test 1: Check connections exist
        print(f"\n🔗 CONNECTION ANALYSIS:")
        if len(connections) > 0:
            print(f"   ✅ Connections present: {len(connections)} connection sets")
            for source_node, connection_data in connections.items():
                targets = connection_data.get('main', [[]])[0]
                if targets:
                    target_node = targets[0].get('node', 'Unknown')
                    print(f"   🔗 {source_node} → {target_node}")
                else:
                    print(f"   ⚠️ {source_node} → No target")
        else:
            print(f"   ❌ No connections found!")
        
        # Test 2: Check node parameters
        print(f"\n⚙️ PARAMETER ANALYSIS:")
        for i, node in enumerate(nodes):
            node_name = node.get('name', 'Unknown')
            node_type = node.get('type', 'Unknown')
            parameters = node.get('parameters', {})
            
            print(f"   📋 Node {i+1}: {node_name}")
            print(f"      Type: {node_type}")
            print(f"      Parameters: {len(parameters)} configured")
            
            if parameters:
                # Show first few parameter keys
                param_keys = list(parameters.keys())[:3]
                print(f"      Keys: {param_keys}")
                
                # Check for specific parameter quality
                if node_type == 'n8n-nodes-base.scheduleTrigger':
                    if 'rule' in parameters:
                        print(f"      ✅ Schedule rule configured")
                    else:
                        print(f"      ❌ Missing schedule rule")
                
                elif 'rssFeedRead' in node_type:
                    if 'url' in parameters:
                        print(f"      ✅ RSS URL configured")
                    else:
                        print(f"      ❌ Missing RSS URL")
                
                elif 'twitter' in node_type.lower():
                    if 'operation' in parameters or 'text' in parameters:
                        print(f"      ✅ Twitter operation configured")
                    else:
                        print(f"      ❌ Missing Twitter configuration")
                
                elif 'linkedin' in node_type.lower():
                    if 'operation' in parameters or 'text' in parameters:
                        print(f"      ✅ LinkedIn operation configured")
                    else:
                        print(f"      ❌ Missing LinkedIn configuration")
            else:
                print(f"      ❌ No parameters configured")
        
        # Test 3: Validate workflow structure
        print(f"\n🏗️ WORKFLOW STRUCTURE VALIDATION:")
        
        # Check if all nodes except the last have outgoing connections
        nodes_with_connections = set(connections.keys())
        node_names = [node.get('name') for node in nodes]
        
        missing_connections = []
        for i, node_name in enumerate(node_names[:-1]):  # Exclude last node
            if node_name not in nodes_with_connections:
                missing_connections.append(node_name)
        
        if not missing_connections:
            print(f"   ✅ All nodes properly connected")
        else:
            print(f"   ❌ Missing connections from: {missing_connections}")
        
        # Test 4: Check for realistic parameter values
        print(f"\n🎯 PARAMETER QUALITY CHECK:")
        quality_issues = []
        
        for node in nodes:
            node_type = node.get('type', '')
            parameters = node.get('parameters', {})
            
            # Check for empty or placeholder values
            if 'scheduleTrigger' in node_type:
                rule = parameters.get('rule', {})
                if not rule or not rule.get('interval'):
                    quality_issues.append(f"{node.get('name')}: Missing schedule interval")
            
            elif 'rssFeedRead' in node_type:
                url = parameters.get('url', '')
                if not url or 'example.com' in url:
                    quality_issues.append(f"{node.get('name')}: Placeholder RSS URL")
            
            elif any(social in node_type.lower() for social in ['twitter', 'linkedin']):
                if not parameters.get('operation') and not parameters.get('text'):
                    quality_issues.append(f"{node.get('name')}: Missing social media configuration")
        
        if not quality_issues:
            print(f"   ✅ All parameters have realistic values")
        else:
            print(f"   ⚠️ Parameter quality issues:")
            for issue in quality_issues:
                print(f"      • {issue}")
        
        # Overall assessment
        print(f"\n📊 OVERALL ASSESSMENT:")
        
        connection_score = len(connections) / max(len(nodes) - 1, 1) if nodes else 0
        parameter_score = sum(1 for node in nodes if node.get('parameters')) / len(nodes) if nodes else 0
        
        print(f"   Connection Coverage: {connection_score:.1%}")
        print(f"   Parameter Coverage: {parameter_score:.1%}")
        
        if connection_score >= 0.8 and parameter_score >= 0.8:
            print(f"   🎉 EXCELLENT - Connections and parameters working well!")
            return True
        elif connection_score >= 0.5 and parameter_score >= 0.5:
            print(f"   ✅ GOOD - Most connections and parameters working")
            return True
        else:
            print(f"   ❌ POOR - Significant issues with connections/parameters")
            return False
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def test_json_output():
    """Test the actual JSON output structure"""
    print(f"\n\n📄 JSON OUTPUT STRUCTURE TEST")
    print("=" * 60)
    
    generator = EnhancedWorkflowGenerator()
    description = "Create a scheduled workflow that reads RSS feeds and posts to Twitter"
    
    try:
        workflow = generator.generate_enhanced_workflow(description, 'schedule', 'medium')
        
        # Convert to JSON and back to test serialization
        json_str = json.dumps(workflow, indent=2)
        parsed_workflow = json.loads(json_str)
        
        print(f"✅ JSON serialization successful")
        print(f"📊 JSON size: {len(json_str)} characters")
        
        # Show sample of the JSON structure
        print(f"\n📋 SAMPLE JSON STRUCTURE:")
        sample_json = {
            "name": workflow.get('name'),
            "nodes": len(workflow.get('nodes', [])),
            "connections": len(workflow.get('connections', {})),
            "sample_node": workflow.get('nodes', [{}])[0] if workflow.get('nodes') else {},
            "sample_connection": list(workflow.get('connections', {}).values())[0] if workflow.get('connections') else {}
        }
        
        print(json.dumps(sample_json, indent=2))
        
        return True
        
    except Exception as e:
        print(f"❌ JSON test failed: {e}")
        return False

def main():
    """Run connection and parameter tests"""
    print("🔧 CONNECTIONS AND PARAMETERS FIX VALIDATION")
    print("=" * 80)
    
    test1_result = test_connections_and_parameters()
    test2_result = test_json_output()
    
    print(f"\n" + "=" * 80)
    if test1_result and test2_result:
        print("🎉 ALL TESTS PASSED - Connections and parameters are working!")
    else:
        print("⚠️ SOME ISSUES REMAIN - Further fixes needed")
    
    return test1_result and test2_result

if __name__ == "__main__":
    main()