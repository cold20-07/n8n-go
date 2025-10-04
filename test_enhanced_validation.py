#!/usr/bin/env python3
"""
Test Enhanced Input Validation
Verify that the enhanced validation improves success rates while maintaining quality
"""

import sys
import json
import time
import random
from collections import defaultdict

sys.path.append('.')

from enhanced_input_validation import validate_workflow_request, validator
from app import create_basic_workflow

def test_enhanced_validation():
    """Test the enhanced validation with problematic inputs"""
    
    print("🧪 Testing Enhanced Input Validation")
    print("="*60)
    
    # Test cases that previously failed
    problematic_inputs = [
        # Empty/minimal inputs
        {'description': ''},
        {'description': '   '},
        {'description': 'a'},
        {'description': 'x'},
        {'description': None},
        {'description': 123},
        
        # Generic/ambiguous inputs
        {'description': 'thing'},
        {'description': 'stuff'},
        {'description': 'process'},
        {'description': 'workflow'},
        {'description': 'do something'},
        {'description': 'handle stuff'},
        
        # Non-English inputs
        {'description': 'flujo de trabajo'},
        {'description': 'système de workflow'},
        {'description': 'システム workflow'},
        {'description': 'процесс workflow'},
        
        # Special characters
        {'description': '!@#$%^&*()'},
        {'description': '<script>alert("test")</script>'},
        {'description': 'DROP TABLE users;'},
        
        # Very long inputs
        {'description': 'workflow ' * 1000},
        {'description': 'a' * 10000},
        
        # Invalid trigger types
        {'description': 'test workflow', 'triggerType': 'invalid'},
        {'description': 'test workflow', 'triggerType': None},
        {'description': 'test workflow', 'triggerType': 123},
        
        # Invalid complexity
        {'description': 'test workflow', 'complexity': 'invalid'},
        {'description': 'test workflow', 'complexity': None},
        
        # Malformed advanced options
        {'description': 'test workflow', 'advanced_options': 'invalid'},
        {'description': 'test workflow', 'advanced_options': None},
    ]
    
    results = {
        'total_tests': len(problematic_inputs),
        'successful_validations': 0,
        'failed_validations': 0,
        'successful_workflows': 0,
        'failed_workflows': 0,
        'improvements': defaultdict(int),
        'errors': []
    }
    
    print(f"Testing {len(problematic_inputs)} problematic inputs...")
    
    for i, test_input in enumerate(problematic_inputs):
        try:
            # Test validation
            cleaned_data, validation_report = validate_workflow_request(test_input)
            results['successful_validations'] += 1
            
            # Count improvements
            transformations = validation_report['description'].get('transformations_applied', [])
            for transformation in transformations:
                results['improvements'][transformation] += 1
            
            # Test workflow creation with cleaned data
            try:
                workflow = create_basic_workflow(
                    cleaned_data['description'],
                    cleaned_data['trigger_type'],
                    cleaned_data['complexity'],
                    '',
                    cleaned_data['advanced_options']
                )
                
                # Validate workflow quality
                if (workflow and 
                    isinstance(workflow, dict) and 
                    workflow.get('nodes') and 
                    len(workflow['nodes']) > 0 and
                    len(workflow.get('name', '')) > 5):
                    results['successful_workflows'] += 1
                    print(f"✅ {i+1:2d}: {str(test_input.get('description', 'None'))[:30]:<30} -> {cleaned_data['description'][:30]}")
                else:
                    results['failed_workflows'] += 1
                    print(f"⚠️  {i+1:2d}: {str(test_input.get('description', 'None'))[:30]:<30} -> Invalid workflow")
                    
            except Exception as e:
                results['failed_workflows'] += 1
                print(f"❌ {i+1:2d}: {str(test_input.get('description', 'None'))[:30]:<30} -> Workflow error: {str(e)[:50]}")
                
        except Exception as e:
            results['failed_validations'] += 1
            results['errors'].append(f"Input {i+1}: {str(e)}")
            print(f"💥 {i+1:2d}: {str(test_input.get('description', 'None'))[:30]:<30} -> Validation error: {str(e)[:50]}")
    
    # Print summary
    print("\n" + "="*60)
    print("📊 ENHANCED VALIDATION TEST RESULTS")
    print("="*60)
    
    validation_success_rate = (results['successful_validations'] / results['total_tests']) * 100
    workflow_success_rate = (results['successful_workflows'] / results['total_tests']) * 100
    
    print(f"Total Tests: {results['total_tests']}")
    print(f"✅ Successful Validations: {results['successful_validations']} ({validation_success_rate:.1f}%)")
    print(f"❌ Failed Validations: {results['failed_validations']}")
    print(f"✅ Successful Workflows: {results['successful_workflows']} ({workflow_success_rate:.1f}%)")
    print(f"❌ Failed Workflows: {results['failed_workflows']}")
    
    print(f"\n🔧 IMPROVEMENTS APPLIED:")
    for improvement, count in sorted(results['improvements'].items(), key=lambda x: x[1], reverse=True):
        print(f"   • {improvement}: {count} times")
    
    if results['errors']:
        print(f"\n❌ VALIDATION ERRORS:")
        for error in results['errors'][:10]:  # Show first 10 errors
            print(f"   • {error}")
        if len(results['errors']) > 10:
            print(f"   • ... and {len(results['errors']) - 10} more errors")
    
    # Quality assessment
    if workflow_success_rate >= 90:
        quality = "🏆 EXCELLENT"
    elif workflow_success_rate >= 80:
        quality = "✅ GOOD"
    elif workflow_success_rate >= 70:
        quality = "⚠️  ACCEPTABLE"
    else:
        quality = "❌ NEEDS IMPROVEMENT"
    
    print(f"\n🎯 QUALITY ASSESSMENT: {quality}")
    print(f"🎯 IMPROVEMENT: Enhanced validation should significantly reduce failures")
    
    return workflow_success_rate >= 80

