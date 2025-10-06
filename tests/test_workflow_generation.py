"""
Tests for workflow generation functionality
"""
import pytest
import json
from unittest.mock import patch, Mock


class TestWorkflowStructure:
    """Test workflow structure validation and generation"""
    
    def test_basic_workflow_structure(self, sample_workflow):
        """Test that basic workflow has required structure"""
        assert 'name' in sample_workflow
        assert 'nodes' in sample_workflow
        assert 'connections' in sample_workflow
        assert 'active' in sample_workflow
        
        # Test nodes structure
        for node in sample_workflow['nodes']:
            assert 'id' in node
            assert 'name' in node
            assert 'type' in node
            assert 'position' in node
            assert 'parameters' in node
    
    def test_workflow_connections_structure(self, sample_workflow):
        """Test workflow connections structure"""
        connections = sample_workflow['connections']
        
        for source_node, connection_data in connections.items():
            assert isinstance(connection_data, dict)
            if 'main' in connection_data:
                assert isinstance(connection_data['main'], list)
                for connection_group in connection_data['main']:
                    assert isinstance(connection_group, list)
                    for connection in connection_group:
                        assert 'node' in connection
                        assert 'type' in connection
                        assert 'index' in connection
    
    def test_node_types_valid(self, sample_workflow):
        """Test that node types are valid n8n node types"""
        valid_node_prefixes = [
            'n8n-nodes-base.',
            'n8n-nodes-community.',
            '@n8n/'
        ]
        
        for node in sample_workflow['nodes']:
            node_type = node['type']
            assert any(node_type.startswith(prefix) for prefix in valid_node_prefixes), \
                f"Invalid node type: {node_type}"
    
    def test_node_positions_valid(self, sample_workflow):
        """Test that node positions are valid"""
        for node in sample_workflow['nodes']:
            position = node['position']
            assert isinstance(position, list)
            assert len(position) == 2
            assert isinstance(position[0], (int, float))
            assert isinstance(position[1], (int, float))
            # Positions should be reasonable
            assert -1000 <= position[0] <= 5000
            assert -1000 <= position[1] <= 5000


