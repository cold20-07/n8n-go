#!/usr/bin/env python3
"""
Corrected Logic and Math Test
Tests the validation system with proper logic and mathematics
"""

import sys
import json
import time
import random
import concurrent.futures
import threading
from collections import defaultdict

sys.path.append('.')

from corrected_validation_system import corrected_validate_workflow_request
from app import create_basic_workflow

class CorrectedLogicTester:
    def __init__(self):
        self.enhanced_passed = 0
        self.enhanced_failed = 0
        self.legacy_passed = 0
        self.legacy_failed = 0
        self.errors = defaultdict(int)
        self.lock = threading.Lock()
        self.start_time = time.time()
        self.detailed_failures = []
        
    def test_corrected_enhanced_validation(self, test_input):
        """Test with corrected enhanced validation that can legitimately fail"""
        try:
            # Use corrected enhanced validation
            cleaned_data, validation_report = corrected_validate_workflow_request(test_input)
            
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
            
            # Additional quality check based on confidence
            confidence = validation_report.get('overall_confidence', 0.0)
            if confidence < 0.3:  # Low confidence workflows might be questionable
                return False, f"Low confidence workflow: {confidence:.3f}"
            
            return True, "Success"
            
        except ValueError as e:
            # This is a legitimate failure from the corrected validator
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
            # Test corrected enhanced validation
            enhanced_success, enhanced_error = self.test_corrected_enhanced_validation(test_input)
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
            self.detailed_failures.extend(batch_failures[:5])  # Sample failures
                
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
        """Print comprehensive comparison summary with corrected logic"""
        total_time = time.time() - self.start_time
        
        enhanced_success_rate = (self.enhanced_passed / total_tests) * 100
        legacy_success_rate = (self.legacy_passed / total_tests) * 100
        improvement = enhanced_success_rate - legacy_success_rate
        
        enhanced_failure_rate = (self.enhanced_failed / total_tests) * 100
        legacy_failure_rate = (self.legacy_failed / total_tests) * 100
        
        print("\n" + "="*100)
        print("🔍 CORRECTED LOGIC AND MATH TEST RESULTS")
        print("="*100)
        
        print(f"📊 TEST STATISTICS:")
        print(f"   Total Tests: {total_tests:,}")
        print(f"   Duration: {total_time:.1f} seconds")
        print(f"   Speed: {total_tests/total_time:.0f} tests/second")
        
        print(f"\n🔧 CORRECTED ENHANCED VALIDATION:")
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
        
        # Realistic quality assessment
        if enhanced_failure_rate > 10.0:
            assessment = "❌ HIGH FAILURE RATE - Needs improvement"
        elif enhanced_failure_rate > 5.0:
            assessment = "⚠️  MODERATE FAILURE RATE - Acceptable but could improve"
        elif enhanced_failure_rate > 2.0:
            assessment = "👍 REASONABLE FAILURE RATE - Good for production"
        elif enhanced_failure_rate > 0.5:
            assessment = "✅ LOW FAILURE RATE - Excellent quality"
        else:
            assessment = "⚠️  SUSPICIOUSLY LOW FAILURE RATE - Check test validity"
        
        print(f"   🎯 Enhanced Failure Rate Assessment: {assessment}")
        
        # Improvement assessment
        if improvement >= 10.0:
            improvement_assessment = "🏆 EXCEPTIONAL IMPROVEMENT"
        elif improvement >= 5.0:
            improvement_assessment = "🌟 EXCELLENT IMPROVEMENT"
        elif improvement >= 2.0:
            improvement_assessment = "✅ SIGNIFICANT IMPROVEMENT"
        elif improvement >= 1.0:
            improvement_assessment = "👍 GOOD IMPROVEMENT"
        elif improvement >= 0.5:
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
            for error_type, count in sorted_errors[:10]:
                percentage = (count / (total_tests * 2)) * 100  # *2 because we test both methods
                print(f"   • {error_type}: {count:,} ({percentage:.3f}%)")
        
        # Sample failures
        if self.detailed_failures:
            print(f"\n🔍 SAMPLE ENHANCED VALIDATION FAILURES:")
            for failure in self.detailed_failures[:8]:
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
        
        # Final verdict with corrected logic
        print(f"\n🎯 FINAL VERDICT:")
        if (improvement >= 2.0 and 
            1.0 <= enhanced_failure_rate <= 8.0 and 
            enhanced_success_rate >= 90.0):
            verdict = "✅ CORRECTED ENHANCED VALIDATION SUCCESSFUL"
            details = "Significant improvement with realistic failure rate"
        elif (improvement >= 1.0 and 
              enhanced_failure_rate <= 10.0 and 
              enhanced_success_rate >= 85.0):
            verdict = "👍 CORRECTED ENHANCED VALIDATION BENEFICIAL"
            details = "Good improvement with acceptable failure rate"
        elif improvement >= 0.5:
            verdict = "📊 CORRECTED ENHANCED VALIDATION MODERATE"
            details = "Some improvement, may need optimization"
        elif improvement >= 0.0:
            verdict = "⚠️  CORRECTED ENHANCED VALIDATION MINIMAL"
            details = "Little improvement, consider alternatives"
        else:
            verdict = "❌ CORRECTED ENHANCED VALIDATION PROBLEMATIC"
            details = "Performance regression detected"
        
        print(f"   {verdict}")
        print(f"   {details}")
        
        print("="*100)
        
        # Success criteria: meaningful improvement with realistic failure rate
        return (improvement >= 1.0 and 
                1.0 <= enhanced_failure_rate <= 8.0 and 
                enhanced_success_rate >= 90.0)

