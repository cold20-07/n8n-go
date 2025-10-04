#!/usr/bin/env python3
"""
Improved N8N Workflow Training System
Fixed logic errors and enhanced with better ML practices based on trained data analysis
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.utils.class_weight import compute_class_weight
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline as ImbPipeline
import pickle
import warnings
warnings.filterwarnings('ignore')

class ImprovedN8NWorkflowTrainer:
    def __init__(self, training_data_dir: str = "training_data"):
        self.data_dir = Path(training_data_dir)
        self.models = {}
        self.vectorizers = {}
        self.scalers = {}
        self.encoders = {}
        self.feature_importance = {}
        self.model_performance = {}
        self.load_training_data()
    
    def load_training_data(self):
        """Load all training data files with error handling"""
        print("Loading training data...")
        
        try:
            # Load CSV data
            self.workflow_features = pd.read_csv(self.data_dir / "workflow_features.csv")
            
            # Load JSON data
            with open(self.data_dir / "workflow_patterns.json", 'r') as f:
                self.workflow_patterns = json.load(f)
            
            with open(self.data_dir / "ai_integration_patterns.json", 'r') as f:
                self.ai_patterns = [p for p in json.load(f) if p is not None]
            
            with open(self.data_dir / "node_sequences.json", 'r') as f:
                self.node_sequences = json.load(f)
            
            with open(self.data_dir / "service_combinations.json", 'r') as f:
                self.service_combinations = json.load(f)
            
            with open(self.data_dir / "workflow_templates.json", 'r') as f:
                self.workflow_templates = json.load(f)
            
            with open(self.data_dir / "statistics.json", 'r') as f:
                self.statistics = json.load(f)
            
            print(f"✓ Loaded training data for {len(self.workflow_features)} workflows")
            
        except Exception as e:
            print(f"❌ Error loading training data: {e}")
            raise
    
    def prepare_classification_features(self) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Prepare enhanced features for workflow classification"""
        print("\n🔧 Preparing enhanced classification features...")
        
        features = []
        labels = []
        feature_names = [
            'node_count', 'has_ai_nodes', 'has_openai', 'has_langchain',
            'has_google_services', 'has_slack', 'has_webhook', 'has_schedule',
            'connections_count', 'sticky_notes_count', 'error_handling_nodes',
            'node_type_diversity', 'ai_node_ratio', 'complexity_score',
            'trigger_count', 'output_count', 'processing_node_ratio'
        ]
        
        for i, (_, row) in enumerate(self.workflow_features.iterrows()):
            if i < len(self.workflow_patterns):
                # Basic features
                node_count = row['node_count']
                has_ai = int(row['has_ai_nodes'])
                has_openai = int(row['has_openai'])
                has_langchain = int(row['has_langchain'])
                has_google = int(row['has_google_services'])
                has_slack = int(row['has_slack'])
                has_webhook = int(row['has_webhook'])
                has_schedule = int(row['has_schedule'])
                connections = row['connections_count']
                sticky_notes = row['sticky_notes_count']
                error_handling = row['error_handling_nodes']
                
                # Enhanced features
                try:
                    node_types = eval(row['node_types']) if isinstance(row['node_types'], str) else row['node_types']
                    node_type_diversity = len(set(node_types)) if node_types else 0
                except:
                    node_type_diversity = 0
                
                # AI node ratio
                try:
                    ai_node_types = eval(row['ai_node_types']) if isinstance(row['ai_node_types'], str) else row['ai_node_types']
                    ai_node_count = len(ai_node_types) if ai_node_types else 0
                    ai_node_ratio = ai_node_count / max(node_count, 1)
                except:
                    ai_node_ratio = 0
                
                # Complexity score (improved calculation)
                complexity_score = (
                    node_count * 1.0 +
                    node_type_diversity * 2.0 +
                    connections * 0.5 +
                    ai_node_count * 1.5 +
                    error_handling * 2.0
                )
                
                # Pattern-based features
                pattern = self.workflow_patterns[i]
                trigger_count = len(pattern.get('trigger_pattern', []))
                output_count = len(pattern.get('output_pattern', []))
                processing_nodes = len(pattern.get('processing_pattern', []))
                processing_node_ratio = processing_nodes / max(node_count, 1)
                
                feature_vector = [
                    node_count, has_ai, has_openai, has_langchain,
                    has_google, has_slack, has_webhook, has_schedule,
                    connections, sticky_notes, error_handling,
                    node_type_diversity, ai_node_ratio, complexity_score,
                    trigger_count, output_count, processing_node_ratio
                ]
                
                features.append(feature_vector)
                labels.append(pattern['category'])
        
        X = np.array(features)
        y = np.array(labels)
        
        print(f"✓ Prepared {len(features)} samples with {len(feature_names)} features")
        print(f"✓ Class distribution: {dict(zip(*np.unique(y, return_counts=True)))}")
        
        return X, y, feature_names
    
    def train_improved_workflow_classifier(self):
        """Train an improved workflow classifier with better handling of class imbalance"""
        print("\n🎯 Training Improved Workflow Classifier...")
        
        X, y, feature_names = self.prepare_classification_features()
        
        # Handle class imbalance
        class_counts = dict(zip(*np.unique(y, return_counts=True)))
        print(f"Original class distribution: {class_counts}")
        
        # Use SMOTE for oversampling minority classes
        smote = SMOTE(random_state=42, k_neighbors=min(3, min(class_counts.values()) - 1))
        
        # Split data first
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Apply SMOTE only to training data
        try:
            X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)
            print(f"✓ Applied SMOTE: {len(X_train)} → {len(X_train_balanced)} training samples")
        except ValueError as e:
            print(f"⚠️ SMOTE failed ({e}), using original data with class weights")
            X_train_balanced, y_train_balanced = X_train, y_train
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train_balanced)
        X_test_scaled = scaler.transform(X_test)
        
        # Calculate class weights for remaining imbalance
        classes = np.unique(y_train_balanced)
        class_weights = compute_class_weight('balanced', classes=classes, y=y_train_balanced)
        class_weight_dict = dict(zip(classes, class_weights))
        
        # Try multiple algorithms
        algorithms = {
            'RandomForest': RandomForestClassifier(
                n_estimators=200,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                class_weight=class_weight_dict,
                random_state=42
            ),
            'GradientBoosting': GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=6,
                random_state=42
            )
        }
        
        best_model = None
        best_score = 0
        best_name = ""
        
        for name, model in algorithms.items():
            # Cross-validation
            cv_scores = cross_val_score(model, X_train_scaled, y_train_balanced, cv=5, scoring='accuracy')
            mean_cv_score = cv_scores.mean()
            
            # Train and test
            model.fit(X_train_scaled, y_train_balanced)
            y_pred = model.predict(X_test_scaled)
            test_accuracy = accuracy_score(y_test, y_pred)
            
            print(f"✓ {name}: CV={mean_cv_score:.3f}, Test={test_accuracy:.3f}")
            
            if test_accuracy > best_score:
                best_score = test_accuracy
                best_model = model
                best_name = name
        
        print(f"✓ Best model: {best_name} (Accuracy: {best_score:.3f})")
        
        # Feature importance
        if hasattr(best_model, 'feature_importances_'):
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': best_model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print(f"\n📊 Top 5 Most Important Features:")
            for _, row in importance_df.head().iterrows():
                print(f"   {row['feature']}: {row['importance']:.3f}")
            
            self.feature_importance['workflow_classifier'] = importance_df
        
        # Detailed evaluation
        y_pred = best_model.predict(X_test_scaled)
        print(f"\n📈 Classification Report:")
        print(classification_report(y_test, y_pred))
        
        # Store model and preprocessing
        self.models['workflow_classifier'] = best_model
        self.scalers['workflow_classifier'] = scaler
        self.model_performance['workflow_classifier'] = {
            'accuracy': best_score,
            'cv_scores': cv_scores.tolist(),
            'feature_names': feature_names,
            'class_distribution': class_counts
        }
        
        return best_model
    
    def train_enhanced_sequence_predictor(self):
        """Train an enhanced sequence predictor with better context handling"""
        print("\n🔗 Training Enhanced Node Sequence Predictor...")
        
        # Prepare enhanced sequence data
        sequences = []
        next_nodes = []
        contexts = []
        
        for sequence in self.node_sequences:
            if len(sequence) > 1:
                for i in range(len(sequence) - 1):
                    # Use variable context window (1-5 nodes)
                    for context_size in [1, 2, 3]:
                        if i >= context_size - 1:
                            context_start = max(0, i - context_size + 1)
                            context = sequence[context_start:i+1]
                            next_node = sequence[i+1]
                            
                            # Create features
                            context_text = ' '.join(context)
                            sequences.append(context_text)
                            next_nodes.append(next_node)
                            contexts.append(len(context))
        
        print(f"✓ Generated {len(sequences)} sequence samples")
        
        # Enhanced vectorization
        vectorizer = TfidfVectorizer(
            max_features=2000,
            ngram_range=(1, 3),
            min_df=2,
            max_df=0.95,
            stop_words=None  # Don't remove node type words
        )
        
        X_text = vectorizer.fit_transform(sequences)
        
        # Add context length as feature
        context_features = np.array(contexts).reshape(-1, 1)
        scaler = StandardScaler()
        context_features_scaled = scaler.fit_transform(context_features)
        
        # Combine text and context features
        from scipy.sparse import hstack
        X_combined = hstack([X_text, context_features_scaled])
        
        y = np.array(next_nodes)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_combined, y, test_size=0.2, random_state=42
        )
        
        # Train model with class balancing
        unique_classes = np.unique(y_train)
        if len(unique_classes) > 2:  # Multi-class
            class_weights = compute_class_weight('balanced', classes=unique_classes, y=y_train)
            class_weight_dict = dict(zip(unique_classes, class_weights))
        else:
            class_weight_dict = 'balanced'
        
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            class_weight=class_weight_dict,
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"✓ Sequence Predictor Accuracy: {accuracy:.3f}")
        print(f"✓ Predicting from {len(unique_classes)} possible node types")
        
        # Store models
        self.models['sequence_predictor'] = model
        self.vectorizers['sequence'] = vectorizer
        self.scalers['sequence_context'] = scaler
        self.model_performance['sequence_predictor'] = {
            'accuracy': accuracy,
            'num_classes': len(unique_classes),
            'sample_count': len(sequences)
        }
        
        return model
    
    def train_advanced_ai_pattern_analyzer(self):
        """Train an advanced AI pattern analyzer"""
        print("\n🤖 Training Advanced AI Pattern Analyzer...")
        
        if not self.ai_patterns:
            print("⚠️ No AI patterns available for training")
            return None
        
        # Enhanced AI pattern features
        features = []
        labels = []
        
        for pattern in self.ai_patterns:
            if pattern and 'ai_nodes' in pattern:
                ai_nodes = pattern.get('ai_nodes', [])
                ai_params = pattern.get('ai_parameters', [])
                
                # Feature extraction
                feature_vector = [
                    len(ai_nodes),  # Number of AI nodes
                    len(ai_params),  # Number of AI parameters
                    int('openai' in str(ai_nodes).lower()),  # Uses OpenAI
                    int('langchain' in str(ai_nodes).lower()),  # Uses LangChain
                    int('gpt' in str(ai_nodes).lower()),  # Uses GPT
                    int('claude' in str(ai_nodes).lower()),  # Uses Claude
                    int('gemini' in str(ai_nodes).lower()),  # Uses Gemini
                    int('agent' in str(ai_nodes).lower()),  # Uses AI agents
                    int('chain' in str(ai_nodes).lower()),  # Uses chains
                    int('embedding' in str(ai_nodes).lower()),  # Uses embeddings
                ]
                
                features.append(feature_vector)
                
                # Enhanced labeling based on complexity and type
                ai_node_count = len(ai_nodes)
                has_agent = 'agent' in str(ai_nodes).lower()
                has_chain = 'chain' in str(ai_nodes).lower()
                has_embedding = 'embedding' in str(ai_nodes).lower()
                
                if has_agent or (ai_node_count >= 5):
                    label = 'Advanced AI'
                elif has_chain or has_embedding or (ai_node_count >= 3):
                    label = 'Intermediate AI'
                else:
                    label = 'Basic AI'
                
                labels.append(label)
        
        if not features:
            print("⚠️ No valid AI features extracted")
            return None
        
        X = np.array(features)
        y = np.array(labels)
        
        print(f"✓ AI Pattern distribution: {dict(zip(*np.unique(y, return_counts=True)))}")
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=100,
            max_depth=8,
            class_weight='balanced',
            random_state=42
        )
        
        # Cross-validation
        cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')
        model.fit(X, y)
        
        print(f"✓ AI Pattern Analyzer CV Accuracy: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
        
        self.models['ai_pattern_analyzer'] = model
        self.model_performance['ai_pattern_analyzer'] = {
            'cv_accuracy': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'feature_count': X.shape[1],
            'sample_count': len(features)
        }
        
        return model
    
    def train_intelligent_clustering(self):
        """Train intelligent workflow clustering with optimal cluster selection"""
        print("\n📊 Training Intelligent Workflow Clustering...")
        
        # Prepare comprehensive features for clustering
        features = []
        workflow_names = []
        
        for i, (_, row) in enumerate(self.workflow_features.iterrows()):
            if i < len(self.workflow_patterns):
                pattern = self.workflow_patterns[i]
                
                feature_vector = [
                    row['node_count'],
                    row['workflow_complexity'],
                    int(row['has_ai_nodes']),
                    int(row['has_openai']),
                    int(row['has_langchain']),
                    int(row['has_google_services']),
                    int(row['has_slack']),
                    int(row['has_webhook']),
                    row['connections_count'],
                    row['sticky_notes_count'],
                    len(pattern.get('trigger_pattern', [])),
                    len(pattern.get('output_pattern', [])),
                    len(pattern.get('processing_pattern', []))
                ]
                
                features.append(feature_vector)
                workflow_names.append(row['workflow_name'])
        
        X = np.array(features)
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Find optimal number of clusters using elbow method and silhouette score
        from sklearn.metrics import silhouette_score
        
        inertias = []
        silhouette_scores = []
        k_range = range(2, min(11, len(X) // 3))  # Reasonable range
        
        for k in k_range:
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            kmeans.fit(X_scaled)
            inertias.append(kmeans.inertia_)
            silhouette_scores.append(silhouette_score(X_scaled, kmeans.labels_))
        
        # Choose k with best silhouette score
        best_k = k_range[np.argmax(silhouette_scores)]
        best_silhouette = max(silhouette_scores)
        
        print(f"✓ Optimal clusters: {best_k} (Silhouette Score: {best_silhouette:.3f})")
        
        # Train final clustering model
        final_kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
        clusters = final_kmeans.fit_predict(X_scaled)
        
        # Analyze clusters
        cluster_analysis = {}
        for i in range(best_k):
            cluster_mask = clusters == i
            cluster_workflows = [workflow_names[j] for j in range(len(workflow_names)) if cluster_mask[j]]
            cluster_features = X[cluster_mask]
            
            if len(cluster_features) > 0:
                cluster_analysis[f'Cluster_{i}'] = {
                    'count': len(cluster_workflows),
                    'workflows': cluster_workflows[:5],  # Sample workflows
                    'characteristics': {
                        'avg_node_count': float(np.mean(cluster_features[:, 0])),
                        'avg_complexity': float(np.mean(cluster_features[:, 1])),
                        'ai_usage_rate': float(np.mean(cluster_features[:, 2]) * 100),
                        'openai_usage_rate': float(np.mean(cluster_features[:, 3]) * 100),
                        'langchain_usage_rate': float(np.mean(cluster_features[:, 4]) * 100)
                    }
                }
        
        self.models['workflow_clusters'] = final_kmeans
        self.scalers['clustering'] = scaler
        self.cluster_analysis = cluster_analysis
        self.model_performance['clustering'] = {
            'optimal_k': best_k,
            'silhouette_score': best_silhouette,
            'inertia': final_kmeans.inertia_
        }
        
        print(f"✓ Created {best_k} workflow clusters")
        return final_kmeans, cluster_analysis
    
    def generate_intelligent_recommendations(self, requirements: Dict) -> List[Dict]:
        """Generate intelligent workflow recommendations using trained models"""
        print(f"\n💡 Generating intelligent recommendations...")
        
        recommendations = []
        
        # Enhanced similarity calculation
        for template in self.workflow_templates:
            score = self.calculate_enhanced_similarity_score(template, requirements)
            if score > 0.2:  # Lower threshold for more recommendations
                
                # Predict category using trained classifier
                predicted_category = self.predict_workflow_category(template)
                
                # Calculate confidence based on multiple factors
                confidence = self.calculate_recommendation_confidence(template, requirements, score)
                
                recommendations.append({
                    'workflow': template,
                    'similarity_score': score,
                    'predicted_category': predicted_category,
                    'confidence': confidence,
                    'reason': self.explain_enhanced_recommendation(template, requirements)
                })
        
        # Sort by combined score (similarity + confidence)
        recommendations.sort(key=lambda x: x['similarity_score'] * x['confidence'], reverse=True)
        
        return recommendations[:10]  # Return top 10 recommendations
    
    def calculate_enhanced_similarity_score(self, template: Dict, requirements: Dict) -> float:
        """Calculate enhanced similarity score with more sophisticated matching"""
        score = 0.0
        
        nodes = template.get('nodes', [])
        node_types = [node.get('type', '') for node in nodes]
        
        # AI requirements matching
        if requirements.get('needs_ai', False):
            ai_nodes = [node for node in nodes 
                       if any(ai_term in node.get('type', '').lower() 
                             for ai_term in ['openai', 'langchain', 'ai', 'gpt', 'claude', 'gemini'])]
            if ai_nodes:
                score += 0.3
                # Bonus for specific AI types
                if requirements.get('ai_type'):
                    if requirements['ai_type'].lower() in str(node_types).lower():
                        score += 0.2
        
        # Service requirements matching
        required_services = requirements.get('services', [])
        for service in required_services:
            matches = sum(1 for node_type in node_types 
                         if service.lower() in node_type.lower())
            if matches > 0:
                score += min(0.2 * matches, 0.4)  # Cap bonus per service
        
        # Complexity matching
        node_count = len(nodes)
        required_complexity = requirements.get('complexity', 'medium')
        
        complexity_ranges = {
            'simple': (1, 15),
            'medium': (10, 30),
            'complex': (25, 100)
        }
        
        min_nodes, max_nodes = complexity_ranges.get(required_complexity, (1, 100))
        if min_nodes <= node_count <= max_nodes:
            score += 0.2
        
        # Industry/domain matching
        if requirements.get('domain'):
            domain_keywords = {
                'content': ['wordpress', 'blog', 'content', 'cms'],
                'communication': ['slack', 'email', 'telegram', 'discord'],
                'data': ['sheets', 'database', 'csv', 'analytics'],
                'ecommerce': ['shopify', 'woocommerce', 'stripe', 'payment']
            }
            
            domain = requirements['domain'].lower()
            if domain in domain_keywords:
                keywords = domain_keywords[domain]
                for keyword in keywords:
                    if any(keyword in node_type.lower() for node_type in node_types):
                        score += 0.15
                        break
        
        return min(score, 1.0)
    
    def predict_workflow_category(self, template: Dict) -> str:
        """Predict workflow category using trained classifier"""
        try:
            if 'workflow_classifier' not in self.models:
                return "Unknown"
            
            # Extract features for prediction
            nodes = template.get('nodes', [])
            node_count = len(nodes)
            
            # Simplified feature extraction for prediction
            has_ai = any(ai_term in str(nodes).lower() 
                        for ai_term in ['openai', 'langchain', 'ai', 'gpt'])
            has_openai = 'openai' in str(nodes).lower()
            has_langchain = 'langchain' in str(nodes).lower()
            has_google = 'google' in str(nodes).lower()
            has_slack = 'slack' in str(nodes).lower()
            
            # Create feature vector (simplified version)
            features = np.array([[
                node_count, int(has_ai), int(has_openai), int(has_langchain),
                int(has_google), int(has_slack), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
            ]])
            
            # Scale features if scaler is available
            if 'workflow_classifier' in self.scalers:
                features = self.scalers['workflow_classifier'].transform(features)
            
            prediction = self.models['workflow_classifier'].predict(features)
            return prediction[0]
            
        except Exception as e:
            print(f"⚠️ Category prediction failed: {e}")
            return "Unknown"
    
    def calculate_recommendation_confidence(self, template: Dict, requirements: Dict, similarity_score: float) -> float:
        """Calculate confidence score for recommendation"""
        confidence = similarity_score
        
        # Boost confidence for exact matches
        nodes = template.get('nodes', [])
        required_services = requirements.get('services', [])
        
        exact_matches = sum(1 for service in required_services
                           if any(service.lower() in node.get('type', '').lower() for node in nodes))
        
        if exact_matches > 0:
            confidence += 0.1 * exact_matches
        
        # Boost confidence for popular/well-documented workflows
        if len(nodes) > 5:  # Substantial workflow
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def explain_enhanced_recommendation(self, template: Dict, requirements: Dict) -> str:
        """Generate enhanced explanation for recommendation"""
        reasons = []
        
        nodes = template.get('nodes', [])
        node_types = [node.get('type', '') for node in nodes]
        
        # AI usage explanation
        ai_nodes = [node for node in nodes 
                   if any(ai_term in node.get('type', '').lower() 
                         for ai_term in ['openai', 'langchain', 'ai', 'gpt'])]
        if ai_nodes and requirements.get('needs_ai', False):
            ai_types = set()
            for node in ai_nodes:
                node_type = node.get('type', '')
                if 'openai' in node_type.lower():
                    ai_types.add('OpenAI')
                elif 'langchain' in node_type.lower():
                    ai_types.add('LangChain')
            reasons.append(f"Uses {', '.join(ai_types)} ({len(ai_nodes)} AI nodes)")
        
        # Service integration explanation
        required_services = requirements.get('services', [])
        matching_services = []
        for service in required_services:
            if any(service.lower() in node_type.lower() for node_type in node_types):
                matching_services.append(service.title())
        
        if matching_services:
            reasons.append(f"Integrates with {', '.join(matching_services)}")
        
        # Complexity explanation
        node_count = len(nodes)
        if requirements.get('complexity') == 'simple' and node_count <= 15:
            reasons.append(f"Simple workflow ({node_count} nodes)")
        elif requirements.get('complexity') == 'complex' and node_count >= 25:
            reasons.append(f"Complex workflow ({node_count} nodes)")
        
        return '; '.join(reasons) if reasons else "General pattern match"
    
    def save_improved_models(self, output_dir: str = "improved_models"):
        """Save all improved models with metadata"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save models
        for model_name, model in self.models.items():
            with open(output_path / f"{model_name}.pkl", 'wb') as f:
                pickle.dump(model, f)
        
        # Save preprocessing objects
        for scaler_name, scaler in self.scalers.items():
            with open(output_path / f"{scaler_name}_scaler.pkl", 'wb') as f:
                pickle.dump(scaler, f)
        
        for vec_name, vectorizer in self.vectorizers.items():
            with open(output_path / f"{vec_name}_vectorizer.pkl", 'wb') as f:
                pickle.dump(vectorizer, f)
        
        # Save performance metrics
        with open(output_path / "model_performance.json", 'w') as f:
            json.dump(self.model_performance, f, indent=2, default=str)
        
        # Save feature importance
        if self.feature_importance:
            for model_name, importance_df in self.feature_importance.items():
                importance_df.to_csv(output_path / f"{model_name}_feature_importance.csv", index=False)
        
        # Save cluster analysis
        if hasattr(self, 'cluster_analysis'):
            with open(output_path / "cluster_analysis.json", 'w') as f:
                json.dump(self.cluster_analysis, f, indent=2, default=str)
        
        print(f"✓ Improved models saved to {output_path}")
        return output_path
    
    def train_all_improved_models(self):
        """Train all improved models with better error handling"""
        print("🚀 Starting improved model training...")
        
        try:
            # Train models with error handling
            self.train_improved_workflow_classifier()
            self.train_enhanced_sequence_predictor()
            self.train_advanced_ai_pattern_analyzer()
            self.train_intelligent_clustering()
            
            # Save all models
            self.save_improved_models()
            
            print("\n✅ All improved models trained successfully!")
            
            # Print performance summary
            print(f"\n📊 MODEL PERFORMANCE SUMMARY")
            print("=" * 50)
            for model_name, performance in self.model_performance.items():
                print(f"{model_name}:")
                if 'accuracy' in performance:
                    print(f"  Accuracy: {performance['accuracy']:.3f}")
                if 'cv_accuracy' in performance:
                    print(f"  CV Accuracy: {performance['cv_accuracy']:.3f}")
                if 'silhouette_score' in performance:
                    print(f"  Silhouette Score: {performance['silhouette_score']:.3f}")
                print()
            
            return self.models
            
        except Exception as e:
            print(f"❌ Training failed: {e}")
            import traceback
            traceback.print_exc()
            return None

def main():
    """Main function to run improved training"""
    # Initialize improved trainer
    trainer = ImprovedN8NWorkflowTrainer()
    
    # Train all improved models
    models = trainer.train_all_improved_models()
    
    if models:
        # Demo: Enhanced recommendations
        print("\n🎯 DEMO: Enhanced Workflow Recommendations")
        print("=" * 60)
        
        test_scenarios = [
            {
                'name': 'AI Content Creation',
                'requirements': {
                    'needs_ai': True,
                    'services': ['openai', 'wordpress'],
                    'complexity': 'medium',
                    'domain': 'content'
                }
            },
            {
                'name': 'Business Communication Automation',
                'requirements': {
                    'needs_ai': True,
                    'services': ['slack', 'email'],
                    'complexity': 'simple',
                    'domain': 'communication'
                }
            }
        ]
        
        for scenario in test_scenarios:
            print(f"\n📋 Scenario: {scenario['name']}")
            recommendations = trainer.generate_intelligent_recommendations(scenario['requirements'])
            
            print(f"Found {len(recommendations)} recommendations:")
            for i, rec in enumerate(recommendations[:3], 1):
                print(f"{i}. {rec['workflow']['name'][:60]}...")
                print(f"   Score: {rec['similarity_score']:.2f}, Confidence: {rec['confidence']:.2f}")
                print(f"   Category: {rec['predicted_category']}")
                print(f"   Reason: {rec['reason']}")
                print()

if __name__ == "__main__":
    main()