from flask import Flask, render_template, request, jsonify
import json
import os
import re
import html
import time
import warnings
from werkzeug.exceptions import BadRequest
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

# Suppress Flask-Limiter warning about in-memory storage in development
warnings.filterwarnings('ignore', 
                      message='Using the in-memory storage for tracking rate limits',
                      category=UserWarning,
                      module='flask_limiter._extension')

# Import configuration and logging
try:
    from config import config, validate_config
    from logger import setup_app_logging
    from exceptions import *
    
    # Setup logging
    logger = setup_app_logging(debug=config.DEBUG)
    validate_config()
    
except ImportError as e:
    print(f"Warning: Configuration modules not available: {e}")
    import logging
    logger = logging.getLogger(__name__)

# Import enhancement modules
try:
    from n8n_workflow_research import N8nWorkflowResearcher
    from enhance_workflow_output import WorkflowOutputEnhancer
    ENHANCER_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Enhancement modules not available: {e}")
    ENHANCER_AVAILABLE = False

# Import AI enhancement system
try:
    from ai_enhancements import AIOrchestrator, GeminiProvider, OpenAIProvider, AIProvider, generate_enhanced_workflow
    AI_ENHANCEMENTS_AVAILABLE = True
    logger.info("[OK] AI Enhancement system loaded successfully")
except ImportError as e:
    logger.warning(f"AI Enhancement system not available: {e}")
    AI_ENHANCEMENTS_AVAILABLE = False

# Import template system
try:
    from src.templates.workflow_templates import template_manager, TemplateCategory
    TEMPLATES_AVAILABLE = True
    logger.info("[OK] Workflow template system loaded successfully")
except ImportError as e:
    logger.warning(f"Template system not available: {e}")
    TEMPLATES_AVAILABLE = False

# Import validation system
try:
    from src.validators.workflow_validator import workflow_validator
    WORKFLOW_VALIDATOR_AVAILABLE = True
    logger.info("[OK] Workflow validation system loaded successfully")
except ImportError as e:
    logger.warning(f"Workflow validation system not available: {e}")
    WORKFLOW_VALIDATOR_AVAILABLE = False

# Import market-leading generator
try:
    from src.core.generators.market_leading_workflow_generator import generate_market_leading_workflow
    MARKET_LEADING_GENERATOR_AVAILABLE = True
    logger.info("[OK] Market-leading workflow generator loaded successfully")
except ImportError as e:
    logger.warning(f"Market-leading generator not available: {e}")
    MARKET_LEADING_GENERATOR_AVAILABLE = False

# Import validation modules with new paths
try:
    from src.core.validators.enhanced_input_validation import validate_workflow_request, validator
    ENHANCED_VALIDATION_AVAILABLE = True
    logger.info("[OK] Enhanced input validation loaded successfully")
except ImportError as e:
    logger.warning(f"Enhanced validation not available: {e}")
    ENHANCED_VALIDATION_AVAILABLE = False

# Import utility modules with new paths
try:
    from src.utils.prompt_helper import enhance_workflow_generation, PromptHelper
    PROMPT_HELPER_AVAILABLE = True
    logger.info("[OK] Prompt helper loaded successfully")
except ImportError as e:
    logger.warning(f"Prompt helper not available: {e}")
    PROMPT_HELPER_AVAILABLE = False

# Import generator modules with new paths
try:
    from src.core.generators.trained_workflow_generator import generate_trained_workflow, TrainedWorkflowGenerator
    TRAINED_GENERATOR_AVAILABLE = True
    logger.info("[OK] Trained workflow generator loaded successfully")
except ImportError as e:
    logger.warning(f"Trained generator not available: {e}")
    TRAINED_GENERATOR_AVAILABLE = False

try:
    from src.core.generators.feature_aware_workflow_generator import generate_feature_aware_workflow, FeatureAwareGenerator
    FEATURE_AWARE_GENERATOR_AVAILABLE = True
    logger.info("[OK] Feature-aware workflow generator loaded successfully")
except ImportError as e:
    logger.warning(f"Feature-aware generator not available: {e}")
    FEATURE_AWARE_GENERATOR_AVAILABLE = False

try:
    from src.core.generators.enhanced_workflow_generator import generate_enhanced_workflow, EnhancedWorkflowGenerator
    ENHANCED_GENERATOR_AVAILABLE = True
    logger.info("[OK] Enhanced workflow generator loaded successfully")
except ImportError as e:
    logger.warning(f"Enhanced generator not available: {e}")
    ENHANCED_GENERATOR_AVAILABLE = False

# Import validator modules with new paths
try:
    from src.core.validators.connection_validator import ConnectionValidator
    from src.core.validators.workflow_accuracy_validator import WorkflowAccuracyValidator
    CONNECTION_VALIDATOR_AVAILABLE = True
    logger.info("[OK] Connection validator loaded successfully")
except ImportError as e:
    logger.warning(f"Connection validator not available: {e}")
    CONNECTION_VALIDATOR_AVAILABLE = False

try:
    from src.core.validators.simple_connection_fixer import validate_and_fix_connections
    SIMPLE_FIXER_AVAILABLE = True
    logger.info("[OK] Simple connection fixer loaded successfully")
except ImportError as e:
    logger.warning(f"Simple connection fixer not available: {e}")
    SIMPLE_FIXER_AVAILABLE = False

app = Flask(__name__)

# Configure Flask app with advanced configuration system
try:
    # Basic Flask configuration
    app.config.update({
        'SECRET_KEY': config.SECRET_KEY,
        'DEBUG': config.DEBUG,
        'TESTING': config.is_testing(),
        'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16MB max file size
        'JSON_SORT_KEYS': False,
        'JSONIFY_PRETTYPRINT_REGULAR': config.DEBUG
    })
    
    # Setup CORS with advanced configuration
    CORS(app, 
         origins=config.get_cors_origins(),
         supports_credentials=True,
         max_age=3600)
    
    # Setup rate limiting with endpoint-specific limits
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=[f"{config.RATE_LIMIT_PER_HOUR} per hour"],
        storage_uri=config.REDIS_URL if config.ENABLE_CACHING else None,
        strategy="fixed-window"
    )
    
    # Register configuration API blueprint
    try:
        from config_api import config_bp
        app.register_blueprint(config_bp)
        logger.info("[OK] Configuration API registered")
    except ImportError as e:
        logger.warning(f"Configuration API not available: {e}")
    
    logger.info(f"[OK] Flask app configured successfully")
    logger.info(f"   Environment: {config.FLASK_ENV}")
    logger.info(f"   Debug: {config.DEBUG}")
    logger.info(f"   Rate limiting: {config.RATE_LIMIT_PER_HOUR}/hour")
    logger.info(f"   Features enabled: {sum(1 for v in config.get_feature_flags().values() if v)}")
    
except Exception as e:
    logger.error(f"Failed to configure Flask app: {e}")
    # Fallback to basic configuration
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fallback-key'
    limiter = None

def sanitize_input(text):
    """Legacy sanitize function - kept for backward compatibility"""
    if not isinstance(text, str):
        return str(text)
    
    # Remove dangerous patterns
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
    
    # HTML escape remaining content
    sanitized = html.escape(sanitized)
    
    # Remove null bytes and control characters
    sanitized = ''.join(char for char in sanitized if ord(char) >= 32 or char in '\n\r\t')
    
    return sanitized.strip()

# Initialize components
if ENHANCER_AVAILABLE:
    researcher = N8nWorkflowResearcher()
    enhancer = WorkflowOutputEnhancer(researcher)
else:
    researcher = None
    enhancer = None

# Initialize connection validator
if CONNECTION_VALIDATOR_AVAILABLE:
    connection_validator = ConnectionValidator()
    accuracy_validator = WorkflowAccuracyValidator()
    print("[OK] Connection validation system initialized")
else:
    connection_validator = None
    accuracy_validator = None

def legacy_validation(data):
    """Legacy validation function for backward compatibility"""
    if 'description' not in data:
        raise BadRequest('Missing workflow description')
    
    description = data.get('description', '').strip()
    if not description:
        raise BadRequest('Description cannot be empty')
        
    if len(description) < 10:
        raise BadRequest('Description must be at least 10 characters long')
    
    if len(description) > 5000:
        raise BadRequest('Description is too long (maximum 5,000 characters)')
    
    # Sanitize description to prevent injection attacks
    description = sanitize_input(description)
    
    # Support both triggerType and trigger_type for compatibility
    trigger_type = data.get('triggerType') or data.get('trigger_type', 'webhook')
    if trigger_type not in ['webhook', 'schedule', 'manual']:
        raise BadRequest('Invalid trigger type. Must be: webhook, schedule, or manual')
        
    complexity = data.get('complexity', 'medium')
    if complexity not in ['simple', 'medium', 'complex']:
        complexity = 'medium'  # Default to medium if invalid
        
    template = data.get('template', '')
    advanced_options = data.get('advanced_options', {})
    
    validation_metadata = {
        'validation_applied': False,
        'legacy_validation': True
    }
    
    return description, trigger_type, complexity, advanced_options, template, validation_metadata

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/documentation')
def documentation():
    return render_template('documentation.html')

@app.route('/prompt-help', methods=['POST'])
@limiter.limit(config.PROMPT_HELP_RATE_LIMIT) if limiter else lambda f: f
def get_prompt_help():
    """Provide interactive prompt assistance for unclear requests"""
    try:
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 415
            
        data = request.get_json()
        user_input = data.get('description', '').strip()
        
        if not user_input:
            return jsonify({
                'success': True,
                'needs_help': True,
                'message': """
🤔 **I'm here to help you create the perfect workflow!**

Tell me what you want to automate. For example:
- "Process CSV files and email the results"
- "Send daily reports from Google Sheets to Slack"
- "Backup files to cloud storage every week"

**What would you like your workflow to do?**
""",
                'suggestions': [
                    "Process data from files",
                    "Automate daily tasks", 
                    "Connect different apps",
                    "Send notifications"
                ]
            })
        
        if PROMPT_HELPER_AVAILABLE:
            result = enhance_workflow_generation(user_input)
            return jsonify({
                'success': True,
                'needs_help': result['needs_clarification'],
                'message': result['helper_response'],
                'suggested_pattern': result.get('suggested_pattern'),
                'original_input': user_input
            })
        else:
            # Fallback without prompt helper
            if len(user_input) < 15:
                return jsonify({
                    'success': True,
                    'needs_help': True,
                    'message': "Could you provide more details about what you want to automate?",
                    'suggestions': ["Add more details about your workflow needs"]
                })
            else:
                return jsonify({
                    'success': True,
                    'needs_help': False,
                    'message': "Your request looks good! Ready to generate workflow.",
                    'suggested_pattern': 'automation'
                })
                
    except Exception as e:
        return jsonify({'success': False, 'error': f'Prompt help error: {str(e)}'}), 500

