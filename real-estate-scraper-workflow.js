#!/usr/bin/env node
/**
 * Real Estate Scraper → Cold Email → Sheets Workflow Generator
 * Creates a comprehensive n8n workflow for real estate lead generation
 */

const crypto = require('crypto');

function generateNodeId() {
  return crypto.randomBytes(8).toString('hex');
}

function createRealEstateScraperWorkflow() {
  const workflowId = `real_estate_scraper_${Date.now()}`;
  
  const workflow = {
    id: workflowId,
    name: "Real Estate Scraper → Cold Email → Sheets",
    active: false,
    nodes: [],
    connections: {},
    settings: {
      executionOrder: "v1",
      saveManualExecutions: true,
      callerPolicy: "workflowsFromSameOwner"
    },
    tags: ["real-estate", "scraping", "email", "sheets", "automation"],
    meta: {
      generated_by: "n8n-workflow-generator",
      complexity: "complex",
      created_at: new Date().toISOString(),
      description: "Scrapes real estate listings, sends cold emails, and tracks results in Google Sheets"
    }
  };

  // 1. Manual Trigger with Configuration
  const manualTrigger = {
    parameters: {
      manualTriggerConfiguration: "once"
    },
    id: generateNodeId(),
    name: "Manual Trigger",
    type: "n8n-nodes-base.manualTrigger",
    typeVersion: 1,
    position: [240, 300],
    onError: "continueRegularOutput"
  };

  // 2. Initialize Configuration
  const initConfig = {
    parameters: {
      jsCode: `// Initialize Real Estate Scraper Configuration
const config = {
  target_urls: [
    "https://example-realestate.com/listings",
    "https://another-site.com/properties"
  ],
  filters: {
    location: "San Francisco, CA",
    type: "apartment",
    price_min: 500000,
    price_max: 2000000,
    bedrooms_min: 2
  },
  pagination: {
    start_page: 1,
    end_page: 5,
    page_param: "page"
  },
  email_config: {
    from_name: "Real Estate Investor",
    from_email: "investor@example.com",
    subject_tpl: "Investment Opportunity - {{title}}",
    html_tpl: \`<h2>Hello {{agent_name}},</h2>
    <p>I'm interested in your listing: <strong>{{title}}</strong></p>
    <p>Location: {{location}}</p>
    <p>Price: {{price}}</p>
    <p>Please contact me to discuss this opportunity.</p>
    <p>Best regards,<br>{{from_name}}</p>\`,
    text_tpl: \`Hello {{agent_name}},
    
I'm interested in your listing: {{title}}
Location: {{location}}
Price: {{price}}

Please contact me to discuss this opportunity.

Best regards,
{{from_name}}\`
  },
  batching: {
    size: 10,
    wait_ms: 2000
  },
  sheets: {
    spreadsheet_id: "1ABC123DEF456GHI789JKL",
    sheet_name: "Real Estate Leads"
  }
};

return [{ json: config }];`
    },
    id: generateNodeId(),
    name: "Initialize Configuration",
    type: "n8n-nodes-base.code",
    typeVersion: 2,
    position: [460, 300],
    onError: "continueRegularOutput"
  };

  // 3. Generate Page URLs
  const generatePageUrls = {
    parameters: {
      jsCode: `// Generate URLs for each page to scrape
const config = $input.first().json;
const pageUrls = [];

for (const baseUrl of config.target_urls) {
  for (let page = config.pagination.start_page; page <= config.pagination.end_page; page++) {
    const url = new URL(baseUrl);
    url.searchParams.set(config.pagination.page_param, page);
    
    // Add filters to URL
    if (config.filters.location) url.searchParams.set('location', config.filters.location);
    if (config.filters.type) url.searchParams.set('type', config.filters.type);
    if (config.filters.price_min) url.searchParams.set('price_min', config.filters.price_min);
    if (config.filters.price_max) url.searchParams.set('price_max', config.filters.price_max);
    if (config.filters.bedrooms_min) url.searchParams.set('bedrooms_min', config.filters.bedrooms_min);
    
    pageUrls.push({
      url: url.toString(),
      page: page,
      base_url: baseUrl,
      config: config
    });
  }
}

return pageUrls.map(item => ({ json: item }));`
    },
    id: generateNodeId(),
    name: "Generate Page URLs",
    type: "n8n-nodes-base.code",
    typeVersion: 2,
    position: [680, 300],
    onError: "continueRegularOutput"
  };

  // 4. Split Pages into Batches
  const splitPageBatches = {
    parameters: {
      batchSize: "={{ $('Initialize Configuration').first().json.batching.size }}",
      options: {}
    },
    id: generateNodeId(),
    name: "Split Pages into Batches",
    type: "n8n-nodes-base.splitInBatches",
    typeVersion: 3,
    position: [900, 300],
    onError: "continueRegularOutput"
  };

  // 5. HTTP Request for Listings Page
  const httpRequestListings = {
    parameters: {
      method: "GET",
      url: "={{ $json.url }}",
      options: {
        timeout: 30000,
        retry: {
          enabled: true,
          maxTries: 3
        },
        headers: {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
      }
    },
    id: generateNodeId(),
    name: "HTTP Request - Listings Page",
    type: "n8n-nodes-base.httpRequest",
    typeVersion: 4.2,
    position: [1120, 300],
    retryOnFail: true,
    maxTries: 3,
    waitBetweenTries: 2000,
    onError: "continueRegularOutput"
  };

  // 6. HTML Extract Listings
  const htmlExtractListings = {
    parameters: {
      operation: "extractHtml",
      extractionValues: {
        values: [
          {
            key: "listings",
            cssSelector: ".listing-item, .property-card, .listing",
            returnArray: true,
            returnValue: "outerHTML"
          }
        ]
      },
      options: {}
    },
    id: generateNodeId(),
    name: "HTML Extract - Listings",
    type: "n8n-nodes-base.html",
    typeVersion: 1,
    position: [1340, 300],
    onError: "continueRegularOutput"
  };

  // 7. Process Individual Listings
  const processListings = {
    parameters: {
      jsCode: `// Process individual listings and extract basic data
const pageData = $input.first().json;
const config = $('Generate Page URLs').first().json.config;
const listings = pageData.listings || [];

const processedListings = [];

for (const listingHtml of listings) {
  try {
    // Parse HTML to extract listing data
    const parser = new DOMParser();
    const doc = parser.parseFromString(listingHtml, 'text/html');
    
    // Extract basic listing information
    const listing = {
      listing_url: doc.querySelector('a[href*="/listing/"], a[href*="/property/"]')?.href || '',
      title: doc.querySelector('.title, .property-title, h3, h4')?.textContent?.trim() || '',
      price: doc.querySelector('.price, .property-price')?.textContent?.trim() || '',
      location: doc.querySelector('.location, .address')?.textContent?.trim() || '',
      bedrooms: doc.querySelector('.bedrooms, .beds')?.textContent?.trim() || '',
      bathrooms: doc.querySelector('.bathrooms, .baths')?.textContent?.trim() || '',
      area_sqft: doc.querySelector('.area, .sqft')?.textContent?.trim() || '',
      // Agent info will be extracted from detail page
      agent_name: '',
      agent_email: '',
      agent_phone: '',
      posted_date: doc.querySelector('.date, .posted')?.textContent?.trim() || '',
      source_page: pageData.url || $json.url,
      config: config
    };
    
    // Only include listings with valid URLs
    if (listing.listing_url && listing.title) {
      processedListings.push(listing);
    }
  } catch (error) {
    console.error('Error processing listing:', error);
  }
}

return processedListings.map(listing => ({ json: listing }));`
    },
    id: generateNodeId(),
    name: "Process Individual Listings",
    type: "n8n-nodes-base.code",
    typeVersion: 2,
    position: [1560, 300],
    onError: "continueRegularOutput"
  };

  // 8. HTTP Request for Detail Page
  const httpRequestDetail = {
    parameters: {
      method: "GET",
      url: "={{ $json.listing_url }}",
      options: {
        timeout: 30000,
        retry: {
          enabled: true,
          maxTries: 2
        },
        headers: {
          "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
      }
    },
    id: generateNodeId(),
    name: "HTTP Request - Detail Page",
    type: "n8n-nodes-base.httpRequest",
    typeVersion: 4.2,
    position: [1780, 300],
    retryOnFail: true,
    maxTries: 2,
    waitBetweenTries: 1000,
    onError: "continueRegularOutput"
  };

  // 9. HTML Extract Agent Contact
  const htmlExtractAgent = {
    parameters: {
      operation: "extractHtml",
      extractionValues: {
        values: [
          {
            key: "agent_name",
            cssSelector: ".agent-name, .contact-name, .realtor-name",
            returnValue: "text"
          },
          {
            key: "agent_email",
            cssSelector: "a[href^='mailto:'], .agent-email, .contact-email",
            returnValue: "text"
          },
          {
            key: "agent_phone",
            cssSelector: ".agent-phone, .contact-phone, .phone",
            returnValue: "text"
          }
        ]
      },
      options: {}
    },
    id: generateNodeId(),
    name: "HTML Extract - Agent Contact",
    type: "n8n-nodes-base.html",
    typeVersion: 1,
    position: [2000, 300],
    onError: "continueRegularOutput"
  };

  // 10. Normalize and Set Data
  const normalizeData = {
    parameters: {
      values: {
        listing_url: "={{ $('Process Individual Listings').item.json.listing_url }}",
        title: "={{ $('Process Individual Listings').item.json.title }}",
        price: "={{ $('Process Individual Listings').item.json.price }}",
        location: "={{ $('Process Individual Listings').item.json.location }}",
        bedrooms: "={{ $('Process Individual Listings').item.json.bedrooms }}",
        bathrooms: "={{ $('Process Individual Listings').item.json.bathrooms }}",
        area_sqft: "={{ $('Process Individual Listings').item.json.area_sqft }}",
        agent_name: "={{ $json.agent_name || 'Unknown Agent' }}",
        agent_email: "={{ $json.agent_email }}",
        agent_phone: "={{ $json.agent_phone }}",
        posted_date: "={{ $('Process Individual Listings').item.json.posted_date }}",
        source_page: "={{ $('Process Individual Listings').item.json.source_page }}",
        scraped_at: "={{ $now }}",
        config: "={{ $('Process Individual Listings').item.json.config }}"
      },
      options: {}
    },
    id: generateNodeId(),
    name: "Normalize and Set Data",
    type: "n8n-nodes-base.set",
    typeVersion: 3.4,
    position: [2220, 300],
    onError: "continueRegularOutput"
  };

  // 11. Validate Listing Data
  const validateListing = {
    parameters: {
      conditions: {
        options: {
          caseSensitive: true,
          leftValue: "",
          typeValidation: "strict"
        },
        conditions: [
          {
            id: "valid_url",
            leftValue: "={{ $json.listing_url }}",
            rightValue: "",
            operator: {
              operation: "notEmpty",
              type: "string"
            }
          },
          {
            id: "valid_contact",
            leftValue: "={{ $json.agent_email || $json.agent_phone }}",
            rightValue: "",
            operator: {
              operation: "notEmpty",
              type: "string"
            }
          }
        ],
        combineOperation: "all"
      },
      options: {}
    },
    id: generateNodeId(),
    name: "Validate Listing Data",
    type: "n8n-nodes-base.if",
    typeVersion: 2,
    position: [2440, 300],
    onError: "continueRegularOutput"
  };

  // 12. Check for Duplicates in Sheets
  const checkDuplicates = {
    parameters: {
      authentication: "oAuth2",
      operation: "lookup",
      documentId: "={{ $json.config.sheets.spreadsheet_id }}",
      sheetName: "={{ $json.config.sheets.sheet_name }}",
      lookupColumn: "A", // listing_url column
      lookupValue: "={{ $json.listing_url }}",
      options: {}
    },
    id: generateNodeId(),
    name: "Check for Duplicates",
    type: "n8n-nodes-base.googleSheets",
    typeVersion: 4.4,
    position: [2660, 200], // True branch
    onError: "continueRegularOutput"
  };

  // 13. Filter New Leads
  const filterNewLeads = {
    parameters: {
      conditions: {
        options: {
          caseSensitive: true,
          leftValue: "",
          typeValidation: "strict"
        },
        conditions: [
          {
            id: "not_duplicate",
            leftValue: "={{ $('Check for Duplicates').item.json }}",
            rightValue: "",
            operator: {
              operation: "isEmpty",
              type: "object"
            }
          }
        ],
        combineOperation: "all"
      },
      options: {}
    },
    id: generateNodeId(),
    name: "Filter New Leads",
    type: "n8n-nodes-base.if",
    typeVersion: 2,
    position: [2880, 200],
    onError: "continueRegularOutput"
  };

  // 14. Prepare Email Data
  const prepareEmailData = {
    parameters: {
      jsCode: `// Prepare personalized email data
const listing = $input.first().json;
const config = listing.config;

// Clean and format data
const cleanPrice = listing.price.replace(/[^0-9,.$]/g, '');
const cleanLocation = listing.location.replace(/\\s+/g, ' ').trim();
const agentName = listing.agent_name || 'Real Estate Professional';

// Personalize email templates
const personalizedSubject = config.email_config.subject_tpl
  .replace(/{{title}}/g, listing.title)
  .replace(/{{location}}/g, cleanLocation)
  .replace(/{{price}}/g, cleanPrice);

const personalizedHtml = config.email_config.html_tpl
  .replace(/{{agent_name}}/g, agentName)
  .replace(/{{title}}/g, listing.title)
  .replace(/{{location}}/g, cleanLocation)
  .replace(/{{price}}/g, cleanPrice)
  .replace(/{{from_name}}/g, config.email_config.from_name);

const personalizedText = config.email_config.text_tpl
  .replace(/{{agent_name}}/g, agentName)
  .replace(/{{title}}/g, listing.title)
  .replace(/{{location}}/g, cleanLocation)
  .replace(/{{price}}/g, cleanPrice)
  .replace(/{{from_name}}/g, config.email_config.from_name);

return [{
  json: {
    ...listing,
    email_data: {
      to_email: listing.agent_email,
      to_name: agentName,
      from_email: config.email_config.from_email,
      from_name: config.email_config.from_name,
      subject: personalizedSubject,
      html: personalizedHtml,
      text: personalizedText
    }
  }
}];`
    },
    id: generateNodeId(),
    name: "Prepare Email Data",
    type: "n8n-nodes-base.code",
    typeVersion: 2,
    position: [3100, 100], // True branch from Filter New Leads
    onError: "continueRegularOutput"
  };

  // 15. Send Cold Email
  const sendEmail = {
    parameters: {
      authentication: "predefinedCredentialType",
      nodeCredentialType: "smtp",
      fromEmail: "={{ $json.email_data.from_email }}",
      fromName: "={{ $json.email_data.from_name }}",
      toEmail: "={{ $json.email_data.to_email }}",
      subject: "={{ $json.email_data.subject }}",
      message: "={{ $json.email_data.html }}",
      options: {
        allowUnauthorizedCerts: false,
        ccEmail: "",
        bccEmail: "",
        replyTo: "={{ $json.email_data.from_email }}",
        priority: "normal",
        headers: {}
      }
    },
    id: generateNodeId(),
    name: "Send Cold Email",
    type: "n8n-nodes-base.emailSend",
    typeVersion: 2.1,
    position: [3320, 100],
    retryOnFail: true,
    maxTries: 2,
    waitBetweenTries: 1000,
    onError: "continueRegularOutput"
  };

  // 16. Wait Between Emails
  const waitBetweenEmails = {
    parameters: {
      amount: "={{ $('Normalize and Set Data').item.json.config.batching.wait_ms }}",
      unit: "ms"
    },
    id: generateNodeId(),
    name: "Wait Between Emails",
    type: "n8n-nodes-base.wait",
    typeVersion: 1.1,
    position: [3540, 100],
    onError: "continueRegularOutput"
  };

  // 17. Record Success
  const recordSuccess = {
    parameters: {
      values: {
        listing_url: "={{ $('Prepare Email Data').item.json.listing_url }}",
        agent_email: "={{ $('Prepare Email Data').item.json.agent_email }}",
        agent_name: "={{ $('Prepare Email Data').item.json.agent_name }}",
        title: "={{ $('Prepare Email Data').item.json.title }}",
        location: "={{ $('Prepare Email Data').item.json.location }}",
        price: "={{ $('Prepare Email Data').item.json.price }}",
        bedrooms: "={{ $('Prepare Email Data').item.json.bedrooms }}",
        bathrooms: "={{ $('Prepare Email Data').item.json.bathrooms }}",
        area_sqft: "={{ $('Prepare Email Data').item.json.area_sqft }}",
        agent_phone: "={{ $('Prepare Email Data').item.json.agent_phone }}",
        posted_date: "={{ $('Prepare Email Data').item.json.posted_date }}",
        source_page: "={{ $('Prepare Email Data').item.json.source_page }}",
        status: "email_sent",
        timestamp: "={{ $now }}",
        error: "",
        source: "real_estate_scraper"
      },
      options: {}
    },
    id: generateNodeId(),
    name: "Record Success",
    type: "n8n-nodes-base.set",
    typeVersion: 3.4,
    position: [3760, 100],
    onError: "continueRegularOutput"
  };

  // 18. Record Duplicate
  const recordDuplicate = {
    parameters: {
      values: {
        listing_url: "={{ $('Normalize and Set Data').item.json.listing_url }}",
        agent_email: "={{ $('Normalize and Set Data').item.json.agent_email }}",
        agent_name: "={{ $('Normalize and Set Data').item.json.agent_name }}",
        title: "={{ $('Normalize and Set Data').item.json.title }}",
        location: "={{ $('Normalize and Set Data').item.json.location }}",
        price: "={{ $('Normalize and Set Data').item.json.price }}",
        bedrooms: "={{ $('Normalize and Set Data').item.json.bedrooms }}",
        bathrooms: "={{ $('Normalize and Set Data').item.json.bathrooms }}",
        area_sqft: "={{ $('Normalize and Set Data').item.json.area_sqft }}",
        agent_phone: "={{ $('Normalize and Set Data').item.json.agent_phone }}",
        posted_date: "={{ $('Normalize and Set Data').item.json.posted_date }}",
        source_page: "={{ $('Normalize and Set Data').item.json.source_page }}",
        status: "duplicate_skipped",
        timestamp: "={{ $now }}",
        error: "",
        source: "real_estate_scraper"
      },
      options: {}
    },
    id: generateNodeId(),
    name: "Record Duplicate",
    type: "n8n-nodes-base.set",
    typeVersion: 3.4,
    position: [3100, 300], // False branch from Filter New Leads
    onError: "continueRegularOutput"
  };

  // 19. Record Invalid
  const recordInvalid = {
    parameters: {
      values: {
        listing_url: "={{ $('Normalize and Set Data').item.json.listing_url }}",
        agent_email: "={{ $('Normalize and Set Data').item.json.agent_email }}",
        agent_name: "={{ $('Normalize and Set Data').item.json.agent_name }}",
        title: "={{ $('Normalize and Set Data').item.json.title }}",
        location: "={{ $('Normalize and Set Data').item.json.location }}",
        price: "={{ $('Normalize and Set Data').item.json.price }}",
        bedrooms: "={{ $('Normalize and Set Data').item.json.bedrooms }}",
        bathrooms: "={{ $('Normalize and Set Data').item.json.bathrooms }}",
        area_sqft: "={{ $('Normalize and Set Data').item.json.area_sqft }}",
        agent_phone: "={{ $('Normalize and Set Data').item.json.agent_phone }}",
        posted_date: "={{ $('Normalize and Set Data').item.json.posted_date }}",
        source_page: "={{ $('Normalize and Set Data').item.json.source_page }}",
        status: "invalid_data",
        timestamp: "={{ $now }}",
        error: "Missing required data (URL or contact info)",
        source: "real_estate_scraper"
      },
      options: {}
    },
    id: generateNodeId(),
    name: "Record Invalid",
    type: "n8n-nodes-base.set",
    typeVersion: 3.4,
    position: [2660, 400], // False branch from Validate Listing
    onError: "continueRegularOutput"
  };

  // 20. Merge All Results
  const mergeResults = {
    parameters: {
      mode: "mergeByIndex",
      options: {}
    },
    id: generateNodeId(),
    name: "Merge All Results",
    type: "n8n-nodes-base.merge",
    typeVersion: 3,
    position: [3980, 300],
    onError: "continueRegularOutput"
  };

  // 21. Append to Google Sheets
  const appendToSheets = {
    parameters: {
      authentication: "oAuth2",
      operation: "appendOrUpdate",
      documentId: "={{ $('Initialize Configuration').first().json.sheets.spreadsheet_id }}",
      sheetName: "={{ $('Initialize Configuration').first().json.sheets.sheet_name }}",
      columnToMatchOn: "A", // listing_url
      dataMode: "defineBelow",
      valueInputMode: "raw",
      values: {
        listing_url: "={{ $json.listing_url }}",
        agent_email: "={{ $json.agent_email }}",
        agent_name: "={{ $json.agent_name }}",
        title: "={{ $json.title }}",
        location: "={{ $json.location }}",
        price: "={{ $json.price }}",
        bedrooms: "={{ $json.bedrooms }}",
        bathrooms: "={{ $json.bathrooms }}",
        area_sqft: "={{ $json.area_sqft }}",
        agent_phone: "={{ $json.agent_phone }}",
        posted_date: "={{ $json.posted_date }}",
        source_page: "={{ $json.source_page }}",
        status: "={{ $json.status }}",
        timestamp: "={{ $json.timestamp }}",
        error: "={{ $json.error }}",
        source: "={{ $json.source }}"
      },
      options: {}
    },
    id: generateNodeId(),
    name: "Append to Google Sheets",
    type: "n8n-nodes-base.googleSheets",
    typeVersion: 4.4,
    position: [4200, 300],
    onError: "continueRegularOutput"
  };

  // 22. Generate Summary
  const generateSummary = {
    parameters: {
      jsCode: `// Generate execution summary
const allResults = $input.all();
const summary = {
  total_processed: allResults.length,
  emails_sent: allResults.filter(item => item.json.status === 'email_sent').length,
  duplicates_skipped: allResults.filter(item => item.json.status === 'duplicate_skipped').length,
  invalid_data: allResults.filter(item => item.json.status === 'invalid_data').length,
  execution_time: new Date().toISOString(),
  success_rate: 0
};

summary.success_rate = summary.total_processed > 0 
  ? Math.round((summary.emails_sent / summary.total_processed) * 100) 
  : 0;

console.log('Real Estate Scraper Summary:', summary);

return [{ json: summary }];`
    },
    id: generateNodeId(),
    name: "Generate Summary",
    type: "n8n-nodes-base.code",
    typeVersion: 2,
    position: [4420, 300],
    onError: "continueRegularOutput"
  };

  // Add all nodes to workflow
  workflow.nodes = [
    manualTrigger,
    initConfig,
    generatePageUrls,
    splitPageBatches,
    httpRequestListings,
    htmlExtractListings,
    processListings,
    httpRequestDetail,
    htmlExtractAgent,
    normalizeData,
    validateListing,
    checkDuplicates,
    filterNewLeads,
    prepareEmailData,
    sendEmail,
    waitBetweenEmails,
    recordSuccess,
    recordDuplicate,
    recordInvalid,
    mergeResults,
    appendToSheets,
    generateSummary
  ];

  // Define connections
  workflow.connections = {
    "Manual Trigger": {
      main: [[{ node: "Initialize Configuration", type: "main", index: 0 }]]
    },
    "Initialize Configuration": {
      main: [[{ node: "Generate Page URLs", type: "main", index: 0 }]]
    },
    "Generate Page URLs": {
      main: [[{ node: "Split Pages into Batches", type: "main", index: 0 }]]
    },
    "Split Pages into Batches": {
      main: [[{ node: "HTTP Request - Listings Page", type: "main", index: 0 }]]
    },
    "HTTP Request - Listings Page": {
      main: [[{ node: "HTML Extract - Listings", type: "main", index: 0 }]]
    },
    "HTML Extract - Listings": {
      main: [[{ node: "Process Individual Listings", type: "main", index: 0 }]]
    },
    "Process Individual Listings": {
      main: [[{ node: "HTTP Request - Detail Page", type: "main", index: 0 }]]
    },
    "HTTP Request - Detail Page": {
      main: [[{ node: "HTML Extract - Agent Contact", type: "main", index: 0 }]]
    },
    "HTML Extract - Agent Contact": {
      main: [[{ node: "Normalize and Set Data", type: "main", index: 0 }]]
    },
    "Normalize and Set Data": {
      main: [[{ node: "Validate Listing Data", type: "main", index: 0 }]]
    },
    "Validate Listing Data": {
      main: [
        [{ node: "Check for Duplicates", type: "main", index: 0 }], // True
        [{ node: "Record Invalid", type: "main", index: 0 }] // False
      ]
    },
    "Check for Duplicates": {
      main: [[{ node: "Filter New Leads", type: "main", index: 0 }]]
    },
    "Filter New Leads": {
      main: [
        [{ node: "Prepare Email Data", type: "main", index: 0 }], // True (new lead)
        [{ node: "Record Duplicate", type: "main", index: 0 }] // False (duplicate)
      ]
    },
    "Prepare Email Data": {
      main: [[{ node: "Send Cold Email", type: "main", index: 0 }]]
    },
    "Send Cold Email": {
      main: [[{ node: "Wait Between Emails", type: "main", index: 0 }]]
    },
    "Wait Between Emails": {
      main: [[{ node: "Record Success", type: "main", index: 0 }]]
    },
    "Record Success": {
      main: [[{ node: "Merge All Results", type: "main", index: 0 }]]
    },
    "Record Duplicate": {
      main: [[{ node: "Merge All Results", type: "main", index: 1 }]]
    },
    "Record Invalid": {
      main: [[{ node: "Merge All Results", type: "main", index: 2 }]]
    },
    "Merge All Results": {
      main: [[{ node: "Append to Google Sheets", type: "main", index: 0 }]]
    },
    "Append to Google Sheets": {
      main: [[{ node: "Generate Summary", type: "main", index: 0 }]]
    }
  };

  return workflow;
}

// Generate and export the workflow
const workflow = createRealEstateScraperWorkflow();

// Export to file
const fs = require('fs');
fs.writeFileSync('real-estate-scraper-workflow.json', JSON.stringify(workflow, null, 2));

console.log('✅ Real Estate Scraper workflow generated successfully!');
console.log('📁 File: real-estate-scraper-workflow.json');
console.log(`📊 Nodes: ${workflow.nodes.length}`);
console.log(`🔗 Connections: ${Object.keys(workflow.connections).length}`);

module.exports = { createRealEstateScraperWorkflow };