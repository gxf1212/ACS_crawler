# Known Limitations

## Technical Constraints

### 1. Selenium-Based Scraping
- **Performance**: Selenium runs a full Chrome browser instance, making it slower than pure HTTP requests
- **Resource Usage**: Higher memory and CPU consumption compared to lightweight scraping methods
- **Startup Time**: Browser initialization adds ~3-5 seconds overhead per job

### 2. Browser Requirements
- **Chrome Required**: Must have Chrome browser installed on the system
- **ChromeDriver**: Requires ChromeDriver binary (auto-downloaded by webdriver-manager, but adds complexity)
- **Headless Mode**: Runs in headless mode by default, but still requires X11 libraries on Linux servers

### 3. Data Extraction Limitations

#### Abstract Extraction
- Abstracts are extracted from individual paper pages, not the journal listing page
- This requires one additional HTTP request per paper, significantly increasing crawl time
- Some papers may not have abstracts available (early publications, corrections, etc.)

#### Metadata Availability
- Only publicly accessible metadata is extracted (no paywalled content)
- Keywords extraction depends on ACS page structure (may be empty for some papers)
- Author affiliations are not currently extracted
- Citation counts and metrics are not captured

### 4. Rate Limiting and Reliability

#### No Built-in Rate Limiting
- The crawler does not implement automatic rate limiting
- Running too many concurrent jobs may trigger ACS's anti-bot measures
- **Recommendation**: Limit to 1-2 concurrent jobs, add delays between large batches

#### Website Structure Changes
- The crawler depends on specific HTML structure of ACS pages
- Changes to ACS website layout will break scraping until code is updated
- Selectors are based on current ACS page structure (as of January 2025)

#### Error Recovery
- Failed jobs are marked as failed but not automatically retried
- Network errors during a job may result in partial data
- No automatic resume capability for interrupted jobs

### 5. Data Storage

#### SQLite Limitations
- SQLite is single-writer, limiting concurrent write operations
- Not suitable for high-traffic production deployments
- Database file size can grow large (no automatic cleanup)
- Full-text search is basic (no advanced query capabilities)

#### Data Duplication
- Papers are identified by DOI
- Re-running the same journal URL will skip existing papers
- No versioning of paper metadata (updates overwrite existing data)

### 6. Scalability Issues

#### Single-Threaded Job Processing
- Jobs are processed sequentially, not in parallel
- Long-running jobs block the queue
- No distributed processing support

#### Memory Usage
- All paper data is loaded into memory during processing
- Large journals (1000+ papers) may consume significant RAM
- No streaming or batch processing of results

### 7. ACS-Specific Limitations

#### Journal Coverage
- Only works with ACS journals (not other publishers)
- URL format must be `https://pubs.acs.org/toc/JOURNAL_CODE/current` or similar
- Special issues and supplements may have different URL patterns

#### Content Types
- Primarily designed for research articles
- May not properly handle corrections, retractions, or editorials
- Book reviews and other non-article content may be missed

### 8. Legal and Ethical Considerations

#### Terms of Service
- **IMPORTANT**: Users are responsible for complying with ACS Terms of Service
- The tool does not enforce rate limits or access restrictions
- Bulk downloading may violate publisher policies

#### Copyright
- Extracted metadata is factual data (generally not copyrighted)
- Full-text content is NOT extracted (respecting copyright)
- Users must obtain proper licenses for any downstream use

### 9. User Interface Limitations

#### Dashboard
- Charts are client-side only (no export functionality)
- Limited filtering options on dashboard
- No user authentication or multi-user support

#### Job Management
- Cannot pause/resume jobs (only cancel)
- No job scheduling or cron-like capabilities
- Limited visibility into job progress during execution

#### Export
- Only CSV export is supported (no JSON, Excel, etc.)
- Export includes all papers (no selective export)
- Large exports may timeout in browser

### 10. Development and Maintenance

#### Testing
- Limited test coverage
- No automated integration tests
- Manual testing required for ACS website changes

#### Documentation
- API documentation is basic (FastAPI auto-docs)
- Code comments could be more comprehensive
- No developer guide for extending functionality

## Workarounds and Best Practices

1. **Rate Limiting**: Manually space out crawl jobs (e.g., one per hour)
2. **Large Journals**: Use `max_results` parameter to limit papers during testing
3. **Reliability**: Monitor job status and manually retry failed jobs
4. **Performance**: Run on a machine with sufficient RAM (4GB+ recommended)
5. **Legal Compliance**: Only crawl for personal research, respect ACS ToS
6. **Database**: Periodically backup the SQLite database file
7. **Updates**: Regularly check for ACS website changes and update selectors

## Future Improvements (Not Currently Supported)

- Parallel job processing
- Automatic retry with exponential backoff
- Support for other publishers (RSC, Springer, etc.)
- PostgreSQL/MySQL backend option
- User authentication and multi-tenant support
- Job scheduling (cron-like)
- More export formats (JSON, Excel, BibTeX)
- API key authentication
- Webhooks for job completion
- Docker containerization
- CI/CD pipeline
