#!/usr/bin/env node
/**
 * Production-Level N8N Automation Readiness Test
 * Tests complex real-world scenarios for enterprise use
 */

const productionTestCases = [
  // Enterprise Business Automation
  {
    category: "Enterprise Business",
    description: "Create a comprehensive lead management system that captures leads from multiple sources (Google Forms, website contact forms, LinkedIn), validates and enriches the data using AI, scores leads based on predefined criteria, assigns them to appropriate sales reps in HubSpot, sends personalized welcome emails via Gmail, creates follow-up tasks in Asana, and logs all activities in Google Sheets for reporting.",
    complexity: "complex",
    expectedFeatures: ["multi-trigger", "ai-processing", "lead-scoring", "crm-integration", "email-automation", "task-management", "reporting"]
  },
  
  // Advanced E-commerce Automation
  {
    category: "E-commerce Advanced",
    description: "Build a sophisticated order fulfillment workflow that monitors Shopify for new orders, validates inventory levels across multiple warehouses, calculates optimal shipping routes, generates shipping labels via ShipStation API, sends order confirmations with tracking info to customers via email and SMS, updates inventory in real-time, handles backorders by notifying suppliers, processes refunds automatically for cancelled orders, and generates daily sales analytics reports.",
    complexity: "complex",
    expectedFeatures: ["order-processing", "inventory-management", "shipping-automation", "customer-communication", "analytics", "supplier-integration"]
  },
  
  // AI-Powered Content Management
  {
    category: "AI Content Management",
    description: "Develop an intelligent content creation and distribution system that monitors trending topics from multiple sources (Google Trends, Twitter API, Reddit), generates relevant blog post ideas using GPT-4, creates draft content with proper SEO optimization, schedules posts across multiple social media platforms (Twitter, LinkedIn, Facebook), monitors engagement metrics, automatically responds to comments using AI, and generates weekly performance reports with actionable insights.",
    complexity: "complex",
    expectedFeatures: ["trend-monitoring", "ai-content-generation", "seo-optimization", "multi-platform-posting", "engagement-tracking", "automated-responses", "analytics"]
  },
  
  // Financial Operations Automation
  {
    category: "Financial Operations",
    description: "Create a comprehensive financial management workflow that processes invoices from multiple sources (email attachments, cloud storage), extracts data using OCR, validates against purchase orders, routes for approval based on amount thresholds, integrates with QuickBooks for accounting, sends payment reminders for overdue invoices, reconciles bank statements automatically, generates monthly financial reports, and alerts management of cash flow issues.",
    complexity: "complex",
    expectedFeatures: ["document-processing", "ocr-integration", "approval-workflows", "accounting-integration", "payment-tracking", "reconciliation", "financial-reporting"]
  },
  
  // Customer Support Automation
  {
    category: "Customer Support",
    description: "Build an advanced customer support system that monitors support channels (email, chat, social media), categorizes tickets using AI sentiment analysis, routes urgent issues to senior agents, creates knowledge base articles from resolved tickets, sends automated responses for common queries, escalates unresolved tickets after SLA timeouts, tracks customer satisfaction scores, and generates support performance dashboards.",
    complexity: "complex",
    expectedFeatures: ["multi-channel-monitoring", "ai-categorization", "intelligent-routing", "knowledge-management", "sla-tracking", "satisfaction-monitoring", "performance-dashboards"]
  },
  
  // DevOps and Monitoring
  {
    category: "DevOps Monitoring",
    description: "Implement a comprehensive DevOps monitoring and incident response workflow that monitors application health across multiple environments, detects anomalies using machine learning, automatically scales resources based on load, creates incident tickets in Jira for critical issues, notifies on-call engineers via PagerDuty, runs automated diagnostics, deploys hotfixes for known issues, and generates post-incident reports with root cause analysis.",
    complexity: "complex",
    expectedFeatures: ["health-monitoring", "anomaly-detection", "auto-scaling", "incident-management", "automated-diagnostics", "deployment-automation", "reporting"]
  },
  
  // Marketing Campaign Automation
  {
    category: "Marketing Automation",
    description: "Create a sophisticated marketing campaign management system that segments customers based on behavior and demographics, personalizes email campaigns using AI, A/B tests subject lines and content, tracks campaign performance across channels, automatically adjusts budgets based on ROI, retargets website visitors with personalized ads, nurtures leads through multi-touch sequences, and provides real-time campaign analytics with predictive insights.",
    complexity: "complex",
    expectedFeatures: ["customer-segmentation", "personalization", "ab-testing", "performance-tracking", "budget-optimization", "retargeting", "lead-nurturing", "predictive-analytics"]
  },
  
  // Supply Chain Management
  {
    category: "Supply Chain",
    description: "Develop a comprehensive supply chain automation that monitors inventory levels across multiple locations, predicts demand using historical data and AI, automatically generates purchase orders when stock is low, tracks shipments from suppliers, manages quality control processes, handles returns and exchanges, optimizes warehouse operations, and provides real-time supply chain visibility with exception alerts.",
    complexity: "complex",
    expectedFeatures: ["inventory-monitoring", "demand-forecasting", "automated-purchasing", "shipment-tracking", "quality-control", "returns-management", "warehouse-optimization", "visibility-dashboards"]
  }
];

