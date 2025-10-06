#!/usr/bin/env python3
"""
Trained Workflow Generator
Uses the actual trained models and patterns from the 100 n8n JSON workflows
"""

import json
import random
import pickle
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Optional

class TrainedWorkflowGenerator:
    def __init__(self):
        self.load_trained_data()
        self.load_models()
    
    def load_trained_data(self):
        """Load the actual workflow patterns from training data"""
        try:
            # Load workflow templates from training
            with open("training_data/workflow_templates.json", 'r') as f:
                self.workflow_templates = json.load(f)
            
            # Load workflow patterns
            with open("training_data/workflow_patterns.json", 'r') as f:
                self.workflow_patterns = json.load(f)
            
            # Load AI integration patterns
            with open("training_data/ai_integration_patterns.json", 'r') as f:
                self.ai_patterns = [p for p in json.load(f) if p is not None]
            
            # Load node sequences
            with open("training_data/node_sequences.json", 'r') as f:
                self.node_sequences = json.load(f)
            
            # Load statistics for realistic parameters
            with open("training_data/statistics.json", 'r') as f:
                self.statistics = json.load(f)
            
            print("[OK] Loaded trained workflow data successfully")
            
        except Exception as e:
            print(f"⚠️ Could not load trained data: {e}")
            self.workflow_templates = []
            self.workflow_patterns = []
            self.ai_patterns = []
            self.node_sequences = []
            self.statistics = {}
    
    def load_models(self):
        """Load trained models if available"""
        self.models = {}
        self.scalers = {}
        
        try:
            model_dir = Path("final_models")
            if model_dir.exists():
                # Load classifier
                with open(model_dir / "robust_classifier.pkl", 'rb') as f:
                    self.models['classifier'] = pickle.load(f)
                
                with open(model_dir / "robust_classifier_scaler.pkl", 'rb') as f:
                    self.scalers['classifier'] = pickle.load(f)
                
                print("[OK] Loaded trained models successfully")
            else:
                print("[WARN] No trained models found")
                
        except Exception as e:
            print(f"⚠️ Could not load trained models: {e}")
    
    def classify_workflow_type(self, description: str) -> str:
        """Use trained classifier to determine workflow type"""
        if 'classifier' not in self.models:
            return self.classify_by_keywords(description)
        
        try:
            # Create feature vector (simplified for classification)
            features = self.extract_features_from_description(description)
            features_scaled = self.scalers['classifier'].transform([features])
            
            prediction = self.models['classifier'].predict(features_scaled)
            return prediction[0]
            
        except Exception as e:
            print(f"⚠️ Classification failed: {e}")
            return self.classify_by_keywords(description)
    
    def classify_by_keywords(self, description: str) -> str:
        """Fallback classification using keywords"""
        desc_lower = description.lower()
        
        # Keywords from actual training data
        if any(word in desc_lower for word in ['ai', 'openai', 'gpt', 'langchain', 'claude', 'gemini']):
            return 'AI/ML'
        elif any(word in desc_lower for word in ['slack', 'email', 'telegram', 'discord', 'notification']):
            return 'Communication'
        elif any(word in desc_lower for word in ['wordpress', 'blog', 'content', 'cms', 'post']):
            return 'Content Management'
        elif any(word in desc_lower for word in ['data', 'csv', 'excel', 'database', 'process']):
            return 'Data Processing'
        else:
            return 'General Automation'
    
    def extract_features_from_description(self, description: str) -> List[float]:
        """Extract features from description for classification"""
        desc_lower = description.lower()
        
        # Basic features based on training data
        features = [
            len(description.split()),  # word count
            5,  # estimated unique_node_types
            3,  # estimated connections
            1 if any(ai in desc_lower for ai in ['ai', 'openai', 'gpt']) else 0,  # ai_node_count
            0.2 if 'ai' in desc_lower else 0,  # ai_node_ratio
            1 if 'openai' in desc_lower else 0,  # has_openai
            1 if 'langchain' in desc_lower else 0,  # has_langchain
            1 if 'google' in desc_lower else 0,  # has_google
            1 if 'slack' in desc_lower else 0,  # has_slack
            1 if 'webhook' in desc_lower else 0,  # has_webhook
            1 if any(sched in desc_lower for sched in ['schedule', 'daily', 'weekly']) else 0,  # has_schedule
            0.1,  # branching_complexity
            0.2,  # documentation_ratio
            0.05,  # error_handling_ratio
            1,  # trigger_count
            1,  # output_count
            len(description.split()) * 2  # complexity_score
        ]
        
        return features
    
    def find_similar_templates(self, workflow_type: str, description: str, limit: int = 5) -> List[Dict]:
        """Find similar workflow templates from training data"""
        # Filter templates by type
        matching_templates = []
        
        for i, pattern in enumerate(self.workflow_patterns):
            if pattern.get('category') == workflow_type and i < len(self.workflow_templates):
                template = self.workflow_templates[i]
                similarity_score = self.calculate_similarity(description, template)
                
                matching_templates.append({
                    'template': template,
                    'pattern': pattern,
                    'similarity': similarity_score
                })
        
        # Sort by similarity and return top matches
        matching_templates.sort(key=lambda x: x['similarity'], reverse=True)
        return matching_templates[:limit]
    
    def calculate_similarity(self, description: str, template: Dict) -> float:
        """Calculate similarity between description and template"""
        desc_words = set(description.lower().split())
        template_name = template.get('name', '').lower()
        template_desc = template.get('description', '').lower()
        
        # Combine template text
        template_text = f"{template_name} {template_desc}"
        template_words = set(template_text.split())
        
        # Calculate word overlap
        if not template_words:
            return 0.0
        
        overlap = len(desc_words.intersection(template_words))
        return overlap / len(template_words.union(desc_words))
    
    def generate_realistic_workflow(self, description: str, trigger_type: str = 'webhook', 
                                  complexity: str = 'medium') -> Dict:
        """Generate a realistic workflow based on trained patterns"""
        
        # Step 1: Classify the workflow type
        workflow_type = self.classify_workflow_type(description)
        print(f"🎯 Classified as: {workflow_type}")
        
        # Step 2: Find similar templates from training data
        similar_templates = self.find_similar_templates(workflow_type, description)
        
        if not similar_templates:
            print("⚠️ No similar templates found, using fallback")
            return self.create_fallback_workflow(description, trigger_type, complexity)
        
        # Step 3: Use the best matching template as base
        best_match = similar_templates[0]
        base_template = best_match['template']
        
        print(f"📋 Using template: {base_template.get('name', 'Unknown')}")
        print(f"🎯 Similarity score: {best_match['similarity']:.2f}")
        
        # Step 4: Create workflow based on template
        workflow = self.create_workflow_from_template(
            base_template, description, trigger_type, complexity
        )
        
        return workflow
    
    def create_workflow_from_template(self, template: Dict, description: str, 
                                    trigger_type: str, complexity: str) -> Dict:
        """Create a workflow based on a real template from training data"""
        
        # Start with basic n8n workflow structure
        workflow_id = f"workflow_{random.randint(100000, 999999)}"
        
        workflow = {
            "id": workflow_id,
            "name": self.generate_workflow_name(description),
            "nodes": [],
            "connections": {},
            "active": True,
            "settings": {},
            "staticData": None,
            "tags": [],
            "triggerCount": 0,
            "updatedAt": "2025-01-01T00:00:00.000Z",
            "versionId": "1"
        }
        
        # Generate nodes based on template pattern
        nodes = self.generate_nodes_from_template(template, trigger_type, description)
        workflow["nodes"] = nodes
        
        # Generate connections between nodes
        connections = self.generate_connections(nodes)
        workflow["connections"] = connections
        
        return workflow
    
    def generate_workflow_name(self, description: str) -> str:
        """Generate a realistic workflow name"""
        # Extract key words from description
        words = description.split()
        key_words = [w for w in words if len(w) > 3 and w.lower() not in 
                    ['the', 'and', 'with', 'from', 'that', 'this', 'will', 'can']]
        
        if len(key_words) >= 2:
            return f"{key_words[0].title()} {key_words[1].title()} Automation"
        elif len(key_words) == 1:
            return f"{key_words[0].title()} Workflow"
        else:
            return "Custom Automation Workflow"
    
    def generate_nodes_from_template(self, template: Dict, trigger_type: str, description: str) -> List[Dict]:
        """Generate nodes based on template patterns"""
        nodes = []
        
        # Get template nodes as reference
        template_nodes = template.get('nodes', [])
        
        if not template_nodes:
            return self.generate_basic_nodes(trigger_type, description)
        
        # Start with trigger node
        trigger_node = self.create_trigger_node(trigger_type)
        nodes.append(trigger_node)
        
        # Add processing nodes based on template
        for i, template_node in enumerate(template_nodes[:6]):  # Limit to 6 nodes
            if template_node.get('type') and 'trigger' not in template_node['type'].lower():
                node = self.create_node_from_template(template_node, i + 1)
                nodes.append(node)
        
        # Ensure we have at least 3 nodes total
        while len(nodes) < 3:
            nodes.append(self.create_basic_processing_node(len(nodes)))
        
        return nodes
    
    def create_trigger_node(self, trigger_type: str) -> Dict:
        """Create a trigger node based on type"""
        node_id = f"trigger_{random.randint(1000, 9999)}"
        
        trigger_configs = {
            'webhook': {
                'type': 'n8n-nodes-base.webhook',
                'name': 'Webhook',
                'parameters': {
                    'httpMethod': 'POST',
                    'path': f'webhook-{random.randint(1000, 9999)}',
                    'options': {}
                }
            },
            'schedule': {
                'type': 'n8n-nodes-base.scheduleTrigger',
                'name': 'Schedule Trigger',
                'parameters': {
                    'rule': {
                        'interval': [{'field': 'hours', 'hoursInterval': 1}]
                    }
                }
            },
            'manual': {
                'type': 'n8n-nodes-base.manualTrigger',
                'name': 'Manual Trigger',
                'parameters': {}
            }
        }
        
        config = trigger_configs.get(trigger_type, trigger_configs['webhook'])
        
        return {
            'id': node_id,
            'name': config['name'],
            'type': config['type'],
            'typeVersion': 1,
            'position': [200, 300],
            'parameters': config['parameters']
        }
    
    def create_node_from_template(self, template_node: Dict, index: int) -> Dict:
        """Create a node based on template node"""
        node_id = f"node_{random.randint(1000, 9999)}"
        
        # Use template node type if available
        node_type = template_node.get('type', 'n8n-nodes-base.set')
        node_name = template_node.get('name', f'Process {index}')
        
        # Common node types from training data
        common_nodes = {
            'n8n-nodes-base.set': {
                'name': 'Set Data',
                'parameters': {
                    'assignments': {
                        'assignments': [
                            {
                                'id': f'field_{random.randint(100, 999)}',
                                'name': 'processedData',
                                'value': '={{ $json }}',
                                'type': 'string'
                            }
                        ]
                    }
                }
            },
            'n8n-nodes-base.httpRequest': {
                'name': 'HTTP Request',
                'parameters': {
                    'url': 'https://api.example.com/endpoint',
                    'options': {}
                }
            },
            '@n8n/n8n-nodes-langchain.lmChatOpenAi': {
                'name': 'OpenAI Chat Model',
                'parameters': {
                    'options': {}
                }
            },
            'n8n-nodes-base.slack': {
                'name': 'Slack',
                'parameters': {
                    'operation': 'post',
                    'channel': '#general',
                    'text': '=Workflow completed: {{ $json }}'
                }
            }
        }
        
        # Get node configuration
        if node_type in common_nodes:
            config = common_nodes[node_type]
        else:
            config = {
                'name': node_name,
                'parameters': {}
            }
        
        return {
            'id': node_id,
            'name': config['name'],
            'type': node_type,
            'typeVersion': 1,
            'position': [400 + (index * 200), 300],
            'parameters': config.get('parameters', {})
        }
    
    def create_basic_processing_node(self, index: int) -> Dict:
        """Create a basic processing node"""
        node_id = f"process_{random.randint(1000, 9999)}"
        
        return {
            'id': node_id,
            'name': f'Process Data {index}',
            'type': 'n8n-nodes-base.set',
            'typeVersion': 1,
            'position': [400 + (index * 200), 300],
            'parameters': {
                'assignments': {
                    'assignments': [
                        {
                            'id': f'assignment_{random.randint(100, 999)}',
                            'name': 'result',
                            'value': '={{ $json }}',
                            'type': 'string'
                        }
                    ]
                }
            }
        }
    
    def generate_basic_nodes(self, trigger_type: str, description: str) -> List[Dict]:
        """Generate basic nodes when no template is available"""
        nodes = []
        
        # Add trigger
        nodes.append(self.create_trigger_node(trigger_type))
        
        # Add processing nodes based on description
        if 'ai' in description.lower() or 'openai' in description.lower():
            nodes.append({
                'id': f'ai_{random.randint(1000, 9999)}',
                'name': 'OpenAI Chat Model',
                'type': '@n8n/n8n-nodes-langchain.lmChatOpenAi',
                'typeVersion': 1,
                'position': [600, 300],
                'parameters': {'options': {}}
            })
        
        # Add data processing
        nodes.append(self.create_basic_processing_node(len(nodes)))
        
        return nodes
    
    def generate_connections(self, nodes: List[Dict]) -> Dict:
        """Generate connections between nodes"""
        connections = {}
        
        for i in range(len(nodes) - 1):
            current_node = nodes[i]
            next_node = nodes[i + 1]
            
            connections[current_node['name']] = {
                'main': [[{
                    'node': next_node['name'],
                    'type': 'main',
                    'index': 0
                }]]
            }
        
        return connections
    
    def create_fallback_workflow(self, description: str, trigger_type: str, complexity: str) -> Dict:
        """Create a fallback workflow when no templates match"""
        workflow_id = f"fallback_{random.randint(100000, 999999)}"
        
        return {
            "id": workflow_id,
            "name": self.generate_workflow_name(description),
            "nodes": self.generate_basic_nodes(trigger_type, description),
            "connections": {},
            "active": True,
            "settings": {},
            "staticData": None,
            "tags": [],
            "triggerCount": 0,
            "updatedAt": "2025-01-01T00:00:00.000Z",
            "versionId": "1"
        }

