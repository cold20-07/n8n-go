#!/usr/bin/env node
/**
 * Comprehensive N8N Workflow Tester
 * Validates every detail of generated workflows including:
 * - Node types and configurations
 * - Parameter correctness
 * - Connection validity
 * - Goal achievement
 * - Production readiness
 */

const apiHandler = require('./api/index.js');

class WorkflowValidator {
  constructor() {
    this.validNodeTypes = {
      'n8n-nodes-base.webhook': { category: 'trigger', requiredParams: ['httpMethod'] },
      'n8n-nodes-base.scheduleTrigger': { category: 'trigger', requiredParams: ['rule'] },
      'n8n-nodes-base.httpRequest': { category: 'action', requiredParams: ['method', 'url'] },
      'n8n-nodes-base.slack': { category: 'action', requiredParams: ['channel', 'text'] },
      'n8n-nodes-base.gmail': { category: 'action', requiredParams: ['operation'] },
      'n8n-nodes-base.googleSheets': { category: 'action', requiredParams: ['operation'] },
      'n8n-nodes-base.trello': { category: 'action', requiredParams: ['operation'] },
      'n8n-nodes-base.shopify': { category: 'action', requiredParams: ['operation'] },
      'n8n-nodes-base.github': { category: 'action', requiredParams: ['operation'] },
      'n8n-nodes-base.code': { category: 'processing', requiredParams: ['jsCode'] },
      'n8n-nodes-base.if': { category: 'logic', requiredParams: ['conditions'] },
      'n8n-nodes-base.airtable': { category: 'action', requiredParams: ['operation'] },
      'n8n-nodes-base.notion': { category: 'action', requiredParams: ['operation'] },
      'n8n-nodes-base.telegram': { category: 'action', requiredParams: ['chatId', 'text'] },
      'n8n-nodes-base.openAi': { category: 'ai', requiredParams: ['operation'] },
      'n8n-nodes-base.stripe': { category: 'payment', requiredParams: ['operation'] },
      'n8n-nodes-base.googleAds': { category: 'marketing', requiredParams: ['operation'] },
      'n8n-nodes-base.discord': { category: 'communication', requiredParams: ['operation'] },
      'n8n-nodes-base.payPal': { category: 'payment', requiredParams: ['operation'] },
      'n8n-nodes-base.quickBooks': { category: 'accounting', requiredParams: ['operation'] },
      'n8n-nodes-base.mongoDb': { category: 'database', requiredParams: ['operation'] },
      'n8n-nodes-base.mySql': { category: 'database', requiredParams: ['operation'] },
      'n8n-nodes-base.dropbox': { category: 'storage', requiredParams: ['operation'] },
      'n8n-nodes-base.googleDrive': { category: 'storage', requiredParams: ['operation'] },
      'n8n-nodes-base.asana': { category: 'project', requiredParams: ['operation'] },
      'n8n-nodes-base.typeform': { category: 'forms', requiredParams: ['operation'] },
      'n8n-nodes-base.microsoftTeams': { category: 'communication', requiredParams: ['operation'] },
      'n8n-nodes-base.microsoftOneDrive': { category: 'storage', requiredParams: ['operation'] },
      'n8n-nodes-base.hubspot': { category: 'crm', requiredParams: ['operation'] },
      'n8n-nodes-base.instagram': { category: 'social', requiredParams: ['operation'] },
      'n8n-nodes-base.twitter': { category: 'social', requiredParams: ['operation'] },
      'n8n-nodes-base.youtube': { category: 'social', requiredParams: ['operation'] },
      'n8n-nodes-base.whatsApp': { category: 'communication', requiredParams: ['operation'] },
      'n8n-nodes-base.mailchimp': { category: 'email', requiredParams: ['operation'] },
      'n8n-nodes-base.wooCommerce': { category: 'ecommerce', requiredParams: ['operation'] }
    };

    this.serviceKeywords = {
      'slack': ['slack', 'message', 'notification', 'channel', 'alert'],
      'gmail': ['gmail', 'email', 'mail', 'send email'],
      'google_sheets': ['google sheets', 'google sheet', 'spreadsheet', 'sheet'],
      'trello': ['trello', 'card', 'board', 'task'],
      'shopify': ['shopify', 'order', 'product', 'store'],
      'github': ['github', 'repository', 'repo', 'issue', 'commit'],
      'api': ['api', 'endpoint', 'http', 'request', 'monitor'],
      'schedule': ['schedule', 'every', 'minutes', 'hours', 'daily', 'cron'],
      'webhook': ['webhook', 'trigger', 'incoming'],
      'telegram': ['telegram', 'message', 'chat'],
      'airtable': ['airtable', 'record', 'database'],
      'notion': ['notion', 'page', 'database'],
      'openai': ['openai', 'gpt', 'ai', 'generate'],
      'stripe': ['stripe', 'payment', 'charge'],
      'google_ads': ['google ads', 'ads', 'leads', 'campaign'],
      'discord': ['discord', 'server', 'channel'],
      'paypal': ['paypal', 'transaction', 'payment'],
      'quickbooks': ['quickbooks', 'invoice', 'accounting'],
      'mongodb': ['mongodb', 'database', 'collection'],
      'mysql': ['mysql', 'database', 'sql'],
      'dropbox': ['dropbox', 'backup', 'storage'],
      'google_drive': ['google drive', 'backup', 'storage'],
      'asana': ['asana', 'task', 'project'],
      'typeform': ['typeform', 'form', 'response'],
      'microsoft_teams': ['microsoft teams', 'teams'],
      'onedrive': ['onedrive', 'document'],
      'hubspot': ['hubspot', 'deals', 'crm'],
      'instagram': ['instagram', 'post', 'social'],
      'twitter': ['twitter', 'tweet', 'social'],
      'youtube': ['youtube', 'video', 'channel'],
      'whatsapp': ['whatsapp', 'message'],
      'mailchimp': ['mailchimp', 'email', 'audience'],
      'woocommerce': ['woocommerce', 'order', 'inventory']
    };
  }

