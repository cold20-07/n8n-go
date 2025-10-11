#!/usr/bin/env node
/**
 * N8N Workflow Connection Helper
 * Helps create properly connected workflows and prevents common issues
 */

class WorkflowConnectionHelper {
  constructor() {
    this.nodeRegistry = {
      triggers: {
        'webhook': { type: 'n8n-nodes-base.webhook', name: 'Webhook Trigger' },
        'schedule': { type: 'n8n-nodes-base.scheduleTrigger', name: 'Schedule Trigger' },
        'manual': { type: 'n8n-nodes-base.manualTrigger', name: 'Manual Trigger' }
      },
      actions: {
        'http': { type: 'n8n-nodes-base.httpRequest', name: 'HTTP Request' },
        'code': { type: 'n8n-nodes-base.code', name: 'Code' },
        'slack': { type: 'n8n-nodes-base.slack', name: 'Slack' },
        'gmail': { type: 'n8n-nodes-base.gmail', name: 'Gmail' },
        'sheets': { type: 'n8n-nodes-base.googleSheets', name: 'Google Sheets' }
      },
      logic: {
        'if': { type: 'n8n-nodes-base.if', name: 'IF' },
        'switch': { type: 'n8n-nodes-base.switch', name: 'Switch' },
        'merge': { type: 'n8n-nodes-base.merge', name: 'Merge' }
      }
    };
  }

  /**
   * Create a new workflow with proper structure
   */
  createWorkflow(name, description = '') {
    return {
      id: this.generateWorkflowId(),
      name: name,
      active: false,
      nodes: [],
      connections: {},
      settings: {
        executionOrder: 'v1'
      },
      tags: [],
      meta: {
        created_at: new Date().toISOString(),
        description: description
      }
    };
  }

  /**
   * Add a node to the workflow
   */
  addNode(workflow, nodeKey, category, customName = null, position = null) {
    const nodeConfig = this.nodeRegistry[category]?.[nodeKey];
    if (!nodeConfig) {
      throw new Error(`Unknown node: ${category}.${nodeKey}`);
    }

    const nodeId = this.generateNodeId();
    const nodeName = customName || nodeConfig.name;
    
    // Auto-position if not specified
    if (!position) {
      position = [240 + workflow.nodes.length * 220, 300];
    }

    const node = {
      id: nodeId,
      name: nodeName,
      type: nodeConfig.type,
      typeVersion: 1,
      position: position,
      parameters: this.getDefaultParameters(nodeConfig.type)
    };

    workflow.nodes.push(node);
    return node;
  }

  /**
   * Connect two nodes
   */
  connectNodes(workflow, sourceNodeName, targetNodeName, outputIndex = 0, inputIndex = 0) {
    // Validate nodes exist
    const sourceExists = workflow.nodes.some(n => n.name === sourceNodeName);
    const targetExists = workflow.nodes.some(n => n.name === targetNodeName);
    
    if (!sourceExists) {
      throw new Error(`Source node '${sourceNodeName}' not found`);
    }
    if (!targetExists) {
      throw new Error(`Target node '${targetNodeName}' not found`);
    }

    // Initialize connections if needed
    if (!workflow.connections[sourceNodeName]) {
      workflow.connections[sourceNodeName] = { main: [] };
    }
    
    if (!workflow.connections[sourceNodeName].main[outputIndex]) {
      workflow.connections[sourceNodeName].main[outputIndex] = [];
    }

    // Add connection
    workflow.connections[sourceNodeName].main[outputIndex].push({
      node: targetNodeName,
      type: 'main',
      index: inputIndex
    });

    return workflow;
  }

  /**
   * Create a linear workflow (trigger → action1 → action2 → ...)
   */
  createLinearWorkflow(name, nodeChain) {
    const workflow = this.createWorkflow(name);
    const addedNodes = [];

    // Add all nodes
    for (const nodeSpec of nodeChain) {
      const { category, nodeKey, customName } = nodeSpec;
      const node = this.addNode(workflow, nodeKey, category, customName);
      addedNodes.push(node);
    }

    // Connect nodes in sequence
    for (let i = 0; i < addedNodes.length - 1; i++) {
      this.connectNodes(workflow, addedNodes[i].name, addedNodes[i + 1].name);
    }

    return workflow;
  }

