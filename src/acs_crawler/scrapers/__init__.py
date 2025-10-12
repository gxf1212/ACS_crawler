"""Scrapers for ACS journals and papers."""

from .selenium_scraper import SeleniumScraper
from .paper_scraper import PaperScraper

__all__ = [
    "SeleniumScraper",
    "PaperScraper",
]
