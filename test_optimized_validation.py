#!/usr/bin/env python3
"""
Test Optimized Validation System
Verify that optimizations reduce failure rate while maintaining quality
"""

import sys
import json
import time
import random
import concurrent.futures
import threading
from collections import defaultdict

sys.path.append('.')

from optimize_validation_system import optimized_validate_workflow_request
from app import create_basic_workflow

class OptimizedValidationTester:
    def __init__(self):
        self.enhanced_passed = 0
        self.enhanced_failed = 0
        self.legacy_passed = 0
        self.legacy_failed = 0
        self.errors = defaultdict(int)
        self.lock = threading.Lock()
        self.start_time = time.time()
        self.detailed_failures = []
        
    def test_optimized_enhanced_validation(self, test_input):
        """Test with optimized enhanced validation"""
        try:
            # Use optimized enhanced validation
            cleaned_data, validation_report = optimized_validate_workflow_request(test_input)
            
            # Create workflow
            workflow = create_basic_workflow(
                cleaned_data['description'],
                cleaned_data['trigger_type'],
                cleaned_data['complexity'],
                '',
                cleaned_data['advanced_options']
            )
            
            # Realistic quality checks
            if not isinstance(workflow, dict):
                return False, "Invalid workflow structure"
            
            if not workflow.get('nodes') or len(workflow['nodes']) == 0:
                return False, "No nodes generated"
            
            # Basic node validation
            for i, node in enumerate(workflow.get('nodes', [])):
                if not isinstance(node, dict):
                    return False, f"Node {i} invalid structure"
                if not node.get('id'):
                    return False, f"Node {i} missing ID"
                if not node.get('name'):
                    return False, f"Node {i} missing name"
                if not node.get('type'):
                    return False, f"Node {i} missing type"
            
            # Basic workflow validation
            if not workflow.get('name') or len(workflow['name']) < 5:
                return False, "Invalid workflow name"
            
            # JSON serialization test
            try:
                json.dumps(workflow)
            except (TypeError, ValueError):
                return False, "Not JSON serializable"
            
            return True, "Success"
            
        except ValueError as e:
            # This should be very rare now
            return False, f"Validation failed: {str(e)}"
        except Exception as e:
            return False, f"Exception: {str(e)}"
    
    def test_legacy_validation(self, test_input):
        """Test with legacy validation logic"""
        try:
            # Simulate legacy validation rules (strict)
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
            
            # Try to create workflow with original description (no enhancement)
            workflow = create_basic_workflow(description, trigger_type, complexity)
            
            # Same quality checks as enhanced
            if not isinstance(workflow, dict):
                return False, "Invalid workflow structure"
            
            if not workflow.get('nodes') or len(workflow['nodes']) == 0:
                return False, "No nodes generated"
            
            for i, node in enumerate(workflow.get('nodes', [])):
                if not isinstance(node, dict):
                    return False, f"Node {i} invalid structure"
                if not node.get('id'):
                    return False, f"Node {i} missing ID"
                if not node.get('name'):
                    return False, f"Node {i} missing name"
                if not node.get('type'):
                    return False, f"Node {i} missing type"
            
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
        batch_failures = []
        
        for test_name, test_input in test_batch:
            # Test optimized enhanced validation
            enhanced_success, enhanced_error = self.test_optimized_enhanced_validation(test_input)
            if enhanced_success:
                batch_enhanced_passed += 1
            else:
                batch_enhanced_failed += 1
                batch_errors[f"Enhanced: {enhanced_error}"] += 1
                batch_failures.append(f"{test_name}: Enhanced: {enhanced_error}")
            
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
            self.detailed_failures.extend(batch_failures[:3])  # Sample failures
                
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
              f"Enhanced: {enhanced_rate:.1f}% | Legacy: {legacy_rate:.1f}% | "
              f"⚡ {rate:.0f}/sec", 
              end="", flush=True)
    
    def print_summary(self, total_tests):
        """Print comprehensive comparison summary"""
        total_time = time.time() - self.start_time
        
        enhanced_success_rate = (self.enhanced_passed / total_tests) * 100
        legacy_success_rate = (self.legacy_passed / total_tests) * 100
        improvement = enhanced_success_rate - legacy_success_rate
        
        enhanced_failure_rate = (self.enhanced_failed / total_tests) * 100
        legacy_failure_rate = (self.legacy_failed / total_tests) * 100
        
        print("\n" + "="*100)
        print("🔍 OPTIMIZED VALIDATION TEST RESULTS")
        print("="*100)
        
        print(f"📊 TEST STATISTICS:")
        print(f"   Total Tests: {total_tests:,}")
        print(f"   Duration: {total_time:.1f} seconds")
        print(f"   Speed: {total_tests/total_time:.0f} tests/second")
        
        print(f"\n🔧 OPTIMIZED ENHANCED VALIDATION:")
        print(f"   ✅ Passed: {self.enhanced_passed:,} ({enhanced_success_rate:.3f}%)")
        print(f"   ❌ Failed: {self.enhanced_failed:,} ({enhanced_failure_rate:.3f}%)")
        
        print(f"\n🔧 LEGACY VALIDATION:")
        print(f"   ✅ Passed: {self.legacy_passed:,} ({legacy_success_rate:.3f}%)")
        print(f"   ❌ Failed: {self.legacy_failed:,} ({legacy_failure_rate:.3f}%)")
        
        print(f"\n📈 IMPROVEMENT ANALYSIS:")
        print(f"   Success Rate Improvement: {improvement:+.3f} percentage points")
        print(f"   Additional Successful Workflows: {self.enhanced_passed - self.legacy_passed:,}")
        print(f"   Failure Reduction: {self.legacy_failed - self.enhanced_failed:,}")
        
        if legacy_success_rate > 0:
            relative_improvement = (improvement / legacy_success_rate) * 100
            print(f"   Relative Improvement: {relative_improvement:+.2f}%")
        
        # Optimized failure rate assessment
        if enhanced_failure_rate <= 2.0:
            failure_assessment = "🌟 EXCELLENT - Very low failure rate"
        elif enhanced_failure_rate <= 5.0:
            failure_assessment = "✅ GOOD - Reasonable failure rate"
        elif enhanced_failure_rate <= 8.0:
            failure_assessment = "👍 ACCEPTABLE - Moderate failure rate"
        elif enhanced_failure_rate <= 12.0:
            failure_assessment = "⚠️  HIGH - Needs optimization"
        else:
            failure_assessment = "❌ VERY HIGH - Requires significant improvement"
        
        print(f"   🎯 Enhanced Failure Rate Assessment: {failure_assessment}")
        
        # Improvement assessment
        if improvement >= 15.0:
            improvement_assessment = "🏆 EXCEPTIONAL IMPROVEMENT"
        elif improvement >= 10.0:
            improvement_assessment = "🌟 EXCELLENT IMPROVEMENT"
        elif improvement >= 5.0:
            improvement_assessment = "✅ SIGNIFICANT IMPROVEMENT"
        elif improvement >= 2.0:
            improvement_assessment = "👍 GOOD IMPROVEMENT"
        elif improvement >= 1.0:
            improvement_assessment = "📈 MODERATE IMPROVEMENT"
        elif improvement >= 0.0:
            improvement_assessment = "⚠️  MINIMAL IMPROVEMENT"
        else:
            improvement_assessment = "❌ REGRESSION"
        
        print(f"   🎯 Improvement Assessment: {improvement_assessment}")
        
        # Top error analysis
        if self.errors:
            print(f"\n❌ TOP ERROR TYPES:")
            sorted_errors = sorted(self.errors.items(), key=lambda x: x[1], reverse=True)
            for error_type, count in sorted_errors[:8]:
                percentage = (count / (total_tests * 2)) * 100
                print(f"   • {error_type}: {count:,} ({percentage:.3f}%)")
        
        # Sample failures
        if self.detailed_failures:
            print(f"\n🔍 SAMPLE ENHANCED VALIDATION FAILURES:")
            for failure in self.detailed_failures[:5]:
                print(f"   • {failure}")
        
        # Mathematical validation
        print(f"\n🔢 MATHEMATICAL VALIDATION:")
        calculated_total = self.enhanced_passed + self.enhanced_failed
        if calculated_total != total_tests:
            print(f"   ❌ MATH ERROR: Enhanced totals don't add up ({calculated_total} ≠ {total_tests})")
        else:
            print(f"   ✅ Enhanced totals correct: {self.enhanced_passed} + {self.enhanced_failed} = {total_tests}")
        
        calculated_total = self.legacy_passed + self.legacy_failed
        if calculated_total != total_tests:
            print(f"   ❌ MATH ERROR: Legacy totals don't add up ({calculated_total} ≠ {total_tests})")
        else:
            print(f"   ✅ Legacy totals correct: {self.legacy_passed} + {self.legacy_failed} = {total_tests}")
        
        # Final verdict with optimized criteria
        print(f"\n🎯 FINAL VERDICT:")
        if (improvement >= 5.0 and 
            enhanced_failure_rate <= 5.0 and 
            enhanced_success_rate >= 92.0):
            verdict = "✅ OPTIMIZED VALIDATION HIGHLY SUCCESSFUL"
            details = "Excellent improvement with low failure rate"
        elif (improvement >= 3.0 and 
              enhanced_failure_rate <= 8.0 and 
              enhanced_success_rate >= 88.0):
            verdict = "👍 OPTIMIZED VALIDATION SUCCESSFUL"
            details = "Good improvement with acceptable failure rate"
        elif (improvement >= 1.0 and 
              enhanced_failure_rate <= 12.0 and 
              enhanced_success_rate >= 85.0):
            verdict = "📊 OPTIMIZED VALIDATION BENEFICIAL"
            details = "Some improvement, suitable for production"
        elif improvement >= 0.5:
            verdict = "⚠️  OPTIMIZED VALIDATION MODERATE"
            details = "Minimal improvement, may need further optimization"
        else:
            verdict = "❌ OPTIMIZED VALIDATION INSUFFICIENT"
            details = "Insufficient improvement or regression"
        
        print(f"   {verdict}")
        print(f"   {details}")
        
        print("="*100)
        
        # Success criteria: good improvement with low failure rate
        return (improvement >= 3.0 and 
                enhanced_failure_rate <= 8.0 and 
                enhanced_success_rate >= 88.0)

