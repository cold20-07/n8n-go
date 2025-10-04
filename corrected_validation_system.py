#!/usr/bin/env python3
"""
Corrected Validation System
Fixes all logical and mathematical errors in the validation system
"""

import re
import html
import json
import unicodedata
from typing import Dict, List, Tuple, Optional, Any
import logging

class CorrectedInputValidator:
    """Corrected input validation with realistic failure detection"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Industry keywords for better classification
        self.industry_keywords = {
            'healthcare': [
                'patient', 'medical', 'doctor', 'hospital', 'clinic', 'treatment', 
                'prescription', 'appointment', 'diagnosis', 'therapy', 'surgery',
                'nurse', 'physician', 'healthcare', 'medicine', 'health'
            ],
            'finance': [
                'payment', 'transaction', 'bank', 'loan', 'credit', 'invoice',
                'billing', 'accounting', 'financial', 'money', 'currency',
                'fraud', 'risk', 'investment', 'portfolio', 'trading'
            ],
            'education': [
                'student', 'teacher', 'course', 'class', 'school', 'university',
                'grade', 'assignment', 'curriculum', 'learning', 'education',
                'academic', 'enrollment', 'semester', 'degree', 'exam'
            ],
            'ecommerce': [
                'order', 'product', 'inventory', 'shipping', 'customer', 'cart',
                'checkout', 'payment', 'store', 'shop', 'purchase', 'sale',
                'catalog', 'price', 'discount', 'promotion', 'delivery'
            ]
        }
        
        # Common workflow actions
        self.workflow_actions = [
            'process', 'manage', 'handle', 'create', 'update', 'delete',
            'send', 'receive', 'validate', 'transform', 'sync', 'monitor',
            'track', 'schedule', 'automate', 'integrate', 'analyze'
        ]
        
        # Define inputs that should LEGITIMATELY FAIL
        self.should_fail_patterns = [
            # Completely empty requests
            lambda data: not data or (isinstance(data, dict) and len(data) == 0),
            
            # Malicious inputs that can't be safely processed
            lambda data: self._is_malicious_input(data.get('description', '') if isinstance(data, dict) else ''),
            
            # Inputs that are fundamentally impossible to process
            lambda data: self._is_impossible_input(data.get('description', '') if isinstance(data, dict) else ''),
            
            # Severely corrupted data
            lambda data: self._is_corrupted_data(data),
        ]
    
    def _is_malicious_input(self, description: str) -> bool:
        """Check if input is malicious and should fail"""
        if not isinstance(description, str):
            return False
        
        # Severe malicious patterns that should fail
        severe_patterns = [
            r'<script[^>]*>.*?</script>.*<script[^>]*>.*?</script>',  # Multiple script tags
            r'DROP\s+TABLE.*;\s*DROP\s+TABLE',  # Multiple SQL drops
            r'rm\s+-rf\s+/.*&&.*rm\s+-rf',  # Multiple destructive commands
            r'\x00.*\x00.*\x00',  # Multiple null bytes
        ]
        
        for pattern in severe_patterns:
            if re.search(pattern, description, re.IGNORECASE | re.DOTALL):
                return True
        
        return False
    
    def _is_impossible_input(self, description: str) -> bool:
        """Check if input is impossible to process meaningfully"""
        if not isinstance(description, str):
            return False
        
        # After all cleaning, if it's still meaningless
        cleaned = self._basic_clean(description)
        
        # Impossible patterns
        if len(cleaned) == 0:  # Completely empty after cleaning
            return True
        
        # Only control characters
        if all(ord(c) < 32 for c in cleaned if c not in '\n\r\t'):
            return True
        
        # Only repeated single character (more than 1000 times)
        if len(set(cleaned.replace(' ', ''))) == 1 and len(cleaned) > 1000:
            return True
        
        return False
    
    def _is_corrupted_data(self, data: Any) -> bool:
        """Check if data is severely corrupted"""
        if data is None:
            return False  # None is handleable
        
        # Circular references or extremely nested structures
        try:
            json.dumps(data)
        except (TypeError, ValueError, RecursionError):
            return True
        
        return False
    
    def _basic_clean(self, text: str) -> str:
        """Basic cleaning for testing purposes"""
        if not isinstance(text, str):
            return ""
        
        # Remove control characters
        cleaned = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
        
        # Normalize whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        return cleaned
    
    def validate_and_enhance_description(self, description: Any) -> Tuple[str, Dict[str, Any]]:
        """
        Validate and enhance workflow description with REALISTIC failure detection
        Returns: (cleaned_description, validation_info)
        """
        validation_info = {
            'original_length': 0,
            'cleaned_length': 0,
            'transformations_applied': [],
            'detected_language': 'en',
            'confidence_score': 0.0,
            'suggested_improvements': [],
            'should_fail': False,
            'failure_reason': None
        }
        
        try:
            # Step 1: Check for inputs that should legitimately fail
            test_data = {'description': description} if not isinstance(description, dict) else description
            
            for fail_check in self.should_fail_patterns:
                if fail_check(test_data):
                    validation_info['should_fail'] = True
                    validation_info['failure_reason'] = "Input fails legitimate quality thresholds"
                    raise ValueError("Input should legitimately fail validation")
            
            # Step 2: Handle non-string inputs
            if description is None:
                description = "general data processing workflow"
                validation_info['transformations_applied'].append('null_to_default')
            
            if not isinstance(description, str):
                description = str(description)
                validation_info['transformations_applied'].append('type_conversion')
            
            validation_info['original_length'] = len(description)
            
            # Step 3: Basic cleaning and normalization
            cleaned = self._normalize_text(description)
            if cleaned != description:
                validation_info['transformations_applied'].append('text_normalization')
            
            # Step 4: Check if still impossible after cleaning
            if self._is_impossible_input(cleaned):
                validation_info['should_fail'] = True
                validation_info['failure_reason'] = "Input impossible to process meaningfully"
                raise ValueError("Input impossible to process after cleaning")
            
            # Step 5: Handle empty or too short descriptions
            if len(cleaned.strip()) == 0:
                cleaned = "automated data processing workflow"
                validation_info['transformations_applied'].append('empty_to_default')
            elif len(cleaned.strip()) < 3:
                cleaned = f"automated {cleaned.strip()} processing workflow"
                validation_info['transformations_applied'].append('short_expansion')
            
            # Step 6: Security sanitization
            cleaned = self._sanitize_security_threats(cleaned)
            
            # Step 7: Language detection
            lang_info = self._detect_language_patterns(cleaned)
            validation_info['detected_language'] = lang_info['language']
            
            # Step 8: Intelligent enhancement for ambiguous descriptions
            enhanced = self._enhance_ambiguous_description(cleaned)
            if enhanced != cleaned:
                validation_info['transformations_applied'].append('ambiguity_resolution')
                cleaned = enhanced
            
            # Step 9: Length optimization
            if len(cleaned) > 5000:
                cleaned = self._truncate_intelligently(cleaned, 5000)
                validation_info['transformations_applied'].append('intelligent_truncation')
            
            # Step 10: Calculate REALISTIC confidence score
            validation_info['confidence_score'] = self._calculate_realistic_confidence_score(
                cleaned, validation_info['transformations_applied']
            )
            
            # Step 11: Final quality check - some enhanced descriptions should still fail
            if validation_info['confidence_score'] < 0.2:  # Very low confidence
                validation_info['should_fail'] = True
                validation_info['failure_reason'] = f"Confidence too low: {validation_info['confidence_score']:.3f}"
                raise ValueError("Enhanced description still has too low confidence")
            
            validation_info['cleaned_length'] = len(cleaned)
            validation_info['suggested_improvements'] = self._generate_suggestions(cleaned)
            
            return cleaned, validation_info
            
        except ValueError as e:
            # This is a legitimate failure
            validation_info['should_fail'] = True
            if not validation_info['failure_reason']:
                validation_info['failure_reason'] = str(e)
            raise e
            
        except Exception as e:
            # Unexpected error - also a failure
            validation_info['should_fail'] = True
            validation_info['failure_reason'] = f"Unexpected error: {str(e)}"
            raise e
    
    def _normalize_text(self, text: str) -> str:
        """Normalize text with Unicode handling and cleanup"""
        try:
            # Unicode normalization
            text = unicodedata.normalize('NFKC', text)
            
            # Remove control characters but keep newlines and tabs
            text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
            
            # Normalize whitespace
            text = re.sub(r'\s+', ' ', text)
            
            # Remove excessive punctuation
            text = re.sub(r'[!]{3,}', '!', text)
            text = re.sub(r'[?]{3,}', '?', text)
            text = re.sub(r'[.]{4,}', '...', text)
            
            return text.strip()
            
        except Exception:
            return text.strip()
    
    def _sanitize_security_threats(self, text: str) -> str:
        """Remove security threats while preserving legitimate content"""
        dangerous_patterns = [
            r'<script[^>]*>.*?</script>',  # Script tags
            r'javascript:',               # JavaScript URLs
            r'on\w+\s*=',                # Event handlers
            r'DROP\s+TABLE',             # SQL injection
            r'DELETE\s+FROM',            # SQL injection
            r'INSERT\s+INTO',            # SQL injection
            r'UPDATE\s+SET',             # SQL injection
            r'rm\s+-rf',                 # Command injection
            r'\.\./',                    # Path traversal
            r'<\?php',                   # PHP injection
            r'<%',                       # ASP injection
        ]
        
        sanitized = text
        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        # HTML escape remaining content but preserve basic structure
        sanitized = html.escape(sanitized, quote=False)
        
        return sanitized
    
    def _detect_language_patterns(self, text: str) -> Dict[str, str]:
        """Detect language patterns and provide hints"""
        text_lower = text.lower()
        
        # Simple language detection based on common words
        language_patterns = {
            'spanish': ['flujo', 'trabajo', 'proceso', 'sistema', 'datos'],
            'french': ['flux', 'travail', 'processus', 'système', 'données'],
            'german': ['workflow', 'arbeit', 'prozess', 'system', 'daten'],
            'italian': ['flusso', 'lavoro', 'processo', 'sistema', 'dati'],
            'portuguese': ['fluxo', 'trabalho', 'processo', 'sistema', 'dados']
        }
        
        for lang, patterns in language_patterns.items():
            if any(pattern in text_lower for pattern in patterns):
                return {'language': lang, 'confidence': 0.7}
        
        # Check for non-Latin scripts
        if re.search(r'[\u4e00-\u9fff]', text):  # Chinese
            return {'language': 'chinese', 'confidence': 0.9}
        elif re.search(r'[\u0400-\u04ff]', text):  # Cyrillic
            return {'language': 'russian', 'confidence': 0.9}
        elif re.search(r'[\u0600-\u06ff]', text):  # Arabic
            return {'language': 'arabic', 'confidence': 0.9}
        
        return {'language': 'en', 'confidence': 0.5}
    
    def _enhance_ambiguous_description(self, text: str) -> str:
        """Enhance ambiguous or vague descriptions"""
        text_lower = text.lower()
        
        # Handle very generic terms
        generic_replacements = {
            r'\bstuff\b': 'data',
            r'\bthing\b': 'item',
            r'\bthings\b': 'items',
            r'\bdo something\b': 'process data',
            r'\bhandle stuff\b': 'process information',
            r'\bmanage things\b': 'manage resources'
        }
        
        enhanced = text
        for pattern, replacement in generic_replacements.items():
            enhanced = re.sub(pattern, replacement, enhanced, flags=re.IGNORECASE)
        
        # Add context for single words
        single_word_enhancements = {
            'workflow': 'automated workflow system',
            'process': 'data processing workflow',
            'system': 'management system workflow',
            'automation': 'business process automation',
            'data': 'data processing and management',
            'management': 'resource management system'
        }
        
        words = enhanced.strip().split()
        if len(words) == 1 and words[0].lower() in single_word_enhancements:
            enhanced = single_word_enhancements[words[0].lower()]
        
        # Add industry context if detected
        for industry, keywords in self.industry_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                if len(words) < 3:  # Short description
                    enhanced = f"{industry} {enhanced} management system"
                break
        
        return enhanced
    
    def _truncate_intelligently(self, text: str, max_length: int) -> str:
        """Intelligently truncate text while preserving meaning"""
        if len(text) <= max_length:
            return text
        
        # Try to truncate at sentence boundaries
        sentences = re.split(r'[.!?]+', text)
        result = ""
        
        for sentence in sentences:
            if len(result + sentence) <= max_length - 3:  # Leave room for "..."
                result += sentence + ". "
            else:
                break
        
        if result:
            return result.strip()
        
        # Fallback: truncate at word boundaries
        words = text.split()
        result = ""
        
        for word in words:
            if len(result + word) <= max_length - 3:
                result += word + " "
            else:
                break
        
        return (result.strip() + "...") if result else text[:max_length-3] + "..."
    
    def _calculate_realistic_confidence_score(self, text: str, transformations: List[str]) -> float:
        """Calculate REALISTIC confidence score that can actually be low"""
        score = 0.0
        text_lower = text.lower()
        
        # Base score depends on transformations needed
        if 'null_to_default' in transformations or 'empty_to_default' in transformations:
            score = 0.1  # Very low for generated defaults
        elif 'type_conversion' in transformations:
            score = 0.2  # Low for type conversions
        elif 'short_expansion' in transformations:
            score = 0.3  # Medium-low for expanded short inputs
        else:
            score = 0.5  # Medium base for normal inputs
        
        # Length factor (realistic ranges)
        length = len(text)
        if 20 <= length <= 200:
            score += 0.2
        elif 10 <= length < 20 or 200 < length <= 500:
            score += 0.1
        elif length < 10:
            score -= 0.1  # Penalty for very short
        
        # Action words presence
        action_count = sum(1 for action in self.workflow_actions if action in text_lower)
        score += min(action_count * 0.1, 0.2)
        
        # Industry keywords presence
        industry_count = sum(1 for keywords in self.industry_keywords.values() 
                           for keyword in keywords if keyword in text_lower)
        score += min(industry_count * 0.05, 0.15)
        
        # Specificity penalty for generic terms
        generic_terms = ['thing', 'stuff', 'something', 'anything', 'item', 'data']
        generic_count = sum(1 for term in generic_terms if term in text_lower)
        score -= generic_count * 0.1
        
        # Heavy penalty for too many transformations
        if len(transformations) > 3:
            score -= 0.2
        
        # Ensure realistic range
        return max(0.0, min(1.0, score))
    
    def _generate_suggestions(self, text: str) -> List[str]:
        """Generate suggestions for improving the description"""
        suggestions = []
        text_lower = text.lower()
        
        # Check for missing action words
        if not any(action in text_lower for action in self.workflow_actions):
            suggestions.append("Consider adding an action word like 'process', 'manage', or 'handle'")
        
        # Check for missing industry context
        if not any(keyword in text_lower for keywords in self.industry_keywords.values() 
                  for keyword in keywords):
            suggestions.append("Consider specifying the industry or domain (e.g., healthcare, finance)")
        
        # Check length
        if len(text) < 15:
            suggestions.append("Consider providing more details about the workflow requirements")
        elif len(text) > 1000:
            suggestions.append("Consider making the description more concise")
        
        # Check for generic terms
        generic_terms = ['thing', 'stuff', 'something', 'item', 'data']
        if any(term in text_lower for term in generic_terms):
            suggestions.append("Replace generic terms with specific nouns")
        
        return suggestions
    
    def validate_trigger_type(self, trigger_type: Any) -> str:
        """Validate and normalize trigger type"""
        if not trigger_type:
            return 'webhook'  # Default
        
        trigger_str = str(trigger_type).lower().strip()
        
        # Handle variations
        trigger_mappings = {
            'webhook': 'webhook',
            'web': 'webhook',
            'http': 'webhook',
            'api': 'webhook',
            'schedule': 'schedule',
            'scheduled': 'schedule',
            'cron': 'schedule',
            'timer': 'schedule',
            'manual': 'manual',
            'button': 'manual',
            'click': 'manual',
            'user': 'manual'
        }
        
        for key, value in trigger_mappings.items():
            if key in trigger_str:
                return value
        
        return 'webhook'  # Safe default
    
    def validate_complexity(self, complexity: Any) -> str:
        """Validate and normalize complexity level"""
        if not complexity:
            return 'medium'  # Default
        
        complexity_str = str(complexity).lower().strip()
        
        # Handle variations
        if any(word in complexity_str for word in ['simple', 'basic', 'easy', 'minimal']):
            return 'simple'
        elif any(word in complexity_str for word in ['complex', 'advanced', 'detailed', 'comprehensive']):
            return 'complex'
        else:
            return 'medium'  # Default for anything else
    
    def validate_advanced_options(self, options: Any) -> Dict[str, Any]:
        """Validate and clean advanced options"""
        if not options:
            return {}
        
        if not isinstance(options, dict):
            try:
                if isinstance(options, str):
                    options = json.loads(options)
                else:
                    return {}
            except (json.JSONDecodeError, TypeError):
                return {}
        
        # Clean and validate known options
        cleaned_options = {}
        
        # Boolean options
        bool_options = ['enable_error_handling', 'add_logging', 'include_validation']
        for option in bool_options:
            if option in options:
                cleaned_options[option] = bool(options[option])
        
        # String options
        string_options = ['template', 'industry', 'integration_type']
        for option in string_options:
            if option in options and options[option]:
                cleaned_options[option] = str(options[option])[:100]  # Limit length
        
        # Numeric options
        numeric_options = ['max_nodes', 'timeout']
        for option in numeric_options:
            if option in options:
                try:
                    value = int(options[option])
                    if option == 'max_nodes':
                        cleaned_options[option] = max(1, min(value, 50))  # Reasonable limits
                    elif option == 'timeout':
                        cleaned_options[option] = max(1, min(value, 3600))  # 1 second to 1 hour
                except (ValueError, TypeError):
                    pass
        
        return cleaned_options

# Global corrected validator instance
corrected_validator = CorrectedInputValidator()

def corrected_validate_workflow_request(data: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Corrected validation that can legitimately fail
    Returns: (cleaned_data, validation_report)
    Raises: ValueError for inputs that should legitimately fail
    """
    validation_report = {
        'description': {},
        'trigger_type': {},
        'complexity': {},
        'advanced_options': {},
        'overall_confidence': 0.0,
        'should_fail': False,
        'failure_reason': None
    }
    
    cleaned_data = {}
    
    try:
        # Validate description - this can now legitimately fail
        description = data.get('description', '')
        cleaned_desc, desc_info = corrected_validator.validate_and_enhance_description(description)
        cleaned_data['description'] = cleaned_desc
        validation_report['description'] = desc_info
        
        # Validate trigger type
        trigger_type = data.get('triggerType') or data.get('trigger_type', 'webhook')
        cleaned_data['trigger_type'] = corrected_validator.validate_trigger_type(trigger_type)
        validation_report['trigger_type'] = {
            'original': trigger_type,
            'cleaned': cleaned_data['trigger_type'],
            'changed': str(trigger_type) != cleaned_data['trigger_type']
        }
        
        # Validate complexity
        complexity = data.get('complexity', 'medium')
        cleaned_data['complexity'] = corrected_validator.validate_complexity(complexity)
        validation_report['complexity'] = {
            'original': complexity,
            'cleaned': cleaned_data['complexity'],
            'changed': str(complexity) != cleaned_data['complexity']
        }
        
        # Validate advanced options
        advanced_options = data.get('advanced_options', {})
        cleaned_data['advanced_options'] = corrected_validator.validate_advanced_options(advanced_options)
        validation_report['advanced_options'] = {
            'original_keys': list(advanced_options.keys()) if isinstance(advanced_options, dict) else [],
            'cleaned_keys': list(cleaned_data['advanced_options'].keys()),
            'options_count': len(cleaned_data['advanced_options'])
        }
        
        # Calculate overall confidence
        validation_report['overall_confidence'] = desc_info.get('confidence_score', 0.0)
        
        return cleaned_data, validation_report
        
    except ValueError as e:
        # This is a legitimate failure
        validation_report['should_fail'] = True
        validation_report['failure_reason'] = str(e)
        raise e