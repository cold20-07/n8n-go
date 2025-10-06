#!/usr/bin/env python3
"""
Cleanup Debug Files
Removes debug and analysis files that are no longer needed
"""

import os
from pathlib import Path

def cleanup_debug_files():
    """Remove debug and analysis files"""
    
    print("🧹 Cleaning up debug and analysis files...")
    
    # Files to remove
    debug_files = [
        "analyze_100k_results.py",
        "analyze_logic_errors.py", 
        "debug_complexity_score.py",
        "debug_complexity.py",
        "debug_connections.py",
        "debug_double_generation.py",
        "debug_failed_tests.py",
        "debug_failure_rate.py",
        "debug_linkedin.py",
        "debug_test_failures.py",
        "create_minimal_perfect_workflow.py",
        "deploy_wasmer.py",
        "final_connection_test.py",
        "generate_final_test.py",
        "intelligent_node_demo.py",
        "interactive_prompt_assistant.py",
        "n8n_training_summary.py",
        "optimize_validation_system.py",
        "quick_connection_test.py",
        "quick_test.py",
        "simple_connection_fixer.py",
        "start_server.py",
        "training_fixes.py",
        "corrected_validation_system.py",
        "prompt_assistance_system.py"
    ]
    
    # JavaScript files to remove
    js_files = [
        "n8n-automation-generator.js",
        "n8n-iterative-test-runner.js", 
        "run-iterative-tests.js",
        "code-node-examples.js"
    ]
    
    # Training system files (keep only the main one)
    training_files = [
        "final_n8n_training_system.py",
        "improved_n8n_training_system.py",
        "optimized_n8n_training_system.py"
    ]
    
    removed_count = 0
    
    # Remove debug files
    for file in debug_files + js_files + training_files:
        if Path(file).exists():
            Path(file).unlink()
            print(f"🗑️ Removed {file}")
            removed_count += 1
    
    # Remove TypeScript files if not needed
    ts_files = ["main.ts", "tsconfig.json"]
    for file in ts_files:
        if Path(file).exists():
            Path(file).unlink()
            print(f"🗑️ Removed {file}")
            removed_count += 1
    
    print(f"\\n✅ Cleanup complete! Removed {removed_count} files")
    
    # Check final size
    total_size = sum(f.stat().st_size for f in Path('.').rglob('*') if f.is_file())
    size_mb = total_size / (1024 * 1024)
    print(f"📊 Current project size: {size_mb:.2f} MB")

if __name__ == "__main__":
    cleanup_debug_files()