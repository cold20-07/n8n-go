#!/usr/bin/env node
/**
 * 50 Prompt Comprehensive Test Suite
 */

const { WorkflowValidator } = require('./comprehensive_workflow_tester.js');

const fiftyPrompts = [
  // Business & Productivity (1-10)
  {
    name: "Slack Lead Notification",
    description: "Create a workflow that automatically sends a Slack message when a new lead is added to Google Sheets.",
    triggerType: "webhook",
    complexity: "medium"
  },
  {
    name: "Gmail to Trello Task",
    description: "Build an automation to create a new Trello card when a Gmail email arrives with the label 'Task'.",
    triggerType: "webhook", 
    complexity: "medium"
  },
  {
    name: "Airtable to Notion Sync",
    description: "Sync every new Airtable record to a Notion database.",
    triggerType: "webhook",
    complexity: "medium"
  },
  {
    name: "Google Drive to Dropbox Backup",
    description: "Automatically back up all Google Drive files daily to Dropbox.",
    triggerType: "schedule",
    complexity: "complex"
  },
  {
    name: "Asana Weekly Email Summary",
    description: "Send an email summary via Gmail of all completed Asana tasks every Friday.",
    triggerType: "schedule",
    complexity: "complex"
  },
  {
    name: "Typeform to Google Sheets",
    description: "Create a new row in Google Sheets whenever a new form response is submitted in Typeform.",
    triggerType: "webhook",
    complexity: "medium"
  },
  {
    name: "OneDrive to Teams Notification",
    description: "Post a message to Microsoft Teams when a new document is uploaded to OneDrive.",
    triggerType: "webhook",
    complexity: "medium"
  },
  {
    name: "HubSpot Daily Sales Report",
    description: "Generate a daily summary report of all closed deals in HubSpot and email it to the sales manager.",
    triggerType: "schedule",
    complexity: "complex"
  },
  {
    name: "File Upload Telegram Alert",
    description: "Monitor a shared folder and notify the admin via Telegram when a new file is uploaded.",
    triggerType: "webhook",
    complexity: "medium"
  },
  {
    name: "Email to GitHub Issues",
    description: "Auto-create GitHub issues from incoming support emails labeled 'bug'.",
    triggerType: "webhook",
    complexity: "medium"
  },

  // Social Media & Marketing (11-20)
  {
    name: "Instagram Auto-Posting",
    description: "Schedule daily Instagram posts automatically from a Google Sheet of content ideas.",
    triggerType: "schedule",
    complexity: "medium"
  },
  {
    name: "YouTube to Twitter Auto-Post",
    description: "Auto-post to Twitter when a new YouTube video goes live on your channel.",
    triggerType: "webhook",
    complexity: "medium"
  },
  {
    name: "Google Ads to Notion CRM",
    description: "Collect new Google Ads leads into a Notion CRM database.",
    triggerType: "webhook",
    complexity: "medium"
  },
  {
    name: "YouTube Comments WhatsApp Alert",
    description: "Send a WhatsApp alert when a trending keyword appears in your YouTube comments.",
    triggerType: "webhook",
    complexity: "complex"
  },
  {
    name: "Social Media Performance Reports",
    description: "Create a workflow that generates weekly performance reports for social media campaigns.",
    triggerType: "schedule",
    complexity: "complex"
  },
  {
    name: "Twitter Images to Google Drive",
    description: "Save every linked image from Tweets containing a specific hashtag into Google Drive.",
    triggerType: "webhook",
    complexity: "complex"
  },
  {
    name: "Facebook to Mailchimp Sync",
    description: "Sync new Facebook page leads to a Mailchimp audience list.",
    triggerType: "webhook",
    complexity: "medium"
  },
  {
    name: "Instagram DM Translation",
    description: "Automatically translate incoming Instagram DMs using DeepL API and reply with the translated message.",
    triggerType: "webhook",
    complexity: "complex"
  },
  {
    name: "Instagram Auto-Thank You",
    description: "Post a thank-you comment automatically when someone tags your brand on Instagram.",
    triggerType: "webhook",
    complexity: "medium"
  },
  {
    name: "LinkedIn to Notion Archive",
    description: "Fetch all new LinkedIn posts from a company page and archive them in Notion.",
    triggerType: "schedule",
    complexity: "complex"
  },

  // AI & Automation (21-30)
  {
    name: "Gmail AI Summary",
    description: "Create an automation that summarizes all unread Gmail emails daily using GPT API.",
    triggerType: "schedule",
    complexity: "complex"
  },
  {
    name: "Customer Feedback AI Categorization",
    description: "Build a workflow that categorizes customer feedback using OpenAI and logs results in Airtable.",
    triggerType: "webhook",
    complexity: "complex"
  },
  {
    name: "AI Blog Ideas from Trends",
    description: "Auto-generate blog ideas from trending Google Trends data using Gemini API.",
    triggerType: "schedule",
    complexity: "complex"
  },
  {
    name: "Zoom Transcript Summary",
    description: "Summarize Zoom meeting transcripts and send a formatted document to Google Docs.",
    triggerType: "webhook",
    complexity: "complex"
  },
  {
    name: "Review Sentiment Analysis",
    description: "Detect sentiment in new customer reviews and assign negative ones to a support team in ClickUp.",
    triggerType: "webhook",
    complexity: "complex"
  },
  {
    name: "Audio to Text Conversion",
    description: "Convert every uploaded audio file in Google Drive into text with AssemblyAI.",
    triggerType: "webhook",
    complexity: "complex"
  },
  {
    name: "AI Instagram Comment Responses",
    description: "Generate AI-written responses to Instagram comments using GPT and send them for manual approval.",
    triggerType: "webhook",
    complexity: "complex"
  },
  {
    name: "Podcast Multi-Language Translation",
    description: "Transcribe and translate uploaded podcast audio to multiple languages automatically.",
    triggerType: "webhook",
    complexity: "complex"
  },
  {
    name: "Computer Vision Object Detection",
    description: "Use computer vision to detect objects in uploaded images via the Hugging Face API.",
    triggerType: "webhook",
    complexity: "complex"
  },
  {
    name: "AI Document Classification",
    description: "Automatically classify documents stored in a folder by type using OpenAI.",
    triggerType: "webhook",
    complexity: "complex"
  },

  // E-commerce & Payment (31-40)
  {
    name: "Stripe to QuickBooks Invoice",
    description: "Automatically create an invoice in QuickBooks when a payment is received via Stripe.",
    triggerType: "webhook",
    complexity: "medium"
  },
  {
    name: "WooCommerce Inventory Alert",
    description: "Send a Telegram alert when low inventory is detected in WooCommerce.",
    triggerType: "webhook",
    complexity: "medium"
  },
  {
    name: "Shopify to CRM Integration",
    description: "Add new Shopify customers to a CRM system like Pipedrive.",
    triggerType: "webhook",
    complexity: "medium"
  },
  {
    name: "Razorpay Sales Summary",
    description: "Generate daily sales summaries from Razorpay transactions and email them as PDFs.",
    triggerType: "schedule",
    complexity: "complex"
  },
  {
    name: "WooCommerce SMS Confirmation",
    description: "Auto-send SMS confirmation to customers for every new WooCommerce order.",
    triggerType: "webhook",
    complexity: "medium"
  },
  {
    name: "Refund Slack Notification",
    description: "When a refund is processed, notify the finance team via Slack.",
    triggerType: "webhook",
    complexity: "medium"
  },
  {
    name: "PayPal Transaction Logging",
    description: "Store all PayPal transaction logs in Google Sheets for bookkeeping.",
    triggerType: "webhook",
    complexity: "medium"
  },
  {
    name: "Discord Big Order Alert",
    description: "Post a message in Discord when a big order (over ₹10,000) is placed.",
    triggerType: "webhook",
    complexity: "medium"
  },
  {
    name: "AI Thank You for Reviews",
    description: "Auto-generate a thank-you note using GPT when a customer leaves a 5-star review.",
    triggerType: "webhook",
    complexity: "complex"
  },
  {
    name: "E-commerce Data Backup",
    description: "Backup all e-commerce order data to Airtable every night.",
    triggerType: "schedule",
    complexity: "complex"
  },

  // Developer & API (41-50)
  {
    name: "API Endpoint Monitoring",
    description: "Monitor an API endpoint every 10 minutes and trigger an alert if response time exceeds 2 seconds.",
    triggerType: "schedule",
    complexity: "complex"
  },
  {
    name: "GitHub Auto-Deploy",
    description: "Automatically deploy a GitHub repository through a webhook when new code is pushed to main.",
    triggerType: "webhook",
    complexity: "complex"
  },
  {
    name: "API Usage Reports",
    description: "Generate and send API usage reports weekly to developers via email.",
    triggerType: "schedule",
    complexity: "complex"
  },
  {
    name: "JSON API to MongoDB",
    description: "Connect n8n to an external JSON API and store results in MongoDB.",
    triggerType: "schedule",
    complexity: "complex"
  },
  {
    name: "Jira CI/CD Pipeline Trigger",
    description: "Trigger a CI/CD pipeline whenever a Jira issue is marked as 'Ready for Release'.",
    triggerType: "webhook",
    complexity: "complex"
  },
  {
    name: "API Key Validation Workflow",
    description: "Create a testing workflow to validate an API key across multiple services.",
    triggerType: "webhook",
    complexity: "complex"
  },
  {
    name: "Website Uptime Monitoring",
    description: "Build a workflow that logs uptime metrics of multiple websites and visualizes it in Google Sheets.",
    triggerType: "schedule",
    complexity: "complex"
  },
  {
    name: "Webhook to MySQL Database",
    description: "Parse JSON data from a webhook and automatically populate a MySQL database.",
    triggerType: "webhook",
    complexity: "complex"
  },
  {
    name: "API Error Alert System",
    description: "When an error occurs in an external app API, send an alert with error details to Slack.",
    triggerType: "webhook",
    complexity: "complex"
  },
  {
    name: "API Response Backup System",
    description: "Create a versioned backup system that saves every new API response for auditing.",
    triggerType: "webhook",
    complexity: "complex"
  }
];

