// Enhanced N8N Workflow Generator - UX Improvements
// Real-time validation, accessibility, and micro-animations

class EnhancedWorkflowGenerator {
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
        this.validationTimeout = null;
        this.progressInterval = null;
        
        // Validation rules
        this.validationRules = {
            description: {
                minLength: 10,
                maxLength: 1000,
                required: true,
                patterns: {
                    hasAction: /\b(send|create|update|delete|process|generate|convert|sync|backup|notify|trigger|execute|run|start|stop|monitor|track|log|save|load|import|export|transform|validate|check|scan|analyze|filter|sort|merge|split|combine|connect|integrate|automate)\b/i,
                    hasSource: /\b(email|webhook|api|database|file|csv|json|xml|spreadsheet|form|calendar|slack|discord|teams|twitter|facebook|instagram|linkedin|youtube|github|gitlab|dropbox|google|microsoft|salesforce|hubspot|mailchimp|stripe|paypal|shopify|woocommerce|wordpress|notion|airtable|trello|asana|jira)\b/i,
                    hasTarget: /\b(to|into|in|save|store|send|post|upload|download|export|import|sync|backup|notify|alert|message|email|sms|push|webhook|api|database|file|folder|drive|cloud|server)\b/i
                }
            },
            triggerType: {
                required: true,
                validOptions: ['webhook', 'schedule', 'manual']
            }
        };
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupAccessibility();
        this.setupAnimations();
        this.setupMobileNavigation();
        this.setupScrollEffects();
        this.createProgressIndicator();
    }
    
    setupEventListeners() {
        if (this.form) {
            this.form.addEventListener('submit', (e) => this.handleSubmit(e));
            
            // Real-time validation
            const descriptionField = document.getElementById('description');
            const triggerField = document.getElementById('triggerType');
            
            if (descriptionField) {
                descriptionField.addEventListener('input', (e) => this.validateField(e.target, 'description'));
                descriptionField.addEventListener('blur', (e) => this.validateField(e.target, 'description', true));
                this.setupCharacterCounter(descriptionField);
            }
            
            if (triggerField) {
                triggerField.addEventListener('change', (e) => this.validateField(e.target, 'triggerType'));
            }
        }
        
        if (this.copyBtn) {
            this.copyBtn.addEventListener('click', () => this.copyToClipboard());
        }
        
        if (this.downloadBtn) {
            this.downloadBtn.addEventListener('click', () => this.downloadWorkflow());
        }
        
        // Template buttons
        document.querySelectorAll('.template-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.loadTemplate(e.target.dataset.template));
        });
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));
    }
    
    setupAccessibility() {
        // Add skip link
        const skipLink = document.createElement('a');
        skipLink.href = '#json-generator';
        skipLink.className = 'skip-link';
        skipLink.textContent = 'Skip to main content';
        document.body.insertBefore(skipLink, document.body.firstChild);
        
        // Add ARIA labels and descriptions
        const form = document.getElementById('workflowForm');
        if (form) {
            form.setAttribute('aria-label', 'Workflow generation form');
            form.setAttribute('role', 'form');
        }
        
        const descriptionField = document.getElementById('description');
        if (descriptionField) {
            descriptionField.setAttribute('aria-describedby', 'description-help');
            const helpText = document.createElement('div');
            helpText.id = 'description-help';
            helpText.className = 'sr-only';
            helpText.textContent = 'Describe what you want to automate. Include source, action, and destination.';
            descriptionField.parentNode.appendChild(helpText);
        }
        
        // Add live region for announcements
        const liveRegion = document.createElement('div');
        liveRegion.id = 'live-region';
        liveRegion.setAttribute('aria-live', 'polite');
        liveRegion.setAttribute('aria-atomic', 'true');
        liveRegion.className = 'sr-only';
        document.body.appendChild(liveRegion);
    }
    
    setupAnimations() {
        // Intersection Observer for scroll animations
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                }
            });
        }, observerOptions);
        
        // Observe elements for animation
        document.querySelectorAll('.feature-card, .form-card, .output-card').forEach(el => {
            el.classList.add('animate-on-scroll');
            observer.observe(el);
        });
        
        // Add hover effects to interactive elements
        this.setupHoverEffects();
    }
    
    setupHoverEffects() {
        document.querySelectorAll('.cta-button, .action-btn, .template-btn').forEach(btn => {
            btn.addEventListener('mouseenter', () => {
                btn.style.transform = 'translateY(-2px)';
            });
            
            btn.addEventListener('mouseleave', () => {
                btn.style.transform = 'translateY(0)';
            });
        });
    }
    
    setupMobileNavigation() {
        const mobileToggle = document.createElement('button');
        mobileToggle.className = 'mobile-nav-toggle';
        mobileToggle.innerHTML = '☰';
        mobileToggle.setAttribute('aria-label', 'Toggle navigation menu');
        mobileToggle.setAttribute('aria-expanded', 'false');
        
        const nav = document.querySelector('nav');
        const navLinks = document.querySelector('.nav-links');
        
        if (nav && navLinks) {
            nav.appendChild(mobileToggle);
            
            mobileToggle.addEventListener('click', () => {
                const isExpanded = mobileToggle.getAttribute('aria-expanded') === 'true';
                mobileToggle.setAttribute('aria-expanded', !isExpanded);
                navLinks.classList.toggle('active');
                mobileToggle.innerHTML = isExpanded ? '☰' : '✕';
            });
        }
    }
    
    setupScrollEffects() {
        let ticking = false;
        
        const updateScrollEffects = () => {
            const header = document.querySelector('header');
            if (header) {
                if (window.scrollY > 100) {
                    header.classList.add('scrolled');
                } else {
                    header.classList.remove('scrolled');
                }
            }
            ticking = false;
        };
        
        window.addEventListener('scroll', () => {
            if (!ticking) {
                requestAnimationFrame(updateScrollEffects);
                ticking = true;
            }
        });
    }
    
    createProgressIndicator() {
        if (this.generateBtn) {
            const progressContainer = document.createElement('div');
            progressContainer.className = 'progress-container';
            progressContainer.innerHTML = '<div class="progress-bar"></div>';
            this.generateBtn.appendChild(progressContainer);
        }
    }
    
    setupCharacterCounter(field) {
        const counter = document.createElement('div');
        counter.className = 'character-counter';
        field.parentNode.appendChild(counter);
        
        const updateCounter = () => {
            const current = field.value.length;
            const max = this.validationRules.description.maxLength;
            const min = this.validationRules.description.minLength;
            
            counter.textContent = `${current}/${max}`;
            
            if (current > max * 0.9) {
                counter.className = 'character-counter warning';
            } else if (current > max) {
                counter.className = 'character-counter error';
            } else {
                counter.className = 'character-counter';
            }
        };
        
        field.addEventListener('input', updateCounter);
        updateCounter();
    }
    
    validateField(field, fieldName, showSuccess = false) {
        clearTimeout(this.validationTimeout);
        
        this.validationTimeout = setTimeout(() => {
            const rules = this.validationRules[fieldName];
            const value = field.value.trim();
            const formGroup = field.closest('.form-group');
            
            let isValid = true;
            let message = '';
            let type = 'success';
            
            // Remove existing validation classes and messages
            formGroup.classList.remove('valid', 'invalid', 'warning');
            this.removeValidationMessage(formGroup);
            
            if (rules.required && !value) {
                isValid = false;
                message = `${fieldName.charAt(0).toUpperCase() + fieldName.slice(1)} is required`;
                type = 'error';
            } else if (value) {
                if (fieldName === 'description') {
                    if (value.length < rules.minLength) {
                        isValid = false;
                        message = `Description must be at least ${rules.minLength} characters`;
                        type = 'error';
                    } else if (value.length > rules.maxLength) {
                        isValid = false;
                        message = `Description must not exceed ${rules.maxLength} characters`;
                        type = 'error';
                    } else {
                        // Check for workflow patterns
                        const hasAction = rules.patterns.hasAction.test(value);
                        const hasSource = rules.patterns.hasSource.test(value);
                        const hasTarget = rules.patterns.hasTarget.test(value);
                        
                        if (!hasAction) {
                            message = 'Consider adding an action word (e.g., send, create, process)';
                            type = 'warning';
                        } else if (!hasSource && !hasTarget) {
                            message = 'Consider specifying a data source or destination';
                            type = 'warning';
                        } else if (showSuccess) {
                            message = 'Great! Your description looks comprehensive';
                            type = 'success';
                        }
                    }
                } else if (fieldName === 'triggerType') {
                    if (!rules.validOptions.includes(value)) {
                        isValid = false;
                        message = 'Please select a valid trigger type';
                        type = 'error';
                    } else if (showSuccess) {
                        message = 'Trigger type selected';
                        type = 'success';
                    }
                }
            }
            
            // Apply validation state
            if (!isValid) {
                formGroup.classList.add('invalid');
            } else if (type === 'warning') {
                formGroup.classList.add('warning');
            } else if (type === 'success' && showSuccess) {
                formGroup.classList.add('valid');
            }
            
            // Show validation message
            if (message) {
                this.showValidationMessage(formGroup, message, type);
            }
            
            // Update form validity
            this.updateFormValidity();
            
        }, 300); // Debounce validation
    }
    
    showValidationMessage(formGroup, message, type) {
        const existingMessage = formGroup.querySelector('.validation-message');
        if (existingMessage) {
            existingMessage.remove();
        }
        
        const messageEl = document.createElement('div');
        messageEl.className = `validation-message ${type}`;
        
        const icon = type === 'success' ? '✓' : type === 'error' ? '✗' : '⚠';
        messageEl.innerHTML = `<span>${icon}</span><span>${message}</span>`;
        
        formGroup.appendChild(messageEl);
        
        // Animate in
        setTimeout(() => messageEl.classList.add('show'), 10);
    }
    
    removeValidationMessage(formGroup) {
        const message = formGroup.querySelector('.validation-message');
        if (message) {
            message.classList.remove('show');
            setTimeout(() => message.remove(), 300);
        }
    }
    
    updateFormValidity() {
        const descriptionField = document.getElementById('description');
        const triggerField = document.getElementById('triggerType');
        
        let isFormValid = true;
        
        if (descriptionField) {
            const value = descriptionField.value.trim();
            const rules = this.validationRules.description;
            if (!value || value.length < rules.minLength || value.length > rules.maxLength) {
                isFormValid = false;
            }
        }
        
        if (triggerField) {
            const value = triggerField.value;
            if (!this.validationRules.triggerType.validOptions.includes(value)) {
                isFormValid = false;
            }
        }
        
        if (this.generateBtn) {
            this.generateBtn.disabled = !isFormValid;
        }
    }
    
    async handleSubmit(e) {
        e.preventDefault();
        
        // Final validation
        const formData = new FormData(this.form);
        const data = {
            description: formData.get('description'),
            triggerType: formData.get('triggerType'),
            complexity: 'medium'
        };
        
        // Validate form data
        if (!this.validateFormData(data)) {
            return;
        }
        
        this.setLoading(true);
        this.startProgress();
        
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
                this.announceToScreenReader('Workflow has been generated successfully');
            } else if (result.needs_prompt_help) {
                this.showPromptHelp(result.helper_message);
            } else {
                throw new Error(result.error || 'Generation failed');
            }
        } catch (error) {
            console.error('Generation error:', error);
            this.showMessage('Failed to generate workflow. Please try again.', 'error');
            this.announceToScreenReader('Workflow generation failed');
        } finally {
            this.setLoading(false);
            this.stopProgress();
        }
    }
    
    validateFormData(data) {
        const descriptionRules = this.validationRules.description;
        
        if (!data.description || data.description.trim().length < descriptionRules.minLength) {
            this.showMessage(`Description must be at least ${descriptionRules.minLength} characters`, 'error');
            document.getElementById('description').focus();
            return false;
        }
        
        if (data.description.length > descriptionRules.maxLength) {
            this.showMessage(`Description must not exceed ${descriptionRules.maxLength} characters`, 'error');
            document.getElementById('description').focus();
            return false;
        }
        
        if (!this.validationRules.triggerType.validOptions.includes(data.triggerType)) {
            this.showMessage('Please select a valid trigger type', 'error');
            document.getElementById('triggerType').focus();
            return false;
        }
        
        return true;
    }
    
    setLoading(loading) {
        if (!this.generateBtn) return;
        
        const btnContent = this.generateBtn.querySelector('.btn-content');
        const btnLoader = this.generateBtn.querySelector('.btn-loader');
        const progressContainer = this.generateBtn.querySelector('.progress-container');
        
        if (loading) {
            btnContent.style.display = 'none';
            btnLoader.style.display = 'flex';
            this.generateBtn.disabled = true;
            this.generateBtn.setAttribute('aria-busy', 'true');
            if (progressContainer) {
                progressContainer.classList.add('active');
            }
        } else {
            btnContent.style.display = 'flex';
            btnLoader.style.display = 'none';
            this.generateBtn.disabled = false;
            this.generateBtn.setAttribute('aria-busy', 'false');
            if (progressContainer) {
                progressContainer.classList.remove('active');
            }
        }
    }
    
    startProgress() {
        const progressBar = this.generateBtn?.querySelector('.progress-bar');
        if (!progressBar) return;
        
        let progress = 0;
        const increment = Math.random() * 15 + 5; // 5-20% increments
        
        this.progressInterval = setInterval(() => {
            progress += increment;
            if (progress > 90) {
                progress = 90; // Don't complete until actual completion
            }
            progressBar.style.width = `${progress}%`;
        }, 500);
    }
    
    stopProgress() {
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
            this.progressInterval = null;
        }
        
        const progressBar = this.generateBtn?.querySelector('.progress-bar');
        if (progressBar) {
            progressBar.style.width = '100%';
            setTimeout(() => {
                progressBar.style.width = '0%';
            }, 1000);
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
        
        // Add accessibility attributes
        this.output.setAttribute('aria-label', 'Generated workflow output');
        this.jsonOutput.setAttribute('aria-label', 'Workflow JSON code');
        
        // Smooth scroll to output
        this.output.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
        
        // Focus management for screen readers
        setTimeout(() => {
            const outputTitle = this.output.querySelector('h3');
            if (outputTitle) {
                outputTitle.focus();
            }
        }, 500);
    }
    
    async copyToClipboard() {
        if (!this.currentWorkflow) return;
        
        const jsonText = JSON.stringify(this.currentWorkflow, null, 2);
        
        try {
            await navigator.clipboard.writeText(jsonText);
            this.showMessage('Workflow copied to clipboard!', 'success');
            this.announceToScreenReader('Workflow copied to clipboard');
            
            // Visual feedback
            const originalContent = this.copyBtn.innerHTML;
            this.copyBtn.innerHTML = '<span class="btn-icon">✅</span>Copied!';
            this.copyBtn.classList.add('success-state');
            
            setTimeout(() => {
                this.copyBtn.innerHTML = originalContent;
                this.copyBtn.classList.remove('success-state');
            }, 2000);
        } catch (error) {
            // Fallback for older browsers
            const textArea = document.createElement('textarea');
            textArea.value = jsonText;
            document.body.appendChild(textArea);
            textArea.select();
            
            try {
                document.execCommand('copy');
                this.showMessage('Workflow copied to clipboard!', 'success');
            } catch (fallbackError) {
                this.showMessage('Failed to copy to clipboard', 'error');
            }
            
            document.body.removeChild(textArea);
        }
    }
    
    downloadWorkflow() {
        if (!this.currentWorkflow) return;
        
        const jsonText = JSON.stringify(this.currentWorkflow, null, 2);
        const blob = new Blob([jsonText], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = this.currentFilename || 'workflow.json';
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        this.showMessage('Workflow downloaded!', 'success');
        this.announceToScreenReader('Workflow file downloaded');
    }
    
    showMessage(text, type) {
        // Remove existing messages
        const existingMessages = document.querySelectorAll('.message');
        existingMessages.forEach(msg => {
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 300);
        });
        
        // Create new message
        const message = document.createElement('div');
        message.className = `message ${type}`;
        
        const icon = type === 'success' ? '✓' : type === 'error' ? '✗' : type === 'warning' ? '⚠' : 'ℹ';
        message.innerHTML = `<span>${icon}</span><span>${text}</span>`;
        
        // Insert before form card
        const formCard = document.querySelector('.form-card');
        if (formCard && formCard.parentNode) {
            formCard.parentNode.insertBefore(message, formCard);
        }
        
        // Animate in
        setTimeout(() => {
            message.style.opacity = '1';
        }, 10);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (message.parentNode) {
                message.style.opacity = '0';
                setTimeout(() => message.remove(), 300);
            }
        }, 5000);
    }
    
    announceToScreenReader(message) {
        const liveRegion = document.getElementById('live-region');
        if (liveRegion) {
            liveRegion.textContent = message;
            setTimeout(() => {
                liveRegion.textContent = '';
            }, 1000);
        }
    }
    
    handleKeyboardShortcuts(e) {
        // Ctrl/Cmd + Enter to submit form
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            e.preventDefault();
            if (this.form && !this.generateBtn.disabled) {
                this.form.dispatchEvent(new Event('submit'));
            }
        }
        
        // Ctrl/Cmd + C to copy when output is visible
        if ((e.ctrlKey || e.metaKey) && e.key === 'c' && this.currentWorkflow) {
            if (!window.getSelection().toString()) { // Only if no text is selected
                e.preventDefault();
                this.copyToClipboard();
            }
        }
        
        // Escape to close mobile menu
        if (e.key === 'Escape') {
            const navLinks = document.querySelector('.nav-links');
            const mobileToggle = document.querySelector('.mobile-nav-toggle');
            if (navLinks && navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                if (mobileToggle) {
                    mobileToggle.setAttribute('aria-expanded', 'false');
                    mobileToggle.innerHTML = '☰';
                }
            }
        }
    }
    
    async loadTemplate(templateId) {
        try {
            this.showLoadingOverlay('Loading template...');
            
            const response = await fetch(`/api/templates/${templateId}`);
            const data = await response.json();
            
            if (data.success) {
                const template = data.template;
                
                // Fill in the description field
                const descriptionField = document.getElementById('description');
                if (descriptionField) {
                    descriptionField.value = `${template.description}\\n\\nUse case: ${template.use_cases[0]}`;
                    this.validateField(descriptionField, 'description');
                }
                
                // Set trigger type if available
                const triggerField = document.getElementById('triggerType');
                if (triggerField && template.trigger_type) {
                    triggerField.value = template.trigger_type;
                    this.validateField(triggerField, 'triggerType');
                }
                
                this.showMessage(`Template loaded: ${template.name}`, 'success');
                this.announceToScreenReader(`Template ${template.name} loaded`);
                
                // Focus on description field
                if (descriptionField) {
                    descriptionField.focus();
                    descriptionField.scrollIntoView({ behavior: 'smooth' });
                }
                
            } else {
                this.showMessage(`Failed to load template: ${data.error}`, 'error');
            }
        } catch (error) {
            console.error('Template loading error:', error);
            this.showMessage('Failed to load template. Please try again.', 'error');
        } finally {
            this.hideLoadingOverlay();
        }
    }
    
    showLoadingOverlay(message) {
        const overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.className = 'loading-overlay';
        overlay.innerHTML = `
            <div class="loading-content">
                <div class="loading-spinner"></div>
                <div class="loading-text">${message}</div>
            </div>
        `;
        document.body.appendChild(overlay);
        
        // Prevent scrolling
        document.body.style.overflow = 'hidden';
        
        // Focus trap
        overlay.setAttribute('tabindex', '-1');
        overlay.focus();
    }
    
    hideLoadingOverlay() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.style.opacity = '0';
            setTimeout(() => {
                overlay.remove();
                document.body.style.overflow = '';
            }, 300);
        }
    }
    
    showPromptHelp(message, suggestions = []) {
        // Implementation for prompt help modal
        // This would create an accessible modal dialog
        console.log('Prompt help:', message, suggestions);
    }
}

