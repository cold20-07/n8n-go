#!/usr/bin/env python3
"""
N8N Workflow Analyzer and Training Data Generator
Processes n8n JSON workflows to extract features and create training datasets
"""

import json
import os
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Tuple
from collections import Counter, defaultdict
import re

class N8NWorkflowAnalyzer:
    def __init__(self, workflows_dir: str):
        self.workflows_dir = Path(workflows_dir)
        self.workflows = []
        self.analysis_results = {}
        
    def load_workflows(self) -> List[Dict]:
        """Load all workflow files from the directory (both .json and .txt files)"""
        workflows = []
        workflow_files = list(self.workflows_dir.glob("*.json")) + list(self.workflows_dir.glob("*.txt"))
        
        print(f"Found {len(workflow_files)} workflow files (.json and .txt)")
        
        for workflow_file in workflow_files:
            try:
                with open(workflow_file, 'r', encoding='utf-8') as f:
                    workflow_data = json.load(f)
                    workflow_data['filename'] = workflow_file.name
                    workflows.append(workflow_data)
                    print(f"✓ Loaded: {workflow_file.name}")
            except Exception as e:
                print(f"✗ Error loading {workflow_file.name}: {e}")
                
        self.workflows = workflows
        return workflows
    
    def extract_workflow_features(self, workflow: Dict) -> Dict:
        """Extract key features from a single workflow"""
        features = {
            'filename': workflow.get('filename', ''),
            'workflow_name': workflow.get('name', ''),
            'workflow_id': workflow.get('id', ''),
            'node_count': 0,
            'node_types': [],
            'node_type_counts': {},
            'has_ai_nodes': False,
            'ai_node_types': [],
            'trigger_types': [],
            'integration_services': [],
            'workflow_complexity': 0,
            'has_langchain': False,
            'has_openai': False,
            'has_google_services': False,
            'has_slack': False,
            'has_webhook': False,
            'has_schedule': False,
            'workflow_tags': workflow.get('tags', []),
            'connections_count': 0,
            'sticky_notes_count': 0,
            'error_handling_nodes': 0
        }
        
        nodes = workflow.get('nodes', [])
        features['node_count'] = len(nodes)
        
        # Analyze nodes
        for node in nodes:
            node_type = node.get('type', '')
            features['node_types'].append(node_type)
            
            # Count node types
            features['node_type_counts'][node_type] = features['node_type_counts'].get(node_type, 0) + 1
            
            # Check for AI-related nodes
            if any(ai_keyword in node_type.lower() for ai_keyword in ['openai', 'langchain', 'ai', 'gpt', 'claude', 'gemini']):
                features['has_ai_nodes'] = True
                features['ai_node_types'].append(node_type)
            
            # Check for specific services
            if 'langchain' in node_type.lower():
                features['has_langchain'] = True
            if 'openai' in node_type.lower():
                features['has_openai'] = True
            if 'google' in node_type.lower():
                features['has_google_services'] = True
            if 'slack' in node_type.lower():
                features['has_slack'] = True
            if 'webhook' in node_type.lower():
                features['has_webhook'] = True
            if 'schedule' in node_type.lower():
                features['has_schedule'] = True
            
            # Check for triggers
            if 'trigger' in node_type.lower():
                features['trigger_types'].append(node_type)
            
            # Check for sticky notes (documentation)
            if node_type == 'n8n-nodes-base.stickyNote':
                features['sticky_notes_count'] += 1
            
            # Check for error handling
            if node.get('onError') == 'continueRegularOutput':
                features['error_handling_nodes'] += 1
            
            # Extract service integrations
            if 'n8n-nodes-base.' in node_type:
                service = node_type.replace('n8n-nodes-base.', '')
                features['integration_services'].append(service)
        
        # Calculate workflow complexity (simple heuristic)
        features['workflow_complexity'] = (
            features['node_count'] * 1 +
            len(set(features['node_types'])) * 2 +
            features['connections_count'] * 0.5
        )
        
        # Count connections
        connections = workflow.get('connections', {})
        features['connections_count'] = sum(len(conn) for conn in connections.values())
        
        return features
    
    def analyze_all_workflows(self) -> pd.DataFrame:
        """Analyze all workflows and return a DataFrame with features"""
        if not self.workflows:
            self.load_workflows()
        
        features_list = []
        for workflow in self.workflows:
            features = self.extract_workflow_features(workflow)
            features_list.append(features)
        
        df = pd.DataFrame(features_list)
        return df
    
    def generate_training_data(self) -> Dict[str, Any]:
        """Generate comprehensive training data from workflows"""
        training_data = {
            'workflow_patterns': [],
            'node_sequences': [],
            'ai_integration_patterns': [],
            'service_combinations': [],
            'workflow_templates': []
        }
        
        for workflow in self.workflows:
            # Extract workflow patterns
            pattern = self.extract_workflow_pattern(workflow)
            training_data['workflow_patterns'].append(pattern)
            
            # Extract node sequences
            sequence = self.extract_node_sequence(workflow)
            training_data['node_sequences'].append(sequence)
            
            # Extract AI integration patterns
            ai_pattern = self.extract_ai_integration_pattern(workflow)
            if ai_pattern:
                training_data['ai_integration_patterns'].append(ai_pattern)
            
            # Extract service combinations
            services = self.extract_service_combinations(workflow)
            training_data['service_combinations'].append(services)
            
            # Create workflow template
            template = self.create_workflow_template(workflow)
            training_data['workflow_templates'].append(template)
        
        return training_data
    
    def extract_workflow_pattern(self, workflow: Dict) -> Dict:
        """Extract high-level workflow pattern"""
        nodes = workflow.get('nodes', [])
        
        pattern = {
            'name': workflow.get('name', ''),
            'category': self.categorize_workflow(workflow),
            'trigger_pattern': [],
            'processing_pattern': [],
            'output_pattern': [],
            'ai_usage': False
        }
        
        for node in nodes:
            node_type = node.get('type', '')
            
            if 'trigger' in node_type.lower():
                pattern['trigger_pattern'].append(node_type)
            elif any(ai_term in node_type.lower() for ai_term in ['openai', 'langchain', 'ai', 'gpt']):
                pattern['processing_pattern'].append(node_type)
                pattern['ai_usage'] = True
            elif any(output_term in node_type.lower() for output_term in ['slack', 'email', 'webhook', 'sheets']):
                pattern['output_pattern'].append(node_type)
            else:
                pattern['processing_pattern'].append(node_type)
        
        return pattern
    
    def extract_node_sequence(self, workflow: Dict) -> List[str]:
        """Extract the sequence of node types in the workflow"""
        nodes = workflow.get('nodes', [])
        return [node.get('type', '') for node in nodes if node.get('type') != 'n8n-nodes-base.stickyNote']
    
    def extract_ai_integration_pattern(self, workflow: Dict) -> Dict:
        """Extract AI-specific integration patterns"""
        nodes = workflow.get('nodes', [])
        ai_nodes = [node for node in nodes if any(ai_term in node.get('type', '').lower() 
                                                 for ai_term in ['openai', 'langchain', 'ai', 'gpt', 'claude', 'gemini'])]
        
        if not ai_nodes:
            return None
        
        pattern = {
            'workflow_name': workflow.get('name', ''),
            'ai_nodes': [node.get('type', '') for node in ai_nodes],
            'ai_parameters': [],
            'input_sources': [],
            'output_destinations': []
        }
        
        # Extract AI node parameters
        for node in ai_nodes:
            params = node.get('parameters', {})
            if params:
                pattern['ai_parameters'].append({
                    'node_type': node.get('type', ''),
                    'parameters': list(params.keys())
                })
        
        return pattern
    
    def extract_service_combinations(self, workflow: Dict) -> List[str]:
        """Extract unique service combinations used in workflow"""
        nodes = workflow.get('nodes', [])
        services = set()
        
        for node in nodes:
            node_type = node.get('type', '')
            if 'n8n-nodes-base.' in node_type:
                service = node_type.replace('n8n-nodes-base.', '')
                services.add(service)
            elif '@n8n/n8n-nodes-langchain.' in node_type:
                service = node_type.replace('@n8n/n8n-nodes-langchain.', 'langchain_')
                services.add(service)
        
        return list(services)
    
    def create_workflow_template(self, workflow: Dict) -> Dict:
        """Create a simplified template from workflow"""
        template = {
            'name': workflow.get('name', ''),
            'description': self.generate_workflow_description(workflow),
            'nodes': [],
            'connections': workflow.get('connections', {}),
            'tags': workflow.get('tags', [])
        }
        
        nodes = workflow.get('nodes', [])
        for node in nodes:
            if node.get('type') != 'n8n-nodes-base.stickyNote':  # Skip documentation nodes
                template_node = {
                    'type': node.get('type', ''),
                    'name': node.get('name', ''),
                    'parameters': list(node.get('parameters', {}).keys())
                }
                template['nodes'].append(template_node)
        
        return template
    
    def categorize_workflow(self, workflow: Dict) -> str:
        """Categorize workflow based on its purpose"""
        name = workflow.get('name', '').lower()
        nodes = workflow.get('nodes', [])
        node_types = [node.get('type', '').lower() for node in nodes]
        
        # AI/ML workflows
        if any('ai' in name or 'gpt' in name or 'openai' in name for name in [name]):
            return 'AI/ML'
        
        # Data processing
        if any('data' in name or 'extract' in name or 'process' in name for name in [name]):
            return 'Data Processing'
        
        # Communication/Notifications
        if any(comm in ' '.join(node_types) for comm in ['slack', 'email', 'telegram', 'discord']):
            return 'Communication'
        
        # Content Management
        if any(cms in ' '.join(node_types) for cms in ['wordpress', 'blog', 'content']):
            return 'Content Management'
        
        # Monitoring/Analytics
        if any(monitor in name for monitor in ['monitor', 'track', 'analyze', 'report']):
            return 'Monitoring'
        
        return 'General Automation'
    
    def generate_workflow_description(self, workflow: Dict) -> str:
        """Generate a description of what the workflow does"""
        name = workflow.get('name', '')
        nodes = workflow.get('nodes', [])
        
        # Count different types of nodes
        triggers = [n for n in nodes if 'trigger' in n.get('type', '').lower()]
        ai_nodes = [n for n in nodes if any(ai in n.get('type', '').lower() 
                                           for ai in ['openai', 'langchain', 'ai', 'gpt'])]
        output_nodes = [n for n in nodes if any(out in n.get('type', '').lower() 
                                               for out in ['slack', 'email', 'sheets', 'webhook'])]
        
        description_parts = []
        
        if triggers:
            trigger_types = [t.get('type', '') for t in triggers]
            if 'scheduleTrigger' in str(trigger_types):
                description_parts.append("Scheduled automation")
            elif 'webhook' in str(trigger_types).lower():
                description_parts.append("Webhook-triggered automation")
            else:
                description_parts.append("Event-driven automation")
        
        if ai_nodes:
            description_parts.append("with AI processing")
        
        if output_nodes:
            output_services = [n.get('type', '').split('.')[-1] for n in output_nodes]
            description_parts.append(f"outputting to {', '.join(set(output_services))}")
        
        return f"{name}: {' '.join(description_parts)}"
    
    def generate_statistics(self) -> Dict:
        """Generate comprehensive statistics about the workflow collection"""
        if not self.workflows:
            self.load_workflows()
        
        df = self.analyze_all_workflows()
        
        stats = {
            'total_workflows': len(self.workflows),
            'node_statistics': {
                'total_nodes': df['node_count'].sum(),
                'avg_nodes_per_workflow': df['node_count'].mean(),
                'max_nodes': df['node_count'].max(),
                'min_nodes': df['node_count'].min()
            },
            'ai_usage': {
                'workflows_with_ai': df['has_ai_nodes'].sum(),
                'ai_adoption_rate': df['has_ai_nodes'].mean() * 100,
                'openai_usage': df['has_openai'].sum(),
                'langchain_usage': df['has_langchain'].sum()
            },
            'service_usage': {
                'google_services': df['has_google_services'].sum(),
                'slack_integration': df['has_slack'].sum(),
                'webhook_usage': df['has_webhook'].sum(),
                'scheduled_workflows': df['has_schedule'].sum()
            },
            'complexity_distribution': {
                'simple_workflows': (df['workflow_complexity'] < 20).sum(),
                'medium_workflows': ((df['workflow_complexity'] >= 20) & (df['workflow_complexity'] < 50)).sum(),
                'complex_workflows': (df['workflow_complexity'] >= 50).sum()
            }
        }
        
        # Most common node types
        all_node_types = []
        for workflow in self.workflows:
            nodes = workflow.get('nodes', [])
            all_node_types.extend([node.get('type', '') for node in nodes])
        
        stats['most_common_nodes'] = dict(Counter(all_node_types).most_common(10))
        
        # Workflow categories
        categories = [self.categorize_workflow(w) for w in self.workflows]
        stats['workflow_categories'] = dict(Counter(categories))
        
        return stats
    
    def save_training_data(self, output_dir: str = "training_data"):
        """Save all training data to files"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Generate and save feature DataFrame
        df = self.analyze_all_workflows()
        df.to_csv(output_path / "workflow_features.csv", index=False)
        
        # Generate and save training data
        training_data = self.generate_training_data()
        
        for data_type, data in training_data.items():
            with open(output_path / f"{data_type}.json", 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        # Save statistics (convert numpy types to native Python types)
        stats = self.generate_statistics()
        stats_json = json.loads(json.dumps(stats, default=str))
        with open(output_path / "statistics.json", 'w', encoding='utf-8') as f:
            json.dump(stats_json, f, indent=2, ensure_ascii=False)
        
        print(f"Training data saved to {output_path}")
        return output_path

def main():
    # Initialize analyzer
    analyzer = N8NWorkflowAnalyzer("drive-download-20251004T130930Z-1-001")
    
    # Load workflows
    workflows = analyzer.load_workflows()
    print(f"\nLoaded {len(workflows)} workflows successfully!")
    
    # Generate statistics
    print("\nGenerating statistics...")
    stats = analyzer.generate_statistics()
    
    print(f"\n📊 WORKFLOW COLLECTION STATISTICS")
    print(f"{'='*50}")
    print(f"Total Workflows: {stats['total_workflows']}")
    print(f"Total Nodes: {stats['node_statistics']['total_nodes']}")
    print(f"Average Nodes per Workflow: {stats['node_statistics']['avg_nodes_per_workflow']:.1f}")
    print(f"AI Adoption Rate: {stats['ai_usage']['ai_adoption_rate']:.1f}%")
    
    print(f"\n🤖 AI USAGE")
    print(f"Workflows with AI: {stats['ai_usage']['workflows_with_ai']}")
    print(f"OpenAI Usage: {stats['ai_usage']['openai_usage']}")
    print(f"LangChain Usage: {stats['ai_usage']['langchain_usage']}")
    
    print(f"\n🔗 SERVICE INTEGRATIONS")
    for service, count in stats['service_usage'].items():
        print(f"{service.replace('_', ' ').title()}: {count}")
    
    print(f"\n📈 WORKFLOW CATEGORIES")
    for category, count in stats['workflow_categories'].items():
        print(f"{category}: {count}")
    
    print(f"\n🏗️ MOST COMMON NODE TYPES")
    for node_type, count in list(stats['most_common_nodes'].items())[:5]:
        print(f"{node_type}: {count}")
    
    # Save training data
    print(f"\n💾 Saving training data...")
    output_path = analyzer.save_training_data()
    
    print(f"\n✅ Analysis complete! Training data saved to: {output_path}")
    print(f"\nFiles created:")
    for file in output_path.glob("*"):
        print(f"  - {file.name}")

if __name__ == "__main__":
    main()