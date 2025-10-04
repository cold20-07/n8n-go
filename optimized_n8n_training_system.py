#!/usr/bin/env python3
"""
Optimized N8N Workflow Training System
Incorporates all identified fixes and improvements for production-ready ML models
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, accuracy_score, f1_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
from imblearn.over_sampling import BorderlineSMOTE, ADASYN
from imblearn.ensemble import BalancedRandomForestClassifier
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pickle
import warnings
warnings.filterwarnings('ignore')

class OptimizedN8NTrainer:
    def __init__(self, training_data_dir: str = "training_data"):
        self.data_dir = Path(training_data_dir)
        self.models = {}
        self.vectorizers = {}
        self.scalers = {}
        self.performance_metrics = {}
        self.load_and_validate_data()
    
    def load_and_validate_data(self):
        """Load and validate training data with quality checks"""
        print("📊 Loading and validating training data...")
        
        try:
            # Load data
            self.workflow_features = pd.read_csv(self.data_dir / "workflow_features.csv")
            
            with open(self.data_dir / "workflow_patterns.json", 'r') as f:
                self.workflow_patterns = json.load(f)
            
            with open(self.data_dir / "ai_integration_patterns.json", 'r') as f:
                self.ai_patterns = [p for p in json.load(f) if p is not None]
            
            with open(self.data_dir / "node_sequences.json", 'r') as f:
                self.node_sequences = json.load(f)
            
            # Data validation and cleaning
            self.clean_data()
            
            print(f"✓ Loaded and validated {len(self.workflow_features)} workflows")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            raise
    
    def clean_data(self):
        """Clean and preprocess data"""
        print("🧹 Cleaning data...")
        
        # Handle missing values intelligently
        numeric_columns = self.workflow_features.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if self.workflow_features[col].isnull().sum() > 0:
                # Use median for numeric features
                median_val = self.workflow_features[col].median()
                self.workflow_features[col].fillna(median_val, inplace=True)
        
        # Handle categorical missing values
        categorical_columns = self.workflow_features.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if self.workflow_features[col].isnull().sum() > 0:
                self.workflow_features[col].fillna('unknown', inplace=True)
        
        # Remove duplicate workflows based on name similarity
        self.workflow_features = self.workflow_features.drop_duplicates(subset=['workflow_name'], keep='first')
        
        print(f"✓ Cleaned data: {len(self.workflow_features)} workflows remaining")
    
    def create_enhanced_features(self) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Create comprehensive enhanced features"""
        print("🔧 Creating enhanced features...")
        
        features = []
        labels = []
        
        feature_names = [
            # Basic metrics
            'node_count', 'unique_node_types', 'connections_count',
            
            # AI features
            'ai_node_count', 'ai_node_ratio', 'has_openai', 'has_langchain', 
            'has_claude', 'has_gemini', 'has_agents',
            
            # Service categories
            'data_services_score', 'communication_score', 'web_services_score',
            'automation_score', 'content_services_score',
            
            # Workflow complexity
            'branching_complexity', 'loop_complexity', 'error_handling_score',
            'documentation_ratio', 'trigger_diversity', 'output_diversity',
            
            # Pattern features
            'workflow_depth', 'parallel_branches', 'sequential_length'
        ]
        
        service_categories = {
            'data_services': ['sheets', 'airtable', 'database', 'csv', 'json', 'xml'],
            'communication': ['slack', 'email', 'telegram', 'discord', 'teams', 'whatsapp'],
            'web_services': ['webhook', 'http', 'api', 'rest', 'graphql'],
            'automation': ['schedule', 'trigger', 'cron', 'timer', 'interval'],
            'content_services': ['wordpress', 'cms', 'blog', 'content', 'seo']
        }
        
        for i, (_, row) in enumerate(self.workflow_features.iterrows()):
            if i < len(self.workflow_patterns):
                try:
                    # Basic metrics
                    node_count = row['node_count']
                    connections = row.get('connections_count', 0)
                    
                    # Parse node types safely
                    try:
                        node_types = eval(row['node_types']) if isinstance(row['node_types'], str) else []
                        if not isinstance(node_types, list):
                            node_types = []
                    except:
                        node_types = []
                    
                    unique_node_types = len(set(node_types))
                    
                    # AI features
                    try:
                        ai_node_types = eval(row['ai_node_types']) if isinstance(row['ai_node_types'], str) else []
                        if not isinstance(ai_node_types, list):
                            ai_node_types = []
                    except:
                        ai_node_types = []
                    
                    ai_node_count = len(ai_node_types)
                    ai_node_ratio = ai_node_count / max(node_count, 1)
                    
                    # Service detection
                    node_types_str = ' '.join(node_types).lower()
                    has_openai = int('openai' in node_types_str)
                    has_langchain = int('langchain' in node_types_str)
                    has_claude = int('claude' in node_types_str)
                    has_gemini = int('gemini' in node_types_str)
                    has_agents = int('agent' in node_types_str)
                    
                    # Service category scores
                    service_scores = {}
                    for category, keywords in service_categories.items():
                        score = sum(1 for keyword in keywords if keyword in node_types_str)
                        service_scores[f'{category}_score'] = score / max(node_count, 1)
                    
                    # Complexity metrics
                    branching_nodes = sum(1 for nt in node_types if 'if' in nt.lower())
                    loop_nodes = sum(1 for nt in node_types 
                                   if any(loop_word in nt.lower() for loop_word in ['loop', 'split', 'merge']))
                    error_handling = row.get('error_handling_nodes', 0)
                    sticky_notes = row.get('sticky_notes_count', 0)
                    
                    branching_complexity = branching_nodes / max(node_count, 1)
                    loop_complexity = loop_nodes / max(node_count, 1)
                    error_handling_score = error_handling / max(node_count, 1)
                    documentation_ratio = sticky_notes / max(node_count, 1)
                    
                    # Pattern analysis
                    pattern = self.workflow_patterns[i]
                    trigger_diversity = len(set(pattern.get('trigger_pattern', [])))
                    output_diversity = len(set(pattern.get('output_pattern', [])))
                    
                    # Workflow structure analysis
                    workflow_depth = min(node_count // 5, 10)  # Estimated depth
                    parallel_branches = max(1, branching_nodes)
                    sequential_length = node_count - branching_nodes
                    
                    # Create feature vector
                    feature_vector = [
                        # Basic metrics
                        node_count, unique_node_types, connections,
                        
                        # AI features
                        ai_node_count, ai_node_ratio, has_openai, has_langchain,
                        has_claude, has_gemini, has_agents,
                        
                        # Service scores
                        service_scores['data_services_score'],
                        service_scores['communication_score'],
                        service_scores['web_services_score'],
                        service_scores['automation_score'],
                        service_scores['content_services_score'],
                        
                        # Complexity
                        branching_complexity, loop_complexity, error_handling_score,
                        documentation_ratio, trigger_diversity, output_diversity,
                        
                        # Structure
                        workflow_depth, parallel_branches, sequential_length
                    ]
                    
                    features.append(feature_vector)
                    labels.append(pattern['category'])
                    
                except Exception as e:
                    print(f"⚠️ Error processing workflow {i}: {e}")
                    continue
        
        X = np.array(features)
        y = np.array(labels)
        
        print(f"✓ Created {len(features)} samples with {len(feature_names)} enhanced features")
        return X, y, feature_names
    
    def train_production_classifier(self):
        """Train production-ready classifier with advanced techniques"""
        print("\n🎯 Training Production Classifier...")
        
        X, y, feature_names = self.create_enhanced_features()
        
        # Analyze class distribution
        unique_classes, class_counts = np.unique(y, return_counts=True)
        class_distribution = dict(zip(unique_classes, class_counts))
        print(f"Class distribution: {class_distribution}")
        
        # Split data with stratification
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, random_state=42, stratify=y
        )
        
        # Feature scaling
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Create ensemble of balanced classifiers
        classifiers = {
            'balanced_rf': BalancedRandomForestClassifier(
                n_estimators=300,
                max_depth=12,
                min_samples_split=3,
                min_samples_leaf=1,
                random_state=42,
                n_jobs=-1
            ),
            'smote_gb': ImbPipeline([
                ('smote', BorderlineSMOTE(random_state=42, k_neighbors=3)),
                ('gb', GradientBoostingClassifier(
                    n_estimators=200,
                    learning_rate=0.05,
                    max_depth=8,
                    random_state=42
                ))
            ]),
            'adasyn_rf': ImbPipeline([
                ('adasyn', ADASYN(random_state=42, n_neighbors=3)),
                ('rf', RandomForestClassifier(
                    n_estimators=250,
                    max_depth=10,
                    class_weight='balanced',
                    random_state=42,
                    n_jobs=-1
                ))
            ])
        }
        
        # Train and evaluate each classifier
        best_classifier = None
        best_score = 0
        best_name = ""
        
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
        
        for name, classifier in classifiers.items():
            try:
                # Cross-validation
                cv_scores = cross_val_score(classifier, X_train_scaled, y_train, 
                                          cv=cv, scoring='f1_weighted', n_jobs=-1)
                
                # Train and test
                classifier.fit(X_train_scaled, y_train)
                y_pred = classifier.predict(X_test_scaled)
                
                test_f1 = f1_score(y_test, y_pred, average='weighted')
                test_accuracy = accuracy_score(y_test, y_pred)
                
                print(f"✓ {name}: CV F1={cv_scores.mean():.3f}±{cv_scores.std():.3f}, "
                      f"Test F1={test_f1:.3f}, Accuracy={test_accuracy:.3f}")
                
                if test_f1 > best_score:
                    best_score = test_f1
                    best_classifier = classifier
                    best_name = name
                    
            except Exception as e:
                print(f"❌ {name} failed: {e}")
        
        if best_classifier is None:
            print("❌ All classifiers failed, using simple RandomForest")
            best_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            best_classifier.fit(X_train_scaled, y_train)
            best_name = "fallback_rf"
        
        # Final evaluation
        y_pred = best_classifier.predict(X_test_scaled)
        final_accuracy = accuracy_score(y_test, y_pred)
        final_f1 = f1_score(y_test, y_pred, average='weighted')
        
        print(f"\n🏆 Best classifier: {best_name}")
        print(f"Final Accuracy: {final_accuracy:.3f}")
        print(f"Final F1 Score: {final_f1:.3f}")
        
        print(f"\n📊 Detailed Classification Report:")
        print(classification_report(y_test, y_pred))
        
        # Store results
        self.models['production_classifier'] = best_classifier
        self.scalers['production_classifier'] = scaler
        self.performance_metrics['production_classifier'] = {
            'accuracy': final_accuracy,
            'f1_score': final_f1,
            'feature_names': feature_names,
            'class_distribution': class_distribution,
            'best_model': best_name
        }
        
        return best_classifier
    
    def train_advanced_sequence_predictor(self):
        """Train advanced sequence predictor with context awareness"""
        print("\n🔗 Training Advanced Sequence Predictor...")
        
        # Enhanced sequence preparation
        contexts = []
        targets = []
        context_lengths = []
        
        for sequence in self.node_sequences:
            if len(sequence) > 2:
                for i in range(1, len(sequence) - 1):
                    # Multiple context windows
                    for window_size in [2, 3, 4, 5]:
                        if i >= window_size - 1:
                            context = sequence[max(0, i-window_size+1):i+1]
                            target = sequence[i+1]
                            
                            # Add positional encoding
                            context_with_pos = []
                            for pos, node in enumerate(context):
                                # Simplify node names for better generalization
                                simple_node = node.split('.')[-1] if '.' in node else node
                                context_with_pos.append(f"{simple_node}_pos{pos}")
                            
                            contexts.append(' '.join(context_with_pos))
                            targets.append(target.split('.')[-1] if '.' in target else target)
                            context_lengths.append(window_size)
        
        print(f"✓ Generated {len(contexts)} enhanced sequence samples")
        
        # Advanced vectorization
        vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 3),
            min_df=3,
            max_df=0.9,
            analyzer='word',
            token_pattern=r'\b\w+\b'
        )
        
        X_text = vectorizer.fit_transform(contexts)
        
        # Add context length as feature
        context_features = np.array(context_lengths).reshape(-1, 1)
        scaler = StandardScaler()
        context_features_scaled = scaler.fit_transform(context_features)
        
        # Combine features
        from scipy.sparse import hstack
        X_combined = hstack([X_text, context_features_scaled])
        
        y = np.array(targets)
        
        # Handle class imbalance in sequence prediction
        unique_targets, target_counts = np.unique(y, return_counts=True)
        print(f"✓ Predicting {len(unique_targets)} unique node types")
        
        # Filter out very rare targets (appear less than 3 times)
        min_count = 3
        valid_targets = unique_targets[target_counts >= min_count]
        
        # Filter data to only include valid targets
        valid_mask = np.isin(y, valid_targets)
        X_filtered = X_combined[valid_mask]
        y_filtered = y[valid_mask]
        
        print(f"✓ Filtered to {len(y_filtered)} samples with {len(valid_targets)} target classes")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_filtered, y_filtered, test_size=0.2, random_state=42, stratify=y_filtered
        )
        
        # Train balanced classifier
        model = BalancedRandomForestClassifier(
            n_estimators=300,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        print(f"✓ Sequence Predictor - Accuracy: {accuracy:.3f}, F1: {f1:.3f}")
        
        # Store results
        self.models['advanced_sequence_predictor'] = model
        self.vectorizers['sequence'] = vectorizer
        self.scalers['sequence_context'] = scaler
        self.performance_metrics['advanced_sequence_predictor'] = {
            'accuracy': accuracy,
            'f1_score': f1,
            'num_classes': len(valid_targets),
            'sample_count': len(y_filtered)
        }
        
        return model
    
    def train_intelligent_clustering(self):
        """Train intelligent clustering with optimal parameters"""
        print("\n📊 Training Intelligent Clustering...")
        
        # Prepare comprehensive features
        X, _, feature_names = self.create_enhanced_features()
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Find optimal number of clusters
        silhouette_scores = []
        inertias = []
        k_range = range(3, min(15, len(X) // 4))
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=20, max_iter=500)
            cluster_labels = kmeans.fit_predict(X_scaled)
            
            silhouette_avg = silhouette_score(X_scaled, cluster_labels)
            silhouette_scores.append(silhouette_avg)
            inertias.append(kmeans.inertia_)
        
        # Choose optimal k
        best_k_idx = np.argmax(silhouette_scores)
        optimal_k = k_range[best_k_idx]
        best_silhouette = silhouette_scores[best_k_idx]
        
        print(f"✓ Optimal clusters: {optimal_k} (Silhouette: {best_silhouette:.3f})")
        
        # Train final clustering model
        final_kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=20, max_iter=500)
        cluster_labels = final_kmeans.fit_predict(X_scaled)
        
        # Analyze clusters
        cluster_analysis = {}
        workflow_names = self.workflow_features['workflow_name'].tolist()
        
        for cluster_id in range(optimal_k):
            cluster_mask = cluster_labels == cluster_id
            cluster_workflows = [workflow_names[i] for i in range(len(workflow_names)) if cluster_mask[i]]
            cluster_features = X[cluster_mask]
            
            if len(cluster_features) > 0:
                cluster_analysis[f'Cluster_{cluster_id}'] = {
                    'size': len(cluster_workflows),
                    'percentage': (len(cluster_workflows) / len(workflow_names)) * 100,
                    'sample_workflows': cluster_workflows[:3],
                    'characteristics': {
                        'avg_node_count': float(np.mean(cluster_features[:, 0])),
                        'avg_ai_nodes': float(np.mean(cluster_features[:, 3])),
                        'ai_adoption_rate': float(np.mean(cluster_features[:, 5:10]) * 100),
                        'complexity_score': float(np.mean(cluster_features[:, 15:18]))
                    }
                }
        
        # Store results
        self.models['intelligent_clustering'] = final_kmeans
        self.scalers['clustering'] = scaler
        self.cluster_analysis = cluster_analysis
        self.performance_metrics['intelligent_clustering'] = {
            'optimal_k': optimal_k,
            'silhouette_score': best_silhouette,
            'inertia': final_kmeans.inertia_,
            'feature_names': feature_names
        }
        
        print(f"✓ Created {optimal_k} intelligent clusters")
        return final_kmeans
    
    def save_production_models(self, output_dir: str = "production_models"):
        """Save production-ready models with comprehensive metadata"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save models
        for model_name, model in self.models.items():
            model_file = output_path / f"{model_name}.pkl"
            with open(model_file, 'wb') as f:
                pickle.dump(model, f)
            print(f"✓ Saved {model_name}")
        
        # Save preprocessing objects
        for scaler_name, scaler in self.scalers.items():
            scaler_file = output_path / f"{scaler_name}_scaler.pkl"
            with open(scaler_file, 'wb') as f:
                pickle.dump(scaler, f)
        
        for vec_name, vectorizer in self.vectorizers.items():
            vec_file = output_path / f"{vec_name}_vectorizer.pkl"
            with open(vec_file, 'wb') as f:
                pickle.dump(vectorizer, f)
        
        # Save comprehensive metadata
        metadata = {
            'model_performance': self.performance_metrics,
            'training_date': pd.Timestamp.now().isoformat(),
            'data_summary': {
                'total_workflows': len(self.workflow_features),
                'total_sequences': len(self.node_sequences),
                'ai_patterns': len(self.ai_patterns)
            },
            'model_descriptions': {
                'production_classifier': 'Enhanced workflow classification with balanced training',
                'advanced_sequence_predictor': 'Context-aware node sequence prediction',
                'intelligent_clustering': 'Optimized workflow clustering with silhouette analysis'
            }
        }
        
        with open(output_path / "model_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2, default=str)
        
        # Save cluster analysis
        if hasattr(self, 'cluster_analysis'):
            with open(output_path / "cluster_analysis.json", 'w') as f:
                json.dump(self.cluster_analysis, f, indent=2, default=str)
        
        print(f"✓ Production models saved to {output_path}")
        return output_path
    
    def train_all_production_models(self):
        """Train all production-ready models"""
        print("🚀 Training Production-Ready Models")
        print("=" * 60)
        
        try:
            # Train models
            self.train_production_classifier()
            self.train_advanced_sequence_predictor()
            self.train_intelligent_clustering()
            
            # Save models
            model_path = self.save_production_models()
            
            print(f"\n✅ ALL PRODUCTION MODELS TRAINED SUCCESSFULLY!")
            print("=" * 60)
            
            # Performance summary
            print(f"📊 PRODUCTION MODEL PERFORMANCE:")
            for model_name, metrics in self.performance_metrics.items():
                print(f"\n{model_name.replace('_', ' ').title()}:")
                if 'accuracy' in metrics:
                    print(f"  Accuracy: {metrics['accuracy']:.3f}")
                if 'f1_score' in metrics:
                    print(f"  F1 Score: {metrics['f1_score']:.3f}")
                if 'silhouette_score' in metrics:
                    print(f"  Silhouette Score: {metrics['silhouette_score']:.3f}")
            
            print(f"\n🎯 READY FOR PRODUCTION DEPLOYMENT!")
            return self.models
            
        except Exception as e:
            print(f"❌ Production training failed: {e}")
            import traceback
            traceback.print_exc()
            return None

def main():
    """Main function for production training"""
    trainer = OptimizedN8NTrainer()
    models = trainer.train_all_production_models()
    
    if models:
        print(f"\n🎉 SUCCESS: Production models are ready!")
        print(f"Models trained: {list(models.keys())}")
        print(f"Performance metrics available in production_models/model_metadata.json")

if __name__ == "__main__":
    main()