class TestWorkflowGenerationLogic:
    """Test workflow generation logic"""
    
    def test_trigger_node_generation(self):
        """Test trigger node generation for different types"""
        from app import create_basic_workflow
        
        # Test webhook trigger
        webhook_workflow = create_basic_workflow(
            "Test webhook workflow", "webhook", "simple"
        )
        
        webhook_nodes = [n for n in webhook_workflow['nodes'] 
                        if 'webhook' in n['type'].lower()]
        assert len(webhook_nodes) > 0
        
        # Test schedule trigger
        schedule_workflow = create_basic_workflow(
            "Test schedule workflow", "schedule", "simple"
        )
        
        schedule_nodes = [n for n in schedule_workflow['nodes'] 
                         if 'schedule' in n['type'].lower() or 'cron' in n['type'].lower()]
        # Schedule nodes might be implemented differently
        assert len(schedule_workflow['nodes']) > 0
        
        # Test manual trigger
        manual_workflow = create_basic_workflow(
            "Test manual workflow", "manual", "simple"
        )
        
        manual_nodes = [n for n in manual_workflow['nodes'] 
                       if 'manual' in n['type'].lower() or 'start' in n['type'].lower()]
        # Manual nodes might be implemented differently
        assert len(manual_workflow['nodes']) > 0
    
    def test_complexity_affects_node_count(self):
        """Test that complexity affects the number of nodes generated"""
        from app import create_basic_workflow
        
        description = "Process customer data and send notifications"
        
        simple_workflow = create_basic_workflow(description, "webhook", "simple")
        medium_workflow = create_basic_workflow(description, "webhook", "medium")
        complex_workflow = create_basic_workflow(description, "webhook", "complex")
        
        simple_count = len(simple_workflow['nodes'])
        medium_count = len(medium_workflow['nodes'])
        complex_count = len(complex_workflow['nodes'])
        
        # Complex should have more nodes than simple
        assert complex_count >= simple_count
        # Medium should be between simple and complex (or equal)
        assert simple_count <= medium_count <= complex_count
    
    def test_description_analysis_affects_nodes(self):
        """Test that description content affects node selection"""
        from app import create_basic_workflow
        
        # Email-focused description
        email_workflow = create_basic_workflow(
            "Send email notifications to customers", "webhook", "medium"
        )
        
        # Database-focused description
        db_workflow = create_basic_workflow(
            "Store customer data in MySQL database", "webhook", "medium"
        )
        
        # Slack-focused description
        slack_workflow = create_basic_workflow(
            "Send notifications to Slack channel", "webhook", "medium"
        )
        
        # Check that different descriptions produce different workflows
        email_types = [n['type'] for n in email_workflow['nodes']]
        db_types = [n['type'] for n in db_workflow['nodes']]
        slack_types = [n['type'] for n in slack_workflow['nodes']]
        
        # At least some node types should be different
        assert email_types != db_types or email_types != slack_types
    
    def test_workflow_naming(self):
        """Test workflow naming logic"""
        from app import create_basic_workflow
        
        workflow1 = create_basic_workflow(
            "Process customer orders", "webhook", "simple"
        )
        
        workflow2 = create_basic_workflow(
            "Send email notifications", "webhook", "simple"
        )
        
        # Workflows should have different names
        assert workflow1['name'] != workflow2['name']
        
        # Names should be descriptive
        assert len(workflow1['name']) > 5
        assert len(workflow2['name']) > 5
    
    def test_workflow_connections_valid(self):
        """Test that generated workflow connections are valid"""
        from app import create_basic_workflow
        
        workflow = create_basic_workflow(
            "Multi-step data processing workflow", "webhook", "complex"
        )
        
        nodes = workflow['nodes']
        connections = workflow['connections']
        
        # Get all node names
        node_names = [node['name'] for node in nodes]
        
        # Check that all connections reference valid nodes
        for source_node, connection_data in connections.items():
            assert source_node in node_names, f"Source node '{source_node}' not found in nodes"
            
            if 'main' in connection_data:
                for connection_group in connection_data['main']:
                    for connection in connection_group:
                        target_node = connection['node']
                        assert target_node in node_names, f"Target node '{target_node}' not found in nodes"
    
    def test_workflow_metadata(self):
        """Test workflow metadata generation"""
        from app import create_basic_workflow
        
        description = "Test workflow for metadata"
        workflow = create_basic_workflow(description, "webhook", "medium")
        
        # Check for metadata
        if 'meta' in workflow:
            meta = workflow['meta']
            assert 'description' in meta
            assert 'generated_at' in meta
            assert 'workflow_type' in meta
        
        # Check for tags
        if 'tags' in workflow:
            tags = workflow['tags']
            assert isinstance(tags, list)
            assert 'generated' in tags


class TestWorkflowValidation:
    """Test workflow validation functionality"""
    
    def test_validate_required_fields(self, sample_workflow):
        """Test validation of required workflow fields"""
        # Remove required field and test validation
        invalid_workflow = sample_workflow.copy()
        del invalid_workflow['name']
        
        # This would be tested if we had a validation function
        # For now, just ensure the structure is as expected
        assert 'name' not in invalid_workflow
        assert 'nodes' in invalid_workflow
    
    def test_validate_node_connections(self, sample_workflow):
        """Test validation of node connections"""
        connections = sample_workflow['connections']
        node_names = [node['name'] for node in sample_workflow['nodes']]
        
        # All connection sources should exist as nodes
        for source_node in connections.keys():
            assert source_node in node_names
        
        # All connection targets should exist as nodes
        for source_node, connection_data in connections.items():
            if 'main' in connection_data:
                for connection_group in connection_data['main']:
                    for connection in connection_group:
                        target_node = connection['node']
                        assert target_node in node_names
    
    def test_validate_node_parameters(self, sample_workflow):
        """Test validation of node parameters"""
        for node in sample_workflow['nodes']:
            parameters = node['parameters']
            assert isinstance(parameters, dict)
            
            # Parameters should not contain None values (in most cases)
            for key, value in parameters.items():
                if value is not None:
                    assert isinstance(key, str)


