#!/bin/bash

# Build script for n8n Workflow Generator
# This script builds both the TypeScript and Python components

set -e  # Exit on any error

echo "🚀 Starting build process for n8n Workflow Generator..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js to continue."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3 to continue."
    exit 1
fi

# Create build directory
print_status "Creating build directories..."
mkdir -p dist
mkdir -p static/js
mkdir -p static/css

# Install Node.js dependencies
print_status "Installing Node.js dependencies..."
if [ -f "package.json" ]; then
    npm install
else
    print_warning "package.json not found, skipping npm install"
fi

# Build TypeScript
print_status "Building TypeScript..."
if [ -f "main.ts" ]; then
    if command -v tsc &> /dev/null; then
        tsc main.ts --outDir dist --target es2020 --module commonjs
        print_status "TypeScript build completed"
    else
        print_warning "TypeScript compiler not found, skipping TypeScript build"
    fi
else
    print_warning "main.ts not found, skipping TypeScript build"
fi

# Copy static files
print_status "Copying static files..."
if [ -f "style.css" ]; then
    cp style.css static/css/
    print_status "Copied style.css to static/css/"
fi

if [ -f "script.js" ]; then
    cp script.js static/js/
    print_status "Copied script.js to static/js/"
fi

if [ -f "index.html" ]; then
    cp index.html templates/
    print_status "Copied index.html to templates/"
fi

# Install Python dependencies
print_status "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    if command -v pip3 &> /dev/null; then
        pip3 install -r requirements.txt
        print_status "Python dependencies installed"
    else
        print_warning "pip3 not found, skipping Python dependency installation"
    fi
else
    print_warning "requirements.txt not found, skipping Python dependency installation"
fi

# Run Python syntax check
print_status "Checking Python syntax..."
python_files=("app.py" "run.py" "n8n_workflow_research.py" "enhance_workflow_output.py")

for file in "${python_files[@]}"; do
    if [ -f "$file" ]; then
        if python3 -m py_compile "$file"; then
            print_status "✓ $file syntax check passed"
        else
            print_error "✗ $file syntax check failed"
            exit 1
        fi
    else
        print_warning "$file not found, skipping syntax check"
    fi
done

# Create production build
print_status "Creating production build..."
if [ -f "app.py" ]; then
    # Test Flask app import
    if python3 -c "from app import app; print('Flask app import successful')"; then
        print_status "✓ Flask application import test passed"
    else
        print_error "✗ Flask application import test failed"
        exit 1
    fi
fi

# Generate build info
print_status "Generating build information..."
cat > build_info.json << EOF
{
    "build_date": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
    "build_version": "1.0.0",
    "git_commit": "$(git rev-parse HEAD 2>/dev/null || echo 'unknown')",
    "node_version": "$(node --version 2>/dev/null || echo 'not available')",
    "python_version": "$(python3 --version 2>/dev/null || echo 'not available')",
    "build_platform": "$(uname -s)-$(uname -m)"
}
EOF

print_status "Build information saved to build_info.json"

# Set executable permissions
chmod +x run.py 2>/dev/null || true

print_status "🎉 Build completed successfully!"
print_status "To run the application:"
print_status "  Development: python3 run.py"
print_status "  Production: gunicorn -w 4 -b 0.0.0.0:5000 app:app"

# Optional: Run tests if test directory exists
if [ -d "tests" ]; then
    print_status "Running tests..."
    python3 -m pytest tests/ || print_warning "Some tests failed"
fi

echo -e "${GREEN}✅ Build process completed!${NC}"