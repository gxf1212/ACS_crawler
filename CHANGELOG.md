# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-01-21

### Added
- Initial release of ACS Paper Crawler
- **43 pre-configured ACS journals** with direct links to current issues
- **Selenium-based web scraping** with ChromeDriver auto-management
- **FastAPI web dashboard** with:
  - Real-time statistics and interactive charts (Chart.js)
  - Job management with progress tracking
  - Paper browsing with advanced filtering
  - RESTful API with Swagger documentation
- **Background job processing** with async crawling
- **SQLite database** with full-text search capability
- **Complete metadata extraction**:
  - Title, DOI, authors, abstract
  - Keywords, journal name, publication date
  - Citation information
- **Docker deployment support** with Docker Compose configuration
- **Comprehensive documentation**:
  - English and Chinese README
  - Installation guides for Docker and local setup
  - API documentation at `/docs`
- **Data export** functionality to Excel format

### Known Limitations
- Search URL crawling blocked by Cloudflare CAPTCHA protection
- Sequential job processing (no parallel crawling)
- SQLite storage (not suitable for production scale)
- Only extracts publicly available metadata
- Designed specifically for ACS Publications structure

### Technical Details
- Python 3.9+ support
- Modern web technologies: FastAPI, Bootstrap 5, Chart.js
- Robust error handling and retry mechanisms
- Type hints and comprehensive logging
- Test suite with pytest

## [0.1.3] - 2025-10-21

### Changed
- **BREAKING**: Package name changed from `acs-crawler` to `acs_crawler` for PEP 625 compliance
- Install command is now: `pip install acs_crawler` (was `pip install acs-crawler`)
- PyPI URL is now: https://pypi.org/project/acs_crawler/

### Note
Old versions under `acs-crawler` name remain available but are deprecated.

## [0.1.2] - 2025-10-21

### Fixed
- Fixed screenshot images not displaying on PyPI by using GitHub absolute URLs
- Screenshots now use `https://raw.githubusercontent.com` URLs for proper display

## [0.1.1] - 2025-10-21

### Added
- **Environment-based configuration** support via `.env` files
- `.env.example` template for easy configuration setup
- `python-dotenv` dependency for config file loading
- Improved ChromeDriver path configuration system

### Changed
- ChromeDriver path can now be configured via:
  1. `CHROMEDRIVER_PATH` environment variable
  2. `.env` file in project root
  3. Auto-download (default fallback)
- Updated README with configuration examples for Windows/Linux/Mac/WSL users

### Fixed
- Windows users can now easily configure ChromeDriver path without code modification
- Better error messages when ChromeDriver path is invalid

## [Unreleased]

### Planned
- Parallel job processing
- PostgreSQL support for production deployment
- Enhanced metadata extraction (affiliations, references)
- Export formats: CSV, JSON, BibTeX
- Scheduled crawling jobs
- Email notifications

---

For more information, see the [documentation](https://acs-crawler.readthedocs.io/) or visit the [GitHub repository](https://github.com/gxf1212/ACS_crawler).
