#!/usr/bin/env node
/**
 * N8N Workflow Node Validator and Fixer
 * Identifies and fixes unconnected and invalid nodes in n8n workflows
 */

const fs = require('fs');
const path = require('path');

class WorkflowNodeValidator {
  constructor() {
    this.validNodeTypes = {
      // Trigger nodes
      'n8n-nodes-base.webhook': { category: 'trigger', requiresInput: false },
      'n8n-nodes-base.scheduleTrigger': { category: 'trigger', requiresInput: false },
      'n8n-nodes-base.manualTrigger': { category: 'trigger', requiresInput: false },
      
      // Action nodes
      'n8n-nodes-base.httpRequest': { category: 'action', requiresInput: true },
      'n8n-nodes-base.code': { category: 'action', requiresInput: true },
      'n8n-nodes-base.if': { category: 'logic', requiresInput: true },
      'n8n-nodes-base.slack': { category: 'communication', requiresInput: true },
      'n8n-nodes-base.gmail': { category: 'communication', requiresInput: true },
      'n8n-nodes-base.googleSheets': { category: 'productivity', requiresInput: true },
      'n8n-nodes-base.trello': { category: 'productivity', requiresInput: true },
      'n8n-nodes-base.shopify': { category: 'ecommerce', requiresInput: true },
      'n8n-nodes-base.airtable': { category: 'database', requiresInput: true },
      'n8n-nodes-base.notion': { category: 'productivity', requiresInput: true },
      'n8n-nodes-base.github': { category: 'development', requiresInput: true },
      'n8n-nodes-base.telegram': { category: 'communication', requiresInput: true },
      'n8n-nodes-base.discord': { category: 'communication', requiresInput: true },
      'n8n-nodes-base.microsoftTeams': { category: 'communication', requiresInput: true },
      'n8n-nodes-base.openAi': { category: 'ai', requiresInput: true },
      'n8n-nodes-base.stripe': { category: 'payment', requiresInput: true },
      'n8n-nodes-base.payPal': { category: 'payment', requiresInput: true },
      'n8n-nodes-base.mongoDb': { category: 'database', requiresInput: true },
      'n8n-nodes-base.mySql': { category: 'database', requiresInput: true },
      
      // Additional valid node types
      'n8n-nodes-base.splitInBatches': { category: 'utility', requiresInput: true },
      'n8n-nodes-base.html': { category: 'utility', requiresInput: true },
      'n8n-nodes-base.set': { category: 'utility', requiresInput: true },
      'n8n-nodes-base.emailSend': { category: 'communication', requiresInput: true },
      'n8n-nodes-base.wait': { category: 'utility', requiresInput: true },
      'n8n-nodes-base.merge': { category: 'utility', requiresInput: true },
      'n8n-nodes-base.function': { category: 'utility', requiresInput: true },
      'n8n-nodes-base.switch': { category: 'logic', requiresInput: true },
      'n8n-nodes-base.rssFeedRead': { category: 'trigger', requiresInput: false },
      'n8n-nodes-base.itemLists': { category: 'utility', requiresInput: true },
      'n8n-nodes-base.filter': { category: 'utility', requiresInput: true }
    };
  }

  /**
   * Validate and fix a workflow
   */
  validateAndFixWorkflow(workflow) {
    const issues = [];
    const fixes = [];
    
    console.log(`🔍 Validating workflow: ${workflow.name || 'Unnamed'}`);
    
    // 1. Validate nodes
    const nodeIssues = this.validateNodes(workflow.nodes);
    issues.push(...nodeIssues.issues);
    
    // 2. Validate connections
    const connectionIssues = this.validateConnections(workflow.nodes, workflow.connections);
    issues.push(...connectionIssues.issues);
    
    // 3. Fix unconnected nodes
    const fixedConnections = this.fixUnconnectedNodes(workflow.nodes, workflow.connections);
    if (fixedConnections.fixed) {
      workflow.connections = fixedConnections.connections;
      fixes.push(...fixedConnections.fixes);
    }
    
    // 4. Fix invalid nodes
    const fixedNodes = this.fixInvalidNodes(workflow.nodes);
    if (fixedNodes.fixed) {
      workflow.nodes = fixedNodes.nodes;
      fixes.push(...fixedNodes.fixes);
    }
    
    return {
      isValid: issues.length === 0,
      issues,
      fixes,
      workflow
    };
  }

