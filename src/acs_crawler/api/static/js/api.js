/**
 * API Service Module
 * Handles all API calls to the backend
 */

const API = {
    BASE_URL: '/api',

    /**
     * Fetch journals list
     */
    async getJournals() {
        try {
            const response = await fetch(`${this.BASE_URL}/journals`);
            if (!response.ok) throw new Error('Failed to fetch journals');
            return await response.json();
        } catch (error) {
            console.error('Error fetching journals:', error);
            throw error;
        }
    },

    /**
     * Fetch statistics data
     */
    async getStatistics() {
        try {
            const response = await fetch(`${this.BASE_URL}/statistics`);
            if (!response.ok) throw new Error('Failed to fetch statistics');
            return await response.json();
        } catch (error) {
            console.error('Error fetching statistics:', error);
            throw error;
        }
    },

    /**
     * Create a new crawl job
     */
    async createJob(journalUrl, maxResults = null) {
        try {
            const body = { journal_url: journalUrl };
            if (maxResults !== null && maxResults !== undefined) {
                body.max_results = maxResults;
            }

            const response = await fetch(`${this.BASE_URL}/jobs`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(body)
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to create job');
            }

            return await response.json();
        } catch (error) {
            console.error('Error creating job:', error);
            throw error;
        }
    },

    /**
     * Get all jobs
     */
    async getJobs() {
        try {
            const response = await fetch(`${this.BASE_URL}/jobs`);
            if (!response.ok) throw new Error('Failed to fetch jobs');
            return await response.json();
        } catch (error) {
            console.error('Error fetching jobs:', error);
            throw error;
        }
    },

    /**
     * Get specific job by ID
     */
    async getJob(jobId) {
        try {
            const response = await fetch(`${this.BASE_URL}/jobs/${jobId}`);
            if (!response.ok) throw new Error('Job not found');
            return await response.json();
        } catch (error) {
            console.error('Error fetching job:', error);
            throw error;
        }
    },

    /**
     * Get all papers
     */
    async getPapers() {
        try {
            const response = await fetch(`${this.BASE_URL}/papers`);
            if (!response.ok) throw new Error('Failed to fetch papers');
            return await response.json();
        } catch (error) {
            console.error('Error fetching papers:', error);
            throw error;
        }
    },

    /**
     * Get specific paper by ID
     */
    async getPaper(paperId) {
        try {
            const response = await fetch(`${this.BASE_URL}/papers/${encodeURIComponent(paperId)}`);
            if (!response.ok) throw new Error('Paper not found');
            return await response.json();
        } catch (error) {
            console.error('Error fetching paper:', error);
            throw error;
        }
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API;
}
