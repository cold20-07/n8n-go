#!/usr/bin/env python3
"""
N8N Workflow Training System
Uses the analyzed workflow data to train various models for workflow generation and analysis
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import pickle

class N8NWorkflowTrainer:
    def __init__(self, training_data_dir: str = "training_data"):
        self.data_dir = Path(training_data_dir)
        self.models = {}
        self.vectorizers = {}
        self.load_training_data()
    
    def load_training_data(self):
        """Load all training data files"""
        print("Loading training data...")
        
        # Load CSV data
        self.workflow_features = pd.read_csv(self.data_dir / "workflow_features.csv")
        
        # Load JSON data
        with open(self.data_dir / "workflow_patterns.json", 'r') as f:
            self.workflow_patterns = json.load(f)
        
        with open(self.data_dir / "ai_integration_patterns.json", 'r') as f:
            self.ai_patterns = json.load(f)
        
        with open(self.data_dir / "node_sequences.json", 'r') as f:
            self.node_sequences = json.load(f)
        
        with open(self.data_dir / "service_combinations.json", 'r') as f:
            self.service_combinations = json.load(f)
        
        with open(self.data_dir / "workflow_templates.json", 'r') as f:
            self.workflow_templates = json.load(f)
        
        with open(self.data_dir / "statistics.json", 'r') as f:
            self.statistics = json.load(f)
        
        print(f"✓ Loaded training data for {len(self.workflow_features)} workflows")
    
    def train_workflow_classifier(self):
        """Train a classifier to categorize workflows"""
        print("\n🎯 Training Workflow Classifier...")
        
        # Prepare features
        features = []
        labels = []
        
        for _, row in self.workflow_features.iterrows():
            # Create feature vector from workflow characteristics
            feature_vector = [
                row['node_count'],
                row['has_ai_nodes'],
                row['has_openai'],
                row['has_langchain'],
                row['has_google_services'],
                row['has_slack'],
                row['has_webhook'],
                row['has_schedule'],
                row['connections_count'],
                row['sticky_notes_count'],
                row['error_handling_nodes']
            ]
            
            # Add node type diversity
            node_types = eval(row['node_types']) if isinstance(row['node_types'], str) else row['node_types']
            feature_vector.append(len(set(node_types)))
            
            features.append(feature_vector)
        
        # Get categories from workflow patterns
        categories = [pattern['category'] for pattern in self.workflow_patterns]
        
        # Train classifier
        X = np.array(features)
        y = np.array(categories)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        classifier.fit(X_train, y_train)
        
        # Evaluate
        y_pred = classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"✓ Workflow Classifier Accuracy: {accuracy:.2f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        self.models['workflow_classifier'] = classifier
        return classifier
    
    def train_node_sequence_predictor(self):
        """Train a model to predict next nodes in a sequence"""
        print("\n🔗 Training Node Sequence Predictor...")
        
        # Prepare sequence data
        sequences = []
        next_nodes = []
        
        for sequence in self.node_sequences:
            if len(sequence) > 1:
                for i in range(len(sequence) - 1):
                    # Use previous 3 nodes as context (or less if not available)
                    context_start = max(0, i - 2)
                    context = sequence[context_start:i+1]
                    next_node = sequence[i+1]
                    
                    sequences.append(' '.join(context))
                    next_nodes.append(next_node)
        
        # Vectorize sequences
        vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
        X = vectorizer.fit_transform(sequences)
        
        # Train classifier
        classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        classifier.fit(X, next_nodes)
        
        self.models['sequence_predictor'] = classifier
        self.vectorizers['sequence'] = vectorizer
        
        print(f"✓ Trained on {len(sequences)} node sequences")
        return classifier
    
    def train_ai_pattern_analyzer(self):
        """Train a model to analyze AI integration patterns"""
        print("\n🤖 Training AI Pattern Analyzer...")
        
        # Prepare AI pattern data
        ai_features = []
        ai_labels = []
        
        for pattern in self.ai_patterns:
            if pattern:  # Skip None patterns
                # Create feature vector
                feature_vector = [
                    len(pattern.get('ai_nodes', [])),
                    len(pattern.get('ai_parameters', [])),
                    'openai' in str(pattern.get('ai_nodes', [])).lower(),
                    'langchain' in str(pattern.get('ai_nodes', [])).lower(),
                    'gpt' in str(pattern.get('ai_nodes', [])).lower(),
                ]
                
                ai_features.append(feature_vector)
                
                # Determine AI complexity level
                node_count = len(pattern.get('ai_nodes', []))
                if node_count <= 2:
                    ai_labels.append('Simple AI')
                elif node_count <= 5:
                    ai_labels.append('Moderate AI')
                else:
                    ai_labels.append('Complex AI')
        
        if ai_features:
            X = np.array(ai_features)
            y = np.array(ai_labels)
            
            classifier = RandomForestClassifier(n_estimators=50, random_state=42)
            classifier.fit(X, y)
            
            self.models['ai_pattern_analyzer'] = classifier
            print(f"✓ Trained AI pattern analyzer on {len(ai_features)} patterns")
        
        return classifier if ai_features else None
    
    def cluster_workflows(self):
        """Cluster workflows based on their characteristics"""
        print("\n📊 Clustering Workflows...")
        
        # Prepare features for clustering
        features = []
        workflow_names = []
        
        for _, row in self.workflow_features.iterrows():
            feature_vector = [
                row['node_count'],
                row['workflow_complexity'],
                row['has_ai_nodes'],
                row['has_openai'],
                row['has_langchain'],
                row['has_google_services'],
                row['has_slack'],
                row['connections_count']
            ]
            features.append(feature_vector)
            workflow_names.append(row['workflow_name'])
        
        # Perform clustering
        X = np.array(features)
        kmeans = KMeans(n_clusters=5, random_state=42)
        clusters = kmeans.fit_predict(X)
        
        # Analyze clusters
        cluster_analysis = {}
        for i in range(5):
            cluster_workflows = [workflow_names[j] for j in range(len(workflow_names)) if clusters[j] == i]
            cluster_analysis[f'Cluster_{i}'] = {
                'count': len(cluster_workflows),
                'workflows': cluster_workflows[:5],  # Show first 5 examples
                'characteristics': self.analyze_cluster_characteristics(X[clusters == i])
            }
        
        self.models['workflow_clusters'] = kmeans
        self.cluster_analysis = cluster_analysis
        
        print(f"✓ Created {len(cluster_analysis)} workflow clusters")
        for cluster_id, info in cluster_analysis.items():
            print(f"  {cluster_id}: {info['count']} workflows")
        
        return kmeans, cluster_analysis
    
    def analyze_cluster_characteristics(self, cluster_data):
        """Analyze the characteristics of a workflow cluster"""
        if len(cluster_data) == 0:
            return {}
        
        means = np.mean(cluster_data, axis=0)
        return {
            'avg_node_count': round(means[0], 1),
            'avg_complexity': round(means[1], 1),
            'ai_usage_rate': round(means[2] * 100, 1),
            'openai_usage_rate': round(means[3] * 100, 1),
            'langchain_usage_rate': round(means[4] * 100, 1)
        }
    
    def generate_workflow_recommendations(self, requirements: Dict) -> List[Dict]:
        """Generate workflow recommendations based on requirements"""
        print(f"\n💡 Generating recommendations for: {requirements}")
        
        recommendations = []
        
        # Find similar workflows based on requirements
        for template in self.workflow_templates:
            score = self.calculate_similarity_score(template, requirements)
            if score > 0.3:  # Threshold for relevance
                recommendations.append({
                    'workflow': template,
                    'similarity_score': score,
                    'reason': self.explain_recommendation(template, requirements)
                })
        
        # Sort by similarity score
        recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return recommendations[:5]  # Return top 5 recommendations
    
    def calculate_similarity_score(self, template: Dict, requirements: Dict) -> float:
        """Calculate similarity score between template and requirements"""
        score = 0.0
        
        # Check for AI requirements
        if requirements.get('needs_ai', False):
            ai_nodes = [node for node in template.get('nodes', []) 
                       if any(ai_term in node.get('type', '').lower() 
                             for ai_term in ['openai', 'langchain', 'ai', 'gpt'])]
            if ai_nodes:
                score += 0.4
        
        # Check for service requirements
        required_services = requirements.get('services', [])
        template_services = [node.get('type', '') for node in template.get('nodes', [])]
        
        for service in required_services:
            if any(service.lower() in node_type.lower() for node_type in template_services):
                score += 0.2
        
        # Check complexity requirements
        node_count = len(template.get('nodes', []))
        required_complexity = requirements.get('complexity', 'medium')
        
        if required_complexity == 'simple' and node_count <= 10:
            score += 0.2
        elif required_complexity == 'medium' and 10 < node_count <= 25:
            score += 0.2
        elif required_complexity == 'complex' and node_count > 25:
            score += 0.2
        
        return min(score, 1.0)
    
    def explain_recommendation(self, template: Dict, requirements: Dict) -> str:
        """Explain why a workflow was recommended"""
        reasons = []
        
        # AI usage
        ai_nodes = [node for node in template.get('nodes', []) 
                   if any(ai_term in node.get('type', '').lower() 
                         for ai_term in ['openai', 'langchain', 'ai', 'gpt'])]
        if ai_nodes and requirements.get('needs_ai', False):
            reasons.append(f"Uses AI ({len(ai_nodes)} AI nodes)")
        
        # Services
        required_services = requirements.get('services', [])
        template_services = [node.get('type', '') for node in template.get('nodes', [])]
        matching_services = []
        
        for service in required_services:
            if any(service.lower() in node_type.lower() for node_type in template_services):
                matching_services.append(service)
        
        if matching_services:
            reasons.append(f"Integrates with {', '.join(matching_services)}")
        
        return '; '.join(reasons) if reasons else "General workflow pattern match"
    
    def save_models(self, output_dir: str = "trained_models"):
        """Save all trained models"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Save models
        for model_name, model in self.models.items():
            with open(output_path / f"{model_name}.pkl", 'wb') as f:
                pickle.dump(model, f)
        
        # Save vectorizers
        for vec_name, vectorizer in self.vectorizers.items():
            with open(output_path / f"{vec_name}_vectorizer.pkl", 'wb') as f:
                pickle.dump(vectorizer, f)
        
        # Save cluster analysis
        if hasattr(self, 'cluster_analysis'):
            with open(output_path / "cluster_analysis.json", 'w') as f:
                json.dump(self.cluster_analysis, f, indent=2)
        
        print(f"✓ Models saved to {output_path}")
        return output_path
    
    def train_all_models(self):
        """Train all available models"""
        print("🚀 Starting comprehensive model training...")
        
        # Train individual models
        self.train_workflow_classifier()
        self.train_node_sequence_predictor()
        self.train_ai_pattern_analyzer()
        self.cluster_workflows()
        
        # Save all models
        self.save_models()
        
        print("\n✅ All models trained successfully!")
        return self.models