def test_specific_enhancements():
    """Test specific enhancement features"""
    
    print("\n🔍 Testing Specific Enhancement Features")
    print("="*60)
    
    test_cases = [
        # Test ambiguity resolution
        {
            'input': {'description': 'thing'},
            'expected_improvements': ['ambiguity_resolution'],
            'test_name': 'Ambiguity Resolution'
        },
        
        # Test empty input handling
        {
            'input': {'description': ''},
            'expected_improvements': ['empty_to_default'],
            'test_name': 'Empty Input Handling'
        },
        
        # Test short expansion
        {
            'input': {'description': 'hi'},
            'expected_improvements': ['short_expansion'],
            'test_name': 'Short Input Expansion'
        },
        
        # Test type conversion
        {
            'input': {'description': 123},
            'expected_improvements': ['type_conversion'],
            'test_name': 'Type Conversion'
        },
        
        # Test trigger type normalization
        {
            'input': {'description': 'test workflow', 'triggerType': 'http'},
            'expected_trigger': 'webhook',
            'test_name': 'Trigger Type Normalization'
        },
        
        # Test complexity normalization
        {
            'input': {'description': 'test workflow', 'complexity': 'advanced'},
            'expected_complexity': 'complex',
            'test_name': 'Complexity Normalization'
        }
    ]
    
    passed = 0
    failed = 0
    
    for test_case in test_cases:
        try:
            cleaned_data, validation_report = validate_workflow_request(test_case['input'])
            
            # Check expected improvements
            if 'expected_improvements' in test_case:
                transformations = validation_report['description'].get('transformations_applied', [])
                expected = test_case['expected_improvements']
                
                if any(exp in transformations for exp in expected):
                    print(f"✅ {test_case['test_name']}: Applied {transformations}")
                    passed += 1
                else:
                    print(f"❌ {test_case['test_name']}: Expected {expected}, got {transformations}")
                    failed += 1
            
            # Check expected trigger type
            if 'expected_trigger' in test_case:
                if cleaned_data['trigger_type'] == test_case['expected_trigger']:
                    print(f"✅ {test_case['test_name']}: Trigger normalized to {cleaned_data['trigger_type']}")
                    passed += 1
                else:
                    print(f"❌ {test_case['test_name']}: Expected {test_case['expected_trigger']}, got {cleaned_data['trigger_type']}")
                    failed += 1
            
            # Check expected complexity
            if 'expected_complexity' in test_case:
                if cleaned_data['complexity'] == test_case['expected_complexity']:
                    print(f"✅ {test_case['test_name']}: Complexity normalized to {cleaned_data['complexity']}")
                    passed += 1
                else:
                    print(f"❌ {test_case['test_name']}: Expected {test_case['expected_complexity']}, got {cleaned_data['complexity']}")
                    failed += 1
                    
        except Exception as e:
            print(f"💥 {test_case['test_name']}: Error - {str(e)}")
            failed += 1
    
    print(f"\n📊 Specific Enhancement Tests: {passed} passed, {failed} failed")
    return failed == 0

def run_comparison_test():
    """Compare enhanced validation vs legacy validation"""
    
    print("\n⚖️  Comparison: Enhanced vs Legacy Validation")
    print("="*60)
    
    # Test with the same problematic inputs that caused failures
    test_inputs = [
        '',
        '   ',
        'a',
        'thing',
        'stuff',
        None,
        123,
        '!@#$%^&*()',
        'workflow ' * 100
    ]
    
    enhanced_successes = 0
    legacy_successes = 0
    
    for test_input in test_inputs:
        # Test enhanced validation
        try:
            cleaned_data, _ = validate_workflow_request({'description': test_input})
            workflow = create_basic_workflow(
                cleaned_data['description'],
                cleaned_data['trigger_type'],
                cleaned_data['complexity']
            )
            if workflow and workflow.get('nodes') and len(workflow['nodes']) > 0:
                enhanced_successes += 1
        except:
            pass
        
        # Test legacy validation (simulate)
        try:
            if not test_input or (isinstance(test_input, str) and len(test_input.strip()) < 10):
                continue  # Would fail legacy validation
            
            # Legacy would only succeed with proper strings >= 10 chars
            if isinstance(test_input, str) and len(test_input.strip()) >= 10:
                legacy_successes += 1
        except:
            pass
    
    print(f"Enhanced Validation Successes: {enhanced_successes}/{len(test_inputs)}")
    print(f"Legacy Validation Successes: {legacy_successes}/{len(test_inputs)}")
    print(f"Improvement: +{enhanced_successes - legacy_successes} successful workflows")
    
    return enhanced_successes > legacy_successes

if __name__ == '__main__':
    print("🚀 Enhanced Input Validation Test Suite")
    print("="*60)
    
    try:
        # Run all tests
        test1_passed = test_enhanced_validation()
        test2_passed = test_specific_enhancements()
        test3_passed = run_comparison_test()
        
        print("\n" + "="*60)
        print("🏁 FINAL RESULTS")
        print("="*60)
        
        if test1_passed and test2_passed and test3_passed:
            print("✅ ALL TESTS PASSED - Enhanced validation is working correctly!")
            print("🎯 Expected improvement: Significant reduction in workflow generation failures")
            sys.exit(0)
        else:
            print("❌ SOME TESTS FAILED - Enhanced validation needs adjustment")
            sys.exit(1)
            
    except Exception as e:
        print(f"💥 Test suite error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)