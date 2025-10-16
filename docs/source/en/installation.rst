Installation
============

This guide provides detailed installation instructions for different operating systems.

Choose Your Installation Method
--------------------------------

This guide covers two installation methods:

* **Docker Installation (Recommended)**: Easiest setup with all dependencies pre-configured
* **Local Installation via Conda**: Full control over the environment

Docker Installation (Recommended)
----------------------------------

Docker provides an isolated, reproducible environment with Chrome, ChromeDriver, and all dependencies pre-installed.

System Requirements
~~~~~~~~~~~~~~~~~~~

* **Docker**: 20.10 or higher
* **Docker Compose**: 2.0 or higher (usually included with Docker Desktop)
* **Memory**: 4GB RAM minimum (8GB recommended)
* **Disk Space**: 500MB for application + database

Quick Start with Docker Compose
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Step 1: Install Docker**

Follow the official Docker installation guide for your platform:

* Linux: https://docs.docker.com/engine/install/
* macOS: https://docs.docker.com/desktop/install/mac-install/
* Windows: https://docs.docker.com/desktop/install/windows-install/

**Step 2: Clone and Start**::

    # Clone repository
    git clone https://github.com/gxf1212/ACS_crawler.git
    cd ACS_crawler

    # Start the application
    docker compose up -d

    # View logs
    docker compose logs -f

**Step 3: Access the Application**

Open http://localhost:8000 in your browser.

**What Docker Does:**

* Automatically installs Chrome and ChromeDriver
* Creates persistent volumes for data and logs
* Starts container on port 8000
* Automatic restart on failure
* Resource limits (2GB RAM, 2 CPUs)

**Manage Docker Container**::

    # Stop the application
    docker compose down

    # Restart
    docker compose restart

    # View logs
    docker compose logs -f

----

Local Installation via Conda
-----------------------------

For users who prefer full control over the environment.

System Requirements
~~~~~~~~~~~~~~~~~~~

* **Python**: 3.9 or higher
* **Chrome Browser**: Latest stable version
* **Memory**: 4GB RAM minimum (8GB recommended)
* **Disk Space**: 500MB for application + database

Step 1: Install Python
~~~~~~~~~~~~~~~~~~~~~~~

**Ubuntu/Debian**::

    sudo apt update
    sudo apt install python3.9 python3-pip

**macOS**::

    # Using Homebrew
    brew install python@3.9

**Windows**:

Download from https://www.python.org/downloads/ and run the installer.
Make sure to check "Add Python to PATH" during installation.

Step 2: Install ACS Crawler
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Clone the Repository
~~~~~~~~~~~~~~~~~~~~

::

    git clone https://github.com/gxf1212/ACS_crawler.git
    cd ACS_crawler

Create Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Option 1: Using Conda (Recommended)**::

    # Create environment
    conda create -n acs_crawler python=3.9

    # Activate environment
    conda activate acs_crawler

    # Install dependencies
    pip install -r requirements.txt

**Option 2: Using Mamba (Faster)**::

    # Create environment
    mamba create -n acs_crawler python=3.9

    # Activate environment
    mamba activate acs_crawler

    # Install dependencies
    pip install -r requirements.txt

Install Dependencies
~~~~~~~~~~~~~~~~~~~~

::

    pip install -r requirements.txt

This will install:

* **FastAPI**: Web framework
* **Selenium**: Browser automation
* **BeautifulSoup4**: HTML parsing
* **SQLite**: Database (built-in with Python)
* **Uvicorn**: ASGI server

Step 3: Install Chrome Browser
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The application requires Chrome browser for web scraping.

**Ubuntu/Debian**::

    # Download Chrome
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

    # Install Chrome
    sudo apt install ./google-chrome-stable_current_amd64.deb

    # Verify installation
    google-chrome --version

**CentOS/RHEL/Fedora**::

    # Add Google Chrome repository
    sudo dnf install fedora-workstation-repositories
    sudo dnf config-manager --set-enabled google-chrome

    # Install Chrome
    sudo dnf install google-chrome-stable

    # Or download directly
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
    sudo dnf install google-chrome-stable_current_x86_64.rpm

**macOS**::

    # Using Homebrew Cask
    brew install --cask google-chrome

    # Or download from https://www.google.com/chrome/

**Windows**:

Download and install from https://www.google.com/chrome/

**Headless Linux Servers**:

For servers without a display (e.g., cloud VMs), you need X11 libraries::

    # Ubuntu/Debian
    sudo apt install xvfb libxi6 libgconf-2-4

    # CentOS/RHEL
    sudo yum install xorg-x11-server-Xvfb libXi libXinerama

Step 4: ChromeDriver Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~

ChromeDriver is automatically downloaded by ``webdriver-manager``. No manual setup needed!

**Manual Configuration (Optional)**:

If you prefer to manage ChromeDriver manually:

1. Download ChromeDriver matching your Chrome version from:
   https://chromedriver.chromium.org/downloads

2. Extract the binary:

   **Linux/macOS**::

       # Extract
       unzip chromedriver_linux64.zip

       # Move to system path
       sudo mv chromedriver /usr/local/bin/

       # Make executable
       sudo chmod +x /usr/local/bin/chromedriver

   **Windows**:

   Extract ``chromedriver.exe`` to a folder (e.g., ``C:\chromedriver\``)

