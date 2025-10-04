#!/usr/bin/env python3
"""
Test Validation Improvement Impact
Measure the improvement in success rate with enhanced validation
"""

import sys
import json
import time
import random
import concurrent.futures
import threading
from collections import defaultdict

sys.path.append('.')

from enhanced_input_validation import validate_workflow_request
from app import create_basic_workflow

class ValidationImprovementTester:
    def __init__(self):
        self.enhanced_passed = 0
        self.enhanced_failed = 0
        self.legacy_passed = 0
        self.legacy_failed = 0
        self.lock = threading.Lock()
        
    def test_enhanced_validation(self, test_input):
        """Test with enhanced validation"""
        try:
            cleaned_data, validation_report = validate_workflow_request(test_input)
            
            workflow = create_basic_workflow(
                cleaned_data['description'],
                cleaned_data['trigger_type'],
                cleaned_data['complexity'],
                '',
                cleaned_data['advanced_options']
            )
            
            # Strict validation criteria
            if (workflow and 
                isinstance(workflow, dict) and 
                workflow.get('nodes') and 
                len(workflow['nodes']) > 0 and
                len(workflow.get('name', '')) > 5):
                return True
            else:
                return False
                
        except Exception:
            return False
    
    def test_legacy_validation(self, test_input):
        """Test with legacy validation logic"""
        try:
            description = test_input.get('description', '')
            
            # Legacy validation rules
            if not description:
                return False
            
            if not isinstance(description, str):
                return False
                
            if len(description.strip()) < 10:
                return False
            
            if len(description) > 5000:
                return False
            
            trigger_type = test_input.get('triggerType') or test_input.get('trigger_type', 'webhook')
            if trigger_type not in ['webhook', 'schedule', 'manual']:
                return False
            
            complexity = test_input.get('complexity', 'medium')
            if complexity not in ['simple', 'medium', 'complex']:
                complexity = 'medium'
            
            # Try to create workflow
            workflow = create_basic_workflow(description, trigger_type, complexity)
            
            if (workflow and 
                isinstance(workflow, dict) and 
                workflow.get('nodes') and 
                len(workflow['nodes']) > 0):
                return True
            else:
                return False
                
        except Exception:
            return False
    
    def run_batch_test(self, test_batch):
        """Run a batch of tests comparing both validation methods"""
        batch_enhanced_passed = 0
        batch_enhanced_failed = 0
        batch_legacy_passed = 0
        batch_legacy_failed = 0
        
        for test_input in test_batch:
            # Test enhanced validation
            if self.test_enhanced_validation(test_input):
                batch_enhanced_passed += 1
            else:
                batch_enhanced_failed += 1
            
            # Test legacy validation
            if self.test_legacy_validation(test_input):
                batch_legacy_passed += 1
            else:
                batch_legacy_failed += 1
        
        # Update global counters
        with self.lock:
            self.enhanced_passed += batch_enhanced_passed
            self.enhanced_failed += batch_enhanced_failed
            self.legacy_passed += batch_legacy_passed
            self.legacy_failed += batch_legacy_failed
        
        return (batch_enhanced_passed, batch_enhanced_failed, 
                batch_legacy_passed, batch_legacy_failed)

def generate_test_data(count=100000):
    """Generate test data including problematic cases"""
    
    print(f"📋 Generating {count:,} test cases...")
    
    test_data = []
    
    # Normal cases (70%)
    normal_descriptions = [
        'process customer orders', 'manage patient records', 'handle payment transactions',
        'automate invoice generation', 'sync inventory data', 'monitor system health',
        'validate user input', 'transform data format', 'send notifications',
        'schedule appointments', 'track shipments', 'analyze sales data'
    ]
    
    for i in range(int(count * 0.7)):
        desc = random.choice(normal_descriptions)
        if i % 3 == 0:
            desc = f"automated {desc} system"
        elif i % 3 == 1:
            desc = f"{desc} workflow"
        
        test_data.append({
            'description': desc,
            'triggerType': random.choice(['webhook', 'schedule', 'manual']),
            'complexity': random.choice(['simple', 'medium', 'complex'])
        })
    
    # Problematic cases (30%) - These should show the biggest improvement
    problematic_cases = [
        # Empty/minimal
        {'description': ''},
        {'description': '   '},
        {'description': 'a'},
        {'description': 'x'},
        {'description': None},
        {'description': 123},
        {'description': 0},
        
        # Generic/ambiguous
        {'description': 'thing'},
        {'description': 'stuff'},
        {'description': 'process'},
        {'description': 'workflow'},
        {'description': 'system'},
        {'description': 'automation'},
        {'description': 'do something'},
        {'description': 'handle stuff'},
        {'description': 'manage things'},
        
        # Non-English
        {'description': 'flujo de trabajo'},
        {'description': 'système workflow'},
        {'description': 'システム process'},
        {'description': 'процесс данных'},
        
        # Special characters
        {'description': '!@#$%^&*()'},
        {'description': '<script>alert("xss")</script>'},
        {'description': 'DROP TABLE users;'},
        {'description': '../../etc/passwd'},
        
        # Very long
        {'description': 'workflow ' * 500},
        {'description': 'a' * 1000},
        
        # Invalid parameters
        {'description': 'test workflow', 'triggerType': 'invalid'},
        {'description': 'test workflow', 'triggerType': None},
        {'description': 'test workflow', 'complexity': 'invalid'},
        {'description': 'test workflow', 'complexity': None},
    ]
    
    # Add problematic cases
    for i in range(int(count * 0.3)):
        case = random.choice(problematic_cases).copy()
        # Add some variation
        if 'triggerType' not in case:
            case['triggerType'] = random.choice(['webhook', 'schedule', 'manual', 'invalid', None])
        if 'complexity' not in case:
            case['complexity'] = random.choice(['simple', 'medium', 'complex', 'invalid', None])
        
        test_data.append(case)
    
    random.shuffle(test_data)
    print(f"✅ Generated {len(test_data):,} test cases")
    return test_data

