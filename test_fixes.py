#!/usr/bin/env python3

import sys
sys.path.append('.')
from app import analyze_workflow_description, generate_nodes_from_description, create_basic_workflow

def test_logic_fixes():
    """Test the fixed logic and math errors"""
    
    # Test 1: Healthcare workflow type detection
    desc1 = 'Create a comprehensive healthcare patient management system with appointment scheduling, medical record validation, and automated notifications to doctors and patients'
    analysis1 = analyze_workflow_description(desc1)
    print("=== Test 1: Healthcare Workflow ===")
    print(f"Analysis type: {analysis1['type']}")
    print(f"Tags: {analysis1.get('tags', [])}")
    print(f"Integrations: {analysis1.get('integrations', [])}")
    print()

    # Test 2: Node generation with complexity
    nodes1 = generate_nodes_from_description(analysis1, 'complex', {}, {'unique_seed': 123})
    print("=== Test 2: Node Generation ===")
    print(f"Generated nodes: {len(nodes1)}")
    for i, node in enumerate(nodes1):
        node_type = node.get('type', 'unknown')
        purpose = node.get('purpose', 'no purpose')
        print(f"  {i+1}. {node_type} - {purpose}")
    print()

    # Test 3: Complete workflow creation
    workflow1 = create_basic_workflow(desc1, 'webhook', 'complex')
    print("=== Test 3: Complete Workflow ===")
    print(f"Workflow name: {workflow1['name']}")
    print(f"Workflow nodes: {len(workflow1['nodes'])}")
    print(f"Workflow connections: {len(workflow1.get('connections', {}))}")
    print(f"Workflow type: {workflow1.get('meta', {}).get('workflow_type', 'unknown')}")
    print()

    # Test 4: Simple workflow (should have fewer nodes)
    desc2 = 'Send email notification'
    analysis2 = analyze_workflow_description(desc2)
    nodes2 = generate_nodes_from_description(analysis2, 'simple', {}, {'unique_seed': 456})
    workflow2 = create_basic_workflow(desc2, 'manual', 'simple')
    
    print("=== Test 4: Simple Workflow ===")
    print(f"Analysis type: {analysis2['type']}")
    print(f"Generated nodes: {len(nodes2)}")
    print(f"Workflow nodes: {len(workflow2['nodes'])}")
    print(f"Workflow name: {workflow2['name']}")
    print()

    # Test 5: Complex business workflow
    desc3 = 'Comprehensive order processing system with inventory management, payment validation, fraud detection, customer notification, shipping coordination, and compliance reporting'
    analysis3 = analyze_workflow_description(desc3)
    nodes3 = generate_nodes_from_description(analysis3, 'complex', {}, {'unique_seed': 789})
    workflow3 = create_basic_workflow(desc3, 'webhook', 'complex')
    
    print("=== Test 5: Complex Business Workflow ===")
    print(f"Analysis type: {analysis3['type']}")
    print(f"Generated nodes: {len(nodes3)}")
    print(f"Workflow nodes: {len(workflow3['nodes'])}")
    print(f"Workflow name: {workflow3['name']}")
    print(f"Tags: {analysis3.get('tags', [])}")
    print()

    # Test 6: Edge case - empty description
    try:
        desc4 = ''
        analysis4 = analyze_workflow_description(desc4)
        print("=== Test 6: Edge Case - Empty Description ===")
        print(f"Analysis type: {analysis4['type']}")
        print("Empty description handled correctly")
    except Exception as e:
        print(f"Error with empty description: {e}")
    print()

    print("=== All Tests Completed ===")

if __name__ == '__main__':
    test_logic_fixes()