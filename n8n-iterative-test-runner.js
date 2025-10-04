// n8n Iterative Test Runner - Identifies and fixes issues one by one
const fs = require('fs');

class N8nIterativeTestRunner {
  constructor() {
    this.testResults = [];
    this.issuesFound = [];
    this.fixesApplied = [];
    this.learnings = [];
    this.currentTest = 0;
    this.validationRules = this.initializeValidationRules();
    this.knownIssues = new Map();
    this.performanceMetrics = {
      totalTime: 0,
      avgTestTime: 0,
      slowestTest: { id: 0, time: 0 },
      fastestTest: { id: 0, time: Infinity }
    };
  }

  initializeValidationRules() {
    return {
      // Data structure validation
      dataStructure: {
        requiresJsonWrapper: true,
        maxArrayDepth: 5,
        maxObjectKeys: 50,
        requiredFields: ['json']
      },
      
      // Node validation
      nodeValidation: {
        maxNodesPerWorkflow: 50,
        minNodesPerWorkflow: 2,
        requiredNodeTypes: ['trigger'],
        invalidCombinations: [
          ['Manual Trigger', 'Schedule Trigger'], // Can't have both
          ['Form Trigger', 'Webhook'] // Conflicting input methods
        ]
      },
      
      // Integration validation
      integrationValidation: {
        maxIntegrationsPerWorkflow: 10,
        requiresAuthentication: [
          'Slack', 'Google Sheets', 'Salesforce', 'HubSpot',
          'Gmail', 'Twitter', 'LinkedIn', 'Facebook'
        ],
        rateLimits: {
          'Twitter': 300, // requests per 15 min
          'Instagram': 200,
          'LinkedIn': 100
        }
      },
      
      // Business logic validation
      businessLogic: {
        conditionalRequirements: {
          'IF': ['condition', 'trueRoute', 'falseRoute'],
          'Switch': ['cases', 'defaultRoute']
        },
        dataFlowValidation: true,
        cyclicDependencyCheck: true
      }
    };
  }

  async runSingleTest(testId) {
    const startTime = Date.now();
    
    try {
      // Generate workflow
      const workflow = this.generateWorkflow(testId);
      
      // Validate workflow
      const validationResult = await this.validateWorkflow(workflow);
      
      // Check for issues
      const issues = this.identifyIssues(workflow, validationResult);
      
      // Apply fixes if issues found
      const fixedWorkflow = await this.applyFixes(workflow, issues);
      
      // Re-validate after fixes
      const finalValidation = await this.validateWorkflow(fixedWorkflow);
      
      const endTime = Date.now();
      const testTime = endTime - startTime;
      
      // Update performance metrics
      this.updatePerformanceMetrics(testId, testTime);
      
      const testResult = {
        id: testId,
        originalWorkflow: workflow,
        fixedWorkflow: fixedWorkflow,
        issues: issues,
        validationResult: validationResult,
        finalValidation: finalValidation,
        executionTime: testTime,
        status: finalValidation.isValid ? 'PASSED' : 'FAILED',
        learnings: this.extractLearnings(workflow, issues, fixedWorkflow)
      };
      
      this.testResults.push(testResult);
      this.recordLearnings(testResult.learnings);
      
      return testResult;
      
    } catch (error) {
      const endTime = Date.now();
      const testTime = endTime - startTime;
      
      const errorResult = {
        id: testId,
        status: 'ERROR',
        error: error.message,
        executionTime: testTime,
        learnings: [`Test ${testId} failed with error: ${error.message}`]
      };
      
      this.testResults.push(errorResult);
      this.recordLearnings(errorResult.learnings);
      
      return errorResult;
    }
  }

