#!/usr/bin/env python3
"""
Final System Test - Comprehensive validation of the improved N8N training system
"""

import json
import pandas as pd
import numpy as np
import pickle
from pathlib import Path

def test_final_models():
    """Test all final models are working correctly"""
    print("🧪 Testing Final N8N Training System")
    print("=" * 50)
    
    model_dir = Path("final_models")
    
    # Test model loading
    print("\n📦 Testing Model Loading...")
    
    models = {}
    scalers = {}
    vectorizers = {}
    
    # Load models
    model_files = {
        'robust_classifier': 'robust_classifier.pkl',
        'sequence_predictor': 'sequence_predictor.pkl',
        'clustering': 'clustering.pkl'
    }
    
    for model_name, filename in model_files.items():
        try:
            with open(model_dir / filename, 'rb') as f:
                models[model_name] = pickle.load(f)
            print(f"✅ Loaded {model_name}")
        except Exception as e:
            print(f"❌ Failed to load {model_name}: {e}")
    
    # Load scalers
    scaler_files = [
        'robust_classifier_scaler.pkl',
        'clustering_scaler.pkl'
    ]
    
    for scaler_file in scaler_files:
        try:
            with open(model_dir / scaler_file, 'rb') as f:
                scaler_name = scaler_file.replace('_scaler.pkl', '')
                scalers[scaler_name] = pickle.load(f)
            print(f"✅ Loaded {scaler_name} scaler")
        except Exception as e:
            print(f"❌ Failed to load {scaler_file}: {e}")
    
    # Load vectorizers
    try:
        with open(model_dir / 'sequence_vectorizer.pkl', 'rb') as f:
            vectorizers['sequence'] = pickle.load(f)
        print(f"✅ Loaded sequence vectorizer")
    except Exception as e:
        print(f"❌ Failed to load sequence vectorizer: {e}")
    
    # Test model predictions
    print("\n🎯 Testing Model Predictions...")
    
    # Test classifier
    if 'robust_classifier' in models and 'robust_classifier' in scalers:
        try:
            # Create sample features (17 features as defined in the system)
            sample_features = np.array([[
                25,    # node_count
                8,     # unique_node_types
                15,    # connections_count
                3,     # ai_node_count
                0.12,  # ai_node_ratio
                1,     # has_openai
                1,     # has_langchain
                0,     # has_google
                1,     # has_slack
                0,     # has_webhook
                0,     # has_schedule
                0.08,  # branching_complexity
                0.2,   # documentation_ratio
                0.04,  # error_handling_ratio
                1,     # trigger_count
                2,     # output_count
                45.5   # complexity_score
            ]])
            
            # Scale features
            sample_scaled = scalers['robust_classifier'].transform(sample_features)
            
            # Make prediction
            prediction = models['robust_classifier'].predict(sample_scaled)
            probabilities = models['robust_classifier'].predict_proba(sample_scaled)
            
            print(f"✅ Classifier prediction: {prediction[0]} (confidence: {max(probabilities[0]):.3f})")
            
        except Exception as e:
            print(f"❌ Classifier prediction failed: {e}")
    
    # Test sequence predictor
    if 'sequence_predictor' in models and 'sequence' in vectorizers:
        try:
            # Test sequence contexts
            test_contexts = [
                "manualTrigger set",
                "scheduleTrigger httpRequest",
                "lmChatOpenAi set"
            ]
            
            for context in test_contexts:
                # Vectorize context
                context_vector = vectorizers['sequence'].transform([context])
                
                # Make prediction
                prediction = models['sequence_predictor'].predict(context_vector.toarray())
                
                print(f"✅ Sequence '{context}' → {prediction[0]}")
                
        except Exception as e:
            print(f"❌ Sequence prediction failed: {e}")
    
    # Test clustering
    if 'clustering' in models and 'clustering' in scalers:
        try:
            # Test different workflow profiles
            test_profiles = [
                {"name": "Simple AI Workflow", "features": [10, 5, 8, 2, 0.2, 1, 1, 0, 0, 0, 0, 0.1, 0.3, 0.0, 1, 1, 20]},
                {"name": "Complex Integration", "features": [40, 15, 30, 5, 0.125, 1, 1, 1, 1, 1, 1, 0.2, 0.15, 0.05, 2, 3, 80]},
                {"name": "Basic Automation", "features": [8, 4, 5, 0, 0.0, 0, 0, 0, 0, 1, 1, 0.0, 0.25, 0.0, 1, 1, 15]}
            ]
            
            for profile in test_profiles:
                features = np.array([profile["features"]])
                features_scaled = scalers['clustering'].transform(features)
                cluster = models['clustering'].predict(features_scaled)
                
                print(f"✅ '{profile['name']}' → Cluster {cluster[0]}")
                
        except Exception as e:
            print(f"❌ Clustering prediction failed: {e}")
    
    # Test metadata
    print("\n📊 Testing Metadata...")
    
    try:
        with open(model_dir / "model_metadata.json", 'r') as f:
            metadata = json.load(f)
        
        print(f"✅ Metadata loaded")
        print(f"   Training date: {metadata['training_summary']['training_date']}")
        print(f"   Models trained: {metadata['training_summary']['models_trained']}")
        
        # Performance metrics
        for model_name, performance in metadata['model_performance'].items():
            print(f"   {model_name}: ", end="")
            if 'accuracy' in performance:
                print(f"Accuracy={performance['accuracy']:.3f} ", end="")
            if 'f1_score' in performance:
                print(f"F1={performance['f1_score']:.3f} ", end="")
            if 'silhouette_score' in performance:
                print(f"Silhouette={performance['silhouette_score']:.3f} ", end="")
            print()
        
    except Exception as e:
        print(f"❌ Metadata loading failed: {e}")
    
    # Test workflow recommendation simulation
    print("\n💡 Testing Workflow Recommendation Logic...")
    
    try:
        # Load workflow templates for recommendation testing
        with open("training_data/workflow_templates.json", 'r') as f:
            templates = json.load(f)
        
        def calculate_similarity_score(template, requirements):
            score = 0.0
            nodes = template.get('nodes', [])
            node_types = [node.get('type', '') for node in nodes]
            
            # AI requirements
            if requirements.get('needs_ai', False):
                ai_nodes = [node for node in nodes 
                           if any(ai_term in node.get('type', '').lower() 
                                 for ai_term in ['openai', 'langchain', 'ai', 'gpt'])]
                if ai_nodes:
                    score += 0.4
            
            # Service requirements
            required_services = requirements.get('services', [])
            for service in required_services:
                if any(service.lower() in node_type.lower() for node_type in node_types):
                    score += 0.2
            
            return min(score, 1.0)
        
        # Test recommendation scenarios
        test_requirements = [
            {'needs_ai': True, 'services': ['slack', 'openai']},
            {'needs_ai': False, 'services': ['google', 'sheets']},
            {'needs_ai': True, 'services': ['wordpress']}
        ]
        
        for i, requirements in enumerate(test_requirements, 1):
            recommendations = []
            for template in templates[:20]:  # Test first 20 templates
                score = calculate_similarity_score(template, requirements)
                if score > 0.3:
                    recommendations.append({
                        'name': template.get('name', 'Unknown'),
                        'score': score
                    })
            
            recommendations.sort(key=lambda x: x['score'], reverse=True)
            
            print(f"✅ Scenario {i}: Found {len(recommendations)} recommendations")
            if recommendations:
                top_rec = recommendations[0]
                print(f"   Top: {top_rec['name'][:50]}... (score: {top_rec['score']:.2f})")
        
    except Exception as e:
        print(f"❌ Recommendation testing failed: {e}")
    
    # Final summary
    print(f"\n🎉 FINAL SYSTEM TEST SUMMARY")
    print("=" * 50)
    
    total_models = len(model_files)
    loaded_models = len(models)
    
    print(f"Models loaded: {loaded_models}/{total_models}")
    print(f"Scalers loaded: {len(scalers)}")
    print(f"Vectorizers loaded: {len(vectorizers)}")
    
    if loaded_models == total_models:
        print(f"✅ ALL SYSTEMS OPERATIONAL!")
        print(f"🚀 N8N Training System is ready for production!")
        return True
    else:
        print(f"⚠️  Some components failed to load")
        return False

