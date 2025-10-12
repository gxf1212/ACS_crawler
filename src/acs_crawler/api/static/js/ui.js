/**
 * UI Module
 * Handles UI interactions and updates
 */

const UI = {
    /**
     * Show alert message
     */
    showAlert(elementId, message, type = 'info') {
        const alertDiv = document.getElementById(elementId);
        if (!alertDiv) return;

        const iconMap = {
            success: 'check-circle',
            danger: 'exclamation-triangle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };

        const icon = iconMap[type] || 'info-circle';

        alertDiv.className = `alert alert-${type} mt-3`;
        alertDiv.innerHTML = `<i class="bi bi-${icon}"></i> ${message}`;
        alertDiv.style.display = 'block';

        return alertDiv;
    },

    /**
     * Hide alert message
     */
    hideAlert(elementId) {
        const alertDiv = document.getElementById(elementId);
        if (alertDiv) {
            alertDiv.style.display = 'none';
        }
    },

    /**
     * Set button loading state
     */
    setButtonLoading(button, loading = true, originalText = '') {
        if (loading) {
            button.disabled = true;
            button.dataset.originalText = button.innerHTML;
            button.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Loading...';
        } else {
            button.disabled = false;
            button.innerHTML = originalText || button.dataset.originalText || 'Submit';
        }
    },

    /**
     * Populate select dropdown with options
     */
    populateSelect(selectId, options, valueKey, labelKey) {
        const select = document.getElementById(selectId);
        if (!select) return;

        // Clear existing options except first (placeholder)
        while (select.options.length > 1) {
            select.remove(1);
        }

        // Add new options
        options.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option[valueKey];
            optionElement.textContent = option[labelKey];
            select.appendChild(optionElement);
        });
    },

    /**
     * Show loading spinner
     */
    showLoading(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3 text-muted">Loading data...</p>
            </div>
        `;
    },

    /**
     * Show error message in container
     */
    showError(containerId, message) {
        const container = document.getElementById(containerId);
        if (!container) return;

        container.innerHTML = `
            <div class="alert alert-danger" role="alert">
                <i class="bi bi-exclamation-triangle"></i> ${message}
            </div>
        `;
    },

    /**
     * Format date string
     */
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    },

    /**
     * Format datetime string
     */
    formatDateTime(dateString) {
        const date = new Date(dateString);
        return date.toLocaleString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    /**
     * Truncate text to specified length
     */
    truncate(text, maxLength = 100) {
        if (!text) return '';
        return text.length > maxLength
            ? text.substring(0, maxLength) + '...'
            : text;
    },

    /**
     * Debounce function for input events
     */
    debounce(func, wait = 300) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    /**
     * Validate URL
     */
    isValidUrl(string) {
        try {
            new URL(string);
            return true;
        } catch (_) {
            return false;
        }
    },

    /**
     * Reload page after delay
     */
    reloadAfterDelay(delay = 2000) {
        setTimeout(() => {
            window.location.reload();
        }, delay);
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UI;
}
