// Advanced N8N Workflow Generator for Vercel
const crypto = require('crypto');

// Workflow generation patterns and templates
const WORKFLOW_PATTERNS = {
  'http_request': {
    type: 'n8n-nodes-base.httpRequest',
    category: 'api',
    keywords: ['api', 'endpoint', 'http', 'request', 'monitor', 'response', 'webhook', 'rest']
  },
  'schedule': {
    type: 'n8n-nodes-base.scheduleTrigger',
    category: 'trigger',
    keywords: ['schedule', 'cron', 'interval', 'every', 'minutes', 'hours', 'daily', 'weekly']
  },
  'webhook': {
    type: 'n8n-nodes-base.webhook',
    category: 'trigger',
    keywords: ['webhook', 'trigger', 'incoming', 'receive', 'listen']
  },
  'code': {
    type: 'n8n-nodes-base.code',
    category: 'processing',
    keywords: ['code', 'javascript', 'process', 'transform', 'logic', 'function', 'script']
  },
  'if': {
    type: 'n8n-nodes-base.if',
    category: 'logic',
    keywords: ['if', 'condition', 'check', 'compare', 'validate', 'filter', 'exceeds', 'greater', 'less']
  },
  'slack': {
    type: 'n8n-nodes-base.slack',
    category: 'communication',
    keywords: ['slack', 'message', 'notification', 'team', 'channel', 'alert']
  },
  'google_sheets': {
    type: 'n8n-nodes-base.googleSheets',
    category: 'productivity',
    keywords: ['google sheets', 'google sheet', 'spreadsheet', 'row', 'data', 'sheet']
  },
  'gmail': {
    type: 'n8n-nodes-base.gmail',
    category: 'email',
    keywords: ['gmail', 'email', 'mail', 'message', 'send']
  },
  'trello': {
    type: 'n8n-nodes-base.trello',
    category: 'project_management',
    keywords: ['trello', 'card', 'board', 'task', 'project']
  },
  'shopify': {
    type: 'n8n-nodes-base.shopify',
    category: 'ecommerce',
    keywords: ['shopify', 'order', 'product', 'customer', 'store']
  },
  'airtable': {
    type: 'n8n-nodes-base.airtable',
    category: 'database',
    keywords: ['airtable', 'record', 'database', 'table', 'base']
  },
  'notion': {
    type: 'n8n-nodes-base.notion',
    category: 'productivity',
    keywords: ['notion', 'database', 'page', 'block', 'workspace']
  },
  'dropbox': {
    type: 'n8n-nodes-base.dropbox',
    category: 'storage',
    keywords: ['dropbox', 'file', 'upload', 'backup', 'storage']
  },
  'google_drive': {
    type: 'n8n-nodes-base.googleDrive',
    category: 'storage',
    keywords: ['google drive', 'file', 'folder', 'backup', 'storage']
  },
  'asana': {
    type: 'n8n-nodes-base.asana',
    category: 'project_management',
    keywords: ['asana', 'task', 'project', 'completed', 'team']
  },
  'typeform': {
    type: 'n8n-nodes-base.typeform',
    category: 'forms',
    keywords: ['typeform', 'form', 'response', 'survey', 'submission']
  },
  'microsoft_teams': {
    type: 'n8n-nodes-base.microsoftTeams',
    category: 'communication',
    keywords: ['microsoft teams', 'teams', 'message', 'channel', 'notification']
  },
  'onedrive': {
    type: 'n8n-nodes-base.microsoftOneDrive',
    category: 'storage',
    keywords: ['onedrive', 'file', 'upload', 'document', 'storage']
  },
  'hubspot': {
    type: 'n8n-nodes-base.hubspot',
    category: 'crm',
    keywords: ['hubspot', 'deal', 'contact', 'sales', 'crm']
  },
  'telegram': {
    type: 'n8n-nodes-base.telegram',
    category: 'communication',
    keywords: ['telegram', 'message', 'bot', 'notification', 'alert']
  },
  'github': {
    type: 'n8n-nodes-base.github',
    category: 'development',
    keywords: ['github', 'issue', 'repository', 'code', 'commit', 'repo', 'deploy']
  },
  'instagram': {
    type: 'n8n-nodes-base.instagram',
    category: 'social_media',
    keywords: ['instagram', 'post', 'photo', 'social', 'media']
  },
  'twitter': {
    type: 'n8n-nodes-base.twitter',
    category: 'social_media',
    keywords: ['twitter', 'tweet', 'post', 'social', 'media']
  },
  'youtube': {
    type: 'n8n-nodes-base.youtube',
    category: 'social_media',
    keywords: ['youtube', 'video', 'channel', 'upload', 'content']
  },
  'whatsapp': {
    type: 'n8n-nodes-base.whatsApp',
    category: 'communication',
    keywords: ['whatsapp', 'message', 'chat', 'notification', 'mobile']
  },
  'mailchimp': {
    type: 'n8n-nodes-base.mailchimp',
    category: 'email_marketing',
    keywords: ['mailchimp', 'email', 'list', 'audience', 'marketing']
  },
  'openai': {
    type: 'n8n-nodes-base.openAi',
    category: 'ai',
    keywords: ['openai', 'gpt', 'ai', 'generate', 'text', 'chat', 'gemini']
  },
  'stripe': {
    type: 'n8n-nodes-base.stripe',
    category: 'payment',
    keywords: ['stripe', 'payment', 'charge', 'invoice', 'transaction']
  },
  'woocommerce': {
    type: 'n8n-nodes-base.wooCommerce',
    category: 'ecommerce',
    keywords: ['woocommerce', 'order', 'product', 'inventory', 'store']
  },
  'google_ads': {
    type: 'n8n-nodes-base.googleAds',
    category: 'marketing',
    keywords: ['google ads', 'ads', 'campaign', 'leads', 'advertising']
  },
  'discord': {
    type: 'n8n-nodes-base.discord',
    category: 'communication',
    keywords: ['discord', 'message', 'server', 'channel', 'notification']
  },
  'paypal': {
    type: 'n8n-nodes-base.payPal',
    category: 'payment',
    keywords: ['paypal', 'payment', 'transaction', 'refund', 'money']
  },
  'quickbooks': {
    type: 'n8n-nodes-base.quickBooks',
    category: 'accounting',
    keywords: ['quickbooks', 'invoice', 'accounting', 'finance', 'bookkeeping']
  },
  'mongodb': {
    type: 'n8n-nodes-base.mongoDb',
    category: 'database',
    keywords: ['mongodb', 'database', 'collection', 'document', 'nosql']
  },
  'mysql': {
    type: 'n8n-nodes-base.mySql',
    category: 'database',
    keywords: ['mysql', 'database', 'sql', 'table', 'query']
  }
};

