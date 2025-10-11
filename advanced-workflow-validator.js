#!/usr/bin/env node
/**
 * Advanced N8N Workflow Connection Validator
 * Detects and fixes complex workflow connection issues
 */

const fs = require('fs');

class AdvancedWorkflowValidator {
  constructor() {
    this.nodeTypes = {
      triggers: [
        'n8n-nodes-base.webhook',
        'n8n-nodes-base.scheduleTrigger', 
        'n8n-nodes-base.manualTrigger',
        'n8n-nodes-base.rssFeedRead'
      ],
      logic: [
        'n8n-nodes-base.if',
        'n8n-nodes-base.switch',
        'n8n-nodes-base.merge'
      ],
      processing: [
        'n8n-nodes-base.code',
        'n8n-nodes-base.function',
        'n8n-nodes-base.set'
      ]
    };
  }

  /**
   * Comprehensive workflow validation
   */
  validateWorkflowConnections(workflow) {
    const issues = [];
    const fixes = [];
    const { nodes, connections } = workflow;
    
    console.log(`🔍 Advanced validation for: ${workflow.name}`);
    
    // 1. Check for orphaned nodes
    const orphanedNodes = this.findOrphanedNodes(nodes, connections);
    if (orphanedNodes.length > 0) {
      issues.push(`Found ${orphanedNodes.length} orphaned nodes: ${orphanedNodes.map(n => n.name).join(', ')}`);
    }
    
    // 2. Check for circular dependencies
    const circularDeps = this.detectCircularDependencies(nodes, connections);
    if (circularDeps.length > 0) {
      issues.push(`Circular dependencies detected: ${circularDeps.join(' → ')}`);
    }
    
    // 3. Check for unreachable nodes
    const unreachableNodes = this.findUnreachableNodes(nodes, connections);
    if (unreachableNodes.length > 0) {
      issues.push(`Unreachable nodes: ${unreachableNodes.map(n => n.name).join(', ')}`);
    }
    
    // 4. Validate data flow
    const dataFlowIssues = this.validateDataFlow(nodes, connections);
    issues.push(...dataFlowIssues);
    
    // 5. Check for missing trigger
    const triggerIssues = this.validateTriggers(nodes);
    issues.push(...triggerIssues);
    
    return {
      isValid: issues.length === 0,
      issues,
      orphanedNodes,
      unreachableNodes,
      circularDependencies: circularDeps
    };
  }

  /**
   * Find nodes that have no connections (input or output)
   */
  findOrphanedNodes(nodes, connections) {
    const connectedNodes = new Set();
    
    // Add all nodes that have outgoing connections
    Object.keys(connections).forEach(nodeName => {
      connectedNodes.add(nodeName);
    });
    
    // Add all nodes that have incoming connections
    Object.values(connections).forEach(nodeConnections => {
      if (nodeConnections.main) {
        nodeConnections.main.forEach(connectionGroup => {
          connectionGroup.forEach(connection => {
            connectedNodes.add(connection.node);
          });
        });
      }
    });
    
    // Find nodes not in connected set
    return nodes.filter(node => !connectedNodes.has(node.name));
  }

  /**
   * Detect circular dependencies in workflow
   */
  detectCircularDependencies(nodes, connections) {
    const visited = new Set();
    const recursionStack = new Set();
    const path = [];
    
    const hasCycle = (nodeName) => {
      if (recursionStack.has(nodeName)) {
        // Found cycle, return the path
        const cycleStart = path.indexOf(nodeName);
        return path.slice(cycleStart).concat([nodeName]);
      }
      
      if (visited.has(nodeName)) {
        return null;
      }
      
      visited.add(nodeName);
      recursionStack.add(nodeName);
      path.push(nodeName);
      
      const nodeConnections = connections[nodeName];
      if (nodeConnections && nodeConnections.main) {
        for (const connectionGroup of nodeConnections.main) {
          for (const connection of connectionGroup) {
            const cycle = hasCycle(connection.node);
            if (cycle) return cycle;
          }
        }
      }
      
      recursionStack.delete(nodeName);
      path.pop();
      return null;
    };
    
    // Check each node for cycles
    for (const node of nodes) {
      if (!visited.has(node.name)) {
        const cycle = hasCycle(node.name);
        if (cycle) return cycle;
      }
    }
    
    return [];
  }

  /**
   * Find nodes that cannot be reached from any trigger
   */
  findUnreachableNodes(nodes, connections) {
    const triggers = nodes.filter(node => 
      this.nodeTypes.triggers.includes(node.type)
    );
    
    if (triggers.length === 0) return nodes; // No triggers, all unreachable
    
    const reachable = new Set();
    
    const traverse = (nodeName) => {
      if (reachable.has(nodeName)) return;
      reachable.add(nodeName);
      
      const nodeConnections = connections[nodeName];
      if (nodeConnections && nodeConnections.main) {
        for (const connectionGroup of nodeConnections.main) {
          for (const connection of connectionGroup) {
            traverse(connection.node);
          }
        }
      }
    };
    
    // Start traversal from all triggers
    triggers.forEach(trigger => traverse(trigger.name));
    
    return nodes.filter(node => !reachable.has(node.name));
  }