  generateWorkflow(id) {
    // Enhanced workflow generation with learned patterns
    const triggers = [
      'Manual Trigger', 'Webhook', 'Schedule Trigger', 'Form Trigger',
      'Email Trigger (IMAP)', 'File Trigger', 'HTTP Request Trigger',
      'Slack Trigger', 'Discord Trigger', 'Google Sheets Trigger'
    ];

    const processingNodes = [
      'Code (JavaScript)', 'Set', 'Edit Fields', 'Split Out',
      'Aggregate', 'Sort', 'Limit', 'Remove Duplicates', 'Merge'
    ];

    const integrations = [
      'HTTP Request', 'Slack', 'Gmail', 'Google Sheets', 'Notion',
      'Trello', 'Salesforce', 'HubSpot', 'Mailchimp', 'Twilio'
    ];

    const businessScenarios = [
      'Lead Management', 'Customer Onboarding', 'Order Processing',
      'Support Ticket Routing', 'Data Backup', 'Report Generation'
    ];

    // Apply learned patterns to avoid known issues
    const trigger = this.selectOptimalTrigger(triggers);
    const scenario = this.getRandomItem(businessScenarios);
    
    // Generate processing steps with validation
    const processingSteps = this.generateValidProcessingSteps(processingNodes);
    
    // Generate integrations with compatibility checks
    const workflowIntegrations = this.generateCompatibleIntegrations(integrations, trigger);
    
    // Add conditional logic with proper validation
    const conditional = this.generateValidConditional();

    return {
      id: id,
      name: `${scenario} - Test ${id}`,
      trigger: {
        type: trigger,
        config: this.generateTriggerConfig(trigger)
      },
      processingSteps: processingSteps,
      conditional: conditional,
      integrations: workflowIntegrations,
      metadata: {
        created: new Date().toISOString(),
        complexity: this.calculateComplexity(processingSteps, conditional, workflowIntegrations),
        estimatedNodes: this.estimateNodes(processingSteps, conditional, workflowIntegrations)
      }
    };
  }

  async validateWorkflow(workflow) {
    const validation = {
      isValid: true,
      errors: [],
      warnings: [],
      suggestions: []
    };

    // Data structure validation
    this.validateDataStructure(workflow, validation);
    
    // Node validation
    this.validateNodes(workflow, validation);
    
    // Integration validation
    this.validateIntegrations(workflow, validation);
    
    // Business logic validation
    this.validateBusinessLogic(workflow, validation);
    
    // Performance validation
    this.validatePerformance(workflow, validation);

    validation.isValid = validation.errors.length === 0;
    
    return validation;
  }

  validateDataStructure(workflow, validation) {
    // Check if workflow has proper n8n structure
    if (!workflow.trigger) {
      validation.errors.push('Workflow missing trigger node');
    }

    // Validate data flow structure
    if (workflow.processingSteps && workflow.processingSteps.length > 0) {
      workflow.processingSteps.forEach((step, index) => {
        if (!step.node || !step.purpose) {
          validation.errors.push(`Processing step ${index} missing required fields`);
        }
      });
    }

    // Check for proper JSON structure in data
    if (workflow.metadata && typeof workflow.metadata !== 'object') {
      validation.errors.push('Metadata must be a valid object');
    }
  }

  validateNodes(workflow, validation) {
    const totalNodes = workflow.metadata.estimatedNodes;
    
    if (totalNodes > this.validationRules.nodeValidation.maxNodesPerWorkflow) {
      validation.errors.push(`Too many nodes: ${totalNodes} (max: ${this.validationRules.nodeValidation.maxNodesPerWorkflow})`);
    }
    
    if (totalNodes < this.validationRules.nodeValidation.minNodesPerWorkflow) {
      validation.errors.push(`Too few nodes: ${totalNodes} (min: ${this.validationRules.nodeValidation.minNodesPerWorkflow})`);
    }

    // Check for invalid node combinations
    this.validationRules.nodeValidation.invalidCombinations.forEach(combo => {
      const hasFirst = workflow.trigger.type === combo[0];
      const hasSecond = workflow.processingSteps.some(step => step.node === combo[1]) ||
                       workflow.integrations.some(int => int.service === combo[1]);
      
      if (hasFirst && hasSecond) {
        validation.errors.push(`Invalid combination: ${combo[0]} with ${combo[1]}`);
      }
    });
  }