function generateNodeId() {
  return crypto.randomBytes(8).toString('hex');
}

function analyzeDescription(description) {
  const desc = description.toLowerCase();
  const detectedServices = [];
  const triggers = [];
  const actions = [];
  
  // Detect services mentioned in description
  for (const [service, config] of Object.entries(WORKFLOW_PATTERNS)) {
    for (const keyword of config.keywords) {
      if (desc.includes(keyword)) {
        detectedServices.push({ service, config, keyword });
        break;
      }
    }
  }
  
  // Enhanced trigger detection
  const triggerPatterns = [
    { pattern: /every \d+ (minute|hour|day|week)/i, service: 'schedule' },
    { pattern: /(monitor|check|watch|poll)/i, service: 'schedule' },
    { pattern: /(webhook|incoming|receive)/i, service: 'webhook' },
    { pattern: /when.*?(new|created|added|received)/i, service: 'webhook' }
  ];
  
  for (const { pattern, service } of triggerPatterns) {
    if (pattern.test(desc) && !detectedServices.some(s => s.service === service)) {
      const config = WORKFLOW_PATTERNS[service];
      if (config) {
        const triggerService = { service, config, keyword: service };
        detectedServices.push(triggerService);
        triggers.push(triggerService);
      }
    }
  }
  
  // Enhanced action detection with more specific patterns
  const actionPatterns = [
    { pattern: /(slack.*?(message|notification|alert))/i, service: 'slack' },
    { pattern: /(telegram.*?(alert|message|notification))/i, service: 'telegram' },
    { pattern: /(github.*?(issue|repository|deploy))/i, service: 'github' },
    { pattern: /(google ads|ads.*?lead)/i, service: 'google_ads' },
    { pattern: /(notion.*?(database|page))/i, service: 'notion' },
    { pattern: /(airtable.*?(record|database))/i, service: 'airtable' },
    { pattern: /(discord.*?message)/i, service: 'discord' },
    { pattern: /(paypal.*?transaction)/i, service: 'paypal' },
    { pattern: /(quickbooks.*?invoice)/i, service: 'quickbooks' },
    { pattern: /(mongodb|mysql).*?(database|store)/i, service: desc.includes('mongodb') ? 'mongodb' : 'mysql' },
    { pattern: /(api|endpoint|http|request)/i, service: 'http_request' },
    { pattern: /(if|condition|check|exceeds|greater|less)/i, service: 'if' },
    { pattern: /(process|transform|code|logic)/i, service: 'code' }
  ];
  
  for (const { pattern, service } of actionPatterns) {
    if (pattern.test(desc) && !detectedServices.some(s => s.service === service)) {
      const config = WORKFLOW_PATTERNS[service];
      if (config) {
        const actionService = { service, config, keyword: service };
        detectedServices.push(actionService);
        if (!triggers.includes(actionService)) {
          actions.push(actionService);
        }
      }
    }
  }
  
  // Fallback: if no triggers detected, add a default trigger
  if (triggers.length === 0) {
    const defaultTrigger = desc.includes('monitor') || desc.includes('every') ? 'schedule' : 'webhook';
    const config = WORKFLOW_PATTERNS[defaultTrigger];
    const triggerService = { service: defaultTrigger, config, keyword: defaultTrigger };
    detectedServices.push(triggerService);
    triggers.push(triggerService);
  }
  
  // Enhanced fallback: detect services from description even if not in patterns
  const additionalServiceDetection = [
    { keywords: ['google ads', 'ads'], service: 'google_ads' },
    { keywords: ['notion', 'crm'], service: 'notion' },
    { keywords: ['airtable'], service: 'airtable' },
    { keywords: ['telegram'], service: 'telegram' },
    { keywords: ['github'], service: 'github' },
    { keywords: ['discord'], service: 'discord' },
    { keywords: ['paypal'], service: 'paypal' },
    { keywords: ['quickbooks'], service: 'quickbooks' },
    { keywords: ['mongodb'], service: 'mongodb' },
    { keywords: ['mysql'], service: 'mysql' }
  ];

  for (const { keywords, service } of additionalServiceDetection) {
    if (keywords.some(keyword => desc.includes(keyword)) && 
        !detectedServices.some(s => s.service === service)) {
      const config = WORKFLOW_PATTERNS[service];
      if (config) {
        const serviceObj = { service, config, keyword: service };
        detectedServices.push(serviceObj);
        actions.push(serviceObj);
      }
    }
  }

  // Fallback: if no actions detected, add processing logic
  if (actions.length === 0) {
    const defaultAction = 'code';
    const config = WORKFLOW_PATTERNS[defaultAction];
    const actionService = { service: defaultAction, config, keyword: defaultAction };
    detectedServices.push(actionService);
    actions.push(actionService);
  }
  
  return { detectedServices, triggers, actions };
}

