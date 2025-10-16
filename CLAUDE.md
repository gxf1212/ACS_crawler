# ACS Crawler Project Guide

## Project Overview
Professional web crawler for ACS Publications with FastAPI-based dashboard.

## Key Technologies
- **Backend**: FastAPI, SQLite, Selenium (anti-bot bypass)
- **Frontend**: Bootstrap 5, Chart.js, Vanilla JS
- **Scraping**: SeleniumScraper (Chromium + anti-detection)

## Architecture
```
src/acs_crawler/
├── api/            # FastAPI web interface + static assets
├── models/         # Data models (Paper, CrawlJob, Author)
├── scrapers/       # SeleniumScraper, PaperScraper
├── storage/        # SQLiteStorage with full-text search
├── data/           # acs_journals.json (43 journals)
├── config.py       # Configuration (CHROMEDRIVER_PATH, etc.)
└── crawler_service.py  # Main orchestration service
```

## Important Notes

### Selenium Configuration
- ChromeDriver path: `config.CHROMEDRIVER_PATH` (auto-downloads if None)
- Headless Chrome with anti-detection flags
- **Limitation**: Search pages blocked by Cloudflare CAPTCHA (use journal URLs instead)

### Working Features
- ✅ Journal issue crawling (37/37 success rate)
- ✅ Max results limiting
- ✅ Background job processing
- ✅ Real-time progress tracking
- ✅ SQLite with relationships (papers, authors, keywords, jobs)
- ✅ Local filtering/search in Papers UI (client-side)
- ❌ Automated search crawling (Cloudflare Turnstile protected)

### Known Issues
1. **Search URL crawling**: ACS search pages (`/action/doSearch`) are protected by Cloudflare Turnstile CAPTCHA
   - Blocks ALL automated tools (Selenium, undetected-chromedriver, curl, etc.)
   - Cannot be bypassed with current stealth techniques
   - **Workaround**: Use journal issue URLs (`/toc/` pages) which work perfectly
   - Users can filter papers locally in the Papers UI after crawling journals
   - Search tab hidden in UI (code remains for future API access)
2. **Wait times**: Page loading can take 10-15 seconds per paper

### Recent Fixes
- ✅ Metadata extraction now works correctly (title, DOI, authors, abstract, journal)

## Testing
- Integration tests: `tests/integration/`
  - `test_crawl_jobs.py` - Full workflow test
  - `test_search_job.py` - Search test (currently blocked)
- don't put tests in project root!

## Running
```bash
python run.py  # Starts on http://localhost:8000
```
