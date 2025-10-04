#!/usr/bin/env python3
"""
Comprehensive Test Suite - 100 Tests for N8n Workflow Generator
Tests all aspects: logic, math, edge cases, industry detection, complexity, naming, etc.
"""

import sys
import json
import time
import traceback
sys.path.append('.')

from app import (
    create_basic_workflow, 
    analyze_workflow_description, 
    generate_nodes_from_description,
    generate_intelligent_workflow_name,
    app
)

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.start_time = time.time()
    
    def run_test(self, test_name, test_func):
        """Run a single test and track results"""
        try:
            result = test_func()
            if result:
                print(f"✅ {test_name}")
                self.passed += 1
            else:
                print(f"❌ {test_name}")
                self.failed += 1
                self.errors.append(f"{test_name}: Test failed")
        except Exception as e:
            print(f"💥 {test_name}: {str(e)}")
            self.failed += 1
            self.errors.append(f"{test_name}: {str(e)}")
    
    def print_summary(self):
        """Print test summary"""
        total_time = time.time() - self.start_time
        total_tests = self.passed + self.failed
        
        print("\n" + "="*80)
        print("🧪 COMPREHENSIVE TEST RESULTS")
        print("="*80)
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"⏱️  Time: {total_time:.2f}s")
        print(f"📊 Success Rate: {(self.passed/total_tests*100):.1f}%")
        
        if self.errors:
            print(f"\n❌ FAILED TESTS ({len(self.errors)}):")
            for error in self.errors[:10]:  # Show first 10 errors
                print(f"  • {error}")
            if len(self.errors) > 10:
                print(f"  ... and {len(self.errors) - 10} more")
        
        print("="*80)
        return self.failed == 0

