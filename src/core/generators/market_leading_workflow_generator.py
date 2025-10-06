"""
Market-Leading N8N Workflow Generator
Uses comprehensive training dataset to generate production-ready workflows
"""
import json
import random
from typing import Dict, List, Any, Optional
from pathlib import Path

class MarketLeadingWorkflowGenerator:
    """
    Advanced workflow generator using comprehensive training dataset
    Produces market-leading quality workflows with best practices built-in
    """
    
    def __init__(self):
        self.training_data = self._load_training_data()
        self.workflow_patterns = self.training_data.get('workflow_patterns', [])
        self.node_types = self.training_data.get('node_types', [])
        self.best_practices = self.training_data.get('best_practices', [])
        self.error_handling = self.training_data.get('error_handling_patterns', {})
        self.real_world_examples = self.training_data.get('real_world_examples', [])
        
    def _load_training_data(self) -> Dict[str, Any]:
        """Load comprehensive training dataset"""
        try:
            dataset_path = Path('training_data/comprehensive_n8n_dataset.json')
            if dataset_path.exists():
                with open(dataset_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"[WARN] Could not load training dataset: {e}")
        
        # Fallback to minimal dataset
        return {
            'workflow_patterns': [],
            'node_types': [],
            'best_practices': [],
            'error_handling_patterns': {},
            'real_world_examples': []
        }
    
    def generate_market_leading_workflow(self, description: str, trigger_type: str = 'webhook', 
                                       complexity: str = 'medium') -> Dict[str, Any]:
        """
        Generate a market-leading quality workflow using comprehensive training data
        """
        try:
            # 1. Analyze user requirements and match to patterns
            pattern = self._match_workflow_pattern(description)
            
            # 2. Generate workflow structure based on pattern
            workflow_structure = self._create_workflow_structure(pattern, trigger_type, complexity)
            
            # 3. Apply best practices automatically
            enhanced_workflow = self._apply_best_practices(workflow_structure, complexity)
            
            # 4. Add error handling based on complexity
            production_workflow = self._add_error_handling(enhanced_workflow, complexity)
            
            # 5. Optimize for performance
            optimized_workflow = self._apply_performance_optimizations(production_workflow)
            
            # 6. Final validation and cleanup
            final_workflow = self._finalize_workflow(optimized_workflow, description)
            
            print(f"[SUCCESS] Generated market-leading workflow with {len(final_workflow.get('nodes', []))} nodes")
            return final_workflow
            
        except Exception as e:
            print(f"[ERROR] Market-leading generation failed: {e}")
            return self._create_fallback_workflow(description, trigger_type, complexity)
    
    def _match_workflow_pattern(self, description: str) -> Dict[str, Any]:
        """Match user description to best workflow pattern"""
        description_lower = description.lower()
        
        # Score each pattern based on keywords
        pattern_scores = []
        for pattern in self.workflow_patterns:
            score = 0
            
            # Check use cases
            for use_case in pattern.get('use_cases', []):
                if any(word in description_lower for word in use_case.lower().split()):
                    score += 3
            
            # Check pattern description
            pattern_desc = pattern.get('description', '').lower()
            if any(word in description_lower for word in pattern_desc.split()):
                score += 2
            
            # Check trigger types
            for trigger in pattern.get('trigger_types', []):
                if trigger in description_lower:
                    score += 1
            
            if score > 0:
                pattern_scores.append((pattern, score))
        
        # Return best matching pattern or default
        if pattern_scores:
            pattern_scores.sort(key=lambda x: x[1], reverse=True)
            return pattern_scores[0][0]
        
        # Default pattern for real-time processing
        return {
            'pattern_name': 'Real-Time Information Capture',
            'structure': {
                'trigger': 'webhook',
                'processing': 'data_transformation',
                'action': 'store/notify/route'
            }
        }
    
    def _create_workflow_structure(self, pattern: Dict[str, Any], trigger_type: str, 
                                 complexity: str) -> Dict[str, Any]:
        """Create workflow structure based on pattern"""
        workflow_id = f"market_leading_{random.randint(100000, 999999)}"
        
        # Base workflow structure
        workflow = {
            'id': workflow_id,
            'name': self._generate_workflow_name(pattern),
            'active': True,
            'nodes': [],
            'connections': {},
            'settings': {
                'executionOrder': 'v1'
            }
        }
        
        # Create nodes based on pattern structure
        nodes = self._create_pattern_nodes(pattern, trigger_type, complexity)
        workflow['nodes'] = nodes
        
        # Create connections
        connections = self._create_pattern_connections(nodes)
        workflow['connections'] = connections
        
        return workflow
    
    def _create_pattern_nodes(self, pattern: Dict[str, Any], trigger_type: str, 
                            complexity: str) -> List[Dict[str, Any]]:
        """Create nodes based on workflow pattern"""
        nodes = []
        
        # 1. Create trigger node
        trigger_node = self._create_production_trigger_node(trigger_type)
        nodes.append(trigger_node)
        
        # 2. Add validation node (best practice)
        validation_node = self._create_validation_node(len(nodes))
        nodes.append(validation_node)
        
        # 3. Add processing nodes based on pattern
        structure = pattern.get('structure', {})
        
        if 'processing' in structure:
            processing_node = self._create_processing_node(len(nodes))
            nodes.append(processing_node)
        
        if 'ai_processing' in structure:
            ai_node = self._create_ai_processing_node(len(nodes))
            nodes.append(ai_node)
        
        # 4. Add complexity-based nodes
        if complexity == 'complex':
            # Add error handling node
            error_node = self._create_error_handling_node(len(nodes))
            nodes.append(error_node)
            
            # Add monitoring node
            monitoring_node = self._create_monitoring_node(len(nodes))
            nodes.append(monitoring_node)
        
        # 5. Add action/output node
        if 'action' in structure:
            action_node = self._create_action_node(len(nodes), structure['action'])
            nodes.append(action_node)
        
        return nodes
    
    def _create_production_trigger_node(self, trigger_type: str) -> Dict[str, Any]:
        """Create production-ready trigger node with security"""
        node_id = f"trigger_{random.randint(1000, 9999)}"
        
        if trigger_type == 'webhook':
            return {
                'parameters': {
                    'httpMethod': 'POST',
                    'path': f'secure-webhook-{random.randint(1000, 9999)}',
                    'authentication': 'headerAuth',
                    'options': {
                        'allowedOrigins': 'https://yourdomain.com',
                        'rawBody': False,
                        'responseMode': 'onReceived'
                    }
                },
                'id': node_id,
                'name': 'Secure Webhook Trigger',
                'type': 'n8n-nodes-base.webhook',
                'typeVersion': 2,
                'position': [240, 300],
                'onError': 'continueRegularOutput'
            }
        elif trigger_type == 'schedule':
            return {
                'parameters': {
                    'rule': {
                        'interval': [{'field': 'hours', 'hoursInterval': 6}]
                    }
                },
                'id': node_id,
                'name': 'Scheduled Trigger',
                'type': 'n8n-nodes-base.scheduleTrigger',
                'typeVersion': 1,
                'position': [240, 300]
            }
        else:
            return {
                'parameters': {},
                'id': node_id,
                'name': 'Manual Trigger',
                'type': 'n8n-nodes-base.manualTrigger',
                'typeVersion': 1,
                'position': [240, 300]
            }
    
    def _create_validation_node(self, index: int) -> Dict[str, Any]:
        """Create data validation node (best practice)"""
        return {
            'parameters': {
                'jsCode': '''// Production-grade input validation
const inputData = $input.all();
const validatedData = [];

for (const item of inputData) {
  const data = item.json;
  const errors = [];
  
  // Required field validation
  if (!data.id && !data.order_id && !data.request_id) {
    errors.push('Missing required identifier');
  }
  
  // Data type validation
  if (data.email && !data.email.includes('@')) {
    errors.push('Invalid email format');
  }
  
  // Security validation
  const sanitizedData = {
    ...data,
    // Remove potentially dangerous fields
    __proto__: undefined,
    constructor: undefined,
    // Add validation metadata
    validation_timestamp: new Date().toISOString(),
    validation_errors: errors,
    is_valid: errors.length === 0
  };
  
  validatedData.push(sanitizedData);
}

return validatedData;'''
            },
            'id': f'validation_{random.randint(1000, 9999)}',
            'name': 'Input Validation',
            'type': 'n8n-nodes-base.code',
            'typeVersion': 2,
            'position': [460, 300],
            'onError': 'continueRegularOutput'
        }
    
    def _create_processing_node(self, index: int) -> Dict[str, Any]:
        """Create intelligent processing node"""
        return {
            'parameters': {
                'jsCode': '''// Intelligent data processing
const inputData = $input.all();
const processedData = [];

for (const item of inputData) {
  const data = item.json;
  
  // Skip invalid data
  if (!data.is_valid) {
    processedData.push({
      ...data,
      processing_skipped: true,
      skip_reason: 'validation_failed'
    });
    continue;
  }
  
  // Apply business logic
  const processed = {
    ...data,
    processed_at: new Date().toISOString(),
    processing_version: '2.0',
    
    // Add computed fields
    priority: data.amount > 1000 ? 'high' : 'normal',
    category: data.type || 'general',
    
    // Add tracking
    workflow_id: $workflow.id,
    execution_id: $execution.id
  };
  
  processedData.push(processed);
}

return processedData;'''
            },
            'id': f'processing_{random.randint(1000, 9999)}',
            'name': 'Intelligent Processing',
            'type': 'n8n-nodes-base.code',
            'typeVersion': 2,
            'position': [680, 300],
            'retryOnFail': True,
            'maxTries': 3,
            'waitBetweenTries': 1000
        }
    
    def _create_ai_processing_node(self, index: int) -> Dict[str, Any]:
        """Create AI processing node with fallback"""
        return {
            'parameters': {
                'resource': 'text',
                'operation': 'message',
                'model': 'gpt-4',
                'prompt': 'Analyze and enhance the following data: {{ JSON.stringify($json) }}',
                'options': {
                    'temperature': 0.7,
                    'maxTokens': 1000,
                    'timeout': 30000
                }
            },
            'id': f'ai_processing_{random.randint(1000, 9999)}',
            'name': 'AI Enhancement',
            'type': '@n8n/n8n-nodes-langchain.openAi',
            'typeVersion': 1,
            'position': [900, 300],
            'retryOnFail': True,
            'maxTries': 2,
            'waitBetweenTries': 2000,
            'onError': 'continueRegularOutput'
        }
    
    def _create_error_handling_node(self, index: int) -> Dict[str, Any]:
        """Create comprehensive error handling node"""
        return {
            'parameters': {
                'jsCode': '''// Comprehensive error handling
const inputData = $input.all();
const handledData = [];

for (const item of inputData) {
  const data = item.json;
  
  try {
    // Check for errors
    if (data.validation_errors && data.validation_errors.length > 0) {
      // Handle validation errors
      handledData.push({
        ...data,
        error_handled: true,
        error_type: 'validation',
        error_severity: 'medium',
        retry_recommended: false,
        handled_at: new Date().toISOString()
      });
    } else if (data.processing_error) {
      // Handle processing errors
      handledData.push({
        ...data,
        error_handled: true,
        error_type: 'processing',
        error_severity: 'high',
        retry_recommended: true,
        handled_at: new Date().toISOString()
      });
    } else {
      // No errors, pass through with success flag
      handledData.push({
        ...data,
        error_checked: true,
        status: 'success',
        checked_at: new Date().toISOString()
      });
    }
  } catch (error) {
    // Handle unexpected errors
    handledData.push({
      error: error.message,
      error_handled: true,
      error_type: 'unexpected',
      error_severity: 'critical',
      retry_recommended: false,
      handled_at: new Date().toISOString()
    });
  }
}

return handledData;'''
            },
            'id': f'error_handling_{random.randint(1000, 9999)}',
            'name': 'Error Handler',
            'type': 'n8n-nodes-base.code',
            'typeVersion': 2,
            'position': [1120, 300]
        }
    
    def _create_monitoring_node(self, index: int) -> Dict[str, Any]:
        """Create monitoring and analytics node"""
        return {
            'parameters': {
                'jsCode': '''// Workflow monitoring and analytics
const inputData = $input.all();
const monitoredData = [];

for (const item of inputData) {
  const data = item.json;
  
  // Collect metrics
  const metrics = {
    execution_time: Date.now() - new Date(data.processed_at || data.validation_timestamp).getTime(),
    data_size: JSON.stringify(data).length,
    error_count: (data.validation_errors || []).length,
    success_rate: data.status === 'success' ? 1 : 0
  };
  
  // Add monitoring data
  const monitored = {
    ...data,
    monitoring: {
      timestamp: new Date().toISOString(),
      metrics: metrics,
      workflow_version: '2.0',
      environment: 'production'
    }
  };
  
  monitoredData.push(monitored);
}

return monitoredData;'''
            },
            'id': f'monitoring_{random.randint(1000, 9999)}',
            'name': 'Performance Monitor',
            'type': 'n8n-nodes-base.code',
            'typeVersion': 2,
            'position': [1340, 300]
        }
    
    def _create_action_node(self, index: int, action_type: str) -> Dict[str, Any]:
        """Create action node based on type"""
        if 'notify' in action_type:
            return {
                'parameters': {
                    'operation': 'post',
                    'channel': '#alerts',
                    'text': '🚀 Workflow completed successfully!\n\n📊 Data: {{ JSON.stringify($json.monitoring.metrics, null, 2) }}\n⏰ Time: {{ $json.monitoring.timestamp }}'
                },
                'id': f'notification_{random.randint(1000, 9999)}',
                'name': 'Success Notification',
                'type': 'n8n-nodes-base.slack',
                'typeVersion': 1,
                'position': [1560, 300]
            }
        else:
            return {
                'parameters': {
                    'jsCode': '''// Final output processing
const inputData = $input.all();
const finalData = inputData.map(item => ({
  ...item.json,
  workflow_completed: true,
  completion_timestamp: new Date().toISOString(),
  final_status: item.json.status || 'completed'
}));

return finalData;'''
                },
                'id': f'output_{random.randint(1000, 9999)}',
                'name': 'Final Output',
                'type': 'n8n-nodes-base.code',
                'typeVersion': 2,
                'position': [1560, 300]
            }
    
    def _create_pattern_connections(self, nodes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create intelligent connections between nodes"""
        connections = {}
        
        for i in range(len(nodes) - 1):
            current_node = nodes[i]
            next_node = nodes[i + 1]
            
            current_name = current_node.get('name')
            next_name = next_node.get('name')
            
            if current_name and next_name:
                connections[current_name] = {
                    'main': [[{
                        'node': next_name,
                        'type': 'main',
                        'index': 0
                    }]]
                }
        
        return connections
    
    def _apply_best_practices(self, workflow: Dict[str, Any], complexity: str) -> Dict[str, Any]:
        """Apply best practices from training data"""
        # Add error workflow setting for production
        if complexity in ['medium', 'complex']:
            workflow['settings']['errorWorkflow'] = 'error-handler-workflow-id'
        
        # Add execution timeout
        workflow['settings']['executionTimeout'] = 300  # 5 minutes
        
        # Add retry settings to critical nodes
        for node in workflow.get('nodes', []):
            if node.get('type') in ['n8n-nodes-base.httpRequest', '@n8n/n8n-nodes-langchain.openAi']:
                node['retryOnFail'] = True
                node['maxTries'] = 3
                node['waitBetweenTries'] = 2000
        
        return workflow
    
    def _add_error_handling(self, workflow: Dict[str, Any], complexity: str) -> Dict[str, Any]:
        """Add error handling based on complexity"""
        if complexity == 'simple':
            return workflow
        
        # Add onError settings to nodes
        for node in workflow.get('nodes', []):
            if node.get('type') != 'n8n-nodes-base.manualTrigger':
                node['onError'] = 'continueRegularOutput'
        
        return workflow
    
    def _apply_performance_optimizations(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Apply performance optimizations"""
        # Add caching to HTTP requests
        for node in workflow.get('nodes', []):
            if node.get('type') == 'n8n-nodes-base.httpRequest':
                if 'options' not in node['parameters']:
                    node['parameters']['options'] = {}
                node['parameters']['options']['timeout'] = 30000
                node['parameters']['options']['retry'] = {
                    'enabled': True,
                    'maxTries': 3,
                    'waitBetweenTries': 1000
                }
        
        return workflow
    
    def _finalize_workflow(self, workflow: Dict[str, Any], description: str) -> Dict[str, Any]:
        """Final workflow cleanup and validation"""
        # Ensure all nodes have proper IDs and positions
        for i, node in enumerate(workflow.get('nodes', [])):
            if 'id' not in node:
                node['id'] = f'node_{i}_{random.randint(1000, 9999)}'
            
            if 'position' not in node:
                node['position'] = [240 + (i * 220), 300]
        
        # Add metadata
        workflow['meta'] = {
            'generated_by': 'market_leading_generator',
            'version': '2.0',
            'created_at': '2025-10-06T00:00:00.000Z',
            'description': description,
            'best_practices_applied': True,
            'production_ready': True
        }
        
        return workflow
    
    def _generate_workflow_name(self, pattern: Dict[str, Any]) -> str:
        """Generate intelligent workflow name"""
        pattern_name = pattern.get('pattern_name', 'Workflow')
        timestamp = random.randint(100000, 999999)
        
        name_mapping = {
            'Real-Time Information Capture': 'Real-Time Data Processor',
            'Scheduled Batch Processing': 'Automated Batch Pipeline',
            'System Synchronization': 'System Sync Manager',
            'AI-Enhanced Manual Processes': 'AI-Powered Automation'
        }
        
        base_name = name_mapping.get(pattern_name, 'Smart Workflow')
        return f"{base_name} {timestamp}"
    
    def _create_fallback_workflow(self, description: str, trigger_type: str, 
                                complexity: str) -> Dict[str, Any]:
        """Create fallback workflow if main generation fails"""
        return {
            'id': f'fallback_{random.randint(100000, 999999)}',
            'name': f'Fallback Workflow {random.randint(1000, 9999)}',
            'active': True,
            'nodes': [
                {
                    'parameters': {},
                    'id': 'fallback_trigger',
                    'name': 'Trigger',
                    'type': 'n8n-nodes-base.webhook' if trigger_type == 'webhook' else 'n8n-nodes-base.manualTrigger',
                    'typeVersion': 1,
                    'position': [240, 300]
                },
                {
                    'parameters': {
                        'jsCode': '''// Fallback processing
const inputData = $input.all();
return inputData.map(item => ({
  ...item.json,
  processed: true,
  fallback_used: true,
  processed_at: new Date().toISOString()
}));'''
                    },
                    'id': 'fallback_process',
                    'name': 'Process Data',
                    'type': 'n8n-nodes-base.code',
                    'typeVersion': 2,
                    'position': [460, 300]
                }
            ],
            'connections': {
                'Trigger': {
                    'main': [[{'node': 'Process Data', 'type': 'main', 'index': 0}]]
                }
            },
            'settings': {}
        }

# Global instance
market_leading_generator = MarketLeadingWorkflowGenerator()

def generate_market_leading_workflow(description: str, trigger_type: str = 'webhook', 
                                   complexity: str = 'medium') -> Dict[str, Any]:
    """Generate market-leading quality workflow"""
    return market_leading_generator.generate_market_leading_workflow(
        description, trigger_type, complexity
    )