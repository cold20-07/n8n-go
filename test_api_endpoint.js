#!/usr/bin/env node
/**
 * Test the API endpoint functionality
 */

// Mock the API function
const apiHandler = require('./api/index.js');

async function testAPIEndpoint() {
  console.log('🧪 Testing API Endpoint Functionality');
  console.log('=' * 40);
  
  // Test health endpoint
  console.log('\n1. Testing Health Endpoint...');
  const healthReq = {
    method: 'GET',
    url: '/health'
  };
  
  let healthResponse = null;
  const healthRes = {
    setHeader: () => {},
    status: (code) => ({
      json: (data) => {
        healthResponse = { statusCode: code, data };
        return healthResponse;
      }
    })
  };
  
  await apiHandler(healthReq, healthRes);
  
  if (healthResponse && healthResponse.statusCode === 200) {
    console.log('   ✅ Health endpoint working');
    console.log(`   📊 Status: ${healthResponse.data.status}`);
    console.log(`   📋 Version: ${healthResponse.data.version}`);
  } else {
    console.log('   ❌ Health endpoint failed');
  }
  
  // Test workflow generation
  console.log('\n2. Testing Workflow Generation...');
  
  const testCases = [
    {
      name: "Slack + Google Sheets",
      description: "Send a Slack message when a new lead is added to Google Sheets",
      triggerType: "webhook",
      complexity: "medium"
    },
    {
      name: "AI Email Summary", 
      description: "Summarize Gmail emails using OpenAI GPT",
      triggerType: "schedule",
      complexity: "complex"
    },
    {
      name: "E-commerce Alert",
      description: "Send Telegram notification for Shopify orders",
      triggerType: "webhook", 
      complexity: "medium"
    }
  ];
  
  let successCount = 0;
  
  for (const testCase of testCases) {
    console.log(`\n   Testing: ${testCase.name}`);
    
    const generateReq = {
      method: 'POST',
      url: '/generate',
      body: JSON.stringify({
        description: testCase.description,
        triggerType: testCase.triggerType,
        complexity: testCase.complexity
      })
    };
    
    let generateResponse = null;
    const generateRes = {
      setHeader: () => {},
      status: (code) => ({
        json: (data) => {
          generateResponse = { statusCode: code, data };
          return generateResponse;
        }
      })
    };
    
    try {
      await apiHandler(generateReq, generateRes);
      
      if (generateResponse && generateResponse.statusCode === 200 && generateResponse.data.success) {
        console.log('   ✅ Generation successful');
        console.log(`   📊 Nodes: ${generateResponse.data.node_count}`);
        console.log(`   🎯 Services: ${generateResponse.data.services_detected?.join(', ') || 'detected'}`);
        console.log(`   📈 Complexity: ${generateResponse.data.complexity}`);
        successCount++;
      } else {
        console.log('   ❌ Generation failed');
        if (generateResponse?.data?.error) {
          console.log(`   Error: ${generateResponse.data.error}`);
        }
      }
    } catch (error) {
      console.log(`   ❌ Generation error: ${error.message}`);
    }
  }
  
  // Summary
  console.log('\n' + '=' * 40);
  console.log(`📊 API Test Results: ${successCount + 1}/${testCases.length + 1} passed`);
  console.log(`📈 Success Rate: ${Math.round(((successCount + 1) / (testCases.length + 1)) * 100)}%`);
  
  if (successCount === testCases.length) {
    console.log('🎉 All API tests passed! Ready for Vercel deployment.');
    return true;
  } else {
    console.log('⚠️ Some API tests failed. Check the implementation.');
    return false;
  }
}

// Run the test
if (require.main === module) {
  testAPIEndpoint().then(success => {
    process.exit(success ? 0 : 1);
  }).catch(error => {
    console.error('API test failed:', error);
    process.exit(1);
  });
}

module.exports = { testAPIEndpoint };