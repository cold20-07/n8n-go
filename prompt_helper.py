#!/usr/bin/env python3
"""
Prompt Helper for N8N Go - Breaks down complex requests into simple yes/no questions
"""

class PromptHelper:
    def __init__(self):
        self.workflow_patterns = {
            'data_processing': {
                'name': 'Data Processing Workflow',
                'steps': ['Get data', 'Process data', 'Save results'],
                'questions': [
                    'Do you want to work with files (CSV, Excel, JSON)?',
                    'Do you need to filter or transform the data?',
                    'Do you want to save results to a file or database?'
                ]
            },
            'automation': {
                'name': 'Automation Workflow', 
                'steps': ['Trigger event', 'Check conditions', 'Take action'],
                'questions': [
                    'Do you want this to run automatically on a schedule?',
                    'Do you need to check certain conditions first?',
                    'Do you want to send notifications when done?'
                ]
            },
            'integration': {
                'name': 'Integration Workflow',
                'steps': ['Connect systems', 'Sync data', 'Handle responses'],
                'questions': [
                    'Do you want to connect two different apps/services?',
                    'Do you need to sync data between them regularly?',
                    'Do you want real-time updates or scheduled sync?'
                ]
            }
        }
    
    def analyze_request(self, user_input):
        """Analyze user input and suggest workflow type"""
        keywords = {
            'data_processing': ['csv', 'excel', 'data', 'file', 'process', 'analyze'],
            'automation': ['automate', 'schedule', 'daily', 'weekly', 'trigger'],
            'integration': ['connect', 'sync', 'api', 'slack', 'sheets', 'between']
        }
        
        scores = {}
        for pattern, words in keywords.items():
            score = sum(1 for word in words if word in user_input.lower())
            scores[pattern] = score
        
        best_match = max(scores, key=scores.get)
        return best_match if scores[best_match] > 0 else 'automation'
    
    def create_plan(self, pattern_type, user_input):
        """Create a simple plan for the user"""
        pattern = self.workflow_patterns[pattern_type]
        
        plan = f"""
🎯 **I think you want: {pattern['name']}**

📋 **Here's what I'll create:**
"""
        for i, step in enumerate(pattern['steps'], 1):
            plan += f"{i}. {step}\n"
        
        plan += f"""
❓ **Does this sound right?**
- Reply 'YES' if this matches what you want
- Reply 'NO' if you need something different
"""
        return plan
    
    def ask_questions(self, pattern_type, question_index=0):
        """Ask clarification questions one by one"""
        pattern = self.workflow_patterns[pattern_type]
        questions = pattern['questions']
        
        if question_index >= len(questions):
            return "✅ Perfect! I have enough information to create your workflow."
        
        return f"""
❓ **Question {question_index + 1} of {len(questions)}:**

{questions[question_index]}

**Please answer YES or NO**
"""
    
    def handle_unclear_prompt(self, user_input):
        """Main method to handle unclear prompts"""
        if len(user_input.strip()) < 10:
            return """
🤔 **I need a bit more information to help you!**

Could you tell me what you want to automate? For example:
- "Process CSV files and email results"
- "Send daily reports from Google Sheets to Slack"  
- "Backup files to cloud storage weekly"

**What would you like your workflow to do?**
"""
        
        # Analyze and create plan
        pattern_type = self.analyze_request(user_input)
        return self.create_plan(pattern_type, user_input)

# Integration with existing app
def enhance_workflow_generation(user_input):
    """Enhanced workflow generation with prompt assistance"""
    helper = PromptHelper()
    
    # Check if input is too vague
    if len(user_input.strip()) < 15 or user_input.count(' ') < 3:
        return {
            'needs_clarification': True,
            'helper_response': helper.handle_unclear_prompt(user_input),
            'suggested_pattern': None
        }
    
    # Analyze and suggest
    pattern_type = helper.analyze_request(user_input)
    plan = helper.create_plan(pattern_type, user_input)
    
    return {
        'needs_clarification': False,
        'helper_response': plan,
        'suggested_pattern': pattern_type
    }

if __name__ == "__main__":
    # Test the helper
    helper = PromptHelper()
    
    test_inputs = [
        "help",
        "automate something", 
        "I want to process CSV files and send email reports",
        "connect slack to sheets"
    ]
    
    for test_input in test_inputs:
        print(f"\nInput: '{test_input}'")
        print("-" * 40)
        result = enhance_workflow_generation(test_input)
        print(result['helper_response'])
        print("=" * 50)