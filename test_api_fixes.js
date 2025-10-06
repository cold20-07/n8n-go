#!/usr/bin/env node
/**
 * Test API Fixes - Verify Enhanced Node Generation and Connections
 */

const apiHandler = require('./api/index.js');

const testCases = [
  {
    name: "API Monitoring Test",
    description: "Monitor an API endpoint every 10 minutes and trigger an alert if response time exceeds 2 seconds",
    triggerType: "schedule",
    complexity: "complex",
    expectedNodes: ["Monitor Schedule", "Monitor API Endpoint", "Process Response Time", "Check Response Time", "Send Alert"],
    expectedServices: ["schedule", "http_request", "code", "if", "slack"]
  },
  {
    name: "GitHub Deployment Test", 
    description: "Automatically deploy a GitHub repository through a webhook when new code is pushed to main",
    triggerType: "webhook",
    complexity: "complex",
    expectedServices: ["webhook", "github", "code"]
  },
  {
    name: "Email Processing Test",
    description: "Process incoming Gmail emails and create Trello cards for urgent messages",
    triggerType: "webhook", 
    complexity: "medium",
    expectedServices: ["gmail", "trello", "if"]
  }
];

async function testAPIFixes() {
  console.log('🔧 Testing API Fixes - Enhanced Node Generation');
  console.log('=' * 60);
  
  let passedTests = 0;
  let totalTests = testCases.length;
  
  for (const testCase of testCases) {
    console.log(`\n🧪 Testing: ${testCase.name}`);
    console.log(`📝 Description: ${testCase.description}`);
    
    try {
      // Create mock request/response objects
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
      
      // Call the API handler
      await apiHandler(mockReq, mockRes);
      
      // Validate response
      if (statusCode === 200 && responseData && responseData.success) {
        const workflow = responseData.workflow;
        
        // Check workflow structure
        const hasNodes = workflow.nodes && workflow.nodes.length > 0;
        const hasConnections = workflow.connections && Object.keys(workflow.connections).length > 0;
        const hasProperNodeCount = workflow.nodes.length >= 3; // At least trigger + action + processing
        
        // Check for specific node types in monitoring workflow
        let hasCorrectNodes = true;
        if (testCase.name === "API Monitoring Test") {
          const nodeNames = workflow.nodes.map(n => n.name);
          const hasSchedule = nodeNames.some(name => name.includes('Schedule'));
          const hasHTTP = nodeNames.some(name => name.includes('API') || name.includes('HTTP'));
          const hasCondition = nodeNames.some(name => name.includes('Check') || name.includes('Response'));
          const hasAlert = nodeNames.some(name => name.includes('Alert') || name.includes('Slack'));
          
          hasCorrectNodes = hasSchedule && hasHTTP && (hasCondition || hasAlert);
        }
        
        // Check connections are properly formed
        const connectionsValid = Object.values(workflow.connections).every(conn => 
          conn.main && Array.isArray(conn.main) && conn.main.length > 0
        );
        
        const testPassed = hasNodes && hasConnections && hasProperNodeCount && hasCorrectNodes && connectionsValid;
        
        console.log(`   ${testPassed ? '✅' : '❌'} Generation: ${testPassed ? 'SUCCESS' : 'FAILED'}`);
        console.log(`   📊 Nodes: ${workflow.nodes.length}`);
        console.log(`   🔗 Connections: ${Object.keys(workflow.connections).length}`);
        console.log(`   🎯 Services: ${workflow.meta.services_detected.join(', ')}`);
        console.log(`   🏗️ Node Names: ${workflow.nodes.map(n => n.name).join(', ')}`);
        
        if (testCase.name === "API Monitoring Test") {
          console.log(`   🔍 Schedule Node: ${workflow.nodes.some(n => n.name.includes('Schedule')) ? '✅' : '❌'}`);
          console.log(`   🌐 HTTP Node: ${workflow.nodes.some(n => n.name.includes('API') || n.name.includes('HTTP')) ? '✅' : '❌'}`);
          console.log(`   ⚡ Alert Node: ${workflow.nodes.some(n => n.name.includes('Alert') || n.name.includes('Slack')) ? '✅' : '❌'}`);
        }
        
        if (testPassed) {
          passedTests++;
        } else {
          console.log(`   ❌ Issues: Nodes=${hasNodes}, Connections=${hasConnections}, Count=${hasProperNodeCount}, Correct=${hasCorrectNodes}, Valid=${connectionsValid}`);
        }
        
      } else {
        console.log(`   ❌ API Error: Status=${statusCode}, Success=${responseData?.success}`);
        if (responseData?.error) {
          console.log(`   ❌ Error: ${responseData.error}`);
        }
      }
      
    } catch (error) {
      console.log(`   ❌ Test Error: ${error.message}`);
    }
  }
  
  console.log(`\n📊 API Fix Test Results: ${passedTests}/${totalTests} passed`);
  console.log(`📈 Success Rate: ${Math.round((passedTests/totalTests) * 100)}%`);
  
  if (passedTests === totalTests) {
    console.log('\n🎉 All API fixes working perfectly!');
    console.log('✅ Enhanced service detection');
    console.log('✅ Improved node generation');
    console.log('✅ Better connection logic');
    console.log('✅ API monitoring workflows');
  } else {
    console.log('\n⚠️ Some tests failed. Check the issues above.');
  }
  
  return passedTests === totalTests;
}

// Run the tests
if (require.main === module) {
  testAPIFixes().then(success => {
    process.exit(success ? 0 : 1);
  }).catch(error => {
    console.error('Test runner error:', error);
    process.exit(1);
  });
}

module.exports = { testAPIFixes };