async function runFiftyPromptTest() {
  console.log('🚀 Running 50 Prompt Comprehensive Test Suite');
  console.log('Each workflow will be validated for:');
  console.log('  • Node Types & Configuration (25 points)');
  console.log('  • Connection Validity (25 points)');
  console.log('  • Parameter Correctness (20 points)');
  console.log('  • Goal Achievement (20 points)');
  console.log('  • Production Readiness (10 points)');
  console.log('='.repeat(80));

  const validator = new WorkflowValidator();
  const results = await validator.runComprehensiveTest(fiftyPrompts);

  // Additional detailed analysis
  console.log('\n📈 CATEGORY BREAKDOWN');
  console.log('='.repeat(50));

  const categoryStats = {
    'Business & Productivity': { range: [0, 9], passed: 0, total: 10 },
    'Social Media & Marketing': { range: [10, 19], passed: 0, total: 10 },
    'AI & Automation': { range: [20, 29], passed: 0, total: 10 },
    'E-commerce & Payment': { range: [30, 39], passed: 0, total: 10 },
    'Developer & API': { range: [40, 49], passed: 0, total: 10 }
  };

  // Calculate category success rates
  for (const [category, stats] of Object.entries(categoryStats)) {
    for (let i = stats.range[0]; i <= stats.range[1]; i++) {
      if (results.results[i] && results.results[i].passed) {
        stats.passed++;
      }
    }
    const rate = Math.round((stats.passed / stats.total) * 100);
    console.log(`${category}: ${stats.passed}/${stats.total} (${rate}%)`);
  }

  // Complexity analysis
  console.log('\n📊 COMPLEXITY ANALYSIS');
  console.log('='.repeat(50));
  
  const complexityStats = { medium: { passed: 0, total: 0 }, complex: { passed: 0, total: 0 } };
  
  fiftyPrompts.forEach((prompt, index) => {
    const complexity = prompt.complexity;
    complexityStats[complexity].total++;
    if (results.results[index] && results.results[index].passed) {
      complexityStats[complexity].passed++;
    }
  });

  for (const [complexity, stats] of Object.entries(complexityStats)) {
    const rate = Math.round((stats.passed / stats.total) * 100);
    console.log(`${complexity}: ${stats.passed}/${stats.total} (${rate}%)`);
  }

  // Score distribution
  console.log('\n📊 SCORE DISTRIBUTION');
  console.log('='.repeat(50));
  
  const scoreRanges = {
    '90-100': 0, '80-89': 0, '70-79': 0, '60-69': 0, 'Below 60': 0
  };
  
  results.results.forEach(result => {
    if (result.score >= 90) scoreRanges['90-100']++;
    else if (result.score >= 80) scoreRanges['80-89']++;
    else if (result.score >= 70) scoreRanges['70-79']++;
    else if (result.score >= 60) scoreRanges['60-69']++;
    else scoreRanges['Below 60']++;
  });

  for (const [range, count] of Object.entries(scoreRanges)) {
    console.log(`${range}: ${count} workflows`);
  }

  return results;
}

// Run the test
if (require.main === module) {
  runFiftyPromptTest().then(results => {
    const passRate = (results.summary.passedTests / results.summary.totalTests) * 100;
    console.log(`\n🎯 FINAL VERDICT: ${passRate.toFixed(1)}% Pass Rate`);
    
    if (passRate >= 90) {
      console.log('🎉 EXCELLENT - Production ready!');
    } else if (passRate >= 80) {
      console.log('✅ GOOD - Minor improvements needed');
    } else if (passRate >= 70) {
      console.log('⚠️ ACCEPTABLE - Some issues to address');
    } else {
      console.log('❌ NEEDS WORK - Major improvements required');
    }
    
    process.exit(0);
  }).catch(error => {
    console.error('Test error:', error);
    process.exit(1);
  });
}

module.exports = { fiftyPrompts, runFiftyPromptTest };