def main():
    # Initialize trainer
    trainer = N8NWorkflowTrainer()
    
    # Train all models
    models = trainer.train_all_models()
    
    # Demo: Generate recommendations
    print("\n🎯 DEMO: Workflow Recommendations")
    print("="*50)
    
    # Example requirements
    requirements = {
        'needs_ai': True,
        'services': ['slack', 'openai'],
        'complexity': 'medium'
    }
    
    recommendations = trainer.generate_workflow_recommendations(requirements)
    
    print(f"\nTop recommendations for AI + Slack integration:")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['workflow']['name']}")
        print(f"   Score: {rec['similarity_score']:.2f}")
        print(f"   Reason: {rec['reason']}")
        print()
    
    # Show cluster analysis
    if hasattr(trainer, 'cluster_analysis'):
        print("\n📊 WORKFLOW CLUSTERS")
        print("="*50)
        for cluster_id, info in trainer.cluster_analysis.items():
            print(f"\n{cluster_id} ({info['count']} workflows):")
            print(f"  Avg Nodes: {info['characteristics']['avg_node_count']}")
            print(f"  AI Usage: {info['characteristics']['ai_usage_rate']}%")
            print(f"  Examples: {', '.join(info['workflows'][:3])}")

if __name__ == "__main__":
    main()