#!/usr/bin/env node
/**
 * Universal Error Handler for N8N Workflow Generation
 * Handles errors from any prompt, any scenario, any workflow generation
 */

const { ProactiveErrorPrevention } = require('./proactive-error-prevention.js');
const fs = require('fs');

class UniversalErrorHandler {
  constructor() {
    this.prevention = new ProactiveErrorPrevention();
    this.errorPatterns = this.buildErrorPatterns();
    this.fixHistory = [];
    this.errorStats = {
      totalErrors: 0,
      fixedErrors: 0,
      errorTypes: {}
    };
  }

  /**
   * Main wrapper for any workflow generation function
   */
  wrapWorkflowGenerator(generatorFunction, options = {}) {
    return async (...args) => {
      const context = {
        functionName: generatorFunction.name || 'anonymous',
        timestamp: new Date().toISOString(),
        args: this.sanitizeArgs(args),
        options
      };

      try {
        console.log(`🛡️ Universal Error Handler: Wrapping ${context.functionName}`);
        
        // Call original function
        let workflow = await generatorFunction(...args);
        
        // Handle different return types
        if (typeof workflow === 'string') {
          try {
            workflow = JSON.parse(workflow);
          } catch (e) {
            throw new Error('Generated workflow is not valid JSON');
          }
        }

        if (!workflow || typeof workflow !== 'object') {
          throw new Error('Generated workflow is not a valid object');
        }

        // Apply universal error handling
        const result = await this.handleAnyWorkflowErrors(workflow, context);
        
        // Log success
        this.logSuccess(context, result);
        
        return result.workflow;

      } catch (error) {
        // Handle generation errors
        return await this.handleGenerationError(error, context, args);
      }
    };
  }

  /**
   * Handle errors in any workflow regardless of source
   */
  async handleAnyWorkflowErrors(workflow, context = {}) {
    console.log(`🔍 Analyzing workflow for errors: ${workflow.name || 'Unnamed'}`);
    
    // Step 1: Basic structure validation
    const structureCheck = this.validateBasicStructure(workflow);
    if (!structureCheck.isValid) {
      workflow = await this.fixBasicStructure(workflow, structureCheck.issues);
    }

    // Step 2: Apply proactive error prevention
    const proactiveResult = await this.prevention.validateAndFixAnyWorkflow(workflow, context);
    
    // Step 3: Apply pattern-based fixes
    const patternResult = await this.applyPatternBasedFixes(proactiveResult.workflow, context);
    
    // Step 4: Final validation
    const finalValidation = await this.finalValidation(patternResult.workflow);
    
    // Compile results
    const allFixes = [
      ...(structureCheck.fixes || []),
      ...(proactiveResult.fixes || []),
      ...(patternResult.fixes || [])
    ];

    const allIssues = [
      ...(structureCheck.issues || []),
      ...(proactiveResult.issues || []),
      ...(patternResult.issues || [])
    ];

    // Update statistics
    this.updateErrorStats(allIssues, allFixes);

    // Log fix history
    if (allFixes.length > 0) {
      this.fixHistory.push({
        timestamp: new Date().toISOString(),
        context,
        fixes: allFixes,
        workflowName: workflow.name
      });
    }

    return {
      workflow: finalValidation.workflow,
      isValid: finalValidation.isValid,
      issues: allIssues,
      fixes: allFixes,
      warnings: proactiveResult.warnings || [],
      metadata: {
        handlerVersion: '1.0',
        processingTime: Date.now() - new Date(context.timestamp).getTime(),
        context
      }
    };
  }

  /**
   * Validate basic workflow structure
   */
  validateBasicStructure(workflow) {
    const issues = [];
    const fixes = [];

    // Check required fields
    if (!workflow.id) {
      workflow.id = `workflow_${Date.now()}`;
      fixes.push('Added missing workflow ID');
    }

    if (!workflow.name) {
      workflow.name = 'Generated Workflow';
      fixes.push('Added missing workflow name');
    }

    if (!workflow.nodes || !Array.isArray(workflow.nodes)) {
      workflow.nodes = [];
      issues.push('Workflow missing nodes array');
    }

    if (!workflow.connections || typeof workflow.connections !== 'object') {
      workflow.connections = {};
      fixes.push('Added missing connections object');
    }

    if (!workflow.settings) {
      workflow.settings = { executionOrder: 'v1' };
      fixes.push('Added missing settings');
    }

    if (!workflow.meta) {
      workflow.meta = { 
        generated_by: 'universal-error-handler',
        created_at: new Date().toISOString()
      };
      fixes.push('Added missing metadata');
    }

    return {
      isValid: issues.length === 0,
      issues,
      fixes
    };
  }