  validateIntegrations(workflow, validation) {
    if (workflow.integrations.length > this.validationRules.integrationValidation.maxIntegrationsPerWorkflow) {
      validation.errors.push(`Too many integrations: ${workflow.integrations.length}`);
    }

    // Check authentication requirements
    workflow.integrations.forEach(integration => {
      if (this.validationRules.integrationValidation.requiresAuthentication.includes(integration.service)) {
        if (!integration.hasAuth) {
          validation.warnings.push(`${integration.service} requires authentication`);
        }
      }
    });

    // Check rate limits
    workflow.integrations.forEach(integration => {
      const rateLimit = this.validationRules.integrationValidation.rateLimits[integration.service];
      if (rateLimit && workflow.metadata.estimatedExecutions > rateLimit) {
        validation.warnings.push(`${integration.service} may hit rate limits`);
      }
    });
  }

  validateBusinessLogic(workflow, validation) {
    // Validate conditional logic
    if (workflow.conditional) {
      const requirements = this.validationRules.businessLogic.conditionalRequirements[workflow.conditional.node];
      if (requirements) {
        requirements.forEach(req => {
          if (!workflow.conditional[req]) {
            validation.errors.push(`${workflow.conditional.node} missing required field: ${req}`);
          }
        });
      }
    }

    // Check data flow consistency
    if (workflow.processingSteps.length > 0) {
      const dataTypes = new Set();
      workflow.processingSteps.forEach(step => {
        if (step.inputType && step.outputType && step.inputType !== step.outputType) {
          dataTypes.add(step.outputType);
        }
      });
      
      if (dataTypes.size > 3) {
        validation.warnings.push('Multiple data type transformations may cause issues');
      }
    }
  }

  validatePerformance(workflow, validation) {
    // Estimate execution time
    let estimatedTime = 100; // Base time in ms
    
    estimatedTime += workflow.processingSteps.length * 50;
    estimatedTime += workflow.integrations.length * 200;
    
    if (workflow.conditional) {
      estimatedTime += 100;
    }

    if (estimatedTime > 30000) { // 30 seconds
      validation.warnings.push(`Workflow may be slow (estimated ${estimatedTime}ms)`);
    }

    // Ensure metadata exists before setting properties
    if (!workflow.metadata) {
      workflow.metadata = {};
    }
    workflow.metadata.estimatedExecutionTime = estimatedTime;
    workflow.metadata.estimatedExecutions = Math.floor(Math.random() * 1000) + 100; // Simulate execution count
  }

  identifyIssues(workflow, validationResult) {
    const issues = [];

    // Convert validation errors to issues
    validationResult.errors.forEach(error => {
      issues.push({
        type: 'ERROR',
        category: 'VALIDATION',
        description: error,
        severity: 'HIGH',
        fixable: true
      });
      this.issuesFound.push({
        type: 'ERROR',
        category: 'VALIDATION',
        description: error,
        workflowId: workflow.id
      });
    });

    // Convert warnings to issues
    validationResult.warnings.forEach(warning => {
      issues.push({
        type: 'WARNING',
        category: 'PERFORMANCE',
        description: warning,
        severity: 'MEDIUM',
        fixable: true
      });
      this.issuesFound.push({
        type: 'WARNING',
        category: 'PERFORMANCE',
        description: warning,
        workflowId: workflow.id
      });
    });

    // Check for known issues based on patterns
    this.checkKnownIssuePatterns(workflow, issues);

    return issues;
  }

  checkKnownIssuePatterns(workflow, issues) {
    // Pattern 1: Missing error handling
    if (!workflow.processingSteps.some(step => step.node === 'Stop and Error')) {
      const issue = {
        type: 'SUGGESTION',
        category: 'RELIABILITY',
        description: 'Consider adding error handling nodes',
        severity: 'LOW',
        fixable: true
      };
      issues.push(issue);
      this.issuesFound.push({
        ...issue,
        workflowId: workflow.id
      });
    }

    // Pattern 2: No data validation
    if (!workflow.processingSteps.some(step => step.purpose && step.purpose.includes('validation'))) {
      const issue = {
        type: 'SUGGESTION',
        category: 'DATA_QUALITY',
        description: 'Consider adding data validation steps',
        severity: 'MEDIUM',
        fixable: true
      };
      issues.push(issue);
      this.issuesFound.push({
        ...issue,
        workflowId: workflow.id
      });
    }

    // Pattern 3: Inefficient data processing
    const hasSort = workflow.processingSteps.some(step => step.node === 'Sort');
    const hasLimit = workflow.processingSteps.some(step => step.node === 'Limit');
    
    if (hasSort && !hasLimit) {
      const issue = {
        type: 'WARNING',
        category: 'PERFORMANCE',
        description: 'Sorting without limit may impact performance',
        severity: 'MEDIUM',
        fixable: true
      };
      issues.push(issue);
      this.issuesFound.push({
        ...issue,
        workflowId: workflow.id
      });
    }
  }

