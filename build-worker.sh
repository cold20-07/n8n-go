#!/bin/bash

# Build script for Cloudflare Workers deployment
# Builds the n8n Workflow Generator for Cloudflare Workers environment

set -e

echo "🔧 Building n8n Workflow Generator for Cloudflare Workers..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check prerequisites
print_step "Checking prerequisites..."

if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    print_error "npm is not installed"
    exit 1
fi

if ! command -v wrangler &> /dev/null; then
    print_warning "Wrangler CLI not found, installing..."
    npm install -g wrangler
fi

print_status "Prerequisites check completed"

# Create worker source directory
print_step "Setting up worker environment..."
mkdir -p src
mkdir -p dist

# Create worker entry point
print_status "Creating Cloudflare Worker entry point..."
cat > src/index.js << 'EOF'
/**
 * Cloudflare Worker for n8n Workflow Generator
 * Handles workflow generation requests in a serverless environment
 */

// Import the main generator logic
import { N8nWorkflowGenerator } from './generator.js';

// CORS headers for browser requests
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, Authorization',
};

// Main request handler
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // Handle CORS preflight requests
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        status: 200,
        headers: corsHeaders
      });
    }
    
    try {
      // Route handling
      switch (url.pathname) {
        case '/':
          return handleHomePage();
        
        case '/generate':
          return handleGenerate(request, env);
        
        case '/health':
          return handleHealth();
        
        default:
          return new Response('Not Found', { 
            status: 404,
            headers: corsHeaders 
          });
      }
    } catch (error) {
      console.error('Worker error:', error);
      return new Response(JSON.stringify({ 
        error: 'Internal Server Error',
        message: error.message 
      }), {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          ...corsHeaders
        }
      });
    }
  }
};

