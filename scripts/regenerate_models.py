#!/usr/bin/env python3
"""
Model Regeneration Script
Run this to regenerate the trained models from training data
"""

import os
import sys
from pathlib import Path

def regenerate_models():
    """Regenerate all trained models"""
    print("🔄 Regenerating trained models...")
    
    # Create model directories
    Path("trained_models").mkdir(exist_ok=True)
    Path("improved_models").mkdir(exist_ok=True) 
    Path("final_models").mkdir(exist_ok=True)
    
    try:
        # Import and run the training system
        from n8n_training_system import N8nTrainingSystem
        
        trainer = N8nTrainingSystem()
        trainer.train_all_models()
        
        print("✅ Models regenerated successfully!")
        print("📁 Check trained_models/, improved_models/, and final_models/ directories")
        
    except ImportError as e:
        print(f"❌ Could not import training system: {e}")
        print("💡 The app will work with fallback methods without trained models")
        
    except Exception as e:
        print(f"❌ Error during model training: {e}")
        print("💡 The app will work with fallback methods without trained models")

if __name__ == "__main__":
    regenerate_models()