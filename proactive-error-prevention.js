#!/usr/bin/env node
/**
 * Proactive Error Prevention System for N8N Workflows
 * Automatically prevents and fixes node connection issues in any scenario
 */

const fs = require('fs');
const path = require('path');

class ProactiveErrorPrevention {
  constructor() {
    this.validationRules = {
      // Critical validation rules that must always pass
      critical: [
        'mustHaveTrigger',
        'noOrphanedNodes', 
        'validConnections',
        'noCircularDeps'
      ],
      // Warning rules that should be checked but not block generation
      warnings: [
        'nodeNaming',
        'positionOverlap',
        'parameterCompleteness'
      ]
    };

    this.autoFixStrategies = {
      'missingTrigger': this.addDefaultTrigger.bind(this),
      'orphanedNodes': this.connectOrphanedNodes.bind(this),
      'invalidConnections': this.fixInvalidConnections.bind(this),
      'circularDependency': this.breakCircularDependency.bind(this),
      'missingParameters': this.addDefaultParameters.bind(this),
      'invalidNodeType': this.replaceInvalidNodeType.bind(this)
    };

    this.nodeTypeRegistry = this.buildNodeTypeRegistry();
  }

  /**
   * Main entry point - validate and fix any workflow
   */
  async validateAndFixAnyWorkflow(workflow, context = {}) {
    console.log(`🔍 Proactive validation: ${workflow.name || 'Unnamed Workflow'}`);
    
    const issues = [];
    const fixes = [];
    let isValid = true;

    try {
      // 1. Pre-validation checks
      const preCheck = this.preValidationCheck(workflow);
      if (!preCheck.isValid) {
        issues.push(...preCheck.issues);
        isValid = false;
      }

      // 2. Critical validation rules
      for (const rule of this.validationRules.critical) {
        const result = await this.runValidationRule(rule, workflow);
        if (!result.isValid) {
          issues.push(...result.issues);
          isValid = false;
          
          // Auto-fix if strategy exists
          const fixStrategy = this.getFixStrategy(result.errorType);
          if (fixStrategy) {
            const fixResult = await fixStrategy(workflow, result);
            if (fixResult.success) {
              fixes.push(...fixResult.fixes);
              console.log(`   🔧 Auto-fixed: ${result.errorType}`);
            }
          }
        }
      }

      // 3. Warning checks (non-blocking)
      const warnings = [];
      for (const rule of this.validationRules.warnings) {
        const result = await this.runValidationRule(rule, workflow);
        if (!result.isValid) {
          warnings.push(...result.issues);
        }
      }

      // 4. Post-fix validation
      if (fixes.length > 0) {
        const postValidation = await this.validateAndFixAnyWorkflow(workflow, { ...context, isRetry: true });
        if (postValidation.isValid) {
          console.log(`   ✅ All issues resolved after auto-fix`);
        }
      }

      return {
        isValid: isValid || fixes.length > 0,
        issues,
        fixes,
        warnings,
        workflow,
        metadata: {
          validationTimestamp: new Date().toISOString(),
          rulesApplied: this.validationRules.critical.length,
          autoFixesApplied: fixes.length,
          context
        }
      };

    } catch (error) {
      console.error(`❌ Validation error: ${error.message}`);
      return {
        isValid: false,
        issues: [`Validation failed: ${error.message}`],
        fixes: [],
        warnings: [],
        workflow,
        error: error.message
      };
    }
  }

  /**
   * Pre-validation basic structure check
   */
  preValidationCheck(workflow) {
    const issues = [];

    if (!workflow) {
      issues.push('Workflow object is null or undefined');
    }

    if (!workflow.nodes || !Array.isArray(workflow.nodes)) {
      issues.push('Workflow must have a nodes array');
    }

    if (!workflow.connections || typeof workflow.connections !== 'object') {
      issues.push('Workflow must have a connections object');
    }

    if (workflow.nodes && workflow.nodes.length === 0) {
      issues.push('Workflow must have at least one node');
    }

    return {
      isValid: issues.length === 0,
      issues
    };
  }