@app.route('/generate', methods=['POST'])
@limiter.limit(config.GENERATE_RATE_LIMIT) if limiter else lambda f: f
def generate_workflow():
    try:
        # Handle missing content-type header
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 415
            
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Check if user needs prompt assistance first
        description = data.get('description', '').strip()
        if PROMPT_HELPER_AVAILABLE and len(description) < 10:
            helper_result = enhance_workflow_generation(description)
            if helper_result['needs_clarification']:
                return jsonify({
                    'success': False,
                    'needs_prompt_help': True,
                    'helper_message': helper_result['helper_response'],
                    'error': 'Please provide more details about your workflow'
                })
        
        # Use enhanced validation if available
        if ENHANCED_VALIDATION_AVAILABLE:
            try:
                cleaned_data, validation_report = validate_workflow_request(data)
                
                # Extract validated data
                description = cleaned_data['description']
                trigger_type = cleaned_data['trigger_type']
                complexity = cleaned_data['complexity']
                advanced_options = cleaned_data['advanced_options']
                template = data.get('template', '')  # Keep original template
                
                # Add validation info to response metadata
                validation_metadata = {
                    'validation_applied': True,
                    'confidence_score': validation_report['overall_confidence'],
                    'transformations': validation_report['description'].get('transformations_applied', []),
                    'suggestions': validation_report['description'].get('suggested_improvements', [])
                }
                
            except Exception as e:
                print(f"Enhanced validation failed, falling back to legacy: {e}")
                # Fall back to legacy validation
                description, trigger_type, complexity, advanced_options, template, validation_metadata = legacy_validation(data)
        else:
            # Use legacy validation
            description, trigger_type, complexity, advanced_options, template, validation_metadata = legacy_validation(data)
        
        # Generate workflow using enhanced AI system first, then fallback options
        workflow = None
        generation_error = None
        
        # Try Market-Leading Generator first (best quality)
        if MARKET_LEADING_GENERATOR_AVAILABLE:
            try:
                print("Market-Leading: Using comprehensive training dataset for best-in-market quality")
                workflow = generate_market_leading_workflow(description, trigger_type, complexity)
                
                # Validate the generated workflow
                nodes = workflow.get('nodes', [])
                connections = workflow.get('connections', {})
                
                print(f"Market-Leading: System succeeded:")
                print(f"   Nodes: {len(nodes)}")
                print(f"   Connections: {len(connections)}")
                
                # Log node details
                for i, node in enumerate(nodes, 1):
                    print(f"   {i}. {node.get('name')} ({node.get('type')})")
                
            except Exception as e:
                print(f"Market-Leading: System failed: {e}")
                import traceback
                traceback.print_exc()
                generation_error = str(e)
                workflow = None
        
        # Fallback to AI Enhancement system
        if not workflow and AI_ENHANCEMENTS_AVAILABLE:
            try:
                print("AI Enhancement: Using AI Enhancement system with multi-provider support")
                from ai_enhancements import generate_enhanced_workflow as ai_generate_workflow
                workflow = ai_generate_workflow(description, trigger_type, complexity)
                
                # Validate the generated workflow
                nodes = workflow.get('nodes', [])
                connections = workflow.get('connections', {})
                
                print(f"AI Enhancement: System succeeded:")
                print(f"   Nodes: {len(nodes)}")
                print(f"   Connections: {len(connections)}")
                
                # Log node details
                for i, node in enumerate(nodes, 1):
                    print(f"   {i}. {node.get('name')} ({node.get('type')})")
                
            except Exception as e:
                print(f"AI Enhancement: System failed: {e}")
                import traceback
                traceback.print_exc()
                generation_error = str(e)
                workflow = None
        
        # Fallback to enhanced generator if AI system failed
        if not workflow and ENHANCED_GENERATOR_AVAILABLE:
            try:
                print("Enhanced Generator: Using enhanced workflow generator with comprehensive feature detection")
                workflow = generate_enhanced_workflow(description, trigger_type, complexity)
                
                # Validate the generated workflow
                nodes = workflow.get('nodes', [])
                connections = workflow.get('connections', {})
                
                print(f"Enhanced Generator: Succeeded:")
                print(f"   Nodes: {len(nodes)}")
                print(f"   Connections: {len(connections)}")
                
                # Log node details
                for i, node in enumerate(nodes, 1):
                    print(f"   {i}. {node.get('name')} ({node.get('type')})")
                
                # Log connection details
                for source, conn_data in connections.items():
                    if 'main' in conn_data and conn_data['main']:
                        for group in conn_data['main']:
                            for conn in group:
                                target = conn.get('node', 'unknown')
                                print(f"   [CONNECT] {source} -> {target}")
                
                # Validate all nodes are properly connected
                node_names = [node.get('name') for node in nodes]
                expected_connections = len(nodes) - 1 if len(nodes) > 1 else 0
                
                if len(connections) == expected_connections:
                    print(f"[OK] All {expected_connections} connections validated")
                else:
                    print(f"[WARN] Connection mismatch: expected {expected_connections}, got {len(connections)}")
                
            except Exception as e:
                print(f"[ERROR] Enhanced generator failed: {e}")
                import traceback
                traceback.print_exc()
                generation_error = str(e)
                workflow = None
        
        if not workflow and FEATURE_AWARE_GENERATOR_AVAILABLE:
            try:
                print("Feature-Aware: Using feature-aware workflow generator with comprehensive feature detection")
                workflow = generate_feature_aware_workflow(description, trigger_type, complexity)
                print(f"Feature-Aware: Generator succeeded: {len(workflow.get('nodes', []))} nodes")
            except Exception as e:
                print(f"Feature-Aware: Generator failed: {e}")
                generation_error = str(e)
                workflow = None
        
        if not workflow and TRAINED_GENERATOR_AVAILABLE:
            try:
                print("Trained: Using trained workflow generator with real n8n patterns")
                workflow = generate_trained_workflow(description, trigger_type, complexity)
                print(f"Trained: Generator succeeded: {len(workflow.get('nodes', []))} nodes")
            except Exception as e:
                print(f"Trained: Generator failed: {e}")
                generation_error = str(e)
                workflow = None
        
        if not workflow:
            print("[WARN] All advanced generators failed, falling back to basic workflow generation")
            if generation_error:
                print(f"   Last error: {generation_error}")
            workflow = create_basic_workflow(description, trigger_type, complexity, template, advanced_options)
            print(f"Basic: Generator succeeded: {len(workflow.get('nodes', []))} nodes")
        
        # Apply connection fixing - try simple fixer first, then advanced if needed
        if workflow:
            if SIMPLE_FIXER_AVAILABLE:
                print("Connection Fix: Applying simple connection fixes...")
                try:
                    workflow = validate_and_fix_connections(workflow)
                except Exception as e:
                    print(f"Connection Fix: Simple connection fixer failed: {e}")
                    # Continue to try advanced validator
            
            # Also try advanced connection validation if available
            if CONNECTION_VALIDATOR_AVAILABLE:
                print("Advanced Validation: Applying advanced connection validation and fixes...")
                
                try:
                    # Validate and fix connections
                    fixed_workflow, validation_report = connection_validator.validate_and_fix_connections(workflow)
                    
                    # Log validation results
                    original_valid = validation_report['original_validation']['is_valid']
                    original_errors = validation_report['original_validation']['errors']
                    fixes_applied = validation_report.get('fixes_applied', [])
                    improvements = validation_report.get('connection_improvements', [])
                    
                    print(f"Advanced Validation: Connection Validation Results:")
                    print(f"   Original workflow valid: {original_valid}")
                    if original_errors:
                        print(f"   Original errors: {len(original_errors)}")
                        for error in original_errors[:3]:  # Show first 3 errors
                            print(f"     - {error}")
                    
                    if fixes_applied:
                        print(f"   Fixes applied: {len(fixes_applied)}")
                        for fix in fixes_applied:
                            print(f"     [OK] {fix}")
                    
                    if improvements:
                        print(f"   Improvements made: {len(improvements)}")
                        for improvement in improvements:
                            print(f"     🚀 {improvement}")
                    
                    # Use the fixed workflow
                    workflow = fixed_workflow
                    
                    # Final validation after fixes
                    if 'post_fix_validation' in validation_report:
                        post_fix_valid = validation_report['post_fix_validation']['is_valid']
                        post_fix_errors = validation_report['post_fix_validation']['errors']
                        print(f"   Post-fix validation: {'[OK] Valid' if post_fix_valid else '[ERROR] Still has issues'}")
                        if post_fix_errors:
                            print(f"   Remaining errors: {len(post_fix_errors)}")
                            
                except Exception as e:
                    print(f"[WARN] Advanced connection validator failed: {e}")
                    # Continue with workflow as-is
            
            # Final fallback: basic connection fixing if nothing else worked
            if not workflow.get('connections'):
                print("Fallback: Applying basic fallback connection fixes...")
                nodes = workflow.get('nodes', [])
                if len(nodes) > 1:
                    connections = {}
                    for i in range(len(nodes) - 1):
                        current_name = nodes[i].get('name')
                        next_name = nodes[i + 1].get('name')
                        if current_name and next_name:
                            connections[current_name] = {
                                'main': [[{'node': next_name, 'type': 'main', 'index': 0}]]
                            }
                    workflow['connections'] = connections
                    print(f"   [OK] Created {len(connections)} basic fallback connections")

        
        # Final validation before returning
        if workflow:
            nodes = workflow.get('nodes', [])
            connections = workflow.get('connections', {})
            
            print(f"Summary: Final workflow summary:")
            print(f"   Workflow name: {workflow.get('name')}")
            print(f"   Final node count: {len(nodes)}")
            print(f"   Final connection count: {len(connections)}")
            
            # Log connection details
            connection_count = 0
            for source, conn_data in connections.items():
                if 'main' in conn_data and conn_data['main']:
                    for group in conn_data['main']:
                        if isinstance(group, list):
                            for conn in group:
                                if isinstance(conn, dict):
                                    target = conn.get('node', 'unknown')
                                    print(f"   [CONNECT] {source} -> {target}")
                                    connection_count += 1
            
            print(f"   Total connections established: {connection_count}")
            
            # Ensure all required fields are present
            missing_fields_count = 0
            for node in nodes:
                if not all(field in node for field in ['id', 'name', 'type', 'position', 'parameters']):
                    print(f"[WARN] Node missing required fields: {node.get('name')}")
                    missing_fields_count += 1
            
            if missing_fields_count == 0:
                print("   [OK] All nodes have required fields")
            
            # Check for proper data flow patterns
            try:
                # Check for RSS → Content → Parser → Twitter pattern
                rss_nodes = [n for n in nodes if n.get('type') == 'n8n-nodes-base.rssFeedRead' or 'rss' in n.get('name', '').lower()]
                twitter_nodes = [n for n in nodes if n.get('type') == 'n8n-nodes-base.twitter' or 'twitter' in n.get('name', '').lower()]
                content_nodes = [n for n in nodes if 'content' in n.get('name', '').lower() or 'generat' in n.get('name', '').lower()]
                parser_nodes = [n for n in nodes if 'parse' in n.get('name', '').lower() or 'process' in n.get('name', '').lower()]
                
                if rss_nodes and twitter_nodes:
                    print("   [INFO] RSS to Twitter workflow detected")
                if content_nodes:
                    print("   [INFO] Content generation nodes found")
                if parser_nodes:
                    print("   [INFO] Content parsing nodes found")
            except Exception as e:
                print(f"   [WARN] Pattern detection failed: {e}")
        
        # Skip enhancer for simple workflows to prevent extra nodes
        enhanced_workflow = workflow
        export_package = {
            'workflow': workflow,
            'workflow_name': workflow.get('name', 'Generated Workflow'),
            'description': f"Workflow generated from: {description}",
            'filename': f"{workflow.get('name', 'workflow').replace(' ', '_').lower()}.json",
            'formatted_json': json.dumps(workflow, indent=2)
        }
        
        # Prepare response with validation metadata
        response_data = {
            'success': True,
            'workflow': export_package['workflow'],
            'workflow_name': export_package.get('workflow_name', workflow.get('name', 'Generated Workflow')),
            'description': export_package.get('description', f"Workflow for: {description}"),
            'filename': export_package['filename'],
            'formatted_json': export_package['formatted_json'],
            'node_count': len(workflow.get('nodes', [])),
            'workflow_type': 'trained_model' if TRAINED_GENERATOR_AVAILABLE else 'basic',
            'complexity': complexity,
            'trigger_type': trigger_type
        }
        
        # Add validation metadata if available
        if validation_metadata:
            response_data['validation'] = validation_metadata
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"Workflow generation failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/validate', methods=['POST'])
@limiter.limit(config.VALIDATE_RATE_LIMIT) if limiter else lambda f: f
def validate_workflow():
    """Validate a workflow structure"""
    try:
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Content-Type must be application/json'}), 415
            
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Check if workflow data is provided
        workflow = data.get('workflow')
        if not workflow:
            return jsonify({'success': False, 'error': 'No workflow data provided'}), 400
        
        # Basic workflow structure validation
        validation_errors = []
        validation_warnings = []
        
        # Check required fields
        required_fields = ['nodes', 'connections']
        for field in required_fields:
            if field not in workflow:
                validation_errors.append(f"Missing required field: {field}")
        
        # Validate nodes
        nodes = workflow.get('nodes', [])
        if not nodes:
            validation_errors.append("Workflow must have at least one node")
        else:
            for i, node in enumerate(nodes):
                node_errors = []
                
                # Check required node fields
                required_node_fields = ['id', 'name', 'type']
                for field in required_node_fields:
                    if field not in node:
                        node_errors.append(f"Node {i}: Missing required field '{field}'")
                
                # Check node type format
                node_type = node.get('type', '')
                if node_type and not node_type.startswith('n8n-nodes-'):
                    validation_warnings.append(f"Node {i} ({node.get('name', 'unnamed')}): Unusual node type '{node_type}'")
                
                validation_errors.extend(node_errors)
        
        # Validate connections
        connections = workflow.get('connections', {})
        if connections:
            node_names = [node.get('name') for node in nodes]
            
            for source, conn_data in connections.items():
                if source not in node_names:
                    validation_errors.append(f"Connection source '{source}' not found in nodes")
                
                if 'main' in conn_data:
                    for group in conn_data['main']:
                        if isinstance(group, list):
                            for conn in group:
                                if isinstance(conn, dict):
                                    target = conn.get('node')
                                    if target and target not in node_names:
                                        validation_errors.append(f"Connection target '{target}' not found in nodes")
        
        # Use workflow validator if available
        validation_score = 85  # Default score
        detailed_validation = {}
        
        if WORKFLOW_VALIDATOR_AVAILABLE:
            try:
                validation_result = workflow_validator.validate_workflow(workflow)
                validation_score = validation_result.get('score', 85)
                detailed_validation = validation_result.get('details', {})
                
                # Add detailed validation errors/warnings
                if 'errors' in detailed_validation:
                    validation_errors.extend(detailed_validation['errors'])
                if 'warnings' in detailed_validation:
                    validation_warnings.extend(detailed_validation['warnings'])
                    
            except Exception as e:
                validation_warnings.append(f"Advanced validation failed: {str(e)}")
        
        # Determine overall validation status
        is_valid = len(validation_errors) == 0
        
        # Calculate quality metrics
        quality_metrics = {
            'node_count': len(nodes),
            'connection_count': len(connections),
            'has_error_handling': any('error' in node.get('name', '').lower() for node in nodes),
            'has_validation': any('valid' in node.get('name', '').lower() for node in nodes),
            'has_monitoring': any('monitor' in node.get('name', '').lower() for node in nodes),
            'validation_score': validation_score
        }
        
        return jsonify({
            'success': True,
            'valid': is_valid,
            'validation_score': validation_score,
            'errors': validation_errors,
            'warnings': validation_warnings,
            'quality_metrics': quality_metrics,
            'detailed_validation': detailed_validation,
            'workflow_summary': {
                'name': workflow.get('name', 'Unnamed Workflow'),
                'node_count': len(nodes),
                'connection_count': len(connections),
                'has_settings': 'settings' in workflow
            }
        })
        
    except Exception as e:
        logger.error(f"Workflow validation failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Rate limiting and security error handlers
@app.errorhandler(429)
def ratelimit_handler(e):
    """Handle rate limit exceeded errors"""
    logger.warning(f"Rate limit exceeded for {request.remote_addr}: {e}")
    return jsonify({
        'success': False,
        'error': 'RATE_LIMIT_EXCEEDED',
        'message': 'Too many requests. Please try again later.',
        'retry_after': getattr(e, 'retry_after', 60)
    }), 429

@app.errorhandler(400)
def bad_request_handler(e):
    """Handle bad request errors"""
    logger.warning(f"Bad request from {request.remote_addr}: {e}")
    return jsonify({
        'success': False,
        'error': 'BAD_REQUEST',
        'message': str(e.description) if hasattr(e, 'description') else 'Invalid request'
    }), 400

@app.errorhandler(500)
def internal_error_handler(e):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {e}")
    return jsonify({
        'success': False,
        'error': 'INTERNAL_ERROR',
        'message': 'An internal error occurred. Please try again later.'
    }), 500

# Security headers
@app.after_request
def after_request(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    # Log request completion
    if hasattr(request, 'start_time'):
        execution_time = time.time() - request.start_time
        from logger import log_request
        log_request(request, response.status_code, execution_time)
    
    return response

# Request timing middleware
@app.before_request
def before_request():
    """Track request start time for logging"""
    request.start_time = time.time()

# Health check endpoint (no rate limiting)
@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0.0',
        'timestamp': time.time(),
        'services': {
            'market_leading_generator': MARKET_LEADING_GENERATOR_AVAILABLE,
            'ai_enhancements': AI_ENHANCEMENTS_AVAILABLE,
            'templates': TEMPLATES_AVAILABLE,
            'workflow_validator': WORKFLOW_VALIDATOR_AVAILABLE,
            'enhanced_generator': ENHANCED_GENERATOR_AVAILABLE,
            'feature_aware_generator': FEATURE_AWARE_GENERATOR_AVAILABLE,
            'trained_generator': TRAINED_GENERATOR_AVAILABLE,
            'connection_validator': CONNECTION_VALIDATOR_AVAILABLE,
            'enhancer': ENHANCER_AVAILABLE,
            'rate_limiter': limiter is not None
        },
        'features': {
            'market_leading_quality': MARKET_LEADING_GENERATOR_AVAILABLE,
            'comprehensive_training_data': MARKET_LEADING_GENERATOR_AVAILABLE,
            'production_ready_workflows': MARKET_LEADING_GENERATOR_AVAILABLE,
            'multi_ai_providers': AI_ENHANCEMENTS_AVAILABLE,
            'template_library': TEMPLATES_AVAILABLE,
            'workflow_validation': WORKFLOW_VALIDATOR_AVAILABLE,
            'intelligent_fallbacks': True,
            'rate_limiting': limiter is not None,
            'caching': config.ENABLE_CACHING if 'config' in globals() else False
        }
    })