// Import the API handler
const apiHandler = require('./api/index.js');

async function testProductionScenario(testCase) {
  console.log(`\n🏭 Testing Production Scenario: ${testCase.category}`);
  console.log(`📋 Description: ${testCase.description.substring(0, 100)}...`);
  console.log(`🎯 Expected Features: ${testCase.expectedFeatures.join(', ')}`);
  
  try {
    // Simulate API request
    const mockReq = {
      method: 'POST',
      url: '/generate',
      body: JSON.stringify({
        description: testCase.description,
        triggerType: 'webhook',
        complexity: testCase.complexity
      })
    };
    
    let response = null;
    const mockRes = {
      setHeader: () => {},
      status: (code) => ({
        json: (data) => {
          response = { statusCode: code, data };
          return response;
        }
      })
    };
    
    await apiHandler(mockReq, mockRes);
    
    if (response && response.statusCode === 200 && response.data.success) {
      const workflow = response.data.workflow;
      const analysis = response.data.analysis;
      
      // Production-level validation
      const productionChecks = {
        hasMultipleNodes: workflow.nodes.length >= 5,
        hasProperConnections: Object.keys(workflow.connections).length >= 3,
        hasErrorHandling: analysis.has_error_handling,
        hasValidation: analysis.has_validation,
        hasProperSettings: workflow.settings && workflow.settings.executionOrder,
        hasMetadata: workflow.meta && workflow.meta.services_detected,
        hasComplexity: workflow.tags && workflow.tags.includes('complex'),
        hasProperNodeTypes: workflow.nodes.every(node => node.type && node.type.startsWith('n8n-nodes-')),
        hasUniqueIds: new Set(workflow.nodes.map(n => n.id)).size === workflow.nodes.length,
        hasProperPositioning: workflow.nodes.every(node => node.position && Array.isArray(node.position))
      };
      
      const productionScore = Object.values(productionChecks).filter(Boolean).length;
      const maxScore = Object.keys(productionChecks).length;
      const productionPercentage = Math.round((productionScore / maxScore) * 100);
      
      // Service detection analysis
      const detectedServices = response.data.services_detected || [];
      const serviceCategories = {
        communication: ['slack', 'telegram', 'whatsapp', 'microsoft_teams'],
        productivity: ['google_sheets', 'notion', 'airtable', 'asana', 'trello'],
        ai: ['openai'],
        ecommerce: ['shopify', 'stripe', 'woocommerce'],
        development: ['github'],
        storage: ['google_drive', 'dropbox', 'onedrive'],
        email: ['gmail', 'mailchimp'],
        social: ['twitter', 'instagram', 'youtube']
      };
      
      const categoriesDetected = Object.keys(serviceCategories).filter(category =>
        serviceCategories[category].some(service => detectedServices.includes(service))
      );
      
      console.log(`   ✅ Generation: SUCCESS`);
      console.log(`   📊 Production Score: ${productionScore}/${maxScore} (${productionPercentage}%)`);
      console.log(`   🏗️ Nodes Generated: ${workflow.nodes.length}`);
      console.log(`   🔗 Connections: ${Object.keys(workflow.connections).length}`);
      console.log(`   🎯 Services Detected: ${detectedServices.length} (${detectedServices.join(', ')})`);
      console.log(`   📂 Service Categories: ${categoriesDetected.join(', ')}`);
      console.log(`   🛡️ Error Handling: ${analysis.has_error_handling ? 'YES' : 'NO'}`);
      console.log(`   ✅ Input Validation: ${analysis.has_validation ? 'YES' : 'NO'}`);
      
      // Production readiness assessment
      const isProductionReady = productionPercentage >= 80 && 
                               workflow.nodes.length >= 4 && 
                               detectedServices.length >= 2 &&
                               analysis.has_error_handling;
      
      console.log(`   🏭 Production Ready: ${isProductionReady ? '✅ YES' : '❌ NO'}`);
      
      if (!isProductionReady) {
        console.log(`   ⚠️ Issues:`);
        if (productionPercentage < 80) console.log(`      - Low production score (${productionPercentage}%)`);
        if (workflow.nodes.length < 4) console.log(`      - Too few nodes (${workflow.nodes.length})`);
        if (detectedServices.length < 2) console.log(`      - Limited service integration (${detectedServices.length})`);
        if (!analysis.has_error_handling) console.log(`      - Missing error handling`);
      }
      
      return {
        success: true,
        productionReady: isProductionReady,
        productionScore: productionPercentage,
        nodeCount: workflow.nodes.length,
        serviceCount: detectedServices.length,
        hasErrorHandling: analysis.has_error_handling,
        hasValidation: analysis.has_validation,
        testCase
      };
      
    } else {
      console.log(`   ❌ Generation: FAILED`);
      if (response?.data?.error) {
        console.log(`   Error: ${response.data.error}`);
      }
      return {
        success: false,
        productionReady: false,
        error: response?.data?.error || 'Unknown error',
        testCase
      };
    }
    
  } catch (error) {
    console.log(`   ❌ Error: ${error.message}`);
    return {
      success: false,
      productionReady: false,
      error: error.message,
      testCase
    };
  }
}