  /**
   * Run individual validation rule
   */
  async runValidationRule(ruleName, workflow) {
    switch (ruleName) {
      case 'mustHaveTrigger':
        return this.validateTriggerExists(workflow);
      
      case 'noOrphanedNodes':
        return this.validateNoOrphanedNodes(workflow);
      
      case 'validConnections':
        return this.validateConnections(workflow);
      
      case 'noCircularDeps':
        return this.validateNoCircularDependencies(workflow);
      
      case 'nodeNaming':
        return this.validateNodeNaming(workflow);
      
      case 'positionOverlap':
        return this.validateNodePositions(workflow);
      
      case 'parameterCompleteness':
        return this.validateParameters(workflow);
      
      default:
        return { isValid: true, issues: [] };
    }
  }

  /**
   * Validate trigger exists
   */
  validateTriggerExists(workflow) {
    const triggerTypes = [
      'n8n-nodes-base.webhook',
      'n8n-nodes-base.scheduleTrigger',
      'n8n-nodes-base.manualTrigger',
      'n8n-nodes-base.rssFeedRead'
    ];

    const triggers = workflow.nodes.filter(node => 
      triggerTypes.includes(node.type)
    );

    if (triggers.length === 0) {
      return {
        isValid: false,
        issues: ['Workflow must have at least one trigger node'],
        errorType: 'missingTrigger'
      };
    }

    return { isValid: true, issues: [] };
  }

  /**
   * Validate no orphaned nodes
   */
  validateNoOrphanedNodes(workflow) {
    const connectedNodes = new Set();
    
    // Add all nodes with outgoing connections
    Object.keys(workflow.connections).forEach(nodeName => {
      connectedNodes.add(nodeName);
    });
    
    // Add all nodes with incoming connections
    Object.values(workflow.connections).forEach(nodeConnections => {
      if (nodeConnections.main) {
        nodeConnections.main.forEach(connectionGroup => {
          connectionGroup.forEach(connection => {
            connectedNodes.add(connection.node);
          });
        });
      }
    });

    const triggerTypes = [
      'n8n-nodes-base.webhook',
      'n8n-nodes-base.scheduleTrigger', 
      'n8n-nodes-base.manualTrigger'
    ];

    const orphanedNodes = workflow.nodes.filter(node => {
      const isTrigger = triggerTypes.includes(node.type);
      return !isTrigger && !connectedNodes.has(node.name);
    });

    if (orphanedNodes.length > 0) {
      return {
        isValid: false,
        issues: [`Found ${orphanedNodes.length} orphaned nodes: ${orphanedNodes.map(n => n.name).join(', ')}`],
        errorType: 'orphanedNodes',
        orphanedNodes
      };
    }

    return { isValid: true, issues: [] };
  }

  /**
   * Validate connections reference existing nodes
   */
  validateConnections(workflow) {
    const issues = [];
    const nodeNames = workflow.nodes.map(n => n.name);
    const invalidConnections = [];

    for (const [sourceName, nodeConnections] of Object.entries(workflow.connections)) {
      if (!nodeNames.includes(sourceName)) {
        issues.push(`Connection source '${sourceName}' does not exist`);
        invalidConnections.push({ type: 'missingSource', source: sourceName });
        continue;
      }

      if (nodeConnections.main) {
        for (const connectionGroup of nodeConnections.main) {
          for (const connection of connectionGroup) {
            if (!nodeNames.includes(connection.node)) {
              issues.push(`Connection target '${connection.node}' does not exist`);
              invalidConnections.push({ 
                type: 'missingTarget', 
                source: sourceName, 
                target: connection.node 
              });
            }
          }
        }
      }
    }

    if (issues.length > 0) {
      return {
        isValid: false,
        issues,
        errorType: 'invalidConnections',
        invalidConnections
      };
    }

    return { isValid: true, issues: [] };
  }

