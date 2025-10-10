# Contributing to N8N Workflow Generator 2.0

Thank you for your interest in contributing! This guide will help you get started.

## Quick Start

1. **Fork the repository**
2. **Clone your fork**: `git clone https://github.com/your-username/perfect-n8n-workflow-generator.git`
3. **Install dependencies**: `npm install && pip install -r requirements.txt`
4. **Run tests**: `npm test && python -m pytest`
5. **Start development server**: `python app.py --debug`

## Development Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- Git

### Environment Setup
```bash
# Copy environment template
cp .env.example .env

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
npm install

# Run setup script
python scripts/setup.py
```

## Project Structure

```
├── src/                 # Core Python modules
├── static/             # Frontend assets (CSS, JS)
├── templates/          # HTML templates
├── public/             # Public web files
├── tests/              # Test suites
├── api/                # API endpoints
├── config/             # Configuration files
└── scripts/            # Utility scripts
```

## Making Changes

### Code Style
- **Python**: Follow PEP 8, use `black` for formatting
- **JavaScript**: Use ES6+, follow Airbnb style guide
- **HTML/CSS**: Use semantic HTML, mobile-first CSS

### Testing
```bash
# Run all tests
npm test

# Run Python tests only
python -m pytest tests/ -v

# Run JavaScript tests only
npm run test:js

# Run with coverage
python -m pytest tests/ --cov=src/
```

### Commit Guidelines
Use conventional commits:
- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation changes
- `style:` formatting changes
- `refactor:` code refactoring
- `test:` adding tests
- `chore:` maintenance tasks

Example: `feat: add template validation system`

## Types of Contributions

### 🐛 Bug Reports
- Use the bug report template
- Include steps to reproduce
- Provide system information
- Add relevant logs/screenshots

### ✨ Feature Requests
- Use the feature request template
- Explain the use case
- Provide implementation ideas
- Consider backward compatibility

### 🔧 Code Contributions
- Start with an issue discussion
- Keep changes focused and small
- Add tests for new functionality
- Update documentation as needed

### 📚 Documentation
- Fix typos and improve clarity
- Add examples and use cases
- Update API documentation
- Improve setup instructions

## Pull Request Process

1. **Create a feature branch**: `git checkout -b feature/your-feature-name`
2. **Make your changes** with tests
3. **Run the test suite**: `npm test`
4. **Update documentation** if needed
5. **Commit your changes** using conventional commits
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Create a pull request** with a clear description

### PR Checklist
- [ ] Tests pass locally
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
- [ ] Commit messages follow convention

## Development Guidelines

### Adding New Node Types
1. Add node definition in `src/core/nodes/`
2. Update the generator in `src/core/generator.py`
3. Add validation rules in `src/validators/`
4. Include tests in `tests/unit/`
5. Update documentation

### Adding New Templates
1. Define template in `src/templates/`
2. Add to template registry
3. Include validation tests
4. Update UI dropdown
5. Add documentation example

### API Changes
1. Update OpenAPI spec if applicable
2. Maintain backward compatibility
3. Add integration tests
4. Update client documentation

## Testing Strategy

### Unit Tests
- Test individual functions/classes
- Mock external dependencies
- Aim for 80%+ coverage

### Integration Tests
- Test API endpoints
- Test workflow generation end-to-end
- Test template loading

### Frontend Tests
- Test UI interactions
- Test form validation
- Test workflow display

## Performance Guidelines

- Keep bundle sizes small
- Optimize API response times
- Use caching where appropriate
- Monitor memory usage
- Profile critical paths

## Security Considerations

- Validate all inputs
- Sanitize user data
- Use HTTPS in production
- Follow OWASP guidelines
- Report security issues privately

## Getting Help

- **Questions**: Open a discussion
- **Bugs**: Create an issue
- **Chat**: Join our community (link in README)
- **Email**: Contact maintainers directly

## Recognition

Contributors are recognized in:
- README.md contributors section
- Release notes
- Annual contributor highlights

Thank you for contributing to make n8n workflow generation better for everyone! 🚀