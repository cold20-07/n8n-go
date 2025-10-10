"""
AI Enhancement Layer for N8N Workflow Generator
Multi-model support with intelligent fallbacks and caching
"""
import json
import hashlib
import time
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import requests

class AIProvider(Enum):
    """Supported AI providers"""
    GEMINI = "gemini"
    OPENAI = "openai"
    CLAUDE = "claude"
    OLLAMA = "ollama"  # Local models

@dataclass
class AIResponse:
    """Standardized AI response"""
    content: str
    provider: AIProvider
    model: str
    tokens_used: int
    response_time: float
    cached: bool = False

class AIProviderInterface(ABC):
    """Abstract interface for AI providers"""
    
    @abstractmethod
    def generate_workflow(self, prompt: str, context: Dict[str, Any]) -> AIResponse:
        """Generate workflow using AI provider"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available"""
        pass
    
    @abstractmethod
    def get_cost_estimate(self, prompt: str) -> float:
        """Estimate cost for the request"""
        pass

class GeminiProvider(AIProviderInterface):
    """Google Gemini AI provider"""
    
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"
    
    def generate_workflow(self, prompt: str, context: Dict[str, Any]) -> AIResponse:
        start_time = time.time()
        
        headers = {"Content-Type": "application/json"}
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": self._create_enhanced_prompt(prompt, context)}]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "topK": 40,
                "topP": 0.95,
                "maxOutputTokens": 2048
            }
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        content = data["candidates"][0]["content"]["parts"][0]["text"]
        
        return AIResponse(
            content=content,
            provider=AIProvider.GEMINI,
            model=self.model,
            tokens_used=self._estimate_tokens(content),
            response_time=time.time() - start_time
        )
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def get_cost_estimate(self, prompt: str) -> float:
        # Gemini pricing estimation
        tokens = self._estimate_tokens(prompt)
        return tokens * 0.00025  # Approximate cost per token
    
    def _create_enhanced_prompt(self, description: str, context: Dict[str, Any]) -> str:
        """Create enhanced prompt with context"""
        return f"""
        You are an expert n8n workflow designer. Create a production-ready n8n workflow.
        
        **User Request:** {description}
        
        **Context:**
        - Trigger Type: {context.get('trigger', 'webhook')}
        - Complexity: {context.get('complexity', 'medium')}
        - Industry: {context.get('industry', 'general')}
        - Use Case: {context.get('use_case', 'automation')}
        
        **Requirements:**
        1. Follow n8n JSON format exactly
        2. Include proper error handling
        3. Use descriptive node names
        4. Optimize for performance
        5. Add appropriate node parameters
        6. Ensure proper node connections
        
        **Output Format:**
        Return ONLY valid n8n workflow JSON. No explanations or markdown.
        
        Example structure:
        {{
          "name": "Descriptive Workflow Name",
          "nodes": [...],
          "connections": {{...}},
          "active": true,
          "settings": {{...}}
        }}
        """
    
    def _estimate_tokens(self, text: str) -> int:
        """Estimate token count"""
        return len(text.split()) * 1.3  # Rough estimation