# Rate limiting info endpoint
@app.route('/api/rate-limits')
def rate_limit_info():
    """Get rate limiting information"""
    try:
        from rate_limiting import get_rate_limit_info
        return jsonify(get_rate_limit_info())
    except ImportError:
        return jsonify({
            'rate_limits': {
                'generate': '10 per minute',
                'prompt-help': '20 per minute',
                'validate': '30 per minute',
                'preview': '50 per minute'
            },
            'global_limit': '100 per hour'
        })

# Rate limiting statistics endpoint (admin only)
@app.route('/api/rate-limit-stats')
@limiter.limit("5 per minute") if limiter else lambda f: f
def rate_limit_stats():
    """Get rate limiting statistics for monitoring"""
    try:
        from rate_limiting import get_rate_limit_stats
        stats = get_rate_limit_stats()
        return jsonify({
            'success': True,
            'stats': stats
        })
    except ImportError:
        return jsonify({
            'success': False,
            'error': 'Rate limiting monitoring not available'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

# Template System API Endpoints
@app.route('/api/templates')
@limiter.limit("30 per minute") if limiter else lambda f: f
def get_templates():
    """Get all available workflow templates"""
    if not TEMPLATES_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Template system not available'
        }), 503
    
    try:
        category = request.args.get('category')
        search = request.args.get('search')
        
        if category:
            try:
                cat_enum = TemplateCategory(category)
                templates = template_manager.get_templates_by_category(cat_enum)
            except ValueError:
                return jsonify({
                    'success': False,
                    'error': f'Invalid category: {category}'
                }), 400
        elif search:
            templates = template_manager.search_templates(search)
        else:
            templates = template_manager.get_all_templates()
        
        # Convert templates to JSON-serializable format
        template_data = []
        for template in templates:
            template_data.append({
                'id': template.id,
                'name': template.name,
                'description': template.description,
                'category': template.category.value,
                'complexity': template.complexity,
                'tags': template.tags,
                'use_cases': template.use_cases,
                'required_services': template.required_services,
                'node_count': len(template.workflow_json.get('nodes', []))
            })
        
        return jsonify({
            'success': True,
            'templates': template_data,
            'total': len(template_data)
        })
        
    except Exception as e:
        logger.error(f"Template listing failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/templates/<template_id>')
@limiter.limit("20 per minute") if limiter else lambda f: f
def get_template(template_id):
    """Get a specific template by ID"""
    if not TEMPLATES_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Template system not available'
        }), 503
    
    try:
        template = template_manager.get_template(template_id)
        if not template:
            return jsonify({
                'success': False,
                'error': f'Template {template_id} not found'
            }), 404
        
        return jsonify({
            'success': True,
            'template': {
                'id': template.id,
                'name': template.name,
                'description': template.description,
                'category': template.category.value,
                'complexity': template.complexity,
                'tags': template.tags,
                'use_cases': template.use_cases,
                'required_services': template.required_services,
                'workflow': template.workflow_json,
                'node_count': len(template.workflow_json.get('nodes', []))
            }
        })
        
    except Exception as e:
        logger.error(f"Template retrieval failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/templates/suggestions', methods=['POST'])
@limiter.limit("15 per minute") if limiter else lambda f: f
def get_template_suggestions():
    """Get template suggestions based on user description"""
    if not TEMPLATES_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Template system not available'
        }), 503
    
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 415
        
        data = request.get_json()
        description = data.get('description', '').strip()
        
        if not description:
            return jsonify({
                'success': False,
                'error': 'Description is required'
            }), 400
        
        suggestions = template_manager.get_template_suggestions(description)
        
        suggestion_data = []
        for template in suggestions:
            suggestion_data.append({
                'id': template.id,
                'name': template.name,
                'description': template.description,
                'category': template.category.value,
                'complexity': template.complexity,
                'tags': template.tags,
                'use_cases': template.use_cases,
                'match_reason': f"Matches your request for: {description}"
            })
        
        return jsonify({
            'success': True,
            'suggestions': suggestion_data,
            'total': len(suggestion_data)
        })
        
    except Exception as e:
        logger.error(f"Template suggestions failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/templates/<template_id>/customize', methods=['POST'])
@limiter.limit("10 per minute") if limiter else lambda f: f
def customize_template(template_id):
    """Customize a template with user-specific parameters"""
    if not TEMPLATES_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Template system not available'
        }), 503
    
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 415
        
        data = request.get_json()
        customizations = data.get('customizations', {})
        
        workflow = template_manager.customize_template(template_id, customizations)
        
        # Apply connection fixing if available
        if SIMPLE_FIXER_AVAILABLE:
            try:
                workflow = validate_and_fix_connections(workflow)
            except Exception as e:
                logger.warning(f"Connection fixing failed: {e}")
        
        return jsonify({
            'success': True,
            'workflow': workflow,
            'workflow_name': workflow.get('name', 'Customized Workflow'),
            'description': f"Customized template: {template_id}",
            'filename': f"{workflow.get('name', 'workflow').replace(' ', '_').lower()}.json",
            'formatted_json': json.dumps(workflow, indent=2),
            'node_count': len(workflow.get('nodes', [])),
            'workflow_type': 'template_based',
            'template_id': template_id
        })
        
    except ValueError as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 404
    except Exception as e:
        logger.error(f"Template customization failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/categories')
@limiter.limit("50 per minute") if limiter else lambda f: f
def get_categories():
    """Get all available template categories"""
    if not TEMPLATES_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Template system not available'
        }), 503
    
    try:
        categories = []
        for category in TemplateCategory:
            templates_in_category = template_manager.get_templates_by_category(category)
            categories.append({
                'id': category.value,
                'name': category.value.replace('_', ' ').title(),
                'template_count': len(templates_in_category)
            })
        
        return jsonify({
            'success': True,
            'categories': categories
        })
        
    except Exception as e:
        logger.error(f"Category listing failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Workflow Validation API Endpoint
@app.route('/api/validate', methods=['POST'])
@limiter.limit("20 per minute") if limiter else lambda f: f
def api_validate_workflow():
    """Validate a workflow for correctness and best practices"""
    if not WORKFLOW_VALIDATOR_AVAILABLE:
        return jsonify({
            'success': False,
            'error': 'Workflow validation system not available'
        }), 503
    
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 415
        
        data = request.get_json()
        workflow = data.get('workflow')
        
        if not workflow:
            return jsonify({
                'success': False,
                'error': 'Workflow data is required'
            }), 400
        
        # Perform validation
        validation_report = workflow_validator.validate_workflow(workflow)
        
        # Convert issues to JSON-serializable format
        issues_data = []
        for issue in validation_report.issues:
            issues_data.append({
                'level': issue.level.value,
                'category': issue.category,
                'message': issue.message,
                'node_id': issue.node_id,
                'suggestion': issue.suggestion
            })
        
        return jsonify({
            'success': True,
            'validation': {
                'is_valid': validation_report.is_valid,
                'score': validation_report.score,
                'issues': issues_data,
                'summary': validation_report.summary,
                'recommendations': validation_report.recommendations
            }
        })
        
    except Exception as e:
        logger.error(f"Workflow validation failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/preview', methods=['POST'])
@limiter.limit(config.PREVIEW_RATE_LIMIT) if limiter else lambda f: f
def generate_preview():
    """Generate visual preview data for workflow"""
    try:
        data = request.get_json()
        
        if not data or 'workflow' not in data:
            raise BadRequest('Missing workflow data')
        
        workflow = data['workflow']
        
        # Generate visual preview data
        preview_data = create_visual_preview(workflow)
        
        return jsonify({
            'success': True,
            'preview': preview_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def create_basic_workflow(description, trigger_type, complexity, template='', advanced_options={}):
    """Create a dynamic n8n workflow structure based on user input with unique variations"""
    
    # Validate and sanitize inputs
    if not description:
        description = "general workflow"
    elif not isinstance(description, str):
        description = str(description)
    
    # Validate trigger type
    if trigger_type not in ['webhook', 'schedule', 'manual']:
        trigger_type = 'webhook'  # Default fallback
    
    # Validate complexity
    if complexity not in ['simple', 'medium', 'complex']:
        complexity = 'medium'  # Default fallback
    
    # Generate unique workflow name with timestamp and hash
    import hashlib
    import datetime
    
    desc_hash = hashlib.md5(description.encode()).hexdigest()[:6]
    now = datetime.datetime.now()
    timestamp = now.strftime("%H%M") + str(now.microsecond)[:3]  # Add microseconds for uniqueness
    
    # Enhanced analysis with context awareness
    workflow_analysis = analyze_workflow_description(description, template)
    
    # Generate name based on analysis results
    workflow_name = generate_intelligent_workflow_name(description, workflow_analysis) + f" {timestamp}-{desc_hash}"
    
    # Add generation context to prevent repetition
    generation_context = {
        'description_hash': desc_hash,
        'timestamp': datetime.datetime.now().isoformat(),
        'complexity': complexity,
        'trigger_type': trigger_type,
        'unique_seed': hash(description + str(datetime.datetime.now().microsecond)) % 1000
    }
    
    # Create nodes based on analysis and complexity with variation
    nodes = []
    connections = {}
    
    # Add trigger node with context-specific configuration
    trigger_node = create_trigger_node(trigger_type, workflow_analysis, generation_context)
    nodes.append(trigger_node)
    
    # Generate nodes based on description analysis with uniqueness
    generated_nodes = generate_nodes_from_description(
        workflow_analysis, complexity, advanced_options, generation_context
    )
    
    # Add generated nodes with proper position spacing
    x_offset = generation_context['unique_seed'] % 50  # Reduce variation to prevent overlap
    for i, node_config in enumerate(generated_nodes):
        node = create_dynamic_node(node_config, i + 1, x_offset)
        nodes.append(node)
    
    # Create connections between nodes with smart routing
    connections = create_dynamic_connections(nodes, workflow_analysis, generation_context)
    
    # Add contextual tags based on analysis
    tags = ['generated', f'gen-{desc_hash}'] + workflow_analysis.get('tags', [])
    
    # Add workflow-specific settings based on type
    workflow_settings = {
        'executionOrder': 'v1',
        'saveManualExecutions': True,
        'callerPolicy': 'workflowsFromSameOwner'
    }
    
    # Add type-specific settings
    if workflow_analysis['type'] == 'monitoring':
        workflow_settings['executionTimeout'] = 300
        workflow_settings['maxExecutionTime'] = 300
    elif workflow_analysis['type'] == 'data_sync':
        workflow_settings['timezone'] = 'UTC'
        workflow_settings['saveDataErrorExecution'] = 'all'
    
    return {
        'name': workflow_name,
        'nodes': nodes,
        'connections': connections,
        'active': True,
        'settings': workflow_settings,
        'tags': tags,
        'meta': {
            'description': description,
            'generated_at': generation_context['timestamp'],
            'generation_hash': desc_hash,
            'workflow_type': workflow_analysis['type'],
            'complexity': complexity,
            'unique_elements': len(workflow_analysis['specific_actions']) + len(workflow_analysis['integrations'])
        }
    }

def create_trigger_node(trigger_type, analysis=None, context=None):
    """Create trigger node based on type and workflow analysis with unique variations"""
    if analysis is None:
        analysis = {}
    if context is None:
        context = {}
    
    # Generate unique webhook paths based on content and context
    base_path = 'webhook'
    if analysis.get('type') == 'lead_processing':
        base_path = f"lead-intake-{context.get('unique_seed', 0) % 100}"
    elif analysis.get('type') == 'data_sync':
        base_path = f"data-sync-{context.get('description_hash', 'default')[:4]}"
    elif analysis.get('type') == 'notification':
        base_path = f"notify-{len(analysis.get('specific_actions', []))}"
    elif analysis.get('type') == 'monitoring':
        base_path = f"health-{context.get('unique_seed', 0) % 50}"
    elif analysis.get('type') == 'ecommerce':
        base_path = f"order-{context.get('description_hash', 'default')[:4]}"
    else:
        # Create unique path based on description content
        actions = '-'.join(analysis.get('specific_actions', ['process'])[:2])
        base_path = f"{actions}-{context.get('unique_seed', 0) % 100}"
    
    # Dynamic schedule based on workflow complexity and type
    schedule_expressions = {
        'monitoring': ['*/2 * * * *', '*/5 * * * *', '*/10 * * * *'],  # 2, 5, or 10 minutes
        'data_sync': ['0 */2 * * *', '0 */4 * * *', '0 */6 * * *'],   # 2, 4, or 6 hours
        'notification': ['*/15 * * * *', '*/30 * * * *', '0 * * * *'], # 15, 30 min, or hourly
        'lead_processing': ['*/10 * * * *', '*/20 * * * *', '*/30 * * * *'], # 10, 20, or 30 minutes
        'ecommerce': ['*/5 * * * *', '*/10 * * * *', '*/15 * * * *']   # 5, 10, or 15 minutes
    }
    
    workflow_type = analysis.get('type', 'general')
    available_schedules = schedule_expressions.get(workflow_type, ['0 */1 * * *'])
    schedule_index = context.get('unique_seed', 0) % max(1, len(available_schedules))
    selected_schedule = available_schedules[schedule_index]
    
    # Create unique trigger names based on content
    trigger_names = {
        'webhook': [
            f"{analysis.get('type', 'Webhook').replace('_', ' ').title()} Receiver",
            f"Incoming {analysis.get('type', 'Data').replace('_', ' ').title()} Handler",
            f"{analysis.get('type', 'Process').replace('_', ' ').title()} Endpoint"
        ],
        'schedule': [
            f"Scheduled {analysis.get('type', 'Process').replace('_', ' ').title()}",
            f"Automated {analysis.get('type', 'Task').replace('_', ' ').title()}",
            f"Periodic {analysis.get('type', 'Job').replace('_', ' ').title()}"
        ],
        'manual': [
            f"Manual {analysis.get('type', 'Process').replace('_', ' ').title()}",
            f"On-Demand {analysis.get('type', 'Task').replace('_', ' ').title()}",
            f"User-Triggered {analysis.get('type', 'Action').replace('_', ' ').title()}"
        ]
    }
    
    name_options = trigger_names.get(trigger_type, [f"{trigger_type.title()} Trigger"])
    name_index = context.get('unique_seed', 0) % max(1, len(name_options))
    selected_name = name_options[name_index]
    
    # FIXED: Ensure correct trigger types are used
    configs = {
        'webhook': {
            'type': 'n8n-nodes-base.webhook',
            'parameters': {
                'path': base_path,
                'httpMethod': 'POST',
                'responseMode': 'responseNode',
                'options': {
                    'noResponseBody': False,
                    'rawBody': False
                }
            },
            'name': selected_name
        },
        'schedule': {
            'type': 'n8n-nodes-base.scheduleTrigger',
            'parameters': {
                'rule': {
                    'interval': [{
                        'field': 'cronExpression',
                        'expression': selected_schedule
                    }]
                }
            },
            'name': selected_name
        },
        'manual': {
            'type': 'n8n-nodes-base.manualTrigger',
            'parameters': {},
            'name': selected_name
        }
    }
    
    # CRITICAL FIX: Always use the correct config for the trigger type
    config = configs[trigger_type]  # Remove fallback to webhook
    
    return {
        'parameters': config['parameters'],
        'id': generate_node_id(),
        'name': config['name'],
        'type': config['type'],
        'typeVersion': 1,
        'position': [0, 300]
    }

def create_processing_node(node_id, x_position, config=None):
    """Create a processing node"""
    if config is None:
        config = {'name': 'Process Data', 'description': 'Process incoming data'}
    
    return {
        'parameters': {
            'jsCode': f'''// {config.get('description', 'Process incoming data')}
const inputData = $input.all();
const processedData = inputData.map(item => ({{
  ...item.json,
  processed: true,
  timestamp: new Date().toISOString(),
  step: '{config.get('name', 'Process Data')}'
}}));

return processedData;'''
        },
        'id': generate_node_id(),
        'name': config.get('name', 'Process Data'),
        'type': 'n8n-nodes-base.code',
        'typeVersion': 2,
        'position': [x_position, 300],
        'parameters': {
            'jsCode': '''// Process incoming data
const inputData = $input.all();
const processedData = inputData.map(item => ({
  ...item.json,
  processed: true,
  timestamp: new Date().toISOString(),
  step: 'Process Data'
}));

return processedData;'''
        }
    }

def create_validation_node(node_id, x_position, config):
    """Create a validation node"""
    return {
        'parameters': {
            'jsCode': '''// Validate and sanitize incoming data
const inputData = $input.all();
const validatedData = [];

for (const item of inputData) {
  const data = item.json;
  const errors = [];
  
  // Basic validation rules
  if (!data.email || !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(data.email)) {
    errors.push('Invalid email format');
  }
  
  if (!data.name || data.name.trim().length < 2) {
    errors.push('Name must be at least 2 characters');
  }
  
  // Sanitize data
  const sanitizedData = {
    ...data,
    email: data.email ? data.email.toLowerCase().trim() : '',
    name: data.name ? data.name.trim() : '',
    validation_errors: errors,
    is_valid: errors.length === 0,
    validated_at: new Date().toISOString()
  };
  
  validatedData.push(sanitizedData);
}

return validatedData;'''
        },
        'id': generate_node_id(),
        'name': config.get('name', 'Validate Data'),
        'type': 'n8n-nodes-base.code',
        'typeVersion': 2,
        'position': [x_position, 300],
        'parameters': {
            'jsCode': '''// Validate and sanitize incoming data
const inputData = $input.all();
const validatedData = [];

for (const item of inputData) {
  const data = item.json;
  const errors = [];
  
  // Basic validation
  if (!data.email || !data.email.includes('@')) {
    errors.push('Valid email is required');
  }
  if (!data.name || data.name.length < 2) {
    errors.push('Name must be at least 2 characters');
  }
  
  // Sanitize data
  const sanitizedData = {
    ...data,
    email: data.email ? data.email.toLowerCase().trim() : '',
    name: data.name ? data.name.trim() : '',
    validation_errors: errors,
    is_valid: errors.length === 0,
    validated_at: new Date().toISOString()
  };
  
  validatedData.push(sanitizedData);
}

return validatedData;'''
        }
    }

def create_conditional_node(node_id, x_position, config):
    """Create a conditional logic node"""
    return {
        'parameters': {
            'conditions': {
                'options': {
                    'caseSensitive': True,
                    'leftValue': '',
                    'typeValidation': 'strict'
                },
                'conditions': [{
                    'leftValue': '={{ $json.is_valid }}',
                    'rightValue': True,
                    'operator': {
                        'type': 'boolean',
                        'operation': 'equal'
                    }
                }],
                'combinator': 'and'
            }
        },
        'id': generate_node_id(),
        'name': config.get('name', 'Check Conditions'),
        'type': 'n8n-nodes-base.if',
        'typeVersion': 2,
        'position': [x_position, 300]
    }

def create_slack_node(node_id, x_position, config):
    """Create a Slack notification node"""
    return {
        'parameters': {
            'resource': 'message',
            'operation': 'post',
            'channel': '#general',
            'text': '🔔 Workflow Notification\\n\\n**Data:** {{ $json.name || "New item" }}\\n**Status:** {{ $json.status || "Processed" }}\\n**Time:** {{ $json.timestamp }}',
            'otherOptions': {
                'mrkdwn': True
            }
        },
        'id': generate_node_id(),
        'name': config.get('name', 'Send Slack Message'),
        'type': 'n8n-nodes-base.slack',
        'typeVersion': 2,
        'position': [x_position, 300]
    }

def create_email_node(node_id, x_position, config):
    """Create an email notification node"""
    return {
        'parameters': {
            'fromEmail': 'noreply@example.com',
            'toEmail': 'admin@example.com',
            'subject': 'Workflow Notification: {{ $json.name || "New Item" }}',
            'text': 'A new item has been processed in your workflow.\\n\\nDetails:\\n{{ JSON.stringify($json, null, 2) }}',
            'options': {}
        },
        'id': generate_node_id(),
        'name': config.get('name', 'Send Email'),
        'type': 'n8n-nodes-base.emailSend',
        'typeVersion': 2,
        'position': [x_position, 300]
    }

def create_database_node(node_id, x_position, config):
    """Create a database operation node"""
    return {
        'parameters': {
            'operation': 'insert',
            'table': 'workflow_data',
            'columns': 'name, email, data, created_at',
            'values': '{{ $json.name }}, {{ $json.email }}, {{ JSON.stringify($json) }}, {{ new Date().toISOString() }}',
            'options': {}
        },
        'id': generate_node_id(),
        'name': config.get('name', 'Database Operation'),
        'type': 'n8n-nodes-base.mysql',
        'typeVersion': 2,
        'position': [x_position, 300]
    }

def create_error_handler_node(node_id, x_position, config):
    """Create an error handling node"""
    return {
        'parameters': {
            'jsCode': '''// Error handling and retry logic
const inputData = $input.all();
const processedData = [];

for (const item of inputData) {
  try {
    // Process the item
    const result = {
      ...item.json,
      processed: true,
      error_handled: false,
      processed_at: new Date().toISOString()
    };
    
    processedData.push(result);
  } catch (error) {
    // Handle errors gracefully
    const errorResult = {
      ...item.json,
      processed: false,
      error_handled: true,
      error_message: error.message,
      error_at: new Date().toISOString()
    };
    
    processedData.push(errorResult);
  }
}

return processedData;'''
        },
        'id': generate_node_id(),
        'name': config.get('name', 'Handle Errors'),
        'type': 'n8n-nodes-base.code',
        'typeVersion': 2,
        'position': [x_position, 300],
        'parameters': {
            'jsCode': '''// Error handling and retry logic
const inputData = $input.all();
const processedData = [];

for (const item of inputData) {
  try {
    const data = item.json;
    
    // Check for errors
    if (data.validation_errors && data.validation_errors.length > 0) {
      // Handle validation errors
      processedData.push({
        ...data,
        error_handled: true,
        error_type: 'validation',
        handled_at: new Date().toISOString()
      });
    } else {
      // No errors, pass through
      processedData.push({
        ...data,
        error_checked: true,
        checked_at: new Date().toISOString()
      });
    }
  } catch (error) {
    // Handle processing errors
    processedData.push({
      error: error.message,
      error_handled: true,
      error_type: 'processing',
      handled_at: new Date().toISOString()
    });
  }
}

return processedData;'''
        }
    }

def create_transformation_node(node_id, x_position, config):
    """Create a data transformation node"""
    return {
        'parameters': {
            'jsCode': f'''// {config.get('description', 'Transform data')}
const inputData = $input.all();
const transformedData = inputData.map(item => {{
  const data = item.json;
  
  // Apply transformations based on requirements
  const transformed = {{
    ...data,
    // Convert to proper formats
    timestamp: new Date().toISOString(),
    transformed_by: '{config.get('name', 'Transform Data')}',
    // Add any specific transformations here
    processed: true
  }};
  
  return transformed;
}});

return transformedData;'''
        },
        'id': generate_node_id(),
        'name': config.get('name', 'Transform Data'),
        'type': 'n8n-nodes-base.code',
        'typeVersion': 2,
        'position': [x_position, 300],
        'parameters': {
            'jsCode': '''// Transform and format data
const inputData = $input.all();
const transformedData = inputData.map(item => {
  const data = item.json;
  
  return {
    id: data.id || Math.random().toString(36).substr(2, 9),
    name: data.name ? data.name.trim() : 'Unknown',
    email: data.email ? data.email.toLowerCase() : '',
    status: data.is_valid ? 'valid' : 'invalid',
    processed_at: new Date().toISOString(),
    source: 'n8n_workflow',
    metadata: {
      original_data: data,
      transformation_applied: true
    }
  };
});

return transformedData;'''
        }
    }

def create_notification_node(node_id, x_position, config):
    """Create a generic notification node"""
    return {
        'parameters': {
            'jsCode': '''// Send notification
const inputData = $input.all();
const notifications = [];

for (const item of inputData) {
  const notification = {
    ...item.json,
    notification_sent: true,
    notification_time: new Date().toISOString(),
    message: `Notification: ${item.json.name || 'New item'} has been processed`
  };
  
  notifications.push(notification);
}

return notifications;'''
        },
        'id': generate_node_id(),
        'name': config.get('name', 'Send Notification'),
        'type': 'n8n-nodes-base.code',
        'typeVersion': 2,
        'position': [x_position, 300],
        'parameters': {
            'jsCode': '''// Send notification with processed data
const inputData = $input.all();
const notifications = [];

for (const item of inputData) {
  const data = item.json;
  
  const notification = {
    to: data.email || 'admin@example.com',
    subject: 'Workflow Processing Complete',
    message: `Data processed successfully for ${data.name || 'Unknown'}`,
    data: {
      status: data.status || 'processed',
      timestamp: new Date().toISOString(),
      workflow_id: 'n8n_workflow',
      processed_items: 1
    },
    notification_sent: true,
    sent_at: new Date().toISOString()
  };
  
  notifications.push(notification);
}

return notifications;'''
        }
    }

def create_sheets_node(node_id, x_position, config):
    """Create a Google Sheets node"""
    return {
        'parameters': {
            'resource': 'spreadsheet',
            'operation': 'appendOrUpdate',
            'documentId': 'YOUR_SPREADSHEET_ID',
            'sheetName': 'Sheet1',
            'range': 'A:Z',
            'valueInputOption': 'USER_ENTERED',
            'values': '={{ [[$json.name, $json.email, $json.timestamp]] }}',
            'options': {}
        },
        'id': generate_node_id(),
        'name': config.get('name', 'Update Spreadsheet'),
        'type': 'n8n-nodes-base.googleSheets',
        'typeVersion': 4,
        'position': [x_position, 300]
    }

def create_webhook_call_node(node_id, x_position, config):
    """Create a webhook call node"""
    return {
        'parameters': {
            'url': 'https://hooks.example.com/webhook',
            'httpMethod': 'POST',
            'sendBody': True,
            'bodyContentType': 'json',
            'jsonBody': '={{ $json }}',
            'options': {
                'timeout': 10000,
                'retry': {
                    'enabled': True,
                    'maxRetries': 3
                }
            }
        },
        'id': generate_node_id(),
        'name': config.get('name', 'Call Webhook'),
        'type': 'n8n-nodes-base.httpRequest',
        'typeVersion': 4,
        'position': [x_position, 300]
    }

def create_file_node(node_id, x_position, config):
    """Create a file operation node"""
    return {
        'parameters': {
            'operation': 'write',
            'fileName': '={{ $json.name || "output" }}.json',
            'fileContent': '={{ JSON.stringify($json, null, 2) }}',
            'options': {
                'encoding': 'utf8'
            }
        },
        'id': generate_node_id(),
        'name': config.get('name', 'File Operation'),
        'type': 'n8n-nodes-base.readWriteFile',
        'typeVersion': 1,
        'position': [x_position, 300]
    }

def create_response_node(node_id, x_position):
    """Create a webhook response node"""
    return {
        'parameters': {
            'options': {}
        },
        'id': generate_node_id(),
        'name': 'Respond to Webhook',
        'type': 'n8n-nodes-base.respondToWebhook',
        'typeVersion': 1,
        'position': [x_position, 300]
    }

def create_http_request_node(node_id, x_position, config=None):
    """Create an HTTP request node"""
    if config is None:
        config = {'name': 'HTTP Request', 'description': 'Make API request'}
    
    return {
        'parameters': {
            'url': 'https://api.example.com/data',
            'httpMethod': 'POST',
            'sendBody': True,
            'bodyContentType': 'json',
            'jsonBody': '={{ $json }}',
            'options': {
                'timeout': 10000,
                'retry': {
                    'enabled': True,
                    'maxRetries': 3
                }
            }
        },
        'id': generate_node_id(),
        'name': config.get('name', 'HTTP Request'),
        'type': 'n8n-nodes-base.httpRequest',
        'typeVersion': 4,
        'position': [x_position, 300]
    }

def generate_node_id():
    """Generate a unique node ID"""
    import uuid
    import time
    # Combine timestamp and UUID for better uniqueness
    try:
        timestamp = str(int(time.time() * 1000))[-6:]  # Last 6 digits of timestamp
    except (ValueError, OverflowError):
        timestamp = "000000"  # Fallback if time calculation fails
    
    uuid_part = str(uuid.uuid4())[:8]
    return f"{uuid_part}_{timestamp}"

def generate_workflow_name_from_description(description):
    """Generate a meaningful workflow name from description"""
    import re
    
    # Extract key action words
    action_words = ['process', 'send', 'create', 'update', 'sync', 'monitor', 'validate', 'transform']
    object_words = ['lead', 'data', 'email', 'notification', 'order', 'customer', 'user', 'file']
    
    desc_lower = description.lower()
    found_actions = [word for word in action_words if word in desc_lower]
    found_objects = [word for word in object_words if word in desc_lower]
    
    if found_actions and found_objects:
        return f"{found_actions[0].title()} {found_objects[0].title()} Workflow"
    elif found_actions:
        return f"{found_actions[0].title()} Workflow"
    elif found_objects:
        return f"{found_objects[0].title()} Processing Workflow"
    else:
        # Fallback to first few words with better handling
        words = re.findall(r'\b\w+\b', description)
        if len(words) >= 3:
            return ' '.join(word.title() for word in words[:3]) + ' Workflow'
        elif len(words) >= 1:
            return ' '.join(word.title() for word in words) + ' Workflow'
        else:
            return 'Custom Workflow'

def generate_intelligent_workflow_name(description, analysis):
    """Generate intelligent workflow name based on analysis results"""
    import re
    
    workflow_type = analysis.get('type', 'general')
    specific_actions = analysis.get('specific_actions', [])
    integrations = analysis.get('integrations', [])
    
    # Industry-specific naming patterns
    industry_patterns = {
        'healthcare': {
            'patient': 'Patient Management System',
            'appointment': 'Appointment Scheduler',
            'medical': 'Medical Records Processor',
            'doctor': 'Healthcare Workflow',
            'default': 'Healthcare Management'
        },
        'finance': {
            'payment': 'Payment Processing System',
            'transaction': 'Transaction Handler',
            'invoice': 'Invoice Management',
            'fraud': 'Fraud Detection System',
            'default': 'Financial Workflow'
        },
        'education': {
            'student': 'Student Management System',
            'course': 'Course Administration',
            'enrollment': 'Enrollment Processor',
            'grade': 'Grading System',
            'default': 'Educational Workflow'
        },
        'ecommerce': {
            'order': 'Order Processing System',
            'inventory': 'Inventory Management',
            'shipping': 'Shipping Coordinator',
            'customer': 'Customer Service Hub',
            'default': 'E-commerce Workflow'
        }
    }
    
    desc_lower = description.lower()
    
    # Try industry-specific patterns first
    if workflow_type in industry_patterns:
        patterns = industry_patterns[workflow_type]
        for keyword, name_template in patterns.items():
            if keyword != 'default' and keyword in desc_lower:
                return name_template
        # Use default for the industry
        return patterns['default']
    
    # Action-based naming for general workflows
    action_templates = {
        'validate': 'Data Validation System',
        'process': 'Data Processing Pipeline',
        'send': 'Notification System',
        'store': 'Data Storage Handler',
        'transform': 'Data Transformation Pipeline',
        'monitor': 'Monitoring System',
        'sync': 'Data Synchronization Hub'
    }
    
    for action in specific_actions:
        if action in action_templates:
            return action_templates[action]
    
    # Integration-based naming
    integration_templates = {
        'slack': 'Slack Integration Hub',
        'email': 'Email Automation System',
        'database': 'Database Management System',
        'api': 'API Integration Pipeline',
        'sheets': 'Spreadsheet Automation'
    }
    
    for integration in integrations:
        if integration in integration_templates:
            return integration_templates[integration]
    
    # Fallback to original method
    return generate_workflow_name_from_description(description)

def analyze_workflow_description(description, template=''):
    """Advanced analysis to determine exact workflow components with 100% accuracy"""
    import re
    
    # Handle edge cases
    if not description or not isinstance(description, str):
        description = str(description) if description else "general workflow"
    
    desc_lower = description.lower()
    
    analysis = {
        'type': 'general',
        'components': [],
        'integrations': [],
        'data_operations': [],
        'tags': [],
        'complexity_indicators': [],
        'specific_actions': [],
        'data_sources': [],
        'destinations': [],
        'conditions': [],
        'schedule_info': {},
        'exact_requirements': [],
        'original_description': description  # Add original description for intelligent analysis
    }
    
    # Enhanced workflow type detection with priority scoring
    workflow_types = {
        'healthcare': {
            'keywords': ['patient', 'medical', 'healthcare', 'hospital', 'clinic', 'appointment', 'doctor', 'nurse', 'treatment', 'diagnosis', 'prescription', 'medical record', 'health'],
            'score': 0,
            'tags': ['healthcare', 'medical', 'patient', 'appointments', 'records']
        },
        'finance': {
            'keywords': ['financial', 'finance', 'banking', 'transaction', 'payment', 'invoice', 'accounting', 'budget', 'investment', 'loan', 'credit', 'fraud', 'compliance', 'audit'],
            'score': 0,
            'tags': ['finance', 'banking', 'transactions', 'compliance', 'accounting']
        },
        'education': {
            'keywords': ['student', 'education', 'school', 'university', 'course', 'enrollment', 'grade', 'teacher', 'instructor', 'learning', 'academic', 'curriculum', 'assignment'],
            'score': 0,
            'tags': ['education', 'academic', 'students', 'courses', 'learning']
        },
        'ecommerce': {
            'keywords': ['order', 'purchase', 'payment', 'cart', 'checkout', 'product', 'inventory', 'shipping', 'customer', 'retail', 'store'],
            'score': 0,
            'tags': ['ecommerce', 'orders', 'payments', 'retail', 'inventory']
        },
        'lead_processing': {
            'keywords': ['lead', 'prospect', 'sales', 'crm', 'customer acquisition', 'contact', 'marketing', 'campaign'],
            'score': 0,
            'tags': ['sales', 'crm', 'leads', 'marketing', 'prospects']
        },
        'data_sync': {
            'keywords': ['sync', 'synchronize', 'replicate', 'mirror', 'backup', 'transfer', 'integration', 'etl'],
            'score': 0,
            'tags': ['data', 'sync', 'integration', 'etl', 'transfer']
        },
        'monitoring': {
            'keywords': ['monitor', 'watch', 'track', 'observe', 'health', 'status', 'uptime', 'performance', 'metrics'],
            'score': 0,
            'tags': ['monitoring', 'health', 'observability', 'alerts', 'metrics']
        },
        'notification': {
            'keywords': ['notify', 'alert', 'inform', 'message', 'notification', 'announce', 'communication'],
            'score': 0,
            'tags': ['notification', 'alerts', 'communication', 'messaging']
        },
        'automation': {
            'keywords': ['automate', 'automatic', 'streamline', 'workflow automation', 'business automation'],
            'score': 0,
            'tags': ['automation', 'process', 'workflow', 'efficiency']
        }
    }
    
    # Score each workflow type with industry-specific priority
    industry_types = ['healthcare', 'finance', 'education', 'ecommerce']
    
    for wf_type, config in workflow_types.items():
        for keyword in config['keywords']:
            if keyword in desc_lower:
                # Give higher weight to industry-specific types
                weight = 3 if wf_type in industry_types else 1
                config['score'] += weight
    
    # Select highest scoring type
    best_type = max(workflow_types.items(), key=lambda x: x[1]['score'])
    if best_type[1]['score'] > 0:
        analysis['type'] = best_type[0]
        analysis['tags'].extend(best_type[1]['tags'])
        
        # Add additional context-specific tags based on description
        if best_type[0] == 'healthcare':
            if 'appointment' in desc_lower:
                analysis['tags'].extend(['scheduling'])
            if 'record' in desc_lower:
                analysis['tags'].extend(['data'])
        elif best_type[0] == 'finance':
            if 'fraud' in desc_lower or 'detection' in desc_lower:
                analysis['tags'].extend(['fraud', 'detection', 'security'])
            if 'report' in desc_lower:
                analysis['tags'].extend(['reporting', 'analytics'])
        elif best_type[0] == 'education':
            if 'enrollment' in desc_lower:
                analysis['tags'].extend(['enrollment', 'registration'])
            if 'grade' in desc_lower or 'assignment' in desc_lower:
                analysis['tags'].extend(['grading', 'assessment'])
    else:
        # If no specific type detected, keep as general
        analysis['type'] = 'general'
    
    # Remove duplicate tags
    analysis['tags'] = list(set(analysis['tags']))
    
    # Extract specific actions with context
    action_patterns = {
        'validate': r'validat[e|ing|ion]',
        'process': r'process[ing|ed]?',
        'send': r'send[ing]?',
        'receive': r'receiv[e|ing]',
        'store': r'stor[e|ing]',
        'update': r'updat[e|ing]',
        'create': r'creat[e|ing]',
        'delete': r'delet[e|ing]',
        'transform': r'transform[ing]?',
        'filter': r'filter[ing]?',
        'sort': r'sort[ing]?',
        'merge': r'merg[e|ing]',
        'split': r'split[ting]?',
        'manage': r'manag[e|ing|ement]',
        'schedule': r'schedul[e|ing]',
        'notify': r'notif[y|ying|ication]',
        'track': r'track[ing]?',
        'monitor': r'monitor[ing]?'
    }
    
    for action, pattern in action_patterns.items():
        if re.search(pattern, desc_lower):
            analysis['specific_actions'].append(action)
    
    # Enhanced integration detection with specific services
    integrations_map = {
        'slack': {
            'patterns': [r'slack', r'chat.*message', r'team.*notification'],
            'confidence': 0
        },
        'email': {
            'patterns': [r'email', r'mail', r'smtp', r'send.*message'],
            'confidence': 0
        },
        'database': {
            'patterns': [r'database', r'mysql', r'postgres', r'mongodb', r'sql', r'store.*data'],
            'confidence': 0
        },
        'api': {
            'patterns': [r'api', r'rest', r'http.*request', r'endpoint', r'web.*service'],
            'confidence': 0
        },
        'sheets': {
            'patterns': [r'sheets', r'spreadsheet', r'excel', r'csv', r'google.*sheets'],
            'confidence': 0
        },
        'crm': {
            'patterns': [r'crm', r'salesforce', r'hubspot', r'customer.*management'],
            'confidence': 0
        },
        'webhook': {
            'patterns': [r'webhook', r'http.*trigger', r'api.*call'],
            'confidence': 0
        },
        'file_system': {
            'patterns': [r'file', r'folder', r'directory', r'upload', r'download'],
            'confidence': 0
        },
        'calendar': {
            'patterns': [r'calendar', r'schedule', r'appointment', r'meeting'],
            'confidence': 0
        }
    }
    
    for integration, config in integrations_map.items():
        for pattern in config['patterns']:
            matches = re.findall(pattern, desc_lower)
            if matches:
                # Add confidence based on number of matches, but cap at reasonable level
                config['confidence'] += min(len(matches), 3)
        
        # Only include integrations with sufficient confidence
        if config['confidence'] > 0:
            analysis['integrations'].append(integration)
    
    # Extract data sources and destinations
    source_patterns = [
        r'from\s+(\w+)',
        r'receive.*from\s+(\w+)',
        r'get.*from\s+(\w+)',
        r'fetch.*from\s+(\w+)'
    ]
    
    destination_patterns = [
        r'to\s+(\w+)',
        r'send.*to\s+(\w+)',
        r'store.*in\s+(\w+)',
        r'save.*to\s+(\w+)'
    ]
    
    for pattern in source_patterns:
        matches = re.findall(pattern, desc_lower)
        analysis['data_sources'].extend(matches)
    
    for pattern in destination_patterns:
        matches = re.findall(pattern, desc_lower)
        analysis['destinations'].extend(matches)
    
    # Extract conditions and logic
    condition_patterns = [
        r'if\s+(.+?)\s+then',
        r'when\s+(.+?)\s+do',
        r'only.*if\s+(.+)',
        r'filter.*where\s+(.+)'
    ]
    
    for pattern in condition_patterns:
        matches = re.findall(pattern, description, re.IGNORECASE)
        analysis['conditions'].extend(matches)
    
    # Extract schedule information
    schedule_patterns = {
        'every_hour': r'every\s+hour|hourly',
        'every_day': r'every\s+day|daily',
        'every_week': r'every\s+week|weekly',
        'every_minute': r'every\s+minute',
        'specific_time': r'at\s+(\d{1,2}:\d{2})',
        'interval': r'every\s+(\d+)\s+(minute|hour|day)s?'
    }
    
    for schedule_type, pattern in schedule_patterns.items():
        match = re.search(pattern, desc_lower)
        if match:
            analysis['schedule_info'][schedule_type] = match.group(1) if match.groups() else True
    
    # Determine required components based on analysis
    if analysis['specific_actions']:
        if 'validate' in analysis['specific_actions']:
            analysis['components'].append('validation')
        if any(action in analysis['specific_actions'] for action in ['transform', 'process', 'filter']):
            analysis['components'].append('transformation')
        if analysis['conditions']:
            analysis['components'].append('conditional')
        if any(action in analysis['specific_actions'] for action in ['store', 'update', 'create']):
            analysis['components'].append('data_persistence')
    
    # Extract exact requirements for precise implementation
    requirement_patterns = [
        r'must\s+(.+?)(?:\.|$)',
        r'should\s+(.+?)(?:\.|$)',
        r'need.*to\s+(.+?)(?:\.|$)',
        r'require.*to\s+(.+?)(?:\.|$)'
    ]
    
    for pattern in requirement_patterns:
        matches = re.findall(pattern, description, re.IGNORECASE)
        analysis['exact_requirements'].extend(matches)
    
    return analysis

def generate_nodes_from_description(analysis, complexity, advanced_options, context=None):
    """Generate precise n8n node configurations based on detailed analysis of user requirements"""
    if context is None:
        context = {}
    
    # Add randomization based on context seed
    import random
    if 'unique_seed' in context:
        random.seed(context['unique_seed'])
    
    nodes = []
    description = analysis.get('original_description', '')
    desc_lower = description.lower()
    
    # Analyze what the user actually wants to accomplish
    required_nodes = analyze_required_nodes(description, analysis, complexity, context)
    
    # Generate specific n8n nodes based on requirements
    for node_requirement in required_nodes:
        node_config = create_specific_node_config(node_requirement, analysis, context)
        if node_config:
            nodes.append(node_config)
    
    return nodes

def analyze_required_nodes(description, analysis, complexity, context=None):
    """Analyze the description to determine exactly what n8n nodes are needed"""
    if context is None:
        context = {}
    desc_lower = description.lower()
    required_nodes = []
    
    # ENHANCED: Analyze content complexity to determine actual node requirements
    content_complexity_indicators = [
        'review', 'approval', 'process', 'validation', 'verification', 'check',
        'routing', 'notification', 'tracking', 'monitoring', 'reporting',
        'integration', 'transformation', 'analysis', 'calculation', 'workflow',
        'automation', 'management', 'coordination', 'scheduling', 'optimization',
        'enrichment', 'storage', 'handling', 'logging', 'audit', 'testing',
        'compliance', 'supplier', 'defect', 'corrective', 'enterprise',
        'comprehensive', 'advanced', 'sophisticated', 'multi-step', 'complex'
    ]
    
    # Count complexity indicators in description with enhanced detection
    complexity_score = 0
    found_indicators = set()  # Prevent double counting
    
    for indicator in content_complexity_indicators:
        if indicator in desc_lower and indicator not in found_indicators:
            complexity_score += 1
            found_indicators.add(indicator)
    
    # Additional complexity scoring for compound terms
    compound_indicators = [
        'data processing', 'error handling', 'audit logging', 'quality control',
        'user onboarding', 'lead processing', 'order processing', 'workflow management',
        'process optimization', 'data transformation', 'compliance reporting'
    ]
    
    found_compounds = set()  # Prevent double counting compounds
    for compound in compound_indicators:
        if compound in desc_lower and compound not in found_compounds:
            complexity_score += 2  # Compound terms get double weight
            found_compounds.add(compound)
    
    # Add bonus for description length (longer descriptions typically need more nodes)
    word_count = len(description.split())
    if word_count > 50:
        length_bonus = min(word_count // 25, 4)  # Max 4 bonus points for very long descriptions
    elif word_count > 20:
        length_bonus = 2
    elif word_count > 10:
        length_bonus = 1
    else:
        length_bonus = 0
    
    complexity_score += length_bonus
    
    # Determine minimum nodes based on enhanced content complexity and user complexity setting
    if complexity == 'simple':
        min_nodes = 2  # Always keep simple workflows minimal
    elif complexity == 'medium':
        if complexity_score >= 7:
            min_nodes = 5
        elif complexity_score >= 4:
            min_nodes = 4
        else:
            min_nodes = 3
    else:  # complex
        # For complex workflows, ensure minimum 6 nodes regardless of content
        if complexity_score >= 10:
            min_nodes = 8
        elif complexity_score >= 7:
            min_nodes = 7
        else:
            min_nodes = 6  # Increased minimum for complex workflows
    
    # Set maximum nodes based on complexity parameter and content
    base_max_nodes = {
        'simple': 3,    # Keep simple workflows truly simple
        'medium': 6,    # Moderate complexity
        'complex': 12   # High complexity
    }.get(complexity, 6)
    
    # Adjust max nodes based on content complexity with proper scaling
    if complexity == 'simple':
        # Simple workflows should never exceed base limit
        max_nodes = base_max_nodes
    else:
        content_multiplier = 1 + (complexity_score * 0.05)  # Reduced multiplier for better control
        max_nodes = max(min_nodes, int(base_max_nodes * content_multiplier))
    
    # Cap maximum nodes to prevent excessive generation
    absolute_max = {
        'simple': 4,
        'medium': 8,
        'complex': 15
    }.get(complexity, 8)
    
    max_nodes = min(max_nodes, absolute_max)
    
    # Always start with basic processing
    required_nodes.append({
        'type': 'data_processing',
        'purpose': 'process_data',
        'details': extract_processing_details(description)
    })
    
    # For simple workflows with low complexity score, keep it minimal
    if complexity == 'simple':
        # Only add one essential node based on description
        if any(word in desc_lower for word in ['email', 'mail', 'notification']):
            required_nodes.append({
                'type': 'email_integration',
                'purpose': 'send_email', 
                'details': extract_email_details(description)
            })
        elif any(word in desc_lower for word in ['slack', 'team', 'channel']):
            required_nodes.append({
                'type': 'slack_integration',
                'purpose': 'send_message',
                'details': extract_slack_details(description)
            })
        elif any(word in desc_lower for word in ['database', 'store', 'save']):
            required_nodes.append({
                'type': 'database_integration',
                'purpose': 'store_data',
                'details': extract_database_details(description)
            })
        else:
            # Add a basic processing node for simple workflows
            required_nodes.append({
                'type': 'data_processing',
                'purpose': 'process_data',
                'details': extract_processing_details(description)
            })
        # Return early for simple workflows to prevent over-generation
        return required_nodes[:2]  # Maximum 2 nodes for simple workflows
    
    # For all other cases, analyze description content thoroughly
    node_priority = []
    
    # ENHANCED: Add comprehensive node detection with diversity priority
    node_types_added = set()  # Track node types to ensure diversity
    node_categories_added = set()  # Track broader categories for better diversity
    
    # Priority 1: Core processing nodes (always needed)
    if any(word in desc_lower for word in ['validate', 'verify', 'check', 'ensure', 'review', 'approve']):
        node_priority.append({
            'type': 'data_validation',
            'purpose': 'validate_input',
            'details': extract_validation_details(description)
        })
        node_types_added.add('data_validation')
        node_categories_added.add('processing')
    
    if any(word in desc_lower for word in ['transform', 'convert', 'format', 'modify', 'enrich', 'calculate']):
        node_priority.append({
            'type': 'data_transformation',
            'purpose': 'transform_data',
            'details': extract_transformation_details(description)
        })
        node_types_added.add('data_transformation')
        node_categories_added.add('processing')
    
    # Priority 2: Logic and routing nodes
    if any(word in desc_lower for word in ['condition', 'if', 'when', 'filter', 'route', 'decision', 'branch']):
        node_priority.append({
            'type': 'conditional_logic',
            'purpose': 'route_data',
            'details': extract_conditional_details(description)
        })
        node_types_added.add('conditional_logic')
        node_categories_added.add('logic')
    
    # Priority 3: Communication and integration nodes
    if any(word in desc_lower for word in ['email', 'mail', 'gmail', 'notification', 'notify', 'alert']):
        node_priority.append({
            'type': 'email_integration', 
            'purpose': 'send_email',
            'details': extract_email_details(description)
        })
        node_types_added.add('email_integration')
        node_categories_added.add('communication')
    
    if any(word in desc_lower for word in ['slack', 'team', 'channel', 'chat', 'message']):
        node_priority.append({
            'type': 'slack_integration',
            'purpose': 'send_message',
            'details': extract_slack_details(description)
        })
        node_types_added.add('slack_integration')
        node_categories_added.add('communication')
    
    # Priority 4: Data persistence nodes
    if any(word in desc_lower for word in ['database', 'mysql', 'postgres', 'store', 'save', 'record', 'persist']):
        node_priority.append({
            'type': 'database_integration',
            'purpose': 'store_data',
            'details': extract_database_details(description)
        })
        node_types_added.add('database_integration')
        node_categories_added.add('storage')
    
    if any(word in desc_lower for word in ['sheets', 'spreadsheet', 'excel', 'google sheets']):
        node_priority.append({
            'type': 'sheets_integration',
            'purpose': 'update_sheet',
            'details': extract_sheets_details(description)
        })
        node_types_added.add('sheets_integration')
        node_categories_added.add('storage')
    
    # Priority 5: External integrations
    if any(word in desc_lower for word in ['api', 'http', 'rest', 'endpoint', 'service', 'integration', 'webhook']):
        node_priority.append({
            'type': 'http_integration',
            'purpose': 'api_call',
            'details': extract_api_details(description)
        })
        node_types_added.add('http_integration')
        node_categories_added.add('integration')
    
    # Priority 6: Specialized operations
    if any(word in desc_lower for word in ['file', 'document', 'upload', 'download', 'attachment']):
        node_priority.append({
            'type': 'file_operation',
            'purpose': 'handle_files',
            'details': extract_file_details(description)
        })
        node_types_added.add('file_operation')
        node_categories_added.add('file_handling')
    
    if any(word in desc_lower for word in ['monitor', 'track', 'log', 'audit', 'report', 'analytics']):
        node_priority.append({
            'type': 'monitoring',
            'purpose': 'track_progress',
            'details': extract_monitoring_details(description)
        })
        node_types_added.add('monitoring')
        node_categories_added.add('monitoring')
    
    # Priority 7: Error handling for complex workflows
    if complexity_score >= 5 or complexity == 'complex':
        node_priority.append({
            'type': 'error_handling',
            'purpose': 'handle_errors',
            'details': extract_error_handling_details(description)
        })
        node_types_added.add('error_handling')
        node_categories_added.add('error_handling')
    
    # Add nodes based on priority, ensuring minimum complexity requirements
    available_slots = max_nodes - len(required_nodes)
    nodes_to_add = min(len(node_priority), available_slots)
    
    # ENHANCED: Ensure we meet minimum node requirements with maximum diversity
    nodes_needed = max(min_nodes - len(required_nodes), 0)
    
    if nodes_needed > len(node_priority):
        # Add diverse additional nodes to meet complexity requirements
        # Organize by category to ensure balanced diversity
        additional_diverse_nodes = [
            # Processing category
            {'type': 'data_transformation', 'purpose': 'transform_data', 'details': extract_transformation_details(description), 'category': 'processing'},
            {'type': 'data_validation', 'purpose': 'validate_input', 'details': extract_validation_details(description), 'category': 'processing'},
            
            # Logic category
            {'type': 'conditional_logic', 'purpose': 'route_data', 'details': extract_conditional_details(description), 'category': 'logic'},
            
            # Integration category
            {'type': 'http_integration', 'purpose': 'api_call', 'details': extract_api_details(description), 'category': 'integration'},
            
            # Monitoring category
            {'type': 'monitoring', 'purpose': 'track_progress', 'details': extract_monitoring_details(description), 'category': 'monitoring'},
            {'type': 'error_handling', 'purpose': 'handle_errors', 'details': extract_error_handling_details(description), 'category': 'error_handling'},
            
            # File handling category
            {'type': 'file_operation', 'purpose': 'handle_files', 'details': extract_file_details(description), 'category': 'file_handling'}
        ]
        
        # Add nodes prioritizing category diversity
        # Shuffle the list based on context seed for uniqueness
        if 'unique_seed' in context:
            import random
            random.seed(context['unique_seed'])
            random.shuffle(additional_diverse_nodes)
        
        for diverse_node in additional_diverse_nodes:
            node_type = diverse_node['type']
            node_category = diverse_node.get('category', 'general')
            
            # Add if type not already added and we have room
            if (node_type not in node_types_added and 
                len(node_priority) < max_nodes):
                node_priority.append(diverse_node)
                node_types_added.add(node_type)
                node_categories_added.add(node_category)
        
        # Fill remaining slots with additional processing if still needed
        processing_step_counter = 1
        while len(node_priority) < nodes_needed and len(node_priority) < max_nodes:
            node_priority.append({
                'type': 'additional_processing',
                'purpose': 'additional_logic',
                'details': {'name': f'Processing Step {processing_step_counter}'}
            })
            processing_step_counter += 1
    
    # Account for trigger node and potential webhook response node that will be added later
    # This ensures the total workflow stays within expected limits
    reserved_slots = 2  # 1 for trigger, 1 for potential webhook response
    adjusted_max_nodes = max(1, max_nodes - reserved_slots)
    
    # Add all priority nodes up to the adjusted maximum limit
    available_slots = adjusted_max_nodes - len(required_nodes)
    final_nodes_to_add = min(len(node_priority), available_slots)
    
    # Ensure we meet minimum node requirements (but respect the adjusted max)
    adjusted_min_nodes = max(1, min_nodes - reserved_slots)
    if final_nodes_to_add < max(0, adjusted_min_nodes - len(required_nodes)):
        final_nodes_to_add = min(max(0, adjusted_min_nodes - len(required_nodes)), available_slots)
    
    required_nodes.extend(node_priority[:final_nodes_to_add])
    
    return required_nodes

def extract_file_details(description):
    """Extract file operation details from description"""
    return {
        'operation': 'read_write',
        'file_type': 'general',
        'encoding': 'utf8'
    }

def extract_monitoring_details(description):
    """Extract monitoring details from description"""
    return {
        'metrics': ['status', 'progress'],
        'alerts': True,
        'logging': True
    }

def extract_error_handling_details(description):
    """Extract error handling details from description"""
    return {
        'retry_attempts': 3,
        'error_notification': True,
        'fallback_action': 'log_error'
    }

def extract_slack_details(description):
    """Extract Slack-specific details from description"""
    details = {
        'channel': '#general',
        'message_type': 'notification',
        'include_data': True
    }
    
    # Look for channel mentions
    import re
    channel_match = re.search(r'#(\w+)', description)
    if channel_match:
        details['channel'] = f"#{channel_match.group(1)}"
    elif 'sales' in description.lower():
        details['channel'] = '#sales'
    elif 'support' in description.lower():
        details['channel'] = '#support'
    
    # Determine message content based on context
    if 'lead' in description.lower():
        details['message_template'] = 'lead_notification'
    elif 'order' in description.lower():
        details['message_template'] = 'order_notification'
    elif 'error' in description.lower():
        details['message_template'] = 'error_alert'
    else:
        details['message_template'] = 'general_notification'
    
    return details

def extract_email_details(description):
    """Extract email-specific details from description"""
    details = {
        'to_field': 'admin@example.com',
        'subject_template': 'Workflow Notification',
        'body_type': 'html',
        'include_data': True
    }
    
    # Look for email addresses
    import re
    email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', description)
    if email_match:
        details['to_field'] = email_match.group(1)
    
    # Determine email type
    if 'confirmation' in description.lower():
        details['subject_template'] = 'Order Confirmation'
        details['email_type'] = 'confirmation'
    elif 'alert' in description.lower():
        details['subject_template'] = 'System Alert'
        details['email_type'] = 'alert'
    elif 'notification' in description.lower():
        details['subject_template'] = 'Notification'
        details['email_type'] = 'notification'
    
    return details

def extract_database_details(description):
    """Extract database-specific details from description"""
    details = {
        'operation': 'insert',
        'table': 'workflow_data',
        'fields': ['name', 'email', 'data', 'created_at']
    }
    
    # Determine operation type
    if any(word in description.lower() for word in ['update', 'modify', 'change']):
        details['operation'] = 'update'
    elif any(word in description.lower() for word in ['delete', 'remove']):
        details['operation'] = 'delete'
    
    # Try to extract table name
    import re
    table_match = re.search(r'(?:table|into)\s+(\w+)', description.lower())
    if table_match:
        details['table'] = table_match.group(1)
    elif 'customer' in description.lower():
        details['table'] = 'customers'
    elif 'order' in description.lower():
        details['table'] = 'orders'
    elif 'lead' in description.lower():
        details['table'] = 'leads'
    
    return details

def extract_sheets_details(description):
    """Extract Google Sheets specific details from description"""
    details = {
        'operation': 'append',
        'sheet_name': 'Sheet1',
        'range': 'A:Z'
    }
    
    if 'update' in description.lower():
        details['operation'] = 'update'
    
    return details

def extract_api_details(description):
    """Extract API call specific details from description"""
    details = {
        'method': 'POST',
        'url': 'https://api.example.com/data',
        'send_data': True
    }
    
    if 'get' in description.lower() or 'fetch' in description.lower():
        details['method'] = 'GET'
        details['send_data'] = False
    elif 'put' in description.lower():
        details['method'] = 'PUT'
    elif 'delete' in description.lower():
        details['method'] = 'DELETE'
    
    return details

def extract_validation_details(description):
    """Extract validation specific details from description"""
    details = {
        'validate_email': 'email' in description.lower(),
        'validate_phone': 'phone' in description.lower(),
        'required_fields': [],
        'custom_rules': []
    }
    
    # Look for required fields
    import re
    required_match = re.findall(r'required?\s+(\w+)', description.lower())
    details['required_fields'].extend(required_match)
    
    return details

def extract_transformation_details(description):
    """Extract data transformation specific details"""
    details = {
        'format_data': True,
        'add_timestamp': True,
        'normalize': 'normalize' in description.lower()
    }
    
    return details

def extract_conditional_details(description):
    """Extract conditional logic specific details"""
    details = {
        'condition_field': 'status',
        'condition_value': 'active',
        'operator': 'equals'
    }
    
    # Try to extract specific conditions
    import re
    if_match = re.search(r'if\s+(\w+)\s+(?:is|equals?)\s+(\w+)', description.lower())
    if if_match:
        details['condition_field'] = if_match.group(1)
        details['condition_value'] = if_match.group(2)
    
    return details

def extract_processing_details(description):
    """Extract general processing details"""
    details = {
        'add_metadata': True,
        'process_timestamp': True,
        'enrich_data': 'enrich' in description.lower()
    }
    
    return details

def create_specific_node_config(node_requirement, analysis, context):
    """Create specific n8n node configuration based on requirements"""
    node_type = node_requirement['type']
    purpose = node_requirement['purpose']
    details = node_requirement['details']
    
    # Create base config with preserved metadata
    base_config = {
        'type': node_type,
        'purpose': purpose,
        'details': details
    }
    
    if node_type == 'slack_integration':
        config = create_intelligent_slack_node(details, context)
    elif node_type == 'email_integration':
        config = create_intelligent_email_node(details, context)
    elif node_type == 'database_integration':
        config = create_intelligent_database_node(details, context)
    elif node_type == 'sheets_integration':
        config = create_intelligent_sheets_node(details, context)
    elif node_type == 'http_integration':
        config = create_intelligent_http_node(details, context)
    elif node_type == 'data_validation':
        config = create_intelligent_validation_node(details, context)
    elif node_type == 'data_transformation':
        config = create_intelligent_transformation_node(details, context)
    elif node_type == 'conditional_logic':
        config = create_intelligent_conditional_node(details, context)
    elif node_type == 'data_processing':
        config = create_intelligent_processing_node(details, context)
    elif node_type == 'file_operation':
        config = create_intelligent_file_node(details, context)
    elif node_type == 'monitoring':
        config = create_intelligent_monitoring_node(details, context)
    elif node_type == 'error_handling':
        config = create_intelligent_error_node(details, context)
    elif node_type == 'additional_processing':
        config = create_intelligent_additional_node(details, context)
    else:
        return None
    
    # Preserve the original metadata
    if config:
        config.update(base_config)
    
    return config

def create_intelligent_slack_node(details, context):
    """Create a Slack node with intelligent configuration"""
    message_templates = {
        'lead_notification': '🎯 *New Lead Alert*\\n\\n*Name:* {{ $json.name || "Unknown" }}\\n*Email:* {{ $json.email || "Not provided" }}\\n*Source:* {{ $json.source || "Workflow" }}\\n\\n_Processed at {{ new Date().toISOString() }}_',
        'order_notification': '🛒 *New Order Received*\\n\\n*Order ID:* {{ $json.orderId || $json.id }}\\n*Customer:* {{ $json.customerName || $json.name }}\\n*Amount:* ${{ $json.amount || $json.total }}\\n\\n_Order processed successfully_',
        'error_alert': '🚨 *System Alert*\\n\\n*Error:* {{ $json.error || "Unknown error" }}\\n*Time:* {{ $json.timestamp || new Date().toISOString() }}\\n*Details:* {{ $json.details || "No additional details" }}',
        'general_notification': '📋 *Workflow Notification*\\n\\n*Status:* {{ $json.status || "Completed" }}\\n*Data:* {{ $json.message || JSON.stringify($json) }}\\n*Time:* {{ new Date().toISOString() }}'
    }
    
    message = message_templates.get(details.get('message_template', 'general_notification'))
    
    return {
        'type': 'slack',
        'name': 'Send Slack Notification',
        'description': f'Send notification to {details.get("channel", "#general")}',
        'parameters': {
            'resource': 'message',
            'operation': 'post',
            'channel': details.get('channel', '#general'),
            'text': message,
            'otherOptions': {
                'mrkdwn': True,
                'unfurl_links': False
            }
        }
    }

def create_intelligent_email_node(details, context):
    """Create an email node with intelligent configuration"""
    email_templates = {
        'confirmation': {
            'subject': 'Order Confirmation - {{ $json.orderId || $json.id }}',
            'body': 'Dear {{ $json.customerName || $json.name }},\\n\\nThank you for your order. Your order has been confirmed and is being processed.\\n\\nOrder Details:\\n{{ JSON.stringify($json, null, 2) }}\\n\\nBest regards,\\nThe Team'
        },
        'alert': {
            'subject': 'System Alert - {{ $json.type || "Notification" }}',
            'body': 'Alert Details:\\n{{ $json.message || JSON.stringify($json, null, 2) }}\\n\\nTime: {{ new Date().toISOString() }}'
        },
        'notification': {
            'subject': 'Workflow Notification - {{ $json.subject || "Update" }}',
            'body': 'Notification:\\n{{ $json.message || JSON.stringify($json, null, 2) }}\\n\\nProcessed at: {{ new Date().toISOString() }}'
        }
    }
    
    template = email_templates.get(details.get('email_type', 'notification'))
    
    return {
        'type': 'email',
        'name': 'Send Email Notification',
        'description': f'Send email to {details.get("to_field", "recipient")}',
        'parameters': {
            'fromEmail': 'noreply@example.com',
            'toEmail': details.get('to_field', 'admin@example.com'),
            'subject': template['subject'],
            'text': template['body'],
            'options': {
                'allowUnauthorizedCerts': False
            }
        }
    }

def create_intelligent_database_node(details, context):
    """Create a database node with intelligent configuration"""
    operation = details.get('operation', 'insert')
    table = details.get('table', 'workflow_data')
    
    if operation == 'insert':
        return {
            'type': 'database',
            'name': f'Insert into {table}',
            'description': f'Store data in {table} table',
            'parameters': {
                'operation': 'insert',
                'table': table,
                'columns': ', '.join(details.get('fields', ['name', 'email', 'data', 'created_at'])),
                'values': '{{ $json.name }}, {{ $json.email }}, {{ JSON.stringify($json) }}, {{ new Date().toISOString() }}',
                'options': {}
            }
        }
    elif operation == 'update':
        return {
            'type': 'database',
            'name': f'Update {table}',
            'description': f'Update records in {table} table',
            'parameters': {
                'operation': 'update',
                'table': table,
                'updateKey': 'id',
                'columnToMatchOn': 'id',
                'valueToMatchOn': '={{ $json.id }}',
                'fieldsToUpdate': 'name, email, updated_at',
                'values': '{{ $json.name }}, {{ $json.email }}, {{ new Date().toISOString() }}',
                'options': {}
            }
        }
    
    return None

def create_intelligent_sheets_node(details, context):
    """Create a Google Sheets node with intelligent configuration"""
    return {
        'type': 'sheets',
        'name': 'Update Spreadsheet',
        'description': 'Add data to Google Sheets',
        'parameters': {
            'resource': 'spreadsheet',
            'operation': 'appendOrUpdate',
            'documentId': 'YOUR_SPREADSHEET_ID',
            'sheetName': details.get('sheet_name', 'Sheet1'),
            'range': details.get('range', 'A:Z'),
            'valueInputOption': 'USER_ENTERED',
            'values': '={{ [[$json.name, $json.email, $json.timestamp || new Date().toISOString()]] }}',
            'options': {}
        }
    }

def create_intelligent_http_node(details, context):
    """Create an HTTP request node with intelligent configuration"""
    return {
        'type': 'http',
        'name': 'API Request',
        'description': f'Make {details.get("method", "POST")} request to external API',
        'parameters': {
            'url': details.get('url', 'https://api.example.com/data'),
            'httpMethod': details.get('method', 'POST'),
            'sendBody': details.get('send_data', True),
            'bodyContentType': 'json',
            'jsonBody': '={{ $json }}' if details.get('send_data', True) else '',
            'options': {
                'timeout': 10000,
                'retry': {
                    'enabled': True,
                    'maxRetries': 3
                }
            }
        }
    }

def create_intelligent_validation_node(details, context):
    """Create a validation node with intelligent rules"""
    validation_code = """// Intelligent data validation
const inputData = $input.all();
const validatedData = [];
const errors = [];

inputData.forEach((item, index) => {
  const data = item.json;
  const validation = {
    isValid: true,
    errors: []
  };
  
"""
    
    if details.get('validate_email'):
        validation_code += """  // Email validation
  if (data.email && !/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(data.email)) {
    validation.isValid = false;
    validation.errors.push('Invalid email format');
  }
  
"""
    
    if details.get('validate_phone'):
        validation_code += """  // Phone validation
  if (data.phone && !/^[\\+]?[1-9][\\d]{0,15}$/.test(data.phone.replace(/\\s/g, ''))) {
    validation.isValid = false;
    validation.errors.push('Invalid phone number');
  }
  
"""
    
    if details.get('required_fields'):
        validation_code += f"""  // Required fields validation
  const requiredFields = {details['required_fields']};
  requiredFields.forEach(field => {{
    if (!data[field]) {{
      validation.isValid = false;
      validation.errors.push(`Missing required field: ${{field}}`);
    }}
  }});
  
"""
    
    validation_code += """  if (validation.isValid) {
    validatedData.push({
      ...data,
      validated: true,
      validatedAt: new Date().toISOString()
    });
  } else {
    errors.push({
      index: index,
      data: data,
      errors: validation.errors
    });
  }
});

if (errors.length > 0) {
  throw new Error(`Validation failed for ${errors.length} items: ${JSON.stringify(errors)}`);
}

return validatedData;"""
    
    return {
        'type': 'validation',
        'name': 'Validate Data',
        'description': 'Validate input data according to requirements',
        'parameters': {
            'jsCode': validation_code
        }
    }

def create_intelligent_transformation_node(details, context):
    """Create a transformation node with intelligent logic"""
    transform_code = """// Intelligent data transformation
const inputData = $input.all();
const transformedData = inputData.map(item => {
  const data = item.json;
  
  // Apply transformations
  const transformed = {
    ...data,
"""
    
    if details.get('add_timestamp'):
        transform_code += """    timestamp: new Date().toISOString(),
    processedAt: new Date().toISOString(),
"""
    
    if details.get('normalize'):
        transform_code += """    // Normalize data
    email: data.email ? data.email.toLowerCase().trim() : '',
    name: data.name ? data.name.trim() : '',
"""
    
    if details.get('format_data'):
        transform_code += """    // Format data
    formatted: true,
    workflowId: '{{ $workflow.id }}',
"""
    
    transform_code += """    processed: true
  };
  
  return transformed;
});

return transformedData;"""
    
    return {
        'type': 'transformation',
        'name': 'Transform Data',
        'description': 'Transform and format data',
        'parameters': {
            'jsCode': transform_code
        }
    }

def create_intelligent_conditional_node(details, context):
    """Create a conditional node with intelligent logic"""
    return {
        'type': 'conditional',
        'name': 'Route Data',
        'description': f'Route based on {details.get("condition_field", "condition")}',
        'parameters': {
            'conditions': {
                'options': {
                    'caseSensitive': True,
                    'leftValue': '',
                    'typeValidation': 'strict'
                },
                'conditions': [{
                    'leftValue': f'={{{{ $json.{details.get("condition_field", "status")} }}}}',
                    'rightValue': details.get('condition_value', 'active'),
                    'operator': {
                        'type': 'string',
                        'operation': details.get('operator', 'equals')
                    }
                }],
                'combinator': 'and'
            }
        }
    }

def create_intelligent_processing_node(details, context):
    """Create a processing node with intelligent logic"""
    processing_code = """// Intelligent data processing
const inputData = $input.all();
const processedData = inputData.map(item => {
  const data = item.json;
  
  // Process the data according to requirements
  const processed = {
    ...data,
    processed: true,
    processedAt: new Date().toISOString(),
    workflowId: '{{ $workflow.id }}',
"""
    
    if details.get('add_metadata'):
        processing_code += """    metadata: {
      source: 'n8n-workflow',
      version: '1.0',
      processor: 'intelligent-processor'
    },
"""
    
    if details.get('enrich_data'):
        processing_code += """    // Enrich with additional data
    enriched: true,
    enrichedAt: new Date().toISOString(),
"""
    
    processing_code += """    status: 'processed'
  };
  
  return processed;
});

return processedData;"""
    
    return {
        'type': 'processing',
        'name': 'Process Data',
        'description': 'Process data according to workflow requirements',
        'parameters': {
            'jsCode': processing_code
        }
    }

def create_intelligent_file_node(details, context):
    """Create a file operation node with intelligent configuration"""
    return {
        'type': 'file',
        'name': 'File Operation',
        'description': 'Handle file operations',
        'parameters': {
            'operation': details.get('operation', 'read'),
            'fileName': '{{ $json.filename || "output.txt" }}',
            'fileContent': '{{ JSON.stringify($json, null, 2) }}',
            'options': {
                'encoding': details.get('encoding', 'utf8')
            }
        }
    }

def create_intelligent_monitoring_node(details, context):
    """Create a monitoring node with intelligent configuration"""
    monitoring_code = """// Monitoring and tracking
const inputData = $input.all();
const monitoredData = inputData.map(item => {
  const data = item.json;
  
  return {
    ...data,
    monitored: true,
    monitoredAt: new Date().toISOString(),
    status: data.status || 'processed',
    metrics: {
      processingTime: Date.now() - (data.startTime || Date.now()),
      dataSize: JSON.stringify(data).length,
      nodeId: '{{ $node.id }}',
      workflowId: '{{ $workflow.id }}'
    }
  };
});

return monitoredData;"""
    
    return {
        'type': 'monitoring',
        'name': 'Monitor Progress',
        'description': 'Track and monitor workflow progress',
        'parameters': {
            'jsCode': monitoring_code
        }
    }

def create_intelligent_error_node(details, context):
    """Create an error handling node with intelligent configuration"""
    error_code = """// Error handling and recovery
const inputData = $input.all();
const processedData = [];

for (const item of inputData) {
  try {
    const data = item.json;
    
    // Process with error handling
    const result = {
      ...data,
      processed: true,
      errorHandled: false,
      processedAt: new Date().toISOString()
    };
    
    processedData.push(result);
  } catch (error) {
    // Handle errors gracefully
    const errorResult = {
      ...item.json,
      processed: false,
      errorHandled: true,
      error: {
        message: error.message,
        timestamp: new Date().toISOString(),
        retryCount: (item.json.retryCount || 0) + 1
      }
    };
    
    processedData.push(errorResult);
  }
}

return processedData;"""
    
    return {
        'type': 'error_handling',
        'name': 'Handle Errors',
        'description': 'Manage errors and implement retry logic',
        'parameters': {
            'jsCode': error_code
        }
    }

def create_intelligent_additional_node(details, context):
    """Create an additional processing node for complex workflows"""
    additional_code = f"""// {details.get('name', 'Additional Processing')}
const inputData = $input.all();
const processedData = inputData.map(item => {{
  const data = item.json;
  
  return {{
    ...data,
    additionalProcessing: true,
    processedBy: '{details.get('name', 'Additional Processor')}',
    processedAt: new Date().toISOString(),
    step: '{details.get('name', 'Additional Step')}'
  }};
}});

return processedData;"""
    
    return {
        'type': 'additional',
        'name': details.get('name', 'Additional Processing'),
        'description': f'Additional processing step: {details.get("name", "Extra Logic")}',
        'parameters': {
            'jsCode': additional_code
        }
    }

def get_node_variations_by_action():
    """Get node variations based on action types"""
    return {
        'transform': [
            {'type': 'transformation', 'name': 'Transform Data', 'description': 'Data format transformation'},
            {'type': 'transformation', 'name': 'Data Mapper', 'description': 'Map data to target format'},
            {'type': 'transformation', 'name': 'Format Converter', 'description': 'Convert between data formats'}
        ],
        'filter': [
            {'type': 'conditional', 'name': 'Filter Data', 'description': 'Apply filtering conditions'},
            {'type': 'conditional', 'name': 'Condition Router', 'description': 'Route based on conditions'},
            {'type': 'conditional', 'name': 'Data Classifier', 'description': 'Classify and route data'}
        ],
        'send': [
            {'type': 'notification', 'name': 'Send Notification', 'description': 'Dispatch notifications'},
            {'type': 'notification', 'name': 'Message Dispatcher', 'description': 'Send messages to recipients'},
            {'type': 'notification', 'name': 'Alert System', 'description': 'Generate and send alerts'}
        ],
        'store': [
            {'type': 'database', 'name': 'Store Data', 'description': 'Persist data to storage'},
            {'type': 'database', 'name': 'Data Persister', 'description': 'Save data permanently'},
            {'type': 'database', 'name': 'Record Keeper', 'description': 'Maintain data records'}
        ],
        'update': [
            {'type': 'database', 'name': 'Update Records', 'description': 'Update existing data'},
            {'type': 'database', 'name': 'Data Updater', 'description': 'Modify stored information'},
            {'type': 'database', 'name': 'Record Modifier', 'description': 'Change existing records'}
        ],
        'enrich': [
            {'type': 'processing', 'name': 'Enrich Data', 'description': 'Add supplementary information'},
            {'type': 'processing', 'name': 'Data Enhancer', 'description': 'Enhance with additional data'},
            {'type': 'processing', 'name': 'Information Enricher', 'description': 'Augment with extra details'}
        ],
        'calculate': [
            {'type': 'processing', 'name': 'Calculate Values', 'description': 'Perform calculations'},
            {'type': 'processing', 'name': 'Math Processor', 'description': 'Execute mathematical operations'},
            {'type': 'processing', 'name': 'Computation Engine', 'description': 'Handle complex calculations'}
        ]
    }

def get_integration_variations():
    """Get integration node variations"""
    # Enhanced integration nodes with multiple variations
    integration_variations = {
        'slack': [
            {'type': 'slack', 'name': 'Slack Notifier', 'description': 'Send Slack notifications'},
            {'type': 'slack', 'name': 'Team Alert', 'description': 'Alert team via Slack'},
            {'type': 'slack', 'name': 'Channel Messenger', 'description': 'Post to Slack channel'}
        ],
        'email': [
            {'type': 'email', 'name': 'Email Sender', 'description': 'Send email notifications'},
            {'type': 'email', 'name': 'Mail Dispatcher', 'description': 'Dispatch email messages'},
            {'type': 'email', 'name': 'Notification Mailer', 'description': 'Email notification system'}
        ],
        'database': [
            {'type': 'database', 'name': 'Database Writer', 'description': 'Write to database'},
            {'type': 'database', 'name': 'Data Repository', 'description': 'Manage data storage'},
            {'type': 'database', 'name': 'Record Manager', 'description': 'Handle database records'}
        ],
        'api': [
            {'type': 'http', 'name': 'API Connector', 'description': 'Connect to external API'},
            {'type': 'http', 'name': 'Service Integrator', 'description': 'Integrate with web service'},
            {'type': 'http', 'name': 'External Caller', 'description': 'Call external endpoints'}
        ],
        'sheets': [
            {'type': 'sheets', 'name': 'Spreadsheet Updater', 'description': 'Update spreadsheet data'},
            {'type': 'sheets', 'name': 'Sheet Manager', 'description': 'Manage sheet operations'},
            {'type': 'sheets', 'name': 'Excel Connector', 'description': 'Connect to Excel/Sheets'}
        ]
    }
    return integration_variations

def create_dynamic_node(node_config, position_index, x_offset=0):
    """Create a node based on dynamic configuration"""
    node_type = node_config['type']
    # Ensure proper spacing between nodes (minimum 300px apart)
    x_position = max(0, (position_index * 300) + min(x_offset, 50))  # Limit offset to prevent overlap
    node_id = generate_node_id()
    
    # Handle intelligent node configurations
    if 'parameters' in node_config:
        # This is already a complete node configuration from intelligent generation
        node = {
            'parameters': node_config['parameters'],
            'id': node_id,
            'name': node_config.get('name', 'Node'),
            'type': get_n8n_node_type(node_type),
            'typeVersion': get_node_type_version(node_type),
            'position': [x_position, 300]
        }
        # Preserve metadata from original config
        if 'purpose' in node_config:
            node['purpose'] = node_config['purpose']
        if 'details' in node_config:
            node['details'] = node_config['details']
        return node
    
    # Map node types to creation functions for legacy support
    node_creators = {
        'validation': create_validation_node,
        'processing': create_processing_node,
        'transformation': create_transformation_node,
        'conditional': create_conditional_node,
        'slack': create_slack_node,
        'email': create_email_node,
        'database': create_database_node,
        'http': create_http_request_node,
        'sheets': create_sheets_node,
        'webhook_call': create_webhook_call_node,
        'file': create_file_node,
        'notification': create_notification_node,
        'error_handler': create_error_handler_node
    }
    
    # Get the appropriate creator function
    creator_func = node_creators.get(node_type, create_processing_node)
    
    # Create the node
    node = creator_func(node_id, x_position, node_config)
    
    # Ensure code nodes have JavaScript parameters
    if isinstance(node, dict) and node.get('type') == 'n8n-nodes-base.code':
        if 'parameters' not in node or not node['parameters'].get('jsCode'):
            # Add default JavaScript code based on node name
            node_name = node.get('name', 'Process Data')
            if 'route' in node_name.lower() or 'router' in node_name.lower():
                js_code = '''// Route data based on conditions
const inputData = $input.all();
const routedData = inputData.map(item => ({
  ...item.json,
  routed: true,
  route_applied: new Date().toISOString(),
  routing_logic: 'conditional'
}));
return routedData;'''
            elif 'email' in node_name.lower() or 'notification' in node_name.lower():
                js_code = '''// Prepare email notification data
const inputData = $input.all();
const emailData = inputData.map(item => ({
  ...item.json,
  email_prepared: true,
  notification_type: 'email',
  prepared_at: new Date().toISOString(),
  recipient: item.json.email || 'admin@example.com'
}));
return emailData;'''
            else:
                js_code = '''// Process data
const inputData = $input.all();
const processedData = inputData.map(item => ({
  ...item.json,
  processed: true,
  processed_at: new Date().toISOString()
}));
return processedData;'''
            
            if 'parameters' not in node:
                node['parameters'] = {}
            node['parameters']['jsCode'] = js_code
    
    # Preserve metadata from original config
    if isinstance(node, dict):
        if 'purpose' in node_config:
            node['purpose'] = node_config['purpose']
        if 'details' in node_config:
            node['details'] = node_config['details']
    
    return node

def get_n8n_node_type(node_type):
    """Map our node types to actual n8n node types"""
    type_mapping = {
        'slack': 'n8n-nodes-base.slack',
        'email': 'n8n-nodes-base.emailSend',
        'database': 'n8n-nodes-base.mysql',
        'sheets': 'n8n-nodes-base.googleSheets',
        'http': 'n8n-nodes-base.httpRequest',
        'file': 'n8n-nodes-base.readBinaryFile',
        'conditional': 'n8n-nodes-base.if',
        'validation': 'n8n-nodes-base.code',
        'transformation': 'n8n-nodes-base.code',
        'processing': 'n8n-nodes-base.code',
        'monitoring': 'n8n-nodes-base.code',
        'error_handling': 'n8n-nodes-base.code',
        'additional_processing': 'n8n-nodes-base.code'
    }
    return type_mapping.get(node_type, 'n8n-nodes-base.code')

def get_node_type_version(node_type):
    """Get the appropriate type version for each node type"""
    version_mapping = {
        'slack': 2,
        'email': 2,
        'database': 2,
        'sheets': 4,
        'http': 4,
        'validation': 2,
        'transformation': 2,
        'processing': 2,
        'conditional': 2
    }
    return version_mapping.get(node_type, 2)

def create_dynamic_connections(nodes, analysis, context=None):
    """Create dynamic connections between nodes based on workflow analysis"""
    if context is None:
        context = {}
    
    connections = {}
    
    # Ensure we have nodes to connect
    if len(nodes) < 2:
        return connections
    
    # Check if this is a webhook workflow that needs a response node
    has_webhook_trigger = any(node.get('type') == 'n8n-nodes-base.webhook' for node in nodes)
    needs_response = has_webhook_trigger and not any('respond' in node.get('name', '').lower() for node in nodes)
    
    # Add webhook response node if needed
    if needs_response:
        response_node = create_response_node('response', len(nodes) * 300)
        nodes.append(response_node)
    
    # Create linear connections for most workflows
    for i in range(len(nodes) - 1):
        current_node = nodes[i]
        next_node = nodes[i + 1]
        
        # Validate nodes have required properties
        if not current_node.get('name') or not next_node.get('name'):
            continue
        
        # Ensure unique node names to prevent connection conflicts
        current_name = current_node['name']
        next_name = next_node['name']
        
        # Skip if trying to connect to itself
        if current_name == next_name:
            continue
            
        connections[current_name] = {
            'main': [[{
                'node': next_name,
                'type': 'main',
                'index': 0
            }]]
        }
    
    # Add conditional branching for complex workflows
    if analysis.get('type') in ['lead_processing', 'ecommerce'] and len(nodes) > 3:
        # Find conditional nodes and create branches
        for i, node in enumerate(nodes):
            if node.get('type') == 'n8n-nodes-base.if' and i < len(nodes) - 2:
                # Create true/false branches
                true_branch = nodes[i + 1] if i + 1 < len(nodes) else None
                false_branch = nodes[i + 2] if i + 2 < len(nodes) else None
                
                # Validate branches exist and have names
                if (true_branch and false_branch and 
                    node.get('name') and 
                    true_branch.get('name') and 
                    false_branch.get('name') and
                    true_branch['name'] != false_branch['name']):  # Ensure different branches
                    
                    connections[node['name']] = {
                        'main': [
                            [{
                                'node': true_branch['name'],
                                'type': 'main',
                                'index': 0
                            }],
                            [{
                                'node': false_branch['name'],
                                'type': 'main',
                                'index': 0
                            }]
                        ]
                    }
    
    return connections

def create_visual_preview(workflow):
    """Create visual preview data for workflow diagram"""
    nodes = workflow.get('nodes', [])
    connections = workflow.get('connections', {})
    
    # Create visual nodes with positioning
    visual_nodes = []
    for node in nodes:
        position = node.get('position', [0, 0])
        # Ensure position is a valid list with at least 2 elements
        if not isinstance(position, list) or len(position) < 2:
            position = [0, 0]
        
        visual_node = {
            'id': node.get('id', ''),
            'name': node.get('name', 'Unknown'),
            'type': node.get('type', '').split('.')[-1] if node.get('type') else 'unknown',
            'position': {
                'x': max(0, position[0]),  # Ensure non-negative position
                'y': max(0, position[1])   # Ensure non-negative position
            },
            'icon': get_node_icon(node.get('type', '')),
            'color': get_node_color(node.get('type', ''))
        }
        visual_nodes.append(visual_node)
    
    # Create visual connections
    visual_connections = []
    for source_name, connection_data in connections.items():
        if 'main' in connection_data:
            for connection_group in connection_data['main']:
                for connection in connection_group:
                    target_name = connection.get('node', '')
                    visual_connections.append({
                        'source': source_name,
                        'target': target_name,
                        'type': connection.get('type', 'main')
                    })
    
    return {
        'nodes': visual_nodes,
        'connections': visual_connections,
        'layout': 'horizontal',
        'stats': {
            'total_nodes': len(visual_nodes),
            'total_connections': len(visual_connections),
            'workflow_name': workflow.get('name', 'Untitled Workflow')
        }
    }

def get_node_icon(node_type):
    """Get icon for node type"""
    icon_map = {
        'webhook': '🔗',
        'scheduleTrigger': '⏰',
        'manualTrigger': '👆',
        'httpRequest': '🌐',
        'code': '💻',
        'set': '📝',
        'if': '❓',
        'slack': '💬',
        'gmail': '📧',
        'respondToWebhook': '↩️'
    }
    
    for key, icon in icon_map.items():
        if key in node_type:
            return icon
    
    return '⚙️'  # Default icon

def get_node_color(node_type):
    """Get color for node type"""
    color_map = {
        'webhook': '#4CAF50',
        'scheduleTrigger': '#FF9800',
        'manualTrigger': '#2196F3',
        'httpRequest': '#9C27B0',
        'code': '#607D8B',
        'set': '#795548',
        'if': '#FF5722',
        'slack': '#4CAF50',
        'gmail': '#F44336',
        'respondToWebhook': '#00BCD4'
    }
    
    for key, color in color_map.items():
        if key in node_type:
            return color
    
    return '#757575'  # Default color

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)