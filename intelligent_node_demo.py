#!/usr/bin/env python3
"""
Demonstration of Intelligent Node Generation System
This shows how the system should analyze user prompts and generate appropriate n8n nodes
"""

import json
import re

def analyze_user_prompt(description):
    """Analyze user prompt to determine exactly what n8n nodes are needed"""
    desc_lower = description.lower()
    required_nodes = []
    
    print(f"🔍 Analyzing: {description}")
    print("=" * 60)
    
    # Check for specific integrations and services mentioned
    if any(word in desc_lower for word in ['slack', 'team notification', 'channel']):
        slack_details = extract_slack_details(description)
        required_nodes.append({
            'type': 'n8n-nodes-base.slack',
            'name': 'Send Slack Notification',
            'parameters': {
                'resource': 'message',
                'operation': 'post',
                'channel': slack_details['channel'],
                'text': slack_details['message'],
                'otherOptions': {'mrkdwn': True}
            }
        })
        print(f"✅ Detected Slack integration -> Channel: {slack_details['channel']}")
    
    if any(word in desc_lower for word in ['email', 'mail', 'gmail', 'send notification']):
        email_details = extract_email_details(description)
        required_nodes.append({
            'type': 'n8n-nodes-base.emailSend',
            'name': 'Send Email Notification',
            'parameters': {
                'fromEmail': 'noreply@example.com',
                'toEmail': email_details['to_field'],
                'subject': email_details['subject'],
                'text': email_details['body']
            }
        })
        print(f"✅ Detected Email integration -> To: {email_details['to_field']}")
    
    if any(word in desc_lower for word in ['database', 'mysql', 'postgres', 'store', 'save data']):
        db_details = extract_database_details(description)
        required_nodes.append({
            'type': 'n8n-nodes-base.mysql',
            'name': f'Store in {db_details["table"]}',
            'parameters': {
                'operation': db_details['operation'],
                'table': db_details['table'],
                'columns': ', '.join(db_details['fields']),
                'values': '{{ $json.name }}, {{ $json.email }}, {{ JSON.stringify($json) }}, {{ new Date().toISOString() }}'
            }
        })
        print(f"✅ Detected Database integration -> Table: {db_details['table']}")
    
    if any(word in desc_lower for word in ['sheets', 'spreadsheet', 'excel', 'google sheets']):
        required_nodes.append({
            'type': 'n8n-nodes-base.googleSheets',
            'name': 'Update Spreadsheet',
            'parameters': {
                'resource': 'spreadsheet',
                'operation': 'append',
                'documentId': 'YOUR_SPREADSHEET_ID',
                'sheetName': 'Sheet1',
                'range': 'A:Z',
                'values': '={{ [[$json.name, $json.email, $json.timestamp]] }}'
            }
        })
        print("✅ Detected Google Sheets integration")
    
    if any(word in desc_lower for word in ['api', 'http', 'rest', 'endpoint', 'service']):
        api_details = extract_api_details(description)
        required_nodes.append({
            'type': 'n8n-nodes-base.httpRequest',
            'name': 'API Request',
            'parameters': {
                'url': api_details['url'],
                'httpMethod': api_details['method'],
                'sendBody': api_details['send_data'],
                'bodyContentType': 'json',
                'jsonBody': '={{ $json }}' if api_details['send_data'] else ''
            }
        })
        print(f"✅ Detected API integration -> Method: {api_details['method']}")
    
    # Check for data operations
    if any(word in desc_lower for word in ['validate', 'verify', 'check', 'ensure']):
        validation_code = generate_validation_code(description)
        required_nodes.append({
            'type': 'n8n-nodes-base.code',
            'name': 'Validate Data',
            'parameters': {
                'jsCode': validation_code
            }
        })
        print("✅ Detected Validation requirement")
    
    if any(word in desc_lower for word in ['transform', 'convert', 'format', 'modify']):
        transform_code = generate_transformation_code(description)
        required_nodes.append({
            'type': 'n8n-nodes-base.code',
            'name': 'Transform Data',
            'parameters': {
                'jsCode': transform_code
            }
        })
        print("✅ Detected Transformation requirement")
    
    if any(word in desc_lower for word in ['condition', 'if', 'when', 'filter', 'route']):
        condition_details = extract_conditional_details(description)
        required_nodes.append({
            'type': 'n8n-nodes-base.if',
            'name': 'Route Data',
            'parameters': {
                'conditions': {
                    'options': {'caseSensitive': True},
                    'conditions': [{
                        'leftValue': f'={{{{ $json.{condition_details["field"]} }}}}',
                        'rightValue': condition_details['value'],
                        'operator': {'type': 'string', 'operation': 'equals'}
                    }],
                    'combinator': 'and'
                }
            }
        })
        print(f"✅ Detected Conditional logic -> {condition_details['field']} = {condition_details['value']}")
    
    return required_nodes