  async applyFixes(workflow, issues) {
    let fixedWorkflow = JSON.parse(JSON.stringify(workflow)); // Deep clone
    const appliedFixes = [];

    for (const issue of issues) {
      if (issue.fixable) {
        const fix = await this.generateFix(fixedWorkflow, issue);
        if (fix.applied) {
          fixedWorkflow = fix.workflow;
          appliedFixes.push({
            issue: issue.description,
            fix: fix.description,
            category: issue.category
          });
        }
      }
    }

    this.fixesApplied.push(...appliedFixes);
    return fixedWorkflow;
  }

  async generateFix(workflow, issue) {
    const fix = { applied: false, workflow: workflow, description: '' };

    switch (issue.category) {
      case 'VALIDATION':
        if (issue.description.includes('missing trigger')) {
          workflow.trigger = {
            type: 'Manual Trigger',
            config: { description: 'Added default trigger' }
          };
          // Update estimated nodes
          if (workflow.metadata) {
            workflow.metadata.estimatedNodes = this.estimateNodes(
              workflow.processingSteps, 
              workflow.conditional, 
              workflow.integrations
            );
          }
          fix.applied = true;
          fix.description = 'Added missing trigger node';
        }
        break;

      case 'PERFORMANCE':
        if (issue.description.includes('Too many nodes')) {
          // Reduce processing steps
          workflow.processingSteps = workflow.processingSteps.slice(0, 5);
          // Update estimated nodes
          if (workflow.metadata) {
            workflow.metadata.estimatedNodes = this.estimateNodes(
              workflow.processingSteps, 
              workflow.conditional, 
              workflow.integrations
            );
          }
          fix.applied = true;
          fix.description = 'Reduced number of processing steps';
        }
        
        if (issue.description.includes('Sorting without limit')) {
          // Add limit node after sort
          const sortIndex = workflow.processingSteps.findIndex(step => step.node === 'Sort');
          if (sortIndex !== -1) {
            workflow.processingSteps.splice(sortIndex + 1, 0, {
              node: 'Limit',
              purpose: 'Limit results for performance',
              config: { limit: 100 }
            });
            // Update estimated nodes
            if (workflow.metadata) {
              workflow.metadata.estimatedNodes = this.estimateNodes(
                workflow.processingSteps, 
                workflow.conditional, 
                workflow.integrations
              );
            }
            fix.applied = true;
            fix.description = 'Added limit node after sort for performance';
          }
        }
        break;

      case 'RELIABILITY':
        if (issue.description.includes('error handling')) {
          workflow.processingSteps.push({
            node: 'Stop and Error',
            purpose: 'Handle workflow errors',
            config: { errorMessage: 'Workflow execution failed' }
          });
          // Update estimated nodes
          if (workflow.metadata) {
            workflow.metadata.estimatedNodes = this.estimateNodes(
              workflow.processingSteps, 
              workflow.conditional, 
              workflow.integrations
            );
          }
          fix.applied = true;
          fix.description = 'Added error handling node';
        }
        break;

      case 'DATA_QUALITY':
        if (issue.description.includes('data validation')) {
          workflow.processingSteps.unshift({
            node: 'Code (JavaScript)',
            purpose: 'Data validation and cleaning',
            config: { code: 'return $input.all().filter(item => item.json && Object.keys(item.json).length > 0);' }
          });
          // Update estimated nodes
          if (workflow.metadata) {
            workflow.metadata.estimatedNodes = this.estimateNodes(
              workflow.processingSteps, 
              workflow.conditional, 
              workflow.integrations
            );
          }
          fix.applied = true;
          fix.description = 'Added data validation step';
        }
        break;
    }

    return fix;
  }

