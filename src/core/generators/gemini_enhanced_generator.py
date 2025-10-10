#!/usr/bin/env python3
"""
Gemini AI Enhanced Generator that combines Gemini AI with 100 real n8n workflows knowledge
This creates the most powerful workflow generation system possible.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path
import requests
import time

logger = logging.getLogger(__name__)

class GeminiEnhancedGenerator:
    """
    Combines Gemini AI with knowledge from 100 real n8n workflows
    for the most accurate and intelligent workflow generation
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model = "gemini-2.5-flash"  # Use latest available model (without models/ prefix)
        self.base_url = "https://generativelanguage.googleapis.com/v1"
        
        # Load 100 workflows knowledge
        self.workflow_patterns = self._load_workflow_patterns()
        self.ai_patterns = self._load_ai_patterns()
        self.statistics = self._load_statistics()
        self.node_sequences = self._load_node_sequences()
        
        logger.info(f"Gemini Enhanced Generator initialized with {len(self.workflow_patterns)} real workflow patterns")
    
    def _load_workflow_patterns(self) -> List[Dict[str, Any]]:
        """Load actual patterns from 100 workflows"""
        try:
            with open('training_data/workflow_patterns.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load workflow patterns: {e}")
            return []
    
    def _load_ai_patterns(self) -> List[Dict[str, Any]]:
        """Load AI integration patterns"""
        try:
            with open('training_data/ai_integration_patterns.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load AI patterns: {e}")
            return []
    
    def _load_statistics(self) -> Dict[str, Any]:
        """Load workflow statistics"""
        try:
            with open('training_data/statistics.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load statistics: {e}")
            return {}
    
    def _load_node_sequences(self) -> Dict[str, Any]:
        """Load common node sequences"""
        try:
            with open('training_data/node_sequences.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Could not load node sequences: {e}")
            return {}
    
    def generate_workflow(self, description: str, trigger_type: str = 'webhook', 
                         complexity: str = 'medium') -> Dict[str, Any]:
        """
        Generate workflow using Gemini AI enhanced with 100 real workflows knowledge
        """
        print(f"🤖 Gemini Enhanced: Combining AI with knowledge from {len(self.workflow_patterns)} real workflows")
        
        # 1. Find relevant patterns from 100 real workflows
        relevant_patterns = self._find_relevant_patterns(description, trigger_type)
        
        # 2. Create enhanced prompt with real workflow knowledge
        enhanced_prompt = self._create_knowledge_enhanced_prompt(
            description, trigger_type, complexity, relevant_patterns
        )
        
        # 3. Generate with Gemini AI
        try:
            workflow = self._generate_with_gemini(enhanced_prompt)
            
            # 4. Post-process with real workflow insights
            workflow = self._apply_real_workflow_insights(workflow, relevant_patterns)
            
            # 5. Add metadata about knowledge usage
            workflow['meta'] = {
                'ai_provider': 'gemini',
                'knowledge_source': '100_real_workflows',
                'patterns_used': len(relevant_patterns),
                'pattern_names': [p.get('name', 'Unnamed') for p in relevant_patterns[:3]]
            }
            
            print(f"✅ Gemini Enhanced: Generated workflow using {len(relevant_patterns)} real patterns")
            return workflow
            
        except Exception as e:
            logger.error(f"Gemini Enhanced generation failed: {e}")
            # Fallback to pattern-based generation
            return self._fallback_pattern_generation(description, trigger_type, complexity, relevant_patterns)
    
    def _find_relevant_patterns(self, description: str, trigger_type: str = None) -> List[Dict[str, Any]]:
        """Find most relevant patterns from 100 real workflows"""
        description_lower = description.lower()
        scored_patterns = []
        
        for pattern in self.workflow_patterns:
            score = 0
            
            # Score by category match
            category = pattern.get('category', '').lower()
            if any(word in description_lower for word in category.split()):
                score += 10
            
            # Score by workflow name
            name = pattern.get('name', '').lower()
            name_words = name.split()
            for word in name_words:
                if word in description_lower:
                    score += 5
            
            # Score by node types
            processing = pattern.get('processing_pattern', [])
            for node_type in processing:
                node_name = node_type.replace('n8n-nodes-base.', '').replace('@n8n/n8n-nodes-langchain.', '')
                if node_name.lower() in description_lower:
                    score += 3
            
            # Score by trigger type match
            if trigger_type and pattern.get('trigger_type') == trigger_type:
                score += 5
            
            if score > 0:
                scored_patterns.append((pattern, score))
        
        # Sort by score and return top patterns
        scored_patterns.sort(key=lambda x: x[1], reverse=True)
        top_patterns = [pattern for pattern, score in scored_patterns[:5]]
        
        if top_patterns:
            print(f"📊 Found {len(top_patterns)} relevant patterns from real workflows")
            for i, pattern in enumerate(top_patterns[:3], 1):
                print(f"   {i}. {pattern.get('name', 'Unnamed')} (category: {pattern.get('category', 'N/A')})")
        
        return top_patterns
    
    def _create_knowledge_enhanced_prompt(self, description: str, trigger_type: str, 
                                        complexity: str, patterns: List[Dict[str, Any]]) -> str:
        """Create Gemini prompt enhanced with real workflow knowledge"""
        
        # Extract insights from real patterns
        common_nodes = self._extract_common_nodes(patterns)
        common_sequences = self._extract_common_sequences(patterns)
        best_practices = self._extract_best_practices(patterns)
        
        # Create a very concise prompt to avoid token limits
        node_types = list(common_nodes.keys())[:3] if common_nodes else []
        clean_nodes = [node.replace('n8n-nodes-base.', '') for node in node_types]
        
        prompt = f"""Create n8n workflow JSON for: {description}
Trigger: {trigger_type}, Complexity: {complexity}
Use nodes: {', '.join(clean_nodes[:3])}

Return only JSON:
{{
  "name": "Workflow Name",
  "nodes": [
    {{"id": "trigger", "name": "Trigger", "type": "n8n-nodes-base.{trigger_type}", "position": [100, 100], "parameters": {{}}}},
    {{"id": "process", "name": "Process", "type": "n8n-nodes-base.set", "position": [300, 100], "parameters": {{}}}}
  ],
  "connections": {{"Trigger": {{"main": [[{{"node": "Process", "type": "main", "index": 0}}]]}}}},
  "active": true
}}"""
        
        return prompt
    
    def _extract_common_nodes(self, patterns: List[Dict[str, Any]]) -> Dict[str, int]:
        """Extract most common node types from patterns"""
        node_counts = {}
        for pattern in patterns:
            for node_type in pattern.get('processing_pattern', []):
                node_counts[node_type] = node_counts.get(node_type, 0) + 1
        return dict(sorted(node_counts.items(), key=lambda x: x[1], reverse=True)[:10])
    
    def _extract_common_sequences(self, patterns: List[Dict[str, Any]]) -> List[List[str]]:
        """Extract common node sequences from patterns"""
        sequences = []
        for pattern in patterns:
            processing = pattern.get('processing_pattern', [])
            if len(processing) >= 2:
                sequences.append(processing[:3])  # Take first 3 nodes as sequence
        return sequences[:5]
    
    def _extract_best_practices(self, patterns: List[Dict[str, Any]]) -> List[str]:
        """Extract best practices from real workflows"""
        practices = []
        
        # Analyze patterns for best practices
        has_error_handling = sum(1 for p in patterns if any('error' in node.lower() for node in p.get('processing_pattern', [])))
        has_validation = sum(1 for p in patterns if any('validate' in node.lower() or 'check' in node.lower() for node in p.get('processing_pattern', [])))
        
        if has_error_handling > len(patterns) * 0.3:
            practices.append("Include error handling nodes (used in 30%+ of real workflows)")
        
        if has_validation > len(patterns) * 0.2:
            practices.append("Add data validation steps (common in production workflows)")
        
        practices.append("Use descriptive node names for maintainability")
        practices.append("Follow the trigger -> process -> output pattern")
        
        return practices
    
    def _format_node_insights(self, nodes: Dict[str, int]) -> str:
        """Format node insights for prompt"""
        if not nodes:
            return "No specific node patterns found"
        
        formatted = []
        for node_type, count in list(nodes.items())[:5]:
            clean_name = node_type.replace('n8n-nodes-base.', '').replace('@n8n/n8n-nodes-langchain.', '')
            formatted.append(f"- {clean_name}: Used in {count} real workflows")
        
        return "\n".join(formatted)
    
    def _format_sequence_insights(self, sequences: List[List[str]]) -> str:
        """Format sequence insights for prompt"""
        if not sequences:
            return "No specific sequences found"
        
        formatted = []
        for i, sequence in enumerate(sequences[:3], 1):
            clean_sequence = [node.replace('n8n-nodes-base.', '').replace('@n8n/n8n-nodes-langchain.', '') for node in sequence]
            formatted.append(f"{i}. {' -> '.join(clean_sequence)}")
        
        return "\n".join(formatted)
    
    def _format_best_practices(self, practices: List[str]) -> str:
        """Format best practices for prompt"""
        return "\n".join(f"- {practice}" for practice in practices)
    
    def _format_pattern_examples(self, patterns: List[Dict[str, Any]]) -> str:
        """Format pattern examples for prompt"""
        if not patterns:
            return "No similar patterns found"
        
        formatted = []
        for i, pattern in enumerate(patterns, 1):
            name = pattern.get('name', 'Unnamed')
            category = pattern.get('category', 'N/A')
            nodes = len(pattern.get('processing_pattern', []))
            formatted.append(f"{i}. {name} (Category: {category}, Nodes: {nodes})")
        
        return "\n".join(formatted)
    
    def _generate_with_gemini(self, prompt: str) -> Dict[str, Any]:
        """Generate workflow using Gemini AI"""
        headers = {"Content-Type": "application/json"}
        url = f"{self.base_url}/models/{self.model}:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.3,
                "topK": 40,
                "topP": 0.8,
                "maxOutputTokens": 8192  # Higher limit to account for internal thoughts
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        
        if response.status_code != 200:
            logger.error(f"Gemini API error {response.status_code}: {response.text}")
            raise ValueError(f"Gemini API returned {response.status_code}: {response.text[:200]}")
        
        response.raise_for_status()
        
        data = response.json()
        
        # Check if response was truncated
        candidate = data["candidates"][0]
        finish_reason = candidate.get("finishReason", "")
        
        if finish_reason == "MAX_TOKENS":
            logger.warning("Gemini response was truncated due to token limit")
            raise ValueError("Response truncated - try simpler prompt")
        
        content = candidate["content"]["parts"][0]["text"]
        
        # Clean and parse JSON
        content = content.strip()
        if content.startswith('```json'):
            content = content[7:]
        if content.endswith('```'):
            content = content[:-3]
        
        # Handle incomplete JSON due to truncation
        if not content.endswith('}'):
            logger.warning("JSON appears incomplete, attempting to fix")
            # Try to close the JSON properly
            open_braces = content.count('{') - content.count('}')
            content += '}' * open_braces
        
        try:
            workflow = json.loads(content)
            return workflow
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {e}")
            logger.error(f"Response content: {content[:500]}...")
            raise ValueError("Gemini returned invalid JSON")
    
    def _apply_real_workflow_insights(self, workflow: Dict[str, Any], patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Apply insights from real workflows to improve the generated workflow"""
        
        # Ensure proper node IDs and positions
        nodes = workflow.get('nodes', [])
        for i, node in enumerate(nodes):
            if 'id' not in node:
                node['id'] = f"node_{i}"
            if 'position' not in node:
                node['position'] = [100 + i * 200, 100]
        
        # Ensure proper connections exist
        if 'connections' not in workflow:
            workflow['connections'] = {}
        
        # Add missing workflow properties based on real workflows
        if 'active' not in workflow:
            workflow['active'] = True
        if 'settings' not in workflow:
            workflow['settings'] = {}
        if 'staticData' not in workflow:
            workflow['staticData'] = {}
        
        return workflow
    
    def _fallback_pattern_generation(self, description: str, trigger_type: str, 
                                   complexity: str, patterns: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Fallback generation using patterns when Gemini fails"""
        print("🔄 Falling back to pattern-based generation")
        
        if not patterns:
            # Create basic workflow
            return self._create_basic_workflow(description, trigger_type)
        
        # Use the best matching pattern
        best_pattern = patterns[0]
        
        # Create workflow based on pattern
        workflow = {
            "name": f"{description[:50]}...",
            "nodes": self._create_nodes_from_pattern(best_pattern, trigger_type),
            "connections": {},
            "active": True,
            "settings": {},
            "staticData": {},
            "meta": {
                "ai_provider": "pattern_fallback",
                "knowledge_source": "100_real_workflows",
                "pattern_used": best_pattern.get('name', 'Unnamed')
            }
        }
        
        # Create connections
        nodes = workflow['nodes']
        if len(nodes) > 1:
            for i in range(len(nodes) - 1):
                source_name = nodes[i]['name']
                target_name = nodes[i + 1]['name']
                workflow['connections'][source_name] = {
                    "main": [[{"node": target_name, "type": "main", "index": 0}]]
                }
        
        return workflow
    
    def _create_nodes_from_pattern(self, pattern: Dict[str, Any], trigger_type: str) -> List[Dict[str, Any]]:
        """Create nodes based on real workflow pattern"""
        nodes = []
        processing_pattern = pattern.get('processing_pattern', [])
        
        # Create trigger node
        trigger_node = {
            "id": "trigger",
            "name": f"{trigger_type.title()} Trigger",
            "type": f"n8n-nodes-base.{trigger_type}",
            "position": [100, 100],
            "parameters": {}
        }
        nodes.append(trigger_node)
        
        # Create processing nodes based on pattern
        for i, node_type in enumerate(processing_pattern[:4], 1):  # Limit to 4 processing nodes
            clean_name = node_type.replace('n8n-nodes-base.', '').replace('@n8n/n8n-nodes-langchain.', '')
            node = {
                "id": f"node_{i}",
                "name": clean_name.title().replace('_', ' '),
                "type": node_type,
                "position": [100 + i * 200, 100],
                "parameters": {}
            }
            nodes.append(node)
        
        return nodes
    
    def _create_basic_workflow(self, description: str, trigger_type: str) -> Dict[str, Any]:
        """Create basic workflow when no patterns available"""
        return {
            "name": f"Basic {description[:30]}",
            "nodes": [
                {
                    "id": "trigger",
                    "name": f"{trigger_type.title()} Trigger",
                    "type": f"n8n-nodes-base.{trigger_type}",
                    "position": [100, 100],
                    "parameters": {}
                },
                {
                    "id": "process",
                    "name": "Process Data",
                    "type": "n8n-nodes-base.set",
                    "position": [300, 100],
                    "parameters": {}
                }
            ],
            "connections": {
                f"{trigger_type.title()} Trigger": {
                    "main": [[{"node": "Process Data", "type": "main", "index": 0}]]
                }
            },
            "active": True,
            "settings": {},
            "staticData": {},
            "meta": {
                "ai_provider": "basic_fallback",
                "knowledge_source": "none"
            }
        }

# Global function for integration
def generate_gemini_enhanced_workflow(description: str, trigger_type: str = 'webhook', 
                                    complexity: str = 'medium', api_key: str = None) -> Dict[str, Any]:
    """Generate workflow using Gemini AI enhanced with 100 real workflows knowledge"""
    
    if not api_key:
        # Try to get from environment or config
        import os
        api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            try:
                from config import config
                api_key = config.GEMINI_API_KEY
            except:
                pass
    
    if not api_key:
        raise ValueError("Gemini API key not available")
    
    generator = GeminiEnhancedGenerator(api_key)
    return generator.generate_workflow(description, trigger_type, complexity)