#!/usr/bin/env node

/**
 * Comprehensive Test Script for Vercel Deployment
 * Tests all UI/UX functionality and API endpoints
 */

const fs = require('fs');
const path = require('path');

console.log('🧪 Testing Vercel Deployment Functionality...\n');

// Test 1: Check all required files exist
console.log('📁 Testing File Structure:');
const requiredFiles = [
    'public/index.html',
    'public/pricing.html', 
    'public/documentation.html',
    'public/static/css/style.css',
    'public/static/js/main.js',
    'public/static/favicon.ico',
    'api/index.js',
    'vercel.json'
];

let filesOk = true;
requiredFiles.forEach(file => {
    if (fs.existsSync(file)) {
        console.log(`✅ ${file}`);
    } else {
        console.log(`❌ ${file} - MISSING`);
        filesOk = false;
    }
});

// Test 2: Check HTML files have correct links
console.log('\n🔗 Testing HTML Links:');
const htmlFiles = ['public/index.html', 'public/pricing.html', 'public/documentation.html'];
let linksOk = true;

htmlFiles.forEach(file => {
    if (fs.existsSync(file)) {
        const content = fs.readFileSync(file, 'utf8');
        
        // Check CSS link
        if (content.includes('/static/css/style.css')) {
            console.log(`✅ ${file} - CSS linked correctly`);
        } else {
            console.log(`❌ ${file} - CSS link missing`);
            linksOk = false;
        }
        
        // Check JS link
        if (content.includes('/static/js/main.js')) {
            console.log(`✅ ${file} - JS linked correctly`);
        } else {
            console.log(`❌ ${file} - JS link missing`);
            linksOk = false;
        }
        
        // Check navigation links
        if (content.includes('/pricing.html') && content.includes('/documentation.html')) {
            console.log(`✅ ${file} - Navigation links correct`);
        } else {
            console.log(`❌ ${file} - Navigation links incorrect`);
            linksOk = false;
        }
    }
});

// Test 3: Check JavaScript functionality
console.log('\n⚙️ Testing JavaScript Functions:');
const jsContent = fs.readFileSync('public/static/js/main.js', 'utf8');
let jsOk = true;

const requiredFunctions = [
    'loadTemplate',
    'showMessage',
    'showLoading',
    'hideLoading',
    'generateWorkflow',
    'displayWorkflow',
    'checkPromptHelp',
    'WorkflowGenerator'
];

requiredFunctions.forEach(func => {
    if (jsContent.includes(`function ${func}`) || jsContent.includes(`${func}(`)) {
        console.log(`✅ ${func} function found`);
    } else {
        console.log(`❌ ${func} function missing`);
        jsOk = false;
    }
});

// Test 4: Check API endpoints
console.log('\n🌐 Testing API Configuration:');
const apiContent = fs.readFileSync('api/index.js', 'utf8');
let apiOk = true;

const requiredEndpoints = [
    '/health',
    '/generate',
    '/api/templates/',
    'TEMPLATES'
];

requiredEndpoints.forEach(endpoint => {
    if (apiContent.includes(endpoint)) {
        console.log(`✅ ${endpoint} endpoint configured`);
    } else {
        console.log(`❌ ${endpoint} endpoint missing`);
        apiOk = false;
    }
});

// Test 5: Check Vercel configuration
console.log('\n⚡ Testing Vercel Configuration:');
const vercelConfig = JSON.parse(fs.readFileSync('vercel.json', 'utf8'));
let vercelOk = true;

const requiredRoutes = [
    { source: '/static/(.*)', destination: '/public/static/$1' },
    { source: '/pricing.html', destination: '/public/pricing.html' },
    { source: '/documentation.html', destination: '/public/documentation.html' },
    { source: '/generate', destination: '/api/index.js' },
    { source: '/api/(.*)', destination: '/api/index.js' }
];

requiredRoutes.forEach(route => {
    const found = vercelConfig.rewrites.some(r => 
        r.source === route.source && r.destination === route.destination
    );
    
    if (found) {
        console.log(`✅ Route: ${route.source} → ${route.destination}`);
    } else {
        console.log(`❌ Route missing: ${route.source} → ${route.destination}`);
        vercelOk = false;
    }
});

// Test 6: Check CSS classes and styling
console.log('\n🎨 Testing CSS Styling:');
const cssContent = fs.readFileSync('public/static/css/style.css', 'utf8');
let cssOk = true;

const requiredClasses = [
    '.hero',
    '.json-generator',
    '.template-btn',
    '.generate-button',
    '.output-card',
    '.pricing-card',
    '.docs-sidebar',
    '.message'
];

requiredClasses.forEach(className => {
    if (cssContent.includes(className)) {
        console.log(`✅ ${className} styling found`);
    } else {
        console.log(`❌ ${className} styling missing`);
        cssOk = false;
    }
});

// Test 7: Check template system
console.log('\n📋 Testing Template System:');
const templates = ['rss_to_social', 'email_processing', 'data_backup', 'ecommerce_orders'];
let templatesOk = true;

templates.forEach(template => {
    if (apiContent.includes(`'${template}'`)) {
        console.log(`✅ Template: ${template}`);
    } else {
        console.log(`❌ Template missing: ${template}`);
        templatesOk = false;
    }
});

// Test 8: Check form elements
console.log('\n📝 Testing Form Elements:');
const indexContent = fs.readFileSync('public/index.html', 'utf8');
let formOk = true;

const requiredFormElements = [
    'id="workflowForm"',
    'id="description"',
    'id="triggerType"',
    'id="output"',
    'id="copyBtn"',
    'id="downloadBtn"'
];

requiredFormElements.forEach(element => {
    if (indexContent.includes(element)) {
        console.log(`✅ Form element: ${element}`);
    } else {
        console.log(`❌ Form element missing: ${element}`);
        formOk = false;
    }
});

// Final Results
console.log('\n📊 Test Results Summary:');
console.log('========================');

const allTests = [
    { name: 'File Structure', status: filesOk },
    { name: 'HTML Links', status: linksOk },
    { name: 'JavaScript Functions', status: jsOk },
    { name: 'API Configuration', status: apiOk },
    { name: 'Vercel Configuration', status: vercelOk },
    { name: 'CSS Styling', status: cssOk },
    { name: 'Template System', status: templatesOk },
    { name: 'Form Elements', status: formOk }
];

let allPassed = true;
allTests.forEach(test => {
    const status = test.status ? '✅ PASS' : '❌ FAIL';
    console.log(`${status} - ${test.name}`);
    if (!test.status) allPassed = false;
});

console.log('\n' + '='.repeat(50));
if (allPassed) {
    console.log('🎉 ALL TESTS PASSED! Ready for deployment.');
    console.log('\nNext steps:');
    console.log('1. Run: vercel --prod');
    console.log('2. Test the deployed site thoroughly');
    console.log('3. Verify all features work in production');
} else {
    console.log('⚠️  SOME TESTS FAILED! Please fix issues before deployment.');
}

console.log('\n🚀 Deployment Command: vercel --prod');
console.log('📝 After deployment, test these features:');
console.log('   • Homepage loads with correct styling');
console.log('   • Template buttons work');
console.log('   • Workflow generation works');
console.log('   • Copy/download functionality works');
console.log('   • Pricing page loads correctly');
console.log('   • Documentation page loads correctly');
console.log('   • Navigation between pages works');
console.log('   • Mobile responsiveness');