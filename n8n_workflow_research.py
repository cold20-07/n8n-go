"""
N8n Workflow Research Module
Analyzes and provides insights for n8n workflow generation
"""

import json
import re
from typing import Dict, List, Any, Optional
from collections import defaultdict, Counter

class N8nWorkflowResearcher:
    """Research and analyze n8n workflow patterns"""
    
    def __init__(self):
        self.analyzed_workflows = []
        self.node_patterns = defaultdict(int)
        self.connection_patterns = defaultdict(int)
        self.common_configurations = {}
        self.insights = []
        
    def analyze_workflow_collection(self, workflows: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze a collection of workflows to extract patterns"""
        
        for workflow in workflows:
            self._analyze_workflow_structure(workflow)
        
        return self._generate_insights()
    
    def _analyze_workflow_structure(self, workflow: Dict[str, Any]) -> None:
        """Analyze individual workflow structure and extract patterns"""
        
        if not isinstance(workflow, dict) or 'nodes' not in workflow:
            return
        
        nodes = workflow.get('nodes', [])
        connections = workflow.get('connections', {})
        
        # Analyze node types and configurations
        for node in nodes:
            if isinstance(node, dict):
                node_type = node.get('type', '')
                if node_type:
                    self.node_patterns[node_type] += 1
                    
                    # Analyze node parameters
                    parameters = node.get('parameters', {})
                    self._analyze_node_parameters(node_type, parameters)
        
        # Analyze connection patterns
        self._analyze_connections(connections)
        
        # Store workflow for further analysis
        self.analyzed_workflows.append({
            'name': workflow.get('name', 'Unknown'),
            'node_count': len(nodes),
            'connection_count': len(connections),
            'complexity': self._calculate_complexity(nodes, connections)
        })
    
    def _analyze_node_parameters(self, node_type: str, parameters: Dict[str, Any]) -> None:
        """Analyze common parameters for each node type"""
        
        if node_type not in self.common_configurations:
            self.common_configurations[node_type] = defaultdict(Counter)
        
        for param_key, param_value in parameters.items():
            if isinstance(param_value, (str, int, bool)):
                self.common_configurations[node_type][param_key][param_value] += 1
    
    def _analyze_connections(self, connections: Dict[str, Any]) -> None:
        """Analyze connection patterns between nodes"""
        
        for source_node, connection_data in connections.items():
            if isinstance(connection_data, dict) and 'main' in connection_data:
                main_connections = connection_data['main']
                if isinstance(main_connections, list):
                    for connection_group in main_connections:
                        if isinstance(connection_group, list):
                            for connection in connection_group:
                                if isinstance(connection, dict):
                                    target_node = connection.get('node', '')
                                    if target_node:
                                        pattern = f"{source_node} -> {target_node}"
                                        self.connection_patterns[pattern] += 1
    
    def _calculate_complexity(self, nodes: List[Dict], connections: Dict) -> str:
        """Calculate workflow complexity based on nodes and connections"""
        
        node_count = len(nodes)
        connection_count = sum(
            len(conn_group) 
            for conn_data in connections.values() 
            if isinstance(conn_data, dict) and 'main' in conn_data
            for conn_group in conn_data['main']
            if isinstance(conn_group, list)
        )
        
        if node_count <= 3:
            return 'simple'
        elif node_count <= 6:
            return 'medium'
        else:
            return 'complex'
    
    def _generate_insights(self) -> Dict[str, Any]:
        """Generate insights from analyzed workflows"""
        
        total_workflows = len(self.analyzed_workflows)
        
        if total_workflows == 0:
            return {
                'node_patterns': {},
                'connection_patterns': {},
                'insights': ['No workflows analyzed yet'],
                'recommendations': []
            }
        
        # Most common node types
        most_common_nodes = dict(Counter(self.node_patterns).most_common(10))
        
        # Most common connection patterns
        most_common_connections = dict(Counter(self.connection_patterns).most_common(10))
        
        # Generate insights
        insights = []
        recommendations = []
        
        # Node usage insights
        if most_common_nodes:
            top_node = max(most_common_nodes, key=most_common_nodes.get)
            insights.append(f"Most commonly used node type: {top_node}")
            recommendations.append(f"Consider using {top_node} for similar workflows")
        
        # Complexity insights
        complexity_distribution = Counter(w['complexity'] for w in self.analyzed_workflows)
        if complexity_distribution:
            most_common_complexity = complexity_distribution.most_common(1)[0][0]
            insights.append(f"Most common workflow complexity: {most_common_complexity}")
        
        # Connection insights
        if most_common_connections:
            insights.append(f"Found {len(most_common_connections)} common connection patterns")
        
        return {
            'node_patterns': most_common_nodes,
            'connection_patterns': most_common_connections,
            'insights': insights,
            'recommendations': recommendations,
            'workflow_stats': {
                'total_analyzed': total_workflows,
                'complexity_distribution': dict(complexity_distribution),
                'average_nodes': sum(w['node_count'] for w in self.analyzed_workflows) / total_workflows if total_workflows > 0 else 0
            }
        }
    
    def get_node_recommendations(self, workflow_type: str, complexity: str) -> List[Dict[str, Any]]:
        """Get node recommendations based on workflow type and complexity"""
        
        recommendations = []
        
        # Base recommendations for all workflows
        base_nodes = [
            {
                'type': 'n8n-nodes-base.webhook',
                'name': 'Webhook Trigger',
                'description': 'Receives HTTP requests to start the workflow'
            },
            {
                'type': 'n8n-nodes-base.code',
                'name': 'Process Data',
                'description': 'Process and transform incoming data'
            }
        ]
        
        # Add complexity-based recommendations
        if complexity in ['medium', 'complex']:
            base_nodes.extend([
                {
                    'type': 'n8n-nodes-base.if',
                    'name': 'Conditional Logic',
                    'description': 'Add branching logic based on conditions'
                },
                {
                    'type': 'n8n-nodes-base.httpRequest',
                    'name': 'HTTP Request',
                    'description': 'Make API calls to external services'
                }
            ])
        
        if complexity == 'complex':
            base_nodes.extend([
                {
                    'type': 'n8n-nodes-base.slack',
                    'name': 'Slack Integration',
                    'description': 'Send notifications to Slack channels'
                },
                {
                    'type': 'n8n-nodes-base.set',
                    'name': 'Data Manipulation',
                    'description': 'Transform and structure data'
                }
            ])
        
        return base_nodes
    
    def get_connection_recommendations(self, nodes: List[Dict[str, Any]]) -> Dict[str, List[Dict]]:
        """Generate connection recommendations based on node types"""
        
        connections = {}
        
        for i, node in enumerate(nodes):
            node_name = node.get('name', f'Node {i}')
            
            if i < len(nodes) - 1:
                next_node = nodes[i + 1]
                next_node_name = next_node.get('name', f'Node {i + 1}')
                
                connections[node_name] = {
                    'main': [[{
                        'node': next_node_name,
                        'type': 'main',
                        'index': 0
                    }]]
                }
        
        return connections
    
    def export_analysis(self) -> Dict[str, Any]:
        """Export complete analysis results"""
        
        return {
            'analyzed_workflows': self.analyzed_workflows,
            'node_patterns': dict(self.node_patterns),
            'connection_patterns': dict(self.connection_patterns),
            'common_configurations': {
                node_type: {
                    param: dict(values) 
                    for param, values in params.items()
                }
                for node_type, params in self.common_configurations.items()
            },
            'insights': self._generate_insights()
        }