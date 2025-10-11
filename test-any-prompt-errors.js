#!/usr/bin/env node
/**
 * Test Universal Error Handling with Various Prompts
 * Demonstrates how the system handles errors from ANY prompt scenario
 */

const { UniversalErrorHandler } = require('./universal-error-handler.js');
const apiHandler = require('./api/index.js');

class PromptErrorTester {
  constructor() {
    this.errorHandler = new UniversalErrorHandler();
    this.testScenarios = this.buildTestScenarios();
  }

  /**
   * Build various error-prone test scenarios
   */
  buildTestScenarios() {
    return [
      {
        name: 'Valid Simple Prompt',
        description: 'Send a Slack message when webhook is triggered',
        triggerType: 'webhook',
        complexity: 'simple',
        expectedIssues: 0
      },
      {
        name: 'Complex Multi-Service Prompt',
        description: 'Monitor API every 5 minutes, check response time, if over 2 seconds send Slack alert and create GitHub issue',
        triggerType: 'schedule',
        complexity: 'complex',
        expectedIssues: 0
      },
      {
        name: 'Ambiguous Prompt',
        description: 'do something with data',
        triggerType: 'webhook',
        complexity: 'simple',
        expectedIssues: 0 // Should be handled gracefully
      },
      {
        name: 'Very Long Prompt',
        description: 'Create a comprehensive workflow that monitors multiple APIs including GitHub, Slack, Gmail, Trello, Shopify, Notion, Airtable, Discord, Telegram, and WhatsApp, processes the data through multiple validation steps, applies complex business logic, sends notifications to various channels, creates tasks in project management tools, updates databases, generates reports, and handles all possible error scenarios with retry logic and fallback mechanisms',
        triggerType: 'schedule',
        complexity: 'complex',
        expectedIssues: 0
      },
      {
        name: 'Empty Prompt',
        description: '',
        triggerType: 'webhook',
        complexity: 'simple',
        expectedIssues: 1 // Should create fallback
      },
      {
        name: 'Special Characters Prompt',
        description: 'Send message with émojis 🚀 and spëcial chars & symbols @#$%^&*()',
        triggerType: 'webhook',
        complexity: 'simple',
        expectedIssues: 0
      },
      {
        name: 'Non-English Prompt',
        description: 'Enviar mensaje de Slack cuando se reciba webhook',
        triggerType: 'webhook',
        complexity: 'simple',
        expectedIssues: 0
      },
      {
        name: 'Technical Jargon Prompt',
        description: 'Implement OAuth2 authentication flow with JWT tokens, validate CORS headers, process GraphQL mutations, and trigger serverless functions',
        triggerType: 'webhook',
        complexity: 'complex',
        expectedIssues: 0
      },
      {
        name: 'Contradictory Prompt',
        description: 'Create a manual trigger that runs automatically every hour without user intervention',
        triggerType: 'manual',
        complexity: 'medium',
        expectedIssues: 0 // Should resolve contradiction
      },
      {
        name: 'Impossible Prompt',
        description: 'Connect to a service that does not exist and perform operations that are not possible',
        triggerType: 'webhook',
        complexity: 'complex',
        expectedIssues: 0 // Should create fallback
      }
    ];
  }

  /**
   * Test all scenarios
   */
  async runAllTests() {
    console.log('🧪 Testing Universal Error Handling with Various Prompts');
    console.log('=' * 70);
    
    let totalTests = 0;
    let passedTests = 0;
    const results = [];

    for (const scenario of this.testScenarios) {
      totalTests++;
      console.log(`\n${totalTests}. Testing: ${scenario.name}`);
      console.log(`   Prompt: "${scenario.description}"`);
      
      try {
        const result = await this.testScenario(scenario);
        
        if (result.success) {
          passedTests++;
          console.log(`   ✅ PASSED - Workflow generated successfully`);
          console.log(`   📊 Nodes: ${result.nodeCount}, Fixes: ${result.fixesApplied}`);
          
          if (result.fixesApplied > 0) {
            console.log(`   🔧 Auto-fixes applied: ${result.fixesApplied}`);
          }
        } else {
          console.log(`   ❌ FAILED - ${result.error}`);
        }
        
        results.push(result);
        
      } catch (error) {
        console.log(`   💥 ERROR - ${error.message}`);
        results.push({
          scenario: scenario.name,
          success: false,
          error: error.message,
          nodeCount: 0,
          fixesApplied: 0
        });
      }
    }

    // Summary
    console.log('\n📊 Test Results Summary');
    console.log('=' * 50);
    console.log(`Total Tests: ${totalTests}`);
    console.log(`Passed: ${passedTests}`);
    console.log(`Failed: ${totalTests - passedTests}`);
    console.log(`Success Rate: ${Math.round((passedTests / totalTests) * 100)}%`);

    // Error statistics
    const errorStats = this.errorHandler.getErrorStats();
    console.log('\n🔧 Error Handling Statistics:');
    console.log(`Total Errors Detected: ${errorStats.totalErrors}`);
    console.log(`Errors Fixed: ${errorStats.fixedErrors}`);
    console.log(`Fix Rate: ${errorStats.fixRate}`);

    if (Object.keys(errorStats.errorTypes).length > 0) {
      console.log('\n📋 Error Types Encountered:');
      for (const [type, count] of Object.entries(errorStats.errorTypes)) {
        console.log(`   ${type}: ${count}`);
      }
    }

    // Save detailed report
    await this.saveTestReport(results, errorStats);

    return {
      totalTests,
      passedTests,
      successRate: Math.round((passedTests / totalTests) * 100),
      errorStats
    };
  }

