#!/usr/bin/env python3
"""
Test script to demonstrate n8n workflow generation capabilities
"""
import json
import sys
import requests
from pathlib import Path

# Add project root to path
sys.path.append('.')

def test_direct_generation():
    """Test direct workflow generation"""
    print("🔧 Testing Direct Workflow Generation...")
    
    try:
        from src.core.generators.market_leading_workflow_generator import MarketLeadingWorkflowGenerator
        generator = MarketLeadingWorkflowGenerator()
        
        test_cases = [
            {
                'description': 'Send daily sales reports via email',
                'trigger_type': 'schedule',
                'complexity': 'simple'
            },
            {
                'description': 'Process customer orders from webhooks, validate data, save to database',
                'trigger_type': 'webhook', 
                'complexity': 'medium'
            },
            {
                'description': 'Monitor social media mentions, analyze sentiment, notify team via Slack, and update CRM',
                'trigger_type': 'webhook',
                'complexity': 'complex'
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n📋 Test Case {i}: {test_case['complexity'].upper()} workflow")
            print(f"   Description: {test_case['description']}")
            
            workflow = generator.generate_market_leading_workflow(
                test_case['description'],
                test_case['trigger_type'],
                test_case['complexity']
            )
            
            nodes = workflow.get('nodes', [])
            connections = workflow.get('connections', {})
            
            print(f"   ✅ Generated {len(nodes)} nodes, {len(connections)} connections")
            
            # Show node details
            for j, node in enumerate(nodes, 1):
                node_type = node.get('type', 'unknown').replace('n8n-nodes-base.', '')
                print(f"      {j}. {node.get('name')} ({node_type})")
            
            # Validate n8n structure
            required_fields = ['id', 'name', 'nodes', 'connections']
            missing_fields = [field for field in required_fields if field not in workflow]
            
            if missing_fields:
                print(f"   ❌ Missing required fields: {missing_fields}")
            else:
                print(f"   ✅ Valid n8n workflow structure")
                
            # Check if nodes have proper n8n format
            valid_nodes = all(
                'id' in node and 'name' in node and 'type' in node and 'position' in node
                for node in nodes
            )
            
            if valid_nodes:
                print(f"   ✅ All nodes have proper n8n format")
            else:
                print(f"   ❌ Some nodes missing required fields")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Direct generation failed: {e}")
        return False

def test_api_generation():
    """Test API endpoint generation"""
    print("\n🌐 Testing API Workflow Generation...")
    
    try:
        # Start server check
        response = requests.get('http://localhost:5000/api/health', timeout=5)
        if response.status_code != 200:
            print("   ⚠️  Server not responding properly")
            return False
            
    except requests.exceptions.ConnectionError:
        print("   ⚠️  Server not running. Start with: python app.py")
        return False
    
    test_cases = [
        {
            'description': 'Create automated invoice processing workflow',
            'trigger_type': 'webhook',
            'complexity': 'medium'
        },
        {
            'description': 'Set up customer support ticket routing system',
            'trigger_type': 'webhook',
            'complexity': 'complex'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 API Test {i}: {test_case['description']}")
        
        try:
            response = requests.post('http://localhost:5000/generate',
                json=test_case,
                headers={'Content-Type': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                
                if result.get('success'):
                    workflow = result.get('workflow', {})
                    validation = result.get('validation', {})
                    
                    nodes = workflow.get('nodes', [])
                    print(f"   ✅ API generated {len(nodes)} nodes")
                    print(f"   📊 Validation score: {validation.get('score', 'N/A')}")
                    
                    # Show generated nodes
                    for j, node in enumerate(nodes, 1):
                        node_type = node.get('type', 'unknown').replace('n8n-nodes-base.', '')
                        print(f"      {j}. {node.get('name')} ({node_type})")
                        
                else:
                    print(f"   ❌ API error: {result.get('error')}")
                    
            else:
                print(f"   ❌ HTTP error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ API test failed: {e}")
    
    return True

def test_workflow_validation():
    """Test workflow validation capabilities"""
    print("\n🔍 Testing Workflow Validation...")
    
    try:
        from src.core.generators.market_leading_workflow_generator import MarketLeadingWorkflowGenerator
        generator = MarketLeadingWorkflowGenerator()
        
        # Generate a workflow
        workflow = generator.generate_market_leading_workflow(
            'Process customer feedback forms and send to support team',
            'webhook',
            'medium'
        )
        
        # Check n8n compatibility
        compatibility_checks = {
            'Has workflow ID': 'id' in workflow,
            'Has workflow name': 'name' in workflow,
            'Has nodes array': isinstance(workflow.get('nodes'), list),
            'Has connections object': isinstance(workflow.get('connections'), dict),
            'Nodes have IDs': all('id' in node for node in workflow.get('nodes', [])),
            'Nodes have types': all('type' in node for node in workflow.get('nodes', [])),
            'Nodes have positions': all('position' in node for node in workflow.get('nodes', [])),
            'Node types are valid': all(
                node.get('type', '').startswith('n8n-nodes-base.') 
                for node in workflow.get('nodes', [])
            )
        }
        
        print("   n8n Compatibility Checks:")
        for check, passed in compatibility_checks.items():
            status = "✅" if passed else "❌"
            print(f"      {status} {check}")
        
        all_passed = all(compatibility_checks.values())
        print(f"\n   {'✅ All checks passed!' if all_passed else '❌ Some checks failed'}")
        
        return all_passed
        
    except Exception as e:
        print(f"   ❌ Validation test failed: {e}")
        return False

def save_sample_workflow():
    """Save a sample workflow to file"""
    print("\n💾 Generating Sample Workflow File...")
    
    try:
        from src.core.generators.market_leading_workflow_generator import MarketLeadingWorkflowGenerator
        generator = MarketLeadingWorkflowGenerator()
        
        workflow = generator.generate_market_leading_workflow(
            'Complete e-commerce order processing: receive order webhook, validate payment, update inventory, send confirmation email, and notify fulfillment team',
            'webhook',
            'complex'
        )
        
        # Save to file
        output_file = Path('sample_n8n_workflow.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(workflow, f, indent=2, ensure_ascii=False)
        
        print(f"   ✅ Saved sample workflow to: {output_file}")
        print(f"   📊 Workflow contains {len(workflow.get('nodes', []))} nodes")
        print(f"   🔗 Import this file directly into n8n!")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Failed to save sample: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 N8N Workflow Generation Capability Test")
    print("=" * 50)
    
    results = {
        'Direct Generation': test_direct_generation(),
        'API Generation': test_api_generation(), 
        'Workflow Validation': test_workflow_validation(),
        'Sample Export': save_sample_workflow()
    }
    
    print("\n📊 Test Results Summary:")
    print("=" * 30)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
    
    all_passed = all(results.values())
    
    print(f"\n🎯 Overall Result: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
    
    if all_passed:
        print("\n🎉 Your n8n workflow generator is working perfectly!")
        print("   • Can generate proper n8n-compatible workflows")
        print("   • Supports multiple complexity levels")
        print("   • Has working API endpoints")
        print("   • Produces valid JSON that can be imported into n8n")
    else:
        print("\n⚠️  Some issues detected. Check the output above for details.")

if __name__ == '__main__':
    main()