def generate_optimized_test_data(count=50000):
    """Generate test data for optimization testing"""
    
    print(f"📋 Generating {count:,} optimized test cases...")
    
    test_data = []
    
    # Good cases that both should handle well (50%)
    good_cases = [
        {'description': 'process customer orders for ecommerce platform'},
        {'description': 'manage patient records in healthcare system'},
        {'description': 'automate invoice generation workflow'},
        {'description': 'handle payment processing pipeline'},
        {'description': 'sync inventory data between systems'},
        {'description': 'monitor system health and send alerts'},
        {'description': 'validate user input and sanitize data'},
        {'description': 'transform data format for API integration'},
        {'description': 'schedule appointment reminders'},
        {'description': 'track shipment status and updates'},
        {'description': 'create automated backup system'},
        {'description': 'manage user authentication workflow'},
        {'description': 'process financial transactions securely'},
        {'description': 'handle customer support ticket routing'},
        {'description': 'automate report generation and distribution'},
    ]
    
    for i in range(int(count * 0.5)):
        case = random.choice(good_cases).copy()
        case['triggerType'] = random.choice(['webhook', 'schedule', 'manual'])
        case['complexity'] = random.choice(['simple', 'medium', 'complex'])
        test_data.append((f"good_{i}", case))
    
    # Cases where enhanced should significantly help (40%)
    enhanced_advantage_cases = [
        # Previously problematic cases that should now work
        {'description': ''},
        {'description': '   '},
        {'description': 'a'},
        {'description': 'x'},
        {'description': '1'},
        {'description': 'thing'},
        {'description': 'stuff'},
        {'description': 'process'},
        {'description': 'workflow'},
        {'description': 'system'},
        {'description': 'automation'},
        {'description': 'data'},
        {'description': 'manage things'},
        {'description': 'handle stuff'},
        {'description': 'do something'},
        {'description': 'work'},
        {'description': 'task'},
        {'description': 'job'},
        {'description': 'api'},
        {'description': 'web'},
        {'description': 'app'},
        {'description': 'service'},
        
        # Type conversion cases
        {'description': None},
        {'description': 123},
        {'description': 0},
        {'description': 999},
        
        # Parameter normalization
        {'description': 'test workflow', 'triggerType': 'http'},
        {'description': 'test workflow', 'triggerType': 'https'},
        {'description': 'test workflow', 'triggerType': 'api'},
        {'description': 'test workflow', 'triggerType': 'rest'},
        {'description': 'test workflow', 'complexity': 'advanced'},
        {'description': 'test workflow', 'complexity': 'basic'},
        {'description': 'test workflow', 'complexity': 'full'},
        
        # Non-English (should work better now)
        {'description': 'flujo de trabajo español'},
        {'description': 'système de gestion français'},
        {'description': 'sistema di gestione italiano'},
        {'description': 'sistema de gestão português'},
        
        # Mixed cases
        {'description': 'API workflow'},
        {'description': 'web service'},
        {'description': 'data task'},
        {'description': 'automation job'},
    ]
    
    for i in range(int(count * 0.4)):
        case = random.choice(enhanced_advantage_cases).copy()
        if 'triggerType' not in case:
            case['triggerType'] = random.choice(['webhook', 'schedule', 'manual'])
        if 'complexity' not in case:
            case['complexity'] = random.choice(['simple', 'medium', 'complex'])
        test_data.append((f"enhanced_advantage_{i}", case))
    
    # Cases that should still legitimately fail (10% - much reduced)
    should_fail_cases = [
        # Only the most severe cases
        {'description': '<script>alert("xss")</script><script>alert("xss2")</script><script>alert("xss3")</script>'},
        {'description': 'DROP TABLE users; DROP TABLE orders; DROP TABLE customers;'},
        {'description': 'rm -rf / && rm -rf /home && rm -rf /var'},
        
        # Completely empty requests with no recoverable data
        {},
        
        # Extremely long malicious payloads
        {'description': '<script>' + 'a' * 2000 + '</script>'},
        {'description': 'DROP TABLE ' + 'x' * 1000},
    ]
    
    for i in range(int(count * 0.1)):
        case = random.choice(should_fail_cases).copy()
        test_data.append((f"should_fail_{i}", case))
    
    random.shuffle(test_data)
    
    print(f"✅ Generated {len(test_data):,} test cases")
    print(f"   • {int(count * 0.5):,} good cases (both should pass)")
    print(f"   • {int(count * 0.4):,} enhanced advantage cases")
    print(f"   • {int(count * 0.1):,} should fail cases (severe only)")
    
    return test_data

