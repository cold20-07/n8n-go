#!/usr/bin/env python3
"""
Distribution Cleanup Script
Removes non-essential files for a minimal distribution
"""

import os
import shutil
from pathlib import Path

def cleanup_for_distribution():
    """Remove non-essential files for distribution"""
    
    # Files and directories to remove for minimal distribution
    cleanup_items = [
        # Test files (keep only essential ones)
        "test_*.py",
        
        # Documentation files (keep only README)
        "*_SUMMARY.md",
        "*_REPORT.md", 
        "*_NOTES.md",
        "*_INSTRUCTIONS.md",
        "FIXES_*.md",
        "ENHANCED_*.md",
        "FINAL_*.md",
        "COMPREHENSIVE_*.md",
        "MASSIVE_*.md",
        "PERFECTION_*.md",
        "REALISTIC_*.md",
        "CORRECTED_*.md",
        "INTELLIGENT_*.md",
        "PROMPT_*.md",
        "TRAINING_*.md",
        "CONNECTION_*.md",
        "BACKEND_*.md",
        "BRANDING_*.md",
        "BUG_*.md",
        "DARK_*.md",
        "FOOTER_*.md",
        "FORM_*.md",
        "FRONTEND_*.md",
        "LOGIC_*.md",
        "NAME_*.md",
        "PUSH_*.md",
        
        # Build and deployment files (keep essential ones)
        "build-worker.sh",
        "build.sh", 
        "build.bat",
        "Dockerfile",
        "app.yaml",
        "wasmer.toml",
        "wrangler.toml",
        
        # Specialized datasets (can be regenerated)
        "specialized_datasets/",
        
        # Example files (keep minimal)
        "examples/",
        
        # Analysis and research files
        "*_analysis*.py",
        "*_research*.py",
        "workflow-analysis.js",
        
        # Demo and fix files
        "demo_*.py",
        "demo_*.json",
        "fix_*.py",
        "fixes-applied-summary.md",
        
        # Temporary and generated files
        "*.json" # Remove most JSON files except essential ones
    ]
    
    # Essential files to keep
    keep_files = [
        "README.md",
        "package.json", 
        "requirements.txt",
        "training_data/",
        "static/",
        "templates/",
        ".gitignore",
        ".gitattributes"
    ]
    
    print("🧹 Cleaning up for minimal distribution...")
    
    # Count files before cleanup
    before_count = len(list(Path(".").rglob("*")))
    
    # Remove test files (keep only a few essential ones)
    essential_tests = [
        "test_app_startup.py",
        "test_workflow_generation.py", 
        "test_final_system.py"
    ]
    
    for test_file in Path(".").glob("test_*.py"):
        if test_file.name not in essential_tests:
            test_file.unlink()
            print(f"🗑️ Removed {test_file}")
    
    # Remove documentation files (keep only README and essential summaries)
    essential_docs = [
        "README.md",
        "SIZE_OPTIMIZATION_SUMMARY.md"
    ]
    
    for doc_file in Path(".").glob("*.md"):
        if doc_file.name not in essential_docs:
            doc_file.unlink()
            print(f"🗑️ Removed {doc_file}")
    
    # Remove build files
    build_files = [
        "build-worker.sh", "build.sh", "build.bat",
        "Dockerfile", "app.yaml", "wasmer.toml", "wrangler.toml"
    ]
    
    for build_file in build_files:
        if Path(build_file).exists():
            Path(build_file).unlink()
            print(f"🗑️ Removed {build_file}")
    
    # Remove specialized datasets
    if Path("specialized_datasets").exists():
        shutil.rmtree("specialized_datasets")
        print("🗑️ Removed specialized_datasets/")
    
    # Remove examples (keep structure but minimal content)
    if Path("examples").exists():
        shutil.rmtree("examples")
        print("🗑️ Removed examples/")
    
    # Remove analysis and demo files
    for pattern in ["*_analysis*.py", "*_research*.py", "demo_*.py", "demo_*.json", "fix_*.py"]:
        for file in Path(".").glob(pattern):
            if file.is_file():
                file.unlink()
                print(f"🗑️ Removed {file}")
    
    # Remove workflow-analysis.js
    if Path("workflow-analysis.js").exists():
        Path("workflow-analysis.js").unlink()
        print("🗑️ Removed workflow-analysis.js")
    
    # Remove most JSON files except essential ones
    essential_jsons = [
        "package.json",
        "tsconfig.json"
    ]
    
    for json_file in Path(".").glob("*.json"):
        if json_file.name not in essential_jsons:
            json_file.unlink()
            print(f"🗑️ Removed {json_file}")
    
    # Count files after cleanup
    after_count = len(list(Path(".").rglob("*")))
    
    print(f"\n✅ Cleanup complete!")
    print(f"📊 Files removed: {before_count - after_count}")
    print(f"📁 Files remaining: {after_count}")

if __name__ == "__main__":
    cleanup_for_distribution()