"""ACS Crawler - A professional crawler for American Chemical Society papers."""

__version__ = "0.1.1"
__author__ = "ACS Crawler Team"

from .models.paper import Paper, PaperMetadata
from .scrapers.selenium_scraper import SeleniumScraper
from .scrapers.paper_scraper import PaperScraper

__all__ = [
    "Paper",
    "PaperMetadata",
    "SeleniumScraper",
    "PaperScraper",
]
