// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add scroll effect to header
window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    if (window.scrollY > 100) {
        header.style.background = 'rgba(26, 26, 26, 0.95)';
        header.style.backdropFilter = 'blur(10px)';
    } else {
        header.style.background = 'transparent';
        header.style.backdropFilter = 'none';
    }
});

// Add intersection observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe feature cards
document.querySelectorAll('.feature-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});

// Template functionality
async function loadTemplate(templateId) {
    try {
        showLoading('Loading template...');
        
        const response = await fetch(`/api/templates/${templateId}`);
        const data = await response.json();
        
        if (data.success) {
            const template = data.template;
            
            // Fill in the description field with template info
            const descriptionField = document.getElementById('description');
            descriptionField.value = `${template.description}\n\nUse case: ${template.use_cases[0]}`;
            
            // Set complexity
            const complexityField = document.getElementById('complexity');
            if (complexityField) {
                complexityField.value = template.complexity;
            }
            
            // Show template info
            showMessage(`Template loaded: ${template.name}`, 'success');
            
            // Scroll to form
            document.getElementById('workflowForm').scrollIntoView({ 
                behavior: 'smooth' 
            });
            
        } else {
            showMessage(`Failed to load template: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('Template loading error:', error);
        showMessage('Failed to load template. Please try again.', 'error');
    } finally {
        hideLoading();
    }
}

// Template suggestions
async function getTemplateSuggestions(description) {
    try {
        const response = await fetch('/api/templates/suggestions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ description })
        });
        
        const data = await response.json();
        
        if (data.success && data.suggestions.length > 0) {
            showTemplateSuggestions(data.suggestions);
        }
    } catch (error) {
        console.error('Template suggestions error:', error);
    }
}

function showTemplateSuggestions(suggestions) {
    const suggestionsHtml = suggestions.map(template => `
        <div class="template-suggestion" onclick="loadTemplate('${template.id}')">
            <h4>${template.name}</h4>
            <p>${template.description}</p>
            <span class="template-category">${template.category.replace('_', ' ')}</span>
        </div>
    `).join('');
    
    const suggestionsContainer = document.getElementById('template-suggestions');
    if (suggestionsContainer) {
        suggestionsContainer.innerHTML = suggestionsHtml;
        suggestionsContainer.style.display = 'block';
    }
}

// Workflow validation
async function validateWorkflow(workflow) {
    try {
        const response = await fetch('/api/validate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ workflow })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showValidationResults(data.validation);
        } else {
            showMessage(`Validation failed: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('Validation error:', error);
        showMessage('Validation failed. Please try again.', 'error');
    }
}

function showValidationResults(validation) {
    const resultsHtml = `
        <div class="validation-results">
            <div class="validation-score ${validation.is_valid ? 'valid' : 'invalid'}">
                <h3>Validation Score: ${validation.score}/100</h3>
                <p>${validation.is_valid ? '✅ Workflow is valid' : '❌ Workflow has issues'}</p>
            </div>
            
            <div class="validation-summary">
                <span class="error-count">Errors: ${validation.summary.errors}</span>
                <span class="warning-count">Warnings: ${validation.summary.warnings}</span>
                <span class="info-count">Info: ${validation.summary.info}</span>
            </div>
            
            ${validation.issues.length > 0 ? `
                <div class="validation-issues">
                    <h4>Issues Found:</h4>
                    ${validation.issues.map(issue => `
                        <div class="issue ${issue.level}">
                            <strong>${issue.category}:</strong> ${issue.message}
                            ${issue.suggestion ? `<br><em>Suggestion: ${issue.suggestion}</em>` : ''}
                        </div>
                    `).join('')}
                </div>
            ` : ''}
            
            ${validation.recommendations.length > 0 ? `
                <div class="validation-recommendations">
                    <h4>Recommendations:</h4>
                    <ul>
                        ${validation.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                    </ul>
                </div>
            ` : ''}
        </div>
    `;
    
    const resultsContainer = document.getElementById('validation-results');
    if (resultsContainer) {
        resultsContainer.innerHTML = resultsHtml;
        resultsContainer.style.display = 'block';
    }
}

// Prompt assistance functionality
let promptAssistanceActive = false;
let currentStep = 0;

function showPromptHelp(message, suggestions = []) {
    const helpDiv = document.createElement('div');
    helpDiv.id = 'prompt-help';
    helpDiv.className = 'prompt-help-overlay';
    helpDiv.innerHTML = `
        <div class="prompt-help-modal">
            <div class="prompt-help-header">
                <h3>🤖 Workflow Assistant</h3>
                <button onclick="closePromptHelp()" class="close-btn">&times;</button>
            </div>
            <div class="prompt-help-content">
                <div class="help-message">${message.replace(/\n/g, '<br>')}</div>
                ${suggestions.length > 0 ? `
                    <div class="help-suggestions">
                        <p><strong>Quick suggestions:</strong></p>
                        ${suggestions.map(s => `<button class="suggestion-btn" onclick="useSuggestion('${s}')">${s}</button>`).join('')}
                    </div>
                ` : ''}
            </div>
            <div class="prompt-help-actions">
                <button onclick="closePromptHelp()" class="btn-secondary">Close</button>
                <button onclick="tryAgain()" class="btn-primary">Try Again</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(helpDiv);
    promptAssistanceActive = true;
}

function closePromptHelp() {
    const helpDiv = document.getElementById('prompt-help');
    if (helpDiv) {
        helpDiv.remove();
    }
    promptAssistanceActive = false;
}

function useSuggestion(suggestion) {
    const descriptionField = document.getElementById('description');
    if (descriptionField) {
        descriptionField.value = suggestion;
        descriptionField.focus();
    }
    closePromptHelp();
}

function tryAgain() {
    closePromptHelp();
    const descriptionField = document.getElementById('description');
    if (descriptionField) {
        descriptionField.focus();
    }
}

async function checkPromptHelp(description) {
    if (!description || description.trim().length < 5) {
        showPromptHelp(`
🤔 <strong>I need more information to help you!</strong><br><br>
Could you tell me what you want to automate? For example:<br>
• "Process CSV files and email results"<br>
• "Send daily reports from Google Sheets to Slack"<br>
• "Backup files to cloud storage weekly"<br><br>
<strong>What would you like your workflow to do?</strong>
        `, [
            "Process CSV files and email results",
            "Send daily reports to Slack", 
            "Backup files automatically",
            "Connect two different apps"
        ]);
        return true;
    }
    
    try {
        const response = await fetch('/prompt-help', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ description: description })
        });
        
        const result = await response.json();
        
        if (result.success && result.needs_help) {
            showPromptHelp(result.message, result.suggestions || []);
            return true;
        }
        
        return false;
    } catch (error) {
        console.error('Prompt help error:', error);
        return false;
    }
}

// Workflow form handling with prompt assistance
document.addEventListener('DOMContentLoaded', function() {
    const workflowForm = document.getElementById('workflowForm');
    const descriptionField = document.getElementById('description');
    
    if (workflowForm) {
        workflowForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const description = descriptionField.value.trim();
            
            // Check if user needs prompt assistance
            const needsHelp = await checkPromptHelp(description);
            if (needsHelp) {
                return; // Stop here and show help
            }
            
            // Proceed with normal workflow generation
            await generateWorkflow();
        });
    }
    
    // Add real-time help as user types
    if (descriptionField) {
        let helpTimeout;
        descriptionField.addEventListener('input', function() {
            clearTimeout(helpTimeout);
            const value = this.value.trim();
            
            // Show help after user stops typing for 2 seconds on short inputs
            if (value.length > 0 && value.length < 15) {
                helpTimeout = setTimeout(() => {
                    if (!promptAssistanceActive) {
                        showQuickHelp();
                    }
                }, 2000);
            }
        });
    }
});

function showQuickHelp() {
    const helpDiv = document.createElement('div');
    helpDiv.className = 'quick-help-tooltip';
    helpDiv.innerHTML = `
        <div class="quick-help-content">
            💡 <strong>Need help?</strong> Try being more specific about what you want to automate.
            <button onclick="this.parentElement.parentElement.remove()" class="quick-help-close">&times;</button>
        </div>
    `;
    
    const descriptionField = document.getElementById('description');
    if (descriptionField) {
        descriptionField.parentElement.appendChild(helpDiv);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (helpDiv.parentElement) {
                helpDiv.remove();
            }
        }, 5000);
    }
}

async function generateWorkflow() {
    const form = document.getElementById('workflowForm');
    const generateBtn = form.querySelector('button[type="submit"]');
    const btnContent = generateBtn.querySelector('.btn-content');
    const btnLoader = generateBtn.querySelector('.btn-loader');
    const output = document.getElementById('output');
    const outputPlaceholder = document.getElementById('outputPlaceholder');
    
    // Show loading state
    btnContent.style.display = 'none';
    btnLoader.style.display = 'flex';
    generateBtn.disabled = true;
    
    try {
        const formData = new FormData(form);
        const data = {
            description: formData.get('description'),
            triggerType: formData.get('triggerType') || 'webhook',
            complexity: 'medium'
        };
        
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (result.success) {
            // Show the generated workflow
            displayWorkflow(result);
            outputPlaceholder.style.display = 'none';
            output.style.display = 'block';
        } else if (result.needs_prompt_help) {
            // Show prompt assistance
            showPromptHelp(result.helper_message);
        } else {
            throw new Error(result.error || 'Generation failed');
        }
        
    } catch (error) {
        console.error('Error generating workflow:', error);
        alert('Error generating workflow: ' + error.message);
    } finally {
        // Reset button state
        btnContent.style.display = 'flex';
        btnLoader.style.display = 'none';
        generateBtn.disabled = false;
    }
}

function displayWorkflow(result) {
    const output = document.getElementById('output');
    const workflowContent = output.querySelector('.workflow-content');
    
    if (workflowContent) {
        // Create connection validation info if available
        let validationInfo = '';
        if (result.validation && result.validation.validation_applied) {
            const confidence = result.validation.confidence_score || 0;
            const transformations = result.validation.transformations || [];
            
            validationInfo = `
                <div class="validation-info">
                    <h5>🔍 Validation Applied</h5>
                    <p>Confidence Score: ${Math.round(confidence * 100)}%</p>
                    ${transformations.length > 0 ? `
                        <p>Improvements: ${transformations.join(', ')}</p>
                    ` : ''}
                </div>
            `;
        }
        
        // Create connection summary
        const connections = result.workflow.connections || {};
        const connectionCount = Object.keys(connections).length;
        const nodeCount = result.workflow.nodes ? result.workflow.nodes.length : 0;
        
        let connectionInfo = '';
        if (connectionCount > 0) {
            connectionInfo = `
                <div class="connection-info">
                    <h5>🔗 Connections</h5>
                    <p>${connectionCount} connections between ${nodeCount} nodes</p>
                    <div class="connection-list">
                        ${Object.entries(connections).map(([source, connData]) => {
                            if (connData.main && connData.main[0]) {
                                const targets = connData.main[0].map(conn => conn.node).join(', ');
                                return `<div class="connection-item">${source} → ${targets}</div>`;
                            }
                            return '';
                        }).join('')}
                    </div>
                </div>
            `;
        }
        
        workflowContent.innerHTML = `
            <div class="workflow-info">
                <h4>${result.workflow_name || 'Generated Workflow'}</h4>
                <p>${result.description || 'Custom workflow generated based on your requirements'}</p>
                ${validationInfo}
                ${connectionInfo}
            </div>
            <pre><code>${JSON.stringify(result.workflow, null, 2)}</code></pre>
        `;
    }
    
    // Setup copy button
    const copyBtn = document.getElementById('copyBtn');
    if (copyBtn) {
        copyBtn.onclick = function() {
            navigator.clipboard.writeText(JSON.stringify(result.workflow, null, 2))
                .then(() => {
                    const originalText = copyBtn.innerHTML;
                    copyBtn.innerHTML = '<span class="btn-icon">✅</span>Copied!';
                    setTimeout(() => {
                        copyBtn.innerHTML = originalText;
                    }, 2000);
                })
                .catch(err => {
                    console.error('Failed to copy:', err);
                    alert('Failed to copy to clipboard');
                });
        };
    }
}

// Add dynamic network connections
function createNetworkConnections() {
    const networkViz = document.querySelector('.network-viz');
    const nodes = networkViz.querySelectorAll('.node');
    
    // Create SVG for connections
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.style.position = 'absolute';
    svg.style.top = '0';
    svg.style.left = '0';
    svg.style.width = '100%';
    svg.style.height = '100%';
    svg.style.pointerEvents = 'none';
    svg.style.zIndex = '-1';
    
    networkViz.appendChild(svg);
    
    // Create connections between nodes
    nodes.forEach((node, i) => {
        const nextNode = nodes[(i + 1) % nodes.length];
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        
        const rect1 = node.getBoundingClientRect();
        const rect2 = nextNode.getBoundingClientRect();
        const vizRect = networkViz.getBoundingClientRect();
        
        line.setAttribute('x1', rect1.left - vizRect.left + rect1.width / 2);
        line.setAttribute('y1', rect1.top - vizRect.top + rect1.height / 2);
        line.setAttribute('x2', rect2.left - vizRect.left + rect2.width / 2);
        line.setAttribute('y2', rect2.top - vizRect.top + rect2.height / 2);
        line.setAttribute('stroke', 'rgba(0, 212, 255, 0.3)');
        line.setAttribute('stroke-width', '2');
        line.setAttribute('stroke-dasharray', '5,5');
        
        svg.appendChild(line);
        
        // Animate the line
        line.style.strokeDashoffset = '10';
        line.style.animation = `dash 2s linear infinite`;
    });
}

// Add CSS for line animation
const style = document.createElement('style');
style.textContent = `
    @keyframes dash {
        to {
            stroke-dashoffset: 0;
        }
    }
`;
document.head.appendChild(style);

// Initialize network connections when page loads
window.addEventListener('load', () => {
    setTimeout(createNetworkConnections, 500);
});

// Add hover effects to nodes
document.querySelectorAll('.node').forEach(node => {
    node.addEventListener('mouseenter', () => {
        node.style.transform = 'scale(1.1)';
        node.style.boxShadow = '0 10px 25px rgba(0, 212, 255, 0.4)';
    });
    
    node.addEventListener('mouseleave', () => {
        node.style.transform = 'scale(1)';
        node.style.boxShadow = 'none';
    });
});

// Add particle effect on hero section
function createParticles() {
    const hero = document.querySelector('.hero');
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.style.position = 'absolute';
        particle.style.width = '2px';
        particle.style.height = '2px';
        particle.style.background = 'rgba(0, 212, 255, 0.5)';
        particle.style.borderRadius = '50%';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animation = `float ${3 + Math.random() * 4}s ease-in-out infinite`;
        particle.style.animationDelay = Math.random() * 2 + 's';
        particle.style.pointerEvents = 'none';
        
        hero.appendChild(particle);
    }
}

// Initialize particles
window.addEventListener('load', createParticles);

// JSON Workflow Generator functionality
class WorkflowGenerator {
    constructor() {
        this.form = document.getElementById('workflowForm');
        this.output = document.getElementById('output');
        this.outputPlaceholder = document.getElementById('outputPlaceholder');
        this.jsonOutput = document.getElementById('jsonOutput');
        this.jsonSize = document.getElementById('jsonSize');
        this.copyBtn = document.getElementById('copyBtn');
        this.downloadBtn = document.getElementById('downloadBtn');
        this.generateBtn = this.form?.querySelector('.generate-button');
        
        this.currentWorkflow = null;
        this.currentFilename = null;
        
        this.init();
    }
    
    init() {
        if (this.form) {
            this.form.addEventListener('submit', (e) => this.handleSubmit(e));
        }
        
        if (this.copyBtn) {
            this.copyBtn.addEventListener('click', () => this.copyToClipboard());
        }
        
        if (this.downloadBtn) {
            this.downloadBtn.addEventListener('click', () => this.downloadWorkflow());
        }
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(this.form);
        const data = {
            description: formData.get('description'),
            triggerType: formData.get('triggerType'),
            complexity: 'medium' // Default to medium complexity
        };
        
        // Validate form
        if (!data.description || data.description.trim().length < 10) {
            this.showMessage('Please provide a detailed description (at least 10 characters)', 'error');
            return;
        }
        
        this.setLoading(true);
        
        try {
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            const result = await response.json();
            
            if (result.success) {
                this.displayWorkflow(result);
                this.showMessage('Workflow generated successfully!', 'success');
            } else {
                this.showMessage(result.error || 'Failed to generate workflow', 'error');
            }
        } catch (error) {
            console.error('Generation error:', error);
            this.showMessage('Network error. Please try again.', 'error');
        } finally {
            this.setLoading(false);
        }
    }
    
    displayWorkflow(result) {
        this.currentWorkflow = result.workflow;
        this.currentFilename = result.filename;
        
        // Format and display JSON
        const formattedJson = result.formatted_json || JSON.stringify(result.workflow, null, 2);
        this.jsonOutput.textContent = formattedJson;
        
        // Update JSON size
        const sizeKB = (new Blob([formattedJson]).size / 1024).toFixed(1);
        this.jsonSize.textContent = `${sizeKB} KB`;
        
        // Hide placeholder and show output
        if (this.outputPlaceholder) {
            this.outputPlaceholder.style.display = 'none';
        }
        this.output.style.display = 'block';
        
        // Scroll to output
        this.output.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    
    copyToClipboard() {
        if (!this.currentWorkflow) return;
        
        const jsonText = JSON.stringify(this.currentWorkflow, null, 2);
        
        navigator.clipboard.writeText(jsonText).then(() => {
            this.showMessage('Workflow copied to clipboard!', 'success');
            
            // Visual feedback
            const originalContent = this.copyBtn.innerHTML;
            this.copyBtn.innerHTML = '<span class="btn-icon">✅</span>Copied!';
            setTimeout(() => {
                this.copyBtn.innerHTML = originalContent;
            }, 2000);
        }).catch(() => {
            this.showMessage('Failed to copy to clipboard', 'error');
        });
    }
    
    downloadWorkflow() {
        if (!this.currentWorkflow) return;
        
        const jsonText = JSON.stringify(this.currentWorkflow, null, 2);
        const blob = new Blob([jsonText], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = this.currentFilename || 'workflow.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showMessage('Workflow downloaded!', 'success');
    }
    
    setLoading(loading) {
        if (!this.generateBtn) return;
        
        const btnContent = this.generateBtn.querySelector('.btn-content');
        const btnLoader = this.generateBtn.querySelector('.btn-loader');
        
        if (loading) {
            btnContent.style.display = 'none';
            btnLoader.style.display = 'flex';
            this.generateBtn.disabled = true;
        } else {
            btnContent.style.display = 'flex';
            btnLoader.style.display = 'none';
            this.generateBtn.disabled = false;
        }
    }
    
    showMessage(text, type) {
        // Remove existing messages
        const existingMessages = document.querySelectorAll('.message');
        existingMessages.forEach(msg => msg.remove());
        
        // Create new message
        const message = document.createElement('div');
        message.className = `message ${type}`;
        message.textContent = text;
        
        // Insert before form card
        const formCard = document.querySelector('.form-card');
        if (formCard && formCard.parentNode) {
            formCard.parentNode.insertBefore(message, formCard);
        }
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (message.parentNode) {
                message.remove();
            }
        }, 5000);
    }
}

// Initialize workflow generator when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new WorkflowGenerator();
});