def run_validation_improvement_test():
    """Run the validation improvement test"""
    
    print("🔍 VALIDATION IMPROVEMENT TEST")
    print("="*80)
    print("🎯 Goal: Measure improvement in success rate with enhanced validation")
    print("⚖️  Method: Compare enhanced vs legacy validation on same test data")
    
    # Generate test data
    test_data = generate_test_data(100000)  # 100k tests for good statistics
    
    # Initialize tester
    tester = ValidationImprovementTester()
    
    print(f"\n🧪 Running {len(test_data):,} validation tests...")
    print("="*80)
    
    start_time = time.time()
    
    # Run tests in parallel
    batch_size = 1000
    max_workers = 8
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        
        # Submit batches
        for i in range(0, len(test_data), batch_size):
            batch = test_data[i:i + batch_size]
            future = executor.submit(tester.run_batch_test, batch)
            futures.append(future)
        
        # Process results with progress
        completed_batches = 0
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
                completed_batches += 1
                
                if completed_batches % 10 == 0:
                    progress = (completed_batches * batch_size / len(test_data)) * 100
                    elapsed = time.time() - start_time
                    rate = (completed_batches * batch_size) / elapsed
                    print(f"\r🔄 Progress: {progress:.1f}% | {rate:.0f} tests/sec", end="", flush=True)
                    
            except Exception as e:
                print(f"\n⚠️  Batch error: {e}")
    
    print()  # New line after progress
    
    # Calculate results
    total_tests = tester.enhanced_passed + tester.enhanced_failed
    enhanced_success_rate = (tester.enhanced_passed / total_tests) * 100
    legacy_success_rate = (tester.legacy_passed / total_tests) * 100
    improvement = enhanced_success_rate - legacy_success_rate
    
    elapsed_time = time.time() - start_time
    
    # Print results
    print("\n" + "="*80)
    print("📊 VALIDATION IMPROVEMENT RESULTS")
    print("="*80)
    
    print(f"Total Tests: {total_tests:,}")
    print(f"Test Duration: {elapsed_time:.1f} seconds")
    print(f"Test Speed: {total_tests/elapsed_time:.0f} tests/second")
    
    print(f"\n🔧 ENHANCED VALIDATION:")
    print(f"   ✅ Passed: {tester.enhanced_passed:,} ({enhanced_success_rate:.3f}%)")
    print(f"   ❌ Failed: {tester.enhanced_failed:,}")
    
    print(f"\n🔧 LEGACY VALIDATION:")
    print(f"   ✅ Passed: {tester.legacy_passed:,} ({legacy_success_rate:.3f}%)")
    print(f"   ❌ Failed: {tester.legacy_failed:,}")
    
    print(f"\n📈 IMPROVEMENT:")
    print(f"   Success Rate Improvement: +{improvement:.3f} percentage points")
    print(f"   Additional Successful Workflows: {tester.enhanced_passed - tester.legacy_passed:,}")
    print(f"   Failure Reduction: {tester.legacy_failed - tester.enhanced_failed:,}")
    
    # Calculate relative improvement
    if legacy_success_rate > 0:
        relative_improvement = (improvement / legacy_success_rate) * 100
        print(f"   Relative Improvement: +{relative_improvement:.1f}%")
    
    # Quality assessment
    if improvement >= 5.0:
        assessment = "🏆 EXCELLENT IMPROVEMENT"
    elif improvement >= 2.0:
        assessment = "✅ SIGNIFICANT IMPROVEMENT"
    elif improvement >= 1.0:
        assessment = "👍 GOOD IMPROVEMENT"
    elif improvement >= 0.5:
        assessment = "📈 MODERATE IMPROVEMENT"
    else:
        assessment = "⚠️  MINIMAL IMPROVEMENT"
    
    print(f"\n🎯 ASSESSMENT: {assessment}")
    
    # Projected impact on 10M tests
    if improvement > 0:
        projected_improvement = int((improvement / 100) * 10000000)
        print(f"🚀 PROJECTED IMPACT: +{projected_improvement:,} successful workflows in 10M test suite")
        
        # Calculate new expected success rate
        original_success_rate = 98.464  # From previous test
        new_success_rate = min(99.999, original_success_rate + improvement)
        print(f"📊 EXPECTED NEW SUCCESS RATE: {new_success_rate:.3f}%")
    
    print("="*80)
    
    return improvement >= 1.0  # Success if improvement is at least 1 percentage point

if __name__ == '__main__':
    try:
        print("🚀 Validation Improvement Analysis")
        print("🎯 Measuring the impact of enhanced input validation")
        print()
        
        success = run_validation_improvement_test()
        
        if success:
            print("✅ VALIDATION IMPROVEMENT CONFIRMED")
            print("🎯 Enhanced validation significantly improves success rates")
            sys.exit(0)
        else:
            print("⚠️  IMPROVEMENT BELOW THRESHOLD")
            print("🔧 Consider further enhancements to validation logic")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n\n💥 Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)