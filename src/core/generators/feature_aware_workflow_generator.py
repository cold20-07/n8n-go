#!/usr/bin/env python3
"""
Feature-Aware Workflow Generator
Enhanced version with comprehensive feature detection and pattern matching
"""

import json
import re
from typing import Dict, List, Set, Any, Optional
from pathlib import Path

class FeatureMap:
    """Comprehensive mapping of features to n8n node types and patterns"""
    
    # AI and ML Features
    AI_NODES = {
        'openai': ['@n8n/n8n-nodes-langchain.lmChatOpenAi', '@n8n/n8n-nodes-langchain.openAi'],
        'langchain': ['@n8n/n8n-nodes-langchain.agent', '@n8n/n8n-nodes-langchain.chainLlm'],
        'claude': ['@n8n/n8n-nodes-langchain.lmClaude'],
        'gemini': ['@n8n/n8n-nodes-langchain.lmGemini'],
        'ai_output': ['@n8n/n8n-nodes-langchain.outputParserStructured', '@n8n/n8n-nodes-langchain.outputParserAutofixing'],
        'embeddings': ['@n8n/n8n-nodes-langchain.embeddingsOpenAi'],
        'vector_store': ['@n8n/n8n-nodes-langchain.vectorStoreQdrant', '@n8n/n8n-nodes-langchain.vectorStorePinecone']
    }
    
    # Communication and Integration Features
    COMMUNICATION_NODES = {
        'slack': ['n8n-nodes-base.slack'],
        'email': ['n8n-nodes-base.emailSend', 'n8n-nodes-base.gmail', 'n8n-nodes-base.outlook'],
        'telegram': ['n8n-nodes-base.telegram'],
        'discord': ['n8n-nodes-base.discord'],
        'webhook': ['n8n-nodes-base.webhook', 'n8n-nodes-base.webhookRespond'],
        'http': ['n8n-nodes-base.httpRequest']
    }
    
    # Data Processing Features
    DATA_NODES = {
        'spreadsheet': ['n8n-nodes-base.googleSheets', 'n8n-nodes-base.microsoftExcel'],
        'database': ['n8n-nodes-base.postgres', 'n8n-nodes-base.mysql', 'n8n-nodes-base.mongodb'],
        'transform': ['n8n-nodes-base.set', 'n8n-nodes-base.code', 'n8n-nodes-base.function'],
        'files': ['n8n-nodes-base.readBinaryFile', 'n8n-nodes-base.writeBinaryFile', 'n8n-nodes-base.spreadsheetFile'],
        'csv': ['n8n-nodes-base.csvReadFile', 'n8n-nodes-base.csvWriteFile']
    }
    
    # Content Management Features
    CMS_NODES = {
        'wordpress': ['n8n-nodes-base.wordpress'],
        'ghost': ['n8n-nodes-base.ghost'],
        'strapi': ['n8n-nodes-base.strapi'],
        'contentful': ['n8n-nodes-base.contentful']
    }
    
    # Flow Control Features
    FLOW_NODES = {
        'conditional': ['n8n-nodes-base.if', 'n8n-nodes-base.switch'],
        'loops': ['n8n-nodes-base.splitInBatches', 'n8n-nodes-base.loop'],
        'merge': ['n8n-nodes-base.merge'],
        'split': ['n8n-nodes-base.splitOut']
    }
    
    # Trigger Features
    TRIGGER_NODES = {
        'schedule': ['n8n-nodes-base.scheduleTrigger', 'n8n-nodes-base.cron'],
        'webhook': ['n8n-nodes-base.webhook'],
        'manual': ['n8n-nodes-base.manualTrigger'],
        'email_trigger': ['n8n-nodes-base.emailTrigger']
    }
    
    # Analytics and Monitoring Features
    ANALYTICS_NODES = {
        'google_analytics': ['n8n-nodes-base.googleAnalytics'],
        'tracking': ['n8n-nodes-base.segment'],
        'monitoring': ['n8n-nodes-base.sentryIo']
    }
    
    # Document Processing Features
    DOCUMENT_NODES = {
        'pdf': ['n8n-nodes-base.pdfExtract', 'n8n-nodes-base.pdfCreate'],
        'ocr': ['n8n-nodes-base.ocrSpace'],
        'docs': ['n8n-nodes-base.googleDocs', 'n8n-nodes-base.microsoftWord']
    }
    
    # Social Media Features
    SOCIAL_NODES = {
        'twitter': ['n8n-nodes-base.twitter'],
        'linkedin': ['n8n-nodes-base.linkedIn'],
        'facebook': ['n8n-nodes-base.facebookGraph'],
        'instagram': ['n8n-nodes-base.instagram']
    }
    
    # CRM Features
    CRM_NODES = {
        'hubspot': ['n8n-nodes-base.hubspot'],
        'salesforce': ['n8n-nodes-base.salesforce'],
        'pipedrive': ['n8n-nodes-base.pipedrive']
    }
    
    @classmethod
    def get_all_features(cls) -> Dict[str, List[str]]:
        """Get all feature categories and their node types"""
        return {
            'AI_ML': cls.AI_NODES,
            'COMMUNICATION': cls.COMMUNICATION_NODES,
            'DATA': cls.DATA_NODES,
            'CMS': cls.CMS_NODES,
            'FLOW': cls.FLOW_NODES,
            'TRIGGER': cls.TRIGGER_NODES,
            'ANALYTICS': cls.ANALYTICS_NODES,
            'DOCUMENT': cls.DOCUMENT_NODES,
            'SOCIAL': cls.SOCIAL_NODES,
            'CRM': cls.CRM_NODES
        }
    
    @classmethod
    def get_nodes_for_feature(cls, feature: str) -> List[str]:
        """Get all node types associated with a feature"""
        feature_lower = feature.lower()
        all_features = cls.get_all_features()
        
        for category in all_features.values():
            for feature_name, nodes in category.items():
                if feature_lower in feature_name.lower():
                    return nodes
        return []
    
    @classmethod
    def detect_features_in_text(cls, text: str) -> Dict[str, List[str]]:
        """Detect features mentioned in text and return relevant node types"""
        text_lower = text.lower()
        detected_features = {}
        
        # Check each feature category
        for category_name, category in cls.get_all_features().items():
            for feature_name, nodes in category.items():
                # Look for feature keywords in text
                if any(keyword in text_lower for keyword in feature_name.lower().split('_')):
                    detected_features[feature_name] = nodes
        
        return detected_features
    
    @classmethod
    def get_required_nodes(cls, features: Dict[str, List[str]]) -> Set[str]:
        """Get unique set of node types needed for detected features"""
        required_nodes = set()
        for nodes in features.values():
            required_nodes.update(nodes)
        return required_nodes

