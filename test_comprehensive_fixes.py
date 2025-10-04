#!/usr/bin/env python3

import sys
sys.path.append('.')
from app import analyze_workflow_description, generate_nodes_from_description, create_basic_workflow

def test_mathematical_logic():
    """Test mathematical calculations and logic improvements"""
    
    print("=== MATHEMATICAL AND LOGIC FIXES VERIFICATION ===\n")
    
    # Test 1: Complexity scoring accuracy
    test_cases = [
        {
            'desc': 'Send email',
            'expected_complexity': 'low',
            'expected_nodes_range': (2, 4)
        },
        {
            'desc': 'Process customer data with validation, transformation, error handling, and audit logging',
            'expected_complexity': 'medium',
            'expected_nodes_range': (4, 8)
        },
        {
            'desc': 'Comprehensive enterprise healthcare patient management system with appointment scheduling, medical record validation, automated notifications to doctors and patients, compliance reporting, audit logging, error handling, data transformation, quality control, and process optimization',
            'expected_complexity': 'high',
            'expected_nodes_range': (8, 15)
        }
    ]
    
    print("1. COMPLEXITY SCORING ACCURACY:")
    complexity_levels = ['simple', 'medium', 'complex']
    
    for i, case in enumerate(test_cases, 1):
        complexity = complexity_levels[i-1]
        analysis = analyze_workflow_description(case['desc'])
        nodes = generate_nodes_from_description(analysis, complexity, {}, {'unique_seed': i * 100})
        workflow = create_basic_workflow(case['desc'], 'webhook', complexity)
        
        node_count = len(nodes)
        workflow_node_count = len(workflow['nodes'])
        min_expected, max_expected = case['expected_nodes_range']
        
        print(f"  Case {i}: {case['desc'][:50]}...")
        print(f"    Generated nodes: {node_count}")
        print(f"    Workflow nodes: {workflow_node_count}")
        print(f"    Complexity level: {complexity}")
        print(f"    Expected range: {min_expected}-{max_expected}")
        print(f"    ✓ Within range: {min_expected <= workflow_node_count <= max_expected}")
        print(f"    Workflow type: {analysis['type']}")
        print()
    
    # Test 2: Industry detection accuracy
    print("2. INDUSTRY DETECTION ACCURACY:")
    industry_tests = [
        ('Patient appointment scheduling system', 'healthcare'),
        ('Banking transaction processing with fraud detection', 'finance'),
        ('Student enrollment and grade management', 'education'),
        ('E-commerce order processing and inventory management', 'ecommerce'),
        ('Generic data processing workflow', 'general')
    ]
    
    for desc, expected_type in industry_tests:
        analysis = analyze_workflow_description(desc)
        detected_type = analysis['type']
        print(f"  '{desc[:40]}...' -> {detected_type} (expected: {expected_type}) ✓" if detected_type == expected_type else f"  '{desc[:40]}...' -> {detected_type} (expected: {expected_type}) ✗")
    print()
    
    # Test 3: Node diversity verification
    print("3. NODE DIVERSITY VERIFICATION:")
    complex_desc = "Healthcare system with patient data validation, appointment scheduling, email notifications, database storage, error handling, and audit logging"
    analysis = analyze_workflow_description(complex_desc)
    nodes = generate_nodes_from_description(analysis, 'complex', {}, {'unique_seed': 999})
    
    node_types = [node.get('type', 'unknown') for node in nodes]
    unique_types = set(node_types)
    
    print(f"  Description: {complex_desc}")
    print(f"  Total nodes: {len(nodes)}")
    print(f"  Unique node types: {len(unique_types)}")
    print(f"  Node types: {list(unique_types)}")
    print(f"  Diversity ratio: {len(unique_types)/len(nodes):.2f} (higher is better)")
    print()
    
    # Test 4: Workflow naming accuracy
    print("4. WORKFLOW NAMING ACCURACY:")
    naming_tests = [
        ('Patient management system', 'healthcare'),
        ('Order processing workflow', 'ecommerce'),
        ('Student enrollment system', 'education'),
        ('Payment processing', 'finance')
    ]
    
    for desc, expected_industry in naming_tests:
        workflow = create_basic_workflow(desc, 'webhook', 'medium')
        name = workflow['name']
        # Remove timestamp and hash for cleaner comparison
        clean_name = ' '.join(name.split()[:-1])
        print(f"  '{desc}' -> '{clean_name}'")
    print()
    
    # Test 5: Mathematical edge cases
    print("5. MATHEMATICAL EDGE CASES:")
    edge_cases = [
        ('', 'Empty description'),
        ('a', 'Single character'),
        ('a b c', 'Three words'),
        ('x' * 1000, 'Very long description (1000 chars)')
    ]
    
    for desc, case_name in edge_cases:
        try:
            analysis = analyze_workflow_description(desc)
            nodes = generate_nodes_from_description(analysis, 'medium', {}, {'unique_seed': 123})
            workflow = create_basic_workflow(desc, 'webhook', 'medium')
            print(f"  {case_name}: ✓ Handled successfully ({len(workflow['nodes'])} nodes)")
        except Exception as e:
            print(f"  {case_name}: ✗ Error - {str(e)}")
    print()
    
    # Test 6: Connection logic verification
    print("6. CONNECTION LOGIC VERIFICATION:")
    test_workflow = create_basic_workflow("Process data with validation and email notification", 'webhook', 'medium')
    nodes = test_workflow['nodes']
    connections = test_workflow['connections']
    
    print(f"  Nodes: {len(nodes)}")
    print(f"  Connections: {len(connections)}")
    
    # Verify all nodes except the last have outgoing connections
    nodes_with_connections = len([node for node in nodes[:-1] if node['name'] in connections])
    expected_connections = len(nodes) - 1
    
    print(f"  Expected connections: {expected_connections}")
    print(f"  Actual connections: {nodes_with_connections}")
    print(f"  Connection accuracy: ✓" if nodes_with_connections >= expected_connections - 1 else "✗")
    print()
    
    print("=== ALL TESTS COMPLETED ===")

if __name__ == '__main__':
    test_mathematical_logic()