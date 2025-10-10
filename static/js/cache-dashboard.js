/**
 * Cache Dashboard for N8N Workflow Generator
 * Provides real-time cache monitoring and management
 */

class CacheDashboard {
    constructor() {
        this.refreshInterval = 5000; // 5 seconds
        this.intervalId = null;
        this.init();
    }

    init() {
        this.createDashboard();
        this.bindEvents();
        this.startAutoRefresh();
    }

    createDashboard() {
        const dashboardHtml = `
            <div id="cache-dashboard" class="cache-dashboard">
                <div class="dashboard-header">
                    <h3>Cache System Dashboard</h3>
                    <div class="dashboard-controls">
                        <button id="refresh-cache-stats" class="btn btn-primary">Refresh</button>
                        <button id="clear-all-cache" class="btn btn-warning">Clear All</button>
                        <button id="warm-cache" class="btn btn-success">Warm Cache</button>
                    </div>
                </div>
                
                <div class="dashboard-content">
                    <div class="stats-grid">
                        <div class="stat-card">
                            <h4>Cache Status</h4>
                            <div id="cache-status" class="status-indicator">Loading...</div>
                        </div>
                        
                        <div class="stat-card">
                            <h4>Hit Rate</h4>
                            <div id="hit-rate" class="metric-value">-</div>
                            <div class="metric-bar">
                                <div id="hit-rate-bar" class="progress-bar"></div>
                            </div>
                        </div>
                        
                        <div class="stat-card">
                            <h4>Total Requests</h4>
                            <div id="total-requests" class="metric-value">-</div>
                        </div>
                        
                        <div class="stat-card">
                            <h4>Cache Errors</h4>
                            <div id="cache-errors" class="metric-value">-</div>
                        </div>
                    </div>
                    
                    <div class="detailed-stats">
                        <div class="stats-section">
                            <h4>Performance Metrics</h4>
                            <table id="performance-table" class="stats-table">
                                <thead>
                                    <tr>
                                        <th>Metric</th>
                                        <th>Value</th>
                                        <th>Status</th>
                                    </tr>
                                </thead>
                                <tbody></tbody>
                            </table>
                        </div>
                        
                        <div class="stats-section">
                            <h4>Cache Operations</h4>
                            <div class="operation-buttons">
                                <button id="clear-workflow-cache" class="btn btn-outline">Clear Workflows</button>
                                <button id="clear-ai-cache" class="btn btn-outline">Clear AI Responses</button>
                                <button id="clear-validation-cache" class="btn btn-outline">Clear Validation</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        // Add to page if not exists
        if (!document.getElementById('cache-dashboard')) {
            const container = document.createElement('div');
            container.innerHTML = dashboardHtml;
            document.body.appendChild(container);
        }
    }

    bindEvents() {
        document.getElementById('refresh-cache-stats')?.addEventListener('click', () => {
            this.refreshStats();
        });

        document.getElementById('clear-all-cache')?.addEventListener('click', () => {
            this.clearCache('all');
        });

        document.getElementById('warm-cache')?.addEventListener('click', () => {
            this.warmCache();
        });

        document.getElementById('clear-workflow-cache')?.addEventListener('click', () => {
            this.clearCache('workflows');
        });

        document.getElementById('clear-ai-cache')?.addEventListener('click', () => {
            this.clearCache('ai');
        });

        document.getElementById('clear-validation-cache')?.addEventListener('click', () => {
            this.clearCache('validation');
        });
    }

    async refreshStats() {
        try {
            const response = await fetch('/api/cache/stats');
            const data = await response.json();
            
            if (data.success) {
                this.updateDashboard(data.statistics);
            } else {
                this.showError('Failed to fetch cache statistics');
            }
        } catch (error) {
            this.showError('Error fetching cache stats: ' + error.message);
        }
    }

    updateDashboard(stats) {
        // Update status indicator
        const statusEl = document.getElementById('cache-status');
        if (statusEl) {
            const status = stats.redis_available ? 'Redis Active' : 'Fallback Mode';
            const statusClass = stats.redis_available ? 'status-good' : 'status-warning';
            statusEl.innerHTML = `<span class="${statusClass}">${status}</span>`;
        }

        // Update hit rate
        const hitRateEl = document.getElementById('hit-rate');
        const hitRateBarEl = document.getElementById('hit-rate-bar');
        if (hitRateEl && hitRateBarEl) {
            hitRateEl.textContent = `${stats.hit_rate}%`;
            hitRateBarEl.style.width = `${stats.hit_rate}%`;
            
            // Color code based on performance
            const barClass = stats.hit_rate > 80 ? 'bar-excellent' : 
                           stats.hit_rate > 60 ? 'bar-good' : 'bar-poor';
            hitRateBarEl.className = `progress-bar ${barClass}`;
        }

        // Update total requests
        const totalRequestsEl = document.getElementById('total-requests');
        if (totalRequestsEl) {
            totalRequestsEl.textContent = stats.total_requests.toLocaleString();
        }

        // Update errors
        const errorsEl = document.getElementById('cache-errors');
        if (errorsEl) {
            errorsEl.textContent = stats.errors;
            errorsEl.className = stats.errors > 0 ? 'metric-value error' : 'metric-value';
        }

        // Update performance table
        this.updatePerformanceTable(stats);
    }

    updatePerformanceTable(stats) {
        const tableBody = document.querySelector('#performance-table tbody');
        if (!tableBody) return;

        const metrics = [
            { name: 'Cache Hits', value: stats.hits, status: 'good' },
            { name: 'Cache Misses', value: stats.misses, status: 'neutral' },
            { name: 'Cache Sets', value: stats.sets, status: 'good' },
            { name: 'Fallback Cache Size', value: stats.fallback_cache_size, status: 'neutral' },
            { name: 'Redis Memory', value: stats.redis_memory_used || 'N/A', status: 'neutral' }
        ];

        tableBody.innerHTML = metrics.map(metric => `
            <tr>
                <td>${metric.name}</td>
                <td>${metric.value}</td>
                <td><span class="status-${metric.status}">●</span></td>
            </tr>
        `).join('');
    }

    async clearCache(type) {
        try {
            let endpoint = '/api/cache/clear';
            let body = {};

            if (type === 'workflows') {
                endpoint = '/api/cache/clear/workflows';
            } else if (type === 'ai') {
                endpoint = '/api/cache/clear/ai';
            } else if (type === 'validation') {
                body = { pattern: 'n8n_cache:validation:*' };
            } else if (type === 'all') {
                body = { pattern: 'all' };
            }

            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(body)
            });

            const data = await response.json();
            
            if (data.success) {
                this.showSuccess(data.message);
                this.refreshStats(); // Refresh stats after clearing
            } else {
                this.showError('Failed to clear cache: ' + data.error);
            }
        } catch (error) {
            this.showError('Error clearing cache: ' + error.message);
        }
    }

    async warmCache() {
        try {
            const response = await fetch('/api/cache/warm', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    types: ['templates', 'validation']
                })
            });

            const data = await response.json();
            
            if (data.success) {
                this.showSuccess('Cache warming completed');
                this.refreshStats();
            } else {
                this.showError('Failed to warm cache: ' + data.error);
            }
        } catch (error) {
            this.showError('Error warming cache: ' + error.message);
        }
    }

    startAutoRefresh() {
        this.refreshStats(); // Initial load
        this.intervalId = setInterval(() => {
            this.refreshStats();
        }, this.refreshInterval);
    }

    stopAutoRefresh() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }

    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    showError(message) {
        this.showNotification(message, 'error');
    }

    showNotification(message, type) {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    destroy() {
        this.stopAutoRefresh();
        const dashboard = document.getElementById('cache-dashboard');
        if (dashboard) {
            dashboard.remove();
        }
    }
}

// CSS for the dashboard
const dashboardCSS = `
.cache-dashboard {
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin: 20px;
    padding: 20px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

.dashboard-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
    border-bottom: 1px solid #eee;
    padding-bottom: 15px;
}

.dashboard-controls {
    display: flex;
    gap: 10px;
}

.btn {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: background-color 0.2s;
}

.btn-primary { background: #007bff; color: white; }
.btn-warning { background: #ffc107; color: black; }
.btn-success { background: #28a745; color: white; }
.btn-outline { background: transparent; border: 1px solid #ddd; color: #333; }

.btn:hover { opacity: 0.9; }

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.stat-card {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 6px;
    text-align: center;
}

.stat-card h4 {
    margin: 0 0 10px 0;
    color: #666;
    font-size: 14px;
    text-transform: uppercase;
}

.metric-value {
    font-size: 24px;
    font-weight: bold;
    color: #333;
}

.metric-value.error {
    color: #dc3545;
}

.metric-bar {
    width: 100%;
    height: 8px;
    background: #e9ecef;
    border-radius: 4px;
    margin-top: 10px;
    overflow: hidden;
}

.progress-bar {
    height: 100%;
    transition: width 0.3s ease;
}

.bar-excellent { background: #28a745; }
.bar-good { background: #ffc107; }
.bar-poor { background: #dc3545; }

.status-indicator .status-good { color: #28a745; }
.status-indicator .status-warning { color: #ffc107; }
.status-indicator .status-error { color: #dc3545; }

.detailed-stats {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 30px;
}

.stats-section h4 {
    margin-bottom: 15px;
    color: #333;
}

.stats-table {
    width: 100%;
    border-collapse: collapse;
}

.stats-table th,
.stats-table td {
    padding: 8px 12px;
    text-align: left;
    border-bottom: 1px solid #eee;
}

.stats-table th {
    background: #f8f9fa;
    font-weight: 600;
}

.operation-buttons {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.status-good { color: #28a745; }
.status-neutral { color: #6c757d; }
.status-error { color: #dc3545; }

.notification {
    position: fixed;
    top: 20px;
    right: 20px;
    padding: 12px 20px;
    border-radius: 4px;
    color: white;
    font-weight: 500;
    z-index: 1000;
    animation: slideIn 0.3s ease;
}

.notification-success { background: #28a745; }
.notification-error { background: #dc3545; }

@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@media (max-width: 768px) {
    .detailed-stats {
        grid-template-columns: 1fr;
    }
    
    .dashboard-header {
        flex-direction: column;
        gap: 15px;
    }
}
`;

// Add CSS to page
const style = document.createElement('style');
style.textContent = dashboardCSS;
document.head.appendChild(style);

// Export for use
window.CacheDashboard = CacheDashboard;