API Usage Guide
===============

This guide covers using the RESTful API for programmatic access.

API Overview
------------

The application provides a RESTful API at http://localhost:8000/api

Interactive documentation available at: http://localhost:8000/docs

Authentication
--------------

Currently, the API does not require authentication. All endpoints are accessible without tokens.

Jobs API
--------

List All Jobs
~~~~~~~~~~~~~

::

    curl http://localhost:8000/api/jobs

Response::

    [
      {
        "job_id": "job_20250112_123456_abc123",
        "journal_url": "https://pubs.acs.org/toc/jacsat/current",
        "status": "completed",
        "papers_crawled": 25,
        "total_papers": 25,
        "created_at": "2025-01-12T12:34:56",
        "completed_at": "2025-01-12T12:45:30"
      }
    ]

Get Job Details
~~~~~~~~~~~~~~~

::

    curl http://localhost:8000/api/jobs/{job_id}

Create New Job
~~~~~~~~~~~~~~

::

    curl -X POST http://localhost:8000/api/jobs \
      -H "Content-Type: application/json" \
      -d '{
        "journal_url": "https://pubs.acs.org/toc/jacsat/current",
        "max_results": 10
      }'

Parameters:

* ``journal_url`` (required): ACS journal URL
* ``max_results`` (optional): Limit number of papers to crawl

Cancel Job
~~~~~~~~~~

::

    curl -X DELETE http://localhost:8000/api/jobs/{job_id}

Papers API
----------

List All Papers
~~~~~~~~~~~~~~~

::

    curl http://localhost:8000/api/papers

Query Parameters:

* ``search``: Search in title/author/abstract
* ``journal``: Filter by journal name
* ``year``: Filter by publication year
* ``has_abstract``: true/false

Example with filters::

    curl "http://localhost:8000/api/papers?journal=JACS&year=2025&has_abstract=true"

Get Paper Details
~~~~~~~~~~~~~~~~~

::

    curl http://localhost:8000/api/papers/{doi}

Replace {doi} with URL-encoded DOI (e.g., ``10.1021/jacs.1c00001``).

Export to Excel
~~~~~~~~~~~~~~~

::

    curl http://localhost:8000/api/papers/export/xlsx -o papers.xlsx

This downloads all papers as an Excel (XLSX) file with:

* Professionally formatted headers (styled with colors)
* Auto-adjusted column widths for better readability
* Native Excel compatibility
* Proper handling of comma-separated values (authors, keywords)

Statistics API
--------------

Get Statistics
~~~~~~~~~~~~~~

::

    curl http://localhost:8000/api/stats

Response::

    {
      "total_papers": 1250,
      "total_jobs": 45,
      "completed_jobs": 40,
      "papers_by_journal": {
        "JACS": 320,
        "Org. Lett.": 180
      }
    }

Python Examples
---------------

Using requests library::

    import requests

    # Create a crawl job
    response = requests.post(
        "http://localhost:8000/api/jobs",
        json={
            "journal_url": "https://pubs.acs.org/toc/jacsat/current",
            "max_results": 10
        }
    )
    job = response.json()
    print(f"Created job: {job['job_id']}")

    # Check job status
    status = requests.get(f"http://localhost:8000/api/jobs/{job['job_id']}")
    print(status.json())

    # List papers
    papers = requests.get("http://localhost:8000/api/papers")
    for paper in papers.json():
        print(f"{paper['title']} - {paper['journal']}")

Error Handling
--------------

The API returns standard HTTP status codes:

* **200**: Success
* **201**: Created
* **400**: Bad Request (invalid parameters)
* **404**: Not Found
* **500**: Internal Server Error

Error response format::

    {
      "detail": "Error message"
    }

Rate Limiting
-------------

There are no enforced rate limits, but please:

* Space out job creation (don't create many jobs simultaneously)
* Respect ACS's terms of service
* Use ``max_results`` for testing

Complete API Reference
----------------------

For complete API documentation with all endpoints, parameters, and response schemas:

Visit http://localhost:8000/docs (FastAPI auto-generated Swagger UI)

Or see :doc:`api` for detailed reference.
