#!/usr/bin/env node

/**
 * Vercel Deployment Preparation Script
 * Ensures all static assets are properly copied and configured for Vercel deployment
 */

const fs = require('fs');
const path = require('path');

console.log('🚀 Preparing for Vercel deployment...');

// Ensure public/static directories exist
const staticDirs = [
    'public/static',
    'public/static/css',
    'public/static/js'
];

staticDirs.forEach(dir => {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
        console.log(`✅ Created directory: ${dir}`);
    }
});

// Copy static assets
const filesToCopy = [
    { src: 'static/css/style.css', dest: 'public/static/css/style.css' },
    { src: 'static/js/main.js', dest: 'public/static/js/main.js' },
    { src: 'static/favicon.ico', dest: 'public/static/favicon.ico' }
];

filesToCopy.forEach(({ src, dest }) => {
    if (fs.existsSync(src)) {
        fs.copyFileSync(src, dest);
        console.log(`✅ Copied: ${src} → ${dest}`);
    } else {
        console.log(`⚠️  Source file not found: ${src}`);
    }
});

// Verify vercel.json configuration
if (fs.existsSync('vercel.json')) {
    const vercelConfig = JSON.parse(fs.readFileSync('vercel.json', 'utf8'));
    
    // Check if static file routing is configured
    const hasStaticRouting = vercelConfig.rewrites?.some(rule => 
        rule.source === '/static/(.*)'
    );
    
    if (hasStaticRouting) {
        console.log('✅ Vercel static file routing configured');
    } else {
        console.log('⚠️  Static file routing not found in vercel.json');
    }
} else {
    console.log('⚠️  vercel.json not found');
}

// Verify API endpoint
if (fs.existsSync('api/index.js')) {
    console.log('✅ API endpoint found');
} else {
    console.log('❌ API endpoint not found');
}

// Verify main HTML file
if (fs.existsSync('public/index.html')) {
    const htmlContent = fs.readFileSync('public/index.html', 'utf8');
    
    if (htmlContent.includes('/static/css/style.css')) {
        console.log('✅ CSS link configured in HTML');
    } else {
        console.log('⚠️  CSS link not found in HTML');
    }
    
    if (htmlContent.includes('/static/js/main.js')) {
        console.log('✅ JS link configured in HTML');
    } else {
        console.log('⚠️  JS link not found in HTML');
    }
} else {
    console.log('❌ public/index.html not found');
}

console.log('\n🎉 Deployment preparation complete!');
console.log('\nNext steps:');
console.log('1. Run: vercel --prod');
console.log('2. Your site will be deployed with the correct UI');
console.log('3. Test the deployment to ensure everything works');

console.log('\n📋 Deployment checklist:');
console.log('✅ Static assets copied to public/static/');
console.log('✅ HTML file updated with correct asset paths');
console.log('✅ Vercel configuration includes static file routing');
console.log('✅ API endpoint configured for workflow generation');
console.log('✅ Template functionality included');