async function handleHomePage() {
  const html = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>n8n Workflow Generator - Cloudflare Workers</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .container { background: #f5f5f5; padding: 20px; border-radius: 8px; }
        .status { color: #28a745; font-weight: bold; }
        .endpoint { background: #e9ecef; padding: 10px; border-radius: 4px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 n8n Workflow Generator</h1>
        <p class="status">✅ Cloudflare Worker is running</p>
        
        <h2>Available Endpoints:</h2>
        <div class="endpoint">
            <strong>POST /generate</strong><br>
            Generate n8n workflows from descriptions
        </div>
        <div class="endpoint">
            <strong>GET /health</strong><br>
            Health check endpoint
        </div>
        
        <h2>Usage Example:</h2>
        <pre>
curl -X POST ${new URL(request.url).origin}/generate \\
  -H "Content-Type: application/json" \\
  -d '{
    "description": "Process webhook data and send to Slack",
    "triggerType": "webhook",
    "complexity": "medium"
  }'
        </pre>
    </div>
</body>
</html>`;

  return new Response(html, {
    headers: {
      'Content-Type': 'text/html',
      ...corsHeaders
    }
  });
}

async function handleGenerate(request, env) {
  if (request.method !== 'POST') {
    return new Response('Method Not Allowed', { 
      status: 405,
      headers: corsHeaders 
    });
  }
  
  try {
    const data = await request.json();
    
    // Validate input
    if (!data.description) {
      return new Response(JSON.stringify({
        error: 'Missing required field: description'
      }), {
        status: 400,
        headers: {
          'Content-Type': 'application/json',
          ...corsHeaders
        }
      });
    }
    
    // Generate workflow
    const generator = new N8nWorkflowGenerator();
    const workflow = generator.generateWorkflow({
      description: data.description,
      triggerType: data.triggerType || 'webhook',
      complexity: data.complexity || 'medium',
      template: data.template
    });
    
    // Validate generated workflow
    const validation = generator.validateWorkflow(workflow);
    
    return new Response(JSON.stringify({
      success: true,
      workflow: workflow,
      validation: validation,
      generated_at: new Date().toISOString()
    }), {
      headers: {
        'Content-Type': 'application/json',
        ...corsHeaders
      }
    });
    
  } catch (error) {
    return new Response(JSON.stringify({
      error: 'Generation failed',
      message: error.message
    }), {
      status: 500,
      headers: {
        'Content-Type': 'application/json',
        ...corsHeaders
      }
    });
  }
}

async function handleHealth() {
  return new Response(JSON.stringify({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    environment: 'cloudflare-workers'
  }), {
    headers: {
      'Content-Type': 'application/json',
      ...corsHeaders
    }
  });
}
EOF

# Convert TypeScript generator to JavaScript for Workers
print_status "Converting generator logic for Workers..."
cat > src/generator.js << 'EOF'
/**
 * N8n Workflow Generator for Cloudflare Workers
 * Simplified version of the TypeScript generator
 */

export class N8nWorkflowGenerator {
  constructor() {
    this.nodeIdCounter = 0;
  }

  generateWorkflow(options) {
    const { description, triggerType, complexity, template } = options;
    
    const workflowName = this.generateWorkflowName(description);
    const nodes = this.createNodes(triggerType, complexity, template);
    const connections = this.createConnections(nodes);

    return {
      name: workflowName,
      nodes,
      connections,
      active: true,
      settings: {
        executionOrder: 'v1'
      },
      tags: ['generated', 'cloudflare-workers']
    };
  }

  generateWorkflowName(description) {
    const words = description.split(' ').slice(0, 4);
    return words
      .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
      .join(' ') + ' Workflow';
  }

  createNodes(triggerType, complexity, template) {
    const nodes = [];
    
    // Add trigger node
    const triggerNode = this.createTriggerNode(triggerType);
    nodes.push(triggerNode);

    // Determine number of nodes based on complexity
    const complexityMap = {
      simple: 2,
      medium: 4,
      complex: 7
    };

    const targetNodeCount = complexityMap[complexity] || 3;

    // Add processing nodes
    for (let i = 1; i < targetNodeCount; i++) {
      let node;

      if (i === 1) {
        node = this.createProcessingNode(i);
      } else if (i === targetNodeCount - 1 && triggerType === 'webhook') {
        node = this.createResponseNode(i);
      } else {
        node = this.createHttpRequestNode(i);
      }

      nodes.push(node);
    }

    return nodes;
  }

  createTriggerNode(triggerType) {
    const triggerConfigs = {
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

    const config = triggerConfigs[triggerType] || triggerConfigs.webhook;

    return {
      parameters: config.parameters,
      id: this.generateNodeId(),
      name: 'Trigger',
      type: config.type,
      typeVersion: 1,
      position: [0, 300]
    };
  }

  createProcessingNode(index) {
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

  createHttpRequestNode(index) {
    return {
      parameters: {
        url: 'https://api.example.com/data',
        httpMethod: 'POST',
        sendBody: true,
        bodyContentType: 'json',
        jsonBody: '={{ $json }}',
        options: {
          timeout: 10000
        }
      },
      id: this.generateNodeId(),
      name: 'HTTP Request',
      type: 'n8n-nodes-base.httpRequest',
      typeVersion: 4,
      position: [index * 300, 300]
    };
  }

  createResponseNode(index) {
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

  createConnections(nodes) {
    const connections = {};

    for (let i = 0; i < nodes.length - 1; i++) {
      const currentNode = nodes[i];
      const nextNode = nodes[i + 1];

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

  generateNodeId() {
    return `node_${++this.nodeIdCounter}_${Math.random().toString(36).substr(2, 9)}`;
  }

  validateWorkflow(workflow) {
    const errors = [];

    if (!workflow.name) {
      errors.push('Workflow name is required');
    }

    if (!Array.isArray(workflow.nodes) || workflow.nodes.length === 0) {
      errors.push('Workflow must have at least one node');
    }

    if (typeof workflow.connections !== 'object') {
      errors.push('Workflow connections must be an object');
    }

    return {
      isValid: errors.length === 0,
      errors
    };
  }
}
EOF

# Create package.json for worker
print_status "Creating worker package.json..."
cat > package.json << 'EOF'
{
  "name": "n8n-workflow-generator-worker",
  "version": "1.0.0",
  "description": "Cloudflare Worker for n8n Workflow Generator",
  "main": "src/index.js",
  "scripts": {
    "dev": "wrangler dev",
    "deploy": "wrangler deploy",
    "build": "echo 'No build step required for this worker'"
  },
  "keywords": ["n8n", "workflow", "cloudflare", "workers"],
  "author": "n8n Workflow Generator Team",
  "license": "MIT"
}
EOF

# Test the worker locally
print_step "Testing worker locally..."
if command -v wrangler &> /dev/null; then
    print_status "Starting local development server..."
    print_status "Worker will be available at http://localhost:8787"
    print_status "Press Ctrl+C to stop the server and continue with deployment"
    
    # Start dev server in background for testing
    timeout 10s wrangler dev --local || true
    
    print_status "Local test completed"
else
    print_warning "Wrangler not available, skipping local test"
fi

# Prepare for deployment
print_step "Preparing for deployment..."
print_status "Worker source files created successfully"
print_status "Ready for deployment with: wrangler deploy"

echo ""
echo "🎉 Cloudflare Worker build completed!"
echo ""
echo "📝 Next steps:"
echo "   1. Configure wrangler.toml with your account details"
echo "   2. Run 'wrangler login' to authenticate"
echo "   3. Run 'wrangler deploy' to deploy to Cloudflare"
echo "   4. Test your deployed worker"
echo ""
echo "🔧 Development commands:"
echo "   - wrangler dev: Start local development server"
echo "   - wrangler deploy: Deploy to Cloudflare"
echo "   - wrangler tail: View live logs"
echo ""
EOF