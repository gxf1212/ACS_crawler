/**
 * Papers Charts Module
 * Handles chart rendering on the papers page modal
 */

const PapersCharts = {
    chartsLoaded: false,

    /**
     * Initialize event listeners
     */
    init() {
        console.log('Initializing papers charts...');

        // Listen for modal show event
        const modal = document.getElementById('chartsModal');
        if (modal) {
            modal.addEventListener('shown.bs.modal', () => {
                this.onModalShown();
            });
        }

        console.log('Papers charts module initialized');
    },

    /**
     * Handle modal shown event
     */
    async onModalShown() {
        // Only load charts once
        if (!this.chartsLoaded) {
            console.log('Loading charts in modal...');
            await this.loadStatistics();
            this.chartsLoaded = true;
        } else {
            // If charts already loaded, just refresh them
            console.log('Charts already loaded, updating...');
            await this.refresh();
        }
    },

    /**
     * Load statistics and render charts
     */
    async loadStatistics() {
        try {
            const stats = await API.getStatistics();

            // Render all charts
            Charts.renderAll(stats);

            console.log('Statistics loaded and charts rendered');
        } catch (error) {
            console.error('Failed to load statistics:', error);
            // Don't show alert for statistics failures - charts will just be empty
        }
    },

    /**
     * Refresh statistics and charts
     */
    async refresh() {
        try {
            const stats = await API.getStatistics();
            Charts.destroyAll();
            Charts.renderAll(stats);
            console.log('Charts refreshed');
        } catch (error) {
            console.error('Failed to refresh charts:', error);
        }
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    PapersCharts.init();
});

// Expose for debugging
window.PapersCharts = PapersCharts;