  /**
   * Validate no circular dependencies
   */
  validateNoCircularDependencies(workflow) {
    const visited = new Set();
    const recursionStack = new Set();
    
    const hasCycle = (nodeName, path = []) => {
      if (recursionStack.has(nodeName)) {
        const cycleStart = path.indexOf(nodeName);
        return path.slice(cycleStart).concat([nodeName]);
      }
      
      if (visited.has(nodeName)) return null;
      
      visited.add(nodeName);
      recursionStack.add(nodeName);
      path.push(nodeName);
      
      const nodeConnections = workflow.connections[nodeName];
      if (nodeConnections && nodeConnections.main) {
        for (const connectionGroup of nodeConnections.main) {
          for (const connection of connectionGroup) {
            const cycle = hasCycle(connection.node, [...path]);
            if (cycle) return cycle;
          }
        }
      }
      
      recursionStack.delete(nodeName);
      path.pop();
      return null;
    };

    for (const node of workflow.nodes) {
      if (!visited.has(node.name)) {
        const cycle = hasCycle(node.name);
        if (cycle) {
          return {
            isValid: false,
            issues: [`Circular dependency detected: ${cycle.join(' → ')}`],
            errorType: 'circularDependency',
            cycle
          };
        }
      }
    }

    return { isValid: true, issues: [] };
  }

  /**
   * Validate node naming
   */
  validateNodeNaming(workflow) {
    const issues = [];
    const nodeNames = new Set();

    for (const node of workflow.nodes) {
      if (!node.name || node.name.trim() === '') {
        issues.push(`Node ${node.id} has empty or missing name`);
      }
      
      if (nodeNames.has(node.name)) {
        issues.push(`Duplicate node name: ${node.name}`);
      }
      
      nodeNames.add(node.name);
    }

    return {
      isValid: issues.length === 0,
      issues
    };
  }

  /**
   * Validate node positions don't overlap
   */
  validateNodePositions(workflow) {
    const issues = [];
    const positions = new Map();

    for (const node of workflow.nodes) {
      if (!node.position || !Array.isArray(node.position)) {
        issues.push(`Node ${node.name} has invalid position`);
        continue;
      }

      const posKey = `${node.position[0]},${node.position[1]}`;
      if (positions.has(posKey)) {
        issues.push(`Nodes ${positions.get(posKey)} and ${node.name} have overlapping positions`);
      } else {
        positions.set(posKey, node.name);
      }
    }

    return {
      isValid: issues.length === 0,
      issues
    };
  }

  /**
   * Validate node parameters
   */
  validateParameters(workflow) {
    const issues = [];

    for (const node of workflow.nodes) {
      if (!node.parameters) {
        issues.push(`Node ${node.name} missing parameters object`);
      }

      if (!node.type) {
        issues.push(`Node ${node.name} missing type`);
      }

      if (!node.typeVersion) {
        issues.push(`Node ${node.name} missing typeVersion`);
      }
    }

    return {
      isValid: issues.length === 0,
      issues
    };
  }

  /**
   * Get fix strategy for error type
   */
  getFixStrategy(errorType) {
    return this.autoFixStrategies[errorType] || null;
  }

  /**
   * Add default trigger node
   */
  async addDefaultTrigger(workflow, validationResult) {
    const triggerNode = {
      id: this.generateNodeId(),
      name: 'Manual Trigger',
      type: 'n8n-nodes-base.manualTrigger',
      typeVersion: 1,
      position: [240, 300],
      parameters: {}
    };

    workflow.nodes.unshift(triggerNode);

    // Connect to first non-trigger node
    const firstActionNode = workflow.nodes.find(node => 
      !['n8n-nodes-base.webhook', 'n8n-nodes-base.scheduleTrigger', 'n8n-nodes-base.manualTrigger'].includes(node.type)
    );

    if (firstActionNode) {
      workflow.connections[triggerNode.name] = {
        main: [[{
          node: firstActionNode.name,
          type: 'main',
          index: 0
        }]]
      };
    }

    return {
      success: true,
      fixes: ['Added missing trigger node and connected to workflow']
    };
  }