  async validateWorkflow(testCase) {
    const results = {
      testCase: testCase.name || testCase.description.substring(0, 50) + '...',
      description: testCase.description,
      passed: false,
      score: 0,
      maxScore: 100,
      details: {
        nodeValidation: { passed: false, score: 0, issues: [] },
        connectionValidation: { passed: false, score: 0, issues: [] },
        parameterValidation: { passed: false, score: 0, issues: [] },
        goalAchievement: { passed: false, score: 0, issues: [] },
        productionReadiness: { passed: false, score: 0, issues: [] }
      }
    };

    try {
      // Generate workflow
      const workflow = await this.generateWorkflow(testCase);
      if (!workflow) {
        results.details.nodeValidation.issues.push('Failed to generate workflow');
        return results;
      }

      // Validate nodes (25 points)
      try {
        this.validateNodes(workflow, testCase, results.details.nodeValidation);
      } catch (error) {
        results.details.nodeValidation.issues.push(`Node validation error: ${error.message}`);
      }
      
      // Validate connections (25 points)
      try {
        this.validateConnections(workflow, results.details.connectionValidation);
      } catch (error) {
        results.details.connectionValidation.issues.push(`Connection validation error: ${error.message}`);
      }
      
      // Validate parameters (20 points)
      try {
        this.validateParameters(workflow, results.details.parameterValidation);
      } catch (error) {
        results.details.parameterValidation.issues.push(`Parameter validation error: ${error.message}`);
      }
      
      // Validate goal achievement (20 points)
      try {
        this.validateGoalAchievement(workflow, testCase, results.details.goalAchievement);
      } catch (error) {
        results.details.goalAchievement.issues.push(`Goal validation error: ${error.message}`);
      }
      
      // Validate production readiness (10 points)
      try {
        this.validateProductionReadiness(workflow, results.details.productionReadiness);
      } catch (error) {
        results.details.productionReadiness.issues.push(`Production validation error: ${error.message}`);
      }

      // Calculate total score
      results.score = Object.values(results.details).reduce((sum, detail) => sum + detail.score, 0);
      results.passed = results.score >= 70; // 70% threshold for passing

    } catch (error) {
      results.details.nodeValidation.issues.push(`Test error: ${error.message}`);
    }

    return results;
  }