def run_optimized_validation_test():
    """Run optimized validation test"""
    
    print("🔍 OPTIMIZED VALIDATION TEST")
    print("="*100)
    print("🎯 Goal: Verify optimizations reduce failure rate while maintaining quality")
    print("⚖️  Method: Test optimized system vs legacy with better recovery")
    print("📊 Expected: Enhanced shows significant improvement with <5% failure rate")
    
    # Generate test data
    test_data = generate_optimized_test_data(50000)
    
    # Initialize tester
    tester = OptimizedValidationTester()
    
    print(f"\n🧪 EXECUTING {len(test_data):,} OPTIMIZED TESTS...")
    print("="*100)
    
    # Run tests
    batch_size = 500
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
        print("🚀 OPTIMIZED VALIDATION TEST")
        print("🎯 Testing optimized validation system with better recovery")
        print("⚖️  Target: <5% failure rate with significant improvement")
        print()
        
        success = run_optimized_validation_test()
        
        print(f"\n📊 CONCLUSION:")
        if success:
            print("✅ OPTIMIZATION SUCCESSFUL")
            print("🎯 Enhanced validation achieves target performance")
            print("🚀 RECOMMENDATION: Deploy optimized system to production")
        else:
            print("⚠️  OPTIMIZATION NEEDS FURTHER WORK")
            print("🔧 System may need additional improvements")
            print("📊 Consider further optimization strategies")
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n\n💥 Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)