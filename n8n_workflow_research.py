#!/usr/bin/env python3
"""
N8N Workflow Research Module
Advanced workflow analysis and research capabilities for n8n workflow generation
"""

import json
import logging
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict

logger = logging.getLogger(__name__)

@dataclass
class WorkflowPattern:
    """Represents a workflow pattern with metadata"""
    name: str
    description: str
    nodes: List[str]
    connections: Dict[str, Any]
    use_cases: List[str]
    complexity: str
    category: str

@dataclass
class NodeAnalysis:
    """Analysis results for a specific node type"""
    node_type: str
    frequency: int
    common_connections: List[str]
    typical_settings: Dict[str, Any]
    use_cases: List[str]

class N8nWorkflowResearcher:
    """Advanced research and analysis for n8n workflows"""
    
    def __init__(self):
        self.workflow_patterns = []
        self.node_statistics = defaultdict(int)
        self.connection_patterns = defaultdict(int)
        self.service_combinations = defaultdict(int)
        self.load_training_data()
    
    def load_training_data(self):
        """Load training data and patterns"""
        try:
            # Load workflow patterns
            with open('training_data/workflow_patterns.json', 'r') as f:
                patterns_data = json.load(f)
                # Handle both list and dict formats
                if isinstance(patterns_data, list):
                    patterns_list = patterns_data
                else:
                    patterns_list = patterns_data.get('patterns', [])
                
                for pattern_data in patterns_list:
                    pattern = WorkflowPattern(
                        name=pattern_data.get('name', ''),
                        description=pattern_data.get('description', ''),
                        nodes=pattern_data.get('nodes', pattern_data.get('trigger_pattern', []) + pattern_data.get('processing_pattern', [])),
                        connections=pattern_data.get('connections', {}),
                        use_cases=pattern_data.get('use_cases', [pattern_data.get('description', '')]),
                        complexity=pattern_data.get('complexity', 'medium'),
                        category=pattern_data.get('category', 'general')
                    )
                    self.workflow_patterns.append(pattern)
            
            # Load node statistics
            with open('training_data/statistics.json', 'r') as f:
                stats_data = json.load(f)
                self.node_statistics.update(stats_data.get('node_usage', {}))
                self.connection_patterns.update(stats_data.get('connection_patterns', {}))
                self.service_combinations.update(stats_data.get('service_combinations', {}))
                
            logger.info(f"Loaded {len(self.workflow_patterns)} workflow patterns")
            
        except FileNotFoundError as e:
            logger.warning(f"Training data not found: {e}")
        except Exception as e:
            logger.error(f"Error loading training data: {e}")
    
    def analyze_description(self, description: str) -> Dict[str, Any]:
        """Analyze workflow description to extract key information"""
        analysis = {
            'triggers': [],
            'actions': [],
            'services': [],
            'data_types': [],
            'complexity_indicators': [],
            'suggested_nodes': [],
            'confidence_score': 0.0
        }
        
        description_lower = description.lower()
        
        # Detect triggers
        trigger_patterns = {
            'webhook': r'\b(webhook|http|api|rest|post|get)\b',
            'schedule': r'\b(schedule|cron|daily|weekly|monthly|timer|interval)\b',
            'manual': r'\b(manual|button|click|start|trigger)\b',
            'email': r'\b(email|mail|imap|smtp)\b',
            'file': r'\b(file|csv|json|xml|upload|download)\b'
        }
        
        for trigger_type, pattern in trigger_patterns.items():
            if re.search(pattern, description_lower):
                analysis['triggers'].append(trigger_type)
        
        # Detect actions
        action_patterns = {
            'send': r'\b(send|post|submit|deliver|dispatch)\b',
            'create': r'\b(create|add|insert|new|generate)\b',
            'update': r'\b(update|modify|change|edit|alter)\b',
            'delete': r'\b(delete|remove|clear|clean)\b',
            'process': r'\b(process|transform|convert|parse|analyze)\b',
            'notify': r'\b(notify|alert|message|notification)\b',
            'store': r'\b(store|save|backup|archive|database)\b',
            'sync': r'\b(sync|synchronize|replicate|mirror)\b'
        }
        
        for action_type, pattern in action_patterns.items():
            if re.search(pattern, description_lower):
                analysis['actions'].append(action_type)
        
        # Detect services
        service_patterns = {
            'slack': r'\b(slack)\b',
            'discord': r'\b(discord)\b',
            'email': r'\b(email|gmail|outlook|smtp)\b',
            'google_sheets': r'\b(google sheets|spreadsheet|gsheet)\b',
            'airtable': r'\b(airtable)\b',
            'notion': r'\b(notion)\b',
            'trello': r'\b(trello)\b',
            'github': r'\b(github|git)\b',
            'dropbox': r'\b(dropbox)\b',
            'salesforce': r'\b(salesforce|crm)\b',
            'stripe': r'\b(stripe|payment)\b',
            'twitter': r'\b(twitter|tweet)\b',
            'facebook': r'\b(facebook|fb)\b',
            'linkedin': r'\b(linkedin)\b',
            'instagram': r'\b(instagram|insta)\b',
            'youtube': r'\b(youtube|video)\b',
            'database': r'\b(database|mysql|postgres|mongodb)\b',
            'api': r'\b(api|rest|graphql|endpoint)\b'
        }
        
        for service_name, pattern in service_patterns.items():
            if re.search(pattern, description_lower):
                analysis['services'].append(service_name)
        
        # Detect data types
        data_type_patterns = {
            'json': r'\b(json|api|rest)\b',
            'csv': r'\b(csv|spreadsheet|excel)\b',
            'xml': r'\b(xml|soap)\b',
            'text': r'\b(text|string|message)\b',
            'image': r'\b(image|photo|picture|jpg|png)\b',
            'file': r'\b(file|document|pdf|attachment)\b'
        }
        
        for data_type, pattern in data_type_patterns.items():
            if re.search(pattern, description_lower):
                analysis['data_types'].append(data_type)
        
        # Assess complexity
        complexity_indicators = []
        if len(analysis['services']) > 3:
            complexity_indicators.append('multiple_services')
        if re.search(r'\b(condition|if|when|filter|transform)\b', description_lower):
            complexity_indicators.append('conditional_logic')
        if re.search(r'\b(loop|iterate|each|multiple|batch)\b', description_lower):
            complexity_indicators.append('iteration')
        if re.search(r'\b(error|retry|fallback|backup)\b', description_lower):
            complexity_indicators.append('error_handling')
        
        analysis['complexity_indicators'] = complexity_indicators
        
        # Suggest nodes based on analysis
        suggested_nodes = self._suggest_nodes(analysis)
        analysis['suggested_nodes'] = suggested_nodes
        
        # Calculate confidence score
        confidence_score = self._calculate_confidence(analysis, description)
        analysis['confidence_score'] = confidence_score
        
        return analysis
    
    def _suggest_nodes(self, analysis: Dict[str, Any]) -> List[str]:
        """Suggest appropriate nodes based on analysis"""
        suggested_nodes = []
        
        # Add trigger nodes
        if 'webhook' in analysis['triggers']:
            suggested_nodes.append('Webhook')
        if 'schedule' in analysis['triggers']:
            suggested_nodes.append('Cron')
        if 'manual' in analysis['triggers']:
            suggested_nodes.append('Manual Trigger')
        if 'email' in analysis['triggers']:
            suggested_nodes.append('Email Trigger (IMAP)')
        
        # Add service nodes
        service_node_mapping = {
            'slack': 'Slack',
            'discord': 'Discord',
            'email': 'Send Email',
            'google_sheets': 'Google Sheets',
            'airtable': 'Airtable',
            'notion': 'Notion',
            'trello': 'Trello',
            'github': 'GitHub',
            'dropbox': 'Dropbox',
            'salesforce': 'Salesforce',
            'stripe': 'Stripe',
            'twitter': 'Twitter',
            'facebook': 'Facebook',
            'linkedin': 'LinkedIn',
            'database': 'MySQL',
            'api': 'HTTP Request'
        }
        
        for service in analysis['services']:
            if service in service_node_mapping:
                suggested_nodes.append(service_node_mapping[service])
        
        # Add processing nodes based on actions
        if 'process' in analysis['actions'] or 'json' in analysis['data_types']:
            suggested_nodes.append('Set')
        if 'condition' in analysis['complexity_indicators']:
            suggested_nodes.append('IF')
        if 'iteration' in analysis['complexity_indicators']:
            suggested_nodes.append('Split In Batches')
        
        # Add utility nodes
        if len(analysis['services']) > 1:
            suggested_nodes.append('Merge')
        if 'error_handling' in analysis['complexity_indicators']:
            suggested_nodes.append('Error Trigger')
        
        return list(set(suggested_nodes))  # Remove duplicates
    
    def _calculate_confidence(self, analysis: Dict[str, Any], description: str) -> float:
        """Calculate confidence score for the analysis"""
        confidence = 0.0
        
        # Base confidence from detected elements
        if analysis['triggers']:
            confidence += 0.3
        if analysis['actions']:
            confidence += 0.3
        if analysis['services']:
            confidence += 0.2
        
        # Bonus for specific details
        if len(analysis['services']) >= 2:
            confidence += 0.1
        if analysis['data_types']:
            confidence += 0.1
        
        # Description quality bonus
        word_count = len(description.split())
        if word_count >= 10:
            confidence += 0.1
        if word_count >= 20:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def find_similar_patterns(self, analysis: Dict[str, Any], limit: int = 3) -> List[WorkflowPattern]:
        """Find similar workflow patterns based on analysis"""
        similar_patterns = []
        
        for pattern in self.workflow_patterns:
            similarity_score = self._calculate_pattern_similarity(analysis, pattern)
            if similarity_score > 0.3:  # Minimum similarity threshold
                similar_patterns.append((pattern, similarity_score))
        
        # Sort by similarity score and return top matches
        similar_patterns.sort(key=lambda x: x[1], reverse=True)
        return [pattern for pattern, score in similar_patterns[:limit]]
    
    def _calculate_pattern_similarity(self, analysis: Dict[str, Any], pattern: WorkflowPattern) -> float:
        """Calculate similarity between analysis and pattern"""
        similarity = 0.0
        
        # Check service overlap
        analysis_services = set(analysis['services'])
        pattern_services = set()
        for node in pattern.nodes:
            # Extract service names from node names
            node_lower = node.lower()
            for service in analysis_services:
                if service in node_lower:
                    pattern_services.add(service)
        
        if analysis_services and pattern_services:
            service_overlap = len(analysis_services.intersection(pattern_services))
            service_similarity = service_overlap / len(analysis_services.union(pattern_services))
            similarity += service_similarity * 0.5
        
        # Check action overlap
        analysis_actions = set(analysis['actions'])
        pattern_actions = set()
        for use_case in pattern.use_cases:
            use_case_lower = use_case.lower()
            for action in analysis_actions:
                if action in use_case_lower:
                    pattern_actions.add(action)
        
        if analysis_actions and pattern_actions:
            action_overlap = len(analysis_actions.intersection(pattern_actions))
            action_similarity = action_overlap / len(analysis_actions.union(pattern_actions))
            similarity += action_similarity * 0.3
        
        # Check complexity match
        complexity_indicators = analysis.get('complexity_indicators', [])
        if pattern.complexity == 'simple' and len(complexity_indicators) <= 1:
            similarity += 0.2
        elif pattern.complexity == 'medium' and 1 < len(complexity_indicators) <= 3:
            similarity += 0.2
        elif pattern.complexity == 'complex' and len(complexity_indicators) > 3:
            similarity += 0.2
        
        return similarity
    
    def get_node_recommendations(self, current_nodes: List[str], analysis: Dict[str, Any]) -> List[str]:
        """Get recommendations for additional nodes"""
        recommendations = []
        current_node_types = set(current_nodes)
        
        # Check for missing essential nodes
        if not any('trigger' in node.lower() or 'webhook' in node.lower() or 'cron' in node.lower() 
                  for node in current_nodes):
            if analysis['triggers']:
                recommendations.extend(self._suggest_trigger_nodes(analysis['triggers']))
        
        # Check for missing processing nodes
        if analysis['actions'] and not any('set' in node.lower() or 'function' in node.lower() 
                                          for node in current_nodes):
            recommendations.append('Set')
        
        # Check for missing conditional logic
        if 'conditional_logic' in analysis.get('complexity_indicators', []) and \
           not any('if' in node.lower() for node in current_nodes):
            recommendations.append('IF')
        
        # Check for missing error handling
        if 'error_handling' in analysis.get('complexity_indicators', []) and \
           not any('error' in node.lower() for node in current_nodes):
            recommendations.append('Error Trigger')
        
        return [rec for rec in recommendations if rec not in current_node_types]
    
    def _suggest_trigger_nodes(self, triggers: List[str]) -> List[str]:
        """Suggest appropriate trigger nodes"""
        trigger_mapping = {
            'webhook': 'Webhook',
            'schedule': 'Cron',
            'manual': 'Manual Trigger',
            'email': 'Email Trigger (IMAP)',
            'file': 'Watch File'
        }
        
        return [trigger_mapping.get(trigger, 'Webhook') for trigger in triggers]
    
    def validate_workflow_structure(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Validate workflow structure and suggest improvements"""
        validation_result = {
            'is_valid': True,
            'warnings': [],
            'suggestions': [],
            'score': 100
        }
        
        nodes = workflow.get('nodes', [])
        connections = workflow.get('connections', {})
        
        # Check for trigger node
        has_trigger = any(
            node.get('type', '').endswith('Trigger') or 
            node.get('type') in ['Webhook', 'Cron', 'Manual Trigger']
            for node in nodes
        )
        
        if not has_trigger:
            validation_result['warnings'].append('No trigger node found')
            validation_result['suggestions'].append('Add a trigger node to start the workflow')
            validation_result['score'] -= 20
        
        # Check for disconnected nodes
        connected_nodes = set()
        for source_node, connections_data in connections.items():
            connected_nodes.add(source_node)
            for connection_type, connection_list in connections_data.items():
                for connection in connection_list:
                    for target in connection:
                        connected_nodes.add(target.get('node', ''))
        
        all_node_names = {node.get('name', '') for node in nodes}
        disconnected_nodes = all_node_names - connected_nodes
        
        if disconnected_nodes:
            validation_result['warnings'].append(f'Disconnected nodes found: {list(disconnected_nodes)}')
            validation_result['suggestions'].append('Connect all nodes to ensure proper workflow execution')
            validation_result['score'] -= 10 * len(disconnected_nodes)
        
        # Check for error handling
        has_error_handling = any(
            'error' in node.get('type', '').lower() or 
            'try' in node.get('type', '').lower()
            for node in nodes
        )
        
        if len(nodes) > 3 and not has_error_handling:
            validation_result['suggestions'].append('Consider adding error handling for robust workflow execution')
            validation_result['score'] -= 5
        
        # Ensure score doesn't go below 0
        validation_result['score'] = max(0, validation_result['score'])
        
        if validation_result['score'] < 70:
            validation_result['is_valid'] = False
        
        return validation_result
    
    def get_workflow_statistics(self) -> Dict[str, Any]:
        """Get statistics about workflow patterns and usage"""
        return {
            'total_patterns': len(self.workflow_patterns),
            'node_statistics': dict(self.node_statistics),
            'connection_patterns': dict(self.connection_patterns),
            'service_combinations': dict(self.service_combinations),
            'categories': list(set(pattern.category for pattern in self.workflow_patterns)),
            'complexity_distribution': {
                'simple': len([p for p in self.workflow_patterns if p.complexity == 'simple']),
                'medium': len([p for p in self.workflow_patterns if p.complexity == 'medium']),
                'complex': len([p for p in self.workflow_patterns if p.complexity == 'complex'])
            }
        }

# Example usage and testing
if __name__ == "__main__":
    researcher = N8nWorkflowResearcher()
    
    # Test analysis
    test_description = "Send daily reports from Google Sheets to Slack and email"
    analysis = researcher.analyze_description(test_description)
    print(f"Analysis: {json.dumps(analysis, indent=2)}")
    
    # Test pattern matching
    similar_patterns = researcher.find_similar_patterns(analysis)
    print(f"Found {len(similar_patterns)} similar patterns")
    
    # Test statistics
    stats = researcher.get_workflow_statistics()
    print(f"Statistics: {json.dumps(stats, indent=2)}")