  async generateWorkflow(testCase) {
    const mockReq = {
      method: 'POST',
      url: '/generate',
      body: JSON.stringify({
        description: testCase.description,
        triggerType: testCase.triggerType || 'webhook',
        complexity: testCase.complexity || 'medium'
      })
    };

    let responseData = null;
    const mockRes = {
      setHeader: () => {},
      status: (code) => mockRes,
      json: (data) => { responseData = data; return mockRes; },
      end: () => {}
    };

    await apiHandler(mockReq, mockRes);
    return responseData?.success ? responseData.workflow : null;
  }

  validateNodes(workflow, testCase, validation) {
    const maxScore = 25;
    let score = 0;
    const issues = [];

    // Check if workflow has nodes
    if (!workflow.nodes || workflow.nodes.length === 0) {
      issues.push('Workflow has no nodes');
      validation.score = 0;
      validation.issues = issues;
      validation.passed = false;
      return;
    }

    score += 5; // Basic node existence

    // Check node types are valid
    const invalidNodes = workflow.nodes.filter(node => !this.validNodeTypes[node.type]);
    if (invalidNodes.length > 0) {
      issues.push(`Invalid node types: ${invalidNodes.map(n => n.type).join(', ')}`);
    } else {
      score += 5; // Valid node types
    }

    // Check for trigger node
    const triggerNodes = workflow.nodes.filter(node => 
      this.validNodeTypes[node.type]?.category === 'trigger'
    );
    if (triggerNodes.length === 0) {
      issues.push('No trigger node found');
    } else if (triggerNodes.length > 1) {
      issues.push('Multiple trigger nodes found');
    } else {
      score += 5; // Proper trigger
    }

    // Check for action nodes
    const actionNodes = workflow.nodes.filter(node => 
      ['action', 'processing', 'logic', 'ai', 'payment'].includes(this.validNodeTypes[node.type]?.category)
    );
    if (actionNodes.length === 0) {
      issues.push('No action nodes found');
    } else {
      score += 5; // Has action nodes
    }

    // Check service relevance
    const detectedServices = this.detectServicesInDescription(testCase.description);
    const workflowServices = this.extractServicesFromWorkflow(workflow);
    
    const relevantServices = detectedServices.filter(service => 
      workflowServices.some(ws => ws && typeof ws === 'string' && ws.includes(service))
    );

    if (relevantServices.length === 0) {
      issues.push('No relevant services detected in workflow');
    } else if (relevantServices.length === detectedServices.length) {
      score += 5; // All services represented
    } else {
      score += 3; // Some services represented
      issues.push(`Missing services: ${detectedServices.filter(s => !relevantServices.includes(s)).join(', ')}`);
    }

    validation.score = score;
    validation.issues = issues;
    validation.passed = score >= 15; // 60% of max score
  }

