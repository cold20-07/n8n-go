#!/usr/bin/env node

/**
 * Force Node.js-only deployment by removing ALL Python traces
 * This script ensures Vercel sees ONLY Node.js configuration
 */

const fs = require('fs');
const path = require('path');

console.log('🧹 FORCING NODE.JS-ONLY DEPLOYMENT');
console.log('=' .repeat(50));

// Step 1: Remove ALL Python files
console.log('\n🗑️  Removing ALL Python files...');

const pythonExtensions = ['.py', '.pyc', '.pyo', '.pyd'];
const pythonFiles = [
    'requirements.txt',
    'requirements-dev.txt', 
    'requirements-prod.txt',
    'setup.py',
    'setup.cfg',
    'pyproject.toml',
    'pytest.ini',
    'tox.ini',
    'Pipfile',
    'Pipfile.lock',
    'poetry.lock',
    'conda.yml',
    'environment.yml'
];

function removeFile(filePath) {
    try {
        if (fs.existsSync(filePath)) {
            fs.unlinkSync(filePath);
            console.log(`   ✅ Removed: ${filePath}`);
            return true;
        }
    } catch (error) {
        console.log(`   ⚠️  Could not remove: ${filePath}`);
    }
    return false;
}

function removeDirectory(dirPath) {
    try {
        if (fs.existsSync(dirPath)) {
            fs.rmSync(dirPath, { recursive: true, force: true });
            console.log(`   ✅ Removed directory: ${dirPath}`);
            return true;
        }
    } catch (error) {
        console.log(`   ⚠️  Could not remove directory: ${dirPath}`);
    }
    return false;
}

// Remove Python configuration files
pythonFiles.forEach(file => removeFile(file));

// Remove Python directories
const pythonDirs = ['__pycache__', '.pytest_cache', '.mypy_cache', 'venv', '.venv', 'env'];
pythonDirs.forEach(dir => removeDirectory(dir));

// Find and remove all .py files
function findAndRemovePythonFiles(dir) {
    if (!fs.existsSync(dir)) return;
    
    const items = fs.readdirSync(dir);
    
    for (const item of items) {
        const fullPath = path.join(dir, item);
        const stat = fs.statSync(fullPath);
        
        if (stat.isDirectory()) {
            // Skip node_modules, .git, and other safe directories
            if (!['node_modules', '.git', '.vercel', 'public'].includes(item)) {
                findAndRemovePythonFiles(fullPath);
            }
        } else if (stat.isFile()) {
            const ext = path.extname(item);
            if (pythonExtensions.includes(ext)) {
                removeFile(fullPath);
            }
        }
    }
}

// Remove Python files from root and subdirectories
findAndRemovePythonFiles('.');

// Step 2: Create Node.js-only indicators
console.log('\n📦 Creating Node.js-only indicators...');

// Create a .node-version file
fs.writeFileSync('.node-version', '18.19.0');
console.log('   ✅ Created .node-version');

// Update .vercelignore to be even more aggressive
const vercelIgnore = `# FORCE NODE.JS DEPLOYMENT - BLOCK ALL PYTHON
# This file ensures Vercel ONLY sees Node.js

# Block ALL Python files and directories
*.py
*.pyc
*.pyo
*.pyd
__pycache__/
.Python
env/
venv/
.venv/
.pytest_cache/
.mypy_cache/
.tox/
.coverage*
*.egg-info/

# Block ALL Python configuration
requirements*.txt
setup.py
setup.cfg
pyproject.toml
pytest.ini
tox.ini
Pipfile*
poetry.lock
conda.yml
environment.yml

# Block Python application files
app.py
config.py
logger.py
exceptions.py
main.py
run.py
wsgi.py
gunicorn*.py
manage.py

# Block Python directories
src/
tests/
migrations/
alembic/
scripts/
training_data/
backups/
logs/

# Block documentation that might reference Python
docs/
*.md
!README.md

# Block development files
.env*
.DS_Store
.vscode/
.idea/
*.swp
*.swo

# Block all JSON except essential
*.json
!package.json
!package-lock.json
!vercel.json

# Block everything else that's not Node.js
*.txt
!.nvmrc
*.ini
*.cfg
*.toml
*.lock
*.log
*.db
*.sqlite*

# Keep only essential Node.js files
!api/
!public/
!node_modules/
!.vercel/
`;

