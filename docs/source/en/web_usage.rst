Web Interface Guide
===================

This guide covers the web-based user interface for ACS Paper Crawler.

Dashboard
---------

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
--------------------

Method 1: Select from Journal List
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Choose a journal from the dropdown (43 journals available)
2. (Optional) Set max_results to limit papers
3. Click "Start Crawling"
4. Monitor progress in Jobs page

Method 2: Custom URL
~~~~~~~~~~~~~~~~~~~~~

Enter any ACS journal URL::

    https://pubs.acs.org/toc/JOURNAL_CODE/current

Examples:

* ``https://pubs.acs.org/toc/jacsat/current`` (JACS)
* ``https://pubs.acs.org/toc/jmcmar/current`` (J. Med. Chem.)

Browsing Papers
---------------

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
-------------

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
--------------

Export papers to CSV:

1. Navigate to Papers page
2. Click "Export CSV" button
3. Save the file

CSV includes: DOI, title, authors, journal, volume, issue, pages, publication date, abstract, keywords, URL.

Best Practices
--------------

* **Rate Limiting**: Avoid running too many jobs simultaneously (1-2 concurrent max)
* **max_results**: Use to limit papers for testing (e.g., 10-50 papers)
* **Monitoring**: Check job status regularly in Jobs page
* **Data Management**: Export data periodically as backup
* **Respect ToS**: Follow ACS terms of service, don't overload their servers