// Enhanced smooth scrolling for navigation
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerHeight = document.querySelector('header').offsetHeight;
                const targetPosition = target.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Focus management for accessibility
                target.setAttribute('tabindex', '-1');
                target.focus();
            }
        });
    });
}

// Enhanced network visualization
function createEnhancedNetworkViz() {
    const networkViz = document.querySelector('.network-viz');
    if (!networkViz) return;
    
    const nodes = networkViz.querySelectorAll('.node');
    
    // Create SVG for connections
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.style.position = 'absolute';
    svg.style.top = '0';
    svg.style.left = '0';
    svg.style.width = '100%';
    svg.style.height = '100%';
    svg.style.pointerEvents = 'none';
    svg.style.zIndex = '0';
    
    networkViz.appendChild(svg);
    
    // Create animated connections
    const createConnection = (node1, node2, delay = 0) => {
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        const rect1 = node1.getBoundingClientRect();
        const rect2 = node2.getBoundingClientRect();
        const vizRect = networkViz.getBoundingClientRect();
        
        line.setAttribute('x1', rect1.left - vizRect.left + rect1.width / 2);
        line.setAttribute('y1', rect1.top - vizRect.top + rect1.height / 2);
        line.setAttribute('x2', rect2.left - vizRect.left + rect2.width / 2);
        line.setAttribute('y2', rect2.top - vizRect.top + rect2.height / 2);
        line.setAttribute('stroke', 'rgba(0, 212, 255, 0.3)');
        line.setAttribute('stroke-width', '2');
        line.setAttribute('stroke-dasharray', '5,5');
        line.style.strokeDashoffset = '10';
        line.style.animation = `dash 2s linear infinite ${delay}s`;
        
        svg.appendChild(line);
    };
    
    // Connect nodes in sequence
    nodes.forEach((node, i) => {
        const nextNode = nodes[(i + 1) % nodes.length];
        createConnection(node, nextNode, i * 0.2);
    });
    
    // Add hover effects
    nodes.forEach(node => {
        node.addEventListener('mouseenter', () => {
            node.style.transform = 'scale(1.1)';
            node.style.zIndex = '10';
        });
        
        node.addEventListener('mouseleave', () => {
            node.style.transform = 'scale(1)';
            node.style.zIndex = '1';
        });
    });
}