  /**
   * Connect orphaned nodes
   */
  async connectOrphanedNodes(workflow, validationResult) {
    const fixes = [];
    const { orphanedNodes } = validationResult;

    const triggers = workflow.nodes.filter(node => 
      ['n8n-nodes-base.webhook', 'n8n-nodes-base.scheduleTrigger', 'n8n-nodes-base.manualTrigger'].includes(node.type)
    );

    if (triggers.length === 0) {
      return { success: false, fixes: ['No trigger nodes available to connect orphaned nodes'] };
    }

    const lastConnectedNode = this.findLastConnectedNode(workflow) || triggers[0];

    for (const orphanedNode of orphanedNodes) {
      if (!workflow.connections[lastConnectedNode.name]) {
        workflow.connections[lastConnectedNode.name] = { main: [[]] };
      }

      if (!workflow.connections[lastConnectedNode.name].main[0]) {
        workflow.connections[lastConnectedNode.name].main[0] = [];
      }

      workflow.connections[lastConnectedNode.name].main[0].push({
        node: orphanedNode.name,
        type: 'main',
        index: 0
      });

      fixes.push(`Connected orphaned node: ${lastConnectedNode.name} → ${orphanedNode.name}`);
    }

    return { success: true, fixes };
  }

  /**
   * Fix invalid connections
   */
  async fixInvalidConnections(workflow, validationResult) {
    const fixes = [];
    const { invalidConnections } = validationResult;

    for (const invalidConn of invalidConnections) {
      if (invalidConn.type === 'missingSource') {
        // Remove connections from non-existent source
        delete workflow.connections[invalidConn.source];
        fixes.push(`Removed connections from non-existent source: ${invalidConn.source}`);
      } else if (invalidConn.type === 'missingTarget') {
        // Remove connection to non-existent target
        const sourceConnections = workflow.connections[invalidConn.source];
        if (sourceConnections && sourceConnections.main) {
          sourceConnections.main = sourceConnections.main.map(connectionGroup =>
            connectionGroup.filter(conn => conn.node !== invalidConn.target)
          ).filter(group => group.length > 0);
          
          if (sourceConnections.main.length === 0) {
            delete workflow.connections[invalidConn.source];
          }
        }
        fixes.push(`Removed invalid connection: ${invalidConn.source} → ${invalidConn.target}`);
      }
    }

    return { success: true, fixes };
  }

  /**
   * Break circular dependency
   */
  async breakCircularDependency(workflow, validationResult) {
    const { cycle } = validationResult;
    
    if (cycle.length < 2) {
      return { success: false, fixes: ['Cannot break circular dependency - invalid cycle'] };
    }

    // Break the cycle by removing the last connection
    const lastNode = cycle[cycle.length - 2];
    const firstNode = cycle[0];

    const sourceConnections = workflow.connections[lastNode];
    if (sourceConnections && sourceConnections.main) {
      sourceConnections.main = sourceConnections.main.map(connectionGroup =>
        connectionGroup.filter(conn => conn.node !== firstNode)
      ).filter(group => group.length > 0);
      
      if (sourceConnections.main.length === 0) {
        delete workflow.connections[lastNode];
      }
    }

    return {
      success: true,
      fixes: [`Broke circular dependency by removing connection: ${lastNode} → ${firstNode}`]
    };
  }