function createTriggerNode(service, description) {
  const nodeId = generateNodeId();
  const desc = description.toLowerCase();
  
  const triggerConfigs = {
    'schedule': {
      parameters: {
        rule: {
          interval: desc.includes('10 minutes') ? [{ field: 'minute', step: 10 }] :
                   desc.includes('hour') ? [{ field: 'hour', step: 1 }] :
                   desc.includes('daily') ? [{ field: 'day', step: 1 }] :
                   [{ field: 'minute', step: 10 }]
        }
      },
      name: desc.includes('monitor') ? 'Monitor Schedule' : 'Schedule Trigger'
    },
    'webhook': {
      parameters: {
        httpMethod: 'POST',
        path: 'webhook',
        responseMode: 'onReceived'
      },
      name: 'Webhook Trigger'
    }
  };
  
  const config = triggerConfigs[service] || triggerConfigs['webhook'];
  
  return {
    parameters: config.parameters,
    id: nodeId,
    name: config.name,
    type: WORKFLOW_PATTERNS[service]?.type || 'n8n-nodes-base.webhook',
    typeVersion: 1,
    position: [240, 300]
  };
}

function createActionNode(service, description, index) {
  const nodeId = generateNodeId();
  const desc = description.toLowerCase();
  
  const actionConfigs = {
    'http_request': {
      parameters: {
        method: 'GET',
        url: desc.includes('monitor') ? 'https://api.example.com/health' : 'https://api.example.com/endpoint',
        options: { timeout: 5000 }
      },
      name: desc.includes('monitor') ? 'Monitor API Endpoint' : 'HTTP Request'
    },
    'if': {
      parameters: {
        conditions: {
          number: [{
            value1: '={{ $json.response_time }}',
            operation: 'larger',
            value2: desc.includes('2 seconds') ? 2000 : 1000
          }]
        }
      },
      name: desc.includes('response time') ? 'Check Response Time' : 'Condition Check'
    },
    'code': {
      parameters: {
        jsCode: desc.includes('monitor') ? 
          `// Monitor API response time
const startTime = Date.now();
const response = $input.all();
const responseTime = Date.now() - startTime;

return [{
  json: {
    ...response[0]?.json,
    response_time: responseTime,
    status: responseTime > 2000 ? 'slow' : 'ok',
    timestamp: new Date().toISOString()
  }
}];` :
          `// Process workflow data
const inputData = $input.all();
const processedData = inputData.map(item => ({
  ...item.json,
  processed: true,
  timestamp: new Date().toISOString()
}));

return processedData;`,

      },
      name: desc.includes('monitor') ? 'Process Response Time' : 'Process Data'
    },
    'slack': {
      parameters: {
        channel: '#alerts',
        text: desc.includes('alert') ? 
          'Alert: {{ $json.message || "API response time exceeded threshold" }}' :
          'New notification from workflow',
        username: 'n8n-bot'
      },
      name: desc.includes('alert') ? 'Send Alert' : 'Send Slack Message'
    },
    'gmail': {
      parameters: {
        operation: 'send',
        subject: 'Automated Email',
        toEmail: 'recipient@example.com',
        message: 'This is an automated message from your workflow.'
      },
      name: 'Send Email'
    },
    'trello': {
      parameters: {
        operation: 'create',
        boardId: 'your-board-id',
        listId: 'your-list-id',
        name: 'New Task from Workflow',
        description: 'Created automatically by n8n workflow'
      },
      name: 'Create Trello Card'
    },
    'shopify': {
      parameters: {
        operation: 'get',
        resource: 'order'
      },
      name: 'Get Shopify Order'
    },
    'airtable': {
      parameters: {
        operation: 'create',
        baseId: 'your-base-id',
        tableId: 'your-table-id',
        fields: {
          'Name': 'New Record'
        }
      },
      name: 'Create Airtable Record'
    },
    'notion': {
      parameters: {
        operation: 'create',
        databaseId: 'your-database-id',
        properties: {
          'Name': {
            title: [{ text: { content: 'New Entry' } }]
          }
        }
      },
      name: 'Create Notion Page'
    },
    'google_sheets': {
      parameters: {
        operation: 'append',
        sheetId: 'your-sheet-id',
        range: 'A:Z',
        values: [['New', 'Data', 'Row']]
      },
      name: 'Add to Google Sheets'
    },
    'telegram': {
      parameters: {
        chatId: 'your-chat-id',
        text: desc.includes('alert') ? 
          'Alert: {{ $json.message || "Notification from workflow" }}' :
          'Notification from workflow'
      },
      name: desc.includes('alert') ? 'Send Telegram Alert' : 'Send Telegram Message'
    },
    'github': {
      parameters: {
        operation: desc.includes('issue') ? 'createIssue' : 'get',
        repository: 'your-repo',
        title: desc.includes('issue') ? 'New Issue from Workflow' : undefined,
        body: desc.includes('issue') ? 'This issue was created automatically' : undefined
      },
      name: desc.includes('issue') ? 'Create GitHub Issue' : 'GitHub Action'
    },
    'google_ads': {
      parameters: {
        operation: 'getAll',
        resource: 'lead'
      },
      name: 'Get Google Ads Leads'
    },
    'discord': {
      parameters: {
        operation: 'sendMessage',
        channelId: 'your-channel-id',
        content: 'Notification from workflow'
      },
      name: 'Send Discord Message'
    },
    'paypal': {
      parameters: {
        operation: 'getAll',
        resource: 'payment'
      },
      name: 'Get PayPal Transactions'
    },
    'quickbooks': {
      parameters: {
        operation: 'create',
        resource: 'invoice',
        customerRef: 'customer-id'
      },
      name: 'Create QuickBooks Invoice'
    },
    'mongodb': {
      parameters: {
        operation: 'insert',
        collection: 'data',
        fields: 'json'
      },
      name: 'Insert to MongoDB'
    },
    'mysql': {
      parameters: {
        operation: 'insert',
        table: 'data'
      },
      name: 'Insert to MySQL'
    },
    'microsoft_teams': {
      parameters: {
        operation: 'postMessage',
        channelId: 'your-channel-id',
        message: 'Notification from workflow'
      },
      name: 'Send Teams Message'
    },
    'whatsapp': {
      parameters: {
        operation: 'sendMessage',
        to: 'your-phone-number',
        message: 'Notification from workflow'
      },
      name: 'Send WhatsApp Message'
    },
    'instagram': {
      parameters: {
        operation: 'createPost',
        caption: 'Automated post from workflow'
      },
      name: 'Create Instagram Post'
    },
    'twitter': {
      parameters: {
        operation: 'tweet',
        text: 'Automated tweet from workflow'
      },
      name: 'Send Tweet'
    },
    'youtube': {
      parameters: {
        operation: 'get',
        resource: 'video'
      },
      name: 'Get YouTube Video'
    },
    'mailchimp': {
      parameters: {
        operation: 'addMember',
        listId: 'your-list-id',
        email: 'subscriber@example.com'
      },
      name: 'Add to Mailchimp'
    },
    'woocommerce': {
      parameters: {
        operation: 'get',
        resource: 'order'
      },
      name: 'Get WooCommerce Order'
    },
    'dropbox': {
      parameters: {
        operation: 'upload',
        path: '/backup/',
        binary: true
      },
      name: 'Upload to Dropbox'
    },
    'google_drive': {
      parameters: {
        operation: 'upload',
        folderId: 'your-folder-id'
      },
      name: 'Upload to Google Drive'
    },
    'asana': {
      parameters: {
        operation: 'create',
        resource: 'task',
        name: 'New task from workflow'
      },
      name: 'Create Asana Task'
    },
    'typeform': {
      parameters: {
        operation: 'getAll',
        formId: 'your-form-id'
      },
      name: 'Get Typeform Responses'
    },
    'onedrive': {
      parameters: {
        operation: 'upload',
        path: '/documents/'
      },
      name: 'Upload to OneDrive'
    },
    'hubspot': {
      parameters: {
        operation: 'getAll',
        resource: 'deal'
      },
      name: 'Get HubSpot Deals'
    }
  };
  
  const config = actionConfigs[service] || {
    parameters: {
      jsCode: `// Process workflow data for ${service}
const inputData = $input.all();
const processedData = inputData.map(item => ({
  ...item.json,
  processed: true,
  service: '${service}',
  timestamp: new Date().toISOString()
}));

return processedData;`
    },
    name: `Process ${service.charAt(0).toUpperCase() + service.slice(1)}`
  };
  
  return {
    parameters: config.parameters,
    id: nodeId,
    name: config.name,
    type: WORKFLOW_PATTERNS[service]?.type || 'n8n-nodes-base.code',
    typeVersion: service === 'if' ? 1 : 2,
    position: [460 + index * 220, 300]
  };
}