fs.writeFileSync('.vercelignore', vercelIgnore);
console.log('   ✅ Updated .vercelignore with aggressive Python blocking');

// Step 3: Create explicit Node.js configuration
console.log('\n⚙️  Creating explicit Node.js configuration...');

// Create a vercel.json that ONLY supports Node.js
const vercelConfig = {
    "version": 2,
    "framework": null,
    "buildCommand": "echo 'Node.js build complete'",
    "builds": [
        {
            "src": "api/index.js",
            "use": "@vercel/node@latest",
            "config": {
                "runtime": "nodejs18.x",
                "maxLambdaSize": "50mb"
            }
        },
        {
            "src": "public/**/*",
            "use": "@vercel/static"
        }
    ],
    "routes": [
        { "src": "/health", "dest": "/api/index.js" },
        { "src": "/generate", "dest": "/api/index.js" },
        { "src": "/api/(.*)", "dest": "/api/index.js" },
        { "src": "/static/(.*)", "dest": "/public/static/$1" },
        { "src": "/pricing", "dest": "/public/pricing.html" },
        { "src": "/documentation", "dest": "/public/documentation.html" },
        { "src": "/", "dest": "/public/index.html" }
    ],
    "functions": {
        "api/index.js": {
            "runtime": "nodejs18.x",
            "maxDuration": 30
        }
    },
    "headers": [
        {
            "source": "/static/(.*)",
            "headers": [
                { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
            ]
        }
    ],
    "env": {
        "NODE_ENV": "production"
    }
};

fs.writeFileSync('vercel.json', JSON.stringify(vercelConfig, null, 2));
console.log('   ✅ Created Node.js-only vercel.json');

// Update package.json to be more explicit
const packageJson = {
    "name": "n8n-workflow-generator",
    "version": "1.0.0",
    "description": "Node.js serverless n8n workflow generator",
    "main": "api/index.js",
    "type": "commonjs",
    "scripts": {
        "start": "node api/index.js",
        "build": "echo 'Node.js build complete'",
        "vercel-build": "echo 'Vercel Node.js build complete'"
    },
    "keywords": ["nodejs", "serverless", "n8n", "workflow", "vercel"],
    "author": "N8N Generator Team",
    "license": "MIT",
    "engines": {
        "node": "18.x",
        "npm": ">=8.0.0"
    },
    "dependencies": {},
    "devDependencies": {}
};

fs.writeFileSync('package.json', JSON.stringify(packageJson, null, 2));
console.log('   ✅ Updated package.json for Node.js-only');

// Step 4: Verification
console.log('\n🔍 Verifying Node.js-only configuration...');

const requiredFiles = ['package.json', 'vercel.json', 'api/index.js'];
let allGood = true;

requiredFiles.forEach(file => {
    if (fs.existsSync(file)) {
        console.log(`   ✅ ${file} exists`);
    } else {
        console.log(`   ❌ ${file} missing`);
        allGood = false;
    }
});

// Check for any remaining Python files
const remainingPython = [];
function checkForPython(dir) {
    if (!fs.existsSync(dir) || ['node_modules', '.git', '.vercel'].includes(path.basename(dir))) return;
    
    const items = fs.readdirSync(dir);
    for (const item of items) {
        const fullPath = path.join(dir, item);
        const stat = fs.statSync(fullPath);
        
        if (stat.isFile() && (item.endsWith('.py') || item === 'requirements.txt')) {
            remainingPython.push(fullPath);
        } else if (stat.isDirectory()) {
            checkForPython(fullPath);
        }
    }
}

checkForPython('.');

if (remainingPython.length > 0) {
    console.log('\n⚠️  Remaining Python files found:');
    remainingPython.forEach(file => console.log(`   - ${file}`));
    allGood = false;
} else {
    console.log('   ✅ No Python files detected');
}

// Final status
console.log('\n' + '=' .repeat(50));
if (allGood) {
    console.log('🎉 NODE.JS-ONLY DEPLOYMENT READY!');
    console.log('✅ All Python files removed');
    console.log('✅ Node.js configuration verified');
    console.log('✅ Vercel will see ONLY Node.js');
    console.log('\n🚀 Deploy with: vercel --prod');
    console.log('\nNo more Python/pip warnings! 🎉');
} else {
    console.log('❌ Issues found - please review above');
}

process.exit(allGood ? 0 : 1);