def extract_slack_details(description):
    """Extract Slack-specific details from description"""
    channel_match = re.search(r'#(\w+)', description)
    channel = f"#{channel_match.group(1)}" if channel_match else '#general'
    
    if 'sales' in description.lower():
        channel = '#sales'
    elif 'support' in description.lower():
        channel = '#support'
    
    # Generate appropriate message based on context
    if 'lead' in description.lower():
        message = '🎯 *New Lead Alert*\\n\\n*Name:* {{ $json.name }}\\n*Email:* {{ $json.email }}\\n*Source:* {{ $json.source }}'
    elif 'order' in description.lower():
        message = '🛒 *New Order*\\n\\n*Order ID:* {{ $json.orderId }}\\n*Customer:* {{ $json.customerName }}\\n*Amount:* ${{ $json.amount }}'
    else:
        message = '📋 *Workflow Notification*\\n\\n*Status:* {{ $json.status }}\\n*Data:* {{ $json.message }}'
    
    return {'channel': channel, 'message': message}

def extract_email_details(description):
    """Extract email-specific details from description"""
    email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,})', description)
    to_field = email_match.group(1) if email_match else '{{ $json.email || "admin@example.com" }}'
    
    if 'confirmation' in description.lower():
        subject = 'Order Confirmation - {{ $json.orderId }}'
        body = 'Thank you for your order. Order ID: {{ $json.orderId }}\\n\\nDetails: {{ JSON.stringify($json, null, 2) }}'
    elif 'alert' in description.lower():
        subject = 'System Alert - {{ $json.type }}'
        body = 'Alert: {{ $json.message }}\\n\\nTime: {{ new Date().toISOString() }}'
    else:
        subject = 'Workflow Notification'
        body = 'Notification: {{ $json.message }}\\n\\nData: {{ JSON.stringify($json, null, 2) }}'
    
    return {'to_field': to_field, 'subject': subject, 'body': body}

def extract_database_details(description):
    """Extract database-specific details from description"""
    operation = 'insert'
    if any(word in description.lower() for word in ['update', 'modify']):
        operation = 'update'
    
    # Try to extract table name from context
    table = 'workflow_data'
    if 'customer' in description.lower():
        table = 'customers'
    elif 'order' in description.lower():
        table = 'orders'
    elif 'lead' in description.lower():
        table = 'leads'
    
    fields = ['name', 'email', 'data', 'created_at']
    
    return {'operation': operation, 'table': table, 'fields': fields}

def extract_api_details(description):
    """Extract API call specific details"""
    method = 'POST'
    if 'get' in description.lower() or 'fetch' in description.lower():
        method = 'GET'
    elif 'put' in description.lower():
        method = 'PUT'
    
    return {
        'method': method,
        'url': 'https://api.example.com/data',
        'send_data': method in ['POST', 'PUT']
    }

