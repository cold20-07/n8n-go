/**
 * N8N Workflow Generator 2.0 - Root Script File
 * 
 * This file serves as a compatibility layer for users expecting
 * script.js in the root directory. The actual application logic
 * is located in static/js/main.js
 */

// Redirect notice for developers
console.warn('⚠️  script.js has been moved to static/js/main.js');
console.info('📁 Please update your references to use the new file structure');
console.info('🔗 Main application: static/js/main.js');
console.info('🔗 Enhanced version: static/js/enhanced-main.js');

// If this script is loaded in a browser context, redirect to the proper location
if (typeof window !== 'undefined') {
    console.info('🚀 Redirecting to public/index.html for the full application');
    
    // Check if we're not already in the public directory
    if (!window.location.pathname.includes('/public/')) {
        window.location.href = 'public/index.html';
    }
}

// Export a notice for Node.js environments
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        notice: 'This file has been moved. Please use static/js/main.js instead.',
        newLocation: 'static/js/main.js',
        enhancedVersion: 'static/js/enhanced-main.js'
    };
}