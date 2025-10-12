# Tests Directory

## Integration Tests

Located in `integration/`:

### `test_crawl_jobs.py`
Full end-to-end test of the crawling workflow:
- Creates journal issue job (JCIM)
- Creates search job (SARS-CoV-2 RdRp inhibitor)
- Monitors progress
- Analyzes metadata completeness

**Usage:**
```bash
python tests/integration/test_crawl_jobs.py
```

**Note:** Requires running API server on localhost:8000

### `test_search_job.py`
Test search functionality:
- Creates search job with date range
- Monitors progress
- Reports results

**Usage:**
```bash
python tests/integration/test_search_job.py
```

**Known Issue:** Currently fails due to Cloudflare protection on search pages

## Unit Tests

Located in `unit/`:
- TODO: Add unit tests for individual components

## Test Data

Test uses real ACS URLs:
- Journal: https://pubs.acs.org/toc/jcisd8/current
- Search: https://pubs.acs.org/action/doSearch (with parameters)

## Running All Tests

```bash
# With pytest (recommended)
pytest tests/

# Individual test
python tests/integration/test_crawl_jobs.py
```