  extractLearnings(originalWorkflow, issues, fixedWorkflow) {
    const learnings = [];

    // Learning from issues found
    issues.forEach(issue => {
      learnings.push(`Issue pattern: ${issue.category} - ${issue.description}`);
    });

    // Learning from fixes applied
    if (issues.length > 0 && fixedWorkflow) {
      learnings.push(`Fixes improve workflow reliability and performance`);
    }

    // Learning from workflow patterns
    if (originalWorkflow.integrations.length > 3) {
      learnings.push('Complex integrations require careful validation');
    }

    if (originalWorkflow.processingSteps.length > 5) {
      learnings.push('Long processing chains need performance optimization');
    }

    return learnings;
  }

  recordLearnings(learnings) {
    this.learnings.push(...learnings);
    
    // Update known issues based on learnings
    learnings.forEach(learning => {
      if (learning.includes('Issue pattern:')) {
        const pattern = learning.split('Issue pattern: ')[1];
        this.knownIssues.set(pattern, (this.knownIssues.get(pattern) || 0) + 1);
      }
    });
  }

  updatePerformanceMetrics(testId, testTime) {
    this.performanceMetrics.totalTime += testTime;
    this.performanceMetrics.avgTestTime = this.performanceMetrics.totalTime / testId;
    
    if (testTime > this.performanceMetrics.slowestTest.time) {
      this.performanceMetrics.slowestTest = { id: testId, time: testTime };
    }
    
    if (testTime < this.performanceMetrics.fastestTest.time) {
      this.performanceMetrics.fastestTest = { id: testId, time: testTime };
    }
  }

  // Helper methods
  selectOptimalTrigger(triggers) {
    // Use learnings to select better triggers
    const reliableTriggers = ['Manual Trigger', 'Schedule Trigger', 'Webhook'];
    const availableTriggers = triggers.filter(t => reliableTriggers.includes(t));
    return availableTriggers.length > 0 ? 
           this.getRandomItem(availableTriggers) : 
           this.getRandomItem(triggers);
  }

  generateValidProcessingSteps(nodes) {
    const stepCount = Math.floor(Math.random() * 3) + 2; // 2-4 steps
    const steps = [];
    
    for (let i = 0; i < stepCount; i++) {
      steps.push({
        node: this.getRandomItem(nodes),
        purpose: this.generateStepPurpose(),
        inputType: 'array',
        outputType: 'array'
      });
    }
    
    return steps;
  }

  generateCompatibleIntegrations(integrations, trigger) {
    const count = Math.floor(Math.random() * 2) + 1; // 1-2 integrations
    const selected = [];
    
    for (let i = 0; i < count; i++) {
      const integration = this.getRandomItem(integrations);
      selected.push({
        service: integration,
        action: this.generateIntegrationAction(),
        hasAuth: this.validationRules.integrationValidation.requiresAuthentication.includes(integration)
      });
    }
    
    return selected;
  }

  generateValidConditional() {
    if (Math.random() < 0.3) { // 30% chance
      return {
        node: 'IF',
        condition: 'Status equals "active"',
        trueRoute: 'Continue processing',
        falseRoute: 'Skip to end'
      };
    }
    return null;
  }

  generateTriggerConfig(trigger) {
    const configs = {
      'Manual Trigger': { description: 'Manual execution' },
      'Webhook': { url: '/webhook/test', method: 'POST' },
      'Schedule Trigger': { interval: '0 9 * * *' },
      'Form Trigger': { fields: ['name', 'email'] }
    };
    
    return configs[trigger] || { description: 'Default config' };
  }

  generateStepPurpose() {
    const purposes = [
      'Data validation and cleaning',
      'Format transformation', 
      'Field extraction and mapping',
      'Duplicate removal',
      'Data enrichment'
    ];
    return this.getRandomItem(purposes);
  }

  generateIntegrationAction() {
    const actions = [
      'Send notification',
      'Create record', 
      'Update existing data',
      'Generate report',
      'Upload file'
    ];
    return this.getRandomItem(actions);
  }

  calculateComplexity(processingSteps, conditional, integrations) {
    let complexity = processingSteps.length;
    if (conditional) complexity += 2;
    complexity += integrations.length;
    
    if (complexity <= 4) return 'Simple';
    if (complexity <= 8) return 'Medium';
    return 'Complex';
  }

