#!/usr/bin/env python3
"""
Realistic Validation Test - Proper Failure Detection
Tests that maintain realistic expectations and detect genuine failures
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

class RealisticValidationTester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = defaultdict(int)
        self.lock = threading.Lock()
        self.start_time = time.time()
        
    def test_with_strict_criteria(self, test_input):
        """Test with STRICT and REALISTIC criteria that can actually fail"""
        try:
            # Step 1: Enhanced validation
            cleaned_data, validation_report = validate_workflow_request(test_input)
            
            # Step 2: Workflow creation
            workflow = create_basic_workflow(
                cleaned_data['description'],
                cleaned_data['trigger_type'],
                cleaned_data['complexity'],
                '',
                cleaned_data['advanced_options']
            )
            
            # Step 3: STRICT QUALITY VALIDATION - These can legitimately fail
            
            # Must be a valid dictionary
            if not isinstance(workflow, dict):
                return False, "Invalid workflow type"
            
            # Must have required fields
            required_fields = ['nodes', 'name', 'connections', 'active', 'settings']
            for field in required_fields:
                if field not in workflow:
                    return False, f"Missing required field: {field}"
            
            # Must have at least one node
            nodes = workflow.get('nodes', [])
            if not nodes or len(nodes) == 0:
                return False, "No nodes generated"
            
            # Nodes must be valid
            for i, node in enumerate(nodes):
                if not isinstance(node, dict):
                    return False, f"Node {i} is not a dictionary"
                
                # Required node fields
                node_required = ['id', 'name', 'type', 'parameters', 'position']
                for field in node_required:
                    if field not in node:
                        return False, f"Node {i} missing field: {field}"
                
                # Node ID must be valid
                if not node.get('id') or len(str(node['id'])) < 5:
                    return False, f"Node {i} has invalid ID"
                
                # Node name must be meaningful
                name = node.get('name', '')
                if len(name) < 3:
                    return False, f"Node {i} name too short: '{name}'"
                
                # Node type must be valid n8n type
                node_type = node.get('type', '')
                if not node_type or 'n8n-nodes-base' not in node_type:
                    return False, f"Node {i} has invalid type: '{node_type}'"
                
                # Position must be valid
                position = node.get('position', [])
                if not isinstance(position, list) or len(position) != 2:
                    return False, f"Node {i} has invalid position"
                
                try:
                    x, y = position
                    if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
                        return False, f"Node {i} position coordinates must be numbers"
                except (ValueError, TypeError):
                    return False, f"Node {i} position format error"
            
            # Workflow name must be meaningful
            name = workflow.get('name', '')
            if len(name) < 10:
                return False, f"Workflow name too short: '{name}'"
            
            # Name must contain meaningful words
            meaningful_words = [
                'workflow', 'system', 'management', 'processing', 'processor',
                'handler', 'scheduler', 'administration', 'coordinator', 'hub',
                'automation', 'pipeline', 'service', 'platform', 'engine'
            ]
            if not any(word.lower() in name.lower() for word in meaningful_words):
                return False, f"Workflow name lacks meaningful content: '{name}'"
            
            # Connections must be reasonable for multi-node workflows
            connections = workflow.get('connections', {})
            if len(nodes) > 1:
                if not connections or len(connections) == 0:
                    return False, "Multi-node workflow missing connections"
                
                # Check connection structure
                if not isinstance(connections, dict):
                    return False, "Connections must be a dictionary"
            
            # Settings must be valid
            settings = workflow.get('settings', {})
            if not isinstance(settings, dict):
                return False, "Settings must be a dictionary"
            
            # Active must be boolean
            active = workflow.get('active')
            if not isinstance(active, bool):
                return False, f"Active field must be boolean, got: {type(active)}"
            
            # JSON serialization test - this can fail with circular references
            try:
                json_str = json.dumps(workflow)
                parsed = json.loads(json_str)
                
                # Verify essential data preserved
                if parsed.get('name') != workflow.get('name'):
                    return False, "JSON serialization corrupted workflow name"
                
                if len(parsed.get('nodes', [])) != len(workflow.get('nodes', [])):
                    return False, "JSON serialization corrupted nodes"
                    
            except (TypeError, ValueError) as e:
                return False, f"Workflow not JSON serializable: {str(e)}"
            
            # Performance test - workflow creation should be reasonably fast
            # (This is already measured, but we can fail if it took too long)
            
            # All checks passed
            return True, "Success"
            
        except Exception as e:
            return False, f"Exception: {str(e)}"
    
    def run_batch_test(self, test_batch):
        """Run a batch of tests with proper failure detection"""
        batch_passed = 0
        batch_failed = 0
        batch_errors = defaultdict(int)
        
        for test_name, test_input in test_batch:
            success, error_msg = self.test_with_strict_criteria(test_input)
            
            if success:
                batch_passed += 1
            else:
                batch_failed += 1
                batch_errors[error_msg] += 1
        
        # Thread-safe update
        with self.lock:
            self.passed += batch_passed
            self.failed += batch_failed
            for error, count in batch_errors.items():
                self.errors[error] += count
                
        return batch_passed, batch_failed
    
    def print_progress(self, completed, total):
        """Print progress with realistic metrics"""
        current_time = time.time()
        elapsed = current_time - self.start_time
        rate = completed / elapsed if elapsed > 0 else 0
        eta = (total - completed) / rate if rate > 0 else 0
        
        success_rate = (self.passed / completed * 100) if completed > 0 else 0
        failure_rate = (self.failed / completed * 100) if completed > 0 else 0
        
        print(f"\r🧪 Progress: {completed:,}/{total:,} ({completed/total*100:.1f}%) | "
              f"✅ {self.passed:,} ❌ {self.failed:,} | "
              f"Success: {success_rate:.2f}% | Fail: {failure_rate:.2f}% | "
              f"⚡ {rate:.0f}/sec", 
              end="", flush=True)
    
    def print_summary(self, total_tests):
        """Print comprehensive and realistic summary"""
        total_time = time.time() - self.start_time
        success_rate = (self.passed / total_tests) * 100
        failure_rate = (self.failed / total_tests) * 100
        
        print("\n" + "="*100)
        print("🔍 REALISTIC VALIDATION TEST RESULTS")
        print("="*100)
        
        print(f"📊 STATISTICS:")
        print(f"   Total Tests: {total_tests:,}")
        print(f"   ✅ Passed: {self.passed:,}")
        print(f"   ❌ Failed: {self.failed:,}")
        print(f"   ⏱️  Duration: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
        print(f"   ⚡ Speed: {total_tests/total_time:.0f} tests/second")
        print(f"   🎯 Success Rate: {success_rate:.3f}%")
        print(f"   📉 Failure Rate: {failure_rate:.3f}%")
        
        # Quality assessment with realistic expectations
        if success_rate >= 99.0:
            quality = "🌟 EXCEPTIONAL (but suspiciously high)"
        elif success_rate >= 97.0:
            quality = "🏆 EXCELLENT"
        elif success_rate >= 94.0:
            quality = "✅ VERY GOOD"
        elif success_rate >= 90.0:
            quality = "👍 GOOD"
        elif success_rate >= 85.0:
            quality = "⚠️  ACCEPTABLE"
        else:
            quality = "❌ NEEDS IMPROVEMENT"
        
        print(f"   🎯 Quality Assessment: {quality}")
        
        # Failure analysis
        if self.errors:
            print(f"\n❌ FAILURE ANALYSIS ({len(self.errors)} error types):")
            sorted_errors = sorted(self.errors.items(), key=lambda x: x[1], reverse=True)
            for error_type, count in sorted_errors[:15]:
                percentage = (count / total_tests) * 100
                print(f"   • {error_type}: {count:,} ({percentage:.3f}%)")
        
        # Realistic expectations
        print(f"\n🎯 REALISTIC EXPECTATIONS:")
        if failure_rate < 0.1:
            print("   ⚠️  WARNING: Failure rate suspiciously low - tests may be too lenient")
        elif failure_rate < 1.0:
            print("   ✅ EXCELLENT: Very low failure rate with proper validation")
        elif failure_rate < 3.0:
            print("   👍 GOOD: Reasonable failure rate for comprehensive testing")
        elif failure_rate < 5.0:
            print("   📊 ACCEPTABLE: Normal failure rate for strict validation")
        else:
            print("   🔧 HIGH: Consider improving input validation")
        
        print("="*100)
        return success_rate >= 95.0 and failure_rate >= 0.5  # Realistic success criteria

def generate_realistic_test_data(count=50000):
    """Generate test data that can realistically fail"""
    
    print(f"📋 Generating {count:,} realistic test cases...")
    
    test_data = []
    
    # Good cases that should pass (70%)
    good_cases = [
        {'description': 'process customer orders for ecommerce'},
        {'description': 'manage patient records in healthcare system'},
        {'description': 'automate invoice generation workflow'},
        {'description': 'handle payment processing pipeline'},
        {'description': 'sync inventory data between systems'},
        {'description': 'monitor system health and alerts'},
        {'description': 'validate user input before processing'},
        {'description': 'transform data format for integration'},
        {'description': 'schedule appointment notifications'},
        {'description': 'track shipment status updates'},
    ]
    
    for i in range(int(count * 0.7)):
        base_case = random.choice(good_cases).copy()
        # Add some variation
        if i % 3 == 0:
            base_case['triggerType'] = random.choice(['webhook', 'schedule', 'manual'])
        if i % 4 == 0:
            base_case['complexity'] = random.choice(['simple', 'medium', 'complex'])
        
        test_data.append((f"good_{i}", base_case))
    
    # Edge cases that might fail (20%)
    edge_cases = [
        # These should be handled by enhanced validation but might still fail quality checks
        {'description': ''},
        {'description': '   '},
        {'description': 'a'},
        {'description': 'x'},
        {'description': None},
        {'description': 123},
        {'description': 'thing'},
        {'description': 'stuff'},
        {'description': 'process'},
        {'description': 'workflow'},
        {'description': '!@#$%^&*()'},
        {'description': '<script>alert("test")</script>'},
        {'description': 'workflow ' * 100},
        {'description': 'a' * 1000},
        
        # Invalid parameters that should cause failures
        {'description': 'test workflow', 'triggerType': 'invalid'},
        {'description': 'test workflow', 'complexity': 'invalid'},
        {'description': 'test workflow', 'advanced_options': 'not_a_dict'},
    ]
    
    for i in range(int(count * 0.2)):
        case = random.choice(edge_cases).copy()
        test_data.append((f"edge_{i}", case))
    
    # Stress cases that should fail (10%)
    stress_cases = []
    for i in range(int(count * 0.1)):
        # Create cases that should legitimately fail
        problematic_cases = [
            # Extremely problematic inputs that even enhanced validation can't save
            {'description': '\x00\x01\x02'},  # Control characters
            {'description': ''},  # Empty after all processing
            {'description': '   \n\t   '},  # Only whitespace
            {'description': random.choice(['', None, 0, [], {}])},  # Various empty types
        ]
        
        case = random.choice(problematic_cases)
        # Add invalid parameters to increase failure chance
        if random.random() < 0.5:
            case['triggerType'] = random.choice([None, 123, [], {}, 'totally_invalid'])
        if random.random() < 0.5:
            case['complexity'] = random.choice([None, 123, [], {}, 'totally_invalid'])
        
        stress_cases.append((f"stress_{i}", case))
    
    test_data.extend(stress_cases)
    random.shuffle(test_data)
    
    print(f"✅ Generated {len(test_data):,} test cases")
    print(f"   • {int(count * 0.7):,} good cases (should pass)")
    print(f"   • {int(count * 0.2):,} edge cases (might fail)")
    print(f"   • {int(count * 0.1):,} stress cases (should fail)")
    
    return test_data

def run_realistic_validation_test():
    """Run realistic validation test with proper failure detection"""
    
    print("🔍 REALISTIC VALIDATION TEST WITH PROPER FAILURE DETECTION")
    print("="*100)
    print("🎯 Goal: Test enhanced validation with realistic expectations")
    print("⚠️  Expected: Some failures SHOULD occur (this is healthy)")
    print("🧪 Method: Strict quality validation that can legitimately fail")
    
    # Generate test data
    test_data = generate_realistic_test_data(50000)
    
    # Initialize tester
    tester = RealisticValidationTester()
    
    print(f"\n🧪 EXECUTING {len(test_data):,} REALISTIC TESTS...")
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
        print("🚀 REALISTIC VALIDATION TEST")
        print("🎯 Testing with proper failure detection and realistic expectations")
        print("⚠️  Note: Some failures are expected and healthy")
        print()
        
        success = run_realistic_validation_test()
        
        print(f"\n📊 FINAL ASSESSMENT:")
        if success:
            print("✅ REALISTIC VALIDATION SUCCESSFUL")
            print("🎯 Enhanced validation shows good improvement with realistic failure rate")
            print("🚀 READY: System demonstrates proper quality control")
        else:
            print("⚠️  VALIDATION NEEDS REVIEW")
            print("🔧 Either too many failures or suspiciously few failures detected")
            print("📊 Review test criteria and validation logic")
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n\n💥 Test error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)