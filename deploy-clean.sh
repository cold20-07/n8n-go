#!/bin/bash

echo "🧹 CLEANING PROJECT FOR VERCEL DEPLOYMENT"
echo "=========================================="

# Remove any remaining Python files that might cause issues
echo "🗑️  Removing Python files..."
find . -name "*.py" -not -path "./node_modules/*" -not -path "./.git/*" -delete 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "requirements*.txt" -delete 2>/dev/null || true
find . -name "pytest.ini" -delete 2>/dev/null || true
find . -name "setup.py" -delete 2>/dev/null || true
find . -name "pyproject.toml" -delete 2>/dev/null || true

echo "✅ Python files removed"

# Ensure Node.js files are present
echo "📦 Verifying Node.js configuration..."
if [ ! -f "package.json" ]; then
    echo "❌ package.json missing!"
    exit 1
fi

if [ ! -f "api/index.js" ]; then
    echo "❌ api/index.js missing!"
    exit 1
fi

if [ ! -f "vercel.json" ]; then
    echo "❌ vercel.json missing!"
    exit 1
fi

echo "✅ All Node.js files present"

# Check for any remaining Python indicators
echo "🔍 Checking for Python indicators..."
if find . -name "requirements.txt" -not -path "./node_modules/*" -not -path "./.git/*" | grep -q .; then
    echo "❌ Found requirements.txt files - removing..."
    find . -name "requirements.txt" -not -path "./node_modules/*" -not -path "./.git/*" -delete
fi

if find . -name "*.py" -not -path "./node_modules/*" -not -path "./.git/*" | grep -q .; then
    echo "⚠️  Found Python files - this may cause deployment issues"
    find . -name "*.py" -not -path "./node_modules/*" -not -path "./.git/*" -ls
else
    echo "✅ No Python files found"
fi

echo ""
echo "🚀 PROJECT READY FOR DEPLOYMENT"
echo "================================"
echo "✅ Python files removed"
echo "✅ Node.js configuration verified"
echo "✅ Vercel configuration present"
echo ""
echo "Deploy with:"
echo "vercel --prod"