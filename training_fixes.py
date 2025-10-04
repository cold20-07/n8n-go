# N8N Training System Fixes
# Generated automatically from analysis

# Improved Classification Features

def create_enhanced_features(workflow_data):
    '''Enhanced feature engineering for better classification'''
    
    features = []
    
    for workflow in workflow_data:
        nodes = workflow.get('nodes', [])
        
        # Basic features
        node_count = len(nodes)
        
        # Advanced node analysis
        node_types = [node.get('type', '') for node in nodes]
        unique_node_types = len(set(node_types))
        
        # Service integration patterns
        service_categories = {
            'ai_services': ['openai', 'langchain', 'claude', 'gemini'],
            'data_services': ['sheets', 'airtable', 'database', 'csv'],
            'communication': ['slack', 'email', 'telegram', 'discord'],
            'web_services': ['webhook', 'http', 'api'],
            'automation': ['schedule', 'trigger', 'cron']
        }
        
        service_scores = {}
        for category, keywords in service_categories.items():
            score = sum(1 for node_type in node_types 
                       if any(keyword in node_type.lower() for keyword in keywords))
            service_scores[f'{category}_score'] = score / max(node_count, 1)
        
        # Workflow complexity metrics
        branching_nodes = sum(1 for node in nodes if 'if' in node.get('type', '').lower())
        loop_nodes = sum(1 for node in nodes if any(loop_word in node.get('type', '').lower() 
                                                   for loop_word in ['loop', 'split', 'merge']))
        
        complexity_score = (
            node_count * 0.5 +
            unique_node_types * 1.0 +
            branching_nodes * 2.0 +
            loop_nodes * 1.5 +
            sum(service_scores.values()) * 3.0
        )
        
        # Create feature vector
        feature_vector = [
            node_count,
            unique_node_types,
            branching_nodes,
            loop_nodes,
            complexity_score
        ] + list(service_scores.values())
        
        features.append(feature_vector)
    
    return np.array(features)


# Balanced Training Strategy

def train_balanced_classifier(X, y):
    '''Balanced training with multiple strategies'''
    
    from sklearn.ensemble import VotingClassifier
    from imblearn.ensemble import BalancedRandomForestClassifier
    from imblearn.over_sampling import BorderlineSMOTE, ADASYN
    
    # Strategy 1: Balanced Random Forest
    balanced_rf = BalancedRandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        random_state=42
    )
    
    # Strategy 2: SMOTE + Gradient Boosting
    smote_gb = Pipeline([
        ('smote', BorderlineSMOTE(random_state=42)),
        ('scaler', StandardScaler()),
        ('gb', GradientBoostingClassifier(n_estimators=100, random_state=42))
    ])
    
    # Strategy 3: ADASYN + Random Forest
    adasyn_rf = Pipeline([
        ('adasyn', ADASYN(random_state=42)),
        ('scaler', StandardScaler()),
        ('rf', RandomForestClassifier(n_estimators=150, class_weight='balanced', random_state=42))
    ])
    
    # Ensemble of strategies
    ensemble = VotingClassifier([
        ('balanced_rf', balanced_rf),
        ('smote_gb', smote_gb),
        ('adasyn_rf', adasyn_rf)
    ], voting='soft')
    
    return ensemble


# Enhanced Sequence Modeling

def create_sequence_model_with_context():
    '''Improved sequence modeling with better context handling'''
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.multioutput import MultiOutputClassifier
    
    # Enhanced sequence preprocessing
    def prepare_sequence_data(sequences):
        contexts = []
        targets = []
        
        for seq in sequences:
            if len(seq) > 2:
                for i in range(1, len(seq) - 1):
                    # Variable context windows
                    for window_size in [2, 3, 4]:
                        if i >= window_size - 1:
                            context = seq[max(0, i-window_size+1):i+1]
                            target = seq[i+1]
                            
                            # Add positional information
                            context_with_pos = [f"{node}_{pos}" for pos, node in enumerate(context)]
                            contexts.append(' '.join(context_with_pos))
                            targets.append(target)
        
        return contexts, targets
    
    # Multi-step prediction
    def train_multi_step_predictor(contexts, targets):
        vectorizer = TfidfVectorizer(
            max_features=3000,
            ngram_range=(1, 4),
            analyzer='word'
        )
        
        X = vectorizer.fit_transform(contexts)
        
        # Predict next 3 nodes
        multi_targets = []
        for i, target in enumerate(targets):
            if i < len(targets) - 2:
                multi_targets.append([targets[i], targets[i+1], targets[i+2]])
        
        if multi_targets:
            multi_output_model = MultiOutputClassifier(
                RandomForestClassifier(n_estimators=200, random_state=42)
            )
            multi_output_model.fit(X[:len(multi_targets)], multi_targets)
            return multi_output_model, vectorizer
        
        return None, vectorizer


# Data Quality Pipeline

def validate_workflow_data(workflow_data):
    '''Comprehensive data quality validation'''
    
    issues = []
    
    for i, workflow in enumerate(workflow_data):
        workflow_issues = []
        
        # Check required fields
        required_fields = ['nodes', 'name']
        for field in required_fields:
            if field not in workflow:
                workflow_issues.append(f"Missing required field: {field}")
        
        # Validate nodes
        if 'nodes' in workflow:
            nodes = workflow['nodes']
            if not isinstance(nodes, list):
                workflow_issues.append("Nodes field is not a list")
            elif len(nodes) == 0:
                workflow_issues.append("Workflow has no nodes")
            else:
                # Check node structure
                for j, node in enumerate(nodes):
                    if not isinstance(node, dict):
                        workflow_issues.append(f"Node {j} is not a dictionary")
                    elif 'type' not in node:
                        workflow_issues.append(f"Node {j} missing type field")
        
        # Check for suspicious patterns
        if 'name' in workflow:
            name = workflow['name']
            if not name or name.strip() == '':
                workflow_issues.append("Empty workflow name")
            elif len(name) > 200:
                workflow_issues.append("Workflow name too long")
        
        if workflow_issues:
            issues.append({
                'workflow_index': i,
                'workflow_name': workflow.get('name', 'Unknown'),
                'issues': workflow_issues
            })
    
    return issues

def clean_workflow_data(workflow_data):
    '''Clean and standardize workflow data'''
    
    cleaned_data = []
    
    for workflow in workflow_data:
        # Skip invalid workflows
        if 'nodes' not in workflow or not workflow['nodes']:
            continue
        
        # Standardize node types
        for node in workflow['nodes']:
            if 'type' in node:
                node_type = node['type']
                # Normalize node type format
                if not node_type.startswith('n8n-nodes-base.') and not node_type.startswith('@n8n/'):
                    node['type'] = f"n8n-nodes-base.{node_type}"
        
        # Ensure required fields
        if 'name' not in workflow:
            workflow['name'] = f"Workflow_{len(cleaned_data)}"
        
        cleaned_data.append(workflow)
    
    return cleaned_data