  /**
   * Fix basic structure issues
   */
  async fixBasicStructure(workflow, issues) {
    console.log(`🔧 Fixing basic structure issues: ${issues.length} found`);
    
    // Ensure workflow has minimum viable structure
    if (!workflow.nodes || workflow.nodes.length === 0) {
      // Add a basic manual trigger
      workflow.nodes = [{
        id: this.generateId(),
        name: 'Manual Trigger',
        type: 'n8n-nodes-base.manualTrigger',
        typeVersion: 1,
        position: [240, 300],
        parameters: {}
      }];
    }

    return workflow;
  }

  /**
   * Apply pattern-based fixes for common issues
   */
  async applyPatternBasedFixes(workflow, context) {
    const fixes = [];
    const issues = [];

    // Pattern 1: Missing node IDs
    for (const node of workflow.nodes) {
      if (!node.id) {
        node.id = this.generateId();
        fixes.push(`Added missing ID to node: ${node.name}`);
      }
    }

    // Pattern 2: Invalid positions
    for (let i = 0; i < workflow.nodes.length; i++) {
      const node = workflow.nodes[i];
      if (!node.position || !Array.isArray(node.position)) {
        node.position = [240 + i * 220, 300];
        fixes.push(`Fixed position for node: ${node.name}`);
      }
    }

    // Pattern 3: Missing typeVersion
    for (const node of workflow.nodes) {
      if (!node.typeVersion) {
        node.typeVersion = 1;
        fixes.push(`Added missing typeVersion to node: ${node.name}`);
      }
    }

    // Pattern 4: Empty parameters
    for (const node of workflow.nodes) {
      if (!node.parameters) {
        node.parameters = {};
        fixes.push(`Added missing parameters to node: ${node.name}`);
      }
    }

    return { workflow, fixes, issues };
  }

  /**
   * Final validation check
   */
  async finalValidation(workflow) {
    // Run one more validation to ensure everything is correct
    const validation = await this.prevention.validateAndFixAnyWorkflow(workflow, {
      source: 'final_validation',
      timestamp: new Date().toISOString()
    });

    return {
      workflow: validation.workflow,
      isValid: validation.isValid,
      issues: validation.issues
    };
  }

  /**
   * Handle generation errors (when the original function fails)
   */
  async handleGenerationError(error, context, originalArgs) {
    console.error(`❌ Generation error in ${context.functionName}:`, error.message);
    
    this.errorStats.totalErrors++;
    
    // Try to create a fallback workflow
    try {
      const fallbackWorkflow = await this.createFallbackWorkflow(error, context, originalArgs);
      const result = await this.handleAnyWorkflowErrors(fallbackWorkflow, {
        ...context,
        isFallback: true,
        originalError: error.message
      });

      console.log('🔄 Created fallback workflow after generation error');
      return result.workflow;

    } catch (fallbackError) {
      console.error('❌ Fallback workflow creation also failed:', fallbackError.message);
      
      // Return minimal viable workflow
      return this.createMinimalWorkflow(error, context);
    }
  }

  /**
   * Create fallback workflow when generation fails
   */
  async createFallbackWorkflow(error, context, originalArgs) {
    // Try to extract intent from original arguments
    let description = 'Fallback workflow';
    
    if (originalArgs && originalArgs.length > 0) {
      const firstArg = originalArgs[0];
      if (typeof firstArg === 'string') {
        description = firstArg;
      } else if (firstArg && firstArg.description) {
        description = firstArg.description;
      }
    }

    return {
      id: `fallback_${Date.now()}`,
      name: `Fallback: ${description.substring(0, 50)}`,
      active: false,
      nodes: [
        {
          id: this.generateId(),
          name: 'Manual Trigger',
          type: 'n8n-nodes-base.manualTrigger',
          typeVersion: 1,
          position: [240, 300],
          parameters: {}
        },
        {
          id: this.generateId(),
          name: 'Error Handler',
          type: 'n8n-nodes-base.code',
          typeVersion: 2,
          position: [460, 300],
          parameters: {
            jsCode: `// Fallback workflow created due to generation error
// Original error: ${error.message}
// Context: ${JSON.stringify(context, null, 2)}

const inputData = $input.all();
return [{
  json: {
    message: 'Fallback workflow executed',
    originalError: '${error.message}',
    timestamp: new Date().toISOString(),
    data: inputData
  }
}];`
          }
        }
      ],
      connections: {
        'Manual Trigger': {
          main: [[{
            node: 'Error Handler',
            type: 'main',
            index: 0
          }]]
        }
      },
      settings: { executionOrder: 'v1' },
      tags: ['fallback', 'error-recovery'],
      meta: {
        generated_by: 'universal-error-handler',
        is_fallback: true,
        original_error: error.message,
        created_at: new Date().toISOString()
      }
    };
  }

