#!/usr/bin/env python3
"""
N8N Training Analysis and Fixes
Analyzes the training results and provides fixes for identified issues
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns

class TrainingAnalyzer:
    def __init__(self):
        self.load_data()
        self.issues_found = []
        self.recommendations = []
    
    def load_data(self):
        """Load training data and results"""
        print("📊 Loading training data for analysis...")
        
        # Load datasets
        self.workflow_features = pd.read_csv("training_data/workflow_features.csv")
        self.classification_data = pd.read_csv("specialized_datasets/classification_dataset.csv")
        
        with open("training_data/statistics.json", 'r') as f:
            self.statistics = json.load(f)
        
        with open("training_data/workflow_patterns.json", 'r') as f:
            self.patterns = json.load(f)
        
        # Load model performance if available
        try:
            with open("improved_models/model_performance.json", 'r') as f:
                self.model_performance = json.load(f)
        except:
            self.model_performance = {}
        
        print("✓ Data loaded successfully")
    
    def analyze_class_imbalance(self):
        """Analyze class imbalance issues"""
        print("\n🔍 Analyzing Class Imbalance...")
        
        # Get class distribution
        categories = [p['category'] for p in self.patterns]
        class_counts = Counter(categories)
        
        total_samples = len(categories)
        class_percentages = {k: (v/total_samples)*100 for k, v in class_counts.items()}
        
        print("Class Distribution:")
        for category, count in class_counts.items():
            percentage = class_percentages[category]
            print(f"  {category}: {count} samples ({percentage:.1f}%)")
        
        # Identify severely imbalanced classes
        min_samples = min(class_counts.values())
        max_samples = max(class_counts.values())
        imbalance_ratio = max_samples / min_samples
        
        if imbalance_ratio > 10:
            self.issues_found.append({
                'type': 'severe_class_imbalance',
                'description': f"Severe class imbalance detected (ratio: {imbalance_ratio:.1f}:1)",
                'impact': 'High - Models will be biased toward majority classes',
                'classes': class_counts
            })
        elif imbalance_ratio > 5:
            self.issues_found.append({
                'type': 'moderate_class_imbalance',
                'description': f"Moderate class imbalance detected (ratio: {imbalance_ratio:.1f}:1)",
                'impact': 'Medium - May affect model performance on minority classes',
                'classes': class_counts
            })
        
        return class_counts
    
    def analyze_feature_quality(self):
        """Analyze feature quality and missing values"""
        print("\n🔍 Analyzing Feature Quality...")
        
        # Check for missing values
        missing_counts = self.workflow_features.isnull().sum()
        missing_percentages = (missing_counts / len(self.workflow_features)) * 100
        
        high_missing_features = missing_percentages[missing_percentages > 20]
        
        if len(high_missing_features) > 0:
            self.issues_found.append({
                'type': 'high_missing_values',
                'description': f"{len(high_missing_features)} features have >20% missing values",
                'impact': 'Medium - May reduce model performance',
                'features': high_missing_features.to_dict()
            })
        
        # Check for low variance features
        numeric_features = self.workflow_features.select_dtypes(include=[np.number])
        low_variance_features = []
        
        for col in numeric_features.columns:
            if numeric_features[col].var() < 0.01:
                low_variance_features.append(col)
        
        if low_variance_features:
            self.issues_found.append({
                'type': 'low_variance_features',
                'description': f"{len(low_variance_features)} features have very low variance",
                'impact': 'Low - These features may not be informative',
                'features': low_variance_features
            })
        
        print(f"✓ Found {len(high_missing_features)} high-missing features")
        print(f"✓ Found {len(low_variance_features)} low-variance features")
    
    def analyze_model_performance(self):
        """Analyze model performance issues"""
        print("\n🔍 Analyzing Model Performance...")
        
        performance_issues = []
        
        # Check classification accuracy
        if 'workflow_classifier' in self.model_performance:
            accuracy = self.model_performance['workflow_classifier'].get('accuracy', 0)
            if accuracy < 0.5:
                performance_issues.append({
                    'model': 'workflow_classifier',
                    'issue': 'low_accuracy',
                    'value': accuracy,
                    'threshold': 0.5
                })
        
        # Check sequence prediction accuracy
        if 'sequence_predictor' in self.model_performance:
            accuracy = self.model_performance['sequence_predictor'].get('accuracy', 0)
            if accuracy < 0.3:  # Lower threshold for sequence prediction
                performance_issues.append({
                    'model': 'sequence_predictor',
                    'issue': 'low_accuracy',
                    'value': accuracy,
                    'threshold': 0.3
                })
        
        # Check clustering quality
        if 'clustering' in self.model_performance:
            silhouette = self.model_performance['clustering'].get('silhouette_score', 0)
            if silhouette < 0.3:
                performance_issues.append({
                    'model': 'clustering',
                    'issue': 'poor_clustering',
                    'value': silhouette,
                    'threshold': 0.3
                })
        
        if performance_issues:
            self.issues_found.append({
                'type': 'poor_model_performance',
                'description': f"{len(performance_issues)} models have performance issues",
                'impact': 'High - Models may not be reliable for production use',
                'details': performance_issues
            })
        
        print(f"✓ Found {len(performance_issues)} performance issues")
    
    def analyze_data_quality(self):
        """Analyze overall data quality"""
        print("\n🔍 Analyzing Data Quality...")
        
        # Check dataset size
        total_workflows = len(self.workflow_features)
        if total_workflows < 100:
            self.issues_found.append({
                'type': 'small_dataset',
                'description': f"Dataset is relatively small ({total_workflows} samples)",
                'impact': 'Medium - May limit model generalization',
                'recommendation': 'Consider collecting more workflow data'
            })
        
        # Check feature diversity
        ai_adoption_rate = self.statistics['ai_usage']['ai_adoption_rate']
        if ai_adoption_rate > 95:
            self.issues_found.append({
                'type': 'low_diversity',
                'description': f"Very high AI adoption rate ({ai_adoption_rate:.1f}%)",
                'impact': 'Medium - Limited diversity in workflow types',
                'recommendation': 'Include more non-AI workflows for balance'
            })
        
        # Check for duplicate or near-duplicate workflows
        workflow_names = self.workflow_features['workflow_name'].tolist()
        unique_names = set(workflow_names)
        if len(unique_names) < len(workflow_names):
            duplicates = len(workflow_names) - len(unique_names)
            self.issues_found.append({
                'type': 'duplicate_workflows',
                'description': f"Found {duplicates} duplicate workflow names",
                'impact': 'Low - May indicate data quality issues',
                'recommendation': 'Review and deduplicate workflow data'
            })
        
        print(f"✓ Dataset size: {total_workflows} workflows")
        print(f"✓ AI adoption rate: {ai_adoption_rate:.1f}%")
    
    def generate_recommendations(self):
        """Generate specific recommendations based on analysis"""
        print("\n💡 Generating Recommendations...")
        
        # Recommendations for class imbalance
        for issue in self.issues_found:
            if issue['type'] in ['severe_class_imbalance', 'moderate_class_imbalance']:
                self.recommendations.extend([
                    {
                        'priority': 'High',
                        'category': 'Data Augmentation',
                        'action': 'Implement advanced SMOTE with borderline samples',
                        'description': 'Use borderline-SMOTE or ADASYN for better minority class handling'
                    },
                    {
                        'priority': 'High',
                        'category': 'Model Training',
                        'action': 'Use ensemble methods with class weighting',
                        'description': 'Combine multiple models with different class weight strategies'
                    },
                    {
                        'priority': 'Medium',
                        'category': 'Data Collection',
                        'action': 'Collect more samples for minority classes',
                        'description': f"Focus on collecting {list(issue['classes'].keys())} workflows"
                    }
                ])
        
        # Recommendations for poor performance
        for issue in self.issues_found:
            if issue['type'] == 'poor_model_performance':
                self.recommendations.extend([
                    {
                        'priority': 'High',
                        'category': 'Feature Engineering',
                        'action': 'Create more informative features',
                        'description': 'Add domain-specific features like workflow patterns, node relationships'
                    },
                    {
                        'priority': 'High',
                        'category': 'Model Architecture',
                        'action': 'Try deep learning approaches',
                        'description': 'Implement neural networks for sequence prediction and classification'
                    },
                    {
                        'priority': 'Medium',
                        'category': 'Hyperparameter Tuning',
                        'action': 'Perform extensive hyperparameter optimization',
                        'description': 'Use grid search or Bayesian optimization for better parameters'
                    }
                ])
        
        # General recommendations
        self.recommendations.extend([
            {
                'priority': 'Medium',
                'category': 'Data Quality',
                'action': 'Implement data validation pipeline',
                'description': 'Add automated checks for data quality and consistency'
            },
            {
                'priority': 'Low',
                'category': 'Monitoring',
                'action': 'Set up model performance monitoring',
                'description': 'Track model performance over time and detect drift'
            }
        ])
    
    def create_fixes(self):
        """Create specific fixes for identified issues"""
        print("\n🔧 Creating Fixes...")
        
        fixes = {
            'improved_classification_features': self.create_improved_features(),
            'balanced_training_strategy': self.create_balanced_training(),
            'enhanced_sequence_modeling': self.create_sequence_improvements(),
            'data_quality_pipeline': self.create_data_quality_checks()
        }
        
        return fixes
    
    def create_improved_features(self):
        """Create improved feature engineering"""
        return """
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
"""
    
    def create_balanced_training(self):
        """Create balanced training strategy"""
        return """
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
"""
    
    def create_sequence_improvements(self):
        """Create sequence modeling improvements"""
        return """
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
"""
    
    def create_data_quality_checks(self):
        """Create data quality validation pipeline"""
        return """
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
"""
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\n📋 Generating Analysis Report...")
        
        report = {
            'analysis_summary': {
                'total_workflows': len(self.workflow_features),
                'issues_found': len(self.issues_found),
                'recommendations_generated': len(self.recommendations)
            },
            'issues': self.issues_found,
            'recommendations': self.recommendations,
            'model_performance': self.model_performance,
            'data_statistics': self.statistics
        }
        
        # Save report
        with open("training_analysis_report.json", 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        return report
    
    def run_complete_analysis(self):
        """Run complete analysis pipeline"""
        print("🔍 N8N TRAINING DATA ANALYSIS")
        print("=" * 50)
        
        # Run all analyses
        self.analyze_class_imbalance()
        self.analyze_feature_quality()
        self.analyze_model_performance()
        self.analyze_data_quality()
        
        # Generate recommendations
        self.generate_recommendations()
        
        # Create fixes
        fixes = self.create_fixes()
        
        # Generate report
        report = self.generate_report()
        
        # Print summary
        print(f"\n📊 ANALYSIS SUMMARY")
        print("=" * 50)
        print(f"Issues Found: {len(self.issues_found)}")
        print(f"Recommendations: {len(self.recommendations)}")
        
        if self.issues_found:
            print(f"\n❌ ISSUES IDENTIFIED:")
            for issue in self.issues_found:
                print(f"  • {issue['description']} (Impact: {issue['impact']})")
        
        print(f"\n💡 TOP RECOMMENDATIONS:")
        high_priority = [r for r in self.recommendations if r['priority'] == 'High']
        for rec in high_priority[:5]:
            print(f"  • {rec['action']}: {rec['description']}")
        
        print(f"\n✅ Analysis complete! Report saved to training_analysis_report.json")
        
        return report, fixes

def main():
    analyzer = TrainingAnalyzer()
    report, fixes = analyzer.run_complete_analysis()
    
    # Save fixes to file
    with open("training_fixes.py", 'w') as f:
        f.write("# N8N Training System Fixes\n")
        f.write("# Generated automatically from analysis\n\n")
        for fix_name, fix_code in fixes.items():
            f.write(f"# {fix_name.replace('_', ' ').title()}\n")
            f.write(fix_code)
            f.write("\n\n")
    
    print(f"\n🔧 Fixes saved to training_fixes.py")

if __name__ == "__main__":
    main()