def extract_conditional_details(description):
    """Extract conditional logic details"""
    # Try to extract specific conditions
    if_match = re.search(r'if\\s+(\\w+)\\s+(?:is|equals?)\\s+(\\w+)', description.lower())
    if if_match:
        return {'field': if_match.group(1), 'value': if_match.group(2)}
    
    return {'field': 'status', 'value': 'active'}

def generate_validation_code(description):
    """Generate validation code based on requirements"""
    code = """// Intelligent data validation
const inputData = $input.all();
const validatedData = [];

inputData.forEach(item => {
  const data = item.json;
  const validation = { isValid: true, errors: [] };
  
"""
    
    if 'email' in description.lower():
        code += """  // Email validation
  if (!data.email || !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(data.email)) {
    validation.isValid = false;
    validation.errors.push('Invalid email format');
  }
  
"""
    
    if 'phone' in description.lower():
        code += """  // Phone validation
  if (data.phone && !/^[\\+]?[1-9][\\d]{0,15}$/.test(data.phone.replace(/\\s/g, ''))) {
    validation.isValid = false;
    validation.errors.push('Invalid phone number');
  }
  
"""
    
    code += """  if (validation.isValid) {
    validatedData.push({ ...data, validated: true, validatedAt: new Date().toISOString() });
  } else {
    throw new Error('Validation failed: ' + validation.errors.join(', '));
  }
});

return validatedData;"""
    
    return code

def generate_transformation_code(description):
    """Generate transformation code based on requirements"""
    code = """// Intelligent data transformation
const inputData = $input.all();
const transformedData = inputData.map(item => {
  const data = item.json;
  
  return {
    ...data,
    processed: true,
    processedAt: new Date().toISOString(),
"""
    
    if 'normalize' in description.lower():
        code += """    // Normalize data
    email: data.email ? data.email.toLowerCase().trim() : '',
    name: data.name ? data.name.trim() : '',
"""
    
    if 'enrich' in description.lower():
        code += """    // Enrich with metadata
    source: 'n8n-workflow',
    enriched: true,
"""
    
    code += """    workflowId: '{{ $workflow.id }}'
  };
});

return transformedData;"""
    
    return code

def test_intelligent_generation():
    """Test the intelligent node generation with various scenarios"""
    test_cases = [
        "Create a workflow that receives customer orders via webhook, validates the order data, stores it in a MySQL database, and sends confirmation emails to customers",
        "Build a lead processing system that gets leads from a form, validates email addresses, sends notifications to the sales team via Slack, and updates a Google Sheets spreadsheet",
        "Create an API integration that fetches data from an external service, transforms the format, and stores results in the database",
        "Design a monitoring workflow that checks system status via API calls, and if there are errors, sends alerts to the #support Slack channel",
        "Build a customer feedback system that receives feedback via webhook, validates the data, stores it in a database, and sends thank you emails"
    ]
    
    print("🚀 INTELLIGENT NODE GENERATION DEMONSTRATION")
    print("=" * 80)
    print()
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📋 TEST CASE {i}")
        nodes = analyze_user_prompt(test_case)
        
        print(f"\\n🎯 Generated {len(nodes)} intelligent nodes:")
        for j, node in enumerate(nodes, 1):
            node_type = node['type'].split('.')[-1]
            print(f"   {j}. {node['name']} ({node_type})")
            
            # Show key parameters
            params = node['parameters']
            if 'channel' in params:
                print(f"      → Slack Channel: {params['channel']}")
            elif 'toEmail' in params:
                print(f"      → Email To: {params['toEmail']}")
            elif 'table' in params:
                print(f"      → Database Table: {params['table']}")
            elif 'url' in params:
                print(f"      → API URL: {params['url']}")
            elif 'jsCode' in params:
                print(f"      → Custom Logic: {len(params['jsCode'])} chars")
        
        print("\\n" + "="*60 + "\\n")

if __name__ == "__main__":
    test_intelligent_generation()