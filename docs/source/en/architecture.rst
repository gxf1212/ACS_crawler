Architecture
============

Project Structure
-----------------

::

    ACS_crawler/
    ├── src/acs_crawler/
    │   ├── api/              # FastAPI web interface
    │   │   ├── main.py       # Routes and endpoints
    │   │   ├── static/       # CSS, JS, images
    │   │   └── templates/    # Jinja2 HTML templates
    │   ├── models/           # Data models
    │   │   └── paper.py      # Paper, Job, Author models
    │   ├── scrapers/         # Scraping engines
    │   │   ├── selenium_scraper.py    # Browser automation
    │   │   └── paper_scraper.py       # Paper metadata extraction
    │   ├── storage/          # Data persistence
    │   │   └── sqlite_storage.py      # SQLite backend
    │   ├── config.py         # Configuration
    │   └── crawler_service.py # Main orchestration
    ├── data/                 # SQLite database
    ├── logs/                 # Application logs
    └── docs/                 # Documentation

Technology Stack
----------------

Backend
~~~~~~~

* **FastAPI**: Modern Python web framework
* **SQLite**: Lightweight database
* **Selenium**: Browser automation
* **BeautifulSoup4**: HTML parsing
* **Pydantic**: Data validation

Frontend
~~~~~~~~

* **Bootstrap 5**: UI framework
* **Chart.js**: Data visualization
* **Vanilla JavaScript**: Modular architecture
* **Jinja2**: Template engine

Database Schema
---------------

**papers**

* paper_id (PK)
* title, doi, url
* abstract, publication_date
* journal, volume, issue, pages
* crawled_at, raw_html

**authors**

* id (PK)
* paper_id (FK)
* name, affiliation, email
* author_order

**keywords**

* id (PK)
* paper_id (FK)
* keyword

**jobs**

* job_id (PK)
* journal_url, status
* created_at, started_at, completed_at
* total_papers, crawled_papers, failed_papers
* error_message, max_results

Workflow
--------

1. User creates crawl job via web interface
2. Job queued in background with status=PENDING
3. CrawlerService starts job (status=RUNNING):
   
   a. Initialize Selenium driver
   b. Fetch journal page
   c. Extract paper URLs and metadata
   d. Apply max_results limit if set
   e. For each paper:
      
      * Check if exists (skip if yes)
      * Get metadata from paper page (or use journal page fallback)
      * Save to database
      * Update job progress

4. Job completes (status=COMPLETED/FAILED)
5. User views papers and stats in dashboard
