#!/usr/bin/env python3
"""
Enhanced Workflow Generator
Fixes the core issues with feature detection and template matching
"""

import json
import random
import re
from pathlib import Path
from typing import Dict, List, Set, Any, Optional, Tuple

class EnhancedFeatureDetector:
    """Improved feature detection with comprehensive keyword mapping"""
    
    FEATURE_KEYWORDS = {
        # AI and ML Features
        'openai': ['openai', 'gpt', 'chatgpt', 'ai analysis', 'ai model', 'language model'],
        'langchain': ['langchain', 'chain', 'llm', 'language chain'],
        'ai_analysis': ['ai analysis', 'analyze', 'sentiment', 'classification', 'ai processing'],
        'ai_content': ['ai content', 'generate content', 'ai writing', 'content generation'],
        'multiple_ai': ['multiple ai', 'different models', 'various ai', 'ai models'],
        
        # Communication Features
        'slack': ['slack', 'slack message', 'slack notification', 'slack channel'],
        'email': ['email', 'send email', 'email notification', 'gmail', 'outlook'],
        'telegram': ['telegram', 'telegram bot', 'telegram message'],
        'discord': ['discord', 'discord bot', 'discord message'],
        
        # Data Processing Features
        'google_sheets': ['google sheets', 'spreadsheet', 'sheets', 'google spreadsheet'],
        'excel': ['excel', 'xlsx', 'microsoft excel'],
        'csv': ['csv', 'csv file', 'comma separated'],
        'database': ['database', 'sql', 'postgres', 'mysql', 'mongodb'],
        'data_processing': ['process data', 'transform data', 'data transformation'],
        
        # Workflow Control Features
        'conditional': ['conditional', 'if then', 'condition', 'logic', 'decision'],
        'schedule': ['schedule', 'daily', 'weekly', 'hourly', 'cron', 'timer'],
        'webhook': ['webhook', 'http trigger', 'api endpoint'],
        'loops': ['loop', 'iterate', 'repeat', 'batch'],
        
        # Document Processing Features
        'pdf': ['pdf', 'pdf processing', 'document processing'],
        'ocr': ['ocr', 'text extraction', 'image to text', 'vision'],
        'document': ['document', 'file processing', 'document analysis'],
        
        # Content Management Features
        'wordpress': ['wordpress', 'blog', 'cms', 'content management'],
        'rss': ['rss', 'rss feed', 'feed reader'],
        'content': ['content', 'post', 'article', 'blog post'],
        
        # Social Media Features
        'twitter': ['twitter', 'tweet', 'social media'],
        'linkedin': ['linkedin', 'professional network'],
        'facebook': ['facebook', 'social platform'],
        
        # Analytics Features
        'analytics': ['analytics', 'tracking', 'metrics', 'reporting'],
        'monitoring': ['monitoring', 'alerts', 'notifications'],
        'dashboard': ['dashboard', 'visualization', 'charts'],
        
        # CRM Features
        'crm': ['crm', 'customer', 'hubspot', 'salesforce'],
        'approval': ['approval', 'workflow approval', 'review process'],
        
        # Financial Features
        'financial': ['financial', 'finance', 'accounting', 'money'],
        'reporting': ['reporting', 'report', 'summary'],
        'compliance': ['compliance', 'audit', 'regulation']
    }
    
    NODE_TYPE_MAPPING = {
        # AI Nodes
        'openai': ['@n8n/n8n-nodes-langchain.lmChatOpenAi', 'n8n-nodes-base.openAi'],
        'langchain': ['@n8n/n8n-nodes-langchain.chainLlm', '@n8n/n8n-nodes-langchain.agent'],
        'ai_analysis': ['@n8n/n8n-nodes-langchain.textClassifier', '@n8n/n8n-nodes-langchain.outputParserStructured'],
        'ai_content': ['@n8n/n8n-nodes-langchain.lmChatOpenAi', '@n8n/n8n-nodes-langchain.outputParserAutofixing'],
        'multiple_ai': ['@n8n/n8n-nodes-langchain.lmChatOpenAi', '@n8n/n8n-nodes-langchain.lmClaude'],
        
        # Communication Nodes
        'slack': ['n8n-nodes-base.slack'],
        'email': ['n8n-nodes-base.emailSend', 'n8n-nodes-base.gmail'],
        'telegram': ['n8n-nodes-base.telegram'],
        'discord': ['n8n-nodes-base.discord'],
        
        # Data Nodes
        'google_sheets': ['n8n-nodes-base.googleSheets'],
        'excel': ['n8n-nodes-base.microsoftExcel'],
        'csv': ['n8n-nodes-base.readBinaryFile'],
        'database': ['n8n-nodes-base.postgres', 'n8n-nodes-base.mysql'],
        'data_processing': ['n8n-nodes-base.set', 'n8n-nodes-base.code'],
        
        # Control Nodes
        'conditional': ['n8n-nodes-base.if', 'n8n-nodes-base.switch'],
        'schedule': ['n8n-nodes-base.scheduleTrigger', 'n8n-nodes-base.cron'],
        'webhook': ['n8n-nodes-base.webhook', 'n8n-nodes-base.respondToWebhook'],
        'loops': ['n8n-nodes-base.splitInBatches'],
        
        # Document Nodes
        'pdf': ['n8n-nodes-base.pdfExtract'],
        'ocr': ['n8n-nodes-base.ocrSpace'],
        'document': ['n8n-nodes-base.readBinaryFile'],
        
        # Content Nodes
        'wordpress': ['n8n-nodes-base.wordpress'],
        'rss': ['n8n-nodes-base.rssFeedRead'],
        'content': ['n8n-nodes-base.set'],
        
        # Social Nodes
        'twitter': ['n8n-nodes-base.twitter'],
        'linkedin': ['n8n-nodes-base.linkedIn'],
        'facebook': ['n8n-nodes-base.facebookGraph'],
        
        # Analytics Nodes
        'analytics': ['n8n-nodes-base.googleAnalytics'],
        'monitoring': ['n8n-nodes-base.httpRequest'],
        'dashboard': ['n8n-nodes-base.httpRequest'],
        
        # CRM Nodes
        'crm': ['n8n-nodes-base.hubspot', 'n8n-nodes-base.salesforce'],
        'approval': ['n8n-nodes-base.if'],
        
        # Financial Nodes
        'financial': ['n8n-nodes-base.set'],
        'reporting': ['n8n-nodes-base.googleSheets'],
        'compliance': ['n8n-nodes-base.set']
    }
    
    @classmethod
    def detect_features(cls, text: str) -> Dict[str, List[str]]:
        """Enhanced feature detection with better keyword matching"""
        text_lower = text.lower()
        detected_features = {}
        
        for feature, keywords in cls.FEATURE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    if feature not in detected_features:
                        detected_features[feature] = cls.NODE_TYPE_MAPPING.get(feature, [])
                    break
        
        return detected_features
    
    @classmethod
    def get_required_nodes(cls, features: Dict[str, List[str]]) -> Set[str]:
        """Get all required node types for detected features"""
        required_nodes = set()
        for node_types in features.values():
            required_nodes.update(node_types)
        return required_nodes