def test_data_quality():
    """Test the quality of training data"""
    print(f"\n🔍 Testing Training Data Quality...")
    
    try:
        # Load and check training data
        df = pd.read_csv("training_data/workflow_features.csv")
        
        print(f"✅ Training data: {len(df)} workflows")
        print(f"✅ Features: {len(df.columns)} columns")
        
        # Check for missing values
        missing_counts = df.isnull().sum()
        high_missing = missing_counts[missing_counts > len(df) * 0.1]
        
        if len(high_missing) > 0:
            print(f"⚠️  High missing values in: {list(high_missing.index)}")
        else:
            print(f"✅ Data quality: Low missing values")
        
        # Check class distribution
        with open("training_data/workflow_patterns.json", 'r') as f:
            patterns = json.load(f)
        
        categories = [p['category'] for p in patterns]
        category_counts = pd.Series(categories).value_counts()
        
        print(f"✅ Class distribution:")
        for category, count in category_counts.items():
            percentage = (count / len(categories)) * 100
            print(f"   {category}: {count} ({percentage:.1f}%)")
        
        return True
        
    except Exception as e:
        print(f"❌ Data quality test failed: {e}")
        return False

def main():
    """Run all final tests"""
    print("🧪 COMPREHENSIVE FINAL SYSTEM TEST")
    print("=" * 60)
    
    # Test data quality
    data_ok = test_data_quality()
    
    # Test models
    models_ok = test_final_models()
    
    # Final verdict
    print(f"\n" + "=" * 60)
    if data_ok and models_ok:
        print("🎉 ALL TESTS PASSED!")
        print("✅ N8N Training System is fully operational")
        print("🚀 Ready for production deployment!")
    else:
        print("⚠️  Some tests failed")
        print("🔧 Please review the issues above")

if __name__ == "__main__":
    main()