  /**
   * Validate individual nodes
   */
  validateNodes(nodes) {
    const issues = [];
    const nodeNames = new Set();
    
    for (const node of nodes) {
      // Check for duplicate node names
      if (nodeNames.has(node.name)) {
        issues.push(`Duplicate node name: ${node.name}`);
      }
      nodeNames.add(node.name);
      
      // Check required fields
      if (!node.id) issues.push(`Node ${node.name} missing id`);
      if (!node.name) issues.push(`Node missing name`);
      if (!node.type) issues.push(`Node ${node.name} missing type`);
      if (!node.position || !Array.isArray(node.position)) {
        issues.push(`Node ${node.name} missing or invalid position`);
      }
      
      // Check if node type is valid
      if (node.type && !this.validNodeTypes[node.type]) {
        issues.push(`Invalid node type: ${node.type} in node ${node.name}`);
      }
      
      // Check typeVersion
      if (!node.typeVersion) {
        issues.push(`Node ${node.name} missing typeVersion`);
      }
    }
    
    return { issues };
  }

  /**
   * Validate node connections
   */
  validateConnections(nodes, connections) {
    const issues = [];
    const nodeNames = nodes.map(n => n.name);
    const connectedNodes = new Set();
    const triggerNodes = nodes.filter(n => 
      this.validNodeTypes[n.type] && !this.validNodeTypes[n.type].requiresInput
    );
    
    // Check if connections reference existing nodes
    for (const [sourceName, nodeConnections] of Object.entries(connections)) {
      if (!nodeNames.includes(sourceName)) {
        issues.push(`Connection source '${sourceName}' does not exist`);
        continue;
      }
      
      connectedNodes.add(sourceName);
      
      if (nodeConnections.main) {
        for (const connectionGroup of nodeConnections.main) {
          for (const connection of connectionGroup) {
            if (!nodeNames.includes(connection.node)) {
              issues.push(`Connection target '${connection.node}' does not exist`);
            } else {
              connectedNodes.add(connection.node);
            }
          }
        }
      }
    }
    
    // Check for unconnected nodes (except triggers)
    for (const node of nodes) {
      const nodeSpec = this.validNodeTypes[node.type];
      if (nodeSpec && nodeSpec.requiresInput && !connectedNodes.has(node.name)) {
        issues.push(`Unconnected node: ${node.name} (requires input connection)`);
      }
    }
    
    // Check if workflow has at least one trigger
    if (triggerNodes.length === 0) {
      issues.push('Workflow has no trigger nodes');
    }
    
    return { issues };
  }

  /**
   * Fix unconnected nodes by creating proper connections
   */
  fixUnconnectedNodes(nodes, connections) {
    const fixes = [];
    let fixed = false;
    const newConnections = { ...connections };
    
    const triggerNodes = nodes.filter(n => 
      this.validNodeTypes[n.type] && !this.validNodeTypes[n.type].requiresInput
    );
    
    const actionNodes = nodes.filter(n => 
      this.validNodeTypes[n.type] && this.validNodeTypes[n.type].requiresInput
    );
    
    // Get currently connected nodes
    const connectedNodes = new Set();
    for (const nodeConnections of Object.values(connections)) {
      if (nodeConnections.main) {
        for (const connectionGroup of nodeConnections.main) {
          for (const connection of connectionGroup) {
            connectedNodes.add(connection.node);
          }
        }
      }
    }
    
    // Find unconnected action nodes
    const unconnectedNodes = actionNodes.filter(node => !connectedNodes.has(node.name));
    
    if (unconnectedNodes.length > 0 && triggerNodes.length > 0) {
      // Connect unconnected nodes in sequence
      let previousNode = triggerNodes[0]; // Start with first trigger
      
      for (const unconnectedNode of unconnectedNodes) {
        if (!newConnections[previousNode.name]) {
          newConnections[previousNode.name] = { main: [[]] };
        }
        
        if (!newConnections[previousNode.name].main[0]) {
          newConnections[previousNode.name].main[0] = [];
        }
        
        // Add connection
        newConnections[previousNode.name].main[0].push({
          node: unconnectedNode.name,
          type: 'main',
          index: 0
        });
        
        fixes.push(`Connected ${previousNode.name} → ${unconnectedNode.name}`);
        previousNode = unconnectedNode;
        fixed = true;
      }
    }
    
    return { fixed, connections: newConnections, fixes };
  }

  /**
   * Fix invalid nodes by correcting common issues
   */
  fixInvalidNodes(nodes) {
    const fixes = [];
    let fixed = false;
    const newNodes = [...nodes];
    
    for (let i = 0; i < newNodes.length; i++) {
      const node = newNodes[i];
      
      // Fix missing id
      if (!node.id) {
        node.id = this.generateNodeId();
        fixes.push(`Added missing id to node: ${node.name}`);
        fixed = true;
      }
      
      // Fix missing typeVersion
      if (!node.typeVersion) {
        node.typeVersion = 1; // Default to version 1
        fixes.push(`Added missing typeVersion to node: ${node.name}`);
        fixed = true;
      }
      
      // Fix missing position
      if (!node.position || !Array.isArray(node.position)) {
        node.position = [240 + i * 220, 300]; // Default positioning
        fixes.push(`Fixed position for node: ${node.name}`);
        fixed = true;
      }
      
      // Fix missing parameters
      if (!node.parameters) {
        node.parameters = {};
        fixes.push(`Added missing parameters to node: ${node.name}`);
        fixed = true;
      }
      
      // Fix invalid node types (replace with code node)
      if (node.type && !this.validNodeTypes[node.type]) {
        node.type = 'n8n-nodes-base.code';
        node.parameters = {
          jsCode: `// Converted from invalid node type
const inputData = $input.all();
return inputData;`
        };
        fixes.push(`Converted invalid node type to code node: ${node.name}`);
        fixed = true;
      }
    }
    
    return { fixed, nodes: newNodes, fixes };
  }

