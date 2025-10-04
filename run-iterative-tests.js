// Execute the iterative n8n test runner
const N8nIterativeTestRunner = require('./n8n-iterative-test-runner.js');
const fs = require('fs');

async function main() {
  const runner = new N8nIterativeTestRunner();
  
  console.log('🎯 n8n Iterative Test Runner');
  console.log('📋 Running 10,000 tests with issue identification and fixing');
  console.log('🔄 Learning and improving with each test\n');
  
  const startTime = Date.now();
  
  try {
    const finalReport = await runner.runAllTests();
    
    const endTime = Date.now();
    const totalTime = endTime - startTime;
    
    console.log('\n' + '='.repeat(60));
    console.log('🎉 FINAL TEST REPORT');
    console.log('='.repeat(60));
    
    console.log('\n📊 SUMMARY:');
    console.log(`   Total Tests: ${finalReport.summary.totalTests}`);
    console.log(`   ✅ Passed: ${finalReport.summary.passedTests}`);
    console.log(`   ❌ Failed: ${finalReport.summary.failedTests}`);
    console.log(`   🚨 Errors: ${finalReport.summary.errorTests}`);
    console.log(`   📈 Success Rate: ${finalReport.summary.successRate}%`);
    
    console.log('\n⏱️ PERFORMANCE:');
    console.log(`   Total Execution Time: ${totalTime}ms (${(totalTime/1000).toFixed(2)}s)`);
    console.log(`   Average Test Time: ${finalReport.performance.avgTestTime.toFixed(2)}ms`);
    console.log(`   Fastest Test: #${finalReport.performance.fastestTest.id} (${finalReport.performance.fastestTest.time}ms)`);
    console.log(`   Slowest Test: #${finalReport.performance.slowestTest.id} (${finalReport.performance.slowestTest.time}ms)`);
    
    console.log('\n🔍 ISSUES ANALYSIS:');
    console.log(`   Total Issues Found: ${finalReport.issues.totalFound}`);
    console.log('   Issues by Category:');
    Object.entries(finalReport.issues.categories).forEach(([category, count]) => {
      console.log(`     ${category}: ${count}`);
    });
    
    console.log('\n🛠️ FIXES APPLIED:');
    console.log(`   Total Fixes Applied: ${finalReport.fixes.totalApplied}`);
    console.log('   Fixes by Category:');
    Object.entries(finalReport.fixes.categories).forEach(([category, count]) => {
      console.log(`     ${category}: ${count}`);
    });
    
    console.log('\n📚 LEARNINGS:');
    console.log(`   Total Learnings: ${finalReport.learnings.total}`);
    console.log(`   Unique Patterns: ${finalReport.learnings.unique}`);
    
    console.log('\n🔥 TOP ISSUE PATTERNS:');
    finalReport.issues.topPatterns.slice(0, 5).forEach(([pattern, count], index) => {
      console.log(`   ${index + 1}. ${pattern} (${count} occurrences)`);
    });
    
    // Save detailed results to file
    const detailedResults = {
      executionTime: totalTime,
      timestamp: new Date().toISOString(),
      finalReport: finalReport,
      testResults: runner.testResults.slice(0, 100), // Save first 100 for analysis
      learnings: runner.learnings,
      fixesApplied: runner.fixesApplied
    };
    
    fs.writeFileSync('n8n-test-results.json', JSON.stringify(detailedResults, null, 2));
    console.log('\n💾 Detailed results saved to n8n-test-results.json');
    
    // Generate insights
    generateInsights(finalReport, runner);
    
  } catch (error) {
    console.error('❌ Test execution failed:', error.message);
    console.error(error.stack);
  }
}

function generateInsights(report, runner) {
  console.log('\n' + '='.repeat(60));
  console.log('💡 KEY INSIGHTS & RECOMMENDATIONS');
  console.log('='.repeat(60));
  
  // Success rate insights
  if (report.summary.successRate > 90) {
    console.log('✅ Excellent success rate! The validation and fixing system is working well.');
  } else if (report.summary.successRate > 75) {
    console.log('⚠️ Good success rate, but there\'s room for improvement in issue detection.');
  } else {
    console.log('🚨 Low success rate indicates need for better validation rules.');
  }
  
  // Performance insights
  if (report.performance.avgTestTime < 10) {
    console.log('🚀 Excellent performance! Tests are running efficiently.');
  } else if (report.performance.avgTestTime < 50) {
    console.log('⚡ Good performance, tests are reasonably fast.');
  } else {
    console.log('🐌 Performance could be improved. Consider optimizing validation logic.');
  }
  
  // Issue pattern insights
  const topCategory = Object.entries(report.issues.categories)
    .sort(([,a], [,b]) => b - a)[0];
  
  if (topCategory) {
    console.log(`🎯 Most common issue category: ${topCategory[0]} (${topCategory[1]} occurrences)`);
    
    switch (topCategory[0]) {
      case 'VALIDATION':
        console.log('   💡 Focus on improving input validation and data structure checks.');
        break;
      case 'PERFORMANCE':
        console.log('   💡 Focus on optimizing workflow complexity and node efficiency.');
        break;
      case 'RELIABILITY':
        console.log('   💡 Focus on adding error handling and fallback mechanisms.');
        break;
      case 'DATA_QUALITY':
        console.log('   💡 Focus on data validation and cleaning processes.');
        break;
    }
  }
  
  // Fix effectiveness
  const totalIssuesFound = Object.values(report.issues.categories).reduce((sum, count) => sum + count, 0);
  const fixRate = totalIssuesFound > 0 ? (report.fixes.totalApplied / totalIssuesFound * 100).toFixed(2) : '100.00';
  console.log(`🔧 Fix effectiveness: ${fixRate}% of issues were automatically fixed`);
  
  if (parseFloat(fixRate) > 80) {
    console.log('   ✅ Excellent fix rate! The automated fixing system is highly effective.');
  } else if (parseFloat(fixRate) > 60) {
    console.log('   ⚠️ Good fix rate, but some issue types need better fix strategies.');
  } else {
    console.log('   🚨 Low fix rate indicates need for more comprehensive fix logic.');
  }
  
  // Learning insights
  const learningRate = report.learnings.unique / report.learnings.total;
  if (learningRate > 0.5) {
    console.log('📚 High learning diversity - discovering many unique patterns.');
  } else {
    console.log('📚 Learning patterns are converging - system is stabilizing.');
  }
  
  console.log('\n🎯 RECOMMENDATIONS:');
  console.log('1. Implement the most effective fixes as default validation rules');
  console.log('2. Create workflow templates based on successful patterns');
  console.log('3. Add monitoring for the top issue categories');
  console.log('4. Develop specialized validators for complex integrations');
  console.log('5. Create automated performance optimization suggestions');
}

// Run the tests
main().catch(console.error);