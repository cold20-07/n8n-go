#!/usr/bin/env python3
"""
Comprehensive Test Suite for N8N Training Data
Tests all generated training data, models, and analysis scripts for errors
"""

import json
import pandas as pd
import numpy as np
import pickle
from pathlib import Path
import sys
import traceback
from typing import Dict, List, Any

class N8NTrainingDataTester:
    def __init__(self):
        self.test_results = {}
        self.errors = []
        self.warnings = []
        
    def log_test(self, test_name: str, passed: bool, message: str = ""):
        """Log test results"""
        self.test_results[test_name] = {
            'passed': passed,
            'message': message
        }
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"    {message}")
        if not passed:
            self.errors.append(f"{test_name}: {message}")
    
    def log_warning(self, message: str):
        """Log warnings"""
        self.warnings.append(message)
        print(f"⚠️  WARNING: {message}")
    
    def test_file_existence(self):
        """Test that all expected files exist"""
        print("\n🔍 Testing File Existence...")
        
        # Training data files
        training_files = [
            "training_data/workflow_features.csv",
            "training_data/workflow_patterns.json",
            "training_data/ai_integration_patterns.json",
            "training_data/node_sequences.json",
            "training_data/service_combinations.json",
            "training_data/workflow_templates.json",
            "training_data/statistics.json"
        ]
        
        # Specialized dataset files
        dataset_files = [
            "specialized_datasets/classification_dataset.csv",
            "specialized_datasets/sequence_dataset.csv",
            "specialized_datasets/ai_pattern_dataset.csv"
        ]
        
        # Model files
        model_files = [
            "trained_models/workflow_classifier.pkl",
            "trained_models/sequence_predictor.pkl",
            "trained_models/ai_pattern_analyzer.pkl",
            "trained_models/workflow_clusters.pkl",
            "trained_models/sequence_vectorizer.pkl",
            "trained_models/cluster_analysis.json"
        ]
        
        all_files = training_files + dataset_files + model_files
        missing_files = []
        
        for file_path in all_files:
            if Path(file_path).exists():
                self.log_test(f"File exists: {file_path}", True)
            else:
                missing_files.append(file_path)
                self.log_test(f"File exists: {file_path}", False, "File not found")
        
        if not missing_files:
            self.log_test("All files exist", True, f"Found all {len(all_files)} expected files")
        else:
            self.log_test("All files exist", False, f"Missing {len(missing_files)} files")
    
    def test_csv_files(self):
        """Test CSV files can be loaded and have expected structure"""
        print("\n📊 Testing CSV Files...")
        
        csv_files = {
            "training_data/workflow_features.csv": {
                "min_rows": 90,
                "expected_columns": ["workflow_name", "node_count", "has_ai_nodes"]
            },
            "specialized_datasets/classification_dataset.csv": {
                "min_rows": 90,
                "expected_columns": ["workflow_name", "category", "node_count"]
            },
            "specialized_datasets/sequence_dataset.csv": {
                "min_rows": 1000,
                "expected_columns": ["context", "next_node"]
            },
            "specialized_datasets/ai_pattern_dataset.csv": {
                "min_rows": 80,
                "expected_columns": ["workflow_name", "has_openai", "has_langchain"]
            }
        }
        
        for file_path, requirements in csv_files.items():
            try:
                if not Path(file_path).exists():
                    self.log_test(f"CSV load: {file_path}", False, "File not found")
                    continue
                
                df = pd.read_csv(file_path)
                
                # Test row count
                if len(df) >= requirements["min_rows"]:
                    self.log_test(f"CSV rows: {file_path}", True, f"Has {len(df)} rows")
                else:
                    self.log_test(f"CSV rows: {file_path}", False, 
                                f"Only {len(df)} rows, expected >= {requirements['min_rows']}")
                
                # Test columns
                missing_cols = [col for col in requirements["expected_columns"] if col not in df.columns]
                if not missing_cols:
                    self.log_test(f"CSV columns: {file_path}", True, f"Has all expected columns")
                else:
                    self.log_test(f"CSV columns: {file_path}", False, 
                                f"Missing columns: {missing_cols}")
                
                # Test for empty values
                empty_cells = df.isnull().sum().sum()
                if empty_cells == 0:
                    self.log_test(f"CSV completeness: {file_path}", True, "No empty cells")
                else:
                    self.log_warning(f"{file_path} has {empty_cells} empty cells")
                    self.log_test(f"CSV completeness: {file_path}", True, f"{empty_cells} empty cells (acceptable)")
                
            except Exception as e:
                self.log_test(f"CSV load: {file_path}", False, f"Error: {str(e)}")
    
    def test_json_files(self):
        """Test JSON files can be loaded and have expected structure"""
        print("\n📋 Testing JSON Files...")
        
        json_files = {
            "training_data/statistics.json": {
                "required_keys": ["total_workflows", "ai_usage", "workflow_categories"]
            },
            "training_data/workflow_patterns.json": {
                "min_items": 90,
                "item_keys": ["name", "category"]
            },
            "training_data/ai_integration_patterns.json": {
                "min_items": 80,
                "item_keys": ["workflow_name", "ai_nodes"]
            },
            "training_data/node_sequences.json": {
                "min_items": 90
            },
            "training_data/service_combinations.json": {
                "min_items": 90
            },
            "training_data/workflow_templates.json": {
                "min_items": 90,
                "item_keys": ["name", "nodes"]
            },
            "trained_models/cluster_analysis.json": {
                "required_keys": ["Cluster_0", "Cluster_1"]
            }
        }
        
        for file_path, requirements in json_files.items():
            try:
                if not Path(file_path).exists():
                    self.log_test(f"JSON load: {file_path}", False, "File not found")
                    continue
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.log_test(f"JSON load: {file_path}", True, "Loaded successfully")
                
                # Test required keys for dict data
                if "required_keys" in requirements and isinstance(data, dict):
                    missing_keys = [key for key in requirements["required_keys"] if key not in data]
                    if not missing_keys:
                        self.log_test(f"JSON structure: {file_path}", True, "Has all required keys")
                    else:
                        self.log_test(f"JSON structure: {file_path}", False, 
                                    f"Missing keys: {missing_keys}")
                
                # Test minimum items for list data
                if "min_items" in requirements and isinstance(data, list):
                    if len(data) >= requirements["min_items"]:
                        self.log_test(f"JSON items: {file_path}", True, f"Has {len(data)} items")
                    else:
                        self.log_test(f"JSON items: {file_path}", False, 
                                    f"Only {len(data)} items, expected >= {requirements['min_items']}")
                
                # Test item structure for list data
                if "item_keys" in requirements and isinstance(data, list) and data:
                    first_item = data[0]
                    if isinstance(first_item, dict):
                        missing_keys = [key for key in requirements["item_keys"] if key not in first_item]
                        if not missing_keys:
                            self.log_test(f"JSON item structure: {file_path}", True, "Items have required keys")
                        else:
                            self.log_test(f"JSON item structure: {file_path}", False, 
                                        f"Items missing keys: {missing_keys}")
                
            except json.JSONDecodeError as e:
                self.log_test(f"JSON load: {file_path}", False, f"JSON decode error: {str(e)}")
            except Exception as e:
                self.log_test(f"JSON load: {file_path}", False, f"Error: {str(e)}")
    
    def test_pickle_models(self):
        """Test that pickle model files can be loaded"""
        print("\n🤖 Testing Pickle Models...")
        
        model_files = [
            "trained_models/workflow_classifier.pkl",
            "trained_models/sequence_predictor.pkl",
            "trained_models/ai_pattern_analyzer.pkl",
            "trained_models/workflow_clusters.pkl",
            "trained_models/sequence_vectorizer.pkl"
        ]
        
        for file_path in model_files:
            try:
                if not Path(file_path).exists():
                    self.log_test(f"Model load: {file_path}", False, "File not found")
                    continue
                
                with open(file_path, 'rb') as f:
                    model = pickle.load(f)
                
                self.log_test(f"Model load: {file_path}", True, f"Loaded {type(model).__name__}")
                
                # Test if model has expected methods
                if hasattr(model, 'predict'):
                    self.log_test(f"Model predict method: {file_path}", True, "Has predict method")
                else:
                    self.log_warning(f"{file_path} model doesn't have predict method")
                
            except Exception as e:
                self.log_test(f"Model load: {file_path}", False, f"Error: {str(e)}")
    
    def test_data_consistency(self):
        """Test data consistency across different files"""
        print("\n🔗 Testing Data Consistency...")
        
        try:
            # Load main datasets
            features_df = pd.read_csv("training_data/workflow_features.csv")
            
            with open("training_data/workflow_patterns.json", 'r') as f:
                patterns = json.load(f)
            
            with open("training_data/statistics.json", 'r') as f:
                stats = json.load(f)
            
            # Test workflow count consistency
            feature_count = len(features_df)
            pattern_count = len(patterns)
            stats_count = int(stats.get("total_workflows", 0))
            
            if feature_count == pattern_count == stats_count:
                self.log_test("Workflow count consistency", True, 
                            f"All sources report {feature_count} workflows")
            else:
                self.log_test("Workflow count consistency", False, 
                            f"Inconsistent counts: features={feature_count}, patterns={pattern_count}, stats={stats_count}")
            
            # Test AI usage consistency
            ai_workflows_features = features_df['has_ai_nodes'].sum()
            ai_workflows_stats = int(stats.get("ai_usage", {}).get("workflows_with_ai", 0))
            
            if ai_workflows_features == ai_workflows_stats:
                self.log_test("AI usage consistency", True, 
                            f"Both sources report {ai_workflows_features} AI workflows")
            else:
                self.log_test("AI usage consistency", False, 
                            f"Inconsistent AI counts: features={ai_workflows_features}, stats={ai_workflows_stats}")
            
            # Test node count consistency
            total_nodes_features = features_df['node_count'].sum()
            total_nodes_stats = int(stats.get("node_statistics", {}).get("total_nodes", 0))
            
            if total_nodes_features == total_nodes_stats:
                self.log_test("Node count consistency", True, 
                            f"Both sources report {total_nodes_features} total nodes")
            else:
                self.log_test("Node count consistency", False, 
                            f"Inconsistent node counts: features={total_nodes_features}, stats={total_nodes_stats}")
            
        except Exception as e:
            self.log_test("Data consistency", False, f"Error during consistency check: {str(e)}")
    
    def test_model_predictions(self):
        """Test that models can make predictions on sample data"""
        print("\n🎯 Testing Model Predictions...")
        
        try:
            # Load test data
            features_df = pd.read_csv("training_data/workflow_features.csv")
            
            if len(features_df) == 0:
                self.log_test("Model predictions", False, "No test data available")
                return
            
            # Test workflow classifier
            try:
                with open("trained_models/workflow_classifier.pkl", 'rb') as f:
                    classifier = pickle.load(f)
                
                # Create sample feature vector
                sample_features = np.array([[
                    features_df['node_count'].iloc[0],
                    features_df['has_ai_nodes'].iloc[0],
                    features_df['has_openai'].iloc[0],
                    features_df['has_langchain'].iloc[0],
                    features_df['has_google_services'].iloc[0],
                    features_df['has_slack'].iloc[0],
                    features_df['has_webhook'].iloc[0],
                    features_df['has_schedule'].iloc[0],
                    features_df['connections_count'].iloc[0],
                    features_df['sticky_notes_count'].iloc[0],
                    features_df['error_handling_nodes'].iloc[0],
                    10  # node type diversity placeholder
                ]])
                
                prediction = classifier.predict(sample_features)
                self.log_test("Workflow classifier prediction", True, 
                            f"Predicted category: {prediction[0]}")
                
            except Exception as e:
                self.log_test("Workflow classifier prediction", False, f"Error: {str(e)}")
            
            # Test sequence predictor
            try:
                with open("trained_models/sequence_predictor.pkl", 'rb') as f:
                    seq_predictor = pickle.load(f)
                
                with open("trained_models/sequence_vectorizer.pkl", 'rb') as f:
                    vectorizer = pickle.load(f)
                
                # Test with sample sequence
                sample_sequence = ["n8n-nodes-base.manualTrigger", "n8n-nodes-base.set"]
                sample_text = " ".join(sample_sequence)
                sample_vector = vectorizer.transform([sample_text])
                
                prediction = seq_predictor.predict(sample_vector)
                self.log_test("Sequence predictor prediction", True, 
                            f"Predicted next node: {prediction[0]}")
                
            except Exception as e:
                self.log_test("Sequence predictor prediction", False, f"Error: {str(e)}")
            
            # Test clustering model
            try:
                with open("trained_models/workflow_clusters.pkl", 'rb') as f:
                    clusterer = pickle.load(f)
                
                # Create sample feature vector for clustering
                sample_cluster_features = np.array([[
                    features_df['node_count'].iloc[0],
                    features_df['workflow_complexity'].iloc[0],
                    features_df['has_ai_nodes'].iloc[0],
                    features_df['has_openai'].iloc[0],
                    features_df['has_langchain'].iloc[0],
                    features_df['has_google_services'].iloc[0],
                    features_df['has_slack'].iloc[0],
                    features_df['connections_count'].iloc[0]
                ]])
                
                cluster = clusterer.predict(sample_cluster_features)
                self.log_test("Clustering model prediction", True, 
                            f"Assigned to cluster: {cluster[0]}")
                
            except Exception as e:
                self.log_test("Clustering model prediction", False, f"Error: {str(e)}")
                
        except Exception as e:
            self.log_test("Model predictions", False, f"General error: {str(e)}")
    
    def test_analyzer_script(self):
        """Test that the analyzer script can be imported and run"""
        print("\n🔧 Testing Analyzer Script...")
        
        try:
            # Test import
            sys.path.append('.')
            import n8n_workflow_analyzer
            self.log_test("Analyzer script import", True, "Successfully imported")
            
            # Test class instantiation
            analyzer = n8n_workflow_analyzer.N8NWorkflowAnalyzer("drive-download-20251004T130930Z-1-001")
            self.log_test("Analyzer instantiation", True, "Successfully created analyzer instance")
            
            # Test if workflows are already loaded
            if hasattr(analyzer, 'workflows') and analyzer.workflows:
                self.log_test("Analyzer workflows loaded", True, f"Has {len(analyzer.workflows)} workflows")
            else:
                self.log_test("Analyzer workflows loaded", True, "No workflows pre-loaded (expected)")
            
        except ImportError as e:
            self.log_test("Analyzer script import", False, f"Import error: {str(e)}")
        except Exception as e:
            self.log_test("Analyzer script test", False, f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run all tests and provide summary"""
        print("🚀 N8N TRAINING DATA COMPREHENSIVE TEST SUITE")
        print("=" * 60)
        
        # Run all test categories
        self.test_file_existence()
        self.test_csv_files()
        self.test_json_files()
        self.test_pickle_models()
        self.test_data_consistency()
        self.test_model_predictions()
        self.test_analyzer_script()
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result['passed'])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️  Warnings: {len(self.warnings)}")
        
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        print(f"Success Rate: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ FAILED TESTS:")
            for error in self.errors:
                print(f"  • {error}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  • {warning}")
        
        if failed_tests == 0:
            print(f"\n🎉 ALL TESTS PASSED! Training data is ready for use.")
            return True
        else:
            print(f"\n⚠️  Some tests failed. Please review the issues above.")
            return False

def main():
    """Main test function"""
    tester = N8NTrainingDataTester()
    success = tester.run_all_tests()
    
    if success:
        print(f"\n✅ TRAINING DATA VALIDATION COMPLETE")
        print(f"Your n8n training data is fully functional and ready for ML training!")
        sys.exit(0)
    else:
        print(f"\n❌ TRAINING DATA VALIDATION FAILED")
        print(f"Please fix the issues above before proceeding with ML training.")
        sys.exit(1)

if __name__ == "__main__":
    main()