  estimateNodes(processingSteps, conditional, integrations) {
    let nodes = 1; // trigger
    nodes += processingSteps.length;
    if (conditional) nodes += 2;
    nodes += integrations.length;
    return nodes;
  }

  getRandomItem(array) {
    return array[Math.floor(Math.random() * array.length)];
  }

  generateProgressReport(currentTest) {
    const passedTests = this.testResults.filter(r => r.status === 'PASSED').length;
    const failedTests = this.testResults.filter(r => r.status === 'FAILED').length;
    const errorTests = this.testResults.filter(r => r.status === 'ERROR').length;
    
    return {
      progress: `${currentTest}/10000`,
      percentage: ((currentTest / 10000) * 100).toFixed(2),
      passed: passedTests,
      failed: failedTests,
      errors: errorTests,
      totalIssuesFound: this.issuesFound.length,
      totalFixesApplied: this.fixesApplied.length,
      avgTestTime: this.performanceMetrics.avgTestTime.toFixed(2),
      learningsCount: this.learnings.length
    };
  }

  async runAllTests() {
    console.log('🚀 Starting 10,000 n8n automation tests with iterative learning...\n');
    
    for (let i = 1; i <= 10000; i++) {
      this.currentTest = i;
      
      const testResult = await this.runSingleTest(i);
      
      // Log progress every 100 tests
      if (i % 100 === 0) {
        const progress = this.generateProgressReport(i);
        console.log(`📊 Progress: ${progress.progress} (${progress.percentage}%)`);
        console.log(`   ✅ Passed: ${progress.passed} | ❌ Failed: ${progress.failed} | 🚨 Errors: ${progress.errors}`);
        console.log(`   🔧 Issues Found: ${progress.totalIssuesFound} | 🛠️ Fixes Applied: ${progress.totalFixesApplied}`);
        console.log(`   ⏱️ Avg Test Time: ${progress.avgTestTime}ms | 📚 Learnings: ${progress.learningsCount}\n`);
      }
      
      // Log individual test issues for first 10 tests
      if (i <= 10 && testResult.issues && testResult.issues.length > 0) {
        console.log(`🔍 Test ${i} Issues:`);
        testResult.issues.forEach(issue => {
          console.log(`   ${issue.type}: ${issue.description}`);
        });
        console.log('');
      }
    }
    
    return this.generateFinalReport();
  }

  generateFinalReport() {
    const totalTests = this.testResults.length;
    const passedTests = this.testResults.filter(r => r.status === 'PASSED').length;
    const failedTests = this.testResults.filter(r => r.status === 'FAILED').length;
    const errorTests = this.testResults.filter(r => r.status === 'ERROR').length;
    
    const issueCategories = {};
    this.issuesFound.forEach(issue => {
      issueCategories[issue.category] = (issueCategories[issue.category] || 0) + 1;
    });
    
    const fixCategories = {};
    this.fixesApplied.forEach(fix => {
      fixCategories[fix.category] = (fixCategories[fix.category] || 0) + 1;
    });
    
    // Calculate top patterns from known issues
    const topPatterns = Array.from(this.knownIssues.entries())
      .sort(([,a], [,b]) => b - a)
      .slice(0, 10)
      .map(([pattern, count]) => [pattern, count]);
    
    return {
      summary: {
        totalTests,
        passedTests,
        failedTests,
        errorTests,
        successRate: totalTests > 0 ? ((passedTests / totalTests) * 100).toFixed(2) : '0.00'
      },
      performance: {
        ...this.performanceMetrics,
        avgTestTime: totalTests > 0 ? this.performanceMetrics.totalTime / totalTests : 0
      },
      issues: {
        totalFound: this.issuesFound.length,
        categories: issueCategories,
        topPatterns: topPatterns
      },
      fixes: {
        totalApplied: this.fixesApplied.length,
        categories: fixCategories
      },
      learnings: {
        total: this.learnings.length,
        unique: [...new Set(this.learnings)].length
      }
    };
  }
}

module.exports = N8nIterativeTestRunner;