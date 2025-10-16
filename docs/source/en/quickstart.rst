Quick Start
===========

This guide will get you up and running with ACS Paper Crawler in minutes.

Prerequisites
-------------

**Option 1: Docker (Recommended)**

* Docker 20.10 or higher
* Docker Compose 2.0 or higher

**Option 2: Local Installation**

* Python 3.9 or higher
* Chrome browser
* pip package manager

Installation
------------

Option 1: Docker (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Clone the repository::

    git clone https://github.com/gxf1212/ACS_crawler.git
    cd ACS_crawler

2. Start with Docker Compose::

    docker compose up -d

3. Open your browser::

    http://localhost:8000

That's it! Docker will automatically install Chrome, ChromeDriver, and all dependencies.

Option 2: Local Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Clone the repository::

    git clone https://github.com/gxf1212/ACS_crawler.git
    cd ACS_crawler

2. Install dependencies::

    pip install -r requirements.txt

3. Run the application::

    python run.py

4. Open your browser::

    http://localhost:8000

You should see the dashboard with statistics and charts.

First Crawl
-----------

1. On the dashboard, select a journal from the dropdown (e.g., "JACS - Journal of the American Chemical Society")
2. Click "Start Crawling"
3. Monitor progress in the Jobs page
4. View crawled papers in the Papers page

Next Steps
----------

* Read :doc:`installation` for detailed setup options
* Learn about :doc:`usage` for advanced features
* Explore :doc:`api` for API integration