  /**
   * Generate a unique node ID
   */
  generateNodeId() {
    return 'node_' + Math.random().toString(36).substr(2, 9);
  }

  /**
   * Validate and fix workflow from file
   */
  async validateWorkflowFile(filePath) {
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      const workflow = JSON.parse(content);
      
      const result = this.validateAndFixWorkflow(workflow);
      
      if (result.fixes.length > 0) {
        // Create backup
        const backupPath = filePath + '.backup';
        fs.writeFileSync(backupPath, content);
        console.log(`📁 Backup created: ${backupPath}`);
        
        // Write fixed workflow
        fs.writeFileSync(filePath, JSON.stringify(result.workflow, null, 2));
        console.log(`✅ Fixed workflow saved: ${filePath}`);
      }
      
      return result;
    } catch (error) {
      return {
        isValid: false,
        issues: [`Failed to process file: ${error.message}`],
        fixes: [],
        workflow: null
      };
    }
  }

  /**
   * Scan and fix all workflow files in a directory
   */
  async scanAndFixWorkflows(directory = '.') {
    const results = [];
    
    try {
      const files = fs.readdirSync(directory);
      const workflowFiles = files.filter(file => 
        file.endsWith('.json') && 
        (file.includes('workflow') || file.includes('n8n'))
      );
      
      console.log(`🔍 Found ${workflowFiles.length} potential workflow files`);
      
      for (const file of workflowFiles) {
        const filePath = path.join(directory, file);
        console.log(`\n📄 Processing: ${file}`);
        
        const result = await this.validateWorkflowFile(filePath);
        result.file = file;
        results.push(result);
        
        // Display results
        if (result.isValid && result.fixes.length === 0) {
          console.log(`   ✅ Valid workflow - no issues found`);
        } else if (result.fixes.length > 0) {
          console.log(`   🔧 Fixed ${result.fixes.length} issues:`);
          result.fixes.forEach(fix => console.log(`      - ${fix}`));
        }
        
        if (result.issues.length > 0) {
          console.log(`   ❌ Remaining issues:`);
          result.issues.forEach(issue => console.log(`      - ${issue}`));
        }
      }
      
    } catch (error) {
      console.error(`Error scanning directory: ${error.message}`);
    }
    
    return results;
  }
}

// CLI usage
async function main() {
  const validator = new WorkflowNodeValidator();
  
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('🔧 N8N Workflow Node Validator and Fixer');
    console.log('Usage:');
    console.log('  node fix-workflow-nodes.js <file.json>     # Fix specific file');
    console.log('  node fix-workflow-nodes.js --scan         # Scan current directory');
    console.log('  node fix-workflow-nodes.js --scan <dir>   # Scan specific directory');
    return;
  }
  
  if (args[0] === '--scan') {
    const directory = args[1] || '.';
    console.log(`🔍 Scanning directory: ${directory}`);
    const results = await validator.scanAndFixWorkflows(directory);
    
    // Summary
    const totalFiles = results.length;
    const validFiles = results.filter(r => r.isValid && r.fixes.length === 0).length;
    const fixedFiles = results.filter(r => r.fixes.length > 0).length;
    const errorFiles = results.filter(r => !r.isValid && r.fixes.length === 0).length;
    
    console.log('\n📊 Summary:');
    console.log(`   Total files: ${totalFiles}`);
    console.log(`   Valid files: ${validFiles}`);
    console.log(`   Fixed files: ${fixedFiles}`);
    console.log(`   Error files: ${errorFiles}`);
    
  } else {
    // Fix specific file
    const filePath = args[0];
    console.log(`🔧 Fixing workflow file: ${filePath}`);
    const result = await validator.validateWorkflowFile(filePath);
    
    if (result.isValid && result.fixes.length === 0) {
      console.log('✅ Workflow is valid - no issues found');
    } else if (result.fixes.length > 0) {
      console.log(`🔧 Applied ${result.fixes.length} fixes:`);
      result.fixes.forEach(fix => console.log(`   - ${fix}`));
    }
    
    if (result.issues.length > 0) {
      console.log(`❌ Remaining issues:`);
      result.issues.forEach(issue => console.log(`   - ${issue}`));
    }
  }
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { WorkflowNodeValidator };