  /**
   * Validate data flow between nodes
   */
  validateDataFlow(nodes, connections) {
    const issues = [];
    
    for (const [sourceName, nodeConnections] of Object.entries(connections)) {
      const sourceNode = nodes.find(n => n.name === sourceName);
      if (!sourceNode) continue;
      
      if (nodeConnections.main) {
        for (const connectionGroup of nodeConnections.main) {
          for (const connection of connectionGroup) {
            const targetNode = nodes.find(n => n.name === connection.node);
            if (!targetNode) continue;
            
            // Check if connection makes logical sense
            const flowIssue = this.validateNodeConnection(sourceNode, targetNode);
            if (flowIssue) {
              issues.push(`Data flow issue: ${sourceName} → ${connection.node}: ${flowIssue}`);
            }
          }
        }
      }
    }
    
    return issues;
  }

  /**
   * Validate connection between two specific nodes
   */
  validateNodeConnection(sourceNode, targetNode) {
    // Triggers should not have inputs
    if (this.nodeTypes.triggers.includes(targetNode.type)) {
      return 'Trigger nodes should not have input connections';
    }
    
    // Logic nodes should have proper flow
    if (this.nodeTypes.logic.includes(sourceNode.type) && 
        this.nodeTypes.triggers.includes(targetNode.type)) {
      return 'Logic nodes should not connect to triggers';
    }
    
    return null; // Connection is valid
  }

  /**
   * Validate trigger nodes
   */
  validateTriggers(nodes) {
    const issues = [];
    const triggers = nodes.filter(node => 
      this.nodeTypes.triggers.includes(node.type)
    );
    
    if (triggers.length === 0) {
      issues.push('Workflow has no trigger nodes');
    } else if (triggers.length > 3) {
      issues.push(`Too many triggers (${triggers.length}). Consider consolidating.`);
    }
    
    return issues;
  }

  /**
   * Auto-fix workflow connection issues
   */
  autoFixWorkflow(workflow) {
    const fixes = [];
    let modified = false;
    
    console.log(`🔧 Auto-fixing workflow: ${workflow.name}`);
    
    // 1. Fix orphaned nodes
    const orphanedNodes = this.findOrphanedNodes(workflow.nodes, workflow.connections);
    if (orphanedNodes.length > 0) {
      const fixResult = this.fixOrphanedNodes(workflow, orphanedNodes);
      if (fixResult.fixed) {
        fixes.push(...fixResult.fixes);
        modified = true;
      }
    }
    
    // 2. Fix unreachable nodes
    const unreachableNodes = this.findUnreachableNodes(workflow.nodes, workflow.connections);
    if (unreachableNodes.length > 0) {
      const fixResult = this.fixUnreachableNodes(workflow, unreachableNodes);
      if (fixResult.fixed) {
        fixes.push(...fixResult.fixes);
        modified = true;
      }
    }
    
    // 3. Add missing trigger if needed
    const triggers = workflow.nodes.filter(node => 
      this.nodeTypes.triggers.includes(node.type)
    );
    if (triggers.length === 0) {
      const fixResult = this.addMissingTrigger(workflow);
      if (fixResult.fixed) {
        fixes.push(...fixResult.fixes);
        modified = true;
      }
    }
    
    return { fixed: modified, fixes, workflow };
  }

  /**
   * Fix orphaned nodes by connecting them to the workflow
   */
  fixOrphanedNodes(workflow, orphanedNodes) {
    const fixes = [];
    let fixed = false;
    
    const triggers = workflow.nodes.filter(node => 
      this.nodeTypes.triggers.includes(node.type)
    );
    
    if (triggers.length === 0) return { fixed, fixes };
    
    const lastConnectedNode = this.findLastConnectedNode(workflow);
    
    for (const orphanedNode of orphanedNodes) {
      if (this.nodeTypes.triggers.includes(orphanedNode.type)) {
        // Don't connect triggers to other nodes as inputs
        continue;
      }
      
      const connectionSource = lastConnectedNode || triggers[0];
      
      if (!workflow.connections[connectionSource.name]) {
        workflow.connections[connectionSource.name] = { main: [[]] };
      }
      
      if (!workflow.connections[connectionSource.name].main[0]) {
        workflow.connections[connectionSource.name].main[0] = [];
      }
      
      workflow.connections[connectionSource.name].main[0].push({
        node: orphanedNode.name,
        type: 'main',
        index: 0
      });
      
      fixes.push(`Connected orphaned node: ${connectionSource.name} → ${orphanedNode.name}`);
      fixed = true;
    }
    
    return { fixed, fixes };
  }