async function runProductionReadinessTest() {
  console.log('🏭 N8N Workflow Generator - Production Readiness Assessment');
  console.log('=' * 70);
  console.log('Testing complex enterprise-level automation scenarios...\n');
  
  const results = [];
  let successCount = 0;
  let productionReadyCount = 0;
  
  for (const testCase of productionTestCases) {
    const result = await testProductionScenario(testCase);
    results.push(result);
    
    if (result.success) {
      successCount++;
      if (result.productionReady) {
        productionReadyCount++;
      }
    }
    
    // Small delay between tests
    await new Promise(resolve => setTimeout(resolve, 200));
  }
  
  // Comprehensive Analysis
  console.log('\n' + '=' * 70);
  console.log('📊 PRODUCTION READINESS ASSESSMENT RESULTS');
  console.log('=' * 70);
  
  const totalTests = productionTestCases.length;
  const successRate = Math.round((successCount / totalTests) * 100);
  const productionReadyRate = Math.round((productionReadyCount / totalTests) * 100);
  
  console.log(`\n📈 Overall Performance:`);
  console.log(`   Generation Success: ${successCount}/${totalTests} (${successRate}%)`);
  console.log(`   Production Ready: ${productionReadyCount}/${totalTests} (${productionReadyRate}%)`);
  
  // Calculate average scores
  const successfulResults = results.filter(r => r.success);
  if (successfulResults.length > 0) {
    const avgProductionScore = Math.round(
      successfulResults.reduce((sum, r) => sum + r.productionScore, 0) / successfulResults.length
    );
    const avgNodeCount = Math.round(
      successfulResults.reduce((sum, r) => sum + r.nodeCount, 0) / successfulResults.length
    );
    const avgServiceCount = Math.round(
      successfulResults.reduce((sum, r) => sum + r.serviceCount, 0) / successfulResults.length
    );
    
    console.log(`\n📊 Quality Metrics:`);
    console.log(`   Average Production Score: ${avgProductionScore}%`);
    console.log(`   Average Node Count: ${avgNodeCount}`);
    console.log(`   Average Service Integration: ${avgServiceCount} services`);
    console.log(`   Error Handling Coverage: ${successfulResults.filter(r => r.hasErrorHandling).length}/${successfulResults.length}`);
    console.log(`   Input Validation Coverage: ${successfulResults.filter(r => r.hasValidation).length}/${successfulResults.length}`);
  }
  
  // Category breakdown
  const categoryResults = {};
  results.forEach(result => {
    const category = result.testCase.category;
    if (!categoryResults[category]) {
      categoryResults[category] = { total: 0, productionReady: 0, avgScore: 0 };
    }
    categoryResults[category].total++;
    if (result.productionReady) {
      categoryResults[category].productionReady++;
    }
    if (result.success) {
      categoryResults[category].avgScore += result.productionScore || 0;
    }
  });
  
  console.log(`\n📋 Results by Category:`);
  for (const [category, stats] of Object.entries(categoryResults)) {
    const readyRate = Math.round((stats.productionReady / stats.total) * 100);
    const avgScore = Math.round(stats.avgScore / stats.total);
    const status = readyRate >= 80 ? '🟢' : readyRate >= 60 ? '🟡' : '🔴';
    console.log(`   ${status} ${category}: ${stats.productionReady}/${stats.total} ready (${readyRate}%, avg score: ${avgScore}%)`);
  }
  
  // Production readiness verdict
  console.log(`\n🏭 PRODUCTION READINESS VERDICT:`);
  
  if (productionReadyRate >= 90) {
    console.log(`🟢 EXCELLENT - Ready for Enterprise Production`);
    console.log(`   ✅ Generates complex, multi-service workflows`);
    console.log(`   ✅ Includes proper error handling and validation`);
    console.log(`   ✅ Suitable for mission-critical business automation`);
  } else if (productionReadyRate >= 75) {
    console.log(`🟡 GOOD - Ready for Production with Monitoring`);
    console.log(`   ✅ Generates solid workflows for most use cases`);
    console.log(`   ⚠️ May need manual review for complex scenarios`);
    console.log(`   ✅ Suitable for standard business automation`);
  } else if (productionReadyRate >= 50) {
    console.log(`🟡 FAIR - Ready for Development/Testing`);
    console.log(`   ⚠️ Generates basic workflows but lacks complexity`);
    console.log(`   ⚠️ Requires significant manual enhancement`);
    console.log(`   ✅ Good for prototyping and simple automation`);
  } else {
    console.log(`🔴 NEEDS IMPROVEMENT - Not Ready for Production`);
    console.log(`   ❌ Limited workflow complexity and features`);
    console.log(`   ❌ Missing critical production requirements`);
    console.log(`   ❌ Requires major enhancements before deployment`);
  }
  
  // Recommendations
  console.log(`\n💡 Recommendations:`);
  if (productionReadyRate >= 75) {
    console.log(`   🚀 Deploy to production with confidence`);
    console.log(`   📊 Monitor workflow performance and user feedback`);
    console.log(`   🔄 Iterate based on real-world usage patterns`);
  } else {
    console.log(`   🔧 Enhance error handling and validation systems`);
    console.log(`   📈 Improve service detection and integration`);
    console.log(`   🧪 Add more comprehensive testing scenarios`);
  }
  
  return {
    totalTests,
    successCount,
    productionReadyCount,
    successRate,
    productionReadyRate,
    categoryResults,
    verdict: productionReadyRate >= 75 ? 'PRODUCTION_READY' : 'NEEDS_IMPROVEMENT'
  };
}

// Run the production readiness test
if (require.main === module) {
  runProductionReadinessTest().then(results => {
    const exitCode = results.verdict === 'PRODUCTION_READY' ? 0 : 1;
    console.log(`\n🎯 Final Assessment: ${results.verdict}`);
    process.exit(exitCode);
  }).catch(error => {
    console.error('Production readiness test failed:', error);
    process.exit(1);
  });
}

module.exports = { productionTestCases, testProductionScenario, runProductionReadinessTest };