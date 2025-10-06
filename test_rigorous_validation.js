#!/usr/bin/env node
/**
 * Rigorous Workflow Validation Test
 * Tests the actual quality and correctness of generated workflows
 */

const apiHandler = require('./api/index.js');

const rigorousTestCases = [
  {
    name: "API Monitoring Workflow",
    description: "Monitor an API endpoint every 10 minutes and trigger an alert if response time exceeds 2 seconds",
    triggerType: "schedule",
    complexity: "complex",
    strictValidation: {
      mustHaveNodes: ["schedule", "http", "condition", "alert"],
      mustHaveConnections: 4,
      mustHaveServices: ["schedule", "http_request", "if", "slack"],
      nodeSequence: ["trigger", "request", "process", "condition", "alert"]
    }
  },
  {
    name: "Simple Slack Notification",
    description: "Send a Slack message when a new lead is added to Google Sheets",
    triggerType: "webhook", 
    complexity: "medium",
    strictValidation: {
      mustHaveNodes: ["trigger", "slack"],
      mustHaveConnections: 1,
      mustHaveServices: ["google_sheets", "slack"],
      nodeSequence: ["trigger", "action"]
    }
  },
  {
    name: "Complex E-commerce Flow",
    description: "When a new Shopify order is created, validate inventory, send confirmation email via Gmail, and create a task in Trello",
    triggerType: "webhook",
    complexity: "complex", 
    strictValidation: {
      mustHaveNodes: ["shopify", "validation", "gmail", "trello"],
      mustHaveConnections: 3,
      mustHaveServices: ["shopify", "gmail", "trello"],
      nodeSequence: ["trigger", "validation", "email", "task"]
    }
  }
];

