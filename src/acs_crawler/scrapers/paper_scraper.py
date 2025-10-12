"""Paper scraper for extracting metadata from ACS paper pages."""

import re
from typing import List, Optional

from bs4 import BeautifulSoup

from ..config import get_logger
from ..models.paper import Author, PaperMetadata


class PaperScraper:
    """Scraper for extracting metadata from ACS paper pages using Selenium.

    Example:
        >>> from selenium_scraper import SeleniumScraper
        >>> selenium_scraper = SeleniumScraper()
        >>> scraper = PaperScraper(selenium_scraper)
        >>> url = "https://pubs.acs.org/doi/10.1021/acs.jmedchem.5c01432"
        >>> metadata = scraper.get_paper_metadata(url)
        >>> print(metadata.title)
    """

    def __init__(self, selenium_scraper) -> None:
        """Initialize paper scraper with Selenium driver.

        Args:
            selenium_scraper: SeleniumScraper instance to use for fetching pages
        """
        self.selenium_scraper = selenium_scraper
        self.logger = get_logger(self.__class__.__name__)

    def get_paper_metadata(self, paper_url: str) -> Optional[PaperMetadata]:
        """Extract complete metadata from a paper page.

        Args:
            paper_url: Full URL to the paper page

        Returns:
            PaperMetadata object or None if extraction failed

        Raises:
            ValueError: If paper_url is invalid
        """
        if not paper_url or not paper_url.startswith("http"):
            raise ValueError(f"Invalid paper URL: {paper_url}")

        html = self.selenium_scraper.fetch_page(paper_url)
        if not html:
            self.logger.error(f"Failed to fetch paper page: {paper_url}")
            return None

        soup = BeautifulSoup(html, "lxml")

        try:
            # Extract DOI from URL or page
            doi = self._extract_doi(soup, paper_url)
            if not doi:
                self.logger.error(f"Could not extract DOI from {paper_url}")
                return None

            # Extract title
            title = self._extract_title(soup)
            if not title:
                self.logger.error(f"Could not extract title from {paper_url}")
                return None

            # Extract other metadata
            authors = self._extract_authors(soup)
            abstract = self._extract_abstract(soup)
            publication_date = self._extract_publication_date(soup)
            journal_info = self._extract_journal_info(soup)
            keywords = self._extract_keywords(soup)
            is_open_access = self._extract_open_access_status(soup)
            oa_pdf_url = self._extract_pdf_url(doi, is_open_access)

            metadata = PaperMetadata(
                title=title,
                doi=doi,
                url=paper_url,
                authors=authors,
                abstract=abstract,
                publication_date=publication_date,
                journal=journal_info.get("journal"),
                volume=journal_info.get("volume"),
                issue=journal_info.get("issue"),
                pages=journal_info.get("pages"),
                keywords=keywords,
                is_open_access=is_open_access,
                oa_pdf_url=oa_pdf_url,
            )

            self.logger.info(f"Successfully extracted metadata for DOI: {doi}")
            return metadata

        except Exception as e:
            self.logger.error(f"Error extracting metadata from {paper_url}: {e}")
            return None

    def _extract_doi(self, soup, paper_url: str) -> Optional[str]:
        """Extract DOI from the page or URL."""
        # Try meta tag first
        doi_meta = soup.find("meta", {"name": "dc.Identifier", "scheme": "doi"})
        if doi_meta and doi_meta.get("content"):
            return doi_meta["content"]

        # Try from URL
        if "/doi/" in paper_url:
            parts = paper_url.split("/doi/")
            if len(parts) >= 2:
                return parts[1].split("?")[0].split("#")[0]

        return None

    def _extract_title(self, soup) -> Optional[str]:
        """Extract paper title."""
        # Try different selectors
        title_selectors = [
            ("meta", {"name": "dc.Title"}),
            ("h1", {"class": "article_header-title"}),
            ("span", {"class": "hlFld-Title"}),
            ("h1", {}),
        ]

        for tag_name, attrs in title_selectors:
            element = soup.find(tag_name, attrs)
            if element:
                if tag_name == "meta":
                    title = element.get("content")
                else:
                    title = element.get_text(strip=True)

                if title:
                    return title

        return None

    def _extract_authors(self, soup) -> List[Author]:
        """Extract author information."""
        authors = []

        # Try to find author information in meta tags or specific divs
        author_elements = soup.find_all("meta", {"name": "dc.Creator"})

        if author_elements:
            for author_elem in author_elements:
                name = author_elem.get("content", "").strip()
                if name:
                    authors.append(Author(name=name))
        else:
            # Alternative: look for author names in specific classes
            author_divs = soup.select('span[property="author"] span[property="name"]')
            for author_div in author_divs:
                name = author_div.get_text(strip=True)
                if name:
                    authors.append(Author(name=name))

        return authors

    def _extract_abstract(self, soup) -> Optional[str]:
        """Extract paper abstract."""
        # Try different abstract selectors
        abstract_selectors = [
            ("meta", {"name": "dc.Description"}),
            ("div", {"class": "article_abstract"}),
            ("div", {"class": "abstractSection"}),
            ("section", {"class": "article-section__abstract"}),
        ]

        for tag_name, attrs in abstract_selectors:
            element = soup.find(tag_name, attrs)
            if element:
                if tag_name == "meta":
                    abstract = element.get("content", "")
                else:
                    # Get text but remove abstract heading if present
                    abstract = element.get_text(separator=" ", strip=True)
                    abstract = re.sub(r"^Abstract[:\s]*", "", abstract, flags=re.IGNORECASE)

                if abstract:
                    return abstract[:5000]  # Limit length

        return None

    def _extract_publication_date(self, soup) -> Optional[str]:
        """Extract publication date."""
        date_meta = soup.find("meta", {"name": "dc.Date"})
        if date_meta:
            return date_meta.get("content")

        # Alternative: look for publication date in the page
        date_pattern = r"\d{4}-\d{2}-\d{2}"
        date_elements = soup.find_all(string=re.compile(date_pattern))
        if date_elements:
            match = re.search(date_pattern, date_elements[0])
            if match:
                return match.group(0)

        return None

    def _extract_journal_info(self, soup) -> dict:
        """Extract journal, volume, issue, and page information."""
        info = {}

        # Journal name
        journal_meta = soup.find("meta", {"name": "dc.Publisher"})
        if journal_meta:
            info["journal"] = journal_meta.get("content")

        # Look for citation text that contains volume/issue/page
        citation = soup.find("div", {"class": "citation"})
        if citation:
            citation_text = citation.get_text(strip=True)

            # Extract volume (pattern: "Vol. 68")
            volume_match = re.search(r"Vol(?:ume)?\.?\s*(\d+)", citation_text, re.IGNORECASE)
            if volume_match:
                info["volume"] = volume_match.group(1)

            # Extract issue (pattern: "No. 19")
            issue_match = re.search(r"(?:No|Issue)\.?\s*(\d+)", citation_text, re.IGNORECASE)
            if issue_match:
                info["issue"] = issue_match.group(1)

            # Extract pages (pattern: "9732-9747")
            pages_match = re.search(r"(\d+)[-–](\d+)", citation_text)
            if pages_match:
                info["pages"] = f"{pages_match.group(1)}-{pages_match.group(2)}"

        return info

    def _extract_keywords(self, soup) -> List[str]:
        """Extract paper keywords."""
        keywords = []

        # Try meta keywords
        keywords_meta = soup.find("meta", {"name": "keywords"})
        if keywords_meta:
            content = keywords_meta.get("content", "")
            if content:
                keywords = [k.strip() for k in content.split(",") if k.strip()]

        # Try keyword section
        if not keywords:
            keyword_section = soup.find("div", {"class": "article-keywords"})
            if keyword_section:
                keyword_links = keyword_section.find_all("a")
                keywords = [link.get_text(strip=True) for link in keyword_links]

        return keywords

    def _extract_open_access_status(self, soup) -> bool:
        """Extract Open Access status from access control icons.

        Returns:
            True if the paper is Open Access, False otherwise
        """
        # Look for access control images with "Open Access" alt text
        access_icons = soup.find_all("img", {"class": "access__control--img"})
        for icon in access_icons:
            alt_text = icon.get("alt", "").lower()
            if "open access" in alt_text or "acs authorchoice" in alt_text:
                return True

        # Alternative: check for open access badges or labels
        oa_labels = soup.find_all(string=lambda text: text and "open access" in text.lower())
        if oa_labels:
            return True

        return False

    def _extract_pdf_url(self, doi: str, is_open_access: bool) -> Optional[str]:
        """Generate PDF download URL for Open Access papers.

        Args:
            doi: Paper DOI
            is_open_access: Whether the paper is Open Access

        Returns:
            PDF download URL if Open Access, None otherwise
        """
        if is_open_access and doi:
            return f"https://pubs.acs.org/doi/pdf/{doi}"
        return None


if __name__ == "__main__":
    # Example usage
    from ..config import setup_logging

    setup_logging()

    scraper = PaperScraper()
    try:
        test_url = "https://pubs.acs.org/doi/10.1021/acs.jmedchem.5c01432"
        metadata = scraper.get_paper_metadata(test_url)

        if metadata:
            print(f"Title: {metadata.title}")
            print(f"DOI: {metadata.doi}")
            print(f"Authors: {len(metadata.authors)}")
            if metadata.authors:
                print(f"First author: {metadata.authors[0].name}")
            print(f"Abstract length: {len(metadata.abstract) if metadata.abstract else 0}")
    finally:
        scraper.close()
