#!/usr/bin/env python3
"""
Final Realistic Assessment
Measure actual improvement while maintaining realistic failure expectations
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

class FinalRealisticTester:
    def __init__(self):
        self.enhanced_passed = 0
        self.enhanced_failed = 0
        self.legacy_passed = 0
        self.legacy_failed = 0
        self.errors = defaultdict(int)
        self.lock = threading.Lock()
        self.start_time = time.time()
        
    def test_enhanced_validation(self, test_input):
        """Test with enhanced validation"""
        try:
            # Use enhanced validation
            cleaned_data, validation_report = validate_workflow_request(test_input)
            
            # Create workflow
            workflow = create_basic_workflow(
                cleaned_data['description'],
                cleaned_data['trigger_type'],
                cleaned_data['complexity'],
                '',
                cleaned_data['advanced_options']
            )
            
            # Realistic quality checks (not overly strict)
            if not isinstance(workflow, dict):
                return False, "Invalid workflow structure"
            
            if not workflow.get('nodes') or len(workflow['nodes']) == 0:
                return False, "No nodes generated"
            
            # Basic node validation
            for node in workflow.get('nodes', []):
                if not isinstance(node, dict):
                    return False, "Invalid node structure"
                if not node.get('id'):
                    return False, "Missing node ID"
                if not node.get('name'):
                    return False, "Missing node name"
                if not node.get('type'):
                    return False, "Missing node type"
            
            # Basic workflow validation
            if not workflow.get('name') or len(workflow['name']) < 5:
                return False, "Invalid workflow name"
            
            # JSON serialization test
            try:
                json.dumps(workflow)
            except (TypeError, ValueError):
                return False, "Not JSON serializable"
            
            return True, "Success"
            
        except Exception as e:
            return False, f"Exception: {str(e)}"
    
    def test_legacy_validation(self, test_input):
        """Test with legacy validation logic"""
        try:
            # Simulate legacy validation
            description = test_input.get('description')
            
            # Legacy validation rules
            if not description:
                return False, "Empty description"
            
            if not isinstance(description, str):
                return False, "Non-string description"
                
            if len(description.strip()) < 10:
                return False, "Description too short"
            
            if len(description) > 5000:
                return False, "Description too long"
            
            trigger_type = test_input.get('triggerType') or test_input.get('trigger_type', 'webhook')
            if trigger_type not in ['webhook', 'schedule', 'manual']:
                return False, "Invalid trigger type"
            
            complexity = test_input.get('complexity', 'medium')
            if complexity not in ['simple', 'medium', 'complex']:
                complexity = 'medium'
            
            # Try to create workflow with original description
            workflow = create_basic_workflow(description, trigger_type, complexity)
            
            # Same quality checks as enhanced
            if not isinstance(workflow, dict):
                return False, "Invalid workflow structure"
            
            if not workflow.get('nodes') or len(workflow['nodes']) == 0:
                return False, "No nodes generated"
            
            for node in workflow.get('nodes', []):
                if not isinstance(node, dict):
                    return False, "Invalid node structure"
                if not node.get('id'):
                    return False, "Missing node ID"
                if not node.get('name'):
                    return False, "Missing node name"
                if not node.get('type'):
                    return False, "Missing node type"
            
            if not workflow.get('name') or len(workflow['name']) < 5:
                return False, "Invalid workflow name"
            
            try:
                json.dumps(workflow)
            except (TypeError, ValueError):
                return False, "Not JSON serializable"
            
            return True, "Success"
            
        except Exception as e:
            return False, f"Exception: {str(e)}"
    
    def run_batch_test(self, test_batch):
        """Run batch test comparing both methods"""
        batch_enhanced_passed = 0
        batch_enhanced_failed = 0
        batch_legacy_passed = 0
        batch_legacy_failed = 0
        batch_errors = defaultdict(int)
        
        for test_name, test_input in test_batch:
            # Test enhanced validation
            enhanced_success, enhanced_error = self.test_enhanced_validation(test_input)
            if enhanced_success:
                batch_enhanced_passed += 1
            else:
                batch_enhanced_failed += 1
                batch_errors[f"Enhanced: {enhanced_error}"] += 1
            
            # Test legacy validation
            legacy_success, legacy_error = self.test_legacy_validation(test_input)
            if legacy_success:
                batch_legacy_passed += 1
            else:
                batch_legacy_failed += 1
                batch_errors[f"Legacy: {legacy_error}"] += 1
        
        # Thread-safe update
        with self.lock:
            self.enhanced_passed += batch_enhanced_passed
            self.enhanced_failed += batch_enhanced_failed
            self.legacy_passed += batch_legacy_passed
            self.legacy_failed += batch_legacy_failed
            for error, count in batch_errors.items():
                self.errors[error] += count
                
        return (batch_enhanced_passed, batch_enhanced_failed, 
                batch_legacy_passed, batch_legacy_failed)
    
    def print_progress(self, completed, total):
        """Print progress"""
        current_time = time.time()
        elapsed = current_time - self.start_time
        rate = completed / elapsed if elapsed > 0 else 0
        
        enhanced_rate = (self.enhanced_passed / completed * 100) if completed > 0 else 0
        legacy_rate = (self.legacy_passed / completed * 100) if completed > 0 else 0
        
        print(f"\r🧪 Progress: {completed:,}/{total:,} ({completed/total*100:.1f}%) | "
              f"Enhanced: {enhanced_rate:.2f}% | Legacy: {legacy_rate:.2f}% | "
              f"⚡ {rate:.0f}/sec", 
              end="", flush=True)
    
    def print_summary(self, total_tests):
        """Print comprehensive comparison summary"""
        total_time = time.time() - self.start_time
        
        enhanced_success_rate = (self.enhanced_passed / total_tests) * 100
        legacy_success_rate = (self.legacy_passed / total_tests) * 100
        improvement = enhanced_success_rate - legacy_success_rate
        
        print("\n" + "="*100)
        print("🔍 FINAL REALISTIC ASSESSMENT RESULTS")
        print("="*100)
        
        print(f"📊 TEST STATISTICS:")
        print(f"   Total Tests: {total_tests:,}")
        print(f"   Duration: {total_time:.1f} seconds")
        print(f"   Speed: {total_tests/total_time:.0f} tests/second")
        
        print(f"\n🔧 ENHANCED VALIDATION:")
        print(f"   ✅ Passed: {self.enhanced_passed:,} ({enhanced_success_rate:.3f}%)")
        print(f"   ❌ Failed: {self.enhanced_failed:,}")
        
        print(f"\n🔧 LEGACY VALIDATION:")
        print(f"   ✅ Passed: {self.legacy_passed:,} ({legacy_success_rate:.3f}%)")
        print(f"   ❌ Failed: {self.legacy_failed:,}")
        
        print(f"\n📈 IMPROVEMENT ANALYSIS:")
        print(f"   Success Rate Improvement: {improvement:+.3f} percentage points")
        print(f"   Additional Successful Workflows: {self.enhanced_passed - self.legacy_passed:,}")
        print(f"   Failure Reduction: {self.legacy_failed - self.enhanced_failed:,}")
        
        if legacy_success_rate > 0:
            relative_improvement = (improvement / legacy_success_rate) * 100
            print(f"   Relative Improvement: {relative_improvement:+.2f}%")
        
        # Quality assessment
        if improvement >= 5.0:
            assessment = "🏆 EXCELLENT IMPROVEMENT"
        elif improvement >= 2.0:
            assessment = "✅ SIGNIFICANT IMPROVEMENT"
        elif improvement >= 1.0:
            assessment = "👍 GOOD IMPROVEMENT"
        elif improvement >= 0.5:
            assessment = "📈 MODERATE IMPROVEMENT"
        elif improvement >= 0.0:
            assessment = "⚠️  MINIMAL IMPROVEMENT"
        else:
            assessment = "❌ REGRESSION"
        
        print(f"   🎯 Assessment: {assessment}")
        
        # Failure rate analysis
        enhanced_failure_rate = (self.enhanced_failed / total_tests) * 100
        legacy_failure_rate = (self.legacy_failed / total_tests) * 100
        
        print(f"\n📉 FAILURE RATE ANALYSIS:")
        print(f"   Enhanced Failure Rate: {enhanced_failure_rate:.3f}%")
        print(f"   Legacy Failure Rate: {legacy_failure_rate:.3f}%")
        print(f"   Failure Rate Reduction: {legacy_failure_rate - enhanced_failure_rate:.3f} percentage points")
        
        # Realistic expectations
        if enhanced_failure_rate <= 2.0:
            failure_assessment = "🌟 EXCELLENT - Very low failure rate"
        elif enhanced_failure_rate <= 5.0:
            failure_assessment = "✅ GOOD - Reasonable failure rate"
        elif enhanced_failure_rate <= 10.0:
            failure_assessment = "👍 ACCEPTABLE - Moderate failure rate"
        else:
            failure_assessment = "⚠️  HIGH - Consider further improvements"
        
        print(f"   Enhanced Failure Assessment: {failure_assessment}")
        
        # Top error analysis
        if self.errors:
            print(f"\n❌ TOP ERROR TYPES:")
            sorted_errors = sorted(self.errors.items(), key=lambda x: x[1], reverse=True)
            for error_type, count in sorted_errors[:8]:
                percentage = (count / (total_tests * 2)) * 100  # *2 because we test both methods
                print(f"   • {error_type}: {count:,} ({percentage:.3f}%)")
        
        # Final verdict
        print(f"\n🎯 FINAL VERDICT:")
        if improvement >= 1.0 and enhanced_failure_rate <= 5.0:
            verdict = "✅ ENHANCED VALIDATION SUCCESSFUL"
            details = "Significant improvement with reasonable failure rate"
        elif improvement >= 0.5:
            verdict = "👍 ENHANCED VALIDATION BENEFICIAL"
            details = "Moderate improvement, good for production"
        elif improvement >= 0.0:
            verdict = "📊 ENHANCED VALIDATION NEUTRAL"
            details = "Minimal improvement, but no regression"
        else:
            verdict = "⚠️  ENHANCED VALIDATION NEEDS REVIEW"
            details = "Performance regression detected"
        
        print(f"   {verdict}")
        print(f"   {details}")
        
        print("="*100)
        return improvement >= 0.5 and enhanced_failure_rate <= 10.0

def generate_balanced_test_data(count=200000):
    """Generate balanced test data for realistic assessment"""
    
    print(f"📋 Generating {count:,} balanced test cases...")
    
    test_data = []
    
    # Good cases that both should handle (50%)
    good_cases = [
        {'description': 'process customer orders for ecommerce platform'},
        {'description': 'manage patient records in healthcare system'},
        {'description': 'automate invoice generation workflow'},
        {'description': 'handle payment processing pipeline'},
        {'description': 'sync inventory data between systems'},
        {'description': 'monitor system health and alerts'},
        {'description': 'validate user input before processing'},
        {'description': 'transform data format for integration'},
        {'description': 'schedule appointment notifications'},
        {'description': 'track shipment status updates'},
        {'description': 'create automated backup system'},
        {'description': 'manage user authentication workflow'},
        {'description': 'process financial transactions'},
        {'description': 'handle customer support tickets'},
        {'description': 'automate report generation'},
    ]
    
    for i in range(int(count * 0.5)):
        case = random.choice(good_cases).copy()
        case['triggerType'] = random.choice(['webhook', 'schedule', 'manual'])
        case['complexity'] = random.choice(['simple', 'medium', 'complex'])
        test_data.append((f"good_{i}", case))
    
    # Cases where enhanced should help (30%)
    enhanced_advantage_cases = [
        {'description': ''},  # Enhanced should handle
        {'description': '   '},  # Enhanced should handle
        {'description': 'thing'},  # Enhanced should improve
        {'description': 'stuff'},  # Enhanced should improve
        {'description': 'process'},  # Enhanced should expand
        {'description': 'workflow'},  # Enhanced should expand
        {'description': None},  # Enhanced should handle
        {'description': 123},  # Enhanced should convert
        {'description': 'a'},  # Enhanced should expand
        {'description': 'x'},  # Enhanced should expand
        {'description': 'flujo de trabajo'},  # Enhanced handles languages
        {'description': 'système workflow'},  # Enhanced handles languages
        {'description': 'do something'},  # Enhanced should improve
        {'description': 'handle stuff'},  # Enhanced should improve
        {'description': 'manage things'},  # Enhanced should improve
    ]
    
    for i in range(int(count * 0.3)):
        case = random.choice(enhanced_advantage_cases).copy()
        case['triggerType'] = random.choice(['webhook', 'schedule', 'manual'])
        case['complexity'] = random.choice(['simple', 'medium', 'complex'])
        test_data.append((f"enhanced_advantage_{i}", case))
    
    # Cases that both should fail (20%)
    both_should_fail_cases = [
        # Completely missing description
        {'triggerType': 'webhook'},
        {'complexity': 'medium'},
        
        # Invalid parameters
        {'description': 'valid workflow', 'triggerType': 'invalid'},
        {'description': 'valid workflow', 'complexity': 'invalid'},
        
        # Extreme cases
        {'description': '\x00\x01\x02'},  # Control characters
        {'description': 'a' * 10000},  # Extremely long
        
        # Empty request
        {},
    ]
    
    for i in range(int(count * 0.2)):
        case = random.choice(both_should_fail_cases).copy()
        test_data.append((f"both_fail_{i}", case))
    
    random.shuffle(test_data)
    
    print(f"✅ Generated {len(test_data):,} test cases")
    print(f"   • {int(count * 0.5):,} good cases (both should pass)")
    print(f"   • {int(count * 0.3):,} enhanced advantage cases")
    print(f"   • {int(count * 0.2):,} failure cases (both should fail)")
    
    return test_data

def run_final_realistic_assessment():
    """Run final realistic assessment"""
    
    print("🔍 FINAL REALISTIC ASSESSMENT")
    print("="*100)
    print("🎯 Goal: Measure actual improvement with realistic expectations")
    print("⚖️  Method: Direct comparison of enhanced vs legacy validation")
    print("📊 Expected: Enhanced should show improvement on problematic inputs")
    
    # Generate test data
    test_data = generate_balanced_test_data(200000)
    
    # Initialize tester
    tester = FinalRealisticTester()
    
    print(f"\n🧪 EXECUTING {len(test_data):,} COMPARATIVE TESTS...")
    print("="*100)
    
    # Run tests
    batch_size = 1000
    max_workers = 8
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        
        # Submit batches
        for i in range(0, len(test_data), batch_size):
            batch = test_data[i:i + batch_size]
            future = executor.submit(tester.run_batch_test, batch)
            futures.append(future)
        
        # Process results
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
                completed += batch_size
                tester.print_progress(min(completed, len(test_data)), len(test_data))
            except Exception as e:
                print(f"\n⚠️  Batch error: {e}")
                completed += batch_size
    
    print()  # New line after progress
    
    # Print results
    return tester.print_summary(len(test_data))

if __name__ == '__main__':
    try:
        print("🚀 FINAL REALISTIC ASSESSMENT")
        print("🎯 Measuring actual improvement of enhanced validation")
        print("⚖️  Comparing enhanced vs legacy validation side-by-side")
        print()
        
        success = run_final_realistic_assessment()
        
        print(f"\n📊 CONCLUSION:")
        if success:
            print("✅ ENHANCED VALIDATION ASSESSMENT SUCCESSFUL")
            print("🎯 Enhanced validation demonstrates measurable improvement")
            print("🚀 RECOMMENDATION: Deploy enhanced validation to production")
        else:
            print("⚠️  ENHANCED VALIDATION NEEDS REVIEW")
            print("🔧 Improvement insufficient or failure rate too high")
            print("📊 Consider further optimization before deployment")
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Assessment interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n\n💥 Assessment error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)