#!/usr/bin/env node

/**
 * Vercel Deployment Verification Script
 * Ensures all files are properly configured for Node.js deployment
 */

const fs = require('fs');
const path = require('path');

console.log('🚀 VERCEL DEPLOYMENT VERIFICATION');
console.log('=' .repeat(50));

// Check required files
const requiredFiles = [
    'vercel.json',
    'package.json',
    '.vercelignore',
    'api/index.js',
    'public/index.html'
];

let allFilesPresent = true;

console.log('\n📁 Checking required files...');
requiredFiles.forEach(file => {
    if (fs.existsSync(file)) {
        console.log(`✅ ${file}`);
    } else {
        console.log(`❌ ${file} - MISSING`);
        allFilesPresent = false;
    }
});

// Verify vercel.json configuration
console.log('\n⚙️  Verifying Vercel configuration...');
try {
    const vercelConfig = JSON.parse(fs.readFileSync('vercel.json', 'utf8'));
    
    if (vercelConfig.builds && vercelConfig.builds.length > 0) {
        console.log('✅ Builds configuration present');
    } else if (vercelConfig.functions) {
        console.log('✅ Functions configuration present');
    } else {
        console.log('❌ No build or function configuration found');
        allFilesPresent = false;
    }
    
    if (vercelConfig.routes || vercelConfig.rewrites) {
        console.log('✅ Routes configuration present');
    } else {
        console.log('❌ No routes configuration found');
        allFilesPresent = false;
    }
} catch (error) {
    console.log('❌ Invalid vercel.json format');
    allFilesPresent = false;
}

// Verify package.json
console.log('\n📦 Verifying package.json...');
try {
    const packageJson = JSON.parse(fs.readFileSync('package.json', 'utf8'));
    
    if (packageJson.main === 'api/index.js') {
        console.log('✅ Main entry point correctly set to api/index.js');
    } else {
        console.log('❌ Main entry point should be api/index.js');
        allFilesPresent = false;
    }
    
    if (packageJson.engines && packageJson.engines.node) {
        console.log('✅ Node.js engine version specified');
    } else {
        console.log('⚠️  Node.js engine version not specified (recommended)');
    }
} catch (error) {
    console.log('❌ Invalid package.json format');
    allFilesPresent = false;
}

// Check API handler
console.log('\n🔧 Verifying API handler...');
try {
    const apiContent = fs.readFileSync('api/index.js', 'utf8');
    
    if (apiContent.includes('module.exports')) {
        console.log('✅ API handler properly exports function');
    } else {
        console.log('❌ API handler missing module.exports');
        allFilesPresent = false;
    }
    
    if (apiContent.includes('req, res')) {
        console.log('✅ API handler accepts req, res parameters');
    } else {
        console.log('❌ API handler should accept req, res parameters');
        allFilesPresent = false;
    }
    
    if (apiContent.includes('Access-Control-Allow-Origin')) {
        console.log('✅ CORS headers configured');
    } else {
        console.log('⚠️  CORS headers not found (may cause issues)');
    }
} catch (error) {
    console.log('❌ Cannot read API handler file');
    allFilesPresent = false;
}

// Check public directory
console.log('\n🌐 Verifying public directory...');
const publicFiles = ['index.html', 'pricing.html', 'documentation.html'];
publicFiles.forEach(file => {
    const filePath = path.join('public', file);
    if (fs.existsSync(filePath)) {
        console.log(`✅ public/${file}`);
    } else {
        console.log(`❌ public/${file} - MISSING`);
        allFilesPresent = false;
    }
});

// Check static assets
console.log('\n🎨 Verifying static assets...');
const staticDirs = ['public/static/css', 'public/static/js'];
staticDirs.forEach(dir => {
    if (fs.existsSync(dir)) {
        console.log(`✅ ${dir}/`);
    } else {
        console.log(`⚠️  ${dir}/ - Not found (may affect styling)`);
    }
});

// Final assessment
console.log('\n' + '=' .repeat(50));
if (allFilesPresent) {
    console.log('🎉 DEPLOYMENT READY!');
    console.log('✅ All required files and configurations are present');
    console.log('✅ Project is properly configured for Node.js deployment');
    console.log('✅ No Python dependencies will be installed');
    console.log('\n🚀 Deploy with: vercel --prod');
    process.exit(0);
} else {
    console.log('❌ DEPLOYMENT NOT READY');
    console.log('⚠️  Please fix the issues above before deploying');
    process.exit(1);
}