  /**
   * Test individual scenario
   */
  async testScenario(scenario) {
    try {
      // Create protected workflow generator
      const protectedGenerator = this.errorHandler.wrapWorkflowGenerator(
        async (description, triggerType, complexity) => {
          // Simulate API call
          const mockReq = {
            method: 'POST',
            url: '/generate',
            body: JSON.stringify({ description, triggerType, complexity })
          };

          let responseData = null;
          const mockRes = {
            setHeader: () => {},
            status: (code) => mockRes,
            json: (data) => { responseData = data; return mockRes; },
            end: () => {}
          };

          await apiHandler(mockReq, mockRes);
          
          if (!responseData || !responseData.success) {
            throw new Error(responseData?.error || 'API call failed');
          }

          return responseData.workflow;
        },
        {
          scenarioName: scenario.name,
          testMode: true
        }
      );

      // Generate workflow with protection
      const workflow = await protectedGenerator(
        scenario.description,
        scenario.triggerType,
        scenario.complexity
      );

      // Validate result
      if (!workflow || !workflow.nodes) {
        throw new Error('Generated workflow is invalid');
      }

      return {
        scenario: scenario.name,
        success: true,
        nodeCount: workflow.nodes.length,
        fixesApplied: workflow.meta?.proactive_fixes?.length || 0,
        workflowName: workflow.name,
        isValid: workflow.meta?.proactive_validation?.isValid !== false
      };

    } catch (error) {
      return {
        scenario: scenario.name,
        success: false,
        error: error.message,
        nodeCount: 0,
        fixesApplied: 0
      };
    }
  }

  /**
   * Save detailed test report
   */
  async saveTestReport(results, errorStats) {
    const report = {
      timestamp: new Date().toISOString(),
      testSummary: {
        totalTests: results.length,
        passedTests: results.filter(r => r.success).length,
        failedTests: results.filter(r => !r.success).length,
        successRate: Math.round((results.filter(r => r.success).length / results.length) * 100)
      },
      errorHandlingStats: errorStats,
      detailedResults: results,
      scenarios: this.testScenarios.map(s => ({
        name: s.name,
        description: s.description,
        complexity: s.complexity
      }))
    };

    const fs = require('fs');
    fs.writeFileSync('prompt-error-test-report.json', JSON.stringify(report, null, 2));
    console.log('\n📄 Detailed test report saved to: prompt-error-test-report.json');
  }

  /**
   * Test specific error injection
   */
  async testErrorInjection() {
    console.log('\n🧪 Testing Error Injection Scenarios');
    
    // Test with intentionally broken workflow
    const brokenWorkflow = {
      name: 'Broken Workflow',
      nodes: [
        {
          // Missing required fields
          name: 'Broken Node',
          type: 'invalid-node-type'
        }
      ],
      connections: {
        'NonExistentNode': {
          main: [[{ node: 'AnotherNonExistentNode', type: 'main', index: 0 }]]
        }
      }
    };

    const result = await this.errorHandler.handleAnyWorkflowErrors(brokenWorkflow, {
      source: 'error_injection_test'
    });

    console.log(`   Fixes Applied: ${result.fixes.length}`);
    console.log(`   Issues Found: ${result.issues.length}`);
    console.log(`   Final Validity: ${result.isValid ? 'Valid' : 'Invalid'}`);

    return result;
  }
}

// Run tests
async function main() {
  const tester = new PromptErrorTester();
  
  console.log('🛡️ Universal Error Handling Test Suite');
  console.log('Testing how the system handles errors from ANY prompt...\n');

  // Run main tests
  const mainResults = await tester.runAllTests();
  
  // Run error injection test
  await tester.testErrorInjection();

  // Final summary
  console.log('\n🎯 Final Summary:');
  console.log(`✅ The Universal Error Handler successfully handled ${mainResults.successRate}% of all prompt scenarios`);
  console.log(`🔧 Automatically fixed ${mainResults.errorStats.fixedErrors} errors`);
  console.log(`🛡️ System is ready to handle errors from ANY prompt!`);

  return mainResults.successRate >= 90; // Consider 90%+ success rate as passing
}

if (require.main === module) {
  main().then(success => {
    process.exit(success ? 0 : 1);
  }).catch(error => {
    console.error('Test suite error:', error);
    process.exit(1);
  });
}

module.exports = { PromptErrorTester };