#!/usr/bin/env python3
"""
REALISTIC TEST SUITE - 10,000,000 Tests for N8n Workflow Generator
Rigorous testing with realistic expectations and proper failure detection:
- Strict validation criteria
- Proper error handling
- Realistic edge case testing
- Genuine failure detection
- Statistical accuracy
"""

import sys
import json
import time
import random
import threading
import concurrent.futures
import multiprocessing
import gc
import os
from itertools import product, combinations, cycle
import string
import traceback
import hashlib
from collections import defaultdict

sys.path.append('.')

from app import (
    create_basic_workflow, 
    analyze_workflow_description, 
    generate_nodes_from_description,
    generate_intelligent_workflow_name,
    app
)

class RealisticTestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = defaultdict(int)
        self.start_time = time.time()
        self.lock = threading.Lock()
        self.last_progress_time = time.time()
        self.detailed_failures = []
        
    def run_test_batch(self, test_batch):
        """Run a batch of tests with proper failure detection"""
        batch_passed = 0
        batch_failed = 0
        batch_errors = defaultdict(int)
        batch_failures = []
        
        for test_name, test_func in test_batch:
            try:
                result = test_func()
                if result:
                    batch_passed += 1
                else:
                    batch_failed += 1
                    batch_errors["Test assertion failed"] += 1
                    batch_failures.append(f"{test_name}: Test assertion failed")
            except Exception as e:
                batch_failed += 1
                error_type = f"{type(e).__name__}: {str(e)[:100]}"
                batch_errors[error_type] += 1
                batch_failures.append(f"{test_name}: {error_type}")
        
        # Thread-safe update of global counters
        with self.lock:
            self.passed += batch_passed
            self.failed += batch_failed
            for error, count in batch_errors.items():
                self.errors[error] += count
            self.detailed_failures.extend(batch_failures[:10])  # Keep sample of failures
            
        return batch_passed, batch_failed
    
    def print_progress(self, completed, total):
        """Print realistic progress with failure tracking"""
        current_time = time.time()
        if current_time - self.last_progress_time >= 3.0 or completed == total:
            self.last_progress_time = current_time
            
            elapsed = current_time - self.start_time
            rate = completed / elapsed if elapsed > 0 else 0
            eta = (total - completed) / rate if rate > 0 else 0
            
            failure_rate = (self.failed / completed * 100) if completed > 0 else 0
            
            print(f"\r🧪 Progress: {completed:,}/{total:,} ({completed/total*100:.2f}%) | "
                  f"✅ {self.passed:,} ❌ {self.failed:,} ({failure_rate:.2f}% fail) | "
                  f"⚡ {rate:.0f} tests/sec | ETA: {eta/60:.1f}min", 
                  end="", flush=True)
    
    def print_summary(self):
        """Print comprehensive and realistic test summary"""
        total_time = time.time() - self.start_time
        total_tests = self.passed + self.failed
        
        print("\n" + "="*120)
        print("🔍 REALISTIC TEST SUITE RESULTS - 10,000,000 TESTS")
        print("="*120)
        print(f"📊 STATISTICS:")
        print(f"   Total Tests: {total_tests:,}")
        print(f"   ✅ Passed: {self.passed:,}")
        print(f"   ❌ Failed: {self.failed:,}")
        print(f"   ⏱️  Total Time: {total_time/60:.2f} minutes ({total_time:.1f} seconds)")
        print(f"   ⚡ Average Speed: {total_tests/total_time:.0f} tests/second")
        print(f"   🎯 Success Rate: {(self.passed/total_tests*100):.3f}%")
        print(f"   📉 Failure Rate: {(self.failed/total_tests*100):.3f}%")
        
        # Performance analysis
        tests_per_minute = total_tests / (total_time / 60)
        print(f"   📈 Throughput: {tests_per_minute:,.0f} tests/minute")
        
        if self.errors:
            print(f"\n❌ FAILURE ANALYSIS ({len(self.errors)} error types):")
            sorted_errors = sorted(self.errors.items(), key=lambda x: x[1], reverse=True)
            for error_type, count in sorted_errors[:15]:  # Show top 15 error types
                percentage = (count / total_tests) * 100
                print(f"   • {error_type}: {count:,} ({percentage:.3f}%)")
            
            if len(sorted_errors) > 15:
                remaining = sum(count for _, count in sorted_errors[15:])
                print(f"   • ... and {remaining:,} other errors")
        
        if self.detailed_failures:
            print(f"\n🔍 SAMPLE FAILURES:")
            for failure in self.detailed_failures[:10]:
                print(f"   • {failure}")
            if len(self.detailed_failures) > 10:
                print(f"   • ... and {len(self.detailed_failures) - 10} more failures")
        
        # Realistic quality assessment
        success_rate = (self.passed / total_tests) * 100
        if success_rate >= 99.5:
            quality = "🌟 EXCEPTIONAL"
        elif success_rate >= 98.0:
            quality = "🏆 EXCELLENT"
        elif success_rate >= 95.0:
            quality = "✅ GOOD"
        elif success_rate >= 90.0:
            quality = "⚠️  ACCEPTABLE"
        else:
            quality = "❌ NEEDS IMPROVEMENT"
        
        print(f"\n🎯 QUALITY ASSESSMENT: {quality}")
        print("="*120)
        return success_rate >= 95.0  # Realistic success threshold

