// static/dashboard.js

// Dashboard functionality
document.addEventListener('DOMContentLoaded', function() {
    updateHealthStatus();
    setInterval(updateHealthStatus, 30000); // Update every 30 seconds
});

async function updateHealthStatus() {
    try {
        const response = await fetch('/health');
        const health = await response.json();
        
        updateStatusIndicator('model-status', health.components.model);
        updateStatusIndicator('email-status', health.components.email);
        updateStatusIndicator('db-status', health.components.database);
        
        console.log('Health status updated:', health);
    } catch (error) {
        console.error('Failed to fetch health status:', error);
        updateStatusIndicator('model-status', 'error');
        updateStatusIndicator('email-status', 'error');
        updateStatusIndicator('db-status', 'error');
    }
}

function updateStatusIndicator(elementId, status) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    let statusText = '';
    let statusClass = '';
    
    switch(status) {
        case 'loaded':
        case 'connected':
        case 'ready':
        case 'healthy':
            statusText = '🟢 Ready';
            statusClass = 'status-healthy';
            break;
        case 'not_loaded':
        case 'not_connected':
        case 'not_ready':
            statusText = '🟡 Not Ready';
            statusClass = 'status-warning';
            break;
        case 'error':
        default:
            statusText = '🔴 Error';
            statusClass = 'status-error';
            break;
    }
    
    element.innerHTML = `<span class="status-indicator ${statusClass}"></span>${statusText}`;
}

async function testPrediction() {
    try {
        showLoading('Testing prediction...');
        
        const testData = {
            input_data: {
                feature_1: Math.random(),
                feature_2: Math.random(),
                feature_3: "test_input"
            },
            model_params: {
                temperature: 0.7
            }
        };
        
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(testData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showAlert('Prediction successful!', 'success');
            console.log('Prediction result:', result);
        } else {
            showAlert(`Prediction failed: ${result.detail}`, 'error');
        }
    } catch (error) {
        showAlert(`Error: ${error.message}`, 'error');
        console.error('Prediction test failed:', error);
    } finally {
        hideLoading();
    }
}

async function sendTestEmail() {
    try {
        showLoading('Sending test email...');
        
        const emailData = {
            to_email: 'test@example.com',
            subject: 'Test Email from Lightning Studio',
            content: 'This is a test email sent from the Lightning Studio API dashboard.',
            priority: 'normal'
        };
        
        const response = await fetch('/send_email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(emailData)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showAlert('Test email sent successfully!', 'success');
            console.log('Email result:', result);
        } else {
            showAlert(`Email sending failed: ${result.detail}`, 'error');
        }
    } catch (error) {
        showAlert(`Error: ${error.message}`, 'error');
        console.error('Email test failed:', error);
    } finally {
        hideLoading();
    }
}

function showAlert(message, type = 'info') {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create new alert
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    
    // Insert at the top of the container
    const container = document.querySelector('.container');
    container.insertBefore(alert, container.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

function showLoading(message = 'Loading...') {
    const existingLoading = document.querySelector('.loading-overlay');
    if (existingLoading) return;
    
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        color: white;
        font-size: 1.2rem;
    `;
    
    overlay.innerHTML = `
        <div style="text-align: center;">
            <div class="loading" style="margin: 0 auto 1rem;"></div>
            <div>${message}</div>
        </div>
    `;
    
    document.body.appendChild(overlay);
}

function hideLoading() {
    const overlay = document.querySelector('.loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}

// API interaction functions
async function makeApiCall(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(endpoint, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.detail || 'API call failed');
        }
        
        return result;
    } catch (error) {
        console.error(`API call to ${endpoint} failed:`, error);
        throw error;
    }
}

// Utility functions
function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

function formatBytes(bytes, decimals = 2) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const dm = decimals < 0 ? 0 : decimals;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
    
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// Export functions for use in other scripts
window.dashboardAPI = {
    updateHealthStatus,
    testPrediction,
    sendTestEmail,
    makeApiCall,
    showAlert,
    showLoading,
    hideLoading
};