Troubleshooting
===============

Common Issues
-------------

ChromeDriver Issues
~~~~~~~~~~~~~~~~~~~

**Symptom**: "ChromeDriver not found" or version mismatch

**Solutions**:

1. Let it auto-download (default behavior)
2. Or manually install:

   * Download from https://chromedriver.chromium.org/
   * Match your Chrome version
   * Update path in ``config.py``

Selenium Timeout
~~~~~~~~~~~~~~~~

**Symptom**: "Timeout waiting for page elements"

**Causes**: Slow network, heavy server load

**Solutions**:

* Increase timeout in selenium_scraper.py (``wait_time`` parameter)
* Check internet connection
* Try again later if ACS servers are slow

Job Fails with "No papers found"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Causes**:

* Invalid journal URL
* Journal page structure changed
* Network issues

**Solutions**:

* Verify URL format: ``https://pubs.acs.org/toc/CODE/current``
* Check if URL works in browser
* Report issue if structure changed

Port Already in Use
~~~~~~~~~~~~~~~~~~~

**Symptom**: "Address already in use"

**Solution**: Change port in ``run.py``::

    uvicorn.run(app, host="0.0.0.0", port=8080)

Database Locked
~~~~~~~~~~~~~~~

**Symptom**: "database is locked"

**Cause**: Multiple processes accessing database

**Solution**: Ensure only one instance is running

Multiple Jobs Fail
~~~~~~~~~~~~~~~~~~

**Symptom**: Second job always fails

**Cause**: Selenium driver becomes stale

**Solution**: (Already fixed in v0.2.0) Driver reinitializes before each job

Debugging
---------

Enable Debug Logging
~~~~~~~~~~~~~~~~~~~~

In ``config.py``::

    LOG_LEVEL = "DEBUG"

Check logs in ``logs/acs_crawler.log``

Inspect Database
~~~~~~~~~~~~~~~~

::

    sqlite3 data/acs_papers.db
    SELECT * FROM jobs ORDER BY created_at DESC LIMIT 5;
    SELECT COUNT(*) FROM papers;

Test Selenium Manually
~~~~~~~~~~~~~~~~~~~~~~~

::

    python -m acs_crawler.scrapers.selenium_scraper

Getting Help
------------

* Check :doc:`usage` for detailed instructions
* Review logs in ``logs/`` directory
* Report bugs on GitHub Issues
* Ask questions in GitHub Discussions
