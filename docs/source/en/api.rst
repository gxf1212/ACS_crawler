API Reference
=============

REST API Endpoints
------------------

All API endpoints are prefixed with ``/api``.

Jobs
~~~~

**POST /api/jobs**

Create a new crawl job.

Request body::

    {
        "journal_url": "https://pubs.acs.org/toc/jacsat/current",
        "max_results": 10  // optional
    }

Response: Job object with ``job_id``, ``status``, etc.

**GET /api/jobs**

List all jobs. Returns array of job objects.

**GET /api/jobs/{job_id}**

Get job details by ID.

**DELETE /api/jobs/{job_id}**

Cancel a running or pending job.

Papers
~~~~~~

**GET /api/papers**

List all crawled papers. Returns array of paper objects.

**GET /api/papers/{paper_id}**

Get paper details by ID (DOI).

**GET /api/papers/export/csv**

Export all papers to CSV format. Returns downloadable CSV file.

Other Endpoints
~~~~~~~~~~~~~~~

**GET /api/journals**

Get list of 43 ACS journals with codes and URLs.

**GET /api/statistics**

Get statistics for dashboard charts:

* Total papers/jobs
* Papers by journal
* Top authors
* Publication timeline
* Papers by year

Web Pages
---------

**GET /**

Dashboard with statistics and charts.

**GET /jobs**

Jobs management page.

**GET /papers**

Papers list with advanced filtering.

**GET /papers/{paper_id}**

Paper detail page.

Interactive API Documentation
-----------------------------

Visit http://localhost:8000/docs for Swagger UI with interactive API testing.