class OpenAIProvider(AIProviderInterface):
    """OpenAI GPT provider"""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1"
    
    def generate_workflow(self, prompt: str, context: Dict[str, Any]) -> AIResponse:
        start_time = time.time()
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert n8n workflow designer. Create production-ready workflows in valid n8n JSON format."
                },
                {
                    "role": "user", 
                    "content": self._create_enhanced_prompt(prompt, context)
                }
            ],
            "temperature": 0.7,
            "max_tokens": 2048
        }
        
        response = requests.post(f"{self.base_url}/chat/completions", 
                               headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        
        return AIResponse(
            content=content,
            provider=AIProvider.OPENAI,
            model=self.model,
            tokens_used=data["usage"]["total_tokens"],
            response_time=time.time() - start_time
        )
    
    def is_available(self) -> bool:
        return bool(self.api_key)
    
    def get_cost_estimate(self, prompt: str) -> float:
        tokens = self._estimate_tokens(prompt)
        if "gpt-4" in self.model:
            return tokens * 0.03 / 1000  # GPT-4 pricing
        else:
            return tokens * 0.002 / 1000  # GPT-3.5 pricing
    
    def _create_enhanced_prompt(self, description: str, context: Dict[str, Any]) -> str:
        return f"""
        Create an n8n workflow for: {description}
        
        Context: {json.dumps(context, indent=2)}
        
        Requirements:
        - Valid n8n JSON format
        - Include error handling nodes
        - Use appropriate node types
        - Optimize connections
        - Add descriptive names
        
        Return only the JSON workflow, no explanations.
        """
    
    def _estimate_tokens(self, text: str) -> int:
        return len(text.split()) * 1.3

class AIOrchestrator:
    """Orchestrates multiple AI providers with intelligent routing"""
    
    def __init__(self):
        self.providers = {}
        self.cache = {}
        self.usage_stats = {}
        self.fallback_order = [
            AIProvider.GEMINI,
            AIProvider.OPENAI,
            AIProvider.CLAUDE,
            AIProvider.OLLAMA
        ]
    
    def register_provider(self, provider: AIProviderInterface, provider_type: AIProvider):
        """Register an AI provider"""
        self.providers[provider_type] = provider
        self.usage_stats[provider_type] = {
            'requests': 0,
            'successes': 0,
            'failures': 0,
            'total_cost': 0.0,
            'avg_response_time': 0.0
        }
    
    def generate_workflow(self, description: str, context: Dict[str, Any]) -> AIResponse:
        """Generate workflow using best available provider"""
        
        # Check Redis cache first
        try:
            from src.core.cache import get_cache
            cache = get_cache()
            cache_key = cache._generate_key("ai_workflow", description, context.get('trigger_type', ''), context.get('complexity', ''))
            
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                cached_response.cached = True
                return cached_response
        except Exception as e:
            print(f"Cache lookup failed: {e}")
        
        # Fallback to in-memory cache
        cache_key = self._get_cache_key(description, context)
        if cache_key in self.cache:
            cached_response = self.cache[cache_key]
            cached_response.cached = True
            return cached_response
        
        # Try providers in order of preference
        last_error = None
        
        for provider_type in self.fallback_order:
            if provider_type not in self.providers:
                continue
            
            provider = self.providers[provider_type]
            
            if not provider.is_available():
                continue
            
            try:
                # Check cost before making request
                estimated_cost = provider.get_cost_estimate(description)
                if estimated_cost > 1.0:  # Cost threshold
                    print(f"⚠️ High cost estimate for {provider_type}: ${estimated_cost:.4f}")
                
                response = provider.generate_workflow(description, context)
                
                # Update stats
                self._update_stats(provider_type, True, estimated_cost, response.response_time)
                
                # Cache successful response in Redis
                try:
                    from src.core.cache import get_cache
                    cache = get_cache()
                    redis_cache_key = cache._generate_key("ai_workflow", description, context.get('trigger_type', ''), context.get('complexity', ''))
                    cache.set(redis_cache_key, response, 3600)  # 1 hour TTL
                except Exception as e:
                    print(f"Redis cache failed: {e}")
                
                # Fallback to in-memory cache
                self.cache[cache_key] = response
                
                return response
                
            except Exception as e:
                last_error = e
                self._update_stats(provider_type, False, 0, 0)
                print(f"❌ {provider_type} failed: {e}")
                continue
        
        # All providers failed
        raise Exception(f"All AI providers failed. Last error: {last_error}")
    
    def get_provider_stats(self) -> Dict[str, Any]:
        """Get usage statistics for all providers"""
        return self.usage_stats
    
    def clear_cache(self):
        """Clear the response cache"""
        self.cache.clear()
    
    def _get_cache_key(self, description: str, context: Dict[str, Any]) -> str:
        """Generate cache key for request"""
        data = f"{description}:{json.dumps(context, sort_keys=True)}"
        return hashlib.md5(data.encode()).hexdigest()
    
    def _update_stats(self, provider_type: AIProvider, success: bool, cost: float, response_time: float):
        """Update provider statistics"""
        stats = self.usage_stats[provider_type]
        stats['requests'] += 1
        
        if success:
            stats['successes'] += 1
            stats['total_cost'] += cost
            
            # Update average response time
            current_avg = stats['avg_response_time']
            stats['avg_response_time'] = (current_avg + response_time) / 2
        else:
            stats['failures'] += 1

class WorkflowEnhancer:
    """Enhance generated workflows with AI-powered improvements"""
    
    def __init__(self, ai_orchestrator: AIOrchestrator):
        self.ai = ai_orchestrator
    
    def enhance_workflow(self, workflow: Dict[str, Any], enhancement_type: str) -> Dict[str, Any]:
        """Enhance workflow with specific improvements"""
        
        enhancements = {
            'error_handling': self._add_error_handling,
            'performance': self._optimize_performance,
            'security': self._add_security_features,
            'monitoring': self._add_monitoring,
            'documentation': self._add_documentation
        }
        
        if enhancement_type in enhancements:
            return enhancements[enhancement_type](workflow)
        
        return workflow
    
    def _add_error_handling(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Add error handling nodes to workflow"""
        # Implementation for adding error handling
        return workflow
    
    def _optimize_performance(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Optimize workflow for performance"""
        # Implementation for performance optimization
        return workflow
    
    def _add_security_features(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Add security features to workflow"""
        # Implementation for security enhancements
        return workflow
    
    def _add_monitoring(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Add monitoring and logging nodes"""
        # Implementation for monitoring
        return workflow
    
    def _add_documentation(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Add documentation and comments"""
        # Implementation for documentation
        return workflow

# Usage example
def setup_ai_system():
    """Setup enhanced AI system"""
    import os
    orchestrator = AIOrchestrator()
    
    # Register providers using environment variables
    gemini_key = os.getenv('GEMINI_API_KEY')
    if gemini_key and gemini_key != 'your-gemini-api-key-here':
        orchestrator.register_provider(
            GeminiProvider(gemini_key),
            AIProvider.GEMINI
        )
    
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key and openai_key != 'your-openai-api-key-here':
        orchestrator.register_provider(
            OpenAIProvider(openai_key),
            AIProvider.OPENAI
        )
    
    return orchestrator

# Integration with existing app
def generate_enhanced_workflow(description: str, trigger: str, complexity: str) -> Dict[str, Any]:
    """Generate workflow using enhanced AI system"""
    
    orchestrator = setup_ai_system()
    enhancer = WorkflowEnhancer(orchestrator)
    
    context = {
        'trigger': trigger,
        'complexity': complexity,
        'timestamp': time.time(),
        'version': '2.0'
    }
    
    try:
        # Generate base workflow
        ai_response = orchestrator.generate_workflow(description, context)
        workflow = json.loads(ai_response.content)
        
        # Enhance workflow
        enhanced_workflow = enhancer.enhance_workflow(workflow, 'error_handling')
        enhanced_workflow = enhancer.enhance_workflow(enhanced_workflow, 'performance')
        
        return enhanced_workflow
        
    except Exception as e:
        print(f"❌ Enhanced AI generation failed: {e}")
        # Fallback to existing system
        from app import create_basic_workflow
        return create_basic_workflow(description, trigger, complexity)

if __name__ == "__main__":
    # Test the enhanced AI system
    test_description = "Process customer emails and send automated responses"
    test_context = {
        'trigger': 'webhook',
        'complexity': 'medium',
        'industry': 'customer_service'
    }
    
    orchestrator = setup_ai_system()
    
    if orchestrator.providers:
        try:
            response = orchestrator.generate_workflow(test_description, test_context)
            print(f"✅ AI generation successful using {response.provider}")
            print(f"   Response time: {response.response_time:.2f}s")
            print(f"   Tokens used: {response.tokens_used}")
        except Exception as e:
            print(f"❌ AI generation failed: {e}")
    else:
        print("⚠️ No AI providers configured")