# Integration function for the main app
def generate_trained_workflow(description: str, trigger_type: str = 'webhook', 
                            complexity: str = 'medium') -> Dict:
    """Main function to generate workflow using trained data"""
    try:
        generator = TrainedWorkflowGenerator()
        workflow = generator.generate_realistic_workflow(description, trigger_type, complexity)
        
        print(f"[OK] Generated workflow with {len(workflow.get('nodes', []))} nodes")
        return workflow
        
    except Exception as e:
        print(f"[ERROR] Trained generation failed: {e}")
        # Fallback to basic generation
        return create_basic_fallback(description, trigger_type, complexity)

def create_basic_fallback(description: str, trigger_type: str, complexity: str) -> Dict:
    """Basic fallback when trained generation fails"""
    return {
        "id": f"basic_{random.randint(100000, 999999)}",
        "name": f"Basic {description[:30]}... Workflow",
        "nodes": [
            {
                'id': 'trigger_1',
                'name': 'Trigger',
                'type': 'n8n-nodes-base.webhook' if trigger_type == 'webhook' else 'n8n-nodes-base.manualTrigger',
                'typeVersion': 1,
                'position': [200, 300],
                'parameters': {}
            }
        ],
        "connections": {},
        "active": True,
        "settings": {},
        "staticData": None,
        "tags": [],
        "triggerCount": 0,
        "updatedAt": "2025-01-01T00:00:00.000Z",
        "versionId": "1"
    }

if __name__ == "__main__":
    # Test the generator
    generator = TrainedWorkflowGenerator()
    
    test_descriptions = [
        "Process CSV files with AI and send results to Slack",
        "Create a daily report automation with Google Sheets",
        "Build a chatbot that answers questions about PDFs"
    ]
    
    for desc in test_descriptions:
        print(f"\n🧪 Testing: {desc}")
        workflow = generator.generate_realistic_workflow(desc)
        print(f"Generated: {workflow['name']} with {len(workflow['nodes'])} nodes")