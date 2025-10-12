/**
 * Charts Module
 * Handles all chart creation and rendering
 */

const Charts = {
    // Color palette for consistent theming
    colors: {
        primary: ['#0d6efd', '#198754', '#dc3545', '#ffc107', '#0dcaf0',
                  '#6f42c1', '#fd7e14', '#20c997', '#e83e8c', '#6c757d'],
        success: '#198754',
        warning: '#ffc107',
        info: '#0dcaf0',
        danger: '#dc3545'
    },

    // Chart instances for cleanup
    instances: {},

    /**
     * Create Papers by Journal doughnut chart
     */
    createJournalChart(canvasId, data) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        // Destroy existing chart if any
        if (this.instances[canvasId]) {
            this.instances[canvasId].destroy();
        }

        const labels = Object.keys(data);
        const values = Object.values(data);

        this.instances[canvasId] = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: this.colors.primary,
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            boxWidth: 12,
                            font: { size: 10 },
                            padding: 10
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((value / total) * 100).toFixed(1);
                                return `${label}: ${value} (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });

        return this.instances[canvasId];
    },

    /**
     * Create Top Authors horizontal bar chart
     */
    createAuthorsChart(canvasId, authorsData) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        if (this.instances[canvasId]) {
            this.instances[canvasId].destroy();
        }

        const topAuthors = authorsData.slice(0, 10);
        const labels = topAuthors.map(a => a.name);
        const values = topAuthors.map(a => a.count);

        this.instances[canvasId] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Papers',
                    data: values,
                    backgroundColor: this.colors.primary[0],
                    borderColor: this.colors.primary[0],
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.parsed.x} papers`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        ticks: { stepSize: 1 }
                    }
                }
            }
        });

        return this.instances[canvasId];
    },

    /**
     * Create Timeline line chart
     */
    createTimelineChart(canvasId, timeData) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        if (this.instances[canvasId]) {
            this.instances[canvasId].destroy();
        }

        const labels = Object.keys(timeData);
        const values = Object.values(timeData);

        this.instances[canvasId] = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Papers Crawled',
                    data: values,
                    borderColor: this.colors.success,
                    backgroundColor: 'rgba(25, 135, 84, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 4,
                    pointHoverRadius: 6
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 10 }
                    }
                },
                interaction: {
                    mode: 'nearest',
                    axis: 'x',
                    intersect: false
                }
            }
        });

        return this.instances[canvasId];
    },

    /**
     * Create Publication Years bar chart
     */
    createPublicationYearsChart(canvasId, yearData) {
        const ctx = document.getElementById(canvasId);
        if (!ctx) return null;

        if (this.instances[canvasId]) {
            this.instances[canvasId].destroy();
        }

        const labels = Object.keys(yearData);
        const values = Object.values(yearData);

        this.instances[canvasId] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Papers Published',
                    data: values,
                    backgroundColor: this.colors.warning,
                    borderColor: this.colors.warning,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return `${context.parsed.y} papers`;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: { stepSize: 5 }
                    }
                }
            }
        });

        return this.instances[canvasId];
    },

    /**
     * Destroy all chart instances
     */
    destroyAll() {
        Object.values(this.instances).forEach(chart => {
            if (chart) chart.destroy();
        });
        this.instances = {};
    },

    /**
     * Render all charts from statistics data
     */
    renderAll(stats) {
        this.createJournalChart('journalChart', stats.papers_by_journal);
        this.createAuthorsChart('authorsChart', stats.top_authors);
        this.createTimelineChart('timelineChart', stats.papers_by_month);
        this.createPublicationYearsChart('pubYearChart', stats.publication_years);
    }
};

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = Charts;
}
