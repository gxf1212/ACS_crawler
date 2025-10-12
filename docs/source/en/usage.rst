Usage Guide
===========

Web Interface
-------------

Dashboard
~~~~~~~~~

The dashboard provides an overview of your crawling activity:

.. figure:: /_static/index.png
   :alt: Dashboard Screenshot
   :align: center
   :width: 90%

   Main dashboard with statistics, charts, and quick access buttons

Features:

* **Statistics Cards**: Total papers, jobs, completion rates
* **Interactive Charts**: Papers by journal, top authors, timeline, publication years
* **Quick Access**: One-click buttons for frequent journals
* **Recent Activity**: Latest jobs and papers

Creating a Crawl Job
~~~~~~~~~~~~~~~~~~~~

**Method 1: Select from Journal List**

1. Choose a journal from the dropdown (43 journals available)
2. (Optional) Set max_results to limit papers
3. Click "Start Crawling"
4. Monitor progress in Jobs page

**Method 2: Custom URL**

Enter any ACS journal URL::

    https://pubs.acs.org/toc/JOURNAL_CODE/current

Examples:

* ``https://pubs.acs.org/toc/jacsat/current`` (JACS)
* ``https://pubs.acs.org/toc/jmcmar/current`` (J. Med. Chem.)

Browsing Papers
~~~~~~~~~~~~~~~

Navigate to the **Papers** page to browse and filter collected papers:

.. figure:: /_static/papers.png
   :alt: Papers List Screenshot
   :align: center
   :width: 90%

   Papers page with advanced filtering and search

How to use:

1. Navigate to **Papers** page
2. Use filters:

   * **Search**: Keywords in title/author/abstract
   * **Journal**: Select specific journal
   * **Year**: Filter by publication year
   * **Abstract**: Filter with/without abstracts

3. Sort by date, title, or journal
4. Click any paper for full details

.. figure:: /_static/paper_detail.png
   :alt: Paper Detail Screenshot
   :align: center
   :width: 90%

   Detailed paper view with complete metadata

Managing Jobs
~~~~~~~~~~~~~

Monitor and manage all crawling jobs in the **Jobs** page:

.. figure:: /_static/jobs.png
   :alt: Jobs Page Screenshot
   :align: center
   :width: 90%

   Jobs management page with status tracking and controls

Features:

* View all jobs with status indicators
* Track progress (crawled/total papers)
* Cancel pending or running jobs
* View error messages for failed jobs

Exporting Data
~~~~~~~~~~~~~~

Export papers to Excel (XLSX):

1. Navigate to Papers page
2. Click "Export Excel" button
3. Save the file

Excel file includes: DOI, title, authors, journal, volume, issue, pages, publication date, Open Access status, PDF URL, abstract, keywords, URL.

API Usage
---------

The application provides a RESTful API at http://localhost:8000/api

Interactive documentation available at: http://localhost:8000/docs

Example API calls::

    # List all jobs
    curl http://localhost:8000/api/jobs

    # Get job details
    curl http://localhost:8000/api/jobs/{job_id}

    # Create new job
    curl -X POST http://localhost:8000/api/jobs \
      -H "Content-Type: application/json" \
      -d '{"journal_url": "https://pubs.acs.org/toc/jacsat/current", "max_results": 10}'

    # List all papers
    curl http://localhost:8000/api/papers

    # Export to Excel
    curl http://localhost:8000/api/papers/export/xlsx -o papers.xlsx

See :doc:`api` for complete API reference.

Best Practices
--------------

* **Rate Limiting**: Avoid running too many jobs simultaneously
* **max_results**: Use to limit papers for testing
* **Monitoring**: Check job status regularly
* **Data Management**: Export data periodically
* **Respect ToS**: Follow ACS terms of service
