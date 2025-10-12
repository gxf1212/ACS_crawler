Installation
============

This guide provides detailed installation instructions for different operating systems.

System Requirements
-------------------

* **Python**: 3.9 or higher
* **Chrome Browser**: Latest stable version
* **Memory**: 4GB RAM minimum (8GB recommended)
* **Disk Space**: 500MB for application + database

Step 1: Install Python
-----------------------

**Ubuntu/Debian**::

    sudo apt update
    sudo apt install python3.9 python3-pip

**macOS**::

    # Using Homebrew
    brew install python@3.9

**Windows**:

Download from https://www.python.org/downloads/ and run the installer.
Make sure to check "Add Python to PATH" during installation.

Step 2: Install Chrome Browser
-------------------------------

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

Step 3: Install ACS Crawler
----------------------------

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

Step 4: ChromeDriver Setup
---------------------------

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
----------------------------

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
-----------------------

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

Docker Installation (Alternative)
----------------------------------

For containerized deployment::

    # Pull image (when available)
    docker pull ghcr.io/gxf1212/acs_crawler:latest

    # Or build from source
    docker build -t acs_crawler .

    # Run container
    docker run -p 8000:8000 -v $(pwd)/data:/app/data acs_crawler

Troubleshooting
---------------

Chrome not found
~~~~~~~~~~~~~~~~

**Error**: ``Chrome binary not found``

**Solution**:

* Verify Chrome installation: ``google-chrome --version`` (Linux/macOS) or check "Add or Remove Programs" (Windows)
* On Linux servers, ensure X11 libraries are installed: ``sudo apt install xvfb``

ChromeDriver version mismatch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error**: ``ChromeDriver version X.Y doesn't match Chrome version A.B``

**Solution**:

* Use auto-download (default, recommended)
* Or manually download matching version from https://chromedriver.chromium.org/downloads
* Check versions: ``google-chrome --version`` and ``chromedriver --version``

Port 8000 already in use
~~~~~~~~~~~~~~~~~~~~~~~~~

**Error**: ``Address already in use``

**Solution**:

Change port in ``run.py``::

    uvicorn.run(app, host="0.0.0.0", port=8080)  # Use 8080 instead

Permission denied (ChromeDriver)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Error**: ``Permission denied: chromedriver``

**Solution (Linux/macOS)**::

    chmod +x /path/to/chromedriver

Import errors
~~~~~~~~~~~~~

**Error**: ``ModuleNotFoundError``

**Solution**::

    # Ensure you're in the correct environment
    conda activate acs_crawler

    # Reinstall dependencies
    pip install -r requirements.txt --force-reinstall

Database locked
~~~~~~~~~~~~~~~

**Error**: ``database is locked``

**Solution**:

* Ensure only one instance is running
* Check for stale lock files in ``data/``
* Restart the application

Getting Help
------------

If you encounter issues not covered here:

* 📚 Check the `Troubleshooting Guide <troubleshooting.html>`_
* 🐛 `Report an Issue <https://github.com/gxf1212/ACS_crawler/issues>`_
* 💬 `Ask in Discussions <https://github.com/gxf1212/ACS_crawler/discussions>`_