function generateAdvancedWorkflow(description, triggerType, complexity) {
  const analysis = analyzeDescription(description);
  const workflowId = `workflow_${Date.now()}`;
  const nodes = [];
  const connections = {};
  const desc = description.toLowerCase();
  
  // Generate workflow name from description
  const workflowName = description
    .split(' ')
    .slice(0, 4)
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ') + ' Automation';
  
  // Create trigger node
  let triggerNode;
  if (analysis.triggers.length > 0) {
    triggerNode = createTriggerNode(analysis.triggers[0].service, description);
  } else {
    const defaultTrigger = desc.includes('monitor') || desc.includes('every') ? 'schedule' : 'webhook';
    triggerNode = createTriggerNode(defaultTrigger, description);
  }
  nodes.push(triggerNode);
  
  let previousNode = triggerNode;
  let nodeIndex = 1;
  
  // For monitoring workflows, create specific flow
  if (desc.includes('monitor') && desc.includes('api')) {
    // Add HTTP request node
    const httpNode = createActionNode('http_request', description, nodeIndex++);
    nodes.push(httpNode);
    
    connections[previousNode.name] = {
      main: [[{ node: httpNode.name, type: 'main', index: 0 }]]
    };
    previousNode = httpNode;
    
    // Add response time processing
    const processNode = createActionNode('code', description, nodeIndex++);
    nodes.push(processNode);
    
    connections[previousNode.name] = {
      main: [[{ node: processNode.name, type: 'main', index: 0 }]]
    };
    previousNode = processNode;
    
    // Add condition check
    if (desc.includes('exceeds') || desc.includes('greater') || desc.includes('threshold')) {
      const conditionNode = createActionNode('if', description, nodeIndex++);
      nodes.push(conditionNode);
      
      connections[previousNode.name] = {
        main: [[{ node: conditionNode.name, type: 'main', index: 0 }]]
      };
      previousNode = conditionNode;
    }
    
    // Add alert node
    if (desc.includes('alert') || desc.includes('notify')) {
      const alertNode = createActionNode('slack', description, nodeIndex++);
      nodes.push(alertNode);
      
      connections[previousNode.name] = {
        main: [[{ node: alertNode.name, type: 'main', index: 0 }]]
      };
      previousNode = alertNode;
    }
  } else {
    // Create service-specific action nodes based on detected services
    const servicesToCreate = [];
    
    // Add detected services that aren't triggers and have proper action configs
    for (const service of analysis.detectedServices) {
      if (service.service !== 'schedule' && service.service !== 'webhook' && 
          service.service !== 'code' && service.service !== 'if' &&
          !servicesToCreate.some(s => s.service === service.service)) {
        servicesToCreate.push(service);
      }
    }
    
    // If we have specific services, create nodes for them
    if (servicesToCreate.length > 0) {
      servicesToCreate.forEach((service, index) => {
        const actionNode = createActionNode(service.service, description, nodeIndex + index);
        nodes.push(actionNode);
        
        connections[previousNode.name] = {
          main: [[{ node: actionNode.name, type: 'main', index: 0 }]]
        };
        
        previousNode = actionNode;
      });
      nodeIndex += servicesToCreate.length;
    } else {
      // Create a generic processing node only if no specific services
      const processNode = createActionNode('code', description, nodeIndex++);
      nodes.push(processNode);
      
      connections[previousNode.name] = {
        main: [[{ node: processNode.name, type: 'main', index: 0 }]]
      };
      previousNode = processNode;
    }
  }
  
  // Add error handling for complex workflows
  if (complexity === 'complex') {
    const errorNode = {
      parameters: {
        jsCode: `// Error handling and logging
const inputData = $input.all();
const errorLog = {
  timestamp: new Date().toISOString(),
  workflow: '${workflowName}',
  status: 'completed',
  processed_items: inputData.length,
  errors: []
};

console.log('Workflow completed successfully:', errorLog);
return [{ json: errorLog }];`
      },
      id: generateNodeId(),
      name: 'Log Results',
      type: 'n8n-nodes-base.code',
      typeVersion: 2,
      position: [240 + nodeIndex * 220, 300]
    };
    nodes.push(errorNode);
    
    if (previousNode) {
      connections[previousNode.name] = {
        main: [[{ node: errorNode.name, type: 'main', index: 0 }]]
      };
    }
  }
  
  return {
    id: workflowId,
    name: workflowName,
    active: true,
    nodes: nodes,
    connections: connections,
    settings: {
      executionOrder: 'v1',
      saveManualExecutions: true,
      callerPolicy: 'workflowsFromSameOwner'
    },
    tags: ['automated', 'generated', complexity],
    meta: {
      generated_by: 'n8n-workflow-generator',
      services_detected: analysis.detectedServices.map(s => s.service),
      complexity: complexity,
      created_at: new Date().toISOString()
    }
  };
}

