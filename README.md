# Perfect n8n Workflow Generator

A powerful web-based application that generates production-ready n8n workflow JSON configurations using AI assistance and intelligent fallback mechanisms.

## 📦 Size Optimized

This project has been optimized to stay under 100MB by:
- Excluding large trained model files (can be regenerated)
- Removing node_modules (run `npm install` to restore)
- Excluding test result files and temporary data
- Using fallback mechanisms when models aren't available

## Features

- **AI-Powered Generation**: Uses Google's Gemini 2.5 API for intelligent workflow creation
- **Fallback System**: Reliable local generation when AI services are unavailable
- **Multiple Trigger Types**: Support for webhook, schedule, and manual triggers
- **Complexity Levels**: Simple (2-3 nodes), Medium (4-6 nodes), Complex (7+ nodes)
- **Pre-built Templates**: Common automation scenarios ready to use
- **Real-time Validation**: Ensures generated workflows are n8n-compatible
- **Export Options**: Copy to clipboard or download as JSON file
- **Responsive Design**: Works on desktop and mobile devices

## Quick Start

1. **Clone or download** this repository
2. **Install dependencies** (if using Node.js features):
   ```bash
   npm install
   ```
3. **Regenerate models** (optional, for enhanced AI features):
   ```bash
   python regenerate_models.py
   ```
4. **Open `index.html`** in your web browser
5. **Configure API Key** (optional):
   - Edit `script.js`
   - Replace `YOUR_GEMINI_API_KEY` with your actual Gemini API key
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

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

For AI-powered generation, you need a Gemini API key:

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Replace `YOUR_GEMINI_API_KEY` in `script.js`

**Note**: The application works without an API key using the fallback generator.

### Customization

#### Adding New Templates

Edit the `templates` object in `script.js`:

```javascript
'your-template': {
    description: 'Your template description...',
    complexity: 'medium'
}
```

#### Adding New Node Types

Extend the node creation methods in the `PerfectN8nGenerator` class:

```javascript
createYourCustomNode(id, x) {
    return {
        parameters: { /* your parameters */ },
        id: this.generateNodeId(),
        name: 'Your Node Name',
        type: 'n8n-nodes-base.yourNodeType',
        typeVersion: 1,
        position: [x, 300]
    };
}
```

## File Structure

```
├── index.html          # Main HTML file
├── style.css           # Styling and responsive design
├── script.js           # Core application logic
└── README.md           # This file
```

## Browser Compatibility

- **Chrome**: 88+
- **Firefox**: 85+
- **Safari**: 14+
- **Edge**: 88+

## Development

### Local Development

1. **Clone the repository**
2. **Open in your preferred editor**
3. **Use a local server** for development:
   ```bash
   # Python
   python -m http.server 8000
   
   # Node.js
   npx serve .
   
   # PHP
   php -S localhost:8000
   ```

### Testing

The application includes built-in validation for:
- Workflow structure compliance
- Required field validation
- Node connection integrity
- n8n compatibility checks

## Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

## License

MIT License - see LICENSE file for details

## Support

- **Issues**: Report bugs and request features via GitHub Issues
- **Documentation**: Check the n8n documentation for node-specific details
- **Community**: Join the n8n community for workflow automation discussions

## Roadmap

- [ ] Visual workflow editor
- [ ] More integration node types
- [ ] Workflow templates library
- [ ] Advanced error handling patterns
- [ ] Batch workflow generation
- [ ] n8n direct import integration

---

**Made with ❤️ for the n8n automation community**