/**
 * Dashboard Module
 * Main controller for dashboard page
 */

const Dashboard = {
    /**
     * Initialize dashboard
     */
    async init() {
        console.log('Initializing dashboard...');

        try {
            // Load journals for dropdown
            await this.loadJournals();

            // Load recent/frequent journals
            await this.loadRecentJournals();

            // Load and render statistics
            await this.loadStatistics();

            // Setup event listeners
            this.setupEventListeners();

            console.log('Dashboard initialized successfully');
        } catch (error) {
            console.error('Failed to initialize dashboard:', error);
            UI.showAlert('jobAlert', 'Failed to load dashboard data', 'danger');
        }
    },

    /**
     * Load journals into dropdown
     */
    async loadJournals() {
        try {
            const data = await API.getJournals();

            if (!data.journals || data.journals.length === 0) {
                console.warn('No journals found');
                return;
            }

            // Transform data for UI
            const journalOptions = data.journals.map(journal => ({
                value: journal.url,
                label: `${journal.name} (${journal.abbreviation})`
            }));

            UI.populateSelect('journalSelect', journalOptions, 'value', 'label');

            console.log(`Loaded ${data.journals.length} journals`);
        } catch (error) {
            console.error('Failed to load journals:', error);
            UI.showAlert('jobAlert', 'Failed to load journals list', 'warning');
        }
    },

    /**
     * Load recent/frequent journals
     */
    async loadRecentJournals() {
        try {
            const stats = await API.getStatistics();
            const journalData = stats.papers_by_journal;

            if (!journalData || Object.keys(journalData).length === 0) {
                return; // No journals to show
            }

            // Sort by paper count (most frequent first)
            const sortedJournals = Object.entries(journalData)
                .sort(([, a], [, b]) => b - a)
                .slice(0, 3); // Top 3

            // Get journal URLs from journals list
            const journalsResponse = await API.getJournals();
            const journalMap = new Map();

            if (journalsResponse.journals) {
                journalsResponse.journals.forEach(j => {
                    journalMap.set(j.name, j.url);
                });
            }

            // Create badges
            const badgesContainer = document.getElementById('recentJournalBadges');
            const section = document.getElementById('recentJournalsSection');

            if (badgesContainer && sortedJournals.length > 0) {
                const badges = sortedJournals.map(([name, count]) => {
                    const url = journalMap.get(name);
                    if (!url) return '';

                    return `
                        <button class="btn btn-outline-primary btn-sm quick-journal-btn"
                                data-url="${url}"
                                onclick="Dashboard.selectQuickJournal('${url}')">
                            <i class="bi bi-journal"></i> ${name}
                            <span class="badge bg-primary rounded-pill ms-2">${count}</span>
                        </button>
                    `;
                }).filter(b => b).join('');

                if (badges) {
                    badgesContainer.innerHTML = badges;
                    section.style.display = 'block';
                }
            }

            console.log('Recent journals loaded');
        } catch (error) {
            console.error('Failed to load recent journals:', error);
            // Silent fail - not critical
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
     * Setup event listeners
     */
    setupEventListeners() {
        // Journal dropdown change
        const journalSelect = document.getElementById('journalSelect');
        if (journalSelect) {
            journalSelect.addEventListener('change', (e) => {
                this.handleJournalSelect(e.target.value);
            });
        }

        // Job creation form
        const createJobForm = document.getElementById('createJobForm');
        if (createJobForm) {
            createJobForm.addEventListener('submit', (e) => {
                this.handleJobSubmit(e);
            });
        }

        // Search job creation form
        const createSearchJobForm = document.getElementById('createSearchJobForm');
        if (createSearchJobForm) {
            createSearchJobForm.addEventListener('submit', (e) => {
                this.handleSearchJobSubmit(e);
            });
        }
    },

    /**
     * Handle journal selection
     */
    handleJournalSelect(url) {
        const urlInput = document.getElementById('journalUrl');
        if (urlInput && url) {
            urlInput.value = url;
        }
    },

    /**
     * Handle quick journal button click
     */
    selectQuickJournal(url) {
        const urlInput = document.getElementById('journalUrl');
        const journalSelect = document.getElementById('journalSelect');

        // Set URL in input
        if (urlInput) {
            urlInput.value = url;
        }

        // Try to select in dropdown too
        if (journalSelect) {
            const option = Array.from(journalSelect.options).find(opt => opt.value === url);
            if (option) {
                journalSelect.value = url;
            }
        }

        // Scroll to form
        document.getElementById('createJobForm').scrollIntoView({ behavior: 'smooth', block: 'center' });

        // Highlight the URL input briefly
        if (urlInput) {
            urlInput.focus();
            urlInput.classList.add('border-primary', 'border-3');
            setTimeout(() => {
                urlInput.classList.remove('border-primary', 'border-3');
            }, 2000);
        }
    },

    /**
     * Handle job form submission
     */
    async handleJobSubmit(event) {
        event.preventDefault();

        const urlInput = document.getElementById('journalUrl');
        const maxResultsInput = document.getElementById('journalMaxResults');
        const submitBtn = event.target.querySelector('button[type="submit"]');
        const alertDiv = 'jobAlert';

        // Validation
        const url = urlInput.value.trim();
        if (!url) {
            UI.showAlert(alertDiv, 'Please select a journal or enter a URL', 'warning');
            return;
        }

        if (!UI.isValidUrl(url)) {
            UI.showAlert(alertDiv, 'Please enter a valid URL', 'danger');
            return;
        }

        // Get max results
        const maxResults = maxResultsInput.value ? parseInt(maxResultsInput.value) : null;

        // Set loading state
        UI.setButtonLoading(submitBtn, true);
        UI.hideAlert(alertDiv);

        try {
            // Create job with max_results
            const job = await API.createJob(url, maxResults);

            // Show success message
            const limitMsg = maxResults ? ` (max ${maxResults} papers)` : '';
            UI.showAlert(
                alertDiv,
                `Job created successfully${limitMsg}! Job ID: ${job.job_id}. The page will refresh in 2 seconds...`,
                'success'
            );

            // Reload page after delay
            UI.reloadAfterDelay(2000);

        } catch (error) {
            // Show error message
            UI.showAlert(alertDiv, `Error: ${error.message}`, 'danger');

            // Reset button state
            UI.setButtonLoading(submitBtn, false, '<i class="bi bi-play-fill"></i> Start Crawling');
        }
    },

    /**
     * Refresh statistics and charts
     */
    async refreshStatistics() {
        try {
            const stats = await API.getStatistics();
            Charts.destroyAll();
            Charts.renderAll(stats);
            console.log('Statistics refreshed');
        } catch (error) {
            console.error('Failed to refresh statistics:', error);
        }
    },

    /**
     * Handle search job form submission
     */
    async handleSearchJobSubmit(event) {
        event.preventDefault();

        const queryInput = document.getElementById('searchQuery');
        const sortBy = document.getElementById('sortBy').value;
        const pageSize = document.getElementById('pageSize').value;
        const maxResultsInput = document.getElementById('searchMaxResults');
        const afterMonth = document.getElementById('afterMonth').value;
        const afterYear = document.getElementById('afterYear').value;
        const beforeMonth = document.getElementById('beforeMonth').value;
        const beforeYear = document.getElementById('beforeYear').value;
        const submitBtn = event.target.querySelector('button[type="submit"]');
        const alertDiv = 'searchJobAlert';

        // Validation
        const query = queryInput.value.trim();
        if (!query) {
            UI.showAlert(alertDiv, 'Please enter a search query', 'warning');
            return;
        }

        // Build search URL with base parameters
        let searchUrl = `https://pubs.acs.org/action/doSearch?AllField=${encodeURIComponent(query)}&sortBy=${sortBy}&startPage=0&pageSize=${pageSize}`;

        // Add date range parameters if provided
        if (afterYear) {
            searchUrl += `&AfterYear=${afterYear}`;
            if (afterMonth) {
                searchUrl += `&AfterMonth=${afterMonth}`;
            }
        }
        if (beforeYear) {
            searchUrl += `&BeforeYear=${beforeYear}`;
            if (beforeMonth) {
                searchUrl += `&BeforeMonth=${beforeMonth}`;
            }
        }

        // Get max results
        const maxResults = maxResultsInput.value ? parseInt(maxResultsInput.value) : null;

        // Set loading state
        UI.setButtonLoading(submitBtn, true);
        UI.hideAlert(alertDiv);

        try {
            // Create job using the same API endpoint with max_results
            const job = await API.createJob(searchUrl, maxResults);

            // Build success message
            const limitMsg = maxResults ? `max ${maxResults} results` : 'all results';
            let dateRangeMsg = '';
            if (afterYear || beforeYear) {
                const monthNames = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
                const fromDate = afterYear ? `${afterMonth ? monthNames[parseInt(afterMonth)] + ' ' : ''}${afterYear}` : '';
                const toDate = beforeYear ? `${beforeMonth ? monthNames[parseInt(beforeMonth)] + ' ' : ''}${beforeYear}` : '';
                if (fromDate && toDate) {
                    dateRangeMsg = `, date range: ${fromDate} to ${toDate}`;
                } else if (fromDate) {
                    dateRangeMsg = `, from: ${fromDate}`;
                } else if (toDate) {
                    dateRangeMsg = `, to: ${toDate}`;
                }
            }

            UI.showAlert(
                alertDiv,
                `Search job created! Query: "${query}", ${limitMsg}${dateRangeMsg}. Job ID: ${job.job_id}. The page will refresh in 2 seconds...`,
                'success'
            );

            // Reload page after delay
            UI.reloadAfterDelay(2000);

        } catch (error) {
            // Show error message
            UI.showAlert(alertDiv, `Error: ${error.message}`, 'danger');

            // Reset button state
            UI.setButtonLoading(submitBtn, false, '<i class="bi bi-search"></i> Start Search Crawl');
        }
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    Dashboard.init();
});

// Expose for debugging
window.Dashboard = Dashboard;
