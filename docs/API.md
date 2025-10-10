# API Documentation

## Base URL
- Development: `http://localhost:5000`
- Production: `https://your-domain.com`

## Authentication
Currently, no authentication is required for public endpoints.

## Rate Limiting
- **Default**: 100 requests per hour per IP
- **Burst**: 10 requests per minute
- **Headers**: Rate limit info included in response headers

## Endpoints

### Generate Workflow
Generate an n8n workflow from a text description.

**Endpoint:** `POST /api/generate`

**Request Body:**
```json
{
  "description": "Process incoming webhooks and save to database",
  "trigger_type": "webhook",
  "complexity": "medium",
  "template": "webhook-to-database"
}
```

**Parameters:**
- `description` (string, required): Workflow description (10-1000 characters)
- `trigger_type` (string, optional): One of `webhook`, `schedule`, `manual`, `email`
- `complexity` (string, optional): One of `simple`, `medium`, `complex`
- `template` (string, optional): Template name to use as base

**Response:**
```json
{
  "success": true,
  "workflow": {
    "name": "Generated Workflow",
    "nodes": [...],
    "connections": {...},
    "settings": {...}
  },
  "validation": {
    "score": 95,
    "issues": [],
    "suggestions": [...]
  },
  "metadata": {
    "generated_at": "2024-01-01T12:00:00Z",
    "complexity": "medium",
    "node_count": 5
  }
}
```

### Validate Workflow
Validate an existing n8n workflow.

**Endpoint:** `POST /api/validate`

**Request Body:**
```json
{
  "workflow": {
    "name": "My Workflow",
    "nodes": [...],
    "connections": {...}
  }
}
```

**Response:**
```json
{
  "valid": true,
  "score": 85,
  "issues": [
    {
      "type": "warning",
      "message": "Node 'HTTP Request' missing error handling",
      "node_id": "node_123",
      "severity": "medium"
    }
  ],
  "suggestions": [
    "Add error handling to HTTP Request nodes",
    "Consider adding data validation"
  ]
}
```

### Get Templates
Retrieve available workflow templates.

**Endpoint:** `GET /api/templates`

**Response:**
```json
{
  "templates": [
    {
      "id": "webhook-to-database",
      "name": "Webhook to Database",
      "description": "Process webhooks and store data",
      "category": "data-processing",
      "complexity": "simple",
      "nodes": ["webhook", "set", "mysql"]
    }
  ]
}
```

### Health Check
Check API health status.

**Endpoint:** `GET /api/health`

**Response:**
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "uptime": 3600,
  "checks": {
    "database": "ok",
    "ai_service": "ok",
    "cache": "ok"
  }
}
```

## Error Responses

All endpoints return errors in this format:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Description must be between 10 and 1000 characters",
    "details": {
      "field": "description",
      "provided_length": 5,
      "min_length": 10
    }
  }
}
```

### Error Codes
- `VALIDATION_ERROR`: Invalid input parameters
- `RATE_LIMIT_EXCEEDED`: Too many requests
- `AI_SERVICE_ERROR`: AI provider unavailable
- `INTERNAL_ERROR`: Server error
- `TEMPLATE_NOT_FOUND`: Requested template doesn't exist

## Response Headers

### Rate Limiting Headers
- `X-RateLimit-Limit`: Request limit per window
- `X-RateLimit-Remaining`: Requests remaining in window
- `X-RateLimit-Reset`: Time when limit resets (Unix timestamp)

### Cache Headers
- `Cache-Control`: Caching policy
- `ETag`: Response version identifier

## SDKs and Examples

### JavaScript/Node.js
```javascript
const response = await fetch('/api/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    description: 'Send daily reports via email',
    trigger_type: 'schedule',
    complexity: 'simple'
  })
});

const result = await response.json();
```

### Python
```python
import requests

response = requests.post('/api/generate', json={
    'description': 'Process customer feedback forms',
    'trigger_type': 'webhook',
    'complexity': 'medium'
})

workflow = response.json()
```

### cURL
```bash
curl -X POST /api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Sync data between systems",
    "trigger_type": "schedule",
    "complexity": "complex"
  }'
```

## Webhooks (Future)
Planned webhook support for workflow events:
- Workflow generated
- Validation completed
- Template updated

## Changelog
- **v2.0.0**: Multi-provider AI, templates, advanced validation
- **v1.0.0**: Initial release with basic generation