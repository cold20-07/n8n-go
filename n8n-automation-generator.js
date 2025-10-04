// n8n Automation Generation Test Suite
// Generates 10,000 unique workflow scenarios for testing

class N8nAutomationGenerator {
  constructor() {
    this.triggers = [
      'Manual Trigger',
      'Webhook',
      'Schedule Trigger',
      'Form Trigger',
      'Email Trigger (IMAP)',
      'File Trigger',
      'HTTP Request Trigger',
      'Slack Trigger',
      'Discord Trigger',
      'Typeform Trigger',
      'Google Sheets Trigger',
      'Airtable Trigger',
      'MongoDB Trigger',
      'MySQL Trigger',
      'Postgres Trigger'
    ];

    this.dataProcessingNodes = [
      'Code (JavaScript)',
      'Set',
      'Edit Fields',
      'Split Out',
      'Aggregate',
      'Sort',
      'Limit',
      'Remove Duplicates',
      'Merge',
      'Item Lists',
      'Date & Time',
      'Crypto',
      'Hash',
      'HTML Extract',
      'XML',
      'JSON',
      'CSV',
      'Markdown'
    ];

    this.conditionalNodes = [
      'IF',
      'Switch',
      'Merge',
      'Wait',
      'Stop and Error',
      'No Operation'
    ];

    this.integrationNodes = [
      'HTTP Request',
      'Slack',
      'Discord',
      'Gmail',
      'Google Sheets',
      'Google Drive',
      'Notion',
      'Airtable',
      'Trello',
      'Asana',
      'Monday.com',
      'Salesforce',
      'HubSpot',
      'Mailchimp',
      'SendGrid',
      'Twilio',
      'WhatsApp Business',
      'Telegram',
      'Twitter',
      'LinkedIn',
      'Facebook',
      'Instagram',
      'YouTube',
      'Shopify',
      'WooCommerce',
      'Stripe',
      'PayPal',
      'AWS S3',
      'AWS Lambda',
      'Google Cloud Functions',
      'Azure Functions',
      'Dropbox',
      'OneDrive',
      'Box',
      'FTP',
      'SSH',
      'MySQL',
      'PostgreSQL',
      'MongoDB',
      'Redis',
      'Elasticsearch',
      'InfluxDB',
      'Supabase',
      'Firebase',
      'Zapier',
      'Make (Integromat)',
      'IFTTT'
    ];

    this.businessScenarios = [
      'Lead Management',
      'Customer Onboarding',
      'Order Processing',
      'Invoice Generation',
      'Support Ticket Routing',
      'Social Media Monitoring',
      'Content Publishing',
      'Data Backup',
      'Report Generation',
      'Inventory Management',
      'Employee Onboarding',
      'Meeting Scheduling',
      'Email Marketing',
      'Survey Processing',
      'File Organization',
      'Security Monitoring',
      'Performance Tracking',
      'Quality Assurance',
      'Compliance Checking',
      'Budget Tracking'
    ];

    this.dataTypes = [
      'User Registration Data',
      'Order Information',
      'Customer Feedback',
      'Product Catalog',
      'Financial Transactions',
      'Employee Records',
      'Project Tasks',
      'Marketing Metrics',
      'Sales Pipeline',
      'Support Tickets',
      'Inventory Levels',
      'Website Analytics',
      'Social Media Posts',
      'Email Campaigns',
      'Survey Responses'
    ];

    this.conditions = [
      'Date is within 7 days',
      'Amount greater than $1000',
      'Status equals "pending"',
      'Email contains domain',
      'Priority is high',
      'Category matches filter',
      'User role is admin',
      'Location is specific region',
      'Time is business hours',
      'Count exceeds threshold'
    ];
  }

  generateWorkflow(id) {
    const trigger = this.getRandomItem(this.triggers);
    const scenario = this.getRandomItem(this.businessScenarios);
    const dataType = this.getRandomItem(this.dataTypes);
    
    // Generate 2-5 processing steps
    const processingSteps = this.generateProcessingSteps();
    
    // Generate conditional logic (30% chance)
    const hasConditional = Math.random() < 0.3;
    const conditional = hasConditional ? {
      node: this.getRandomItem(this.conditionalNodes),
      condition: this.getRandomItem(this.conditions)
    } : null;
    
    // Generate 1-3 integration endpoints
    const integrations = this.generateIntegrations();
    
    return {
      id: id,
      name: `${scenario} - ${dataType} Workflow`,
      trigger: {
        type: trigger,
        description: this.generateTriggerDescription(trigger, scenario)
      },
      dataType: dataType,
      processingSteps: processingSteps,
      conditional: conditional,
      integrations: integrations,
      complexity: this.calculateComplexity(processingSteps, conditional, integrations),
      estimatedNodes: this.estimateNodeCount(processingSteps, conditional, integrations),
      useCase: this.generateUseCase(scenario, dataType, trigger)
    };
  }

  generateProcessingSteps() {
    const stepCount = Math.floor(Math.random() * 4) + 2; // 2-5 steps
    const steps = [];
    
    for (let i = 0; i < stepCount; i++) {
      steps.push({
        node: this.getRandomItem(this.dataProcessingNodes),
        purpose: this.generateStepPurpose()
      });
    }
    
    return steps;
  }