class FeatureAwareGenerator:
    """Enhanced workflow generator with comprehensive feature awareness"""
    
    def __init__(self, training_data_dir: str = "training_data"):
        self.data_dir = Path(training_data_dir)
        self.feature_map = FeatureMap()
        self.load_training_data()
    
    def load_training_data(self):
        """Load and analyze training data"""
        try:
            # Load workflow templates
            with open(self.data_dir / "workflow_templates.json", 'r') as f:
                self.workflow_templates = json.load(f)
            
            # Load workflow patterns
            with open(self.data_dir / "workflow_patterns.json", 'r') as f:
                self.workflow_patterns = json.load(f)
            
            # Load statistics for node frequencies
            with open(self.data_dir / "statistics.json", 'r') as f:
                self.statistics = json.load(f)
            
            # Analyze node patterns in training data
            self.analyze_training_patterns()
            
        except Exception as e:
            print(f"⚠️ Error loading training data: {e}")
            raise
    
    def analyze_training_patterns(self):
        """Analyze patterns in training data for better matching"""
        self.node_patterns = {}
        self.feature_patterns = {}
        
        for template in self.workflow_templates:
            nodes = template.get('nodes', [])
            node_types = [node.get('type', '') for node in nodes]
            
            # Extract features from this template
            features = self.detect_template_features(node_types)
            
            # Store pattern
            pattern_key = frozenset(features.keys())
            if pattern_key not in self.feature_patterns:
                self.feature_patterns[pattern_key] = []
            self.feature_patterns[pattern_key].append(template)
    
    def detect_template_features(self, node_types: List[str]) -> Dict[str, List[str]]:
        """Detect features present in a template based on its node types"""
        features = {}
        
        for category_name, category in self.feature_map.get_all_features().items():
            for feature_name, feature_nodes in category.items():
                if any(node_type in feature_nodes for node_type in node_types):
                    features[feature_name] = feature_nodes
        
        return features
    
    def find_matching_templates(self, required_features: Dict[str, List[str]], 
                              description: str) -> List[Dict]:
        """Find templates that match required features"""
        matching_templates = []
        required_feature_set = frozenset(required_features.keys())
        
        # Look for exact feature matches first
        if required_feature_set in self.feature_patterns:
            matching_templates.extend(self.feature_patterns[required_feature_set])
        
        # Look for partial matches
        for pattern_features, templates in self.feature_patterns.items():
            if not matching_templates and pattern_features.intersection(required_feature_set):
                matching_templates.extend(templates)
        
        # Score matches
        scored_templates = []
        for template in matching_templates:
            score = self.calculate_template_match_score(template, required_features, description)
            scored_templates.append((template, score))
        
        # Sort by score
        scored_templates.sort(key=lambda x: x[1], reverse=True)
        
        return [t[0] for t in scored_templates]
    
    def calculate_template_match_score(self, template: Dict, required_features: Dict[str, List[str]], 
                                     description: str) -> float:
        """Calculate how well a template matches requirements"""
        score = 0.0
        template_nodes = template.get('nodes', [])
        template_node_types = [node.get('type', '') for node in template_nodes]
        
        # Feature coverage (50%)
        required_nodes = self.feature_map.get_required_nodes(required_features)
        feature_coverage = sum(1 for node in required_nodes 
                             if any(node in nt for nt in template_node_types))
        score += (feature_coverage / max(len(required_nodes), 1)) * 0.5
        
        # Node type similarity (30%)
        template_features = self.detect_template_features(template_node_types)
        feature_similarity = len(set(template_features.keys()) & set(required_features.keys()))
        score += (feature_similarity / max(len(required_features), 1)) * 0.3
        
        # Text similarity (20%)
        desc_words = set(description.lower().split())
        template_words = set(template.get('name', '').lower().split())
        text_similarity = len(desc_words & template_words) / max(len(desc_words | template_words), 1)
        score += text_similarity * 0.2
        
        return score
    
    def generate_workflow(self, description: str, trigger_type: str = 'webhook',
                         complexity: str = 'medium') -> Dict:
        """Generate a workflow with comprehensive feature awareness"""
        
        # Step 1: Detect required features
        required_features = self.feature_map.detect_features_in_text(description)
        print(f"Feature Detection: Detected features: {list(required_features.keys())}")
        
        # Step 2: Find matching templates
        matching_templates = self.find_matching_templates(required_features, description)
        
        if not matching_templates:
            print("⚠️ No exact template matches, generating from features")
            return self.generate_from_features(required_features, description, trigger_type)
        
        # Step 3: Use best matching template
        template = matching_templates[0]
        print(f"📋 Using template: {template.get('name', 'Unknown')}")
        
        # Step 4: Customize template
        workflow = self.customize_template(template, required_features, description, trigger_type)
        
        return workflow
    
    def generate_from_features(self, required_features: Dict[str, List[str]], 
                             description: str, trigger_type: str) -> Dict:
        """Generate workflow directly from required features"""
        
        # Create basic workflow structure
        workflow = {
            "name": self.generate_name(description),
            "nodes": [],
            "connections": {},
            "active": True,
            "settings": {},
            "tags": [],
            "triggerCount": 1
        }
        
        # Add trigger node
        trigger_node = self.create_trigger_node(trigger_type)
        workflow['nodes'].append(trigger_node)
        last_node = trigger_node
        
        # Add nodes for each required feature
        for feature_name, feature_nodes in required_features.items():
            if feature_nodes:
                node = self.create_feature_node(feature_name, feature_nodes[0])
                workflow['nodes'].append(node)
                
                # Connect to previous node
                if last_node:
                    workflow['connections'][last_node['name']] = {
                        'main': [[{'node': node['name'], 'type': 'main', 'index': 0}]]
                    }
                last_node = node
        
        return workflow
    
    def customize_template(self, template: Dict, required_features: Dict[str, List[str]],
                         description: str, trigger_type: str) -> Dict:
        """Customize a template with required features"""
        workflow = template.copy()
        
        # Update basic info
        workflow['name'] = self.generate_name(description)
        
        # Ensure all required features are present
        required_nodes = self.feature_map.get_required_nodes(required_features)
        existing_nodes = set(node.get('type', '') for node in workflow.get('nodes', []))
        
        # Add missing feature nodes
        for node_type in required_nodes:
            if not any(node_type in nt for nt in existing_nodes):
                feature_name = next(name for name, nodes in required_features.items() 
                                  if node_type in nodes)
                node = self.create_feature_node(feature_name, node_type)
                workflow['nodes'].append(node)
                
                # Connect to last node
                if workflow['nodes']:
                    last_node = workflow['nodes'][-2]
                    workflow['connections'][last_node['name']] = {
                        'main': [[{'node': node['name'], 'type': 'main', 'index': 0}]]
                    }
        
        return workflow
    
    def create_trigger_node(self, trigger_type: str) -> Dict:
        """Create appropriate trigger node"""
        trigger_nodes = self.feature_map.TRIGGER_NODES.get(trigger_type, 
                       self.feature_map.TRIGGER_NODES['webhook'])
        
        return {
            'name': 'Trigger',
            'type': trigger_nodes[0],
            'parameters': {},
            'position': [250, 300]
        }
    
    def create_feature_node(self, feature_name: str, node_type: str) -> Dict:
        """Create a node for a specific feature"""
        return {
            'name': f"{feature_name.replace('_', ' ').title()} Node",
            'type': node_type,
            'parameters': self.get_default_parameters(node_type),
            'position': [450, 300]
        }
    
    def get_default_parameters(self, node_type: str) -> Dict:
        """Get default parameters for node type"""
        if 'openai' in node_type.lower() or 'langchain' in node_type.lower():
            return {'options': {}}
        elif 'slack' in node_type.lower():
            return {'channel': '#general', 'text': '={{ $json }}'}
        elif 'sheets' in node_type.lower():
            return {'operation': 'append'}
        elif 'http' in node_type.lower():
            return {'url': '', 'options': {}}
        return {}
    
    def generate_name(self, description: str) -> str:
        """Generate workflow name from description"""
        words = description.split()[:3]
        return ' '.join(word.capitalize() for word in words) + ' Workflow'

# Integration function
def generate_feature_aware_workflow(description: str, trigger_type: str = 'webhook',
                                  complexity: str = 'medium') -> Dict:
    """Generate workflow using feature-aware system"""
    generator = FeatureAwareGenerator()
    return generator.generate_workflow(description, trigger_type, complexity)

if __name__ == "__main__":
    # Test the feature-aware generator
    test_description = """Create an AI-powered workflow that monitors Slack messages, 
    uses OpenAI to analyze sentiment and categorize topics, stores results in Google Sheets, 
    and sends notifications based on urgency levels."""
    
    generator = FeatureAwareGenerator()
    workflow = generator.generate_workflow(test_description)
    
    print(f"\n✅ Generated workflow with {len(workflow.get('nodes', []))} nodes")
    print(f"Features detected: {list(FeatureMap.detect_features_in_text(test_description).keys())}")
    print(f"Node types used: {[node.get('type') for node in workflow.get('nodes', [])]}")