  validateConnections(workflow, validation) {
    const maxScore = 25;
    let score = 0;
    const issues = [];

    if (!workflow.connections || Object.keys(workflow.connections).length === 0) {
      issues.push('No connections found');
      validation.score = 0;
      validation.issues = issues;
      validation.passed = false;
      return;
    }

    score += 5; // Basic connections exist

    // Check connection structure
    const nodeNames = workflow.nodes.map(n => n.name);
    let validConnections = 0;
    let totalConnections = 0;

    for (const [sourceName, connections] of Object.entries(workflow.connections)) {
      if (!nodeNames.includes(sourceName)) {
        issues.push(`Connection source '${sourceName}' not found in nodes`);
        continue;
      }

      if (!connections.main || !Array.isArray(connections.main)) {
        issues.push(`Invalid connection structure for '${sourceName}'`);
        continue;
      }

      for (const connectionGroup of connections.main) {
        if (!Array.isArray(connectionGroup)) {
          issues.push(`Invalid connection group for '${sourceName}'`);
          continue;
        }

        for (const connection of connectionGroup) {
          totalConnections++;
          if (!connection.node || !nodeNames.includes(connection.node)) {
            issues.push(`Connection target '${connection.node}' not found in nodes`);
          } else if (connection.type !== 'main' || typeof connection.index !== 'number') {
            issues.push(`Invalid connection format for '${sourceName}' -> '${connection.node}'`);
          } else {
            validConnections++;
          }
        }
      }
    }

    if (totalConnections === 0) {
      issues.push('No connection details found');
    } else {
      const connectionRatio = validConnections / totalConnections;
      score += Math.round(connectionRatio * 10); // Up to 10 points for connection validity
    }

    // Check workflow continuity
    const triggerNodes = workflow.nodes.filter(node => 
      this.validNodeTypes[node.type]?.category === 'trigger'
    );

    if (triggerNodes.length > 0) {
      const reachableNodes = this.findReachableNodes(workflow, triggerNodes[0].name);
      const reachabilityRatio = reachableNodes.size / workflow.nodes.length;
      
      if (reachabilityRatio < 0.5) {
        issues.push('Many nodes are not reachable from trigger');
      } else if (reachabilityRatio === 1) {
        score += 10; // Perfect reachability
      } else {
        score += Math.round(reachabilityRatio * 10);
      }
    }

    validation.score = Math.min(score, maxScore);
    validation.issues = issues;
    validation.passed = score >= 15; // 60% of max score
  }

  validateParameters(workflow, validation) {
    const maxScore = 20;
    let score = 0;
    const issues = [];

    let validParameterNodes = 0;
    let totalNodes = workflow.nodes.length;

    for (const node of workflow.nodes) {
      const nodeTypeInfo = this.validNodeTypes[node.type];
      if (!nodeTypeInfo) continue;

      const requiredParams = nodeTypeInfo.requiredParams || [];
      let nodeScore = 0;

      // Check if node has parameters
      if (!node.parameters) {
        issues.push(`Node '${node.name}' missing parameters`);
        continue;
      }

      // Check required parameters
      const missingParams = requiredParams.filter(param => 
        !(param in node.parameters) || 
        node.parameters[param] === null || 
        node.parameters[param] === undefined ||
        (typeof node.parameters[param] === 'string' && node.parameters[param].trim() === '')
      );

      if (missingParams.length === 0) {
        nodeScore = 1;
        validParameterNodes++;
      } else {
        issues.push(`Node '${node.name}' missing required parameters: ${missingParams.join(', ')}`);
      }

      // Check parameter quality for specific node types
      if (node.type === 'n8n-nodes-base.httpRequest') {
        if (node.parameters.url && node.parameters.url.startsWith('http')) {
          nodeScore += 0.5;
        } else {
          issues.push(`Node '${node.name}' has invalid URL`);
        }
      }

      if (node.type === 'n8n-nodes-base.code') {
        if (node.parameters.jsCode && node.parameters.jsCode.length > 50) {
          nodeScore += 0.5;
        } else {
          issues.push(`Node '${node.name}' has insufficient code`);
        }
      }

      if (node.type === 'n8n-nodes-base.slack') {
        if (node.parameters.channel && node.parameters.text) {
          nodeScore += 0.5;
        } else {
          issues.push(`Node '${node.name}' missing Slack channel or text`);
        }
      }
    }

    if (totalNodes > 0) {
      score = Math.round((validParameterNodes / totalNodes) * maxScore);
    }

    validation.score = score;
    validation.issues = issues;
    validation.passed = score >= 12; // 60% of max score
  }

