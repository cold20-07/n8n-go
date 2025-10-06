#!/usr/bin/env node
/**
 * 50 Prompt Test Runner
 * Ready to test 50 different workflow generation prompts
 */

const { WorkflowValidator } = require('./comprehensive_workflow_tester.js');

// This will hold your 50 test prompts
let testPrompts = [];

// Function to add test prompts
function addTestPrompt(name, description, triggerType = 'webhook', complexity = 'medium', expectedServices = []) {
  testPrompts.push({
    name,
    description,
    triggerType,
    complexity,
    expectedServices
  });
}

// Function to run all 50 tests
async function run50PromptTest() {
  if (testPrompts.length === 0) {
    console.log('❌ No test prompts loaded. Please add your 50 prompts using addTestPrompt()');
    return;
  }

  console.log(`🚀 Running ${testPrompts.length} Prompt Test Suite`);
  console.log('Each prompt will be validated for:');
  console.log('  • Node Types & Configuration (25 points)');
  console.log('  • Connection Validity (25 points)');
  console.log('  • Parameter Correctness (20 points)');
  console.log('  • Goal Achievement (20 points)');
  console.log('  • Production Readiness (10 points)');
  console.log('='.repeat(80));

  const validator = new WorkflowValidator();
  const results = await validator.runComprehensiveTest(testPrompts);

  // Detailed analysis
  console.log('\n📈 DETAILED ANALYSIS');
  console.log('='.repeat(50));

  // Category breakdown
  const categories = {
    nodeValidation: 'Node Quality',
    connectionValidation: 'Connection Quality', 
    parameterValidation: 'Parameter Quality',
    goalAchievement: 'Goal Achievement',
    productionReadiness: 'Production Readiness'
  };

  for (const [key, name] of Object.entries(categories)) {
    const scores = results.results.map(r => r.details[key].score);
    const avgScore = scores.reduce((a, b) => a + b, 0) / scores.length;
    const passRate = scores.filter(s => s >= (key === 'productionReadiness' ? 6 : key === 'parameterValidation' || key === 'goalAchievement' ? 12 : 15)).length;
    
    console.log(`${name}: ${avgScore.toFixed(1)} avg, ${passRate}/${testPrompts.length} passed`);
  }

  // Failed tests analysis
  const failedTests = results.results.filter(r => !r.passed);
  if (failedTests.length > 0) {
    console.log(`\n❌ FAILED TESTS (${failedTests.length}/${testPrompts.length})`);
    console.log('='.repeat(50));
    
    failedTests.forEach((test, index) => {
      console.log(`${index + 1}. ${test.testCase} (Score: ${test.score}/100)`);
      
      // Show main issues
      const allIssues = [];
      Object.values(test.details).forEach(detail => {
        allIssues.push(...detail.issues);
      });
      
      if (allIssues.length > 0) {
        console.log(`   Issues: ${allIssues.slice(0, 3).join(', ')}${allIssues.length > 3 ? '...' : ''}`);
      }
    });
  }

  // Success rate by complexity
  const complexityStats = {};
  testPrompts.forEach((prompt, index) => {
    const complexity = prompt.complexity;
    if (!complexityStats[complexity]) {
      complexityStats[complexity] = { total: 0, passed: 0 };
    }
    complexityStats[complexity].total++;
    if (results.results[index].passed) {
      complexityStats[complexity].passed++;
    }
  });

  console.log('\n📊 SUCCESS RATE BY COMPLEXITY');
  console.log('='.repeat(50));
  for (const [complexity, stats] of Object.entries(complexityStats)) {
    const rate = Math.round((stats.passed / stats.total) * 100);
    console.log(`${complexity}: ${stats.passed}/${stats.total} (${rate}%)`);
  }

  return results;
}

// Export functions for external use
module.exports = {
  addTestPrompt,
  run50PromptTest,
  testPrompts
};

// CLI usage
if (require.main === module) {
  console.log('🔧 50 Prompt Test Runner Ready!');
  console.log('');
  console.log('To use this tester:');
  console.log('1. Add your test prompts using addTestPrompt()');
  console.log('2. Call run50PromptTest() to execute all tests');
  console.log('');
  console.log('Example:');
  console.log('  addTestPrompt("Test 1", "Send Slack message when...", "webhook", "medium");');
  console.log('  run50PromptTest();');
  console.log('');
  console.log('Ready for your 50 prompts! 🚀');
}