"""
Workflow Output Enhancement Module
Enhances and formats n8n workflow outputs for export
"""

import json
import re
from typing import Dict, Any, Optional
from datetime import datetime
import uuid

class WorkflowOutputEnhancer:
    """Enhance and format n8n workflow outputs for export"""
    
    def __init__(self, researcher_instance=None):
        self.researcher = researcher_instance
        self.enhancement_rules = self._load_enhancement_rules()
    
    def create_export_package(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a complete export package with workflow, filename, and formatted JSON"""
        
        if not isinstance(workflow, dict):
            raise ValueError("Workflow must be a dictionary")
        
        # Generate appropriate filename
        filename = self._generate_filename(workflow.get('name', 'workflow'))
        
        # Format workflow JSON for better readability
        formatted_json = self._format_workflow_json(workflow)
        
        # Validate workflow structure
        validated_workflow = self._validate_and_fix_workflow(workflow)
        
        return {
            'workflow': validated_workflow,
            'filename': filename,
            'formatted_json': formatted_json,
            'export_timestamp': datetime.now().isoformat(),
            'version': '1.0'
        }
    
    def enhance_output(self, workflow_output: Dict[str, Any]) -> Dict[str, Any]:
        """Enhances workflow output with research-based improvements"""
        
        if not isinstance(workflow_output, dict):
            return workflow_output
        
        enhanced_workflow = workflow_output.copy()
        
        # Apply enhancement rules
        enhanced_workflow = self._apply_enhancement_rules(enhanced_workflow)
        
        # Add metadata enhancements
        enhanced_workflow = self._add_metadata_enhancements(enhanced_workflow)
        
        # Optimize node positioning
        enhanced_workflow = self._optimize_node_positioning(enhanced_workflow)
        
        # Add error handling improvements
        enhanced_workflow = self._add_error_handling(enhanced_workflow)
        
        # Apply research-based improvements if researcher is available
        if self.researcher:
            enhanced_workflow = self._apply_research_insights(enhanced_workflow)
        
        return enhanced_workflow
    
    def _generate_filename(self, workflow_name: str) -> str:
        """Generates appropriate filenames for workflows"""
        
        if not workflow_name or not isinstance(workflow_name, str):
            workflow_name = "untitled_workflow"
        
        # Clean the workflow name for filename use
        clean_name = re.sub(r'[^\w\s-]', '', workflow_name.strip())
        clean_name = re.sub(r'[-\s]+', '_', clean_name)
        clean_name = clean_name.lower()
        
        # Ensure filename is not too long
        if len(clean_name) > 50:
            clean_name = clean_name[:50]
        
        # Add timestamp for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        return f"{clean_name}_{timestamp}.json"
    
    def _format_workflow_json(self, workflow: Dict[str, Any]) -> str:
        """Formats workflow JSON for better readability"""
        
        try:
            # Custom JSON formatting with proper indentation
            formatted = json.dumps(workflow, indent=2, ensure_ascii=False, sort_keys=False)
            
            # Additional formatting improvements
            formatted = self._improve_json_formatting(formatted)
            
            return formatted
            
        except (TypeError, ValueError) as e:
            # Fallback to basic formatting if custom formatting fails
            return json.dumps(workflow, indent=2, default=str)
    
    def _improve_json_formatting(self, json_string: str) -> str:
        """Apply additional formatting improvements to JSON string"""
        
        # Add extra spacing around major sections
        json_string = re.sub(r'("nodes":\s*\[)', r'\n  \1', json_string)
        json_string = re.sub(r'("connections":\s*{)', r'\n  \1', json_string)
        
        # Improve array formatting for better readability
        json_string = re.sub(r'(\],\s*)(\{)', r'\1\n    \2', json_string)
        
        return json_string
    
    def _validate_and_fix_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and fix common workflow structure issues"""
        
        validated = workflow.copy()
        
        # Ensure required fields exist
        if 'name' not in validated or not validated['name']:
            validated['name'] = 'Generated Workflow'
        
        if 'nodes' not in validated:
            validated['nodes'] = []
        
        if 'connections' not in validated:
            validated['connections'] = {}
        
        if 'active' not in validated:
            validated['active'] = True
        
        if 'settings' not in validated:
            validated['settings'] = {}
        
        if 'tags' not in validated:
            validated['tags'] = ['generated']
        
        # Validate and fix nodes
        validated['nodes'] = self._validate_nodes(validated['nodes'])
        
        # Validate and fix connections
        validated['connections'] = self._validate_connections(validated['connections'], validated['nodes'])
        
        return validated
    
    def _validate_nodes(self, nodes: list) -> list:
        """Validate and fix node structures"""
        
        validated_nodes = []
        
        for i, node in enumerate(nodes):
            if not isinstance(node, dict):
                continue
            
            validated_node = node.copy()
            
            # Ensure required node fields
            if 'id' not in validated_node or not validated_node['id']:
                validated_node['id'] = str(uuid.uuid4())[:8]
            
            if 'name' not in validated_node or not validated_node['name']:
                validated_node['name'] = f'Node {i + 1}'
            
            if 'type' not in validated_node:
                validated_node['type'] = 'n8n-nodes-base.code'
            
            if 'typeVersion' not in validated_node:
                validated_node['typeVersion'] = 1
            
            if 'position' not in validated_node or not isinstance(validated_node['position'], list):
                validated_node['position'] = [i * 300, 300]
            
            if 'parameters' not in validated_node:
                validated_node['parameters'] = {}
            
            validated_nodes.append(validated_node)
        
        return validated_nodes
    
    def _validate_connections(self, connections: dict, nodes: list) -> dict:
        """Validate and fix connection structures"""
        
        if not isinstance(connections, dict):
            return {}
        
        node_names = {node.get('name') for node in nodes if isinstance(node, dict) and 'name' in node}
        validated_connections = {}
        
        for source_node, connection_data in connections.items():
            if source_node not in node_names:
                continue
            
            if not isinstance(connection_data, dict) or 'main' not in connection_data:
                continue
            
            validated_connections[source_node] = {
                'main': self._validate_main_connections(connection_data['main'], node_names)
            }
        
        return validated_connections
    
    def _validate_main_connections(self, main_connections: list, valid_node_names: set) -> list:
        """Validate main connection arrays"""
        
        if not isinstance(main_connections, list):
            return [[]]
        
        validated_main = []
        
        for connection_group in main_connections:
            if not isinstance(connection_group, list):
                validated_main.append([])
                continue
            
            validated_group = []
            for connection in connection_group:
                if (isinstance(connection, dict) and 
                    'node' in connection and 
                    connection['node'] in valid_node_names):
                    
                    validated_connection = {
                        'node': connection['node'],
                        'type': connection.get('type', 'main'),
                        'index': connection.get('index', 0)
                    }
                    validated_group.append(validated_connection)
            
            validated_main.append(validated_group)
        
        return validated_main if validated_main else [[]]
    
    def _apply_enhancement_rules(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Apply predefined enhancement rules"""
        
        enhanced = workflow.copy()
        
        # Apply each enhancement rule
        for rule_name, rule_func in self.enhancement_rules.items():
            try:
                enhanced = rule_func(enhanced)
            except Exception as e:
                print(f"Warning: Enhancement rule '{rule_name}' failed: {e}")
        
        return enhanced
    
    def _add_metadata_enhancements(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Add metadata enhancements to the workflow"""
        
        enhanced = workflow.copy()
        
        # Add generation metadata to settings
        if 'settings' not in enhanced:
            enhanced['settings'] = {}
        
        enhanced['settings']['generated_by'] = 'n8n-workflow-generator'
        enhanced['settings']['generation_timestamp'] = datetime.now().isoformat()
        enhanced['settings']['version'] = '1.0'
        
        # Enhance tags
        if 'tags' not in enhanced:
            enhanced['tags'] = []
        
        if 'generated' not in enhanced['tags']:
            enhanced['tags'].append('generated')
        
        return enhanced
    
    def _optimize_node_positioning(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize node positioning for better visual layout"""
        
        enhanced = workflow.copy()
        nodes = enhanced.get('nodes', [])
        
        # Arrange nodes in a logical flow
        for i, node in enumerate(nodes):
            if isinstance(node, dict):
                # Position nodes horizontally with proper spacing
                x_position = i * 300
                y_position = 300
                
                # Adjust positioning for different node types
                node_type = node.get('type', '')
                if 'trigger' in node_type.lower():
                    y_position = 200  # Triggers at the top
                elif 'webhook' in node_type.lower() and 'respond' in node_type.lower():
                    y_position = 400  # Response nodes at the bottom
                
                node['position'] = [x_position, y_position]
        
        return enhanced
    
    def _add_error_handling(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Add basic error handling improvements"""
        
        enhanced = workflow.copy()
        nodes = enhanced.get('nodes', [])
        
        # Add error handling to HTTP request nodes
        for node in nodes:
            if (isinstance(node, dict) and 
                node.get('type') == 'n8n-nodes-base.httpRequest'):
                
                parameters = node.get('parameters', {})
                if 'options' not in parameters:
                    parameters['options'] = {}
                
                # Add timeout and retry options
                parameters['options']['timeout'] = 10000
                parameters['options']['retry'] = {
                    'enabled': True,
                    'maxRetries': 3
                }
        
        return enhanced
    
    def _apply_research_insights(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Apply research-based insights if researcher is available"""
        
        if not self.researcher:
            return workflow
        
        enhanced = workflow.copy()
        
        try:
            # Get recommendations from researcher
            insights = self.researcher._generate_insights()
            
            # Apply common node patterns
            node_patterns = insights.get('node_patterns', {})
            if node_patterns:
                enhanced = self._apply_node_pattern_insights(enhanced, node_patterns)
            
            # Apply connection patterns
            connection_patterns = insights.get('connection_patterns', {})
            if connection_patterns:
                enhanced = self._apply_connection_pattern_insights(enhanced, connection_patterns)
            
        except Exception as e:
            print(f"Warning: Could not apply research insights: {e}")
        
        return enhanced
    
    def _apply_node_pattern_insights(self, workflow: Dict[str, Any], patterns: Dict[str, int]) -> Dict[str, Any]:
        """Apply insights from node usage patterns"""
        
        # This could be expanded to suggest additional nodes based on patterns
        # For now, just ensure common configurations are applied
        return workflow
    
    def _apply_connection_pattern_insights(self, workflow: Dict[str, Any], patterns: Dict[str, int]) -> Dict[str, Any]:
        """Apply insights from connection patterns"""
        
        # This could be expanded to optimize connection structures
        # For now, just ensure connections are properly formatted
        return workflow
    
    def _load_enhancement_rules(self) -> Dict[str, callable]:
        """Load enhancement rules as callable functions"""
        
        return {
            'ensure_webhook_response': self._ensure_webhook_response_rule,
            'add_processing_nodes': self._add_processing_nodes_rule,
            'optimize_parameters': self._optimize_parameters_rule
        }
    
    def _ensure_webhook_response_rule(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure webhook workflows have proper response nodes"""
        
        nodes = workflow.get('nodes', [])
        has_webhook_trigger = any(
            node.get('type') == 'n8n-nodes-base.webhook' 
            for node in nodes 
            if isinstance(node, dict)
        )
        
        has_response_node = any(
            node.get('type') == 'n8n-nodes-base.respondToWebhook' 
            for node in nodes 
            if isinstance(node, dict)
        )
        
        if has_webhook_trigger and not has_response_node:
            # Add response node if missing
            response_node = {
                'parameters': {'options': {}},
                'id': str(uuid.uuid4())[:8],
                'name': 'Respond to Webhook',
                'type': 'n8n-nodes-base.respondToWebhook',
                'typeVersion': 1,
                'position': [len(nodes) * 300, 300]
            }
            workflow['nodes'].append(response_node)
        
        return workflow
    
    def _add_processing_nodes_rule(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure workflows have adequate processing nodes"""
        
        nodes = workflow.get('nodes', [])
        
        # Count processing nodes
        processing_nodes = [
            node for node in nodes 
            if isinstance(node, dict) and node.get('type') in [
                'n8n-nodes-base.code',
                'n8n-nodes-base.set',
                'n8n-nodes-base.httpRequest'
            ]
        ]
        
        # If no processing nodes, add a basic one
        if not processing_nodes and len(nodes) > 0:
            processing_node = {
                'parameters': {
                    'jsCode': '// Process data\nreturn $input.all();'
                },
                'id': str(uuid.uuid4())[:8],
                'name': 'Process Data',
                'type': 'n8n-nodes-base.code',
                'typeVersion': 2,
                'position': [300, 300]
            }
            
            # Insert processing node between first and last node
            workflow['nodes'].insert(-1 if len(nodes) > 1 else 0, processing_node)
        
        return workflow
    
    def _optimize_parameters_rule(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize node parameters for better functionality"""
        
        nodes = workflow.get('nodes', [])
        
        for node in nodes:
            if not isinstance(node, dict):
                continue
            
            node_type = node.get('type', '')
            parameters = node.get('parameters', {})
            
            # Optimize webhook parameters
            if node_type == 'n8n-nodes-base.webhook':
                if 'responseMode' not in parameters:
                    parameters['responseMode'] = 'responseNode'
                if 'httpMethod' not in parameters:
                    parameters['httpMethod'] = 'POST'
            
            # Optimize HTTP request parameters
            elif node_type == 'n8n-nodes-base.httpRequest':
                if 'options' not in parameters:
                    parameters['options'] = {}
                if 'timeout' not in parameters['options']:
                    parameters['options']['timeout'] = 10000
        
        return workflow