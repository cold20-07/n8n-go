# N8N Workflow Generator 2.0 🚀

A comprehensive, AI-powered web application that generates production-ready n8n workflow JSON configurations with multi-provider AI support, workflow templates, and advanced validation.

## 📦 Size Optimized

This project has been optimized to stay under 100MB by:
- Excluding large trained model files (can be regenerated)
- Removing node_modules (run `npm install` to restore)
- Excluding test result files and temporary data
- Using fallback mechanisms when models aren't available

## ✨ What's New in 2.0

### 🤖 **Enhanced AI System**
- **Multi-provider support**: Gemini, OpenAI, Claude, Ollama
- **Intelligent fallbacks**: Automatic provider switching
- **Response caching**: Improved performance
- **Cost optimization**: Usage tracking and thresholds

### 📚 **Workflow Template Library**
- **Pre-built templates**: RSS to Social, Email Processing, Data Backup, E-commerce
- **Smart suggestions**: AI-powered template recommendations
- **Easy customization**: One-click template loading
- **Category organization**: Templates organized by use case

### 🔍 **Advanced Validation System**
- **Comprehensive checks**: Structure, connections, security, performance
- **Scoring system**: 0-100 validation score
- **Best practices**: Industry standard recommendations
- **Detailed reports**: Issue categorization and suggestions

### 🎯 **Quick Wins Implemented**
- **Enhanced error handling**: Custom exception classes
- **Rate limiting**: Per-endpoint limits with Redis support
- **Security hardening**: Input validation and CORS
- **Performance optimization**: Caching and connection pooling

## 🚀 Features

- **AI-Powered Generation**: Multi-provider AI with intelligent fallbacks
- **Template Library**: 4+ pre-built templates for common scenarios
- **Advanced Validation**: Comprehensive workflow analysis and scoring
- **Multiple Trigger Types**: Webhook, schedule, manual, and email triggers
- **Complexity Levels**: Simple (2-3 nodes), Medium (4-6 nodes), Complex (7+ nodes)
- **Real-time Validation**: Ensures generated workflows are n8n-compatible
- **Rate Limiting**: Prevents abuse with configurable limits
- **Caching**: Redis-based caching for improved performance
- **Export Options**: Copy to clipboard or download as JSON file
- **Responsive Design**: Works on desktop and mobile devices

## Quick Start

### Option 1: Frontend Only (Simple)
1. **Clone or download** this repository
2. **Open `index.html`** in your web browser (automatically redirects to `public/index.html`)
3. **Start using** the workflow generator immediately with fallback generation

### Option 2: Full Stack (Recommended)
1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   # Python dependencies
   pip install -r requirements.txt
   
   # Node.js dependencies (optional)
   npm install
   ```
3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```
4. **Start the server**:
   ```bash
   python app.py
   ```
5. **Open** http://localhost:5000 in your browser

