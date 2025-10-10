"""
Workflow Template System for N8N Workflow Generator
Provides pre-built templates for common automation patterns
"""
import json
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class TemplateCategory(Enum):
    """Template categories for organization"""
    DATA_PROCESSING = "data_processing"
    COMMUNICATION = "communication"
    SOCIAL_MEDIA = "social_media"
    E_COMMERCE = "e_commerce"
    MONITORING = "monitoring"
    PRODUCTIVITY = "productivity"
    INTEGRATION = "integration"
    AUTOMATION = "automation"

@dataclass
class WorkflowTemplate:
    """Workflow template definition"""
    id: str
    name: str
    description: str
    category: TemplateCategory
    complexity: str
    tags: List[str]
    workflow_json: Dict[str, Any]
    use_cases: List[str]
    required_services: List[str]

class WorkflowTemplateManager:
    """Manages workflow templates and provides template-based generation"""
    
    def __init__(self):
        self.templates = {}
        self._load_default_templates()
    
    def _load_default_templates(self):
        """Load default workflow templates"""
        
        # RSS to Social Media Template
        self.register_template(WorkflowTemplate(
            id="rss_to_social",
            name="RSS to Social Media",
            description="Monitor RSS feeds and automatically post to social media platforms",
            category=TemplateCategory.SOCIAL_MEDIA,
            complexity="medium",
            tags=["rss", "social", "automation", "content"],
            use_cases=[
                "Auto-post blog updates to Twitter",
                "Share news articles on LinkedIn",
                "Cross-post content to multiple platforms"
            ],
            required_services=["RSS Feed", "Twitter/LinkedIn/Facebook"],
            workflow_json={
                "name": "RSS to Social Media Automation",
                "nodes": [
                    {
                        "id": "rss-trigger",
                        "name": "RSS Feed Monitor",
                        "type": "n8n-nodes-base.rssFeedRead",
                        "position": [250, 300],
                        "parameters": {
                            "url": "https://example.com/feed.xml",
                            "pollTimes": {
                                "item": [
                                    {"mode": "everyMinute", "value": 15}
                                ]
                            }
                        }
                    },
                    {
                        "id": "content-filter",
                        "name": "Content Filter",
                        "type": "n8n-nodes-base.if",
                        "position": [450, 300],
                        "parameters": {
                            "conditions": {
                                "string": [
                                    {
                                        "value1": "={{$json.title}}",
                                        "operation": "isNotEmpty"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "id": "format-post",
                        "name": "Format Social Post",
                        "type": "n8n-nodes-base.set",
                        "position": [650, 300],
                        "parameters": {
                            "values": {
                                "string": [
                                    {
                                        "name": "post_content",
                                        "value": "New post: {{$json.title}} - {{$json.link}}"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "id": "post-twitter",
                        "name": "Post to Twitter",
                        "type": "n8n-nodes-base.twitter",
                        "position": [850, 300],
                        "parameters": {
                            "operation": "tweet",
                            "text": "={{$json.post_content}}"
                        }
                    }
                ],
                "connections": {
                    "RSS Feed Monitor": {
                        "main": [
                            [{"node": "Content Filter", "type": "main", "index": 0}]
                        ]
                    },
                    "Content Filter": {
                        "main": [
                            [{"node": "Format Social Post", "type": "main", "index": 0}]
                        ]
                    },
                    "Format Social Post": {
                        "main": [
                            [{"node": "Post to Twitter", "type": "main", "index": 0}]
                        ]
                    }
                },
                "active": True,
                "settings": {}
            }
        ))
        
        # Email Processing Template
        self.register_template(WorkflowTemplate(
            id="email_processing",
            name="Email Processing & Response",
            description="Process incoming emails and send automated responses",
            category=TemplateCategory.COMMUNICATION,
            complexity="medium",
            tags=["email", "automation", "customer-service"],
            use_cases=[
                "Auto-respond to customer inquiries",
                "Process support tickets",
                "Forward emails based on content"
            ],
            required_services=["Email (IMAP)", "Email (SMTP)"],
            workflow_json={
                "name": "Email Processing Automation",
                "nodes": [
                    {
                        "id": "email-trigger",
                        "name": "Email Trigger",
                        "type": "n8n-nodes-base.emailReadImap",
                        "position": [250, 300],
                        "parameters": {
                            "format": "simple",
                            "options": {
                                "allowUnauthorizedCerts": True
                            }
                        }
                    },
                    {
                        "id": "analyze-email",
                        "name": "Analyze Email Content",
                        "type": "n8n-nodes-base.set",
                        "position": [450, 300],
                        "parameters": {
                            "values": {
                                "string": [
                                    {
                                        "name": "priority",
                                        "value": "={{$json.subject.toLowerCase().includes('urgent') ? 'high' : 'normal'}}"
                                    },
                                    {
                                        "name": "category",
                                        "value": "={{$json.subject.toLowerCase().includes('support') ? 'support' : 'general'}}"
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "id": "send-response",
                        "name": "Send Auto Response",
                        "type": "n8n-nodes-base.emailSend",
                        "position": [650, 300],
                        "parameters": {
                            "toEmail": "={{$json.from}}",
                            "subject": "Re: {{$json.subject}}",
                            "message": "Thank you for your email. We have received your {{$json.category}} request and will respond within 24 hours."
                        }
                    }
                ],
                "connections": {
                    "Email Trigger": {
                        "main": [
                            [{"node": "Analyze Email Content", "type": "main", "index": 0}]
                        ]
                    },
                    "Analyze Email Content": {
                        "main": [
                            [{"node": "Send Auto Response", "type": "main", "index": 0}]
                        ]
                    }
                },
                "active": True,
                "settings": {}
            }
        ))
        
        # Data Backup Template
        self.register_template(WorkflowTemplate(
            id="data_backup",
            name="Automated Data Backup",
            description="Automatically backup files to cloud storage on schedule",
            category=TemplateCategory.DATA_PROCESSING,
            complexity="simple",
            tags=["backup", "storage", "schedule", "files"],
            use_cases=[
                "Daily database backups",
                "Weekly file system backups",
                "Sync important documents to cloud"
            ],
            required_services=["File System", "Cloud Storage (Google Drive/Dropbox)"],
            workflow_json={
                "name": "Automated Data Backup",
                "nodes": [
                    {
                        "id": "schedule-trigger",
                        "name": "Daily Backup Schedule",
                        "type": "n8n-nodes-base.cron",
                        "position": [250, 300],
                        "parameters": {
                            "triggerTimes": {
                                "item": [
                                    {"hour": 2, "minute": 0}
                                ]
                            }
                        }
                    },
                    {
                        "id": "read-files",
                        "name": "Read Files",
                        "type": "n8n-nodes-base.readBinaryFiles",
                        "position": [450, 300],
                        "parameters": {
                            "fileSelector": "/path/to/backup/*"
                        }
                    },
                    {
                        "id": "upload-cloud",
                        "name": "Upload to Cloud",
                        "type": "n8n-nodes-base.googleDrive",
                        "position": [650, 300],
                        "parameters": {
                            "operation": "upload",
                            "name": "backup_{{$now.format('YYYY-MM-DD')}}.zip"
                        }
                    }
                ],
                "connections": {
                    "Daily Backup Schedule": {
                        "main": [
                            [{"node": "Read Files", "type": "main", "index": 0}]
                        ]
                    },
                    "Read Files": {
                        "main": [
                            [{"node": "Upload to Cloud", "type": "main", "index": 0}]
                        ]
                    }
                },
                "active": True,
                "settings": {}
            }
        ))
        
        # E-commerce Order Processing Template
        self.register_template(WorkflowTemplate(
            id="ecommerce_orders",
            name="E-commerce Order Processing",
            description="Process new orders, update inventory, and send notifications",
            category=TemplateCategory.E_COMMERCE,
            complexity="complex",
            tags=["ecommerce", "orders", "inventory", "notifications"],
            use_cases=[
                "Process Shopify orders",
                "Update inventory systems",
                "Send order confirmations",
                "Notify fulfillment team"
            ],
            required_services=["E-commerce Platform", "Email", "Inventory System"],
            workflow_json={
                "name": "E-commerce Order Processing",
                "nodes": [
                    {
                        "id": "order-webhook",
                        "name": "New Order Webhook",
                        "type": "n8n-nodes-base.webhook",
                        "position": [250, 300],
                        "parameters": {
                            "httpMethod": "POST",
                            "path": "new-order"
                        }
                    },
                    {
                        "id": "validate-order",
                        "name": "Validate Order",
                        "type": "n8n-nodes-base.if",
                        "position": [450, 300],
                        "parameters": {
                            "conditions": {
                                "number": [
                                    {
                                        "value1": "={{$json.total_price}}",
                                        "operation": "larger",
                                        "value2": 0
                                    }
                                ]
                            }
                        }
                    },
                    {
                        "id": "update-inventory",
                        "name": "Update Inventory",
                        "type": "n8n-nodes-base.httpRequest",
                        "position": [650, 200],
                        "parameters": {
                            "method": "POST",
                            "url": "https://api.inventory.com/update",
                            "body": {
                                "order_id": "={{$json.id}}",
                                "items": "={{$json.line_items}}"
                            }
                        }
                    },
                    {
                        "id": "send-confirmation",
                        "name": "Send Order Confirmation",
                        "type": "n8n-nodes-base.emailSend",
                        "position": [650, 400],
                        "parameters": {
                            "toEmail": "={{$json.customer.email}}",
                            "subject": "Order Confirmation #{{$json.order_number}}",
                            "message": "Thank you for your order! Your order #{{$json.order_number}} has been received and is being processed."
                        }
                    }
                ],
                "connections": {
                    "New Order Webhook": {
                        "main": [
                            [{"node": "Validate Order", "type": "main", "index": 0}]
                        ]
                    },
                    "Validate Order": {
                        "main": [
                            [
                                {"node": "Update Inventory", "type": "main", "index": 0},
                                {"node": "Send Order Confirmation", "type": "main", "index": 0}
                            ]
                        ]
                    }
                },
                "active": True,
                "settings": {}
            }
        ))
    
    def register_template(self, template: WorkflowTemplate):
        """Register a new workflow template"""
        self.templates[template.id] = template
    
    def get_template(self, template_id: str) -> Optional[WorkflowTemplate]:
        """Get a specific template by ID"""
        # Check cache first
        try:
            from src.core.cache import get_cache
            cache = get_cache()
            cache_key = cache._generate_key("template", template_id)
            
            cached_template = cache.get(cache_key)
            if cached_template is not None:
                return cached_template
        except Exception:
            pass
        
        template = self.templates.get(template_id)
        
        # Cache the result
        if template:
            try:
                from src.core.cache import get_cache
                cache = get_cache()
                cache_key = cache._generate_key("template", template_id)
                cache.set(cache_key, template, 7200)  # 2 hours TTL
            except Exception:
                pass
        
        return template
    
    def get_templates_by_category(self, category: TemplateCategory) -> List[WorkflowTemplate]:
        """Get all templates in a specific category"""
        return [t for t in self.templates.values() if t.category == category]
    
    def search_templates(self, query: str) -> List[WorkflowTemplate]:
        """Search templates by name, description, or tags"""
        query_lower = query.lower()
        results = []
        
        for template in self.templates.values():
            if (query_lower in template.name.lower() or 
                query_lower in template.description.lower() or
                any(query_lower in tag.lower() for tag in template.tags)):
                results.append(template)
        
        return results
    
    def get_all_templates(self) -> List[WorkflowTemplate]:
        """Get all available templates"""
        # Check cache first
        try:
            from src.core.cache import get_cache
            cache = get_cache()
            cache_key = cache._generate_key("all_templates")
            
            cached_templates = cache.get(cache_key)
            if cached_templates is not None:
                return cached_templates
        except Exception:
            pass
        
        templates = list(self.templates.values())
        
        # Cache the result
        try:
            from src.core.cache import get_cache
            cache = get_cache()
            cache_key = cache._generate_key("all_templates")
            cache.set(cache_key, templates, 7200)  # 2 hours TTL
        except Exception:
            pass
        
        return templates
    
    def get_template_suggestions(self, description: str) -> List[WorkflowTemplate]:
        """Get template suggestions based on user description"""
        description_lower = description.lower()
        suggestions = []
        
        # Score templates based on keyword matches
        for template in self.templates.values():
            score = 0
            
            # Check tags
            for tag in template.tags:
                if tag.lower() in description_lower:
                    score += 3
            
            # Check use cases
            for use_case in template.use_cases:
                if any(word in description_lower for word in use_case.lower().split()):
                    score += 2
            
            # Check name and description
            if any(word in description_lower for word in template.name.lower().split()):
                score += 2
            
            if score > 0:
                suggestions.append((template, score))
        
        # Sort by score and return top suggestions
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return [template for template, score in suggestions[:5]]
    
    def customize_template(self, template_id: str, customizations: Dict[str, Any]) -> Dict[str, Any]:
        """Customize a template with user-specific parameters"""
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        # Deep copy the workflow JSON
        workflow = json.loads(json.dumps(template.workflow_json))
        
        # Apply customizations
        if 'name' in customizations:
            workflow['name'] = customizations['name']
        
        # Customize node parameters
        if 'node_params' in customizations:
            for node in workflow['nodes']:
                node_id = node['id']
                if node_id in customizations['node_params']:
                    node['parameters'].update(customizations['node_params'][node_id])
        
        return workflow

# Global template manager instance
template_manager = WorkflowTemplateManager()

# Global convenience functions
def get_all_templates() -> List[WorkflowTemplate]:
    """Get all available templates"""
    return template_manager.get_all_templates()

def get_template(template_id: str) -> Optional[WorkflowTemplate]:
    """Get a specific template by ID"""
    return template_manager.get_template(template_id)

def get_template_suggestions(description: str) -> List[WorkflowTemplate]:
    """Get template suggestions based on description"""
    return template_manager.get_template_suggestions(description)

def customize_template(template_id: str, customizations: Dict[str, Any]) -> Dict[str, Any]:
    """Customize a template with user-specific parameters"""
    return template_manager.customize_template(template_id, customizations)