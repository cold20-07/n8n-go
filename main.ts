/**
 * Main TypeScript entry point for n8n Workflow Generator
 * Provides type-safe workflow generation and validation
 */

interface N8nNode {
    parameters: Record<string, any>;
    id: string;
    name: string;
    type: string;
    typeVersion: number;
    position: [number, number];
}

interface N8nConnection {
    node: string;
    type: string;
    index: number;
}

interface N8nWorkflow {
    name: string;
    nodes: N8nNode[];
    connections: Record<string, { main: N8nConnection[][] }>;
    active: boolean;
    settings: Record<string, any>;
    tags: string[];
}

interface WorkflowGenerationOptions {
    description: string;
    triggerType: 'webhook' | 'schedule' | 'manual';
    complexity: 'simple' | 'medium' | 'complex';
    template?: string;
}

class N8nWorkflowGenerator {
    private nodeIdCounter: number = 0;

    constructor() {
        this.initializeGenerator();
    }

    private initializeGenerator(): void {
        console.log('N8n Workflow Generator initialized');
    }

    /**
     * Generate a complete n8n workflow based on options
     */
    public generateWorkflow(options: WorkflowGenerationOptions): N8nWorkflow {
        const { description, triggerType, complexity, template } = options;

        // Generate workflow name from description
        const workflowName = this.generateWorkflowName(description);

        // Create nodes based on complexity
        const nodes = this.createNodes(triggerType, complexity, template);

        // Create connections between nodes
        const connections = this.createConnections(nodes);

        return {
            name: workflowName,
            nodes,
            connections,
            active: true,
            settings: {
                executionOrder: 'v1'
            },
            tags: ['generated', 'typescript']
        };
    }

    /**
     * Generate workflow name from description
     */
    private generateWorkflowName(description: string): string {
        const words = description.split(' ').slice(0, 4);
        return words
            .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
            .join(' ') + ' Workflow';
    }

    /**
     * Create nodes based on trigger type and complexity
     */
    private createNodes(
        triggerType: string, 
        complexity: string, 
        _template?: string
    ): N8nNode[] {
        const nodes: N8nNode[] = [];

        // Add trigger node
        const triggerNode = this.createTriggerNode(triggerType);
        nodes.push(triggerNode);

        // Determine number of additional nodes based on complexity
        const complexityMap: Record<string, number> = {
            simple: 2,
            medium: 4,
            complex: 7
        };

        const targetNodeCount = complexityMap[complexity] || 3;

        // Add processing nodes
        for (let i = 1; i < targetNodeCount; i++) {
            let node: N8nNode;

            if (i === 1) {
                node = this.createProcessingNode(i);
            } else if (i === targetNodeCount - 1 && triggerType === 'webhook') {
                node = this.createResponseNode(i);
            } else if (complexity === 'complex' && i === Math.floor(targetNodeCount / 2)) {
                node = this.createConditionalNode(i);
            } else {
                node = this.createHttpRequestNode(i);
            }

            nodes.push(node);
        }

        return nodes;
    }

    /**
     * Create trigger node based on type
     */
    private createTriggerNode(triggerType: string): N8nNode {
        const nodeId = this.generateNodeId();

        const triggerConfigs: Record<string, Partial<N8nNode>> = {
            webhook: {
                type: 'n8n-nodes-base.webhook',
                parameters: {
                    path: 'webhook-endpoint',
                    httpMethod: 'POST',
                    responseMode: 'responseNode'
                }
            },
            schedule: {
                type: 'n8n-nodes-base.scheduleTrigger',
                parameters: {
                    rule: {
                        interval: [{
                            field: 'cronExpression',
                            expression: '0 */1 * * *'
                        }]
                    }
                }
            },
            manual: {
                type: 'n8n-nodes-base.manualTrigger',
                parameters: {}
            }
        };

        const config = triggerConfigs[triggerType] || triggerConfigs['webhook'];

        return {
            parameters: config?.parameters || {},
            id: nodeId,
            name: 'Trigger',
            type: config?.type || 'n8n-nodes-base.webhook',
            typeVersion: 1,
            position: [0, 300]
        };
    }

    /**
     * Create processing node
     */
    private createProcessingNode(index: number): N8nNode {
        return {
            parameters: {
                jsCode: `// Process incoming data
const inputData = $input.all();
const processedData = inputData.map(item => ({
  ...item.json,
  processed: true,
  timestamp: new Date().toISOString(),
  nodeIndex: ${index}
}));

return processedData;`
            },
            id: this.generateNodeId(),
            name: 'Process Data',
            type: 'n8n-nodes-base.code',
            typeVersion: 2,
            position: [index * 300, 300]
        };
    }