  generateIntegrations() {
    const integrationCount = Math.floor(Math.random() * 3) + 1; // 1-3 integrations
    const integrations = [];
    
    for (let i = 0; i < integrationCount; i++) {
      integrations.push({
        service: this.getRandomItem(this.integrationNodes),
        action: this.generateIntegrationAction()
      });
    }
    
    return integrations;
  }

  generateTriggerDescription(trigger, scenario) {
    const descriptions = {
      'Manual Trigger': `Manual execution for ${scenario} process`,
      'Webhook': `External system triggers ${scenario} via webhook`,
      'Schedule Trigger': `Automated ${scenario} runs on schedule`,
      'Form Trigger': `Web form submission initiates ${scenario}`,
      'Email Trigger (IMAP)': `Incoming email triggers ${scenario}`,
      'File Trigger': `File upload/change triggers ${scenario}`
    };
    
    return descriptions[trigger] || `${trigger} initiates ${scenario}`;
  }

  generateStepPurpose() {
    const purposes = [
      'Data validation and cleaning',
      'Format transformation',
      'Field extraction and mapping',
      'Duplicate removal',
      'Data enrichment',
      'Calculation and aggregation',
      'Filtering and sorting',
      'Structure conversion',
      'Validation checks',
      'Data normalization'
    ];
    
    return this.getRandomItem(purposes);
  }

  generateIntegrationAction() {
    const actions = [
      'Send notification',
      'Create record',
      'Update existing data',
      'Generate report',
      'Upload file',
      'Send email',
      'Post message',
      'Create task',
      'Log event',
      'Trigger webhook'
    ];
    
    return this.getRandomItem(actions);
  }

  generateUseCase(scenario, dataType, trigger) {
    return `When ${trigger.toLowerCase()} receives ${dataType.toLowerCase()}, automatically process and route through ${scenario.toLowerCase()} workflow to relevant systems and stakeholders.`;
  }

  calculateComplexity(processingSteps, conditional, integrations) {
    let complexity = processingSteps.length;
    if (conditional) complexity += 2;
    complexity += integrations.length;
    
    if (complexity <= 4) return 'Simple';
    if (complexity <= 8) return 'Medium';
    return 'Complex';
  }

  estimateNodeCount(processingSteps, conditional, integrations) {
    let nodeCount = 1; // trigger
    nodeCount += processingSteps.length;
    if (conditional) nodeCount += 2; // conditional + branch
    nodeCount += integrations.length;
    return nodeCount;
  }

  getRandomItem(array) {
    return array[Math.floor(Math.random() * array.length)];
  }

  generateTestSuite(count = 10000) {
    console.log(`Generating ${count} n8n automation test scenarios...`);
    const startTime = Date.now();
    
    const workflows = [];
    const stats = {
      triggers: {},
      complexity: { Simple: 0, Medium: 0, Complex: 0 },
      scenarios: {},
      totalNodes: 0
    };
    
    for (let i = 1; i <= count; i++) {
      const workflow = this.generateWorkflow(i);
      workflows.push(workflow);
      
      // Update statistics
      stats.triggers[workflow.trigger.type] = (stats.triggers[workflow.trigger.type] || 0) + 1;
      stats.complexity[workflow.complexity]++;
      stats.scenarios[workflow.dataType] = (stats.scenarios[workflow.dataType] || 0) + 1;
      stats.totalNodes += workflow.estimatedNodes;
      
      if (i % 1000 === 0) {
        console.log(`Generated ${i} workflows...`);
      }
    }
    
    const endTime = Date.now();
    const duration = endTime - startTime;
    
    return {
      workflows: workflows,
      statistics: {
        ...stats,
        averageNodesPerWorkflow: Math.round(stats.totalNodes / count * 100) / 100,
        generationTime: `${duration}ms`,
        workflowsPerSecond: Math.round(count / (duration / 1000))
      }
    };
  }
}

// Generate the test suite
const generator = new N8nAutomationGenerator();
const testSuite = generator.generateTestSuite(10000);

// Export class and generator function
module.exports = N8nAutomationGenerator;

// If running directly, output sample results
if (require.main === module) {
  console.log('\n=== N8N AUTOMATION TEST SUITE RESULTS ===');
  console.log(`Total Workflows Generated: ${testSuite.workflows.length}`);
  console.log(`Generation Time: ${testSuite.statistics.generationTime}`);
  console.log(`Workflows/Second: ${testSuite.statistics.workflowsPerSecond}`);
  console.log(`Average Nodes per Workflow: ${testSuite.statistics.averageNodesPerWorkflow}`);
  
  console.log('\n=== COMPLEXITY DISTRIBUTION ===');
  Object.entries(testSuite.statistics.complexity).forEach(([complexity, count]) => {
    const percentage = ((count / 10000) * 100).toFixed(1);
    console.log(`${complexity}: ${count} (${percentage}%)`);
  });
  
  console.log('\n=== TOP 10 TRIGGERS ===');
  const topTriggers = Object.entries(testSuite.statistics.triggers)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 10);
  
  topTriggers.forEach(([trigger, count]) => {
    console.log(`${trigger}: ${count}`);
  });
  
  console.log('\n=== SAMPLE WORKFLOWS ===');
  testSuite.workflows.slice(0, 5).forEach(workflow => {
    console.log(`\n${workflow.id}. ${workflow.name}`);
    console.log(`   Trigger: ${workflow.trigger.type}`);
    console.log(`   Complexity: ${workflow.complexity} (${workflow.estimatedNodes} nodes)`);
    console.log(`   Use Case: ${workflow.useCase}`);
  });
}