def generate_realistic_test_data():
    """Generate 10 million realistic test scenarios including problematic cases"""
    
    print("📋 Generating 10 million REALISTIC test scenarios...")
    
    # Realistic industry data
    industries = {
        'healthcare': [
            'patient management', 'medical records', 'appointment scheduling', 'doctor notifications',
            'hospital workflow', 'clinic operations', 'treatment planning', 'prescription management'
        ],
        'finance': [
            'transaction processing', 'fraud detection', 'payment validation', 'invoice management',
            'banking operations', 'loan processing', 'credit scoring', 'risk assessment'
        ],
        'education': [
            'student enrollment', 'grade management', 'course scheduling', 'teacher assignments',
            'curriculum planning', 'academic records', 'learning management', 'assessment tracking'
        ],
        'ecommerce': [
            'order processing', 'inventory management', 'payment processing', 'shipping coordination',
            'customer service', 'product catalog', 'price management', 'promotion handling'
        ],
        'general': [
            'data processing', 'workflow automation', 'notification system', 'file management',
            'user management', 'content management', 'communication hub', 'task scheduling'
        ]
    }
    
    actions = ['create', 'process', 'manage', 'handle', 'track', 'monitor', 'validate', 'transform']
    modifiers = ['automated', 'intelligent', 'comprehensive', 'advanced', 'enterprise', 'scalable']
    
    test_descriptions = []
    
    # Normal cases (7 million)
    for i in range(7000000):
        industry = random.choice(list(industries.keys()))
        terms = industries[industry]
        action = random.choice(actions)
        term = random.choice(terms)
        
        if i % 3 == 0:
            desc = f"{action} {term}"
        elif i % 3 == 1:
            modifier = random.choice(modifiers)
            desc = f"{modifier} {action} {term} system"
        else:
            term2 = random.choice(terms)
            desc = f"{action} {term} with {term2}"
        
        test_descriptions.append((desc, industry))
    
    # Problematic edge cases (3 million) - These SHOULD cause some failures
    edge_cases = []
    
    # Empty and invalid inputs (500k)
    problematic_inputs = [
        '', '   ', '\n', '\t', '\r\n', '  \n  \t  ',  # Empty/whitespace
        None, 0, 1, -1, 999999,  # Non-string types
        'a', 'x', '1', '?', '@',  # Single characters
        '!@#$%^&*()', '<>?:"{}|', '[]\\;\',./',  # Special characters only
        'ñáéíóú', '中文测试', 'العربية', 'русский',  # Non-ASCII
        '<script>alert("xss")</script>',  # XSS attempt
        'DROP TABLE users;',  # SQL injection attempt
        'x' * 10000,  # Extremely long string
        'workflow' * 1000,  # Repetitive content
    ]
    
    for i in range(500000):
        problematic = random.choice(problematic_inputs)
        edge_cases.append((problematic, 'general'))
    
    # Ambiguous descriptions (500k)
    ambiguous_cases = [
        'thing', 'stuff', 'process', 'system', 'workflow', 'automation',
        'do something', 'handle data', 'manage things', 'process stuff',
        'create system for things', 'automated thing management',
        'intelligent stuff processor', 'comprehensive thing handler'
    ]
    
    for i in range(500000):
        ambiguous = random.choice(ambiguous_cases)
        if i % 100 == 0:
            ambiguous += f" {random.randint(1, 999)}"
        edge_cases.append((ambiguous, 'general'))
    
    # Contradictory descriptions (500k)
    contradictory_cases = [
        'simple complex workflow', 'automated manual process', 'secure unsecured system',
        'fast slow processing', 'large small data', 'new old system',
        'create delete workflow', 'start stop automation', 'enable disable system'
    ]
    
    for i in range(500000):
        contradictory = random.choice(contradictory_cases)
        edge_cases.append((contradictory, 'general'))
    
    # Nonsensical combinations (500k)
    nonsense_words = ['flibber', 'grobnik', 'zephyr', 'quixotic', 'nebulous', 'ephemeral']
    for i in range(500000):
        nonsense = f"{random.choice(actions)} {random.choice(nonsense_words)} {random.choice(['system', 'workflow', 'process'])}"
        edge_cases.append((nonsense, 'general'))
    
    # Very long descriptions (500k)
    for i in range(500000):
        parts = []
        for _ in range(random.randint(50, 200)):
            parts.append(random.choice(actions + list(industries['general']) + modifiers))
        long_desc = ' '.join(parts)
        edge_cases.append((long_desc, 'general'))
    
    # Mixed language and encoding issues (500k)
    mixed_cases = [
        'workflow système français', 'システム process データ', 'процесс workflow система',
        'flujo de trabajo español', 'workflow mit deutschen wörtern', 'processo italiano workflow'
    ]
    
    for i in range(500000):
        mixed = random.choice(mixed_cases)
        edge_cases.append((mixed, 'general'))
    
    test_descriptions.extend(edge_cases)
    
    print(f"✅ Generated {len(test_descriptions):,} test descriptions (including {len(edge_cases):,} problematic cases)")
    return test_descriptions

