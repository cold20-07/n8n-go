#!/usr/bin/env python3
"""
Final N8N Workflow Training System
Production-ready system with all fixes applied and error handling
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import classification_report, accuracy_score, f1_score
from sklearn.preprocessing import StandardScaler
from sklearn.utils.class_weight import compute_class_weight
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import pickle
import warnings
warnings.filterwarnings('ignore')

class FinalN8NTrainer:
    def __init__(self, training_data_dir: str = "training_data"):
        self.data_dir = Path(training_data_dir)
        self.models = {}
        self.vectorizers = {}
        self.scalers = {}
        self.performance_metrics = {}
        self.load_and_validate_data()
    
    def load_and_validate_data(self):
        """Load and validate training data"""
        print("📊 Loading training data...")
        
        try:
            # Load data
            self.workflow_features = pd.read_csv(self.data_dir / "workflow_features.csv")
            
            with open(self.data_dir / "workflow_patterns.json", 'r') as f:
                self.workflow_patterns = json.load(f)
            
            with open(self.data_dir / "ai_integration_patterns.json", 'r') as f:
                self.ai_patterns = [p for p in json.load(f) if p is not None]
            
            with open(self.data_dir / "node_sequences.json", 'r') as f:
                self.node_sequences = json.load(f)
            
            # Clean data
            self.clean_data()
            
            print(f"✓ Loaded {len(self.workflow_features)} workflows")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            raise
    
    def clean_data(self):
        """Clean and preprocess data"""
        print("🧹 Cleaning data...")
        
        # Handle missing values
        numeric_columns = self.workflow_features.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            if self.workflow_features[col].isnull().sum() > 0:
                median_val = self.workflow_features[col].median()
                self.workflow_features[col].fillna(median_val, inplace=True)
        
        # Handle categorical missing values
        categorical_columns = self.workflow_features.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if self.workflow_features[col].isnull().sum() > 0:
                self.workflow_features[col].fillna('unknown', inplace=True)
        
        print(f"✓ Data cleaned")
    
    def create_robust_features(self) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Create robust features with error handling"""
        print("🔧 Creating robust features...")
        
        features = []
        labels = []
        
        feature_names = [
            'node_count', 'unique_node_types', 'connections_count',
            'ai_node_count', 'ai_node_ratio', 'has_openai', 'has_langchain',
            'has_google', 'has_slack', 'has_webhook', 'has_schedule',
            'branching_complexity', 'documentation_ratio', 'error_handling_ratio',
            'trigger_count', 'output_count', 'complexity_score'
        ]
        
        for i, (_, row) in enumerate(self.workflow_features.iterrows()):
            if i < len(self.workflow_patterns):
                try:
                    # Basic metrics
                    node_count = max(1, row['node_count'])  # Avoid division by zero
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
                    ai_node_ratio = ai_node_count / node_count
                    
                    # Service detection
                    node_types_str = ' '.join(node_types).lower()
                    has_openai = int('openai' in node_types_str)
                    has_langchain = int('langchain' in node_types_str)
                    has_google = int('google' in node_types_str)
                    has_slack = int('slack' in node_types_str)
                    has_webhook = int('webhook' in node_types_str)
                    has_schedule = int('schedule' in node_types_str)
                    
                    # Complexity metrics
                    branching_nodes = sum(1 for nt in node_types if 'if' in nt.lower())
                    branching_complexity = branching_nodes / node_count
                    
                    sticky_notes = row.get('sticky_notes_count', 0)
                    documentation_ratio = sticky_notes / node_count
                    
                    error_handling = row.get('error_handling_nodes', 0)
                    error_handling_ratio = error_handling / node_count
                    
                    # Pattern features
                    pattern = self.workflow_patterns[i]
                    trigger_count = len(pattern.get('trigger_pattern', []))
                    output_count = len(pattern.get('output_pattern', []))
                    
                    # Overall complexity score
                    complexity_score = (
                        node_count * 0.5 +
                        unique_node_types * 1.0 +
                        ai_node_count * 1.5 +
                        branching_nodes * 2.0 +
                        connections * 0.3
                    )
                    
                    # Create feature vector
                    feature_vector = [
                        node_count, unique_node_types, connections,
                        ai_node_count, ai_node_ratio, has_openai, has_langchain,
                        has_google, has_slack, has_webhook, has_schedule,
                        branching_complexity, documentation_ratio, error_handling_ratio,
                        trigger_count, output_count, complexity_score
                    ]
                    
                    features.append(feature_vector)
                    labels.append(pattern['category'])
                    
                except Exception as e:
                    print(f"⚠️ Error processing workflow {i}: {e}")
                    continue
        
        X = np.array(features)
        y = np.array(labels)
        
        print(f"✓ Created {len(features)} samples with {len(feature_names)} features")
        return X, y, feature_names
    
    def train_robust_classifier(self):
        """Train robust classifier with proper error handling"""
        print("\n🎯 Training Robust Classifier...")
        
        X, y, feature_names = self.create_robust_features()
        
        if len(X) == 0:
            print("❌ No valid features created")
            return None
        
        # Check class distribution
        unique_classes, class_counts = np.unique(y, return_counts=True)
        class_distribution = dict(zip(unique_classes, class_counts))
        print(f"Class distribution: {class_distribution}")
        
        # Handle small dataset
        if len(X) < 10:
            print("⚠️ Very small dataset, using simple model")
            test_size = 0.2
        else:
            test_size = 0.25
        
        # Split data
        try:
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42, stratify=y
            )
        except ValueError:
            # If stratification fails, split without stratification
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=42
            )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Calculate class weights
        classes = np.unique(y_train)
        class_weights = compute_class_weight('balanced', classes=classes, y=y_train)
        class_weight_dict = dict(zip(classes, class_weights))
        
        # Train robust classifier
        classifier = RandomForestClassifier(
            n_estimators=min(200, len(X_train) * 5),  # Adjust based on data size
            max_depth=min(10, len(feature_names)),
            min_samples_split=max(2, len(X_train) // 20),
            min_samples_leaf=max(1, len(X_train) // 50),
            class_weight=class_weight_dict,
            random_state=42,
            n_jobs=-1
        )
        
        # Train and evaluate
        classifier.fit(X_train_scaled, y_train)
        y_pred = classifier.predict(X_test_scaled)
        
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        print(f"✓ Classifier - Accuracy: {accuracy:.3f}, F1: {f1:.3f}")
        
        # Feature importance
        if hasattr(classifier, 'feature_importances_'):
            importance_df = pd.DataFrame({
                'feature': feature_names,
                'importance': classifier.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print(f"\n📊 Top 5 Features:")
            for _, row in importance_df.head().iterrows():
                print(f"   {row['feature']}: {row['importance']:.3f}")
        
        # Store results
        self.models['robust_classifier'] = classifier
        self.scalers['robust_classifier'] = scaler
        self.performance_metrics['robust_classifier'] = {
            'accuracy': accuracy,
            'f1_score': f1,
            'feature_names': feature_names,
            'class_distribution': class_distribution
        }
        
        return classifier
    
    def train_sequence_predictor(self):
        """Train sequence predictor with proper matrix handling"""
        print("\n🔗 Training Sequence Predictor...")
        
        # Prepare sequence data
        contexts = []
        targets = []
        
        for sequence in self.node_sequences:
            if len(sequence) > 2:
                for i in range(1, len(sequence) - 1):
                    # Use context window of 2-3 nodes
                    for window_size in [2, 3]:
                        if i >= window_size - 1:
                            context = sequence[max(0, i-window_size+1):i+1]
                            target = sequence[i+1]
                            
                            # Simplify node names
                            simple_context = []
                            for node in context:
                                simple_node = node.split('.')[-1] if '.' in node else node
                                simple_context.append(simple_node)
                            
                            simple_target = target.split('.')[-1] if '.' in target else target
                            
                            contexts.append(' '.join(simple_context))
                            targets.append(simple_target)
        
        if len(contexts) == 0:
            print("⚠️ No sequence data available")
            return None
        
        print(f"✓ Generated {len(contexts)} sequence samples")
        
        # Vectorize with simpler parameters
        vectorizer = TfidfVectorizer(
            max_features=min(1000, len(contexts) // 2),
            ngram_range=(1, 2),
            min_df=max(1, len(contexts) // 100),
            max_df=0.95
        )
        
        X = vectorizer.fit_transform(contexts)
        y = np.array(targets)
        
        # Filter rare targets
        unique_targets, target_counts = np.unique(y, return_counts=True)
        min_count = max(2, len(contexts) // 200)
        valid_targets = unique_targets[target_counts >= min_count]
        
        # Convert sparse matrix to dense for indexing
        X_dense = X.toarray()
        valid_mask = np.isin(y, valid_targets)
        X_filtered = X_dense[valid_mask]
        y_filtered = y[valid_mask]
        
        if len(X_filtered) == 0:
            print("⚠️ No valid sequence samples after filtering")
            return None
        
        print(f"✓ Filtered to {len(y_filtered)} samples with {len(valid_targets)} targets")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_filtered, y_filtered, test_size=0.2, random_state=42
        )
        
        # Train model
        model = RandomForestClassifier(
            n_estimators=min(100, len(X_train)),
            max_depth=min(10, X_train.shape[1] // 10),
            class_weight='balanced',
            random_state=42,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"✓ Sequence Predictor - Accuracy: {accuracy:.3f}")
        
        # Store results
        self.models['sequence_predictor'] = model
        self.vectorizers['sequence'] = vectorizer
        self.performance_metrics['sequence_predictor'] = {
            'accuracy': accuracy,
            'num_classes': len(valid_targets),
            'sample_count': len(y_filtered)
        }
        
        return model
    
    def train_clustering(self):
        """Train clustering with optimal parameters"""
        print("\n📊 Training Clustering...")
        
        X, _, feature_names = self.create_robust_features()
        
        if len(X) < 6:
            print("⚠️ Too few samples for clustering")
            return None
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Find optimal clusters
        max_k = min(8, len(X) // 2)
        if max_k < 2:
            max_k = 2
        
        best_k = 3  # Default
        best_silhouette = -1
        
        for k in range(2, max_k + 1):
            try:
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                labels = kmeans.fit_predict(X_scaled)
                silhouette = silhouette_score(X_scaled, labels)
                
                if silhouette > best_silhouette:
                    best_silhouette = silhouette
                    best_k = k
            except:
                continue
        
        print(f"✓ Optimal clusters: {best_k} (Silhouette: {best_silhouette:.3f})")
        
        # Train final model
        final_kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
        cluster_labels = final_kmeans.fit_predict(X_scaled)
        
        # Store results
        self.models['clustering'] = final_kmeans
        self.scalers['clustering'] = scaler
        self.performance_metrics['clustering'] = {
            'optimal_k': best_k,
            'silhouette_score': best_silhouette
        }
        
        return final_kmeans
    
    def save_models(self, output_dir: str = "final_models"):
        """Save all models"""
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
        
        # Save metadata
        metadata = {
            'model_performance': self.performance_metrics,
            'training_summary': {
                'total_workflows': len(self.workflow_features),
                'models_trained': list(self.models.keys()),
                'training_date': pd.Timestamp.now().isoformat()
            }
        }
        
        with open(output_path / "model_metadata.json", 'w') as f:
            json.dump(metadata, f, indent=2, default=str)
        
        print(f"✓ Models saved to {output_path}")
        return output_path
    
    def train_all_models(self):
        """Train all models with comprehensive error handling"""
        print("🚀 Training Final N8N Models")
        print("=" * 50)
        
        success_count = 0
        
        # Train classifier
        try:
            classifier = self.train_robust_classifier()
            if classifier is not None:
                success_count += 1
        except Exception as e:
            print(f"❌ Classifier training failed: {e}")
        
        # Train sequence predictor
        try:
            seq_model = self.train_sequence_predictor()
            if seq_model is not None:
                success_count += 1
        except Exception as e:
            print(f"❌ Sequence predictor training failed: {e}")
        
        # Train clustering
        try:
            cluster_model = self.train_clustering()
            if cluster_model is not None:
                success_count += 1
        except Exception as e:
            print(f"❌ Clustering training failed: {e}")
        
        # Save models
        if success_count > 0:
            model_path = self.save_models()
            
            print(f"\n✅ TRAINING COMPLETE!")
            print("=" * 50)
            print(f"Successfully trained: {success_count}/3 models")
            
            # Performance summary
            print(f"\n📊 MODEL PERFORMANCE:")
            for model_name, metrics in self.performance_metrics.items():
                print(f"\n{model_name.replace('_', ' ').title()}:")
                if 'accuracy' in metrics:
                    print(f"  Accuracy: {metrics['accuracy']:.3f}")
                if 'f1_score' in metrics:
                    print(f"  F1 Score: {metrics['f1_score']:.3f}")
                if 'silhouette_score' in metrics:
                    print(f"  Silhouette Score: {metrics['silhouette_score']:.3f}")
            
            return self.models
        else:
            print("❌ No models were successfully trained")
            return None

def main():
    """Main training function"""
    trainer = FinalN8NTrainer()
    models = trainer.train_all_models()
    
    if models:
        print(f"\n🎉 SUCCESS!")
        print(f"Trained models: {list(models.keys())}")
        print(f"Models ready for production use!")
    else:
        print(f"\n❌ Training failed")

if __name__ == "__main__":
    main()