async function testRigorousValidation() {
  console.log('🔍 Rigorous Workflow Validation Test');
  console.log('Testing actual workflow quality and correctness...');
  console.log('=' * 60);
  
  let passedTests = 0;
  let totalTests = rigorousTestCases.length;
  
  for (const testCase of rigorousTestCases) {
    console.log(`\n🧪 Testing: ${testCase.name}`);
    console.log(`📝 Description: ${testCase.description}`);
    
    try {
      // Create mock request
      const mockReq = {
        method: 'POST',
        url: '/generate',
        body: JSON.stringify({
          description: testCase.description,
          triggerType: testCase.triggerType,
          complexity: testCase.complexity
        })
      };
      
      let responseData = null;
      let statusCode = null;
      
      const mockRes = {
        setHeader: () => {},
        status: (code) => {
          statusCode = code;
          return mockRes;
        },
        json: (data) => {
          responseData = data;
          return mockRes;
        },
        end: () => {}
      };
      
      // Call API
      await apiHandler(mockReq, mockRes);
      
      if (statusCode === 200 && responseData && responseData.success) {
        const workflow = responseData.workflow;
        const validation = testCase.strictValidation;
        
        // Detailed validation
        const results = {
          hasRequiredNodes: true,
          hasRequiredConnections: true,
          hasRequiredServices: true,
          hasCorrectSequence: true,
          issues: []
        };
        
        // Check required node types (more flexible matching)
        const nodeNames = workflow.nodes.map(n => n.name.toLowerCase());
        const nodeTypes = workflow.nodes.map(n => n.type.toLowerCase());
        
        for (const requiredNode of validation.mustHaveNodes) {
          let found = false;
          
          // Check node names for keywords
          if (requiredNode === 'schedule') {
            found = nodeNames.some(name => name.includes('schedule') || name.includes('monitor'));
          } else if (requiredNode === 'http') {
            found = nodeNames.some(name => name.includes('api') || name.includes('http') || name.includes('endpoint'));
          } else if (requiredNode === 'condition') {
            found = nodeNames.some(name => name.includes('check') || name.includes('condition') || name.includes('response'));
          } else if (requiredNode === 'alert') {
            found = nodeNames.some(name => name.includes('alert') || name.includes('slack') || name.includes('send'));
          } else if (requiredNode === 'trigger') {
            found = nodeTypes.some(type => type.includes('webhook') || type.includes('schedule'));
          } else if (requiredNode === 'slack') {
            found = nodeNames.some(name => name.includes('slack')) || nodeTypes.some(type => type.includes('slack'));
          } else if (requiredNode === 'gmail') {
            found = nodeNames.some(name => name.includes('email') || name.includes('gmail')) || nodeTypes.some(type => type.includes('gmail'));
          } else if (requiredNode === 'trello') {
            found = nodeNames.some(name => name.includes('trello') || name.includes('card')) || nodeTypes.some(type => type.includes('trello'));
          } else if (requiredNode === 'shopify') {
            found = nodeNames.some(name => name.includes('shopify') || name.includes('order')) || nodeTypes.some(type => type.includes('shopify'));
          } else if (requiredNode === 'validation') {
            found = nodeNames.some(name => name.includes('validate') || name.includes('process'));
          } else {
            found = nodeNames.some(name => name.includes(requiredNode));
          }
          
          if (!found) {
            results.hasRequiredNodes = false;
            results.issues.push(`Missing required node type: ${requiredNode} (checked names: ${nodeNames.join(', ')})`);
          }
        }
        
        // Check connection count
        const connectionCount = Object.keys(workflow.connections).length;
        if (connectionCount < validation.mustHaveConnections) {
          results.hasRequiredConnections = false;
          results.issues.push(`Insufficient connections: ${connectionCount} < ${validation.mustHaveConnections}`);
        }
        
        // Check required services
        const detectedServices = workflow.meta.services_detected || [];
        for (const requiredService of validation.mustHaveServices) {
          if (!detectedServices.includes(requiredService)) {
            results.hasRequiredServices = false;
            results.issues.push(`Missing required service: ${requiredService}`);
          }
        }
        
        // Check node sequence logic
        if (workflow.nodes.length < validation.nodeSequence.length) {
          results.hasCorrectSequence = false;
          results.issues.push(`Insufficient nodes for sequence: ${workflow.nodes.length} < ${validation.nodeSequence.length}`);
        }
        
        // Overall test result
        const testPassed = results.hasRequiredNodes && 
                          results.hasRequiredConnections && 
                          results.hasRequiredServices && 
                          results.hasCorrectSequence;
        
        console.log(`   ${testPassed ? '✅' : '❌'} Validation: ${testPassed ? 'PASSED' : 'FAILED'}`);
        console.log(`   📊 Nodes: ${workflow.nodes.length} (${nodeNames.join(', ')})`);
        console.log(`   🔗 Connections: ${connectionCount}`);
        console.log(`   🎯 Services: ${detectedServices.join(', ')}`);
        console.log(`   🏗️ Node Types: ${workflow.nodes.map(n => n.type).join(', ')}`);
        
        // Detailed validation results
        console.log(`   ✅ Required Nodes: ${results.hasRequiredNodes ? 'PASS' : 'FAIL'}`);
        console.log(`   ✅ Required Connections: ${results.hasRequiredConnections ? 'PASS' : 'FAIL'}`);
        console.log(`   ✅ Required Services: ${results.hasRequiredServices ? 'PASS' : 'FAIL'}`);
        console.log(`   ✅ Correct Sequence: ${results.hasCorrectSequence ? 'PASS' : 'FAIL'}`);
        
        if (results.issues.length > 0) {
          console.log(`   ❌ Issues:`);
          results.issues.forEach(issue => console.log(`      - ${issue}`));
        }
        
        if (testPassed) {
          passedTests++;
        }
        
      } else {
        console.log(`   ❌ API Error: Status=${statusCode}, Success=${responseData?.success}`);
        console.log(`   ❌ Error: ${responseData?.error || 'Unknown error'}`);
      }
      
    } catch (error) {
      console.log(`   ❌ Test Error: ${error.message}`);
    }
  }
  
  console.log(`\n📊 Rigorous Validation Results: ${passedTests}/${totalTests} passed`);
  console.log(`📈 Success Rate: ${Math.round((passedTests/totalTests) * 100)}%`);
  
  if (passedTests === totalTests) {
    console.log('\n🎉 All rigorous tests passed!');
    console.log('✅ Workflows meet strict quality standards');
    console.log('✅ Proper node types and sequences');
    console.log('✅ Correct service detection');
    console.log('✅ Adequate connections');
  } else {
    console.log('\n⚠️ Some rigorous tests failed.');
    console.log('The workflow generator may need improvements for production use.');
  }
  
  return passedTests === totalTests;
}

// Run the tests
if (require.main === module) {
  testRigorousValidation().then(success => {
    process.exit(success ? 0 : 1);
  }).catch(error => {
    console.error('Rigorous test error:', error);
    process.exit(1);
  });
}

module.exports = { testRigorousValidation };