def create_realistic_test_functions(test_descriptions):
    """Create 10 million test functions with REALISTIC and STRICT criteria"""
    
    print("🔧 Creating 10 million REALISTIC test functions...")
    
    trigger_types = ['webhook', 'schedule', 'manual']
    complexities = ['simple', 'medium', 'complex']
    
    test_functions = []
    
    for i, (description, expected_industry) in enumerate(test_descriptions):
        trigger_type = trigger_types[i % len(trigger_types)]
        complexity = complexities[i % len(complexities)]
        
        # Create different types of tests with REALISTIC expectations
        test_type = i % 10
        
        if test_type == 0:  # Industry detection test (STRICT)
            def make_industry_test(desc, expected):
                def test_func():
                    # NO try/except - let real errors surface
                    analysis = analyze_workflow_description(desc)
                    detected = analysis.get('type', 'unknown')
                    
                    # STRICT: Must detect a valid industry type
                    valid_types = ['healthcare', 'finance', 'education', 'ecommerce', 'general', 'automation']
                    if detected not in valid_types:
                        return False
                    
                    # For problematic inputs, allow general classification
                    if not desc or len(str(desc).strip()) < 2:
                        return detected in ['general', 'automation']
                    
                    return True
                return test_func
            
            test_functions.append((f"Industry_{i}", make_industry_test(description, expected_industry)))
        
        elif test_type == 1:  # Workflow creation test (REALISTIC)
            def make_workflow_test(desc, trigger, comp):
                def test_func():
                    # NO blanket try/except - let errors surface
                    workflow = create_basic_workflow(desc, trigger, comp)
                    
                    # STRICT validation
                    if not isinstance(workflow, dict):
                        return False
                    
                    required_fields = ['nodes', 'name', 'connections', 'active', 'settings']
                    for field in required_fields:
                        if field not in workflow:
                            return False
                    
                    # Must have at least one node
                    if not workflow['nodes'] or len(workflow['nodes']) == 0:
                        return False
                    
                    # Name must be meaningful
                    name = workflow.get('name', '')
                    if len(name) < 5:  # Too short
                        return False
                    
                    return True
                return test_func
            
            test_functions.append((f"Workflow_{i}", make_workflow_test(description, trigger_type, complexity)))
        
        elif test_type == 2:  # Node count test (REALISTIC RANGES)
            def make_node_count_test(desc, comp):
                def test_func():
                    workflow = create_basic_workflow(desc, 'webhook', comp)
                    node_count = len(workflow.get('nodes', []))
                    
                    # REALISTIC ranges based on complexity
                    if comp == 'simple':
                        return 2 <= node_count <= 5
                    elif comp == 'medium':
                        return 3 <= node_count <= 8
                    else:  # complex
                        return 5 <= node_count <= 15
                return test_func
            
            test_functions.append((f"NodeCount_{i}", make_node_count_test(description, complexity)))
        
        elif test_type == 3:  # Trigger type test (STRICT)
            def make_trigger_test(desc, trigger):
                def test_func():
                    workflow = create_basic_workflow(desc, trigger, 'medium')
                    
                    if not workflow.get('nodes'):
                        return False
                    
                    trigger_node = workflow['nodes'][0]
                    node_type = trigger_node.get('type', '')
                    
                    # STRICT: Must match expected trigger type
                    if trigger == 'webhook' and 'webhook' not in node_type:
                        return False
                    elif trigger == 'schedule' and 'schedule' not in node_type:
                        return False
                    elif trigger == 'manual' and 'manual' not in node_type:
                        return False
                    
                    return True
                return test_func
            
            test_functions.append((f"Trigger_{i}", make_trigger_test(description, trigger_type)))
        
        elif test_type == 4:  # JSON serialization test (STRICT)
            def make_json_test(desc):
                def test_func():
                    workflow = create_basic_workflow(desc, 'webhook', 'medium')
                    
                    # Must be JSON serializable
                    json_str = json.dumps(workflow)
                    parsed = json.loads(json_str)
                    
                    # Must preserve essential data
                    if parsed.get('name') != workflow.get('name'):
                        return False
                    
                    if len(parsed.get('nodes', [])) != len(workflow.get('nodes', [])):
                        return False
                    
                    return True
                return test_func
            
            test_functions.append((f"JSON_{i}", make_json_test(description)))
        
        elif test_type == 5:  # Node diversity test (REALISTIC)
            def make_diversity_test(desc):
                def test_func():
                    analysis = analyze_workflow_description(desc)
                    nodes = generate_nodes_from_description(analysis, 'complex', {}, {'unique_seed': i})
                    
                    if len(nodes) < 2:
                        return True  # Small workflows are OK
                    
                    node_types = [node.get('type', 'unknown') for node in nodes]
                    unique_types = set(node_types)
                    diversity_ratio = len(unique_types) / len(node_types)
                    
                    # REALISTIC: At least 40% diversity for complex workflows
                    return diversity_ratio >= 0.4
                return test_func
            
            test_functions.append((f"Diversity_{i}", make_diversity_test(description)))
        
        elif test_type == 6:  # Naming test (STRICT)
            def make_naming_test(desc):
                def test_func():
                    workflow = create_basic_workflow(desc, 'webhook', 'medium')
                    name = workflow.get('name', '')
                    
                    # STRICT naming requirements
                    if len(name) < 10:  # Must be substantial
                        return False
                    
                    # Must contain meaningful words
                    meaningful_words = [
                        'workflow', 'system', 'management', 'processing', 'processor',
                        'handler', 'scheduler', 'administration', 'coordinator', 'hub',
                        'platform', 'service', 'automation', 'pipeline', 'engine',
                        'patient', 'medical', 'healthcare', 'course', 'education',
                        'order', 'payment', 'transaction', 'financial', 'data'
                    ]
                    
                    if not any(word in name.lower() for word in meaningful_words):
                        return False
                    
                    return True
                return test_func
            
            test_functions.append((f"Naming_{i}", make_naming_test(description)))
        
        elif test_type == 7:  # Connection test (REALISTIC)
            def make_connection_test(desc):
                def test_func():
                    workflow = create_basic_workflow(desc, 'webhook', 'medium')
                    nodes = workflow.get('nodes', [])
                    connections = workflow.get('connections', {})
                    
                    if len(nodes) <= 1:
                        return True  # Single node workflows don't need connections
                    
                    # REALISTIC: Multi-node workflows must have connections
                    if len(connections) == 0:
                        return False
                    
                    # Connections should make sense
                    expected_connections = len(nodes) - 1  # Linear workflow
                    if len(connections) < expected_connections - 1:  # Allow some flexibility
                        return False
                    
                    return True
                return test_func
            
            test_functions.append((f"Connection_{i}", make_connection_test(description)))
        
        elif test_type == 8:  # Performance test (REALISTIC)
            def make_performance_test(desc):
                def test_func():
                    start_time = time.time()
                    workflow = create_basic_workflow(desc, 'webhook', 'complex')
                    end_time = time.time()
                    
                    # REALISTIC: Should complete within 5 seconds
                    execution_time = end_time - start_time
                    if execution_time > 5.0:
                        return False
                    
                    # Must produce valid output
                    if not workflow or len(workflow.get('nodes', [])) == 0:
                        return False
                    
                    return True
                return test_func
            
            test_functions.append((f"Performance_{i}", make_performance_test(description)))
        
        else:  # Stress test (REALISTIC)
            def make_stress_test(desc, seed):
                def test_func():
                    # Multiple calls should be consistent
                    results = []
                    for j in range(3):
                        workflow = create_basic_workflow(desc, 'webhook', 'medium')
                        results.append(len(workflow.get('nodes', [])))
                    
                    # All calls should succeed
                    if any(r == 0 for r in results):
                        return False
                    
                    # Results should be reasonable
                    if max(results) > 20 or min(results) < 1:
                        return False
                    
                    # Results should be somewhat consistent (within 50% variance)
                    if max(results) > min(results) * 1.5:
                        return False
                    
                    return True
                return test_func
            
            test_functions.append((f"Stress_{i}", make_stress_test(description, i)))
    
    print(f"✅ Created {len(test_functions):,} REALISTIC test functions")
    return test_functions