    /**
     * Create HTTP request node
     */
    private createHttpRequestNode(index: number): N8nNode {
        return {
            parameters: {
                url: 'https://api.example.com/data',
                authentication: 'genericCredentialType',
                genericAuthType: 'httpHeaderAuth',
                httpMethod: 'POST',
                sendBody: true,
                bodyContentType: 'json',
                jsonBody: '={{ $json }}',
                options: {
                    timeout: 10000,
                    retry: {
                        enabled: true,
                        maxRetries: 3
                    }
                }
            },
            id: this.generateNodeId(),
            name: 'HTTP Request',
            type: 'n8n-nodes-base.httpRequest',
            typeVersion: 4,
            position: [index * 300, 300]
        };
    }

    /**
     * Create conditional node
     */
    private createConditionalNode(index: number): N8nNode {
        return {
            parameters: {
                conditions: {
                    options: {
                        caseSensitive: true,
                        leftValue: '',
                        typeValidation: 'strict'
                    },
                    conditions: [{
                        leftValue: '={{ $json.status }}',
                        rightValue: 'active',
                        operator: {
                            type: 'string',
                            operation: 'equals'
                        }
                    }],
                    combinator: 'and'
                }
            },
            id: this.generateNodeId(),
            name: 'Check Condition',
            type: 'n8n-nodes-base.if',
            typeVersion: 2,
            position: [index * 300, 300]
        };
    }

    /**
     * Create webhook response node
     */
    private createResponseNode(index: number): N8nNode {
        return {
            parameters: {
                options: {}
            },
            id: this.generateNodeId(),
            name: 'Respond to Webhook',
            type: 'n8n-nodes-base.respondToWebhook',
            typeVersion: 1,
            position: [index * 300, 300]
        };
    }

    /**
     * Create connections between nodes
     */
    private createConnections(nodes: N8nNode[]): Record<string, { main: N8nConnection[][] }> {
        const connections: Record<string, { main: N8nConnection[][] }> = {};

        // Ensure we have at least 2 nodes before creating connections
        if (nodes.length < 2) {
            return connections;
        }

        for (let i = 0; i < nodes.length - 1; i++) {
            const currentNode = nodes[i];
            const nextNode = nodes[i + 1];

            // Validate nodes exist and have names
            if (!currentNode || !nextNode || !currentNode.name || !nextNode.name) {
                continue;
            }

            connections[currentNode.name] = {
                main: [[{
                    node: nextNode.name,
                    type: 'main',
                    index: 0
                }]]
            };
        }

        return connections;
    }

    /**
     * Generate unique node ID
     */
    private generateNodeId(): string {
        const timestamp = Date.now().toString(36);
        const random = Math.random().toString(36).substring(2, 9);
        return `node_${++this.nodeIdCounter}_${timestamp}_${random}`;
    }

    /**
     * Validate workflow structure
     */
    public validateWorkflow(workflow: N8nWorkflow): { isValid: boolean; errors: string[] } {
        const errors: string[] = [];

        // Check required fields
        if (!workflow.name) {
            errors.push('Workflow name is required');
        }

        if (!Array.isArray(workflow.nodes) || workflow.nodes.length === 0) {
            errors.push('Workflow must have at least one node');
        }

        if (typeof workflow.connections !== 'object') {
            errors.push('Workflow connections must be an object');
        }

        // Validate nodes
        workflow.nodes.forEach((node, index) => {
            if (!node.id) {
                errors.push(`Node ${index}: Missing id`);
            }
            if (!node.name) {
                errors.push(`Node ${index}: Missing name`);
            }
            if (!node.type) {
                errors.push(`Node ${index}: Missing type`);
            }
            if (!Array.isArray(node.position) || node.position.length !== 2) {
                errors.push(`Node ${index}: Invalid position`);
            }
        });

        // Validate connections
        const nodeNames = new Set(workflow.nodes.map(node => node.name));
        Object.entries(workflow.connections).forEach(([sourceName, connectionData]) => {
            if (!nodeNames.has(sourceName)) {
                errors.push(`Connection source '${sourceName}' does not exist`);
            }

            if (connectionData.main) {
                connectionData.main.forEach((connectionGroup, _groupIndex) => {
                    connectionGroup.forEach((connection, _connIndex) => {
                        if (!nodeNames.has(connection.node)) {
                            errors.push(`Connection target '${connection.node}' does not exist`);
                        }
                    });
                });
            }
        });

        return {
            isValid: errors.length === 0,
            errors
        };
    }

    /**
     * Export workflow as JSON string
     */
    public exportWorkflow(workflow: N8nWorkflow): string {
        return JSON.stringify(workflow, null, 2);
    }
}

// Export for use in other modules
export { N8nWorkflowGenerator, N8nWorkflow, WorkflowGenerationOptions };

// Initialize generator if running in browser
if (typeof window !== 'undefined') {
    (window as any).N8nWorkflowGenerator = N8nWorkflowGenerator;
}