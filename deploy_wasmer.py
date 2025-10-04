#!/usr/bin/env python3
"""
Deployment script for Wasmer Edge
Automates the deployment of n8n Workflow Generator to Wasmer Edge
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path

class WasmerDeployer:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.wasmer_config = self.project_root / "wasmer.toml"
        
    def check_prerequisites(self):
        """Check if all prerequisites are met"""
        print("🔍 Checking prerequisites...")
        
        # Check if wasmer is installed
        try:
            result = subprocess.run(["wasmer", "--version"], 
                                  capture_output=True, text=True, check=True)
            print(f"✅ Wasmer installed: {result.stdout.strip()}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Wasmer is not installed or not in PATH")
            print("Please install Wasmer: https://wasmer.io/install")
            return False
        
        # Check if wasmer.toml exists
        if not self.wasmer_config.exists():
            print("❌ wasmer.toml not found")
            return False
        
        print("✅ wasmer.toml found")
        
        # Check if required files exist
        required_files = ["app.py", "requirements.txt"]
        for file in required_files:
            if not (self.project_root / file).exists():
                print(f"❌ Required file {file} not found")
                return False
            print(f"✅ {file} found")
        
        return True
    
    def build_application(self):
        """Build the application for Wasmer"""
        print("🔨 Building application...")
        
        try:
            # Install Python dependencies
            print("📦 Installing Python dependencies...")
            subprocess.run([
                "pip", "install", "-r", "requirements.txt", "--target", "./lib"
            ], check=True, cwd=self.project_root)
            
            # Create deployment package
            print("📦 Creating deployment package...")
            
            # Copy necessary files
            deployment_files = [
                "app.py",
                "run.py", 
                "n8n_workflow_research.py",
                "enhance_workflow_output.py",
                "requirements.txt"
            ]
            
            for file in deployment_files:
                source = self.project_root / file
                if source.exists():
                    print(f"✅ Including {file}")
                else:
                    print(f"⚠️  {file} not found, skipping")
            
            print("✅ Build completed")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Build failed: {e}")
            return False
    
    def deploy_to_wasmer(self):
        """Deploy to Wasmer Edge"""
        print("🚀 Deploying to Wasmer Edge...")
        
        try:
            # Login check
            print("🔐 Checking Wasmer login status...")
            try:
                subprocess.run(["wasmer", "whoami"], 
                             check=True, capture_output=True)
                print("✅ Already logged in to Wasmer")
            except subprocess.CalledProcessError:
                print("❌ Not logged in to Wasmer")
                print("Please run: wasmer login")
                return False
            
            # Deploy the package
            print("📤 Deploying package...")
            result = subprocess.run([
                "wasmer", "deploy", "--non-interactive"
            ], cwd=self.project_root, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Deployment successful!")
                
                # Extract deployment URL from output
                output_lines = result.stdout.split('\n')
                for line in output_lines:
                    if 'https://' in line and 'wasmer.app' in line:
                        print(f"🌐 Application URL: {line.strip()}")
                        break
                
                return True
            else:
                print(f"❌ Deployment failed: {result.stderr}")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Deployment error: {e}")
            return False
    
    def test_deployment(self, url=None):
        """Test the deployed application"""
        if not url:
            print("⚠️  No URL provided for testing")
            return
        
        print(f"🧪 Testing deployment at {url}")
        
        try:
            import requests
            
            # Test health endpoint
            health_url = f"{url}/health" if not url.endswith('/') else f"{url}health"
            response = requests.get(health_url, timeout=10)
            
            if response.status_code == 200:
                print("✅ Health check passed")
            else:
                print(f"⚠️  Health check returned status {response.status_code}")
            
            # Test main endpoint
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print("✅ Main endpoint accessible")
            else:
                print(f"⚠️  Main endpoint returned status {response.status_code}")
                
        except ImportError:
            print("⚠️  requests library not available, skipping tests")
        except Exception as e:
            print(f"⚠️  Test failed: {e}")
    
    def cleanup(self):
        """Clean up temporary files"""
        print("🧹 Cleaning up...")
        
        # Remove lib directory if it exists
        lib_dir = self.project_root / "lib"
        if lib_dir.exists():
            import shutil
            shutil.rmtree(lib_dir)
            print("✅ Cleaned up temporary files")
    
    def deploy(self):
        """Main deployment process"""
        print("🚀 Starting Wasmer Edge deployment...")
        print("=" * 50)
        
        try:
            # Check prerequisites
            if not self.check_prerequisites():
                print("❌ Prerequisites not met")
                return False
            
            # Build application
            if not self.build_application():
                print("❌ Build failed")
                return False
            
            # Deploy to Wasmer
            if not self.deploy_to_wasmer():
                print("❌ Deployment failed")
                return False
            
            print("=" * 50)
            print("🎉 Deployment completed successfully!")
            print("📝 Next steps:")
            print("   1. Test your application")
            print("   2. Configure custom domain (optional)")
            print("   3. Set up monitoring")
            
            return True
            
        except KeyboardInterrupt:
            print("\n⚠️  Deployment cancelled by user")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
        finally:
            self.cleanup()

def main():
    """Main entry point"""
    deployer = WasmerDeployer()
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "check":
            deployer.check_prerequisites()
        elif command == "build":
            deployer.build_application()
        elif command == "deploy":
            deployer.deploy()
        elif command == "cleanup":
            deployer.cleanup()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: check, build, deploy, cleanup")
    else:
        # Run full deployment
        success = deployer.deploy()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()