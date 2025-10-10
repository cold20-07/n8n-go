#!/usr/bin/env python3
"""
Interactive Prompt Assistant for N8N Go
Breaks down complex requests and guides users with yes/no questions
"""

import json
import re
from typing import Dict, List, Any, Optional

class InteractivePromptAssistant:
    def __init__(self):
        self.conversation_state = {
            'current_step': 0,
            'workflow_plan': {},
            'user_responses': {},
            'clarifications_needed': []
        }
        
        # Common workflow patterns and their breakdown
        self.workflow_patterns = {
            'data_processing': {
                'name': 'Data Processing Workflow',
                'steps': [
                    'Get data from source',
                    'Transform/process the data',
                    'Save results to destination'
                ],
                'questions': [
                    'Do you want to process data from files, APIs, or databases?',
                    'Do you need to filter, transform, or analyze this data?',
                    'Do you want to save the results to a file, database, or email?'
                ]
            },
            'automation': {
                'name': 'Business Process Automation',
                'steps': [
                    'Trigger when event occurs',
                    'Check conditions/rules',
                    'Execute actions',
                    'Send notifications'
                ],
                'questions': [
                    'Do you want this to run on a schedule, manually, or when something specific happens?',
                    'Do you need to check certain conditions before taking action?',
                    'Do you need to notify someone when this completes?'
                ]
            },
            'integration': {
                'name': 'System Integration',
                'steps': [
                    'Connect first system',
                    'Get data from source',
                    'Transform data format',
                    'Send to destination system'
                ],
                'questions': [
                    'Do you want to connect two different applications or services?',
                    'Do you need to sync data between systems regularly?',
                    'Do you use different data formats that need conversion?'
                ]
            }
        }
        
        # Keywords for pattern detection
        self.keywords = {
            'data_processing': ['data', 'file', 'excel', 'csv', 'transform', 'analyze', 'process', 'filter'],
            'automation': ['automate', 'trigger', 'schedule', 'when', 'if', 'notify', 'email', 'slack'],
            'integration': ['connect', 'sync', 'api', 'webhook', 'integrate', 'between', 'from', 'to']
        }
    
    def analyze_user_request(self, user_input: str) -> Dict[str, Any]:
        """Analyze user input and determine best workflow pattern"""
        user_input_lower = user_input.lower()
        
        # Score each pattern
        pattern_scores = {}
        for pattern, keywords in self.keywords.items():
            score = sum(1 for keyword in keywords if keyword in user_input_lower)
            pattern_scores[pattern] = score
        
        # Get the best matching pattern
        best_pattern = max(pattern_scores, key=pattern_scores.get)
        confidence = pattern_scores[best_pattern] / len(self.keywords[best_pattern])
        
        return {
            'suggested_pattern': best_pattern,
            'confidence': confidence,
            'pattern_scores': pattern_scores,
            'all_scores': pattern_scores
        }
    
    def create_workflow_plan(self, pattern_type: str, user_input: str) -> Dict[str, Any]:
        """Create a detailed workflow plan based on the pattern"""
        pattern = self.workflow_patterns[pattern_type]
        
        plan = {
            'workflow_name': pattern['name'],
            'description': f"Based on your request: '{user_input}'",
            'steps': pattern['steps'].copy(),
            'questions_to_clarify': pattern['questions'].copy(),
            'complexity': 'Medium',
            'estimated_nodes': len(pattern['steps']) + 2,  # +2 for trigger and end
            'confidence': 0.8
        }
        
        # Adjust complexity based on input length and keywords
        if len(user_input.split()) > 20:
            plan['complexity'] = 'High'
            plan['estimated_nodes'] += 3
        elif len(user_input.split()) < 10:
            plan['complexity'] = 'Simple'
            plan['estimated_nodes'] -= 1
        
        return plan
    
    def present_plan_to_user(self, plan: Dict[str, Any]) -> str:
        """Present the workflow plan in a user-friendly format"""
        response = f"""
🎯 **I understand you want to create: {plan['workflow_name']}**

📋 **Here's my plan for your workflow:**

**Description:** {plan['description']}
**Estimated Complexity:** {plan['complexity']}
**Estimated Nodes:** {plan['estimated_nodes']}

**Steps I'll include:**
"""
        
        for i, step in enumerate(plan['steps'], 1):
            response += f"{i}. {step}\n"
        
        response += f"""
❓ **Does this plan match what you want to achieve?**

- Type 'YES' if this looks right
- Type 'NO' if you need something different
(If NO, please tell me what you need instead)
"""
        
        return response
    
    def ask_clarification_questions(self, plan: Dict[str, Any], question_index: int = 0) -> str:
        """Ask clarification questions one by one"""
        if question_index >= len(plan['questions_to_clarify']):
            return self.generate_final_workflow_summary()
        
        question = plan['questions_to_clarify'][question_index]
        
        response = f"""
❓ **Question {question_index + 1} of {len(plan['questions_to_clarify'])}:**

{question}

**Please answer YES or NO**
(Type 'YES' if this applies to your workflow)
"""
        
        return response
    
    def process_user_response(self, user_response: str, context: str = "plan_approval") -> Dict[str, Any]:
        """Process user's yes/no response and determine next action"""
        user_response_clean = user_response.strip().lower()
        
        result = {
            'response_type': 'unknown',
            'next_action': 'clarify',
            'needs_clarification': False,
            'message': ''
        }
        
        # Check for yes/no responses
        if any(word in user_response_clean for word in ['yes', 'y', 'correct', 'right', 'good']):
            result['response_type'] = 'yes'
            if context == "plan_approval":
                result['next_action'] = 'ask_details'
                result['message'] = "Great! Let me ask a few questions to customize your workflow:"
            else:
                result['next_action'] = 'next_question'
                result['message'] = "Perfect! Moving to the next question:"
        elif any(word in user_response_clean for word in ['no', 'n', 'wrong', 'different']):
            result['response_type'] = 'no'
            result['next_action'] = 'clarify'
            result['needs_clarification'] = True
            result['message'] = "I understand, and this isn't quite right. Could you tell me what you need instead?"
        else:
            result['response_type'] = 'unclear'
            result['next_action'] = 'clarify'
            result['needs_clarification'] = True
            result['message'] = "I'm not sure if that's a yes or no. Could you please respond with 'YES' or 'NO'?"
        
        return result
    
    def continue_conversation(self, user_response: str, current_context: str) -> str:
        """Continue the conversation based on current context"""
        if current_context == "plan_approval":
            response_analysis = self.process_user_response(user_response, "plan_approval")
            
            if response_analysis['response_type'] == 'yes':
                # Start asking detailed questions
                plan = self.conversation_state.get('workflow_plan', {})
                return self.ask_clarification_questions(plan, 0)
            else:
                return "I understand. Could you tell me specifically what you'd like to change about the plan?"
        
        elif current_context == "clarification_questions":
            current_step = self.conversation_state.get('current_step', 0)
            plan = self.conversation_state.get('workflow_plan', {})
            
            # Store the response
            self.conversation_state['user_responses'][current_step] = user_response
            
            # Move to next question
            self.conversation_state['current_step'] += 1
            
            if current_step < len(plan.get('questions_to_clarify', [])):
                return self.ask_clarification_questions(plan, current_step + 1)
            else:
                # All questions answered
                return self.generate_final_workflow_summary()
        
        return "I'm not sure how to help with that. Could you clarify what you need?"
    
    def generate_final_workflow_summary(self) -> str:
        """Generate final workflow summary"""
        plan = self.conversation_state.get('workflow_plan', {})
        responses = self.conversation_state.get('user_responses', {})
        
        summary = f"""
✅ **Workflow Configuration Complete!**

**Workflow Type:** {plan.get('workflow_name', 'Custom Workflow')}
**Complexity:** {plan.get('complexity', 'Medium')}

**Your Preferences:**
"""
        
        for i, (question, answer) in enumerate(responses.items(), 1):
            summary += f"{i}. {question} → {answer}\n"
        
        summary += """
🚀 **Ready to Generate Your Workflow!**

Would you like me to:
1. Generate the workflow now (type 'GENERATE')
2. Make changes to the plan (type 'MODIFY')
3. Start over with a different approach (type 'RESTART')
"""
        
        return summary
    
    def handle_complex_request(self, user_input: str) -> str:
        """Main method to handle complex user requests"""
        # Step 1: Analyze the request
        analysis = self.analyze_user_request(user_input)
        
        # Step 2: Create a workflow plan
        if analysis['confidence'] > 0.3:
            plan = self.create_workflow_plan(analysis['suggested_pattern'], user_input)
            self.conversation_state['workflow_plan'] = plan
            return self.present_plan_to_user(plan)
        else:
            # Step 3: Ask basic clarification
            return self.ask_for_basic_clarification(user_input)
    
    def ask_for_basic_clarification(self, user_input: str) -> str:
        """Ask basic clarification when we can't determine the workflow type"""
        return f"""
🤔 **I want to help you create the perfect workflow!**

I see you mentioned: *{user_input}*

To better understand what you need, could you tell me which of these best describes your goal:

**A) Data Processing** - Process, analyze, or transform data from files/databases
**B) Business Automation** - Automate repetitive tasks or business processes  
**C) System Integration** - Connect different systems or sync data between systems
**D) Something else**

**Please answer A, B, C, or D**
(If D, please let me know what you have in mind)
"""

def demo_interactive_assistant():
    """Demonstrate the interactive assistant"""
    print("🤖 Interactive Prompt Assistant Demo")
    print("=" * 50)
    
    assistant = InteractivePromptAssistant()
    
    # Test cases
    test_requests = [
        "I want to process CSV files and send results via email",
        "Connect Google Sheets to Slack for daily reports",
        "Automate something with data"
    ]
    
    for i, request in enumerate(test_requests, 1):
        print(f"\n📝 Test Case {i}:")
        print(f"Request: '{request}'")
        print("-" * 30)
        response = assistant.handle_complex_request(request)
        print(response)

if __name__ == "__main__":
    demo_interactive_assistant()