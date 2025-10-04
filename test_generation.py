#!/usr/bin/env python3
"""
Test script to verify that the JSON generator creates unique workflows
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_basic_workflow
import json

def test_unique_generation():
    """Test that different prompts generate different workflows"""
    
    # Test cases with different descriptions
    test_cases = [
        {
            'description': 'Create a lead processing workflow that receives leads via webhook and sends them to Slack',
            'triggerType': 'webhook',
            'complexity': 'medium'
        },
        {
            'description': 'Build a data synchronization system that pulls customer data from CRM and updates spreadsheet',
            'triggerType': 'schedule', 
            'complexity': 'complex'
        },
        {
            'description': 'Design an email notification system that monitors database changes and alerts users',
            'triggerType': 'schedule',
            'complexity': 'medium'
        },
        {
            'description': 'Create an order processing automation that validates orders and stores them in database',
            'triggerType': 'webhook',
            'complexity': 'complex'
        },
        {
            'description': 'Build a simple webhook to database workflow for storing form submissions',
            'triggerType': 'webhook',
            'complexity': 'simple'
        }
    ]
    
    generated_workflows = []
    
    print("Testing workflow generation uniqueness...")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Description: {test_case['description']}")
        
        # Generate workflow
        workflow = create_basic_workflow(
            test_case['description'],
            test_case['triggerType'], 
            test_case['complexity']
        )
        
        generated_workflows.append(workflow)
        
        # Print key characteristics
        print(f"Generated Name: {workflow['name']}")
        print(f"Number of Nodes: {len(workflow['nodes'])}")
        print(f"Node Types: {[node['type'] for node in workflow['nodes']]}")
        print(f"Tags: {workflow['tags']}")
        print(f"Workflow Type: {workflow['meta']['workflow_type']}")
        
    # Check for uniqueness
    print("\n" + "=" * 50)
    print("UNIQUENESS ANALYSIS:")
    print("=" * 50)
    
    # Compare workflow names
    names = [w['name'] for w in generated_workflows]
    unique_names = len(set(names))
    print(f"Unique workflow names: {unique_names}/{len(names)}")
    
    # Compare node configurations
    node_configs = []
    for w in generated_workflows:
        config = tuple(sorted([node['type'] + ':' + node['name'] for node in w['nodes']]))
        node_configs.append(config)
    
    unique_configs = len(set(node_configs))
    print(f"Unique node configurations: {unique_configs}/{len(node_configs)}")
    
    # Compare workflow structures
    structures = []
    for w in generated_workflows:
        structure = {
            'node_count': len(w['nodes']),
            'node_types': sorted([node['type'] for node in w['nodes']]),
            'workflow_type': w['meta']['workflow_type']
        }
        structures.append(str(structure))
    
    unique_structures = len(set(structures))
    print(f"Unique workflow structures: {unique_structures}/{len(structures)}")
    
    # Overall assessment
    if unique_names == len(names) and unique_configs >= len(names) * 0.8:
        print("\n✅ SUCCESS: Workflows are sufficiently unique!")
        return True
    else:
        print("\n❌ ISSUE: Workflows are too similar!")
        return False

if __name__ == "__main__":
    success = test_unique_generation()
    sys.exit(0 if success else 1)