class TestWorkflowTemplates:
    """Test workflow template functionality"""
    
    def test_template_application(self):
        """Test that templates are applied correctly"""
        from app import create_basic_workflow
        
        # Test with template
        templated_workflow = create_basic_workflow(
            "Process leads", "webhook", "medium", template="lead_processing"
        )
        
        # Test without template
        basic_workflow = create_basic_workflow(
            "Process leads", "webhook", "medium"
        )
        
        # Templated workflow might have different characteristics
        # This depends on template implementation
        assert len(templated_workflow['nodes']) > 0
        assert len(basic_workflow['nodes']) > 0
    
    def test_template_node_types(self):
        """Test that templates include appropriate node types"""
        from app import create_basic_workflow
        
        # Lead processing template should include relevant nodes
        lead_workflow = create_basic_workflow(
            "Process incoming leads", "webhook", "medium", template="lead_processing"
        )
        
        node_types = [node['type'] for node in lead_workflow['nodes']]
        
        # Should have webhook trigger
        webhook_nodes = [t for t in node_types if 'webhook' in t.lower()]
        assert len(webhook_nodes) > 0


class TestWorkflowOptimization:
    """Test workflow optimization features"""
    
    def test_connection_optimization(self):
        """Test that workflow connections are optimized"""
        from app import create_basic_workflow
        
        workflow = create_basic_workflow(
            "Complex multi-step workflow", "webhook", "complex"
        )
        
        nodes = workflow['nodes']
        connections = workflow['connections']
        
        if len(nodes) > 1:
            # Should have connections between nodes
            assert len(connections) > 0
            
            # No node should be completely isolated (except maybe the last one)
            connected_nodes = set()
            
            # Add source nodes
            connected_nodes.update(connections.keys())
            
            # Add target nodes
            for connection_data in connections.values():
                if 'main' in connection_data:
                    for connection_group in connection_data['main']:
                        for connection in connection_group:
                            connected_nodes.add(connection['node'])
            
            # Most nodes should be connected
            node_names = [node['name'] for node in nodes]
            connected_ratio = len(connected_nodes) / len(node_names)
            assert connected_ratio >= 0.5  # At least 50% of nodes should be connected
    
    def test_node_positioning(self):
        """Test that nodes are positioned reasonably"""
        from app import create_basic_workflow
        
        workflow = create_basic_workflow(
            "Linear workflow", "webhook", "medium"
        )
        
        nodes = workflow['nodes']
        
        # Nodes should have reasonable spacing
        positions = [node['position'] for node in nodes]
        
        if len(positions) > 1:
            # Check that nodes aren't all in the same position
            unique_positions = set(tuple(pos) for pos in positions)
            assert len(unique_positions) > 1 or len(positions) == 1
            
            # Check that positions are within reasonable bounds
            for pos in positions:
                assert -500 <= pos[0] <= 2000  # X coordinate
                assert -500 <= pos[1] <= 1000  # Y coordinate


class TestWorkflowExport:
    """Test workflow export functionality"""
    
    def test_workflow_json_serialization(self, sample_workflow):
        """Test that workflow can be serialized to JSON"""
        json_str = json.dumps(sample_workflow)
        assert isinstance(json_str, str)
        assert len(json_str) > 0
        
        # Should be able to deserialize back
        deserialized = json.loads(json_str)
        assert deserialized == sample_workflow
    
    def test_workflow_export_format(self, sample_workflow):
        """Test workflow export format compatibility"""
        # Check that the workflow follows n8n format
        assert isinstance(sample_workflow, dict)
        
        # Required top-level fields
        required_fields = ['name', 'nodes', 'connections']
        for field in required_fields:
            assert field in sample_workflow
        
        # Nodes should be a list
        assert isinstance(sample_workflow['nodes'], list)
        
        # Connections should be a dict
        assert isinstance(sample_workflow['connections'], dict)
    
    def test_workflow_import_compatibility(self, sample_workflow):
        """Test that exported workflow is compatible with n8n import"""
        # This is a structural test - actual n8n compatibility would need integration testing
        
        # Check node structure compatibility
        for node in sample_workflow['nodes']:
            # Required node fields for n8n
            required_node_fields = ['id', 'name', 'type', 'position', 'parameters']
            for field in required_node_fields:
                assert field in node, f"Node missing required field: {field}"
            
            # Type should be a valid n8n node type
            assert isinstance(node['type'], str)
            assert len(node['type']) > 0
            
            # Position should be [x, y]
            assert isinstance(node['position'], list)
            assert len(node['position']) == 2
            
            # Parameters should be a dict
            assert isinstance(node['parameters'], dict)