  /**
   * Add default parameters
   */
  async addDefaultParameters(workflow, validationResult) {
    const fixes = [];

    for (const node of workflow.nodes) {
      if (!node.parameters) {
        node.parameters = {};
        fixes.push(`Added missing parameters to node: ${node.name}`);
      }

      if (!node.typeVersion) {
        node.typeVersion = 1;
        fixes.push(`Added missing typeVersion to node: ${node.name}`);
      }

      if (!node.position) {
        node.position = [240, 300];
        fixes.push(`Added missing position to node: ${node.name}`);
      }
    }

    return { success: true, fixes };
  }

  /**
   * Replace invalid node type
   */
  async replaceInvalidNodeType(workflow, validationResult) {
    const fixes = [];

    for (const node of workflow.nodes) {
      if (!this.nodeTypeRegistry[node.type]) {
        node.type = 'n8n-nodes-base.code';
        node.parameters = {
          jsCode: '// Converted from invalid node type\nconst inputData = $input.all();\nreturn inputData;'
        };
        fixes.push(`Replaced invalid node type with code node: ${node.name}`);
      }
    }

    return { success: true, fixes };
  }

  /**
   * Build node type registry
   */
  buildNodeTypeRegistry() {
    return {
      'n8n-nodes-base.webhook': true,
      'n8n-nodes-base.scheduleTrigger': true,
      'n8n-nodes-base.manualTrigger': true,
      'n8n-nodes-base.httpRequest': true,
      'n8n-nodes-base.code': true,
      'n8n-nodes-base.if': true,
      'n8n-nodes-base.slack': true,
      'n8n-nodes-base.gmail': true,
      'n8n-nodes-base.googleSheets': true,
      'n8n-nodes-base.trello': true,
      'n8n-nodes-base.shopify': true,
      'n8n-nodes-base.airtable': true,
      'n8n-nodes-base.notion': true,
      'n8n-nodes-base.github': true,
      'n8n-nodes-base.telegram': true,
      'n8n-nodes-base.discord': true,
      'n8n-nodes-base.openAi': true,
      'n8n-nodes-base.stripe': true,
      'n8n-nodes-base.mongoDb': true,
      'n8n-nodes-base.mySql': true
    };
  }

  /**
   * Find last connected node
   */
  findLastConnectedNode(workflow) {
    const endNodes = workflow.nodes.filter(node => !workflow.connections[node.name]);
    return endNodes.length > 0 ? endNodes[0] : workflow.nodes[workflow.nodes.length - 1];
  }

  /**
   * Generate unique node ID
   */
  generateNodeId() {
    return 'node_' + Math.random().toString(36).substr(2, 9);
  }

  /**
   * Monitor and auto-fix workflows in real-time
   */
  async monitorWorkflowGeneration(workflowGeneratorFunction) {
    return async (...args) => {
      try {
        // Call original workflow generator
        const workflow = await workflowGeneratorFunction(...args);
        
        // Auto-validate and fix
        const validationResult = await this.validateAndFixAnyWorkflow(workflow, {
          source: 'realtime_generation',
          timestamp: new Date().toISOString()
        });

        if (!validationResult.isValid && validationResult.fixes.length === 0) {
          console.warn('⚠️ Workflow validation failed and could not be auto-fixed');
          console.warn('Issues:', validationResult.issues);
        }

        return validationResult.workflow;
      } catch (error) {
        console.error('❌ Error in workflow generation monitoring:', error);
        throw error;
      }
    };
  }
}

// Export for use in other modules
module.exports = { ProactiveErrorPrevention };

// CLI usage
if (require.main === module) {
  const prevention = new ProactiveErrorPrevention();
  
  console.log('🛡️ Proactive Error Prevention System');
  console.log('This system will automatically prevent and fix node connection issues.');
  console.log('Use this module in your workflow generation code to ensure reliability.');
  console.log('\nExample usage:');
  console.log('const { ProactiveErrorPrevention } = require("./proactive-error-prevention.js");');
  console.log('const prevention = new ProactiveErrorPrevention();');
  console.log('const result = await prevention.validateAndFixAnyWorkflow(workflow);');
}