def generate_corrected_test_data(count=50000):
    """Generate test data with proper distribution for realistic testing"""
    
    print(f"📋 Generating {count:,} corrected test cases...")
    
    test_data = []
    
    # Good cases that both should handle well (60%)
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
    
    for i in range(int(count * 0.6)):
        case = random.choice(good_cases).copy()
        case['triggerType'] = random.choice(['webhook', 'schedule', 'manual'])
        case['complexity'] = random.choice(['simple', 'medium', 'complex'])
        test_data.append((f"good_{i}", case))
    
    # Cases where enhanced should help (25%)
    enhanced_advantage_cases = [
        # Recoverable cases
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
        
        # Type conversion cases
        {'description': 123},
        {'description': 0},
        
        # Parameter normalization
        {'description': 'test workflow', 'triggerType': 'http'},
        {'description': 'test workflow', 'complexity': 'advanced'},
        
        # Non-English (should work)
        {'description': 'flujo de trabajo español'},
        {'description': 'système de gestion français'},
    ]
    
    for i in range(int(count * 0.25)):
        case = random.choice(enhanced_advantage_cases).copy()
        if 'triggerType' not in case:
            case['triggerType'] = random.choice(['webhook', 'schedule', 'manual'])
        if 'complexity' not in case:
            case['complexity'] = random.choice(['simple', 'medium', 'complex'])
        test_data.append((f"enhanced_advantage_{i}", case))
    
    # Cases that SHOULD legitimately fail (15%)
    should_fail_cases = [
        # Completely empty requests
        {},
        
        # Malicious inputs
        {'description': '<script>alert("xss")</script><script>alert("xss2")</script>'},
        {'description': 'DROP TABLE users; DROP TABLE orders;'},
        {'description': 'rm -rf / && rm -rf /home'},
        
        # Impossible inputs
        {'description': '\x00\x01\x02\x03\x04'},
        {'description': 'a' * 10000},  # Extremely long
        {'description': ''},  # Will be enhanced but might still fail confidence
        {'description': '   '},  # Will be enhanced but might still fail confidence
        {'description': None},  # Will be enhanced but might still fail confidence
        
        # Severely corrupted data
        {'description': 'test', 'triggerType': ['invalid', 'array']},
        {'description': 'test', 'complexity': {'invalid': 'object'}},
    ]
    
    for i in range(int(count * 0.15)):
        case = random.choice(should_fail_cases).copy()
        test_data.append((f"should_fail_{i}", case))
    
    random.shuffle(test_data)
    
    print(f"✅ Generated {len(test_data):,} test cases")
    print(f"   • {int(count * 0.6):,} good cases (both should pass)")
    print(f"   • {int(count * 0.25):,} enhanced advantage cases")
    print(f"   • {int(count * 0.15):,} should fail cases (legitimate failures)")
    
    return test_data

def run_corrected_logic_and_math_test():
    """Run corrected test with proper logic and mathematics"""
    
    print("🔍 CORRECTED LOGIC AND MATH TEST")
    print("="*100)
    print("🎯 Goal: Test with corrected logic and realistic mathematics")
    print("⚖️  Method: Proper comparison with legitimate failure detection")
    print("📊 Expected: Enhanced shows improvement with 2-5% realistic failure rate")
    
    # Generate test data
    test_data = generate_corrected_test_data(50000)
    
    # Initialize tester
    tester = CorrectedLogicTester()
    
    print(f"\n🧪 EXECUTING {len(test_data):,} CORRECTED TESTS...")
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
        print("🚀 CORRECTED LOGIC AND MATH TEST")
        print("🎯 Testing with fixed logical and mathematical errors")
        print("⚖️  Realistic failure rates and proper improvement measurement")
        print()
        
        success = run_corrected_logic_and_math_test()
        
        print(f"\n📊 CONCLUSION:")
        if success:
            print("✅ CORRECTED TEST SHOWS REALISTIC IMPROVEMENT")
            print("🎯 Enhanced validation demonstrates meaningful improvement")
            print("🚀 RECOMMENDATION: System shows proper balance of improvement and quality")
        else:
            print("⚠️  SYSTEM NEEDS FURTHER OPTIMIZATION")
            print("🔧 Either insufficient improvement or unrealistic failure patterns")
            print("📊 Review validation logic and quality thresholds")
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n\n💥 Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)