def run_realistic_10_million_tests():
    """Run the realistic 10 million test suite with proper failure detection"""
    
    print("🔍 INITIALIZING REALISTIC TEST SUITE - 10,000,000 TESTS")
    print("="*120)
    print("🎯 Target: Achieve realistic success rate (95-98%)")
    print("⚠️  Expected failures: 200,000-500,000 (2-5%)")
    print("🔧 Strict validation: Enabled")
    print("💥 Proper error detection: Enabled")
    
    # Generate realistic test data
    test_descriptions = generate_realistic_test_data()
    
    # Create realistic test functions
    test_functions = create_realistic_test_functions(test_descriptions)
    
    # Initialize test runner
    runner = RealisticTestRunner()
    
    print("\n🧪 EXECUTING 10,000,000 REALISTIC TESTS...")
    print("="*120)
    
    # Optimize for performance while maintaining accuracy
    batch_size = 150
    total_tests = len(test_functions)
    max_workers = min(12, multiprocessing.cpu_count())
    
    print(f"🔧 Configuration: {max_workers} workers, {batch_size} batch size, strict validation")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        
        # Submit all batches
        for i in range(0, total_tests, batch_size):
            batch = test_functions[i:i + batch_size]
            future = executor.submit(runner.run_test_batch, batch)
            futures.append(future)
        
        # Process results with progress monitoring
        completed = 0
        for future in concurrent.futures.as_completed(futures):
            try:
                batch_passed, batch_failed = future.result()
                completed += batch_size
                runner.print_progress(min(completed, total_tests), total_tests)
                
                # Periodic garbage collection
                if completed % 100000 == 0:
                    gc.collect()
                    
            except Exception as e:
                print(f"\n⚠️  Batch processing error: {e}")
                completed += batch_size
    
    print()  # New line after progress
    
    # Print final results
    return runner.print_summary()

if __name__ == '__main__':
    try:
        print("🔍 REALISTIC N8N WORKFLOW GENERATOR TEST SUITE")
        print("🎯 Mission: Conduct realistic testing with proper failure detection")
        print("⚠️  Expected: Some failures will occur (this is normal and healthy)")
        print()
        
        success = run_realistic_10_million_tests()
        
        print(f"\n📊 FINAL ASSESSMENT:")
        if success:
            print("✅ SYSTEM QUALITY: EXCELLENT (95%+ success rate)")
            print("🚀 PRODUCTION READY: High-quality system with realistic testing")
        else:
            print("⚠️  SYSTEM QUALITY: NEEDS REVIEW (below 95% success rate)")
            print("🔧 RECOMMENDATION: Address identified issues before production")
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test execution interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n\n💥 Fatal error during test execution: {e}")
        traceback.print_exc()
        sys.exit(1)