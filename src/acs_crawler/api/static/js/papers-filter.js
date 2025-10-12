/**
 * Papers Filter Module
 * Handles filtering and sorting of papers
 */

const PapersFilter = {
    // Store original paper elements
    papers: [],
    filters: {
        search: '',
        journal: '',
        year: '',
        abstract: ''
    },
    sortBy: 'date-desc',

    /**
     * Initialize the filter system
     */
    init() {
        console.log('Initializing papers filter...');

        // Store all paper elements
        this.papers = Array.from(document.querySelectorAll('.paper-card'));

        // Populate filter dropdowns
        this.populateFilters();

        // Setup event listeners
        this.setupEventListeners();

        // Initial count
        this.updateCounts();

        console.log(`Loaded ${this.papers.length} papers`);
    },

    /**
     * Populate filter dropdown options
     */
    populateFilters() {
        // Get unique journals
        const journals = new Set();
        const years = new Set();

        this.papers.forEach(paper => {
            const journal = paper.dataset.journal;
            const year = paper.dataset.year;

            if (journal) journals.add(journal);
            if (year) years.add(year);
        });

        // Populate journal filter
        const journalFilter = document.getElementById('journalFilter');
        Array.from(journals).sort().forEach(journal => {
            const option = document.createElement('option');
            option.value = journal;
            option.textContent = journal;
            journalFilter.appendChild(option);
        });

        // Populate year filter
        const yearFilter = document.getElementById('yearFilter');
        Array.from(years).sort().reverse().forEach(year => {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            yearFilter.appendChild(option);
        });
    },

    /**
     * Setup event listeners
     */
    setupEventListeners() {
        // Search input with debounce
        const searchInput = document.getElementById('searchInput');
        if (searchInput) {
            searchInput.addEventListener('input', UI.debounce((e) => {
                this.filters.search = e.target.value.toLowerCase();
                this.applyFilters();
            }, 300));
        }

        // Journal filter
        const journalFilter = document.getElementById('journalFilter');
        if (journalFilter) {
            journalFilter.addEventListener('change', (e) => {
                this.filters.journal = e.target.value;
                this.applyFilters();
            });
        }

        // Year filter
        const yearFilter = document.getElementById('yearFilter');
        if (yearFilter) {
            yearFilter.addEventListener('change', (e) => {
                this.filters.year = e.target.value;
                this.applyFilters();
            });
        }

        // Abstract filter
        const abstractFilter = document.getElementById('abstractFilter');
        if (abstractFilter) {
            abstractFilter.addEventListener('change', (e) => {
                this.filters.abstract = e.target.value;
                this.applyFilters();
            });
        }

        // Sort select
        const sortSelect = document.getElementById('sortSelect');
        if (sortSelect) {
            sortSelect.addEventListener('change', (e) => {
                this.sortBy = e.target.value;
                this.sortPapers();
            });
        }

        // Clear filters button
        const clearFilters = document.getElementById('clearFilters');
        if (clearFilters) {
            clearFilters.addEventListener('click', () => {
                this.clearFilters();
            });
        }
    },

    /**
     * Apply all filters
     */
    applyFilters() {
        let visibleCount = 0;

        this.papers.forEach(paper => {
            let visible = true;

            // Search filter (title, authors, DOI, abstract)
            if (this.filters.search) {
                const searchTerm = this.filters.search;
                const matchesTitle = paper.dataset.title.includes(searchTerm);
                const matchesAuthors = paper.dataset.authors.includes(searchTerm);
                const matchesDoi = paper.dataset.doi.includes(searchTerm);
                const matchesAbstract = paper.dataset.abstract.includes(searchTerm);

                visible = matchesTitle || matchesAuthors || matchesDoi || matchesAbstract;
            }

            // Journal filter
            if (visible && this.filters.journal) {
                visible = paper.dataset.journal === this.filters.journal;
            }

            // Year filter
            if (visible && this.filters.year) {
                visible = paper.dataset.year === this.filters.year;
            }

            // Abstract filter
            if (visible && this.filters.abstract) {
                if (this.filters.abstract === 'with') {
                    visible = paper.dataset.hasAbstract === 'yes';
                } else if (this.filters.abstract === 'without') {
                    visible = paper.dataset.hasAbstract === 'no';
                }
            }

            // Show or hide paper
            paper.style.display = visible ? '' : 'none';
            if (visible) visibleCount++;
        });

        // Update counts
        this.updateCounts(visibleCount);

        // Show/hide no results message
        this.toggleNoResults(visibleCount === 0);

        // Update active filters display
        this.updateActiveFilters();
    },

    /**
     * Sort papers
     */
    sortPapers() {
        const container = document.getElementById('papersList');
        if (!container) return;

        const visiblePapers = this.papers.filter(p => p.style.display !== 'none');

        visiblePapers.sort((a, b) => {
            switch (this.sortBy) {
                case 'date-desc':
                    return b.dataset.crawled.localeCompare(a.dataset.crawled);

                case 'date-asc':
                    return a.dataset.crawled.localeCompare(b.dataset.crawled);

                case 'title-asc':
                    return a.dataset.title.localeCompare(b.dataset.title);

                case 'title-desc':
                    return b.dataset.title.localeCompare(a.dataset.title);

                case 'journal':
                    return a.dataset.journal.localeCompare(b.dataset.journal);

                default:
                    return 0;
            }
        });

        // Reorder in DOM
        visiblePapers.forEach(paper => {
            container.appendChild(paper);
        });
    },

    /**
     * Clear all filters
     */
    clearFilters() {
        // Reset filter values
        this.filters = {
            search: '',
            journal: '',
            year: '',
            abstract: ''
        };

        // Reset form elements
        const searchInput = document.getElementById('searchInput');
        const journalFilter = document.getElementById('journalFilter');
        const yearFilter = document.getElementById('yearFilter');
        const abstractFilter = document.getElementById('abstractFilter');

        if (searchInput) searchInput.value = '';
        if (journalFilter) journalFilter.value = '';
        if (yearFilter) yearFilter.value = '';
        if (abstractFilter) abstractFilter.value = '';

        // Reapply filters (will show all)
        this.applyFilters();
    },

    /**
     * Update paper counts
     */
    updateCounts(filteredCount) {
        const totalCount = this.papers.length;
        const filtered = filteredCount !== undefined ? filteredCount : totalCount;

        // Update badges
        const totalCountEl = document.getElementById('totalCount');
        const filteredCountEl = document.getElementById('filteredCount');
        const resultCountEl = document.getElementById('resultCount');

        if (totalCountEl) totalCountEl.textContent = totalCount;
        if (filteredCountEl) filteredCountEl.textContent = filtered;
        if (resultCountEl) resultCountEl.textContent = filtered;
    },

    /**
     * Toggle no results message
     */
    toggleNoResults(show) {
        const noResultsCard = document.getElementById('noResultsCard');
        const papersContainer = document.getElementById('papersContainer');

        if (noResultsCard) {
            noResultsCard.style.display = show ? 'block' : 'none';
        }
        if (papersContainer) {
            papersContainer.style.opacity = show ? '0.5' : '1';
        }
    },

    /**
     * Update active filters display
     */
    updateActiveFilters() {
        const activeFiltersRow = document.getElementById('activeFiltersRow');
        const activeFilterBadges = document.getElementById('activeFilterBadges');

        if (!activeFiltersRow || !activeFilterBadges) return;

        const badges = [];

        // Add badges for active filters
        if (this.filters.search) {
            badges.push(`
                <span class="badge bg-primary me-1">
                    <i class="bi bi-search"></i> "${this.filters.search}"
                    <i class="bi bi-x" style="cursor: pointer;" onclick="PapersFilter.removeFilter('search')"></i>
                </span>
            `);
        }

        if (this.filters.journal) {
            badges.push(`
                <span class="badge bg-info me-1">
                    <i class="bi bi-journal"></i> ${this.filters.journal}
                    <i class="bi bi-x" style="cursor: pointer;" onclick="PapersFilter.removeFilter('journal')"></i>
                </span>
            `);
        }

        if (this.filters.year) {
            badges.push(`
                <span class="badge bg-success me-1">
                    <i class="bi bi-calendar"></i> ${this.filters.year}
                    <i class="bi bi-x" style="cursor: pointer;" onclick="PapersFilter.removeFilter('year')"></i>
                </span>
            `);
        }

        if (this.filters.abstract) {
            const abstractText = this.filters.abstract === 'with' ? 'With Abstract' : 'Without Abstract';
            badges.push(`
                <span class="badge bg-warning me-1">
                    <i class="bi bi-file-text"></i> ${abstractText}
                    <i class="bi bi-x" style="cursor: pointer;" onclick="PapersFilter.removeFilter('abstract')"></i>
                </span>
            `);
        }

        // Show/hide active filters row
        if (badges.length > 0) {
            activeFilterBadges.innerHTML = badges.join('');
            activeFiltersRow.style.display = 'block';
        } else {
            activeFiltersRow.style.display = 'none';
        }
    },

    /**
     * Remove specific filter
     */
    removeFilter(filterName) {
        this.filters[filterName] = '';

        // Reset corresponding input
        const elementMap = {
            search: 'searchInput',
            journal: 'journalFilter',
            year: 'yearFilter',
            abstract: 'abstractFilter'
        };

        const elementId = elementMap[filterName];
        const element = document.getElementById(elementId);
        if (element) {
            element.value = '';
        }

        // Reapply filters
        this.applyFilters();
    }
};

/**
 * Search by keyword (called from badge clicks)
 */
function searchKeyword(keyword) {
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.value = keyword;
        PapersFilter.filters.search = keyword.toLowerCase();
        PapersFilter.applyFilters();
        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    PapersFilter.init();
});

// Expose for debugging
window.PapersFilter = PapersFilter;