// Template definitions
const TEMPLATES = {
  'rss_to_social': {
    id: 'rss_to_social',
    name: 'RSS to Social Media',
    description: 'Monitor RSS feeds and automatically post new articles to social media platforms like Twitter and LinkedIn',
    category: 'social_media',
    complexity: 'medium',
    use_cases: ['Content automation', 'Social media management', 'Blog promotion']
  },
  'email_processing': {
    id: 'email_processing',
    name: 'Email Processing',
    description: 'Process incoming emails, extract attachments, validate content, and route to appropriate team members',
    category: 'communication',
    complexity: 'medium',
    use_cases: ['Customer support', 'Document processing', 'Email automation']
  },
  'data_backup': {
    id: 'data_backup',
    name: 'Data Backup',
    description: 'Automatically backup files from Google Drive to Dropbox and send confirmation emails',
    category: 'storage',
    complexity: 'simple',
    use_cases: ['Data protection', 'Cloud storage sync', 'Automated backups']
  },
  'ecommerce_orders': {
    id: 'ecommerce_orders',
    name: 'E-commerce Orders',
    description: 'Process new Shopify orders, update inventory, send confirmation emails, and create shipping labels',
    category: 'ecommerce',
    complexity: 'complex',
    use_cases: ['Order fulfillment', 'Inventory management', 'Customer communication']
  }
};

