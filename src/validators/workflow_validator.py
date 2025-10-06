"""
Comprehensive Workflow Validation System
Validates n8n workflows for correctness, best practices, and potential issues
"""
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class ValidationLevel(Enum):
    """Validation severity levels"""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    SUCCESS = "success"

@dataclass
class ValidationIssue:
    """Represents a validation issue"""
    level: ValidationLevel
    category: str
    message: str
    node_id: Optional[str] = None
    suggestion: Optional[str] = None

@dataclass
class ValidationReport:
    """Complete validation report"""
    is_valid: bool
    score: float  # 0-100
    issues: List[ValidationIssue]
    summary: Dict[str, int]
    recommendations: List[str]

class WorkflowValidator:
    """Comprehensive workflow validator"""
    
    def __init__(self):
        self.required_node_fields = ['id', 'name', 'type', 'position', 'parameters']
        self.required_workflow_fields = ['name', 'nodes', 'connections']
        self.known_node_types = {
            'n8n-nodes-base.webhook',
            'n8n-nodes-base.cron',
            'n8n-nodes-base.manualTrigger',
            'n8n-nodes-base.httpRequest',
            'n8n-nodes-base.set',
            'n8n-nodes-base.if',
            'n8n-nodes-base.switch',
            'n8n-nodes-base.emailSend',
            'n8n-nodes-base.emailReadImap',
            'n8n-nodes-base.rssFeedRead',
            'n8n-nodes-base.twitter',
            'n8n-nodes-base.slack',
            'n8n-nodes-base.googleSheets',
            'n8n-nodes-base.googleDrive',
            'n8n-nodes-base.mysql',
            'n8n-nodes-base.postgres',
            'n8n-nodes-base.function',
            'n8n-nodes-base.code',
            'n8n-nodes-base.respondToWebhook',
            'n8n-nodes-base.scheduleTrigger',
            'n8n-nodes-base.noOp',
            '@n8n/n8n-nodes-langchain.lmChatOpenAi',
            '@n8n/n8n-nodes-langchain.chainLlm',
            '@n8n/n8n-nodes-langchain.textClassifier'
        }
    
    def validate_workflow(self, workflow: Dict[str, Any]) -> ValidationReport:
        """Perform comprehensive workflow validation"""
        issues = []
        
        # Basic structure validation
        issues.extend(self._validate_structure(workflow))
        
        # Node validation
        issues.extend(self._validate_nodes(workflow.get('nodes', [])))
        
        # Connection validation
        issues.extend(self._validate_connections(workflow))
        
        # Flow validation
        issues.extend(self._validate_flow(workflow))
        
        # Best practices validation
        issues.extend(self._validate_best_practices(workflow))
        
        # Security validation
        issues.extend(self._validate_security(workflow))
        
        # Performance validation
        issues.extend(self._validate_performance(workflow))
        
        # Calculate validation score and summary
        score = self._calculate_score(issues)
        summary = self._create_summary(issues)
        recommendations = self._generate_recommendations(issues)
        
        is_valid = not any(issue.level == ValidationLevel.ERROR for issue in issues)
        
        return ValidationReport(
            is_valid=is_valid,
            score=score,
            issues=issues,
            summary=summary,
            recommendations=recommendations
        )
    
    def _validate_structure(self, workflow: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate basic workflow structure"""
        issues = []
        
        # Check required fields
        for field in self.required_workflow_fields:
            if field not in workflow:
                issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    category="structure",
                    message=f"Missing required field: {field}",
                    suggestion=f"Add the '{field}' field to your workflow"
                ))
        
        # Check workflow name
        if 'name' in workflow:
            name = workflow['name']
            if not name or not isinstance(name, str):
                issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    category="structure",
                    message="Workflow name must be a non-empty string",
                    suggestion="Provide a descriptive name for your workflow"
                ))
            elif len(name) < 3:
                issues.append(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    category="structure",
                    message="Workflow name is very short",
                    suggestion="Use a more descriptive workflow name"
                ))
        
        # Check nodes array
        if 'nodes' in workflow:
            nodes = workflow['nodes']
            if not isinstance(nodes, list):
                issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    category="structure",
                    message="Nodes must be an array",
                    suggestion="Ensure 'nodes' is a valid array"
                ))
            elif len(nodes) == 0:
                issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    category="structure",
                    message="Workflow must have at least one node",
                    suggestion="Add nodes to your workflow"
                ))
        
        return issues
    
    def _validate_nodes(self, nodes: List[Dict[str, Any]]) -> List[ValidationIssue]:
        """Validate individual nodes"""
        issues = []
        node_ids = set()
        node_names = set()
        
        for i, node in enumerate(nodes):
            node_id = node.get('id', f'node_{i}')
            
            # Check required fields
            for field in self.required_node_fields:
                if field not in node:
                    issues.append(ValidationIssue(
                        level=ValidationLevel.ERROR,
                        category="nodes",
                        message=f"Node '{node_id}' missing required field: {field}",
                        node_id=node_id,
                        suggestion=f"Add the '{field}' field to the node"
                    ))
            
            # Check unique IDs
            if 'id' in node:
                if node['id'] in node_ids:
                    issues.append(ValidationIssue(
                        level=ValidationLevel.ERROR,
                        category="nodes",
                        message=f"Duplicate node ID: {node['id']}",
                        node_id=node_id,
                        suggestion="Ensure all node IDs are unique"
                    ))
                node_ids.add(node['id'])
            
            # Check unique names
            if 'name' in node:
                if node['name'] in node_names:
                    issues.append(ValidationIssue(
                        level=ValidationLevel.WARNING,
                        category="nodes",
                        message=f"Duplicate node name: {node['name']}",
                        node_id=node_id,
                        suggestion="Use unique names for better workflow clarity"
                    ))
                node_names.add(node['name'])
            
            # Check node type
            if 'type' in node:
                node_type = node['type']
                if node_type not in self.known_node_types:
                    issues.append(ValidationIssue(
                        level=ValidationLevel.WARNING,
                        category="nodes",
                        message=f"Unknown node type: {node_type}",
                        node_id=node_id,
                        suggestion="Verify the node type is correct and supported"
                    ))
            
            # Check position
            if 'position' in node:
                position = node['position']
                if not isinstance(position, list) or len(position) != 2:
                    issues.append(ValidationIssue(
                        level=ValidationLevel.WARNING,
                        category="nodes",
                        message=f"Invalid position format for node '{node_id}'",
                        node_id=node_id,
                        suggestion="Position should be [x, y] coordinates"
                    ))
            
            # Check parameters
            if 'parameters' in node:
                if not isinstance(node['parameters'], dict):
                    issues.append(ValidationIssue(
                        level=ValidationLevel.ERROR,
                        category="nodes",
                        message=f"Node parameters must be an object for '{node_id}'",
                        node_id=node_id,
                        suggestion="Ensure parameters is a valid object"
                    ))
        
        return issues
    
    def _validate_connections(self, workflow: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate node connections"""
        issues = []
        
        nodes = workflow.get('nodes', [])
        connections = workflow.get('connections', {})
        
        if not isinstance(connections, dict):
            issues.append(ValidationIssue(
                level=ValidationLevel.ERROR,
                category="connections",
                message="Connections must be an object",
                suggestion="Ensure connections is a valid object"
            ))
            return issues
        
        # Get all node names for validation
        node_names = {node.get('name') for node in nodes if 'name' in node}
        
        # Validate each connection
        for source_name, conn_data in connections.items():
            if source_name not in node_names:
                issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    category="connections",
                    message=f"Connection source '{source_name}' does not exist",
                    suggestion=f"Remove connection or add node named '{source_name}'"
                ))
                continue
            
            if not isinstance(conn_data, dict):
                issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    category="connections",
                    message=f"Invalid connection data for '{source_name}'",
                    suggestion="Connection data must be an object"
                ))
                continue
            
            # Check main connections
            if 'main' in conn_data:
                main_conns = conn_data['main']
                if not isinstance(main_conns, list):
                    issues.append(ValidationIssue(
                        level=ValidationLevel.ERROR,
                        category="connections",
                        message=f"Main connections must be an array for '{source_name}'",
                        suggestion="Ensure main connections is a valid array"
                    ))
                    continue
                
                for i, conn_group in enumerate(main_conns):
                    if not isinstance(conn_group, list):
                        issues.append(ValidationIssue(
                            level=ValidationLevel.ERROR,
                            category="connections",
                            message=f"Connection group must be an array for '{source_name}'",
                            suggestion="Each connection group must be an array"
                        ))
                        continue
                    
                    for conn in conn_group:
                        if not isinstance(conn, dict):
                            issues.append(ValidationIssue(
                                level=ValidationLevel.ERROR,
                                category="connections",
                                message=f"Invalid connection format in '{source_name}'",
                                suggestion="Each connection must be an object"
                            ))
                            continue
                        
                        target_node = conn.get('node')
                        if target_node not in node_names:
                            issues.append(ValidationIssue(
                                level=ValidationLevel.ERROR,
                                category="connections",
                                message=f"Connection target '{target_node}' does not exist",
                                suggestion=f"Remove connection or add node named '{target_node}'"
                            ))
        
        return issues
    
    def _validate_flow(self, workflow: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate workflow flow logic"""
        issues = []
        
        nodes = workflow.get('nodes', [])
        connections = workflow.get('connections', {})
        
        # Check for trigger nodes
        trigger_types = {
            'n8n-nodes-base.webhook',
            'n8n-nodes-base.cron',
            'n8n-nodes-base.manualTrigger',
            'n8n-nodes-base.emailReadImap'
        }
        
        trigger_nodes = [node for node in nodes if node.get('type') in trigger_types]
        
        if not trigger_nodes:
            issues.append(ValidationIssue(
                level=ValidationLevel.WARNING,
                category="flow",
                message="No trigger node found",
                suggestion="Add a trigger node to start your workflow"
            ))
        elif len(trigger_nodes) > 1:
            issues.append(ValidationIssue(
                level=ValidationLevel.INFO,
                category="flow",
                message="Multiple trigger nodes found",
                suggestion="Consider if multiple triggers are necessary"
            ))
        
        # Check for orphaned nodes (nodes with no incoming connections)
        node_names = {node.get('name') for node in nodes if 'name' in node}
        connected_nodes = set()
        
        for conn_data in connections.values():
            if 'main' in conn_data:
                for conn_group in conn_data['main']:
                    for conn in conn_group:
                        if isinstance(conn, dict) and 'node' in conn:
                            connected_nodes.add(conn['node'])
        
        # Trigger nodes don't need incoming connections
        trigger_node_names = {node.get('name') for node in trigger_nodes}
        
        orphaned_nodes = node_names - connected_nodes - trigger_node_names
        if orphaned_nodes:
            for node_name in orphaned_nodes:
                issues.append(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    category="flow",
                    message=f"Node '{node_name}' has no incoming connections",
                    suggestion="Connect this node to the workflow or remove it"
                ))
        
        # Check for dead-end nodes (nodes with no outgoing connections)
        nodes_with_outgoing = set(connections.keys())
        all_node_names = {node.get('name') for node in nodes}
        dead_end_nodes = all_node_names - nodes_with_outgoing
        
        if len(dead_end_nodes) > 1:  # It's normal to have one final node
            issues.append(ValidationIssue(
                level=ValidationLevel.INFO,
                category="flow",
                message=f"Multiple nodes with no outgoing connections: {', '.join(dead_end_nodes)}",
                suggestion="Consider if all these endpoints are intentional"
            ))
        
        return issues
    
    def _validate_best_practices(self, workflow: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate against best practices"""
        issues = []
        
        nodes = workflow.get('nodes', [])
        
        # Check workflow complexity
        if len(nodes) > 20:
            issues.append(ValidationIssue(
                level=ValidationLevel.WARNING,
                category="best_practices",
                message="Workflow has many nodes (>20)",
                suggestion="Consider breaking into smaller workflows"
            ))
        
        # Check for error handling
        error_handling_types = {'n8n-nodes-base.if', 'n8n-nodes-base.switch'}
        has_error_handling = any(node.get('type') in error_handling_types for node in nodes)
        
        if len(nodes) > 5 and not has_error_handling:
            issues.append(ValidationIssue(
                level=ValidationLevel.INFO,
                category="best_practices",
                message="Consider adding error handling nodes",
                suggestion="Add IF or Switch nodes for error handling"
            ))
        
        # Check node naming
        generic_names = {'Node', 'HTTP Request', 'Set', 'IF'}
        for node in nodes:
            name = node.get('name', '')
            if name in generic_names:
                issues.append(ValidationIssue(
                    level=ValidationLevel.INFO,
                    category="best_practices",
                    message=f"Generic node name: '{name}'",
                    node_id=node.get('id'),
                    suggestion="Use descriptive names for better workflow clarity"
                ))
        
        return issues
    
    def _validate_security(self, workflow: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate security aspects"""
        issues = []
        
        nodes = workflow.get('nodes', [])
        
        for node in nodes:
            parameters = node.get('parameters', {})
            
            # Check for hardcoded credentials
            if isinstance(parameters, dict):
                for key, value in parameters.items():
                    if isinstance(value, str):
                        if any(keyword in key.lower() for keyword in ['password', 'token', 'key', 'secret']):
                            if value and not value.startswith('{{'):  # Not an expression
                                issues.append(ValidationIssue(
                                    level=ValidationLevel.WARNING,
                                    category="security",
                                    message=f"Potential hardcoded credential in node '{node.get('name')}'",
                                    node_id=node.get('id'),
                                    suggestion="Use environment variables or expressions for credentials"
                                ))
            
            # Check HTTP nodes for HTTPS
            if node.get('type') == 'n8n-nodes-base.httpRequest':
                url = parameters.get('url', '')
                if url.startswith('http://'):
                    issues.append(ValidationIssue(
                        level=ValidationLevel.WARNING,
                        category="security",
                        message=f"HTTP request uses insecure protocol in '{node.get('name')}'",
                        node_id=node.get('id'),
                        suggestion="Use HTTPS for secure communication"
                    ))
        
        return issues
    
    def _validate_performance(self, workflow: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate performance aspects"""
        issues = []
        
        nodes = workflow.get('nodes', [])
        
        # Check for potential performance issues
        for node in nodes:
            node_type = node.get('type')
            parameters = node.get('parameters', {})
            
            # Check cron triggers for high frequency
            if node_type == 'n8n-nodes-base.cron':
                # This is a simplified check - real implementation would parse cron expression
                issues.append(ValidationIssue(
                    level=ValidationLevel.INFO,
                    category="performance",
                    message=f"Review cron schedule in '{node.get('name')}'",
                    node_id=node.get('id'),
                    suggestion="Ensure cron frequency is appropriate for your use case"
                ))
            
            # Check for large data operations
            if node_type in ['n8n-nodes-base.googleSheets', 'n8n-nodes-base.mysql']:
                issues.append(ValidationIssue(
                    level=ValidationLevel.INFO,
                    category="performance",
                    message=f"Consider data volume for '{node.get('name')}'",
                    node_id=node.get('id'),
                    suggestion="Implement pagination or limits for large datasets"
                ))
        
        return issues
    
    def _calculate_score(self, issues: List[ValidationIssue]) -> float:
        """Calculate validation score (0-100)"""
        if not issues:
            return 100.0
        
        error_weight = 20
        warning_weight = 5
        info_weight = 1
        
        total_penalty = 0
        for issue in issues:
            if issue.level == ValidationLevel.ERROR:
                total_penalty += error_weight
            elif issue.level == ValidationLevel.WARNING:
                total_penalty += warning_weight
            elif issue.level == ValidationLevel.INFO:
                total_penalty += info_weight
        
        score = max(0, 100 - total_penalty)
        return round(score, 1)
    
    def _create_summary(self, issues: List[ValidationIssue]) -> Dict[str, int]:
        """Create issue summary by level"""
        summary = {
            'errors': 0,
            'warnings': 0,
            'info': 0,
            'total': len(issues)
        }
        
        for issue in issues:
            if issue.level == ValidationLevel.ERROR:
                summary['errors'] += 1
            elif issue.level == ValidationLevel.WARNING:
                summary['warnings'] += 1
            elif issue.level == ValidationLevel.INFO:
                summary['info'] += 1
        
        return summary
    
    def _generate_recommendations(self, issues: List[ValidationIssue]) -> List[str]:
        """Generate top recommendations based on issues"""
        recommendations = []
        
        # Group issues by category
        categories = {}
        for issue in issues:
            if issue.category not in categories:
                categories[issue.category] = []
            categories[issue.category].append(issue)
        
        # Generate category-specific recommendations
        if 'structure' in categories:
            recommendations.append("Fix structural issues first - they prevent workflow execution")
        
        if 'connections' in categories:
            recommendations.append("Review node connections to ensure proper data flow")
        
        if 'security' in categories:
            recommendations.append("Address security concerns to protect sensitive data")
        
        if 'best_practices' in categories:
            recommendations.append("Follow best practices for maintainable workflows")
        
        if not recommendations:
            recommendations.append("Great job! Your workflow follows good practices")
        
        return recommendations

# Global validator instance
workflow_validator = WorkflowValidator()