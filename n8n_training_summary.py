#!/usr/bin/env python3
"""
N8N Workflow Training Summary
Provides comprehensive insights and training data from the 100 n8n workflows
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter, defaultdict

def load_and_analyze_training_data():
    """Load and provide comprehensive analysis of the training data"""
    
    print("🚀 N8N WORKFLOW TRAINING DATA ANALYSIS")
    print("="*60)
    
    # Load the data
    data_dir = Path("training_data")
    
    # Load workflow features
    df = pd.read_csv(data_dir / "workflow_features.csv")
    
    # Load statistics
    with open(data_dir / "statistics.json", 'r') as f:
        stats = json.load(f)
    
    # Load patterns
    with open(data_dir / "workflow_patterns.json", 'r') as f:
        patterns = json.load(f)
    
    # Load AI patterns
    with open(data_dir / "ai_integration_patterns.json", 'r') as f:
        ai_patterns = json.load(f)
    
    # Load node sequences
    with open(data_dir / "node_sequences.json", 'r') as f:
        sequences = json.load(f)
    
    print(f"\n📊 DATASET OVERVIEW")
    print(f"Total Workflows Analyzed: {stats['total_workflows']}")
    print(f"Total Nodes: {stats['node_statistics']['total_nodes']}")
    print(f"Average Nodes per Workflow: {stats['node_statistics']['avg_nodes_per_workflow']:.1f}")
    print(f"AI Adoption Rate: {stats['ai_usage']['ai_adoption_rate']:.1f}%")
    
    print(f"\n🤖 AI INTEGRATION INSIGHTS")
    print(f"Workflows with AI: {stats['ai_usage']['workflows_with_ai']}")
    print(f"OpenAI Usage: {stats['ai_usage']['openai_usage']}")
    print(f"LangChain Usage: {stats['ai_usage']['langchain_usage']}")
    
    # Analyze AI patterns
    ai_node_types = []
    for pattern in ai_patterns:
        if pattern:
            ai_node_types.extend(pattern.get('ai_nodes', []))
    
    ai_counter = Counter(ai_node_types)
    print(f"\nMost Common AI Node Types:")
    for node_type, count in ai_counter.most_common(5):
        print(f"  {node_type}: {count}")
    
    print(f"\n🔗 SERVICE INTEGRATIONS")
    for service, count in stats['service_usage'].items():
        print(f"{service.replace('_', ' ').title()}: {count}")
    
    print(f"\n📈 WORKFLOW CATEGORIES")
    for category, count in stats['workflow_categories'].items():
        print(f"{category}: {count}")
    
    print(f"\n🏗️ COMPLEXITY DISTRIBUTION")
    for complexity, count in stats['complexity_distribution'].items():
        print(f"{complexity.replace('_', ' ').title()}: {count}")
    
    print(f"\n🔧 MOST COMMON NODE TYPES")
    for node_type, count in list(stats['most_common_nodes'].items())[:10]:
        short_name = node_type.split('.')[-1] if '.' in node_type else node_type
        print(f"  {short_name}: {count}")
    
    # Analyze workflow patterns
    print(f"\n🎯 WORKFLOW PATTERN ANALYSIS")
    
    # Trigger patterns
    trigger_patterns = []
    for pattern in patterns:
        trigger_patterns.extend(pattern.get('trigger_pattern', []))
    
    trigger_counter = Counter(trigger_patterns)
    print(f"\nMost Common Triggers:")
    for trigger, count in trigger_counter.most_common(5):
        short_name = trigger.split('.')[-1] if '.' in trigger else trigger
        print(f"  {short_name}: {count}")
    
    # Output patterns
    output_patterns = []
    for pattern in patterns:
        output_patterns.extend(pattern.get('output_pattern', []))
    
    output_counter = Counter(output_patterns)
    print(f"\nMost Common Outputs:")
    for output, count in output_counter.most_common(5):
        short_name = output.split('.')[-1] if '.' in output else output
        print(f"  {short_name}: {count}")
    
    # Analyze node sequences for common patterns
    print(f"\n🔄 COMMON WORKFLOW SEQUENCES")
    
    # Find common 3-node sequences
    three_node_sequences = []
    for sequence in sequences:
        if len(sequence) >= 3:
            for i in range(len(sequence) - 2):
                three_seq = tuple(sequence[i:i+3])
                three_node_sequences.append(three_seq)
    
    seq_counter = Counter(three_node_sequences)
    print(f"\nMost Common 3-Node Sequences:")
    for seq, count in seq_counter.most_common(3):
        short_seq = [node.split('.')[-1] if '.' in node else node for node in seq]
        print(f"  {' → '.join(short_seq)}: {count} times")
    
    return {
        'dataframe': df,
        'statistics': stats,
        'patterns': patterns,
        'ai_patterns': ai_patterns,
        'sequences': sequences
    }

def generate_training_insights(data):
    """Generate insights for training ML models"""
    
    print(f"\n🎓 TRAINING INSIGHTS & RECOMMENDATIONS")
    print("="*60)
    
    df = data['dataframe']
    stats = data['statistics']
    
    print(f"\n📚 DATASET CHARACTERISTICS FOR ML TRAINING:")
    print(f"• Dataset Size: {len(df)} workflows (good for initial training)")
    print(f"• Feature Diversity: {len(df.columns)} features per workflow")
    print(f"• AI Usage Rate: {stats['ai_usage']['ai_adoption_rate']:.1f}% (high AI adoption)")
    print(f"• Category Balance: {len(stats['workflow_categories'])} categories")
    
    # Check class balance
    categories = [p['category'] for p in data['patterns']]
    category_counts = Counter(categories)
    
    print(f"\n⚖️ CLASS BALANCE ANALYSIS:")
    for category, count in category_counts.items():
        percentage = (count / len(categories)) * 100
        print(f"• {category}: {count} workflows ({percentage:.1f}%)")
    
    # Identify most predictive features
    print(f"\n🎯 KEY FEATURES FOR PREDICTION:")
    print(f"• Node Count: Range {df['node_count'].min()}-{df['node_count'].max()}")
    print(f"• AI Integration: {df['has_ai_nodes'].sum()}/{len(df)} workflows")
    print(f"• Service Diversity: Multiple integration patterns")
    print(f"• Complexity Levels: 3 distinct complexity tiers")
    
    print(f"\n🔮 RECOMMENDED TRAINING APPROACHES:")
    print(f"1. Workflow Classification:")
    print(f"   • Use node types, counts, and service integrations")
    print(f"   • Random Forest or Gradient Boosting recommended")
    print(f"   • Consider ensemble methods for better accuracy")
    
    print(f"2. Node Sequence Prediction:")
    print(f"   • Use n-gram analysis on node sequences")
    print(f"   • LSTM or Transformer models for sequence learning")
    print(f"   • Context window of 3-5 previous nodes")
    
    print(f"3. AI Pattern Recognition:")
    print(f"   • Focus on AI node combinations and parameters")
    print(f"   • Clustering for pattern discovery")
    print(f"   • Rule-based systems for specific AI workflows")
    
    print(f"4. Workflow Generation:")
    print(f"   • Template-based generation with learned patterns")
    print(f"   • Conditional generation based on requirements")
    print(f"   • Validation using trained classifiers")

def create_training_datasets():
    """Create specific datasets for different training tasks"""
    
    print(f"\n💾 CREATING SPECIALIZED TRAINING DATASETS")
    print("="*60)
    
    data_dir = Path("training_data")
    output_dir = Path("specialized_datasets")
    output_dir.mkdir(exist_ok=True)
    
    # Load data
    df = pd.read_csv(data_dir / "workflow_features.csv")
    
    with open(data_dir / "workflow_patterns.json", 'r') as f:
        patterns = json.load(f)
    
    with open(data_dir / "node_sequences.json", 'r') as f:
        sequences = json.load(f)
    
    # 1. Classification Dataset
    classification_data = []
    for i, (_, row) in enumerate(df.iterrows()):
        if i < len(patterns):
            classification_data.append({
                'workflow_name': row['workflow_name'],
                'node_count': row['node_count'],
                'has_ai': row['has_ai_nodes'],
                'has_openai': row['has_openai'],
                'has_langchain': row['has_langchain'],
                'has_google': row['has_google_services'],
                'has_slack': row['has_slack'],
                'complexity': row['workflow_complexity'],
                'category': patterns[i]['category']
            })
    
    classification_df = pd.DataFrame(classification_data)
    classification_df.to_csv(output_dir / "classification_dataset.csv", index=False)
    print(f"✓ Created classification dataset: {len(classification_df)} samples")
    
    # 2. Sequence Dataset
    sequence_data = []
    for sequence in sequences:
        if len(sequence) > 2:
            for i in range(len(sequence) - 1):
                sequence_data.append({
                    'context': ' '.join(sequence[max(0, i-2):i+1]),
                    'next_node': sequence[i+1],
                    'sequence_length': len(sequence),
                    'position': i+1
                })
    
    sequence_df = pd.DataFrame(sequence_data)
    sequence_df.to_csv(output_dir / "sequence_dataset.csv", index=False)
    print(f"✓ Created sequence dataset: {len(sequence_df)} samples")
    
    # 3. AI Pattern Dataset
    ai_data = []
    for i, (_, row) in enumerate(df.iterrows()):
        if row['has_ai_nodes']:
            ai_data.append({
                'workflow_name': row['workflow_name'],
                'ai_node_count': len(eval(row['ai_node_types'])) if row['ai_node_types'] != '[]' else 0,
                'has_openai': row['has_openai'],
                'has_langchain': row['has_langchain'],
                'node_count': row['node_count'],
                'complexity': 'Simple' if row['workflow_complexity'] < 20 else 'Complex'
            })
    
    ai_df = pd.DataFrame(ai_data)
    ai_df.to_csv(output_dir / "ai_pattern_dataset.csv", index=False)
    print(f"✓ Created AI pattern dataset: {len(ai_df)} samples")
    
    print(f"\n📁 Specialized datasets saved to: {output_dir}")
    return output_dir

def main():
    """Main function to run the complete analysis"""
    
    # Load and analyze data
    data = load_and_analyze_training_data()
    
    # Generate training insights
    generate_training_insights(data)
    
    # Create specialized datasets
    create_training_datasets()
    
    print(f"\n✅ TRAINING DATA ANALYSIS COMPLETE!")
    print(f"\n📋 SUMMARY:")
    print(f"• Analyzed 97 n8n workflows successfully")
    print(f"• Generated comprehensive feature datasets")
    print(f"• Created specialized training datasets")
    print(f"• Identified key patterns and insights")
    print(f"• Ready for ML model training!")
    
    print(f"\n🎯 NEXT STEPS:")
    print(f"1. Use classification_dataset.csv for workflow categorization")
    print(f"2. Use sequence_dataset.csv for node prediction models")
    print(f"3. Use ai_pattern_dataset.csv for AI workflow analysis")
    print(f"4. Experiment with different ML algorithms")
    print(f"5. Build workflow generation systems")

if __name__ == "__main__":
    main()