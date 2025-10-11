#!/usr/bin/env node
/**
 * Real Estate Scraper Workflow Tester
 * Tests the generated real estate workflow for errors and issues
 */

const fs = require('fs');

class RealEstateWorkflowTester {
  constructor() {
    this.requiredNodes = [
      'Manual Trigger',
      'Initialize Configuration', 
      'Generate Page URLs',
      'Split Pages into Batches',
      'HTTP Request - Listings Page',
      'HTML Extract - Listings',
      'Process Individual Listings',
      'HTTP Request - Detail Page',
      'HTML Extract - Agent Contact',
      'Normalize and Set Data',
      'Validate Listing Data',
      'Check for Duplicates',
      'Filter New Leads',
      'Prepare Email Data',
      'Send Cold Email',
      'Wait Between Emails',
      'Record Success',
      'Record Duplicate', 
      'Record Invalid',
      'Merge All Results',
      'Append to Google Sheets',
      'Generate Summary'
    ];
    
    this.requiredConnections = [
      'Manual Trigger → Initialize Configuration',
      'Initialize Configuration → Generate Page URLs',
      'Generate Page URLs → Split Pages into Batches',
      'Split Pages into Batches → HTTP Request - Listings Page',
      'HTTP Request - Listings Page → HTML Extract - Listings',
      'HTML Extract - Listings → Process Individual Listings',
      'Process Individual Listings → HTTP Request - Detail Page',
      'HTTP Request - Detail Page → HTML Extract - Agent Contact',
      'HTML Extract - Agent Contact → Normalize and Set Data',
      'Normalize and Set Data → Validate Listing Data',
      'Validate Listing Data → Check for Duplicates (true)',
      'Validate Listing Data → Record Invalid (false)',
      'Check for Duplicates → Filter New Leads',
      'Filter New Leads → Prepare Email Data (true)',
      'Filter New Leads → Record Duplicate (false)',
      'Prepare Email Data → Send Cold Email',
      'Send Cold Email → Wait Between Emails',
      'Wait Between Emails → Record Success',
      'Record Success → Merge All Results',
      'Record Duplicate → Merge All Results',
      'Record Invalid → Merge All Results',
      'Merge All Results → Append to Google Sheets',
      'Append to Google Sheets → Generate Summary'
    ];
  }

  /**
   * Test the real estate workflow
   */
  testWorkflow(workflowPath) {
    console.log('🏠 Real Estate Scraper Workflow Tester');
    console.log('=====================================');
    
    try {
      const workflow = JSON.parse(fs.readFileSync(workflowPath, 'utf8'));
      
      const results = {
        nodeStructure: this.testNodeStructure(workflow),
        connectionFlow: this.testConnectionFlow(workflow),
        parameterValidation: this.testParameters(workflow),
        dataFlow: this.testDataFlow(workflow),
        errorHandling: this.testErrorHandling(workflow),
        productionReadiness: this.testProductionReadiness(workflow)
      };
      
      this.displayResults(results);
      return results;
      
    } catch (error) {
      console.error('❌ Failed to load workflow:', error.message);