3. Edit ``src/acs_crawler/config.py``::

       CHROMEDRIVER_PATH: Optional[str] = "/usr/local/bin/chromedriver"  # Linux/macOS
       # or
       CHROMEDRIVER_PATH: Optional[str] = r"C:\chromedriver\chromedriver.exe"  # Windows

Step 5: Verify Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Run the Application
~~~~~~~~~~~~~~~~~~~

::

    python run.py

Expected output::

    INFO:     Started server process [12345]
    INFO:     Waiting for application startup.
    INFO:     Application startup complete.
    INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

Access the Dashboard
~~~~~~~~~~~~~~~~~~~~

Open your browser and visit:

http://localhost:8000

You should see:

* Statistics dashboard
* Interactive charts
* Journal selection dropdown
* Recent jobs and papers

Platform-Specific Notes
~~~~~~~~~~~~~~~~~~~~~~~

Ubuntu/Debian
~~~~~~~~~~~~~

**Install all prerequisites**::

    # System packages
    sudo apt update
    sudo apt install python3.9 python3-pip google-chrome-stable

    # For headless servers
    sudo apt install xvfb

**Install Conda/Mamba**::

    # Miniconda
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh

    # Mamba (via conda-forge)
    conda install mamba -n base -c conda-forge

macOS
~~~~~

**Using Homebrew**::

    # Install Homebrew (if not installed)
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # Install prerequisites
    brew install python@3.9 google-chrome

    # Install Conda
    brew install --cask miniconda

Windows
~~~~~~~

1. **Install Python**: Download from https://www.python.org/
2. **Install Chrome**: Download from https://www.google.com/chrome/
3. **Install Conda**: Download Miniconda from https://docs.conda.io/en/latest/miniconda.html

**PowerShell commands**::

    # Clone repository
    git clone https://github.com/gxf1212/ACS_crawler.git
    cd ACS_crawler

    # Create conda environment
    conda create -n acs_crawler python=3.9
    conda activate acs_crawler

    # Install dependencies
    pip install -r requirements.txt

    # Run application
    python run.py

Known Limitations
------------------

**Search URL Crawling Not Supported**

ACS search pages (``/action/doSearch``) are protected by Cloudflare Turnstile CAPTCHA that blocks all automated access:

* **Blocked**: Selenium, undetected-chromedriver, curl, and other automated tools
* **Why**: JavaScript-based challenge requires human interaction
* **Workaround**: Use journal issue URLs (``/toc/`` pages) which work perfectly

**Alternative Approach**:

Instead of crawling search results, you can:

1. Browse specific journals relevant to your research
2. Crawl journal issues that match your timeframe
3. Use the Papers UI to filter locally by keywords after crawling

Example::

    # Instead of searching for "SARS-CoV-2"
    # Crawl relevant journals like:
    - Journal of Medicinal Chemistry
    - ACS Infectious Diseases
    - Then filter in Papers UI

The local filtering in the Papers page supports searching across:

* Paper titles
* Author names
* Abstracts
* Keywords

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**ChromeDriver Issues**

*Symptom*: "ChromeDriver not found" or version mismatch

*Solutions*:

1. Let it auto-download (default behavior)
2. Or manually install:

   * Download from https://chromedriver.chromium.org/
   * Match your Chrome version
   * Update path in ``config.py``

**Selenium Timeout**

*Symptom*: "Timeout waiting for page elements"

*Causes*: Slow network, heavy server load

*Solutions*:

* Increase timeout in selenium_scraper.py (``wait_time`` parameter)
* Check internet connection
* Try again later if ACS servers are slow

**Job Fails with "No papers found"**

*Causes*:

* Invalid journal URL
* Journal page structure changed
* Network issues

*Solutions*:

* Verify URL format: ``https://pubs.acs.org/toc/CODE/current``
* Check if URL works in browser
* Report issue if structure changed

**Port Already in Use**

*Symptom*: "Address already in use"

*Solution*: Change port in ``run.py``::

    uvicorn.run(app, host="0.0.0.0", port=8080)

**Database Locked**

*Symptom*: "database is locked"

*Cause*: Multiple processes accessing database

*Solution*: Ensure only one instance is running

**Multiple Jobs Fail**

*Symptom*: Second job always fails

*Cause*: Selenium driver becomes stale

*Solution*: (Already fixed in v0.2.0) Driver reinitializes before each job

Debugging
~~~~~~~~~

**Inspect Database**::

    sqlite3 data/acs_papers.db
    SELECT * FROM jobs ORDER BY created_at DESC LIMIT 5;
    SELECT COUNT(*) FROM papers;

**Test Selenium Manually**::

    python -m acs_crawler.scrapers.selenium_scraper

Getting Help
~~~~~~~~~~~~

* 🐛 `Report an Issue <https://github.com/gxf1212/ACS_crawler/issues>`_
* 💬 `Ask in Discussions <https://github.com/gxf1212/ACS_crawler/discussions>`_