  /**
   * Create minimal viable workflow as last resort
   */
  createMinimalWorkflow(error, context) {
    return {
      id: `minimal_${Date.now()}`,
      name: 'Minimal Workflow',
      active: false,
      nodes: [{
        id: this.generateId(),
        name: 'Manual Trigger',
        type: 'n8n-nodes-base.manualTrigger',
        typeVersion: 1,
        position: [240, 300],
        parameters: {}
      }],
      connections: {},
      settings: { executionOrder: 'v1' },
      tags: ['minimal', 'error-recovery'],
      meta: {
        generated_by: 'universal-error-handler',
        is_minimal: true,
        error: error.message,
        created_at: new Date().toISOString()
      }
    };
  }

  /**
   * Build common error patterns
   */
  buildErrorPatterns() {
    return {
      missingId: /missing.*id/i,
      missingName: /missing.*name/i,
      invalidPosition: /invalid.*position/i,
      missingParameters: /missing.*parameters/i,
      invalidConnection: /invalid.*connection/i,
      orphanedNode: /orphaned.*node/i,
      circularDependency: /circular.*dependency/i
    };
  }

  /**
   * Update error statistics
   */
  updateErrorStats(issues, fixes) {
    this.errorStats.totalErrors += issues.length;
    this.errorStats.fixedErrors += fixes.length;

    for (const issue of issues) {
      for (const [pattern, regex] of Object.entries(this.errorPatterns)) {
        if (regex.test(issue)) {
          this.errorStats.errorTypes[pattern] = (this.errorStats.errorTypes[pattern] || 0) + 1;
          break;
        }
      }
    }
  }

  /**
   * Log successful handling
   */
  logSuccess(context, result) {
    if (result.fixes.length > 0) {
      console.log(`✅ Successfully handled ${result.fixes.length} issues in ${context.functionName}`);
    }
  }

  /**
   * Get error statistics
   */
  getErrorStats() {
    return {
      ...this.errorStats,
      fixRate: this.errorStats.totalErrors > 0 ? 
        (this.errorStats.fixedErrors / this.errorStats.totalErrors * 100).toFixed(2) + '%' : 
        '0%',
      recentFixes: this.fixHistory.slice(-10)
    };
  }

  /**
   * Sanitize arguments for logging
   */
  sanitizeArgs(args) {
    return args.map(arg => {
      if (typeof arg === 'string') {
        return arg.length > 100 ? arg.substring(0, 100) + '...' : arg;
      }
      return typeof arg;
    });
  }

  /**
   * Generate unique ID
   */
  generateId() {
    return 'node_' + Math.random().toString(36).substr(2, 9);
  }

  /**
   * Save error report
   */
  async saveErrorReport(filename = 'error-report.json') {
    const report = {
      timestamp: new Date().toISOString(),
      statistics: this.getErrorStats(),
      recentFixes: this.fixHistory.slice(-50),
      systemInfo: {
        nodeVersion: process.version,
        platform: process.platform
      }
    };

    fs.writeFileSync(filename, JSON.stringify(report, null, 2));
    console.log(`📊 Error report saved to: ${filename}`);
  }
}

// Export for use
module.exports = { UniversalErrorHandler };

// CLI usage
if (require.main === module) {
  const handler = new UniversalErrorHandler();
  
  console.log('🛡️ Universal Error Handler for N8N Workflows');
  console.log('This system handles errors from ANY prompt or workflow generation scenario.');
  console.log('\nUsage:');
  console.log('const { UniversalErrorHandler } = require("./universal-error-handler.js");');
  console.log('const handler = new UniversalErrorHandler();');
  console.log('const safeGenerator = handler.wrapWorkflowGenerator(yourGeneratorFunction);');
  console.log('const workflow = await safeGenerator(prompt);');
}