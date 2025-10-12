Installation
============

Requirements
------------

* Python 3.9 or higher
* Chrome browser
* ChromeDriver (auto-downloaded if not configured)

Basic Installation
------------------

Install from source::

    git clone https://github.com/gxf1212/ACS_crawler.git
    cd ACS_crawler
    pip install -r requirements.txt

Optional: ChromeDriver Configuration
-------------------------------------

By default, ChromeDriver is automatically downloaded. To use a custom path:

1. Download ChromeDriver from https://chromedriver.chromium.org/downloads
2. Extract to a directory (e.g., ``/usr/local/bin/chromedriver``)
3. Edit ``src/acs_crawler/config.py``::

    CHROMEDRIVER_PATH: Optional[str] = "/path/to/chromedriver"

Virtual Environment (Recommended)
----------------------------------

Using conda::

    conda create -n acs_crawler python=3.9
    conda activate acs_crawler
    pip install -r requirements.txt

Or using mamba (faster)::

    mamba create -n acs_crawler python=3.9
    mamba activate acs_crawler
    pip install -r requirements.txt

Verifying Installation
----------------------

Test the installation::

    python run.py

Visit http://localhost:8000 - you should see the dashboard.

Troubleshooting
---------------

**ChromeDriver version mismatch**

If you see errors about ChromeDriver version:

* Let it auto-download (recommended)
* Or manually download matching version

**Port 8000 already in use**

Change the port in ``run.py``::

    uvicorn.run(app, host="0.0.0.0", port=8080)
