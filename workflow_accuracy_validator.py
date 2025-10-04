"""
Comprehensive n8n Workflow Accuracy Validator
Implements strict validation for node connections, data flow, and accuracy requirements.
"""

import json
import re
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of validation with detailed feedback"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    node_validation: Dict[str, Any]
    connection_validation: Dict[str, Any]
    data_flow_validation: Dict[str, Any]


class WorkflowAccuracyValidator:
    """
    Comprehensive validator for n8n workflows ensuring:
    - Only official current node types are used
    - All required parameters are present
    - Proper data flow connections exist
    - No placeholder URLs or invalid configurations
    """
    
    # Official n8n node types registry with current versions and required parameters
    OFFICIAL_NODE_TYPES = {
        # Trigger Nodes
        'n8n-nodes-base.webhook': {
            'current_type_version': 2,
            'supported_versions': [1, 2],
            'required_params': ['httpMethod', 'path'],
            'optional_params': ['responseMode', 'authentication', 'options'],
            'category': 'trigger'
        },
        'n8n-nodes-base.scheduleTrigger': {
            'current_type_version': 1,
            'supported_versions': [1],
            'required_params': ['rule'],
            'optional_params': ['timezone'],
            'category': 'trigger'
        },
        'n8n-nodes-base.manualTrigger': {
            'current_type_version': 1,
            'supported_versions': [1],
            'required_params': [],
            'optional_params': [],
            'category': 'trigger'
        },
        'n8n-nodes-base.rssFeedRead': {
            'current_type_version': 1,
            'supported_versions': [1],
            'required_params': ['url'],
            'optional_params': ['pollTimes', 'feedReadMode'],
            'category': 'trigger'
        },
        
        # Processing Nodes
        'n8n-nodes-base.httpRequest': {
            'current_type_version': 4,
            'supported_versions': [1, 2, 3, 4],
            'required_params': ['url', 'method'],
            'optional_params': ['authentication', 'sendHeaders', 'sendQuery', 'sendBody', 'options'],
            'category': 'processing'
        },
        'n8n-nodes-base.code': {
            'current_type_version': 2,
            'supported_versions': [1, 2],
            'required_params': ['jsCode'],
            'optional_params': ['mode'],
            'category': 'processing'
        },
        'n8n-nodes-base.set': {
            'current_type_version': 3,
            'supported_versions': [1, 2, 3],
            'required_params': ['values'],
            'optional_params': ['options'],
            'category': 'processing'
        },
        'n8n-nodes-base.if': {
            'current_type_version': 2,
            'supported_versions': [1, 2],
            'required_params': ['conditions'],
            'optional_params': ['combineOperation'],
            'category': 'processing'
        },
        
        # Integration Nodes
        'n8n-nodes-base.openAi': {
            'current_type_version': 1,
            'supported_versions': [1],
            'required_params': ['resource', 'operation'],
            'optional_params': ['model', 'prompt', 'maxTokens', 'temperature'],
            'category': 'integration'
        },
        'n8n-nodes-base.slack': {
            'current_type_version': 2,
            'supported_versions': [1, 2],
            'required_params': ['resource', 'operation'],
            'optional_params': ['channel', 'text', 'attachments'],
            'category': 'integration'
        },
        'n8n-nodes-base.twitter': {
            'current_type_version': 2,
            'supported_versions': [1, 2],
            'required_params': ['resource', 'operation'],
            'optional_params': ['text', 'additionalFields'],
            'category': 'integration'
        },
        'n8n-nodes-base.gmail': {
            'current_type_version': 2,
            'supported_versions': [1, 2],
            'required_params': ['resource', 'operation'],
            'optional_params': ['subject', 'message', 'toList'],
            'category': 'integration'
        },
        'n8n-nodes-base.respondToWebhook': {
            'current_type_version': 1,
            'supported_versions': [1],
            'required_params': [],
            'optional_params': ['respondWith', 'responseBody', 'responseHeaders', 'responseStatusCode'],
            'category': 'response'
        }
    }
    
    # Valid n8n data flow expression patterns
    DATA_FLOW_PATTERNS = {
        'valid_expressions': [
            r'\{\{\s*\$json\["[\w\-\.]+"\]\s*\}\}',  # {{ $json["fieldName"] }}
            r'\{\{\s*\$json\.[\w\-\.]+\s*\}\}',      # {{ $json.fieldName }}
            r'\{\{\s*\$node\["[\w\s\-\.]+"\]\.json\["[\w\-\.]+"\]\s*\}\}',  # {{ $node["Node Name"].json["field"] }}
            r'\{\{\s*\$input\.all\(\)\s*\}\}',       # {{ $input.all() }}
            r'\{\{\s*\$input\.first\(\)\s*\}\}'      # {{ $input.first() }}
        ],
        'invalid_patterns': [
            r'\{\{\s*data\.',     # Avoid generic "data." references
            r'\{\{\s*item\.',     # Avoid generic "item." references
            r'\{\{\s*response\.'  # Avoid generic "response." references
        ]
    }
    
    # Prohibited placeholder URLs
    INVALID_URLS = [
        'example.com',
        'placeholder.com',
        'your-api-endpoint.com',
        'https://example.com',
        'http://example.com',
        'test.com',
        'sample.com'
    ]
    
    # Valid URL patterns for different services
    VALID_URL_PATTERNS = {
        'rss': r'^https?:\/\/.+\.(xml|rss)(\?.*)?$',
        'api': r'^https?:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(\/.*)?$',
        'webhook': r'^https?:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(\/.*)?$'
    }
    
    def validate_complete_workflow(self, workflow: Dict[str, Any]) -> ValidationResult:
        """
        Perform comprehensive validation of the entire workflow
        """
        errors = []
        warnings = []
        suggestions = []
        node_validation = {}
        connection_validation = {}
        data_flow_validation = {}
        
        # 1. Validate workflow structure
        structure_errors = self._validate_workflow_structure(workflow)
        errors.extend(structure_errors)
        
        # 2. Validate each node for accuracy
        nodes = workflow.get('nodes', [])
        for node in nodes:
            node_result = self._validate_node_complete(node)
            node_validation[node.get('name', 'unknown')] = node_result
            
            if not node_result['is_valid']:
                errors.extend(node_result['errors'])
            warnings.extend(node_result.get('warnings', []))
        
        # 3. Validate connections and data flow
        connection_result = self._validate_workflow_connections(workflow)
        connection_validation = connection_result
        
        if not connection_result['is_valid']:
            errors.extend(connection_result['errors'])
        warnings.extend(connection_result.get('warnings', []))
        
        # 4. Validate data flow expressions
        data_flow_result = self._validate_all_data_flow_expressions(workflow)
        data_flow_validation = data_flow_result
        
        if not data_flow_result['is_valid']:
            errors.extend(data_flow_result['errors'])
        warnings.extend(data_flow_result.get('warnings', []))
        
        # 5. Generate suggestions for improvements
        suggestions = self._generate_improvement_suggestions(workflow, errors, warnings)
        
        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            node_validation=node_validation,
            connection_validation=connection_validation,
            data_flow_validation=data_flow_validation
        )
    
    def _validate_workflow_structure(self, workflow: Dict[str, Any]) -> List[str]:
        """Validate basic workflow structure"""
        errors = []
        
        required_fields = ['name', 'nodes', 'connections', 'active', 'settings']
        for field in required_fields:
            if field not in workflow:
                errors.append(f"Missing required workflow field: {field}")
        
        # Validate nodes array
        if 'nodes' in workflow:
            if not isinstance(workflow['nodes'], list):
                errors.append("Workflow 'nodes' must be an array")
            elif len(workflow['nodes']) == 0:
                errors.append("Workflow must contain at least one node")
        
        # Validate connections object
        if 'connections' in workflow:
            if not isinstance(workflow['connections'], dict):
                errors.append("Workflow 'connections' must be an object")
        
        return errors
    
    def _validate_node_complete(self, node: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a single node completely"""
        errors = []
        warnings = []
        
        # Check required node fields
        required_fields = ['id', 'name', 'type', 'typeVersion', 'position', 'parameters']
        for field in required_fields:
            if field not in node:
                errors.append(f"Node '{node.get('name', 'unknown')}' missing required field: {field}")
        
        # Validate node type and version
        node_type = node.get('type')
        type_version = node.get('typeVersion')
        
        if node_type:
            accuracy_result = self._validate_node_accuracy(node_type, type_version, node.get('parameters', {}))
            if not accuracy_result['is_valid']:
                errors.append(accuracy_result['error'])
        
        # Validate URLs and credentials
        url_errors = self._validate_url_and_credentials(node)
        errors.extend(url_errors)
        
        # Validate parameter completeness
        param_errors = self._validate_parameter_completeness(node)
        errors.extend(param_errors)
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def _validate_node_accuracy(self, node_type: str, type_version: int, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Validate node type accuracy against official registry"""
        node_spec = self.OFFICIAL_NODE_TYPES.get(node_type)
        
        if not node_spec:
            return {
                'is_valid': False,
                'error': f"Invalid node type: {node_type}. Only official n8n-nodes-base.* nodes are allowed."
            }
        
        if type_version not in node_spec['supported_versions']:
            return {
                'is_valid': False,
                'error': f"Invalid typeVersion {type_version} for {node_type}. Supported versions: {node_spec['supported_versions']}"
            }
        
        # Check required parameters
        missing_params = []
        for param in node_spec['required_params']:
            if param not in parameters:
                missing_params.append(param)
        
        if missing_params:
            return {
                'is_valid': False,
                'error': f"Missing required parameters for {node_type}: {', '.join(missing_params)}"
            }
        
        return {'is_valid': True}
    
    def _validate_workflow_connections(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Validate workflow connections ensure proper data flow"""
        errors = []
        warnings = []
        
        nodes = workflow.get('nodes', [])
        connections = workflow.get('connections', {})
        
        # Create node name mapping
        node_names = {node.get('name') for node in nodes}
        trigger_nodes = {node.get('name') for node in nodes 
                        if self._is_trigger_node(node.get('type', ''))}
        
        # Validate that non-trigger nodes have input connections
        for node in nodes:
            node_name = node.get('name')
            node_type = node.get('type', '')
            
            if not self._is_trigger_node(node_type):
                # Non-trigger nodes must have input connections
                has_input = self._node_has_input_connection(node_name, connections)
                if not has_input:
                    errors.append(f"Node '{node_name}' has no input connection. Non-trigger nodes must receive data from other nodes.")
        
        # Validate connection targets exist
        for source_name, node_connections in connections.items():
            if source_name not in node_names:
                errors.append(f"Connection source '{source_name}' does not exist in workflow")
                continue
            
            if 'main' in node_connections:
                for connection_group in node_connections['main']:
                    for connection in connection_group:
                        target_node = connection.get('node')
                        if target_node not in node_names:
                            errors.append(f"Connection target '{target_node}' does not exist in workflow")
        
        # Check for logical flow patterns (RSS → Content Generator → Content Parser → Twitter)
        flow_warnings = self._validate_logical_flow_patterns(nodes, connections)
        warnings.extend(flow_warnings)
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def _validate_logical_flow_patterns(self, nodes: List[Dict], connections: Dict) -> List[str]:
        """Validate logical flow patterns like RSS → Content Generator → Content Parser → Twitter"""
        warnings = []
        
        # Find specific node types
        rss_nodes = [n for n in nodes if n.get('type') == 'n8n-nodes-base.rssFeedRead']
        content_nodes = [n for n in nodes if 'content' in n.get('name', '').lower() or 'generate' in n.get('name', '').lower()]
        parser_nodes = [n for n in nodes if 'parse' in n.get('name', '').lower() or 'process' in n.get('name', '').lower()]
        twitter_nodes = [n for n in nodes if n.get('type') == 'n8n-nodes-base.twitter']
        
        # Check RSS → Content flow
        if rss_nodes and content_nodes:
            rss_connected_to_content = False
            for rss_node in rss_nodes:
                rss_name = rss_node.get('name')
                if rss_name in connections:
                    for connection_group in connections[rss_name].get('main', []):
                        for connection in connection_group:
                            target = connection.get('node')
                            if any(target == cn.get('name') for cn in content_nodes):
                                rss_connected_to_content = True
                                break
            
            if not rss_connected_to_content:
                warnings.append("RSS Feed Reader should be connected to Content Generator for proper data flow")
        
        # Check Content → Parser flow
        if content_nodes and parser_nodes:
            content_connected_to_parser = False
            for content_node in content_nodes:
                content_name = content_node.get('name')
                if content_name in connections:
                    for connection_group in connections[content_name].get('main', []):
                        for connection in connection_group:
                            target = connection.get('node')
                            if any(target == pn.get('name') for pn in parser_nodes):
                                content_connected_to_parser = True
                                break
            
            if not content_connected_to_parser:
                warnings.append("Content Generator should be connected to Content Parser for proper processing")
        
        # Check Parser → Twitter flow
        if parser_nodes and twitter_nodes:
            parser_connected_to_twitter = False
            for parser_node in parser_nodes:
                parser_name = parser_node.get('name')
                if parser_name in connections:
                    for connection_group in connections[parser_name].get('main', []):
                        for connection in connection_group:
                            target = connection.get('node')
                            if any(target == tn.get('name') for tn in twitter_nodes):
                                parser_connected_to_twitter = True
                                break
            
            if not parser_connected_to_twitter:
                warnings.append("Content Parser should be connected to Twitter Post for final output")
        
        return warnings
    
    def _is_trigger_node(self, node_type: str) -> bool:
        """Check if a node type is a trigger node"""
        node_spec = self.OFFICIAL_NODE_TYPES.get(node_type, {})
        return node_spec.get('category') == 'trigger'
    
    def _node_has_input_connection(self, node_name: str, connections: Dict) -> bool:
        """Check if a node has any input connections"""
        for source_connections in connections.values():
            if 'main' in source_connections:
                for connection_group in source_connections['main']:
                    for connection in connection_group:
                        if connection.get('node') == node_name:
                            return True
        return False
    
    def _validate_all_data_flow_expressions(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Validate all data flow expressions in the workflow"""
        errors = []
        warnings = []
        
        nodes = workflow.get('nodes', [])
        
        for node in nodes:
            parameters = node.get('parameters', {})
            node_name = node.get('name', 'unknown')
            
            # Check for data flow expressions in parameters
            expression_errors = self._find_and_validate_expressions(parameters, node_name)
            errors.extend(expression_errors)
        
        return {
            'is_valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    def _find_and_validate_expressions(self, obj: Any, context: str) -> List[str]:
        """Recursively find and validate data flow expressions"""
        errors = []
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                errors.extend(self._find_and_validate_expressions(value, f"{context}.{key}"))
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                errors.extend(self._find_and_validate_expressions(item, f"{context}[{i}]"))
        elif isinstance(obj, str):
            # Check for n8n expressions
            if '{{' in obj and '}}' in obj:
                validation_result = self._validate_data_flow_expression(obj)
                if not validation_result['is_valid']:
                    errors.append(f"Invalid data flow expression in {context}: {validation_result['error']}")
        
        return errors
    
    def _validate_data_flow_expression(self, expression: str) -> Dict[str, Any]:
        """Validate a single data flow expression"""
        # Check for valid patterns
        is_valid = any(re.search(pattern, expression) for pattern in self.DATA_FLOW_PATTERNS['valid_expressions'])
        
        # Check for invalid patterns
        has_invalid_pattern = any(re.search(pattern, expression) for pattern in self.DATA_FLOW_PATTERNS['invalid_patterns'])
        
        if has_invalid_pattern:
            return {
                'is_valid': False,
                'error': f"Invalid data flow expression: {expression}. Use proper n8n syntax like {{ $json[\"fieldName\"] }}"
            }
        
        if not is_valid and ('{{' in expression and '}}' in expression):
            return {
                'is_valid': False,
                'error': f"Unrecognized data flow expression pattern: {expression}. Use {{ $json.fieldName }} or {{ $json[\"fieldName\"] }}"
            }
        
        return {'is_valid': True}
    
    def _validate_url_and_credentials(self, node: Dict[str, Any]) -> List[str]:
        """Validate URLs and credentials in node parameters"""
        errors = []
        parameters = node.get('parameters', {})
        node_name = node.get('name', 'unknown')
        node_type = node.get('type', '')
        
        # Check for placeholder URLs
        url_fields = ['url', 'endpoint', 'webhookUrl', 'apiUrl']
        for field in url_fields:
            if field in parameters:
                url = str(parameters[field]).lower()
                if any(invalid_url in url for invalid_url in self.INVALID_URLS):
                    errors.append(f"Node '{node_name}' uses placeholder URL in {field}. Provide actual endpoint or mark as placeholder.")
        
        # Validate RSS URLs specifically
        if node_type == 'n8n-nodes-base.rssFeedRead' and 'url' in parameters:
            url = parameters['url']
            if not re.match(self.VALID_URL_PATTERNS['rss'], url, re.IGNORECASE):
                errors.append(f"RSS Feed node '{node_name}' requires valid RSS/XML URL")
        
        # Check credential references
        if parameters.get('authentication') and parameters['authentication'] != 'none':
            if 'credentials' not in node or not node['credentials']:
                errors.append(f"Node '{node_name}' requires authentication but no credentials specified")
        
        return errors
    
    def _validate_parameter_completeness(self, node: Dict[str, Any]) -> List[str]:
        """Validate parameter completeness for specific node types"""
        errors = []
        node_type = node.get('type', '')
        node_name = node.get('name', 'unknown')
        parameters = node.get('parameters', {})
        
        # Node-specific parameter validation
        if node_type == 'n8n-nodes-base.scheduleTrigger':
            if not parameters.get('rule') or not parameters['rule'].get('interval'):
                errors.append(f"Schedule trigger '{node_name}' missing valid cron expression or interval")
        
        elif node_type == 'n8n-nodes-base.httpRequest':
            if not parameters.get('authentication') or parameters['authentication'] == 'none':
                # This is a warning, not an error
                pass
        
        elif node_type == 'n8n-nodes-base.openAi':
            if not parameters.get('model'):
                errors.append(f"OpenAI node '{node_name}' missing model specification")
        
        return errors
    
    def _generate_improvement_suggestions(self, workflow: Dict[str, Any], errors: List[str], warnings: List[str]) -> List[str]:
        """Generate actionable improvement suggestions"""
        suggestions = []
        
        nodes = workflow.get('nodes', [])
        connections = workflow.get('connections', {})
        
        # Suggest connection improvements
        if len(nodes) > 1 and len(connections) < len(nodes) - 1:
            suggestions.append("Consider connecting more nodes to create a proper data flow pipeline")
        
        # Suggest error handling
        has_error_handling = any('error' in node.get('name', '').lower() for node in nodes)
        if not has_error_handling and len(nodes) > 2:
            suggestions.append("Add error handling nodes for production-ready workflows")
        
        # Suggest authentication setup
        auth_nodes = [n for n in nodes if n.get('type') in ['n8n-nodes-base.httpRequest', 'n8n-nodes-base.slack', 'n8n-nodes-base.twitter']]
        if auth_nodes:
            suggestions.append("Ensure all integration nodes have proper authentication configured")
        
        # Suggest data validation
        has_validation = any('valid' in node.get('name', '').lower() for node in nodes)
        if not has_validation and len(nodes) > 1:
            suggestions.append("Add data validation nodes to ensure data quality")
        
        return suggestions


def fix_workflow_connections(workflow: Dict[str, Any]) -> Dict[str, Any]:
    """
    Fix common connection issues in workflows
    Specifically addresses RSS → Content Generator → Content Parser → Twitter flow
    """
    nodes = workflow.get('nodes', [])
    connections = workflow.get('connections', {})
    
    if len(nodes) < 2:
        return workflow
    
    # Find nodes by type and name patterns
    rss_nodes = [n for n in nodes if n.get('type') == 'n8n-nodes-base.rssFeedRead']
    content_nodes = [n for n in nodes if 'content' in n.get('name', '').lower() or 'generate' in n.get('name', '').lower()]
    parser_nodes = [n for n in nodes if 'parse' in n.get('name', '').lower() or 'process' in n.get('name', '').lower()]
    twitter_nodes = [n for n in nodes if n.get('type') == 'n8n-nodes-base.twitter']
    
    # Create proper connections
    new_connections = connections.copy()
    
    # Connect RSS → Content Generator
    if rss_nodes and content_nodes:
        rss_name = rss_nodes[0].get('name')
        content_name = content_nodes[0].get('name')
        new_connections[rss_name] = {
            'main': [[{'node': content_name, 'type': 'main', 'index': 0}]]
        }
    
    # Connect Content Generator → Content Parser
    if content_nodes and parser_nodes:
        content_name = content_nodes[0].get('name')
        parser_name = parser_nodes[0].get('name')
        new_connections[content_name] = {
            'main': [[{'node': parser_name, 'type': 'main', 'index': 0}]]
        }
    
    # Connect Content Parser → Twitter
    if parser_nodes and twitter_nodes:
        parser_name = parser_nodes[0].get('name')
        twitter_name = twitter_nodes[0].get('name')
        new_connections[parser_name] = {
            'main': [[{'node': twitter_name, 'type': 'main', 'index': 0}]]
        }
    
    # If no specific pattern, create sequential connections
    if not (rss_nodes or content_nodes or parser_nodes or twitter_nodes):
        for i in range(len(nodes) - 1):
            current_node = nodes[i].get('name')
            next_node = nodes[i + 1].get('name')
            new_connections[current_node] = {
                'main': [[{'node': next_node, 'type': 'main', 'index': 0}]]
            }
    
    workflow['connections'] = new_connections
    return workflow


# Example usage and testing
if __name__ == "__main__":
    # Test the validator with a sample workflow
    validator = WorkflowAccuracyValidator()
    
    sample_workflow = {
        "name": "RSS to Twitter Workflow",
        "nodes": [
            {
                "id": "1",
                "name": "RSS Feed Reader",
                "type": "n8n-nodes-base.rssFeedRead",
                "typeVersion": 1,
                "position": [0, 300],
                "parameters": {
                    "url": "https://feeds.example.com/rss.xml"
                }
            },
            {
                "id": "2", 
                "name": "Content Generator",
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [300, 300],
                "parameters": {
                    "jsCode": "return [{ json: { content: $json.title } }];"
                }
            }
        ],
        "connections": {},
        "active": True,
        "settings": {}
    }
    
    result = validator.validate_complete_workflow(sample_workflow)
    print(f"Validation Result: {result.is_valid}")
    print(f"Errors: {result.errors}")
    print(f"Warnings: {result.warnings}")
    print(f"Suggestions: {result.suggestions}")