  validateGoalAchievement(workflow, testCase, validation) {
    const maxScore = 20;
    let score = 0;
    const issues = [];

    const description = testCase.description.toLowerCase();
    const workflowServices = this.extractServicesFromWorkflow(workflow);
    const nodeNames = workflow.nodes.map(n => n.name.toLowerCase());

    // Check if workflow addresses the main goal
    let goalKeywords = [];
    
    // Extract action keywords from description
    if (description.includes('send') || description.includes('notify')) {
      goalKeywords.push('send', 'notify', 'message');
    }
    if (description.includes('create') || description.includes('add')) {
      goalKeywords.push('create', 'add');
    }
    if (description.includes('monitor') || description.includes('check')) {
      goalKeywords.push('monitor', 'check', 'api', 'endpoint');
    }
    if (description.includes('process') || description.includes('transform')) {
      goalKeywords.push('process', 'transform');
    }
    if (description.includes('backup') || description.includes('sync')) {
      goalKeywords.push('backup', 'sync');
    }

    // Check if workflow nodes reflect the goals
    const goalReflection = goalKeywords.some(keyword => 
      nodeNames.some(name => name.includes(keyword)) ||
      workflowServices.some(service => service.includes(keyword))
    );

    if (goalReflection) {
      score += 10;
    } else {
      issues.push('Workflow does not reflect the stated goals');
    }

    // Check for logical workflow sequence
    const hasLogicalSequence = this.checkLogicalSequence(workflow, description);
    if (hasLogicalSequence) {
      score += 5;
    } else {
      issues.push('Workflow sequence does not follow logical order');
    }

    // Check for completeness
    const detectedServices = this.detectServicesInDescription(description);
    const servicesCovered = detectedServices.filter(service => 
      workflowServices.some(ws => ws && typeof ws === 'string' && ws.includes(service))
    );

    if (servicesCovered.length === detectedServices.length) {
      score += 5;
    } else if (servicesCovered.length > 0) {
      score += 3;
      issues.push(`Incomplete service coverage: missing ${detectedServices.filter(s => !servicesCovered.includes(s)).join(', ')}`);
    } else {
      issues.push('No relevant services implemented');
    }

    validation.score = score;
    validation.issues = issues;
    validation.passed = score >= 12; // 60% of max score
  }

  validateProductionReadiness(workflow, validation) {
    const maxScore = 10;
    let score = 0;
    const issues = [];

    // Check for error handling
    const hasErrorHandling = workflow.nodes.some(node => 
      (node.name && node.name.toLowerCase().includes('error')) ||
      (node.name && node.name.toLowerCase().includes('log')) ||
      (node.type === 'n8n-nodes-base.code' && 
       node.parameters && node.parameters.jsCode && 
       (node.parameters.jsCode.includes('try') || 
        node.parameters.jsCode.includes('catch')))
    );

    if (hasErrorHandling) {
      score += 3;
    } else {
      issues.push('No error handling detected');
    }

    // Check for proper node IDs
    const hasValidIds = workflow.nodes.every(node => 
      node.id && typeof node.id === 'string' && node.id.length > 0
    );

    if (hasValidIds) {
      score += 2;
    } else {
      issues.push('Invalid or missing node IDs');
    }

    // Check for proper positioning
    const hasValidPositions = workflow.nodes.every(node => 
      node.position && Array.isArray(node.position) && 
      node.position.length === 2 && 
      typeof node.position[0] === 'number' && 
      typeof node.position[1] === 'number'
    );

    if (hasValidPositions) {
      score += 2;
    } else {
      issues.push('Invalid node positions');
    }

    // Check workflow metadata
    if (workflow.settings && workflow.tags && workflow.meta) {
      score += 2;
    } else {
      issues.push('Missing workflow metadata');
    }

    // Check for reasonable complexity
    if (workflow.nodes.length >= 2 && workflow.nodes.length <= 20) {
      score += 1;
    } else {
      issues.push('Workflow complexity outside reasonable range');
    }

    validation.score = score;
    validation.issues = issues;
    validation.passed = score >= 6; // 60% of max score
  }

  // Helper methods
  detectServicesInDescription(description) {
    const desc = description.toLowerCase();
    const services = [];
    
    for (const [service, keywords] of Object.entries(this.serviceKeywords)) {
      if (keywords.some(keyword => desc.includes(keyword))) {
        services.push(service);
      }
    }
    
    return services;
  }

  extractServicesFromWorkflow(workflow) {
    const services = [];
    
    for (const node of workflow.nodes) {
      services.push(node.type.toLowerCase());
      services.push(node.name.toLowerCase());
    }
    
    if (workflow.meta && workflow.meta.services_detected) {
      services.push(...workflow.meta.services_detected.map(s => s.toLowerCase()));
    }
    
    return services;
  }