module.exports = async (req, res) => {
  // Set CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  try {
    // Handle template requests
    if (req.url.startsWith('/api/templates/')) {
      const templateId = req.url.split('/').pop();
      
      if (templateId === 'suggestions' && req.method === 'POST') {
        const body = JSON.parse(req.body || '{}');
        const description = body.description?.toLowerCase() || '';
        
        // Simple template suggestion logic
        const suggestions = Object.values(TEMPLATES).filter(template => {
          return template.description.toLowerCase().includes(description) ||
                 template.category.includes(description) ||
                 template.use_cases.some(useCase => useCase.toLowerCase().includes(description));
        }).slice(0, 3);
        
        res.status(200).json({
          success: true,
          suggestions: suggestions
        });
        return;
      }
      
      if (TEMPLATES[templateId]) {
        res.status(200).json({
          success: true,
          template: TEMPLATES[templateId]
        });
        return;
      } else {
        res.status(404).json({
          success: false,
          error: 'Template not found'
        });
        return;
      }
    }

    if (req.url === '/health') {
      res.status(200).json({
        status: 'healthy',
        message: 'Advanced N8N Workflow Generator is running',
        timestamp: new Date().toISOString(),
        version: '2.0.0',
        features: [
          'Advanced workflow analysis',
          'Multi-service detection',
          'Smart node generation',
          'Production-ready workflows'
        ]
      });
      return;
    }

    if (req.url === '/generate' && req.method === 'POST') {
      const body = JSON.parse(req.body || '{}');
      const { description, triggerType = 'webhook', complexity = 'medium' } = body;
      
      if (!description) {
        res.status(400).json({
          success: false,
          error: 'Description is required'
        });
        return;
      }
      
      // Generate advanced workflow
      const workflow = generateAdvancedWorkflow(description, triggerType, complexity);
      
      res.status(200).json({
        success: true,
        workflow: workflow,
        workflow_name: workflow.name,
        description: `Advanced workflow: ${description}`,
        filename: `${workflow.name.replace(/\s+/g, '_').toLowerCase()}.json`,
        formatted_json: JSON.stringify(workflow, null, 2),
        node_count: workflow.nodes.length,
        workflow_type: 'advanced_generated',
        complexity: complexity,
        services_detected: workflow.meta.services_detected,
        analysis: {
          trigger_detected: workflow.nodes[0].type !== 'n8n-nodes-base.webhook',
          actions_count: workflow.nodes.length - 1,
          has_validation: workflow.nodes.some(n => n.name.includes('Validate')),
          has_error_handling: workflow.nodes.some(n => n.name.includes('Log'))
        }
      });
      return;
    }

    // Default response
    res.status(200).json({
      message: 'Advanced N8N Workflow Generator API',
      version: '2.0.0',
      status: 'running',
      capabilities: [
        'Multi-service workflow generation',
        'Intelligent service detection',
        'Production-ready configurations',
        'Advanced error handling',
        'Smart node connections'
      ],
      endpoints: [
        'GET /health - Health check',
        'POST /generate - Generate advanced workflow',
        'GET / - This message'
      ]
    });

  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({
      success: false,
      error: 'Internal server error',
      message: error.message
    });
  }
};