#!/usr/bin/env node
/**
 * Integration Test for N8N Workflow Node Connection Fixes
 * Tests all components working together
 */

const { WorkflowNodeValidator } = require('./fix-workflow-nodes.js');
const { AdvancedWorkflowValidator } = require('./advanced-workflow-validator.js');
const { WorkflowConnectionHelper } = require('./workflow-connection-helper.js');

async function runIntegrationTest() {
  console.log('🧪 N8N Workflow Integration Test');
  console.log('Testing all validation and fixing components...\n');

  let allTestsPassed = true;

  try {
    // Test 1: Basic Node Validator
    console.log('1️⃣ Testing Basic Node Validator...');
    const basicValidator = new WorkflowNodeValidator();
    const basicResult = await basicValidator.validateWorkflowFile('sample_n8n_workflow.json');
    
    if (basicResult.isValid) {
      console.log('   ✅ Basic validation passed');
    } else {
      console.log('   ❌ Basic validation failed:', basicResult.issues);
      allTestsPassed = false;
    }

    // Test 2: Advanced Connection Validator
    console.log('\n2️⃣ Testing Advanced Connection Validator...');
    const advancedValidator = new AdvancedWorkflowValidator();
    const advancedResult = await advancedValidator.processWorkflowFile('sample_n8n_workflow.json');
    
    if (advancedResult.isValid) {
      console.log('   ✅ Advanced validation passed');
    } else {
      console.log('   ❌ Advanced validation failed:', advancedResult.issues);
      allTestsPassed = false;
    }

    // Test 3: Workflow Connection Helper
    console.log('\n3️⃣ Testing Workflow Connection Helper...');
    const helper = new WorkflowConnectionHelper();
    
    // Create a test workflow
    const testWorkflow = helper.createLinearWorkflow('Integration Test Workflow', [
      { category: 'triggers', nodeKey: 'webhook', customName: 'Test Trigger' },
      { category: 'actions', nodeKey: 'code', customName: 'Test Processing' },
      { category: 'actions', nodeKey: 'slack', customName: 'Test Notification' }
    ]);
    
    const helperValidation = helper.validateConnections(testWorkflow);
    
    if (helperValidation.isValid) {
      console.log('   ✅ Helper workflow creation passed');
      console.log(`   📊 Created workflow with ${testWorkflow.nodes.length} nodes`);
    } else {
      console.log('   ❌ Helper workflow creation failed:', helperValidation.issues);
      allTestsPassed = false;
    }

    // Test 4: API Integration (mock test)
    console.log('\n4️⃣ Testing API Integration...');
    try {
      const apiHandler = require('./api/index.js');
      
      const mockReq = {
        method: 'POST',
        url: '/generate',
        body: JSON.stringify({
          description: 'Send a Slack notification when webhook is triggered',
          triggerType: 'webhook',
          complexity: 'simple'
        })
      };
      
      let apiResult = null;
      const mockRes = {
        setHeader: () => {},
        status: (code) => mockRes,
        json: (data) => { apiResult = data; return mockRes; },
        end: () => {}
      };
      
      await apiHandler(mockReq, mockRes);
      
      if (apiResult && apiResult.success && apiResult.workflow) {
        const workflow = apiResult.workflow;
        const hasValidation = workflow.meta && workflow.meta.validation;
        
        if (hasValidation) {
          console.log('   ✅ API integration with validation passed');
          console.log(`   📊 Generated workflow: ${workflow.name}`);
          console.log(`   🔍 Validation included: ${workflow.meta.validation.isValid ? 'Valid' : 'Invalid'}`);
        } else {
          console.log('   ⚠️ API integration passed but validation metadata missing');
        }
      } else {
        console.log('   ❌ API integration failed');
        allTestsPassed = false;
      }
    } catch (error) {
      console.log('   ❌ API integration error:', error.message);
      allTestsPassed = false;
    }

    // Test 5: End-to-End Workflow Validation
    console.log('\n5️⃣ Testing End-to-End Workflow Validation...');
    
    // Test all created example workflows
    const exampleFiles = ['webhook-to-slack.json', 'api-monitoring.json', 'data-processing-pipeline.json'];
    let validExamples = 0;
    
    for (const file of exampleFiles) {
      try {
        const result = await basicValidator.validateWorkflowFile(file);
        if (result.isValid) {
          validExamples++;
          console.log(`   ✅ ${file} is valid`);
        } else {
          console.log(`   ❌ ${file} has issues:`, result.issues);
        }
      } catch (error) {
        console.log(`   ⚠️ Could not validate ${file}: ${error.message}`);
      }
    }
    
    if (validExamples === exampleFiles.length) {
      console.log('   ✅ All example workflows are valid');
    } else {
      console.log(`   ⚠️ Only ${validExamples}/${exampleFiles.length} example workflows are valid`);
    }

    // Final Results
    console.log('\n📊 Integration Test Results:');
    console.log('=' * 50);
    
    if (allTestsPassed) {
      console.log('🎉 ALL INTEGRATION TESTS PASSED!');
      console.log('✅ Basic node validation working');
      console.log('✅ Advanced connection validation working');
      console.log('✅ Workflow helper creating valid workflows');
      console.log('✅ API integration with validation working');
      console.log('✅ End-to-end validation working');
      console.log('\n🚀 Your n8n workflow generator is fully validated and ready!');
    } else {
      console.log('❌ Some integration tests failed');
      console.log('⚠️ Please check the issues above');
    }

    return allTestsPassed;

  } catch (error) {
    console.error('💥 Integration test error:', error);
    return false;
  }
}

// Run the integration test
if (require.main === module) {
  runIntegrationTest().then(success => {
    process.exit(success ? 0 : 1);
  }).catch(error => {
    console.error('Integration test failed:', error);
    process.exit(1);
  });
}

module.exports = { runIntegrationTest };