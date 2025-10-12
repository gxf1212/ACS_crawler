"""Selenium-based scraper for bypassing anti-bot protection.

This scraper uses a real browser to fetch pages, which bypasses most
anti-scraping measures. It's slower but more reliable for protected sites.
"""

from typing import List, Optional
import time

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

from ..config import get_logger, CHROMEDRIVER_PATH


class SeleniumScraper:
    """Browser-based scraper using Selenium.

    This scraper uses Selenium with Chrome to fetch pages, which appears
    as a real browser to the server and bypasses anti-bot protection.

    Example:
        >>> scraper = SeleniumScraper()
        >>> papers = scraper.get_paper_urls("https://pubs.acs.org/toc/jctcce/current")
        >>> print(f"Found {len(papers)} papers")
        >>> scraper.close()

    Note:
        Requires selenium and webdriver-manager packages:
        pip install selenium webdriver-manager
    """

    def __init__(self, headless: bool = True) -> None:
        """Initialize the Selenium scraper.

        Args:
            headless: Run browser in headless mode (no GUI)

        Raises:
            ImportError: If selenium is not installed
        """
        if not SELENIUM_AVAILABLE:
            raise ImportError(
                "Selenium is not installed. Install with: "
                "pip install selenium webdriver-manager"
            )

        self.logger = get_logger(self.__class__.__name__)
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None
        self._init_driver()

    def _init_driver(self) -> None:
        """Initialize the Chrome WebDriver."""
        options = Options()

        if self.headless:
            options.add_argument("--headless=new")

        # Enhanced anti-detection options
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-web-security")
        options.add_argument("--allow-running-insecure-content")

        # More realistic Linux user agent
        options.add_argument(
            "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        # Exclude automation flags and logging
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option("useAutomationExtension", False)

        # Add preferences to appear more human
        prefs = {
            "profile.default_content_setting_values.notifications": 2,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }
        options.add_experimental_option("prefs", prefs)

        try:
            # Use configured ChromeDriver path or auto-download
            if CHROMEDRIVER_PATH:
                import os
                if os.path.exists(CHROMEDRIVER_PATH):
                    service = Service(CHROMEDRIVER_PATH)
                    self.logger.info(f"Using ChromeDriver from: {CHROMEDRIVER_PATH}")
                else:
                    self.logger.warning(
                        f"Configured ChromeDriver path does not exist: {CHROMEDRIVER_PATH}. "
                        "Falling back to auto-download."
                    )
                    service = Service(ChromeDriverManager().install())
            else:
                self.logger.info("Auto-downloading ChromeDriver...")
                service = Service(ChromeDriverManager().install())

            self.driver = webdriver.Chrome(service=service, options=options)

            # Execute CDP commands to hide automation (enhanced stealth)
            self.driver.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {
                    "source": """
                        Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                        Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                        Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
                        window.chrome = {runtime: {}};
                    """
                },
            )

            self.logger.info("Selenium WebDriver initialized successfully")

        except Exception as e:
            self.logger.error(f"Failed to initialize WebDriver: {e}")
            raise

    def fetch_page(self, url: str, wait_time: int = 15) -> Optional[str]:
        """Fetch a webpage using Selenium.

        Args:
            url: URL to fetch
            wait_time: Maximum time to wait for page load (seconds)

        Returns:
            HTML content as string, or None if failed
        """
        if not self.driver:
            self.logger.error("WebDriver not initialized")
            return None

        try:
            self.logger.info(f"Fetching {url} with Selenium")
            self.driver.get(url)

            # Wait for the page to load - different selectors for different page types
            try:
                if "/toc/" in url:
                    # Journal issue page - wait for issue items
                    WebDriverWait(self.driver, wait_time).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "issue-item"))
                    )
                    self.logger.info("Journal page loaded successfully")
                    time.sleep(2)
                elif "/doi/" in url:
                    # Paper page - wait for title element in page body
                    WebDriverWait(self.driver, wait_time).until(
                        EC.presence_of_element_located((By.TAG_NAME, "h1"))
                    )
                    self.logger.info("Paper page content loaded successfully")

                    # Simulate human behavior with scrolling to bypass anti-bot detection
                    self.logger.info("Simulating human scrolling behavior")
                    self.driver.execute_script("window.scrollTo(0, 500);")
                    time.sleep(1)
                    self.driver.execute_script("window.scrollTo(0, 1000);")
                    time.sleep(1)
                    self.driver.execute_script("window.scrollTo(0, 0);")
                    time.sleep(1)

                    # Wait for JavaScript to populate meta tags
                    self.logger.info("Waiting for metadata to load")
                    time.sleep(8)
                else:
                    # Generic page - just wait for body
                    WebDriverWait(self.driver, wait_time).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    self.logger.info("Page loaded successfully")
                    time.sleep(2)
            except Exception as e:
                self.logger.warning(f"Timeout waiting for page elements: {e}")
                # Continue anyway - we'll get whatever loaded

            html = self.driver.page_source
            self.logger.info(f"Retrieved {len(html)} bytes of HTML")
            return html

        except Exception as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None

    def get_paper_urls(self, journal_url: str) -> List[str]:
        """Extract paper URLs from a journal page.

        Args:
            journal_url: URL of the journal issue page

        Returns:
            List of paper URLs
        """
        html = self.fetch_page(journal_url)
        if not html:
            return []

        # Use BeautifulSoup to parse the HTML
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "lxml")
        paper_urls = []
        seen_dois = set()

        # Find all issue items
        issue_items = soup.find_all("div", class_="issue-item")
        self.logger.info(f"Found {len(issue_items)} issue items")

        for item in issue_items:
            title_elem = item.find("h3", class_="issue-item_title")
            if title_elem:
                link = title_elem.find("a", href=True)
                if link:
                    url = link["href"]

                    # Extract DOI
                    if "/doi/" in url:
                        doi = url.split("/doi/")[-1].split("?")[0].split("#")[0]

                        if doi not in seen_dois:
                            seen_dois.add(doi)
                            # Ensure full URL
                            if not url.startswith("http"):
                                url = f"https://pubs.acs.org{url}"
                            paper_urls.append(url)

        self.logger.info(f"Extracted {len(paper_urls)} unique paper URLs")
        return paper_urls

    def get_papers_with_journal_metadata(self, journal_url: str) -> List[dict]:
        """Extract paper URLs and metadata from journal page.

        Args:
            journal_url: URL of the journal issue page

        Returns:
            List of dicts with 'url', 'doi', 'title', 'authors', 'abstract', and 'publication_date' keys
        """
        html = self.fetch_page(journal_url)
        if not html:
            return []

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html, "lxml")
        papers_data = []
        seen_dois = set()

        # Find all issue items
        issue_items = soup.find_all("div", class_="issue-item")
        self.logger.info(f"Found {len(issue_items)} issue items")

        for item in issue_items:
            title_elem = item.find("h3", class_="issue-item_title")
            if title_elem:
                link = title_elem.find("a", href=True)
                if link:
                    url = link["href"]
                    title = link.text.strip()

                    # Extract DOI
                    if "/doi/" in url:
                        doi = url.split("/doi/")[-1].split("?")[0].split("#")[0]

                        if doi not in seen_dois:
                            seen_dois.add(doi)
                            # Ensure full URL
                            if not url.startswith("http"):
                                url = f"https://pubs.acs.org{url}"

                            # Extract authors
                            authors = []
                            author_list = item.find("ul", class_="issue-item_loa")
                            if author_list:
                                for author_elem in author_list.find_all("span", class_="hlFld-ContribAuthor"):
                                    given_names_elem = author_elem.find("given-names")
                                    surname_elem = author_elem.find("surname")
                                    if given_names_elem and surname_elem:
                                        full_name = f"{given_names_elem.text.strip()} {surname_elem.text.strip()}"
                                        authors.append(full_name)

                            # Extract publication date
                            publication_date = None
                            pub_date_elem = item.find("span", class_="pub-date-value")
                            if pub_date_elem:
                                publication_date = pub_date_elem.text.strip()

                            # Extract abstract if available
                            abstract = None
                            abstract_elem = item.find("span", class_="hlFld-Abstract")
                            if abstract_elem:
                                # Get text from all paragraphs in abstract
                                abstract_text = abstract_elem.get_text(separator=" ", strip=True)
                                if abstract_text:
                                    abstract = abstract_text[:5000]  # Limit length

                            # Extract journal metadata
                            journal = None
                            journal_elem = item.find("span", class_="issue-item_jour-name")
                            if journal_elem:
                                journal_text = journal_elem.get_text(strip=True)
                                if journal_text:
                                    journal = journal_text

                            # Extract volume
                            volume = None
                            volume_elem = item.find("span", class_="issue-item_vol-num")
                            if volume_elem:
                                volume = volume_elem.get_text(strip=True)

                            # Extract issue number
                            issue = None
                            issue_elem = item.find("span", class_="issue-item_issue-num")
                            if issue_elem:
                                issue = issue_elem.get_text(strip=True)

                            # Extract pages
                            pages = None
                            pages_elem = item.find("span", class_="issue-item_page-range")
                            if pages_elem:
                                pages_text = pages_elem.get_text(strip=True)
                                # Clean up the text (remove comma and nbsp)
                                if pages_text:
                                    pages = pages_text.replace(',', '').replace('\xa0', '').strip()

                            papers_data.append({
                                "url": url,
                                "doi": doi,
                                "title": title,
                                "authors": authors,
                                "abstract": abstract,
                                "publication_date": publication_date,
                                "journal": journal,
                                "volume": volume,
                                "issue": issue,
                                "pages": pages
                            })

        self.logger.info(f"Extracted {len(papers_data)} papers with metadata from journal page")
        return papers_data

    def extract_doi_from_url(self, url: str) -> Optional[str]:
        """Extract DOI from a paper URL.

        Args:
            url: Paper URL

        Returns:
            DOI string or None if not found
        """
        if "/doi/" not in url:
            return None

        parts = url.split("/doi/")
        if len(parts) < 2:
            return None

        doi = parts[1].split("?")[0].split("#")[0]
        return doi if doi else None

    def save_page(self, url: str, output_path: str) -> bool:
        """Fetch and save a page to a file.

        Args:
            url: URL to fetch
            output_path: Path to save HTML file

        Returns:
            True if successful, False otherwise
        """
        html = self.fetch_page(url)
        if not html:
            return False

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html)
            self.logger.info(f"Saved page to {output_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save page: {e}")
            return False

    def reinit_driver(self) -> None:
        """Reinitialize the WebDriver.

        Closes the existing driver and creates a fresh one.
        Useful for recovering from stale driver states between jobs.
        """
        self.logger.info("Reinitializing WebDriver...")
        self.close()
        self._init_driver()
        self.logger.info("WebDriver reinitialized successfully")

    def close(self) -> None:
        """Close the browser and cleanup resources."""
        if self.driver:
            try:
                self.driver.quit()
                self.logger.info("WebDriver closed")
            except Exception as e:
                self.logger.error(f"Error closing WebDriver: {e}")

    def __enter__(self) -> "SeleniumScraper":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        """Context manager exit."""
        self.close()


if __name__ == "__main__":
    from ..config import setup_logging

    setup_logging()

    if not SELENIUM_AVAILABLE:
        print("ERROR: Selenium not installed!")
        print("Install with: pip install selenium webdriver-manager")
        exit(1)

    # Test the scraper
    print("=" * 70)
    print("Testing Selenium Scraper")
    print("=" * 70)

    test_url = "https://pubs.acs.org/toc/jctcce/current"

    with SeleniumScraper(headless=True) as scraper:
        print(f"\nFetching: {test_url}")
        print("-" * 70)

        paper_urls = scraper.get_paper_urls(test_url)

        if paper_urls:
            print(f"\n✅ SUCCESS! Found {len(paper_urls)} papers")
            print(f"\nFirst 5 papers:")
            for i, url in enumerate(paper_urls[:5], 1):
                doi = scraper.extract_doi_from_url(url)
                print(f"  {i}. DOI: {doi}")
        else:
            print("\n⚠️ No papers found")

    print("\n" + "=" * 70)