  /**
   * Create a branching workflow (trigger → condition → [action1, action2])
   */
  createBranchingWorkflow(name, trigger, condition, trueBranch, falseBranch) {
    const workflow = this.createWorkflow(name);

    // Add trigger
    const triggerNode = this.addNode(workflow, trigger.nodeKey, trigger.category, trigger.customName);
    
    // Add condition
    const conditionNode = this.addNode(workflow, condition.nodeKey, condition.category, condition.customName);
    this.connectNodes(workflow, triggerNode.name, conditionNode.name);

    // Add true branch
    const trueBranchNodes = [];
    for (const nodeSpec of trueBranch) {
      const node = this.addNode(workflow, nodeSpec.nodeKey, nodeSpec.category, nodeSpec.customName);
      trueBranchNodes.push(node);
    }
    
    // Connect true branch
    if (trueBranchNodes.length > 0) {
      this.connectNodes(workflow, conditionNode.name, trueBranchNodes[0].name, 0); // True output
      for (let i = 0; i < trueBranchNodes.length - 1; i++) {
        this.connectNodes(workflow, trueBranchNodes[i].name, trueBranchNodes[i + 1].name);
      }
    }

    // Add false branch
    const falseBranchNodes = [];
    for (const nodeSpec of falseBranch) {
      const node = this.addNode(workflow, nodeSpec.nodeKey, nodeSpec.category, nodeSpec.customName);
      falseBranchNodes.push(node);
    }
    
    // Connect false branch
    if (falseBranchNodes.length > 0) {
      this.connectNodes(workflow, conditionNode.name, falseBranchNodes[0].name, 1); // False output
      for (let i = 0; i < falseBranchNodes.length - 1; i++) {
        this.connectNodes(workflow, falseBranchNodes[i].name, falseBranchNodes[i + 1].name);
      }
    }

    return workflow;
  }

  /**
   * Validate workflow connections
   */
  validateConnections(workflow) {
    const issues = [];
    const { nodes, connections } = workflow;
    
    // Check for triggers
    const triggers = nodes.filter(node => 
      Object.values(this.nodeRegistry.triggers).some(t => t.type === node.type)
    );
    
    if (triggers.length === 0) {
      issues.push('Workflow must have at least one trigger node');
    }

    // Check all connections reference existing nodes
    for (const [sourceName, nodeConnections] of Object.entries(connections)) {
      if (!nodes.some(n => n.name === sourceName)) {
        issues.push(`Connection source '${sourceName}' does not exist`);
        continue;
      }

      if (nodeConnections.main) {
        for (const connectionGroup of nodeConnections.main) {
          for (const connection of connectionGroup) {
            if (!nodes.some(n => n.name === connection.node)) {
              issues.push(`Connection target '${connection.node}' does not exist`);
            }
          }
        }
      }
    }

    // Check for unconnected non-trigger nodes
    const connectedNodes = new Set(Object.keys(connections));
    Object.values(connections).forEach(nodeConnections => {
      if (nodeConnections.main) {
        nodeConnections.main.forEach(connectionGroup => {
          connectionGroup.forEach(connection => {
            connectedNodes.add(connection.node);
          });
        });
      }
    });

    const unconnectedNodes = nodes.filter(node => {
      const isTrigger = Object.values(this.nodeRegistry.triggers).some(t => t.type === node.type);
      return !isTrigger && !connectedNodes.has(node.name);
    });

    if (unconnectedNodes.length > 0) {
      issues.push(`Unconnected nodes: ${unconnectedNodes.map(n => n.name).join(', ')}`);
    }

    return {
      isValid: issues.length === 0,
      issues
    };
  }

  /**
   * Get default parameters for node types
   */
  getDefaultParameters(nodeType) {
    const defaults = {
      'n8n-nodes-base.webhook': {
        httpMethod: 'POST',
        path: 'webhook',
        responseMode: 'onReceived'
      },
      'n8n-nodes-base.scheduleTrigger': {
        rule: {
          interval: [{ field: 'minute', step: 10 }]
        }
      },
      'n8n-nodes-base.httpRequest': {
        method: 'GET',
        url: 'https://api.example.com'
      },
      'n8n-nodes-base.code': {
        jsCode: '// Process the input data\nconst inputData = $input.all();\nreturn inputData;'
      },
      'n8n-nodes-base.if': {
        conditions: {
          number: [{
            value1: '={{ $json.value }}',
            operation: 'equal',
            value2: 'expected'
          }]
        }
      },
      'n8n-nodes-base.slack': {
        channel: '#general',
        text: 'Hello from n8n!'
      },
      'n8n-nodes-base.gmail': {
        operation: 'send',
        subject: 'Automated Email',
        toEmail: 'recipient@example.com',
        message: 'This is an automated message.'
      }
    };

    return defaults[nodeType] || {};
  }