  findReachableNodes(workflow, startNode) {
    const reachable = new Set([startNode]);
    const queue = [startNode];
    
    while (queue.length > 0) {
      const current = queue.shift();
      const connections = workflow.connections[current];
      
      if (connections && connections.main) {
        for (const connectionGroup of connections.main) {
          for (const connection of connectionGroup) {
            if (!reachable.has(connection.node)) {
              reachable.add(connection.node);
              queue.push(connection.node);
            }
          }
        }
      }
    }
    
    return reachable;
  }

  checkLogicalSequence(workflow, description) {
    // Simple heuristic: trigger should come first, actions should follow
    const triggerNodes = workflow.nodes.filter(node => 
      this.validNodeTypes[node.type]?.category === 'trigger'
    );
    
    if (triggerNodes.length === 0) return false;
    
    // Check if trigger has the earliest position
    const triggerNode = triggerNodes[0];
    const earliestX = Math.min(...workflow.nodes.map(n => n.position[0]));
    
    return triggerNode.position[0] === earliestX;
  }

  // Main testing method
  async runComprehensiveTest(testCases) {
    console.log('🔍 Comprehensive N8N Workflow Validation');
    console.log('Testing every detail: nodes, connections, parameters, goals, production readiness');
    console.log('='.repeat(80));
    
    const results = [];
    let totalScore = 0;
    let passedTests = 0;
    
    for (let i = 0; i < testCases.length; i++) {
      const testCase = testCases[i];
      console.log(`\n🧪 Test ${i + 1}/${testCases.length}: ${testCase.name || 'Unnamed Test'}`);
      console.log(`📝 Description: ${testCase.description}`);
      
      const result = await this.validateWorkflow(testCase);
      results.push(result);
      
      totalScore += result.score;
      if (result.passed) passedTests++;
      
      // Display results
      console.log(`   ${result.passed ? '✅' : '❌'} Overall: ${result.passed ? 'PASSED' : 'FAILED'} (${result.score}/${result.maxScore})`);
      
      // Detailed breakdown
      for (const [category, details] of Object.entries(result.details)) {
        const status = details.passed ? '✅' : '❌';
        console.log(`   ${status} ${category}: ${details.score} points`);
        
        if (details.issues.length > 0) {
          details.issues.forEach(issue => {
            console.log(`      - ${issue}`);
          });
        }
      }
    }
    
    // Summary
    console.log(`\n📊 COMPREHENSIVE TEST RESULTS`);
    console.log('='.repeat(50));
    console.log(`Tests Passed: ${passedTests}/${testCases.length} (${Math.round((passedTests/testCases.length) * 100)}%)`);
    console.log(`Average Score: ${Math.round(totalScore/testCases.length)}/100`);
    console.log(`Total Score: ${totalScore}/${testCases.length * 100}`);
    
    if (passedTests === testCases.length) {
      console.log('\n🎉 ALL TESTS PASSED! Workflow generator is production ready.');
    } else {
      console.log(`\n⚠️ ${testCases.length - passedTests} tests failed. Review issues above.`);
    }
    
    return {
      results,
      summary: {
        totalTests: testCases.length,
        passedTests,
        averageScore: Math.round(totalScore/testCases.length),
        totalScore,
        maxPossibleScore: testCases.length * 100
      }
    };
  }
}

// Export for use
module.exports = { WorkflowValidator };

// CLI usage
if (require.main === module) {
  const validator = new WorkflowValidator();
  
  // Sample test cases for demonstration
  const sampleTests = [
    {
      name: "API Monitoring Test",
      description: "Monitor an API endpoint every 10 minutes and send a Slack alert if response time exceeds 2 seconds",
      triggerType: "schedule",
      complexity: "complex"
    },
    {
      name: "Simple Slack Notification",
      description: "Send a Slack message when a new lead is added to Google Sheets",
      triggerType: "webhook",
      complexity: "medium"
    }
  ];
  
  validator.runComprehensiveTest(sampleTests).then(results => {
    process.exit(results.summary.passedTests === results.summary.totalTests ? 0 : 1);
  }).catch(error => {
    console.error('Test runner error:', error);
    process.exit(1);
  });
}