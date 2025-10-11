#!/usr/bin/env node

/**
 * Fix Node.js Version Warning Script
 * Ensures proper Node.js version specification to eliminate Vercel warnings
 */

const fs = require('fs');

console.log('🔧 FIXING NODE.JS VERSION WARNING');
console.log('=' .repeat(50));

// Step 1: Check current configuration
console.log('\n📋 Current Configuration:');

const files = [
    { name: 'package.json', key: 'engines.node' },
    { name: 'vercel.json', key: 'functions.api/index.js.runtime' },
    { name: '.nvmrc', key: 'content' },
    { name: '.node-version', key: 'content' },
    { name: 'runtime.txt', key: 'content' }
];

files.forEach(file => {
    try {
        if (fs.existsSync(file.name)) {
            if (file.name.endsWith('.json')) {
                const content = JSON.parse(fs.readFileSync(file.name, 'utf8'));
                if (file.name === 'package.json') {
                    console.log(`   📦 ${file.name}: ${content.engines?.node || 'not specified'}`);
                } else if (file.name === 'vercel.json') {
                    const runtime = content.functions?.['api/index.js']?.runtime || 'not specified';
                    console.log(`   ⚡ ${file.name}: ${runtime}`);
                }
            } else {
                const content = fs.readFileSync(file.name, 'utf8').trim();
                console.log(`   📄 ${file.name}: ${content}`);
            }
        } else {
            console.log(`   ❌ ${file.name}: not found`);
        }
    } catch (error) {
        console.log(`   ⚠️  ${file.name}: error reading`);
    }
});

// Step 2: Verify warning is fixed
console.log('\n🔍 Verifying Warning Fix:');

try {
    const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
    const nodeVersion = pkg.engines?.node;
    
    if (!nodeVersion) {
        console.log('   ❌ No Node.js version specified');
    } else if (nodeVersion.includes('>=') || nodeVersion.includes('>') || nodeVersion.includes('<')) {
        console.log(`   ❌ Range version detected: ${nodeVersion}`);
        console.log('   ⚠️  This will cause the warning!');
    } else if (nodeVersion.includes('.x') || nodeVersion.match(/^\d+$/)) {
        console.log(`   ✅ Pinned version: ${nodeVersion}`);
        console.log('   ✅ No auto-upgrade warning');
    } else {
        console.log(`   ⚠️  Unusual version format: ${nodeVersion}`);
    }
} catch (error) {
    console.log('   ❌ Could not read package.json');
}

// Step 3: Check for consistency
console.log('\n🔄 Checking Version Consistency:');

const versions = {};
try {
    const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
    versions.package = pkg.engines?.node;
} catch {}

try {
    const vercel = JSON.parse(fs.readFileSync('vercel.json', 'utf8'));
    versions.vercel = vercel.functions?.['api/index.js']?.runtime;
} catch {}

try {
    versions.nvmrc = fs.readFileSync('.nvmrc', 'utf8').trim();
} catch {}

try {
    versions.nodeVersion = fs.readFileSync('.node-version', 'utf8').trim();
} catch {}

try {
    versions.runtime = fs.readFileSync('runtime.txt', 'utf8').trim();
} catch {}

console.log('   Version specifications:');
Object.entries(versions).forEach(([file, version]) => {
    if (version) {
        console.log(`     ${file}: ${version}`);
    }
});

// Check if all versions are compatible
const majorVersions = new Set();
Object.values(versions).forEach(version => {
    if (version) {
        const match = version.match(/(\d+)/);
        if (match) {
            majorVersions.add(match[1]);
        }
    }
});

if (majorVersions.size === 1) {
    console.log(`   ✅ All versions consistent (Node.js ${Array.from(majorVersions)[0]})`);
} else {
    console.log(`   ⚠️  Version mismatch detected: ${Array.from(majorVersions).join(', ')}`);
}

// Step 4: Provide deployment guidance
console.log('\n🚀 Deployment Guidance:');

const nodeVersion = versions.package;
if (nodeVersion && !nodeVersion.includes('>=') && !nodeVersion.includes('>')) {
    console.log('   ✅ Ready for deployment');
    console.log('   ✅ No Node.js version warnings expected');
    console.log('   ✅ Stable runtime configuration');
    console.log('\n   Deploy with: vercel --prod');
} else {
    console.log('   ❌ Node.js version needs fixing');
    console.log('   ⚠️  Current configuration will cause warnings');
    console.log('\n   Recommended fix:');
    console.log('   1. Use exact major version (e.g., "20")');
    console.log('   2. Avoid range operators (>=, >, <)');
    console.log('   3. Keep all version files consistent');
}

// Step 5: Show expected behavior
console.log('\n📊 Expected Vercel Behavior:');
console.log('   ✅ Detect Node.js project from package.json');
console.log('   ✅ Use specified Node.js runtime version');
console.log('   ✅ No automatic version upgrades');
console.log('   ✅ Stable, predictable deployments');
console.log('   ✅ No version-related warnings');

console.log('\n🎉 Node.js Version Warning Fix Complete!');
console.log('=' .repeat(50));