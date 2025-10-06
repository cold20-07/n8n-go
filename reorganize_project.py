#!/usr/bin/env python3
"""
Script to reorganize the N8N workflow generator project structure
"""
import os
import shutil
from pathlib import Path

def create_new_structure():
    """Create organized directory structure"""
    
    # Define new structure
    directories = [
        'src/core/generators',
        'src/core/validators', 
        'src/core/models',
        'src/api/routes',
        'src/utils',
        'tests/unit',
        'tests/integration',
        'config',
        'scripts',
        'docs'
    ]
    
    # Create directories
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created: {directory}")

def move_files():
    """Move files to appropriate locations"""
    
    file_mappings = {
        # Core generators
        'src/core/generators/': [
            'n8n_training_system.py',
            'enhanced_workflow_generator.py', 
            'feature_aware_workflow_generator.py',
            'trained_workflow_generator.py',
            'improved_n8n_training_system.py',
            'optimized_n8n_training_system.py',
            'final_n8n_training_system.py'
        ],
        
        # Validators
        'src/core/validators/': [
            'connection_validator.py',
            'workflow_accuracy_validator.py',
            'enhanced_input_validation.py',
            'simple_connection_fixer.py'
        ],
        
        # Utilities
        'src/utils/': [
            'prompt_helper.py',
            'prompt_assistance_system.py',
            'interactive_prompt_assistant.py'
        ],
        
        # Scripts
        'scripts/': [
            'cleanup_debug_files.py',
            'cleanup_for_distribution.py',
            'quick_improvements.py',
            'regenerate_models.py',
            'setup.py'
        ],
        
        # Tests (move debug files here)
        'tests/': [f for f in os.listdir('.') if f.startswith('debug_') and f.endswith('.py')],
        
        # Config
        'config/': [
            'requirements.txt',
            'tsconfig.json'
        ]
    }
    
    for target_dir, files in file_mappings.items():
        for file in files:
            if os.path.exists(file):
                try:
                    shutil.move(file, target_dir + file)
                    print(f"📁 Moved: {file} → {target_dir}")
                except Exception as e:
                    print(f"❌ Failed to move {file}: {e}")

if __name__ == "__main__":
    print("🏗️ Reorganizing project structure...")
    create_new_structure()
    move_files()
    print("✅ Project reorganization complete!")