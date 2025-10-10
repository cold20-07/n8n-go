#!/usr/bin/env python3
"""
Workflow Accuracy Validator
Validates n8n workflows for accuracy, completeness, and best practices
"""

import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Result of workflow validation"""
    is_valid: bool
    score: float
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    metrics: Dict[str, Any]

class WorkflowAccuracyValidator:
    """Validates n8n workflows for accuracy and best practices"""
    
    def __init__(self):
        self.required_fields = {
            'workflow': ['name', 'nodes', 'connections'],
            'node': ['id', 'name', 'type', 'position', 'parameters']
        }
        
        self.node_type_patterns = {
            'trigger': ['trigger', 'webhook', 'cron', 'manual'],
            'action': ['http', 'email', 'slack', 'database'],
            'logic': ['if', 'switch', 'merge', 'split'],
            'data': ['set', 'code', 'function', 'json']
        }
    
    def validate_workflow(self, workflow: Dict[str, Any]) -> ValidationResult:
        """Validate a complete workflow"""
        return self.validate_complete_workflow(workflow)
    
    def validate_complete_workflow(self, workflow: Dict[str, Any]) -> ValidationResult:
        """Validate a complete workflow - alias for validate_workflow"""
        errors = []
        warnings = []
        suggestions = []
        metrics = {}
        
        # Basic structure validation
        structure_valid, structure_errors = self._validate_structure(workflow)
        errors.extend(structure_errors)
        
        # Node validation
        nodes_valid, node_errors, node_warnings = self._validate_nodes(workflow.get('nodes', []))
        errors.extend(node_errors)
        warnings.extend(node_warnings)
        
        # Connection validation
        connections_valid, conn_errors, conn_warnings = self._validate_connections(
            workflow.get('nodes', []), 
            workflow.get('connections', {})
        )
        errors.extend(conn_errors)
        warnings.extend(conn_warnings)
        
        # Workflow logic validation
        logic_valid, logic_warnings, logic_suggestions = self._validate_workflow_logic(workflow)
        warnings.extend(logic_warnings)
        suggestions.extend(logic_suggestions)
        
        # Calculate metrics
        metrics = self._calculate_metrics(workflow)
        
        # Calculate overall score
        score = self._calculate_score(errors, warnings, metrics)
        
        # Generate suggestions
        suggestions.extend(self._generate_suggestions(workflow, metrics))
        
        is_valid = len(errors) == 0 and score >= 75 and len(warnings) <= 3
        
        return ValidationResult(
            is_valid=is_valid,
            score=score,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            metrics=metrics
        )
    
    def _validate_structure(self, workflow: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate basic workflow structure"""
        errors = []
        
        # Check required fields
        for field in self.required_fields['workflow']:
            if field not in workflow:
                errors.append(f"Missing required field: {field}")
        
        # Check data types
        if 'nodes' in workflow and not isinstance(workflow['nodes'], list):
            errors.append("'nodes' must be a list")
        
        if 'connections' in workflow and not isinstance(workflow['connections'], dict):
            errors.append("'connections' must be a dictionary")
        
        return len(errors) == 0, errors
    
    def _validate_nodes(self, nodes: List[Dict[str, Any]]) -> Tuple[bool, List[str], List[str]]:
        """Validate workflow nodes"""
        errors = []
        warnings = []
        
        if not nodes:
            errors.append("Workflow must contain at least one node")
            return False, errors, warnings
        
        node_names = set()
        node_ids = set()
        
        for i, node in enumerate(nodes):
            # Check required fields
            for field in self.required_fields['node']:
                if field not in node:
                    errors.append(f"Node {i}: Missing required field '{field}'")
            
            # Check for duplicate names/IDs
            node_name = node.get('name', '')
            node_id = node.get('id', '')
            
            if node_name in node_names:
                errors.append(f"Duplicate node name: {node_name}")
            node_names.add(node_name)
            
            if node_id in node_ids:
                errors.append(f"Duplicate node ID: {node_id}")
            node_ids.add(node_id)
            
            # Validate node type
            node_type = node.get('type', '')
            if not node_type:
                errors.append(f"Node '{node_name}': Missing node type")
            elif not self._is_valid_node_type(node_type):
                warnings.append(f"Node '{node_name}': Unknown node type '{node_type}'")
            
            # Validate position
            position = node.get('position', {})
            if not isinstance(position, dict) or 'x' not in position or 'y' not in position:
                warnings.append(f"Node '{node_name}': Invalid or missing position")
        
        return len(errors) == 0, errors, warnings
    
    def _validate_connections(self, nodes: List[Dict[str, Any]], connections: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """Validate workflow connections"""
        errors = []
        warnings = []
        
        node_names = {node.get('name', '') for node in nodes}
        
        # Check if all nodes are connected
        connected_nodes = set()
        
        for source_node, connection_data in connections.items():
            if source_node not in node_names:
                errors.append(f"Connection source '{source_node}' does not exist")
                continue
            
            connected_nodes.add(source_node)
            
            if not isinstance(connection_data, dict):
                errors.append(f"Invalid connection data for '{source_node}'")
                continue
            
            for connection_type, connection_list in connection_data.items():
                if not isinstance(connection_list, list):
                    errors.append(f"Invalid connection list for '{source_node}.{connection_type}'")
                    continue
                
                for connection_group in connection_list:
                    if not isinstance(connection_group, list):
                        errors.append(f"Invalid connection group in '{source_node}.{connection_type}'")
                        continue
                    
                    for connection in connection_group:
                        target_node = connection.get('node', '')
                        if target_node not in node_names:
                            errors.append(f"Connection target '{target_node}' does not exist")
                        else:
                            connected_nodes.add(target_node)
        
        # Check for disconnected nodes
        disconnected_nodes = node_names - connected_nodes
        if disconnected_nodes:
            warnings.append(f"Disconnected nodes found: {list(disconnected_nodes)}")
        
        return len(errors) == 0, errors, warnings
    
    def _validate_workflow_logic(self, workflow: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
        """Validate workflow logic and flow"""
        warnings = []
        suggestions = []
        
        nodes = workflow.get('nodes', [])
        
        # Check for trigger nodes
        trigger_nodes = [node for node in nodes if self._is_trigger_node(node.get('type', ''))]
        if not trigger_nodes:
            warnings.append("No trigger node found - workflow may not start automatically")
            suggestions.append("Add a trigger node (Webhook, Cron, or Manual Trigger)")
        elif len(trigger_nodes) > 1:
            warnings.append("Multiple trigger nodes found - this may cause unexpected behavior")
        
        # Check for error handling
        error_nodes = [node for node in nodes if 'error' in node.get('type', '').lower()]
        if len(nodes) > 3 and not error_nodes:
            suggestions.append("Consider adding error handling nodes for robust workflow execution")
        
        # Check for data validation
        validation_nodes = [node for node in nodes if self._is_validation_node(node.get('type', ''))]
        if not validation_nodes and len(nodes) > 2:
            suggestions.append("Consider adding data validation nodes to ensure data quality")
        
        return True, warnings, suggestions
    
    def _calculate_metrics(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate workflow metrics"""
        nodes = workflow.get('nodes', [])
        connections = workflow.get('connections', {})
        
        # Basic metrics
        node_count = len(nodes)
        connection_count = sum(
            len(conn_list) 
            for conn_data in connections.values() 
            for conn_list in conn_data.values()
        )
        
        # Node type distribution
        node_types = {}
        for node in nodes:
            node_type = node.get('type', 'unknown')
            node_types[node_type] = node_types.get(node_type, 0) + 1
        
        # Complexity indicators
        has_conditional_logic = any('if' in node.get('type', '').lower() for node in nodes)
        has_loops = any('split' in node.get('type', '').lower() or 'batch' in node.get('type', '').lower() for node in nodes)
        has_error_handling = any('error' in node.get('type', '').lower() for node in nodes)
        
        # Calculate complexity score
        complexity_score = 0
        if node_count > 5:
            complexity_score += 1
        if connection_count > node_count:
            complexity_score += 1
        if has_conditional_logic:
            complexity_score += 1
        if has_loops:
            complexity_score += 2
        if has_error_handling:
            complexity_score += 1
        
        complexity_level = 'simple'
        if complexity_score >= 3:
            complexity_level = 'medium'
        if complexity_score >= 5:
            complexity_level = 'complex'
        
        return {
            'node_count': node_count,
            'connection_count': connection_count,
            'node_types': node_types,
            'complexity_score': complexity_score,
            'complexity_level': complexity_level,
            'has_conditional_logic': has_conditional_logic,
            'has_loops': has_loops,
            'has_error_handling': has_error_handling,
            'unique_node_types': len(node_types)
        }
    
    def _calculate_score(self, errors: List[str], warnings: List[str], metrics: Dict[str, Any]) -> float:
        """Calculate overall workflow score"""
        # Realistic scoring - no system is 100% perfect
        base_score = 95.0  # Start with realistic maximum
        
        # Deduct for errors (major issues)
        base_score -= len(errors) * 15  # Reduced penalty for more realistic scoring
        
        # Deduct for warnings (minor issues)
        base_score -= len(warnings) * 3  # Reduced penalty
        
        # Add realistic variance based on complexity
        complexity_level = metrics.get('complexity_level', 'simple')
        if complexity_level == 'complex':
            base_score -= 5  # Complex workflows are harder to get perfect
        
        # Ensure minimum realistic score
        if base_score > 98 and (errors or warnings):
            base_score = min(base_score, 97)  # Cap at 97% if there are any issues
        
        # Bonus for good practices
        if metrics.get('has_error_handling', False):
            base_score += 5
        
        if metrics.get('complexity_level') == 'medium':
            base_score += 5
        elif metrics.get('complexity_level') == 'complex':
            base_score += 10
        
        if metrics.get('unique_node_types', 0) >= 3:
            base_score += 5
        
        return max(0.0, min(100.0, base_score))
    
    def _generate_suggestions(self, workflow: Dict[str, Any], metrics: Dict[str, Any]) -> List[str]:
        """Generate improvement suggestions"""
        suggestions = []
        
        # Suggest improvements based on metrics
        if metrics.get('node_count', 0) < 3:
            suggestions.append("Consider adding more processing nodes to make the workflow more useful")
        
        if metrics.get('connection_count', 0) == 0:
            suggestions.append("Add connections between nodes to create a functional workflow")
        
        if not metrics.get('has_error_handling', False) and metrics.get('node_count', 0) > 3:
            suggestions.append("Add error handling to make the workflow more robust")
        
        if metrics.get('unique_node_types', 0) < 2:
            suggestions.append("Use different types of nodes to create more sophisticated workflows")
        
        return suggestions
    
    def _is_valid_node_type(self, node_type: str) -> bool:
        """Check if node type is valid"""
        # This is a simplified check - in reality, you'd have a comprehensive list
        common_types = [
            'webhook', 'cron', 'manual', 'http', 'email', 'slack', 'discord',
            'set', 'code', 'function', 'if', 'switch', 'merge', 'split',
            'google', 'airtable', 'notion', 'trello', 'github', 'database'
        ]
        
        return any(common_type in node_type.lower() for common_type in common_types)
    
    def _is_trigger_node(self, node_type: str) -> bool:
        """Check if node is a trigger node"""
        trigger_indicators = ['trigger', 'webhook', 'cron', 'manual', 'watch']
        return any(indicator in node_type.lower() for indicator in trigger_indicators)
    
    def _is_validation_node(self, node_type: str) -> bool:
        """Check if node is used for validation"""
        validation_indicators = ['validate', 'check', 'verify', 'code', 'function', 'if']
        return any(indicator in node_type.lower() for indicator in validation_indicators)

# Global validator instance
workflow_accuracy_validator = WorkflowAccuracyValidator()

# Convenience functions
def validate_workflow_accuracy(workflow: Dict[str, Any]) -> ValidationResult:
    """Validate workflow accuracy using the global validator"""
    return workflow_accuracy_validator.validate_workflow(workflow)

def fix_workflow_connections(workflow: Dict[str, Any]) -> Dict[str, Any]:
    """Fix common connection issues in workflows"""
    if not workflow or 'nodes' not in workflow:
        return workflow
    
    nodes = workflow.get('nodes', [])
    connections = workflow.get('connections', {})
    
    # Create a copy to avoid modifying the original
    fixed_workflow = json.loads(json.dumps(workflow))
    fixed_connections = fixed_workflow.setdefault('connections', {})
    
    # Get node names
    node_names = [node.get('name', '') for node in nodes if node.get('name')]
    
    if len(node_names) < 2:
        return fixed_workflow
    
    # If no connections exist, create basic sequential connections
    if not connections:
        for i in range(len(node_names) - 1):
            source_node = node_names[i]
            target_node = node_names[i + 1]
            
            fixed_connections[source_node] = {
                'main': [[{
                    'node': target_node,
                    'type': 'main',
                    'index': 0
                }]]
            }
    
    # Validate existing connections and fix broken ones
    else:
        for source_node, conn_data in connections.items():
            if source_node not in node_names:
                continue
                
            fixed_conn_data = {}
            for conn_type, conn_list in conn_data.items():
                fixed_conn_list = []
                for conn_group in conn_list:
                    fixed_conn_group = []
                    for conn in conn_group:
                        target_node = conn.get('node', '')
                        if target_node in node_names:
                            fixed_conn_group.append(conn)
                    if fixed_conn_group:
                        fixed_conn_list.append(fixed_conn_group)
                
                if fixed_conn_list:
                    fixed_conn_data[conn_type] = fixed_conn_list
            
            if fixed_conn_data:
                fixed_connections[source_node] = fixed_conn_data
    
    return fixed_workflow

# Example usage
if __name__ == "__main__":
    # Test with a sample workflow
    sample_workflow = {
        "name": "Test Workflow",
        "nodes": [
            {
                "id": "1",
                "name": "Webhook",
                "type": "n8n-nodes-base.webhook",
                "position": {"x": 100, "y": 100},
                "parameters": {}
            },
            {
                "id": "2", 
                "name": "Process Data",
                "type": "n8n-nodes-base.set",
                "position": {"x": 300, "y": 100},
                "parameters": {}
            }
        ],
        "connections": {
            "Webhook": {
                "main": [[{"node": "Process Data", "type": "main", "index": 0}]]
            }
        }
    }
    
    result = validate_workflow_accuracy(sample_workflow)
    print(f"Validation Result: {result}")