// Add CSS animations
function addAnimationStyles() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes dash {
            to {
                stroke-dashoffset: 0;
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .success-state {
            background: linear-gradient(135deg, var(--success-green), #16a34a) !important;
        }
        
        .animate-on-scroll {
            animation: fadeInUp 0.6s ease-out forwards;
        }
    `;
    document.head.appendChild(style);
}

// Enhanced particle system for hero section
function createEnhancedParticles() {
    const hero = document.querySelector('.hero');
    if (!hero) return;
    
    const particleCount = window.innerWidth < 768 ? 20 : 50;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.style.position = 'absolute';
        particle.style.width = Math.random() * 3 + 1 + 'px';
        particle.style.height = particle.style.width;
        particle.style.background = `rgba(0, 212, 255, ${Math.random() * 0.5 + 0.1})`;
        particle.style.borderRadius = '50%';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = Math.random() * 100 + '%';
        particle.style.animation = `float ${3 + Math.random() * 4}s ease-in-out infinite`;
        particle.style.animationDelay = Math.random() * 2 + 's';
        particle.style.pointerEvents = 'none';
        particle.style.zIndex = '0';
        
        hero.appendChild(particle);
    }
}

// Performance optimization: Reduce animations on low-end devices
function optimizeForPerformance() {
    const isLowEndDevice = navigator.hardwareConcurrency < 4 || 
                          navigator.deviceMemory < 4 || 
                          window.innerWidth < 768;
    
    if (isLowEndDevice) {
        document.documentElement.style.setProperty('--transition-base', '0.15s');
        document.documentElement.style.setProperty('--transition-slow', '0.3s');
        
        // Reduce particle count
        const particles = document.querySelectorAll('.hero div[style*="position: absolute"]');
        particles.forEach((particle, index) => {
            if (index % 2 === 0) {
                particle.remove();
            }
        });
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Initialize main application
    new EnhancedWorkflowGenerator();
    
    // Setup additional features
    setupSmoothScrolling();
    addAnimationStyles();
    optimizeForPerformance();
    
    // Initialize visual effects after a short delay
    setTimeout(() => {
        createEnhancedNetworkViz();
        createEnhancedParticles();
    }, 500);
});

// Handle window resize for responsive adjustments
let resizeTimeout;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        // Recreate network visualization on resize
        const existingSvg = document.querySelector('.network-viz svg');
        if (existingSvg) {
            existingSvg.remove();
            createEnhancedNetworkViz();
        }
    }, 250);
});

// Service Worker registration for offline support (optional)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}