### API Key Configuration (Optional)
- **Gemini**: Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **OpenAI**: Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- **Claude**: Get your API key from [Anthropic Console](https://console.anthropic.com/)

**Note**: The application works without API keys using the fallback generator.

## Usage

### Basic Workflow Generation

1. **Describe your workflow** in the text area
2. **Select trigger type**: Webhook, Schedule, or Manual
3. **Choose complexity level**: Simple, Medium, or Complex
4. **Click "Generate Workflow"**
5. **Copy or download** the generated JSON

### Using Templates

1. **Select a template** from the dropdown:
   - Lead Processing
   - Data Synchronization
   - Notification System
   - API Integration
   - Webhook to Database
2. **Customize the description** if needed
3. **Generate and export** your workflow

### Example Workflows

#### Simple Webhook to Database
```
Description: "Receive customer data via webhook and store it in a MySQL database"
Trigger: Webhook
Complexity: Simple
```

#### Complex Lead Processing
```
Description: "Process incoming leads, validate data, enrich with external APIs, and notify sales team via Slack"
Trigger: Webhook
Complexity: Complex
```

## Supported n8n Node Types

- **Triggers**: Webhook, Schedule, Manual
- **HTTP**: HTTP Request, Respond to Webhook
- **Processing**: Code (JavaScript), Set (Data manipulation)
- **Logic**: IF (Conditional logic)
- **Integrations**: Slack, Gmail
- **And more**: Extensible architecture for additional node types

## Configuration

### API Key Setup (Optional)

For enhanced AI-powered generation, configure your API keys:

1. **Copy environment template**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file** with your API keys:
   ```bash
   GEMINI_API_KEY=your-gemini-api-key
   OPENAI_API_KEY=your-openai-api-key
   CLAUDE_API_KEY=your-claude-api-key
   ```

3. **Get API keys**:
   - [Google AI Studio](https://makersuite.google.com/app/apikey) for Gemini
   - [OpenAI Platform](https://platform.openai.com/api-keys) for GPT
   - [Anthropic Console](https://console.anthropic.com/) for Claude

**Note**: The application works without API keys using the fallback generator.

### Customization

#### Adding New Templates

Edit the templates in `src/templates/workflow_templates.py` or `training_data/workflow_templates.json`:

```python
# In src/templates/workflow_templates.py
WORKFLOW_TEMPLATES = {
    "your-template": {
        "name": "Your Template Name",
        "description": "Your template description...",
        "complexity": "medium",
        "category": "integration",
        "nodes": ["webhook", "set", "http-request"]
    }
}
```

Or in JSON format (`training_data/workflow_templates.json`):
```json
{
  "your-template": {
    "name": "Your Template Name",
    "description": "Your template description...",
    "complexity": "medium",
    "category": "integration",
    "nodes": ["webhook", "set", "http-request"]
  }
}
```

#### Adding New Node Types

Extend the node creation methods in one of the generator files:
- `src/core/generators/enhanced_workflow_generator.py`
- `src/core/generators/feature_aware_workflow_generator.py`
- `src/core/generators/trained_workflow_generator.py`

```python
def create_your_custom_node(self, node_id: str, position: List[int]) -> Dict:
    return {
        'parameters': {
            # your parameters
        },
        'id': node_id,
        'name': 'Your Node Name',
        'type': 'n8n-nodes-base.yourNodeType',
        'typeVersion': 1,
        'position': position
    }
```

## File Structure

```
├── index.html                    # Root entry point (redirects)
├── script.js                     # Compatibility layer
├── style.css                     # Compatibility layer
├── app.py                        # Flask application
├── requirements.txt              # Python dependencies
├── package.json                  # Node.js dependencies
├── .env.example                  # Environment template
├── LICENSE                       # MIT License
├── CONTRIBUTING.md               # Contribution guidelines
├── public/                       # Public web files
│   ├── index.html               # Main HTML application
│   ├── documentation.html
│   └── pricing.html
├── static/                       # Static assets
│   ├── css/
│   │   └── style.css           # Main styles
│   └── js/
│       ├── main.js             # Core application logic
│       └── enhanced-main.js    # Enhanced version
├── src/                          # Python backend modules
│   ├── core/
│   │   ├── generators/         # Workflow generators
│   │   ├── models/             # Data models
│   │   └── validators/         # Validation logic
│   ├── api/                    # API endpoints
│   ├── templates/              # Workflow templates
│   └── utils/                  # Utility functions
├── templates/                    # Flask HTML templates
├── config/                       # Configuration files
│   └── security.py             # Security settings
├── docs/                         # Documentation
│   ├── API.md                  # API documentation
│   └── DEPLOYMENT.md           # Deployment guide
├── tests/                        # Test suites
│   ├── unit/                   # Unit tests
│   └── integration/            # Integration tests
├── training_data/                # AI training data
│   └── workflow_templates.json # Template definitions
├── scripts/                      # Utility scripts
├── api/                          # API configuration
└── .github/                      # GitHub templates
    ├── ISSUE_TEMPLATE/
    └── pull_request_template.md
```

## Browser Compatibility

- **Chrome**: 88+
- **Firefox**: 85+
- **Safari**: 14+
- **Edge**: 88+

## Development

### Local Development

1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   npm install
   ```
3. **Set up environment**:
   ```bash
   cp .env.example .env
   # Configure your API keys in .env
   ```
4. **Start development server**:
   ```bash
   # Full stack development (recommended)
   npm run dev
   # or
   python app.py --debug
   
   # Frontend only (limited functionality)
   npm run serve
   # or
   npx serve . --listen 127.0.0.1:8000
   ```
5. **Run tests**:
   ```bash
   # All tests (Python + JS)
   npm test
   
   # Python tests only
   python -m pytest tests/ -v
   
   # JavaScript tests only
   npm run test:js
   
   # Validation tests
   npm run validate
   ```

### Testing

The application includes comprehensive testing:

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/unit/ -v          # Unit tests
python -m pytest tests/integration/ -v   # Integration tests

# Run with coverage
python -m pytest tests/ --cov=src/ --cov-report=html

# Frontend tests
npm run test:js
```

**Test Coverage**:
- Workflow structure compliance
- Required field validation
- Node connection integrity
- n8n compatibility checks
- API endpoint testing
- Rate limiting validation

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

**Quick Steps**:
1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** with tests
4. **Run the test suite**: 
   ```bash
   npm test                    # All tests
   npm run lint               # Code linting
   npm run format             # Code formatting
   ```
5. **Submit a pull request** with a clear description

**Development Setup**:
```bash
# Clone your fork
git clone https://github.com/your-username/perfect-n8n-workflow-generator.git

# Install dependencies
pip install -r requirements.txt
npm install

# Run tests
python -m pytest tests/ -v
```

## Architecture

### Frontend
- **HTML/CSS/JavaScript**: Modern, responsive web interface
- **Progressive Enhancement**: Works without JavaScript
- **Accessibility**: WCAG 2.1 AA compliant
- **Mobile-First**: Optimized for all devices

### Backend
- **Flask**: Python web framework
- **Multi-AI Integration**: Gemini, OpenAI, Claude, Ollama
- **Redis**: Caching and rate limiting
- **Validation Engine**: Comprehensive workflow validation
- **RESTful API**: Clean, documented endpoints

### Deployment
- **Docker**: Containerized deployment
- **Vercel**: Serverless deployment option
- **Traditional**: VPS/dedicated server support
- **CI/CD**: GitHub Actions pipeline

## API Documentation

See [API Documentation](docs/API.md) for detailed endpoint information.

**Quick Example**:
```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Send daily reports via email",
    "trigger_type": "schedule",
    "complexity": "simple"
  }'
```

## Deployment

See [Deployment Guide](docs/DEPLOYMENT.md) for detailed deployment instructions.

**Quick Deploy Options**:
- **Vercel**: `vercel --prod`
- **Docker**: `docker-compose up -d`
- **Traditional**: `gunicorn -w 4 -b 0.0.0.0:5000 app:app`

## License

MIT License - see [LICENSE](LICENSE) file for details

## Support

- **🐛 Bug Reports**: [Create an issue](https://github.com/your-username/perfect-n8n-workflow-generator/issues/new?template=bug_report.md)
- **✨ Feature Requests**: [Request a feature](https://github.com/your-username/perfect-n8n-workflow-generator/issues/new?template=feature_request.md)
- **📚 Documentation**: Check our [docs](docs/) and [n8n documentation](https://docs.n8n.io/)
- **💬 Community**: Join the [n8n community](https://community.n8n.io/) for workflow automation discussions
- **🚀 Deployment Help**: See our [Deployment Guide](docs/DEPLOYMENT.md)

## Roadmap

- [ ] Visual workflow editor
- [ ] More integration node types
- [ ] Workflow templates library
- [ ] Advanced error handling patterns
- [ ] Batch workflow generation
- [ ] n8n direct import integration

---

**Made with ❤️ for the n8n automation community**