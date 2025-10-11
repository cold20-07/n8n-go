#!/usr/bin/env node
/**
 * API with Universal Error Protection
 * Wraps the main API with comprehensive error handling for any prompt
 */

const { UniversalErrorHandler } = require('../universal-error-handler.js');
const originalApiHandler = require('./index.js');

// Create universal error handler instance
const errorHandler = new UniversalErrorHandler();

// Wrap the original API handler
const protectedApiHandler = async (req, res) => {
  console.log('🛡️ API Request with Universal Protection');
  
  try {
    // Create a wrapper for the original API logic
    const wrappedHandler = errorHandler.wrapWorkflowGenerator(
      async (request, response) => {
        // Call original API handler
        await originalApiHandler(request, response);
        
        // If we get here, the API succeeded
        return { success: true };
      },
      {
        source: 'api_request',
        method: req.method,
        url: req.url,
        timestamp: new Date().toISOString()
      }
    );

    // Execute with protection
    await wrappedHandler(req, res);

  } catch (error) {
    console.error('🚨 API Error caught by Universal Protection:', error.message);
    
    // Send error response with fallback workflow if applicable
    if (req.url === '/generate' && req.method === 'POST') {
      try {
        const fallbackWorkflow = await errorHandler.createFallbackWorkflow(error, {
          source: 'api_error',
          url: req.url,
          method: req.method
        }, [req.body]);

        res.status(200).json({
          success: true,
          workflow: fallbackWorkflow,
          workflow_name: fallbackWorkflow.name,
          description: 'Fallback workflow created due to API error',
          filename: `${fallbackWorkflow.name.replace(/\s+/g, '_').toLowerCase()}.json`,
          formatted_json: JSON.stringify(fallbackWorkflow, null, 2),
          node_count: fallbackWorkflow.nodes.length,
          workflow_type: 'fallback_generated',
          error_handled: true,
          original_error: error.message,
          protection_applied: true
        });
      } catch (fallbackError) {
        res.status(500).json({
          success: false,
          error: 'API error and fallback creation failed',
          original_error: error.message,
          fallback_error: fallbackError.message
        });
      }
    } else {
      res.status(500).json({
        success: false,
        error: error.message,
        protection_applied: true,
        timestamp: new Date().toISOString()
      });
    }
  }
};

module.exports = protectedApiHandler;