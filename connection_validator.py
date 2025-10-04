"""
Connection Validator and Fixer for n8n Workflows
Specifically addresses the RSS → Content Generator → Content Parser → Twitter connection issue
"""

from typing import Dict, List, Any, Tuple
from workflow_accuracy_validator import WorkflowAccuracyValidator, fix_workflow_connections


class ConnectionValidator:
    """
    Validates and fixes workflow connections to ensure proper data flow
    """
    
    def __init__(self):
        self.accuracy_validator = WorkflowAccuracyValidator()
    
    def validate_and_fix_connections(self, workflow: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Validate workflow connections and fix common issues
        Returns: (fixed_workflow, validation_report)
        """
        # First, validate the current workflow
        validation_result = self.accuracy_validator.validate_complete_workflow(workflow)
        
        # Fix connections if there are issues
        fixed_workflow = workflow.copy()
        
        if not validation_result.is_valid or validation_result.warnings:
            print("🔧 Fixing workflow connections...")
            fixed_workflow = fix_workflow_connections(workflow)
            
            # Validate again after fixing
            post_fix_validation = self.accuracy_validator.validate_complete_workflow(fixed_workflow)
            
            validation_report = {
                'original_validation': {
                    'is_valid': validation_result.is_valid,
                    'errors': validation_result.errors,
                    'warnings': validation_result.warnings,
                    'suggestions': validation_result.suggestions
                },
                'post_fix_validation': {
                    'is_valid': post_fix_validation.is_valid,
                    'errors': post_fix_validation.errors,
                    'warnings': post_fix_validation.warnings,
                    'suggestions': post_fix_validation.suggestions
                },
                'fixes_applied': self._get_fixes_applied(workflow, fixed_workflow),
                'connection_improvements': self._analyze_connection_improvements(workflow, fixed_workflow)
            }
        else:
            validation_report = {
                'original_validation': {
                    'is_valid': validation_result.is_valid,
                    'errors': validation_result.errors,
                    'warnings': validation_result.warnings,
                    'suggestions': validation_result.suggestions
                },
                'fixes_applied': [],
                'connection_improvements': []
            }
        
        return fixed_workflow, validation_report
    
    def _get_fixes_applied(self, original: Dict[str, Any], fixed: Dict[str, Any]) -> List[str]:
        """Identify what fixes were applied"""
        fixes = []
        
        original_connections = original.get('connections', {})
        fixed_connections = fixed.get('connections', {})
        
        # Check for new connections
        for source, connections in fixed_connections.items():
            if source not in original_connections:
                if 'main' in connections:
                    for connection_group in connections['main']:
                        for connection in connection_group:
                            target = connection.get('node')
                            fixes.append(f"Added connection: {source} → {target}")
            else:
                # Check for modified connections
                original_targets = set()
                if 'main' in original_connections[source]:
                    for group in original_connections[source]['main']:
                        for conn in group:
                            original_targets.add(conn.get('node'))
                
                fixed_targets = set()
                if 'main' in connections:
                    for group in connections['main']:
                        for conn in group:
                            fixed_targets.add(conn.get('node'))
                
                new_targets = fixed_targets - original_targets
                for target in new_targets:
                    fixes.append(f"Added connection: {source} → {target}")
        
        return fixes
    
    def _analyze_connection_improvements(self, original: Dict[str, Any], fixed: Dict[str, Any]) -> List[str]:
        """Analyze connection improvements made"""
        improvements = []
        
        original_nodes = original.get('nodes', [])
        original_connections = original.get('connections', {})
        fixed_connections = fixed.get('connections', {})
        
        # Count connections
        original_connection_count = sum(
            len(group) for connections in original_connections.values() 
            for group in connections.get('main', [])
        )
        
        fixed_connection_count = sum(
            len(group) for connections in fixed_connections.values() 
            for group in connections.get('main', [])
        )
        
        if fixed_connection_count > original_connection_count:
            improvements.append(f"Increased connections from {original_connection_count} to {fixed_connection_count}")
        
        # Check for specific flow patterns
        if self._has_rss_to_twitter_flow(fixed):
            improvements.append("Established RSS → Content → Parser → Twitter data flow")
        
        # Check for proper sequential flow
        if len(original_nodes) > 1:
            connected_nodes = self._count_connected_nodes(fixed_connections, original_nodes)
            if connected_nodes == len(original_nodes):
                improvements.append("All nodes are now properly connected in sequence")
        
        return improvements
    
    def _has_rss_to_twitter_flow(self, workflow: Dict[str, Any]) -> bool:
        """Check if workflow has RSS to Twitter flow pattern"""
        nodes = workflow.get('nodes', [])
        connections = workflow.get('connections', {})
        
        rss_nodes = [n for n in nodes if n.get('type') == 'n8n-nodes-base.rssFeedRead']
        twitter_nodes = [n for n in nodes if n.get('type') == 'n8n-nodes-base.twitter']
        
        if not (rss_nodes and twitter_nodes):
            return False
        
        # Check if there's a path from RSS to Twitter
        return self._has_connection_path(connections, rss_nodes[0].get('name'), twitter_nodes[0].get('name'))
    
    def _has_connection_path(self, connections: Dict[str, Any], start: str, end: str, visited: set = None) -> bool:
        """Check if there's a connection path between two nodes"""
        if visited is None:
            visited = set()
        
        if start == end:
            return True
        
        if start in visited:
            return False
        
        visited.add(start)
        
        if start in connections and 'main' in connections[start]:
            for connection_group in connections[start]['main']:
                for connection in connection_group:
                    target = connection.get('node')
                    if self._has_connection_path(connections, target, end, visited.copy()):
                        return True
        
        return False
    
    def _count_connected_nodes(self, connections: Dict[str, Any], nodes: List[Dict]) -> int:
        """Count how many nodes are connected"""
        connected = set()
        
        for source, node_connections in connections.items():
            connected.add(source)
            if 'main' in node_connections:
                for connection_group in node_connections['main']:
                    for connection in connection_group:
                        connected.add(connection.get('node'))
        
        return len(connected)
    
    def create_sequential_connections(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Create sequential connections between all nodes"""
        nodes = workflow.get('nodes', [])
        
        if len(nodes) < 2:
            return workflow
        
        connections = {}
        
        for i in range(len(nodes) - 1):
            current_node = nodes[i].get('name')
            next_node = nodes[i + 1].get('name')
            
            connections[current_node] = {
                'main': [[{'node': next_node, 'type': 'main', 'index': 0}]]
            }
        
        workflow['connections'] = connections
        return workflow
    
    def create_smart_connections(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Create smart connections based on node types and names"""
        nodes = workflow.get('nodes', [])
        
        if len(nodes) < 2:
            return workflow
        
        # Categorize nodes
        trigger_nodes = []
        processing_nodes = []
        output_nodes = []
        
        for node in nodes:
            node_type = node.get('type', '')
            node_name = node.get('name', '').lower()
            
            if self.accuracy_validator._is_trigger_node(node_type):
                trigger_nodes.append(node)
            elif any(keyword in node_name for keyword in ['slack', 'twitter', 'email', 'send', 'post']):
                output_nodes.append(node)
            else:
                processing_nodes.append(node)
        
        # Create logical connections
        connections = {}
        
        # Connect triggers to first processing node or output
        if trigger_nodes:
            trigger = trigger_nodes[0]
            if processing_nodes:
                target = processing_nodes[0]
            elif output_nodes:
                target = output_nodes[0]
            else:
                return workflow
            
            connections[trigger.get('name')] = {
                'main': [[{'node': target.get('name'), 'type': 'main', 'index': 0}]]
            }
        
        # Connect processing nodes in sequence
        for i in range(len(processing_nodes) - 1):
            current = processing_nodes[i]
            next_node = processing_nodes[i + 1]
            
            connections[current.get('name')] = {
                'main': [[{'node': next_node.get('name'), 'type': 'main', 'index': 0}]]
            }
        
        # Connect last processing node to output
        if processing_nodes and output_nodes:
            last_processing = processing_nodes[-1]
            output = output_nodes[0]
            
            connections[last_processing.get('name')] = {
                'main': [[{'node': output.get('name'), 'type': 'main', 'index': 0}]]
            }
        
        workflow['connections'] = connections
        return workflow


# Test the connection validator
if __name__ == "__main__":
    validator = ConnectionValidator()
    
    # Test workflow with connection issues
    test_workflow = {
        "name": "RSS to Twitter Test",
        "nodes": [
            {
                "id": "1",
                "name": "RSS Feed Reader",
                "type": "n8n-nodes-base.rssFeedRead",
                "typeVersion": 1,
                "position": [0, 300],
                "parameters": {"url": "https://example.com/feed.xml"}
            },
            {
                "id": "2",
                "name": "Content Generator", 
                "type": "n8n-nodes-base.code",
                "typeVersion": 2,
                "position": [300, 300],
                "parameters": {"jsCode": "return [{ json: { content: $json.title } }];"}
            },
            {
                "id": "3",
                "name": "Content Parser",
                "type": "n8n-nodes-base.code", 
                "typeVersion": 2,
                "position": [600, 300],
                "parameters": {"jsCode": "return [{ json: { parsed: $json.content } }];"}
            },
            {
                "id": "4",
                "name": "Twitter Post",
                "type": "n8n-nodes-base.twitter",
                "typeVersion": 2,
                "position": [900, 300],
                "parameters": {"resource": "tweet", "operation": "create"}
            }
        ],
        "connections": {},  # No connections - this is the problem!
        "active": True,
        "settings": {}
    }
    
    fixed_workflow, report = validator.validate_and_fix_connections(test_workflow)
    
    print("🔍 Validation Report:")
    print(f"Original valid: {report['original_validation']['is_valid']}")
    print(f"Original errors: {report['original_validation']['errors']}")
    print(f"Fixes applied: {report['fixes_applied']}")
    print(f"Connection improvements: {report['connection_improvements']}")
    
    print("\n🔗 Fixed Connections:")
    for source, connections in fixed_workflow.get('connections', {}).items():
        for group in connections.get('main', []):
            for conn in group:
                print(f"  {source} → {conn['node']}")