  /**
   * Generate unique IDs
   */
  generateWorkflowId() {
    return 'workflow_' + Date.now();
  }

  generateNodeId() {
    return 'node_' + Math.random().toString(36).substr(2, 9);
  }

  /**
   * Export workflow to JSON file
   */
  exportWorkflow(workflow, filename) {
    const fs = require('fs');
    const json = JSON.stringify(workflow, null, 2);
    fs.writeFileSync(filename, json);
    console.log(`✅ Workflow exported to: ${filename}`);
  }

  /**
   * Create common workflow templates
   */
  createTemplates() {
    return {
      // Simple webhook to Slack
      webhookToSlack: () => {
        return this.createLinearWorkflow('Webhook to Slack', [
          { category: 'triggers', nodeKey: 'webhook', customName: 'Webhook Trigger' },
          { category: 'actions', nodeKey: 'slack', customName: 'Send Slack Message' }
        ]);
      },

      // API monitoring workflow
      apiMonitoring: () => {
        const workflow = this.createWorkflow('API Monitoring');
        
        // Add nodes
        const trigger = this.addNode(workflow, 'schedule', 'triggers', 'Monitor Schedule');
        const httpRequest = this.addNode(workflow, 'http', 'actions', 'Check API');
        const condition = this.addNode(workflow, 'if', 'logic', 'Check Response');
        const alert = this.addNode(workflow, 'slack', 'actions', 'Send Alert');
        
        // Connect nodes
        this.connectNodes(workflow, trigger.name, httpRequest.name);
        this.connectNodes(workflow, httpRequest.name, condition.name);
        this.connectNodes(workflow, condition.name, alert.name, 0); // True branch only
        
        return workflow;
      },

      // Data processing pipeline
      dataProcessing: () => {
        return this.createLinearWorkflow('Data Processing Pipeline', [
          { category: 'triggers', nodeKey: 'webhook', customName: 'Data Input' },
          { category: 'actions', nodeKey: 'code', customName: 'Validate Data' },
          { category: 'actions', nodeKey: 'code', customName: 'Transform Data' },
          { category: 'actions', nodeKey: 'sheets', customName: 'Save to Sheets' },
          { category: 'actions', nodeKey: 'slack', customName: 'Notify Completion' }
        ]);
      }
    };
  }
}

// CLI usage and examples
async function main() {
  const helper = new WorkflowConnectionHelper();
  
  console.log('🔧 N8N Workflow Connection Helper');
  console.log('Creating example workflows...\n');

  // Create templates
  const templates = helper.createTemplates();

  // 1. Simple webhook to Slack
  const webhookSlack = templates.webhookToSlack();
  const validation1 = helper.validateConnections(webhookSlack);
  console.log('📝 Webhook to Slack:');
  console.log(`   Nodes: ${webhookSlack.nodes.length}`);
  console.log(`   Valid: ${validation1.isValid ? '✅' : '❌'}`);
  if (!validation1.isValid) {
    validation1.issues.forEach(issue => console.log(`   - ${issue}`));
  }
  helper.exportWorkflow(webhookSlack, 'webhook-to-slack.json');

  // 2. API monitoring
  const apiMonitoring = templates.apiMonitoring();
  const validation2 = helper.validateConnections(apiMonitoring);
  console.log('\n📊 API Monitoring:');
  console.log(`   Nodes: ${apiMonitoring.nodes.length}`);
  console.log(`   Valid: ${validation2.isValid ? '✅' : '❌'}`);
  if (!validation2.isValid) {
    validation2.issues.forEach(issue => console.log(`   - ${issue}`));
  }
  helper.exportWorkflow(apiMonitoring, 'api-monitoring.json');

  // 3. Data processing pipeline
  const dataProcessing = templates.dataProcessing();
  const validation3 = helper.validateConnections(dataProcessing);
  console.log('\n🔄 Data Processing Pipeline:');
  console.log(`   Nodes: ${dataProcessing.nodes.length}`);
  console.log(`   Valid: ${validation3.isValid ? '✅' : '❌'}`);
  if (!validation3.isValid) {
    validation3.issues.forEach(issue => console.log(`   - ${issue}`));
  }
  helper.exportWorkflow(dataProcessing, 'data-processing-pipeline.json');

  console.log('\n✅ Example workflows created successfully!');
  console.log('📁 Files created:');
  console.log('   - webhook-to-slack.json');
  console.log('   - api-monitoring.json');
  console.log('   - data-processing-pipeline.json');
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { WorkflowConnectionHelper };