  /**
   * Fix unreachable nodes by connecting them to triggers
   */
  fixUnreachableNodes(workflow, unreachableNodes) {
    const fixes = [];
    let fixed = false;
    
    const triggers = workflow.nodes.filter(node => 
      this.nodeTypes.triggers.includes(node.type)
    );
    
    if (triggers.length === 0) return { fixed, fixes };
    
    for (const unreachableNode of unreachableNodes) {
      if (this.nodeTypes.triggers.includes(unreachableNode.type)) {
        // Skip triggers
        continue;
      }
      
      const trigger = triggers[0];
      
      if (!workflow.connections[trigger.name]) {
        workflow.connections[trigger.name] = { main: [[]] };
      }
      
      if (!workflow.connections[trigger.name].main[0]) {
        workflow.connections[trigger.name].main[0] = [];
      }
      
      workflow.connections[trigger.name].main[0].push({
        node: unreachableNode.name,
        type: 'main',
        index: 0
      });
      
      fixes.push(`Connected unreachable node: ${trigger.name} → ${unreachableNode.name}`);
      fixed = true;
    }
    
    return { fixed, fixes };
  }

  /**
   * Add a missing trigger node
   */
  addMissingTrigger(workflow) {
    const fixes = [];
    
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
      !this.nodeTypes.triggers.includes(node.type)
    );
    
    if (firstActionNode) {
      workflow.connections[triggerNode.name] = {
        main: [[{
          node: firstActionNode.name,
          type: 'main',
          index: 0
        }]]
      };
      
      fixes.push(`Added missing trigger and connected to: ${firstActionNode.name}`);
    } else {
      fixes.push('Added missing trigger node');
    }
    
    return { fixed: true, fixes };
  }

  /**
   * Find the last connected node in the workflow
   */
  findLastConnectedNode(workflow) {
    const { nodes, connections } = workflow;
    
    // Find nodes that have no outgoing connections
    const endNodes = nodes.filter(node => !connections[node.name]);
    
    if (endNodes.length > 0) {
      return endNodes[0];
    }
    
    // Fallback to last node
    return nodes[nodes.length - 1];
  }

  /**
   * Generate unique node ID
   */
  generateNodeId() {
    return 'node_' + Math.random().toString(36).substr(2, 9);
  }

  /**
   * Process workflow file
   */
  async processWorkflowFile(filePath) {
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      const workflow = JSON.parse(content);
      
      // Validate
      const validation = this.validateWorkflowConnections(workflow);
      
      // Auto-fix if issues found
      let fixResult = { fixed: false, fixes: [] };
      if (!validation.isValid) {
        fixResult = this.autoFixWorkflow(workflow);
        
        if (fixResult.fixed) {
          // Create backup
          const backupPath = filePath + '.backup';
          fs.writeFileSync(backupPath, content);
          
          // Save fixed workflow
          fs.writeFileSync(filePath, JSON.stringify(workflow, null, 2));
        }
      }
      
      return {
        ...validation,
        ...fixResult,
        file: filePath
      };
      
    } catch (error) {
      return {
        isValid: false,
        issues: [`Failed to process file: ${error.message}`],
        fixed: false,
        fixes: []
      };
    }
  }
}

// CLI usage
async function main() {
  const validator = new AdvancedWorkflowValidator();
  
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('🔧 Advanced N8N Workflow Connection Validator');
    console.log('Usage:');
    console.log('  node advanced-workflow-validator.js <file.json>  # Validate and fix specific file');
    return;
  }
  
  const filePath = args[0];
  console.log(`🔍 Processing workflow: ${filePath}`);
  
  const result = await validator.processWorkflowFile(filePath);
  
  // Display results
  console.log(`\n📊 Validation Results:`);
  console.log(`   Valid: ${result.isValid ? '✅' : '❌'}`);
  
  if (result.issues && result.issues.length > 0) {
    console.log(`   Issues found:`);
    result.issues.forEach(issue => console.log(`      - ${issue}`));
  }
  
  if (result.orphanedNodes && result.orphanedNodes.length > 0) {
    console.log(`   Orphaned nodes: ${result.orphanedNodes.map(n => n.name).join(', ')}`);
  }
  
  if (result.unreachableNodes && result.unreachableNodes.length > 0) {
    console.log(`   Unreachable nodes: ${result.unreachableNodes.map(n => n.name).join(', ')}`);
  }
  
  if (result.circularDependencies && result.circularDependencies.length > 0) {
    console.log(`   Circular dependencies: ${result.circularDependencies.join(' → ')}`);
  }
  
  if (result.fixed && result.fixes.length > 0) {
    console.log(`\n🔧 Applied fixes:`);
    result.fixes.forEach(fix => console.log(`   - ${fix}`));
    console.log(`   ✅ Workflow has been automatically fixed!`);
  } else if (result.isValid) {
    console.log(`   ✅ No issues found - workflow is properly connected!`);
  }
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { AdvancedWorkflowValidator };