const apiHandler = require('./api/index.js');

async function testSingleWorkflow() {
  const mockReq = {
    method: 'POST',
    url: '/generate',
    body: JSON.stringify({
      description: "Create a workflow that automatically sends a Slack message when a new lead is added to Google Sheets.",
      triggerType: 'webhook',
      complexity: 'medium'
    })
  };

  let responseData = null;
  const mockRes = {
    setHeader: () => {},
    status: (code) => mockRes,
    json: (data) => { responseData = data; return mockRes; },
    end: () => {}
  };

  await apiHandler(mockReq, mockRes);
  
  if (responseData?.success) {
    console.log('Workflow generated successfully!');
    console.log('Nodes:', responseData.workflow.nodes.map(n => ({ name: n.name, type: n.type, params: Object.keys(n.parameters || {}) })));
    console.log('Services detected:', responseData.workflow.meta.services_detected);
  } else {
    console.log('Failed to generate workflow');
  }
}

testSingleWorkflow();