class EnhancedWorkflowGenerator:
    """Enhanced workflow generator with better feature matching"""
    
    def __init__(self):
        self.feature_detector = EnhancedFeatureDetector()
        self.load_training_data()
        self.create_feature_templates()
    
    def load_training_data(self):
        """Load training data with error handling"""
        try:
            with open("training_data/workflow_templates.json", 'r') as f:
                self.workflow_templates = json.load(f)
            
            with open("training_data/workflow_patterns.json", 'r') as f:
                self.workflow_patterns = json.load(f)
            
            print("✅ Loaded training data successfully")
        except Exception as e:
            print(f"⚠️ Could not load training data: {e}")
            self.workflow_templates = []
            self.workflow_patterns = []
    
    def create_feature_templates(self):
        """Create specialized templates for common feature combinations"""
        self.feature_templates = {
            'simple_webhook_slack': {
                'name': 'Simple Webhook to Slack Notification',
                'features': ['webhook', 'slack'],
                'nodes': [
                    {'type': 'n8n-nodes-base.webhook', 'name': 'Webhook'},
                    {'type': 'n8n-nodes-base.slack', 'name': 'Slack'}
                ]
            },
            'ai_slack_sheets': {
                'name': 'AI-Powered Slack and Google Sheets Integration',
                'features': ['openai', 'slack', 'google_sheets', 'conditional'],
                'nodes': [
                    {'type': 'n8n-nodes-base.webhook', 'name': 'Webhook Trigger'},
                    {'type': '@n8n/n8n-nodes-langchain.lmChatOpenAi', 'name': 'OpenAI Analysis'},
                    {'type': '@n8n/n8n-nodes-langchain.textClassifier', 'name': 'Text Classifier'},
                    {'type': 'n8n-nodes-base.if', 'name': 'Conditional Logic'},
                    {'type': 'n8n-nodes-base.slack', 'name': 'Slack Notification'},
                    {'type': 'n8n-nodes-base.googleSheets', 'name': 'Google Sheets Update'},
                    {'type': 'n8n-nodes-base.set', 'name': 'Data Processing'}
                ]
            },
            'document_ai_processing': {
                'name': 'Intelligent Document Processing Pipeline',
                'features': ['pdf', 'ocr', 'ai_analysis', 'email'],
                'nodes': [
                    {'type': 'n8n-nodes-base.emailTrigger', 'name': 'Email Trigger'},
                    {'type': 'n8n-nodes-base.pdfExtract', 'name': 'PDF Text Extraction'},
                    {'type': 'n8n-nodes-base.ocrSpace', 'name': 'OCR Processing'},
                    {'type': '@n8n/n8n-nodes-langchain.lmChatOpenAi', 'name': 'AI Document Analysis'},
                    {'type': '@n8n/n8n-nodes-langchain.textClassifier', 'name': 'Document Classification'},
                    {'type': 'n8n-nodes-base.if', 'name': 'Classification Logic'},
                    {'type': 'n8n-nodes-base.emailSend', 'name': 'Email Response'}
                ]
            },
            'content_generation_social': {
                'name': 'Multi-Platform Content Generation System',
                'features': ['ai_content', 'schedule', 'twitter', 'linkedin', 'analytics'],
                'nodes': [
                    {'type': 'n8n-nodes-base.scheduleTrigger', 'name': 'Schedule Trigger'},
                    {'type': 'n8n-nodes-base.rssFeedRead', 'name': 'RSS Feed Reader'},
                    {'type': '@n8n/n8n-nodes-langchain.lmChatOpenAi', 'name': 'Content Generator'},
                    {'type': '@n8n/n8n-nodes-langchain.outputParserStructured', 'name': 'Content Parser'},
                    {'type': 'n8n-nodes-base.twitter', 'name': 'Twitter Post'},
                    {'type': 'n8n-nodes-base.linkedIn', 'name': 'LinkedIn Post'},
                    {'type': 'n8n-nodes-base.googleAnalytics', 'name': 'Analytics Tracking'}
                ]
            },
            'financial_analysis': {
                'name': 'Automated Financial Analysis and Reporting',
                'features': ['database', 'ai_analysis', 'reporting', 'analytics'],
                'nodes': [
                    {'type': 'n8n-nodes-base.scheduleTrigger', 'name': 'Daily Schedule'},
                    {'type': 'n8n-nodes-base.postgres', 'name': 'Database Query'},
                    {'type': 'n8n-nodes-base.set', 'name': 'Data Transformation'},
                    {'type': '@n8n/n8n-nodes-langchain.lmChatOpenAi', 'name': 'AI Analysis'},
                    {'type': '@n8n/n8n-nodes-langchain.textClassifier', 'name': 'Anomaly Detection'},
                    {'type': 'n8n-nodes-base.if', 'name': 'Alert Logic'},
                    {'type': 'n8n-nodes-base.googleSheets', 'name': 'Report Generation'},
                    {'type': 'n8n-nodes-base.emailSend', 'name': 'Report Distribution'}
                ]
            },
            'customer_journey': {
                'name': 'Real-Time Customer Journey Orchestration',
                'features': ['webhook', 'ai_analysis', 'email', 'slack', 'crm'],
                'nodes': [
                    {'type': 'n8n-nodes-base.webhook', 'name': 'Event Trigger'},
                    {'type': '@n8n/n8n-nodes-langchain.lmChatOpenAi', 'name': 'AI Prediction'},
                    {'type': '@n8n/n8n-nodes-langchain.textClassifier', 'name': 'Customer Segmentation'},
                    {'type': 'n8n-nodes-base.if', 'name': 'Journey Logic'},
                    {'type': 'n8n-nodes-base.hubspot', 'name': 'CRM Update'},
                    {'type': 'n8n-nodes-base.emailSend', 'name': 'Personalized Email'},
                    {'type': 'n8n-nodes-base.slack', 'name': 'Team Notification'},
                    {'type': 'n8n-nodes-base.set', 'name': 'Data Processing'}
                ]
            }
        }
    
    def find_best_template(self, detected_features: Dict[str, List[str]], 
                          description: str) -> Tuple[Dict, float]:
        """Find the best matching template based on features"""
        
        best_template = None
        best_score = 0.0
        
        # Check feature templates first
        for template_name, template in self.feature_templates.items():
            score = self.calculate_feature_template_score(template, detected_features, description)
            if score > best_score:
                best_score = score
                best_template = template
        
        # Check training data templates if no good feature template match
        if best_score < 0.3 and self.workflow_templates:
            for template in self.workflow_templates[:10]:  # Check top 10
                score = self.calculate_training_template_score(template, detected_features, description)
                if score > best_score:
                    best_score = score
                    best_template = template
        
        return best_template, best_score
    
    def calculate_feature_template_score(self, template: Dict, detected_features: Dict[str, List[str]], 
                                       description: str) -> float:
        """Calculate score for feature templates"""
        template_features = set(template.get('features', []))
        detected_feature_names = set(detected_features.keys())
        
        # Feature overlap (70% weight)
        if template_features:
            feature_overlap = len(template_features & detected_feature_names) / len(template_features)
        else:
            feature_overlap = 0.0
        
        # Description similarity (30% weight)
        desc_words = set(description.lower().split())
        template_words = set(template.get('name', '').lower().split())
        if template_words:
            text_similarity = len(desc_words & template_words) / len(template_words | desc_words)
        else:
            text_similarity = 0.0
        
        return (feature_overlap * 0.7) + (text_similarity * 0.3)
    
    def calculate_training_template_score(self, template: Dict, detected_features: Dict[str, List[str]], 
                                        description: str) -> float:
        """Calculate score for training data templates"""
        # Extract node types from template
        template_nodes = template.get('nodes', [])
        template_node_types = set(node.get('type', '') for node in template_nodes)
        
        # Get required node types from detected features
        required_nodes = self.feature_detector.get_required_nodes(detected_features)
        
        # Node type overlap (60% weight)
        if required_nodes:
            node_overlap = len(template_node_types & required_nodes) / len(required_nodes)
        else:
            node_overlap = 0.0
        
        # Description similarity (40% weight)
        desc_words = set(description.lower().split())
        template_name = template.get('name', '').lower()
        template_words = set(template_name.split())
        
        if template_words:
            text_similarity = len(desc_words & template_words) / len(desc_words | template_words)
        else:
            text_similarity = 0.0
        
        return (node_overlap * 0.6) + (text_similarity * 0.4)
    
    def generate_enhanced_workflow(self, description: str, trigger_type: str = 'webhook',
                                 complexity: str = 'medium') -> Dict:
        """Generate workflow with enhanced feature detection and matching"""
        
        # Step 1: Enhanced feature detection
        detected_features = self.feature_detector.detect_features(description)
        print(f"🔍 Detected features: {list(detected_features.keys())}")
        
        if not detected_features:
            print("⚠️ No features detected, using basic generation")
            return self.create_basic_workflow(description, trigger_type)
        
        # Step 2: Find best matching template
        best_template, score = self.find_best_template(detected_features, description)
        
        if not best_template or score < 0.1:
            print("⚠️ No good template match, generating from features")
            return self.generate_from_features(detected_features, description, trigger_type)
        
        print(f"📋 Using template: {best_template.get('name', 'Unknown')}")
        print(f"🎯 Match score: {score:.2f}")
        
        # Step 3: Generate workflow from template
        workflow = self.create_workflow_from_template(best_template, detected_features, 
                                                    description, trigger_type)
        
        return workflow
    
    def generate_from_features(self, detected_features: Dict[str, List[str]], 
                             description: str, trigger_type: str) -> Dict:
        """Generate workflow directly from detected features"""
        
        workflow_id = f"feature_workflow_{random.randint(100000, 999999)}"
        
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
        
        # Create nodes for each detected feature
        nodes = []
        
        # Add trigger node
        trigger_node = self.create_trigger_node(trigger_type)
        nodes.append(trigger_node)
        
        # Add feature nodes
        for feature_name, node_types in detected_features.items():
            if node_types:
                # Use the first (most appropriate) node type
                node_type = node_types[0]
                node = self.create_feature_node(feature_name, node_type, len(nodes))
                nodes.append(node)
        
        # Ensure minimum complexity
        while len(nodes) < 5:
            nodes.append(self.create_processing_node(len(nodes)))
        
        workflow['nodes'] = nodes
        workflow['connections'] = self.create_connections(nodes)
        
        return workflow
    
    def create_workflow_from_template(self, template: Dict, detected_features: Dict[str, List[str]],
                                    description: str, trigger_type: str) -> Dict:
        """Create workflow from template with feature customization"""
        
        workflow_id = f"enhanced_workflow_{random.randint(100000, 999999)}"
        
        workflow = {
            "id": workflow_id,
            "name": self.generate_workflow_name(description),
            "nodes": [],
            "connections": {},
            "active": True,
            "settings": {
                "generated_by": "n8n-workflow-generator",
                "generation_timestamp": "2025-01-01T00:00:00.000Z",
                "version": "1.0"
            },
            "staticData": None,
            "tags": ["generated"],
            "triggerCount": 1,
            "updatedAt": "2025-01-01T00:00:00.000Z",
            "versionId": "1"
        }
        
        # Use template nodes if it's a feature template
        if 'nodes' in template and isinstance(template['nodes'], list):
            nodes = []
            for i, node_template in enumerate(template['nodes']):
                node = self.create_node_from_template_spec(node_template, i)
                nodes.append(node)
        else:
            # Use training data template
            nodes = self.create_nodes_from_training_template(template, detected_features, trigger_type)
        
        workflow['nodes'] = nodes
        workflow['connections'] = self.create_connections(nodes)
        
        return workflow
    
    def create_node_from_template_spec(self, node_spec: Dict, index: int) -> Dict:
        """Create node from template specification with proper structure"""
        node_id = f"node_{random.randint(1000, 9999)}"
        node_type = node_spec.get('type', 'n8n-nodes-base.set')
        
        node = {
            'id': node_id,
            'name': node_spec.get('name', f'Node {index + 1}'),
            'type': node_type,
            'typeVersion': self.get_type_version(node_type),
            'position': [200 + (index * 300), 300],  # Consistent spacing
            'parameters': self.get_node_parameters(node_type)
        }
        
        return node
    
    def create_nodes_from_training_template(self, template: Dict, detected_features: Dict[str, List[str]],
                                          trigger_type: str) -> List[Dict]:
        """Create nodes from training data template"""
        nodes = []
        
        # Add trigger
        trigger_node = self.create_trigger_node(trigger_type)
        nodes.append(trigger_node)
        
        # Add nodes from template
        template_nodes = template.get('nodes', [])
        for i, template_node in enumerate(template_nodes[:8]):  # Limit to 8 nodes
            if 'trigger' not in template_node.get('type', '').lower():
                node = self.create_node_from_training_node(template_node, i + 1)
                nodes.append(node)
        
        return nodes
    
    def create_node_from_training_node(self, template_node: Dict, index: int) -> Dict:
        """Create node from training data node"""
        node_id = f"node_{random.randint(1000, 9999)}"
        
        return {
            'id': node_id,
            'name': template_node.get('name', f'Process {index}'),
            'type': template_node.get('type', 'n8n-nodes-base.set'),
            'typeVersion': 1,
            'position': [200 + (index * 200), 300],
            'parameters': self.get_node_parameters(template_node.get('type', ''))
        }
    
    def create_trigger_node(self, trigger_type: str) -> Dict:
        """Create appropriate trigger node with proper parameters"""
        node_id = f"trigger_{random.randint(1000, 9999)}"
        
        trigger_configs = {
            'webhook': {
                'type': 'n8n-nodes-base.webhook',
                'name': 'Webhook Trigger',
                'parameters': {
                    'httpMethod': 'POST',
                    'path': f'content-webhook-{random.randint(1000, 9999)}',
                    'options': {}
                }
            },
            'schedule': {
                'type': 'n8n-nodes-base.scheduleTrigger',
                'name': 'Schedule Trigger',
                'parameters': {
                    'rule': {
                        'interval': [{'field': 'hours', 'hoursInterval': 6}]
                    }
                }
            },
            'manual': {
                'type': 'n8n-nodes-base.manualTrigger',
                'name': 'Manual Trigger',
                'parameters': {}
            }
        }
        
        config = trigger_configs.get(trigger_type, trigger_configs['schedule'])
        
        return {
            'id': node_id,
            'name': config['name'],
            'type': config['type'],
            'typeVersion': self.get_type_version(config['type']),
            'position': [200, 300],
            'parameters': config['parameters']
        }
    
    def create_feature_node(self, feature_name: str, node_type: str, index: int) -> Dict:
        """Create node for specific feature"""
        node_id = f"feature_{random.randint(1000, 9999)}"
        
        return {
            'id': node_id,
            'name': f"{feature_name.replace('_', ' ').title()} Node",
            'type': node_type,
            'typeVersion': 1,
            'position': [200 + (index * 200), 300],
            'parameters': self.get_node_parameters(node_type)
        }
    
    def create_processing_node(self, index: int) -> Dict:
        """Create basic processing node"""
        node_id = f"process_{random.randint(1000, 9999)}"
        
        return {
            'id': node_id,
            'name': f'Process Data {index}',
            'type': 'n8n-nodes-base.set',
            'typeVersion': 1,
            'position': [200 + (index * 200), 300],
            'parameters': {
                'assignments': {
                    'assignments': [
                        {
                            'id': f'assignment_{random.randint(100, 999)}',
                            'name': 'processedData',
                            'value': '={{ $json }}',
                            'type': 'string'
                        }
                    ]
                }
            }
        }
    
    def get_node_parameters(self, node_type: str) -> Dict:
        """Get appropriate parameters for node type with proper configurations"""
        
        # Schedule Trigger
        if 'scheduleTrigger' in node_type:
            return {
                'rule': {
                    'interval': [{'field': 'hours', 'hoursInterval': 6}]
                }
            }
        
        # RSS Feed Reader
        elif 'rssFeedRead' in node_type:
            return {
                'url': 'https://feeds.example.com/rss.xml'
            }
        
        # OpenAI/LangChain nodes
        elif 'openai' in node_type.lower() or 'langchain' in node_type.lower():
            if 'lmChatOpenAi' in node_type:
                return {
                    'options': {
                        'systemMessage': 'Generate engaging social media posts based on the provided content.'
                    }
                }
            elif 'outputParserStructured' in node_type:
                return {
                    'jsonSchema': {
                        'type': 'object',
                        'properties': {
                            'post': {'type': 'string', 'description': 'Social media post content'},
                            'hashtags': {'type': 'array', 'items': {'type': 'string'}}
                        }
                    }
                }
            else:
                return {'options': {}}
        
        # Social Media nodes
        elif 'twitter' in node_type.lower():
            return {
                'operation': 'tweet',
                'text': '={{ $json.post }} {{ $json.hashtags.join(" ") }}'
            }
        elif 'linkedin' in node_type.lower():
            return {
                'operation': 'post',
                'text': '={{ $json.post }}',
                'visibility': 'public'
            }
        
        # Communication nodes
        elif 'slack' in node_type.lower():
            return {
                'operation': 'post',
                'channel': '#general',
                'text': '🚨 Webhook Alert!\n\n📝 Message: {{ $json.message || "Webhook triggered" }}\n⏰ Time: {{ new Date().toLocaleString() }}\n📊 Data: {{ JSON.stringify($json, null, 2) }}'
            }
        elif 'email' in node_type.lower():
            return {
                'toEmail': 'team@company.com',
                'subject': 'Content Posted Successfully',
                'text': '=Content has been posted: {{ $json.post }}'
            }
        
        # Data processing nodes
        elif 'sheets' in node_type.lower():
            return {
                'operation': 'append',
                'sheetId': 'Content Log',
                'range': 'A:D',
                'values': {
                    'values': [
                        ['={{ new Date().toISOString() }}', '={{ $json.title }}', '={{ $json.post }}', '=Posted']
                    ]
                }
            }
        elif 'set' in node_type.lower():
            return {
                'assignments': {
                    'assignments': [
                        {
                            'id': f'assignment_{random.randint(100, 999)}',
                            'name': 'message',
                            'value': '={{ $json.message || "Webhook notification received" }}',
                            'type': 'string'
                        },
                        {
                            'id': f'assignment_{random.randint(100, 999)}',
                            'name': 'timestamp',
                            'value': '={{ new Date().toISOString() }}',
                            'type': 'string'
                        },
                        {
                            'id': f'assignment_{random.randint(100, 999)}',
                            'name': 'originalData',
                            'value': '={{ $json }}',
                            'type': 'object'
                        }
                    ]
                }
            }
        
        # Analytics nodes
        elif 'analytics' in node_type.lower():
            return {
                'operation': 'track',
                'event': 'content_posted',
                'properties': {
                    'platform': '={{ $json.platform }}',
                    'content_type': 'social_media_post'
                }
            }
        
        # HTTP Request
        elif 'http' in node_type.lower():
            return {
                'url': 'https://api.example.com/webhook',
                'method': 'POST',
                'options': {
                    'headers': {
                        'Content-Type': 'application/json'
                    }
                },
                'body': {
                    'data': '={{ $json }}'
                }
            }
        
        # Webhook
        elif 'webhook' in node_type.lower():
            return {
                'httpMethod': 'POST',
                'path': f'slack-alert-{random.randint(1000, 9999)}',
                'options': {
                    'noResponseBody': False
                },
                'responseMode': 'onReceived'
            }
        
        # Conditional logic
        elif 'if' in node_type.lower():
            return {
                'conditions': {
                    'options': {
                        'caseSensitive': True,
                        'leftValue': '={{ $json.content }}',
                        'operation': 'isNotEmpty'
                    }
                }
            }
        
        # Code nodes
        elif 'code' in node_type.lower():
            return {
                'jsCode': '''// Process and transform data
const inputData = $input.all();
const processedData = inputData.map(item => ({
  ...item.json,
  processed: true,
  processed_at: new Date().toISOString(),
  workflow_step: 'enhanced_processing'
}));

return processedData;'''
            }
        
        return {}
    
    def create_connections(self, nodes: List[Dict]) -> Dict:
        """Create proper connections between nodes using node names (n8n format)"""
        connections = {}
        
        for i in range(len(nodes) - 1):
            current_node = nodes[i]
            next_node = nodes[i + 1]
            
            # n8n uses node names as keys for connections
            current_name = current_node['name']
            next_name = next_node['name']
            
            # Ensure proper n8n connection format
            connections[current_name] = {
                'main': [[{
                    'node': next_name,
                    'type': 'main',
                    'index': 0
                }]]
            }
        
        return connections
    
    def get_type_version(self, node_type: str) -> int:
        """Get appropriate type version for node type"""
        # Common type versions for n8n nodes
        if 'langchain' in node_type.lower():
            return 1
        elif 'scheduleTrigger' in node_type:
            return 1.2
        elif 'code' in node_type:
            return 2
        else:
            return 1
    
    def generate_workflow_name(self, description: str) -> str:
        """Generate appropriate workflow name"""
        words = description.split()
        key_words = [w for w in words if len(w) > 3 and w.lower() not in 
                    ['the', 'and', 'with', 'from', 'that', 'this', 'will', 'can', 'for']]
        
        if len(key_words) >= 3:
            return f"{key_words[0].title()} {key_words[1].title()} {key_words[2].title()}"
        elif len(key_words) >= 2:
            return f"{key_words[0].title()} {key_words[1].title()} Workflow"
        elif len(key_words) >= 1:
            return f"{key_words[0].title()} Automation"
        else:
            return "Custom Workflow"
    
    def create_basic_workflow(self, description: str, trigger_type: str) -> Dict:
        """Create basic workflow when feature detection fails"""
        workflow_id = f"basic_{random.randint(100000, 999999)}"
        
        return {
            "id": workflow_id,
            "name": self.generate_workflow_name(description),
            "nodes": [
                self.create_trigger_node(trigger_type),
                self.create_processing_node(1),
                self.create_processing_node(2)
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

# Main integration function
def generate_enhanced_workflow(description: str, trigger_type: str = 'webhook',
                             complexity: str = 'medium') -> Dict:
    """Generate workflow using enhanced system"""
    try:
        generator = EnhancedWorkflowGenerator()
        workflow = generator.generate_enhanced_workflow(description, trigger_type, complexity)
        
        print(f"✅ Generated enhanced workflow with {len(workflow.get('nodes', []))} nodes")
        return workflow
        
    except Exception as e:
        print(f"❌ Enhanced generation failed: {e}")
        # Create minimal fallback
        return {
            "id": f"fallback_{random.randint(100000, 999999)}",
            "name": f"Fallback Workflow",
            "nodes": [],
            "connections": {},
            "active": True
        }

if __name__ == "__main__":
    # Test the enhanced generator
    test_descriptions = [
        "Create an AI-powered workflow that monitors Slack messages, uses OpenAI to analyze sentiment, stores results in Google Sheets, and sends notifications based on conditional logic",
        "Build a multi-modal content generation system with scheduled triggers, RSS feeds, AI content generation, and multi-platform posting to Twitter and LinkedIn",
        "Design an intelligent document processing workflow with email triggers, OCR processing, AI document classification, and CRM integration"
    ]
    
    generator = EnhancedWorkflowGenerator()
    
    for desc in test_descriptions:
        print(f"\n🧪 Testing: {desc[:80]}...")
        workflow = generator.generate_enhanced_workflow(desc)
        print(f"Generated: {workflow['name']} with {len(workflow['nodes'])} nodes")
        
        # Show node types
        node_types = [node.get('type', 'unknown') for node in workflow.get('nodes', [])]
        print(f"Node types: {node_types}")