def run_100_tests():
    """Run all 100 comprehensive tests"""
    runner = TestRunner()
    
    print("🚀 STARTING 100 COMPREHENSIVE TESTS")
    print("="*80)
    
    # CATEGORY 1: INDUSTRY DETECTION TESTS (20 tests)
    print("\n📋 CATEGORY 1: INDUSTRY DETECTION (20 tests)")
    
    def test_healthcare_detection_1():
        analysis = analyze_workflow_description("Patient appointment scheduling system")
        return analysis['type'] == 'healthcare'
    
    def test_healthcare_detection_2():
        analysis = analyze_workflow_description("Medical record management with doctor notifications")
        return analysis['type'] == 'healthcare'
    
    def test_healthcare_detection_3():
        analysis = analyze_workflow_description("Hospital patient intake and treatment workflow")
        return analysis['type'] == 'healthcare'
    
    def test_healthcare_detection_4():
        analysis = analyze_workflow_description("Clinic appointment booking and reminder system")
        return analysis['type'] == 'healthcare'
    
    def test_healthcare_detection_5():
        analysis = analyze_workflow_description("Healthcare compliance reporting and audit logging")
        return analysis['type'] == 'healthcare'
    
    def test_finance_detection_1():
        analysis = analyze_workflow_description("Banking transaction processing system")
        return analysis['type'] == 'finance'
    
    def test_finance_detection_2():
        analysis = analyze_workflow_description("Financial fraud detection and prevention")
        return analysis['type'] == 'finance'
    
    def test_finance_detection_3():
        analysis = analyze_workflow_description("Invoice processing and payment automation")
        return analysis['type'] == 'finance'
    
    def test_finance_detection_4():
        analysis = analyze_workflow_description("Investment portfolio management and reporting")
        return analysis['type'] == 'finance'
    
    def test_finance_detection_5():
        analysis = analyze_workflow_description("Credit scoring and loan approval workflow")
        return analysis['type'] == 'finance'
    
    def test_education_detection_1():
        analysis = analyze_workflow_description("Student enrollment and registration system")
        return analysis['type'] == 'education'
    
    def test_education_detection_2():
        analysis = analyze_workflow_description("Course management and grade tracking")
        return analysis['type'] == 'education'
    
    def test_education_detection_3():
        analysis = analyze_workflow_description("University academic record management")
        return analysis['type'] == 'education'
    
    def test_education_detection_4():
        analysis = analyze_workflow_description("Teacher assignment and curriculum planning")
        return analysis['type'] == 'education'
    
    def test_education_detection_5():
        analysis = analyze_workflow_description("Learning management system integration")
        return analysis['type'] == 'education'
    
    def test_ecommerce_detection_1():
        analysis = analyze_workflow_description("Order processing and inventory management")
        return analysis['type'] == 'ecommerce'
    
    def test_ecommerce_detection_2():
        analysis = analyze_workflow_description("Product catalog and shopping cart system")
        return analysis['type'] == 'ecommerce'
    
    def test_ecommerce_detection_3():
        analysis = analyze_workflow_description("Customer purchase and shipping coordination")
        return analysis['type'] == 'ecommerce'
    
    def test_ecommerce_detection_4():
        analysis = analyze_workflow_description("Retail store inventory and payment processing")
        return analysis['type'] == 'ecommerce'
    
    def test_general_detection():
        analysis = analyze_workflow_description("Generic data processing workflow")
        return analysis['type'] == 'general'
    
    # Run industry detection tests
    industry_tests = [
        ("Healthcare Detection 1", test_healthcare_detection_1),
        ("Healthcare Detection 2", test_healthcare_detection_2),
        ("Healthcare Detection 3", test_healthcare_detection_3),
        ("Healthcare Detection 4", test_healthcare_detection_4),
        ("Healthcare Detection 5", test_healthcare_detection_5),
        ("Finance Detection 1", test_finance_detection_1),
        ("Finance Detection 2", test_finance_detection_2),
        ("Finance Detection 3", test_finance_detection_3),
        ("Finance Detection 4", test_finance_detection_4),
        ("Finance Detection 5", test_finance_detection_5),
        ("Education Detection 1", test_education_detection_1),
        ("Education Detection 2", test_education_detection_2),
        ("Education Detection 3", test_education_detection_3),
        ("Education Detection 4", test_education_detection_4),
        ("Education Detection 5", test_education_detection_5),
        ("Ecommerce Detection 1", test_ecommerce_detection_1),
        ("Ecommerce Detection 2", test_ecommerce_detection_2),
        ("Ecommerce Detection 3", test_ecommerce_detection_3),
        ("Ecommerce Detection 4", test_ecommerce_detection_4),
        ("General Detection", test_general_detection),
    ]
    
    for name, test_func in industry_tests:
        runner.run_test(name, test_func)
    
    # CATEGORY 2: COMPLEXITY SCALING TESTS (20 tests)
    print("\n⚙️ CATEGORY 2: COMPLEXITY SCALING (20 tests)")
    
    def test_simple_complexity_1():
        workflow = create_basic_workflow("Send email", "manual", "simple")
        return 2 <= len(workflow['nodes']) <= 4
    
    def test_simple_complexity_2():
        workflow = create_basic_workflow("Basic notification", "webhook", "simple")
        return 2 <= len(workflow['nodes']) <= 4
    
    def test_simple_complexity_3():
        workflow = create_basic_workflow("Store data", "manual", "simple")
        return 2 <= len(workflow['nodes']) <= 4
    
    def test_simple_complexity_4():
        workflow = create_basic_workflow("Process input", "webhook", "simple")
        return 2 <= len(workflow['nodes']) <= 4
    
    def test_simple_complexity_5():
        workflow = create_basic_workflow("Send message", "manual", "simple")
        return 2 <= len(workflow['nodes']) <= 4
    
    def test_medium_complexity_1():
        workflow = create_basic_workflow("Customer data processing with validation", "webhook", "medium")
        return 4 <= len(workflow['nodes']) <= 8
    
    def test_medium_complexity_2():
        workflow = create_basic_workflow("Order processing with notifications", "webhook", "medium")
        return 4 <= len(workflow['nodes']) <= 8
    
    def test_medium_complexity_3():
        workflow = create_basic_workflow("Lead management with CRM integration", "webhook", "medium")
        return 4 <= len(workflow['nodes']) <= 8
    
    def test_medium_complexity_4():
        workflow = create_basic_workflow("Data sync between systems", "schedule", "medium")
        return 4 <= len(workflow['nodes']) <= 8
    
    def test_medium_complexity_5():
        workflow = create_basic_workflow("User onboarding with email sequences", "webhook", "medium")
        return 4 <= len(workflow['nodes']) <= 8
    
    def test_complex_complexity_1():
        workflow = create_basic_workflow("Enterprise order processing with fraud detection, inventory management, and compliance reporting", "webhook", "complex")
        return 8 <= len(workflow['nodes']) <= 15
    
    def test_complex_complexity_2():
        workflow = create_basic_workflow("Healthcare patient management with appointment scheduling, medical records, and doctor notifications", "webhook", "complex")
        return 8 <= len(workflow['nodes']) <= 15
    
    def test_complex_complexity_3():
        workflow = create_basic_workflow("Financial transaction processing with fraud detection, compliance monitoring, and audit logging", "schedule", "complex")
        return 8 <= len(workflow['nodes']) <= 15
    
    def test_complex_complexity_4():
        workflow = create_basic_workflow("Multi-channel marketing automation with lead scoring, segmentation, and personalized campaigns", "webhook", "complex")
        return 8 <= len(workflow['nodes']) <= 15
    
    def test_complex_complexity_5():
        workflow = create_basic_workflow("Supply chain management with inventory tracking, supplier coordination, and quality control", "schedule", "complex")
        return 8 <= len(workflow['nodes']) <= 15
    
    def test_complexity_scaling_consistency_1():
        simple = create_basic_workflow("Test workflow", "webhook", "simple")
        medium = create_basic_workflow("Test workflow", "webhook", "medium")
        return len(simple['nodes']) < len(medium['nodes'])
    
    def test_complexity_scaling_consistency_2():
        medium = create_basic_workflow("Test workflow", "webhook", "medium")
        complex_wf = create_basic_workflow("Test workflow", "webhook", "complex")
        return len(medium['nodes']) < len(complex_wf['nodes'])
    
    def test_complexity_scaling_consistency_3():
        simple = create_basic_workflow("Test workflow", "webhook", "simple")
        complex_wf = create_basic_workflow("Test workflow", "webhook", "complex")
        return len(simple['nodes']) < len(complex_wf['nodes'])
    
    def test_complexity_bounds_simple():
        workflow = create_basic_workflow("Test", "webhook", "simple")
        return len(workflow['nodes']) <= 4
    
    def test_complexity_bounds_complex():
        workflow = create_basic_workflow("Very complex enterprise system with multiple integrations", "webhook", "complex")
        return len(workflow['nodes']) <= 15
    
    # Run complexity tests
    complexity_tests = [
        ("Simple Complexity 1", test_simple_complexity_1),
        ("Simple Complexity 2", test_simple_complexity_2),
        ("Simple Complexity 3", test_simple_complexity_3),
        ("Simple Complexity 4", test_simple_complexity_4),
        ("Simple Complexity 5", test_simple_complexity_5),
        ("Medium Complexity 1", test_medium_complexity_1),
        ("Medium Complexity 2", test_medium_complexity_2),
        ("Medium Complexity 3", test_medium_complexity_3),
        ("Medium Complexity 4", test_medium_complexity_4),
        ("Medium Complexity 5", test_medium_complexity_5),
        ("Complex Complexity 1", test_complex_complexity_1),
        ("Complex Complexity 2", test_complex_complexity_2),
        ("Complex Complexity 3", test_complex_complexity_3),
        ("Complex Complexity 4", test_complex_complexity_4),
        ("Complex Complexity 5", test_complex_complexity_5),
        ("Complexity Scaling 1", test_complexity_scaling_consistency_1),
        ("Complexity Scaling 2", test_complexity_scaling_consistency_2),
        ("Complexity Scaling 3", test_complexity_scaling_consistency_3),
        ("Complexity Bounds Simple", test_complexity_bounds_simple),
        ("Complexity Bounds Complex", test_complexity_bounds_complex),
    ]
    
    for name, test_func in complexity_tests:
        runner.run_test(name, test_func)
    
    # CATEGORY 3: TRIGGER TYPE TESTS (15 tests)
    print("\n🔗 CATEGORY 3: TRIGGER TYPES (15 tests)")
    
    def test_webhook_trigger_1():
        workflow = create_basic_workflow("Test webhook", "webhook", "medium")
        trigger_node = workflow['nodes'][0] if workflow['nodes'] else None
        return trigger_node and trigger_node['type'] == 'n8n-nodes-base.webhook'
    
    def test_webhook_trigger_2():
        workflow = create_basic_workflow("API endpoint", "webhook", "simple")
        trigger_node = workflow['nodes'][0] if workflow['nodes'] else None
        return trigger_node and 'webhook' in trigger_node['type']
    
    def test_webhook_trigger_3():
        workflow = create_basic_workflow("HTTP receiver", "webhook", "complex")
        trigger_node = workflow['nodes'][0] if workflow['nodes'] else None
        return trigger_node and trigger_node['type'] == 'n8n-nodes-base.webhook'
    
    def test_schedule_trigger_1():
        workflow = create_basic_workflow("Scheduled task", "schedule", "medium")
        trigger_node = workflow['nodes'][0] if workflow['nodes'] else None
        return trigger_node and trigger_node['type'] == 'n8n-nodes-base.scheduleTrigger'
    
    def test_schedule_trigger_2():
        workflow = create_basic_workflow("Periodic job", "schedule", "simple")
        trigger_node = workflow['nodes'][0] if workflow['nodes'] else None
        return trigger_node and 'schedule' in trigger_node['type']
    
    def test_schedule_trigger_3():
        workflow = create_basic_workflow("Automated process", "schedule", "complex")
        trigger_node = workflow['nodes'][0] if workflow['nodes'] else None
        return trigger_node and trigger_node['type'] == 'n8n-nodes-base.scheduleTrigger'
    
    def test_manual_trigger_1():
        workflow = create_basic_workflow("Manual process", "manual", "medium")
        trigger_node = workflow['nodes'][0] if workflow['nodes'] else None
        return trigger_node and trigger_node['type'] == 'n8n-nodes-base.manualTrigger'
    
    def test_manual_trigger_2():
        workflow = create_basic_workflow("User initiated", "manual", "simple")
        trigger_node = workflow['nodes'][0] if workflow['nodes'] else None
        return trigger_node and 'manual' in trigger_node['type']
    
    def test_manual_trigger_3():
        workflow = create_basic_workflow("On-demand task", "manual", "complex")
        trigger_node = workflow['nodes'][0] if workflow['nodes'] else None
        return trigger_node and trigger_node['type'] == 'n8n-nodes-base.manualTrigger'
    
    def test_webhook_response_node():
        workflow = create_basic_workflow("Webhook with response", "webhook", "medium")
        has_response = any('respond' in node.get('name', '').lower() for node in workflow['nodes'])
        return has_response
    
    def test_trigger_parameters_webhook():
        workflow = create_basic_workflow("Test", "webhook", "simple")
        trigger_node = workflow['nodes'][0] if workflow['nodes'] else None
        return trigger_node and 'parameters' in trigger_node
    
    def test_trigger_parameters_schedule():
        workflow = create_basic_workflow("Test", "schedule", "simple")
        trigger_node = workflow['nodes'][0] if workflow['nodes'] else None
        return trigger_node and 'parameters' in trigger_node
    
    def test_trigger_parameters_manual():
        workflow = create_basic_workflow("Test", "manual", "simple")
        trigger_node = workflow['nodes'][0] if workflow['nodes'] else None
        return trigger_node and 'parameters' in trigger_node
    
    def test_trigger_positioning():
        workflow = create_basic_workflow("Test", "webhook", "medium")
        trigger_node = workflow['nodes'][0] if workflow['nodes'] else None
        return trigger_node and trigger_node['position'] == [0, 300]
    
    def test_trigger_unique_ids():
        workflow1 = create_basic_workflow("Test 1", "webhook", "simple")
        workflow2 = create_basic_workflow("Test 2", "webhook", "simple")
        id1 = workflow1['nodes'][0]['id'] if workflow1['nodes'] else None
        id2 = workflow2['nodes'][0]['id'] if workflow2['nodes'] else None
        return id1 and id2 and id1 != id2
    
    # Run trigger tests
    trigger_tests = [
        ("Webhook Trigger 1", test_webhook_trigger_1),
        ("Webhook Trigger 2", test_webhook_trigger_2),
        ("Webhook Trigger 3", test_webhook_trigger_3),
        ("Schedule Trigger 1", test_schedule_trigger_1),
        ("Schedule Trigger 2", test_schedule_trigger_2),
        ("Schedule Trigger 3", test_schedule_trigger_3),
        ("Manual Trigger 1", test_manual_trigger_1),
        ("Manual Trigger 2", test_manual_trigger_2),
        ("Manual Trigger 3", test_manual_trigger_3),
        ("Webhook Response Node", test_webhook_response_node),
        ("Trigger Parameters Webhook", test_trigger_parameters_webhook),
        ("Trigger Parameters Schedule", test_trigger_parameters_schedule),
        ("Trigger Parameters Manual", test_trigger_parameters_manual),
        ("Trigger Positioning", test_trigger_positioning),
        ("Trigger Unique IDs", test_trigger_unique_ids),
    ]
    
    for name, test_func in trigger_tests:
        runner.run_test(name, test_func)
    
    # CATEGORY 4: INTELLIGENT NAMING TESTS (15 tests)
    print("\n🏷️ CATEGORY 4: INTELLIGENT NAMING (15 tests)")
    
    def test_healthcare_naming_1():
        workflow = create_basic_workflow("Patient management system", "webhook", "medium")
        return "Patient" in workflow['name'] or "Healthcare" in workflow['name']
    
    def test_healthcare_naming_2():
        workflow = create_basic_workflow("Medical record processing", "webhook", "medium")
        return "Medical" in workflow['name'] or "Healthcare" in workflow['name']
    
    def test_healthcare_naming_3():
        workflow = create_basic_workflow("Doctor appointment scheduling", "webhook", "medium")
        return "Appointment" in workflow['name'] or "Healthcare" in workflow['name']
    
    def test_finance_naming_1():
        workflow = create_basic_workflow("Payment processing system", "webhook", "medium")
        return "Payment" in workflow['name'] or "Financial" in workflow['name']
    
    def test_finance_naming_2():
        workflow = create_basic_workflow("Transaction monitoring", "webhook", "medium")
        return "Transaction" in workflow['name'] or "Financial" in workflow['name']
    
    def test_finance_naming_3():
        workflow = create_basic_workflow("Invoice management", "webhook", "medium")
        return "Invoice" in workflow['name'] or "Financial" in workflow['name']
    
    def test_education_naming_1():
        workflow = create_basic_workflow("Student enrollment system", "webhook", "medium")
        return "Student" in workflow['name'] or "Educational" in workflow['name']
    
    def test_education_naming_2():
        workflow = create_basic_workflow("Course management", "webhook", "medium")
        return "Course" in workflow['name'] or "Educational" in workflow['name']
    
    def test_education_naming_3():
        workflow = create_basic_workflow("Grade processing", "webhook", "medium")
        return "Grading" in workflow['name'] or "Educational" in workflow['name']
    
    def test_ecommerce_naming_1():
        workflow = create_basic_workflow("Order processing system", "webhook", "medium")
        return "Order" in workflow['name'] or "E-commerce" in workflow['name']
    
    def test_ecommerce_naming_2():
        workflow = create_basic_workflow("Inventory management", "webhook", "medium")
        return "Inventory" in workflow['name'] or "E-commerce" in workflow['name']
    
    def test_ecommerce_naming_3():
        workflow = create_basic_workflow("Customer service", "webhook", "medium")
        return "Customer" in workflow['name'] or "E-commerce" in workflow['name']
    
    def test_action_based_naming_1():
        workflow = create_basic_workflow("Validate user data", "webhook", "medium")
        return "Validation" in workflow['name'] or "Data" in workflow['name']
    
    def test_action_based_naming_2():
        workflow = create_basic_workflow("Send notifications", "webhook", "medium")
        return "Notification" in workflow['name']
    
    def test_unique_naming():
        workflow1 = create_basic_workflow("Test workflow", "webhook", "medium")
        workflow2 = create_basic_workflow("Test workflow", "webhook", "medium")
        # Names should be different due to timestamp/hash
        return workflow1['name'] != workflow2['name']
    
    # Run naming tests
    naming_tests = [
        ("Healthcare Naming 1", test_healthcare_naming_1),
        ("Healthcare Naming 2", test_healthcare_naming_2),
        ("Healthcare Naming 3", test_healthcare_naming_3),
        ("Finance Naming 1", test_finance_naming_1),
        ("Finance Naming 2", test_finance_naming_2),
        ("Finance Naming 3", test_finance_naming_3),
        ("Education Naming 1", test_education_naming_1),
        ("Education Naming 2", test_education_naming_2),
        ("Education Naming 3", test_education_naming_3),
        ("Ecommerce Naming 1", test_ecommerce_naming_1),
        ("Ecommerce Naming 2", test_ecommerce_naming_2),
        ("Ecommerce Naming 3", test_ecommerce_naming_3),
        ("Action Based Naming 1", test_action_based_naming_1),
        ("Action Based Naming 2", test_action_based_naming_2),
        ("Unique Naming", test_unique_naming),
    ]
    
    for name, test_func in naming_tests:
        runner.run_test(name, test_func)
    
    # CATEGORY 5: NODE GENERATION AND DIVERSITY TESTS (15 tests)
    print("\n🔧 CATEGORY 5: NODE GENERATION (15 tests)")
    
    def test_node_diversity_1():
        analysis = analyze_workflow_description("Healthcare system with validation, email, database, and monitoring")
        nodes = generate_nodes_from_description(analysis, 'complex', {}, {'unique_seed': 123})
        node_types = [node.get('type', 'unknown') for node in nodes]
        unique_types = set(node_types)
        return len(unique_types) >= 4
    
    def test_node_diversity_2():
        analysis = analyze_workflow_description("E-commerce with payment, inventory, notifications, and analytics")
        nodes = generate_nodes_from_description(analysis, 'complex', {}, {'unique_seed': 456})
        node_types = [node.get('type', 'unknown') for node in nodes]
        unique_types = set(node_types)
        return len(unique_types) >= 4
    
    def test_node_purposes_preserved():
        analysis = analyze_workflow_description("Process customer data with validation")
        nodes = generate_nodes_from_description(analysis, 'medium', {}, {'unique_seed': 789})
        purposes = [node.get('purpose', 'no purpose') for node in nodes]
        return all(purpose != 'no purpose' for purpose in purposes)
    
    def test_email_node_generation():
        analysis = analyze_workflow_description("Send email notifications to customers")
        nodes = generate_nodes_from_description(analysis, 'medium', {}, {'unique_seed': 111})
        has_email = any('email' in node.get('type', '') for node in nodes)
        return has_email
    
    def test_database_node_generation():
        analysis = analyze_workflow_description("Store customer data in database")
        nodes = generate_nodes_from_description(analysis, 'medium', {}, {'unique_seed': 222})
        has_database = any('database' in node.get('type', '') for node in nodes)
        return has_database
    
    def test_validation_node_generation():
        analysis = analyze_workflow_description("Validate user input data")
        nodes = generate_nodes_from_description(analysis, 'medium', {}, {'unique_seed': 333})
        has_validation = any('validation' in node.get('type', '') for node in nodes)
        return has_validation
    
    def test_conditional_node_generation():
        analysis = analyze_workflow_description("Route data based on conditions")
        nodes = generate_nodes_from_description(analysis, 'medium', {}, {'unique_seed': 444})
        has_conditional = any('conditional' in node.get('type', '') for node in nodes)
        return has_conditional
    
    def test_http_node_generation():
        analysis = analyze_workflow_description("Make API calls to external services")
        nodes = generate_nodes_from_description(analysis, 'medium', {}, {'unique_seed': 555})
        has_http = any('http' in node.get('type', '') for node in nodes)
        return has_http
    
    def test_slack_node_generation():
        analysis = analyze_workflow_description("Send Slack messages to team")
        nodes = generate_nodes_from_description(analysis, 'medium', {}, {'unique_seed': 666})
        has_slack = any('slack' in node.get('type', '') for node in nodes)
        return has_slack
    
    def test_error_handling_node():
        analysis = analyze_workflow_description("Complex system with error handling and retry logic")
        nodes = generate_nodes_from_description(analysis, 'complex', {}, {'unique_seed': 777})
        has_error_handling = any('error' in node.get('type', '') for node in nodes)
        return has_error_handling
    
    def test_monitoring_node():
        analysis = analyze_workflow_description("Monitor system performance and track metrics")
        nodes = generate_nodes_from_description(analysis, 'complex', {}, {'unique_seed': 888})
        has_monitoring = any('monitoring' in node.get('type', '') for node in nodes)
        return has_monitoring
    
    def test_file_operation_node():
        analysis = analyze_workflow_description("Process files and handle document uploads")
        nodes = generate_nodes_from_description(analysis, 'medium', {}, {'unique_seed': 999})
        has_file_ops = any('file' in node.get('type', '') for node in nodes)
        return has_file_ops
    
    def test_node_metadata_preservation():
        analysis = analyze_workflow_description("Test workflow")
        nodes = generate_nodes_from_description(analysis, 'medium', {}, {'unique_seed': 101})
        return all('type' in node and 'purpose' in node for node in nodes)
    
    def test_node_count_scaling():
        simple_analysis = analyze_workflow_description("Simple task")
        complex_analysis = analyze_workflow_description("Complex enterprise system with multiple integrations")
        
        simple_nodes = generate_nodes_from_description(simple_analysis, 'simple', {}, {'unique_seed': 102})
        complex_nodes = generate_nodes_from_description(complex_analysis, 'complex', {}, {'unique_seed': 103})
        
        return len(simple_nodes) < len(complex_nodes)
    
    def test_node_uniqueness():
        analysis = analyze_workflow_description("Test workflow")
        nodes1 = generate_nodes_from_description(analysis, 'medium', {}, {'unique_seed': 104})
        nodes2 = generate_nodes_from_description(analysis, 'medium', {}, {'unique_seed': 105})
        
        # Should generate different configurations due to different seeds
        return nodes1 != nodes2
    
    # Run node generation tests
    node_tests = [
        ("Node Diversity 1", test_node_diversity_1),
        ("Node Diversity 2", test_node_diversity_2),
        ("Node Purposes Preserved", test_node_purposes_preserved),
        ("Email Node Generation", test_email_node_generation),
        ("Database Node Generation", test_database_node_generation),
        ("Validation Node Generation", test_validation_node_generation),
        ("Conditional Node Generation", test_conditional_node_generation),
        ("HTTP Node Generation", test_http_node_generation),
        ("Slack Node Generation", test_slack_node_generation),
        ("Error Handling Node", test_error_handling_node),
        ("Monitoring Node", test_monitoring_node),
        ("File Operation Node", test_file_operation_node),
        ("Node Metadata Preservation", test_node_metadata_preservation),
        ("Node Count Scaling", test_node_count_scaling),
        ("Node Uniqueness", test_node_uniqueness),
    ]
    
    for name, test_func in node_tests:
        runner.run_test(name, test_func)
    
    # CATEGORY 6: EDGE CASES AND ERROR HANDLING (15 tests)
    print("\n🛡️ CATEGORY 6: EDGE CASES (15 tests)")
    
    def test_empty_description():
        try:
            workflow = create_basic_workflow("", "webhook", "medium")
            return len(workflow['nodes']) > 0
        except:
            return False
    
    def test_very_short_description():
        try:
            workflow = create_basic_workflow("a", "webhook", "medium")
            return len(workflow['nodes']) > 0
        except:
            return False
    
    def test_very_long_description():
        long_desc = "This is a very long description " * 100
        try:
            workflow = create_basic_workflow(long_desc, "webhook", "medium")
            return len(workflow['nodes']) > 0
        except:
            return False
    
    def test_special_characters():
        try:
            workflow = create_basic_workflow("Test with special chars: @#$%^&*()", "webhook", "medium")
            return len(workflow['nodes']) > 0
        except:
            return False
    
    def test_unicode_characters():
        try:
            workflow = create_basic_workflow("Test with unicode: 你好 🚀 café", "webhook", "medium")
            return len(workflow['nodes']) > 0
        except:
            return False
    
    def test_invalid_trigger_type():
        try:
            workflow = create_basic_workflow("Test", "invalid_trigger", "medium")
            return len(workflow['nodes']) > 0  # Should fallback gracefully
        except:
            return False
    
    def test_invalid_complexity():
        try:
            workflow = create_basic_workflow("Test", "webhook", "invalid_complexity")
            return len(workflow['nodes']) > 0  # Should fallback gracefully
        except:
            return False
    
    def test_none_description():
        try:
            workflow = create_basic_workflow(None, "webhook", "medium")
            return len(workflow['nodes']) > 0
        except:
            return False
    
    def test_numeric_description():
        try:
            workflow = create_basic_workflow(12345, "webhook", "medium")
            return len(workflow['nodes']) > 0
        except:
            return False
    
    def test_workflow_json_serialization():
        try:
            workflow = create_basic_workflow("Test workflow", "webhook", "medium")
            json_str = json.dumps(workflow)
            parsed = json.loads(json_str)
            return parsed['name'] == workflow['name']
        except:
            return False
    
    def test_workflow_structure_validity():
        workflow = create_basic_workflow("Test", "webhook", "medium")
        required_fields = ['name', 'nodes', 'connections', 'active', 'settings', 'tags']
        return all(field in workflow for field in required_fields)
    
    def test_node_structure_validity():
        workflow = create_basic_workflow("Test", "webhook", "medium")
        if not workflow['nodes']:
            return False
        
        node = workflow['nodes'][0]
        required_fields = ['parameters', 'id', 'name', 'type', 'typeVersion', 'position']
        return all(field in node for field in required_fields)
    
    def test_connection_structure_validity():
        workflow = create_basic_workflow("Test with multiple nodes", "webhook", "medium")
        if len(workflow['nodes']) < 2:
            return True  # No connections needed for single node
        
        connections = workflow['connections']
        return isinstance(connections, dict)
    
    def test_large_workflow_generation():
        try:
            desc = "Enterprise system with " + ", ".join([f"component {i}" for i in range(50)])
            workflow = create_basic_workflow(desc, "webhook", "complex")
            return len(workflow['nodes']) <= 15  # Should respect max limits
        except:
            return False
    
    def test_concurrent_generation():
        try:
            import threading
            results = []
            
            def generate_workflow():
                workflow = create_basic_workflow("Concurrent test", "webhook", "medium")
                results.append(len(workflow['nodes']))
            
            threads = [threading.Thread(target=generate_workflow) for _ in range(5)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            
            return len(results) == 5 and all(r > 0 for r in results)
        except:
            return False
    
    # Run edge case tests
    edge_tests = [
        ("Empty Description", test_empty_description),
        ("Very Short Description", test_very_short_description),
        ("Very Long Description", test_very_long_description),
        ("Special Characters", test_special_characters),
        ("Unicode Characters", test_unicode_characters),
        ("Invalid Trigger Type", test_invalid_trigger_type),
        ("Invalid Complexity", test_invalid_complexity),
        ("None Description", test_none_description),
        ("Numeric Description", test_numeric_description),
        ("JSON Serialization", test_workflow_json_serialization),
        ("Workflow Structure", test_workflow_structure_validity),
        ("Node Structure", test_node_structure_validity),
        ("Connection Structure", test_connection_structure_validity),
        ("Large Workflow", test_large_workflow_generation),
        ("Concurrent Generation", test_concurrent_generation),
    ]
    
    for name, test_func in edge_tests:
        runner.run_test(name, test_func)
    
    # Print final summary
    return runner.print_summary()

if __name__ == '__main__':
    success = run_100_tests()
    sys.exit(0 if success else 1)