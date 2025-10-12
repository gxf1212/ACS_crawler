"""Crawler service for orchestrating paper crawling operations."""

import uuid
from datetime import datetime
from typing import Optional

from .config import get_logger
from .models.paper import CrawlJob, JobStatus, Paper
from .scrapers.selenium_scraper import SeleniumScraper
from .scrapers.paper_scraper import PaperScraper
from .storage.sqlite_storage import SQLiteStorage


class CrawlerService:
    """Service for managing crawl operations.

    This service orchestrates the workflow of:
    1. Getting paper URLs from journal pages
    2. Scraping metadata from each paper
    3. Storing results

    Attributes:
        storage: Storage backend for persistence
        journal_scraper: Scraper for journal pages (Selenium-based)
        paper_scraper: Scraper for paper pages
        logger: Logger instance
    """

    def __init__(self, storage: Optional[SQLiteStorage] = None) -> None:
        """Initialize the crawler service.

        Args:
            storage: Storage backend (defaults to SQLiteStorage)
        """
        self.storage = storage or SQLiteStorage()
        self.selenium_scraper = SeleniumScraper(headless=True)
        self.journal_scraper = self.selenium_scraper  # Alias for compatibility
        self.paper_scraper = PaperScraper(self.selenium_scraper)
        self.logger = get_logger(self.__class__.__name__)

    def create_job(self, journal_url: str, max_results: Optional[int] = None) -> CrawlJob:
        """Create a new crawl job.

        Args:
            journal_url: URL of the journal issue to crawl
            max_results: Maximum number of papers to crawl (None for unlimited)

        Returns:
            Created CrawlJob object

        Raises:
            ValueError: If journal_url is invalid
        """
        if not journal_url or not journal_url.startswith("http"):
            raise ValueError(f"Invalid journal URL: {journal_url}")

        job = CrawlJob(
            job_id=str(uuid.uuid4()),
            journal_url=journal_url,
            status=JobStatus.PENDING,
            max_results=max_results,
        )

        self.storage.save_job(job)
        self.logger.info(f"Created job {job.job_id} for {journal_url} (max_results={max_results})")
        return job

    def run_job(self, job_id: str) -> CrawlJob:
        """Execute a crawl job.

        Args:
            job_id: ID of the job to run

        Returns:
            Updated CrawlJob object

        Raises:
            ValueError: If job not found
        """
        job = self.storage.get_job(job_id)
        if not job:
            raise ValueError(f"Job not found: {job_id}")

        if job.status != JobStatus.PENDING:
            self.logger.warning(f"Job {job_id} is not pending (status: {job.status})")
            return job

        # Update job status to running
        job.status = JobStatus.RUNNING
        job.started_at = datetime.now()
        self.storage.save_job(job)

        try:
            # Reinitialize Selenium driver for fresh start
            self.logger.info("Reinitializing Selenium driver for job")
            self.selenium_scraper.reinit_driver()

            # Step 1: Get papers with basic metadata from journal page
            self.logger.info(f"Fetching papers with metadata from {job.journal_url}")
            papers_data = self.journal_scraper.get_papers_with_journal_metadata(job.journal_url)

            # Apply max_results limit if specified
            if job.max_results is not None and job.max_results > 0:
                original_count = len(papers_data)
                papers_data = papers_data[:job.max_results]
                self.logger.info(f"Limiting crawl from {original_count} to {len(papers_data)} papers (max_results={job.max_results})")

            job.total_papers = len(papers_data)
            self.storage.save_job(job)

            if not papers_data:
                raise Exception("No papers found on journal page")

            self.logger.info(f"Found {len(papers_data)} papers to crawl")

            # Step 2: Crawl each paper
            for i, paper_data in enumerate(papers_data, 1):
                paper_url = paper_data["url"]
                doi = paper_data["doi"]
                journal_title = paper_data["title"]
                journal_authors = paper_data.get("authors", [])
                journal_abstract = paper_data.get("abstract")
                journal_pub_date = paper_data.get("publication_date")
                journal_name = paper_data.get("journal")
                journal_volume = paper_data.get("volume")
                journal_issue = paper_data.get("issue")
                journal_pages = paper_data.get("pages")

                self.logger.info(f"Crawling paper {i}/{len(papers_data)}: {doi}")

                try:
                    # Skip if already exists
                    if self.storage.paper_exists(doi):
                        self.logger.info(f"Paper {doi} already exists, skipping")
                        job.crawled_papers += 1
                        self.storage.save_job(job)
                        continue

                    # Try to get full metadata from paper page
                    metadata = self.paper_scraper.get_paper_metadata(paper_url)

                    # Fallback: Use journal page metadata if paper page fails
                    if not metadata or metadata.title == "pubs.acs.org":
                        self.logger.warning(f"Paper page metadata failed for {doi}, using journal page data")
                        from .models.paper import PaperMetadata, Author

                        # Convert author names to Author objects
                        author_objects = [Author(name=name) for name in journal_authors]

                        metadata = PaperMetadata(
                            doi=doi,
                            title=journal_title,
                            url=paper_url,
                            authors=author_objects,
                            abstract=journal_abstract,
                            publication_date=journal_pub_date,
                            journal=journal_name,
                            volume=journal_volume,
                            issue=journal_issue,
                            pages=journal_pages
                        )

                    # Save paper
                    paper = Paper(paper_id=doi, metadata=metadata)
                    if self.storage.save_paper(paper):
                        job.crawled_papers += 1
                    else:
                        job.failed_papers += 1

                    self.storage.save_job(job)

                except Exception as e:
                    self.logger.error(f"Error crawling {paper_url}: {e}")
                    job.failed_papers += 1
                    self.storage.save_job(job)

            # Mark job as completed
            job.status = JobStatus.COMPLETED
            job.completed_at = datetime.now()
            self.storage.save_job(job)

            self.logger.info(
                f"Job {job_id} completed: "
                f"{job.crawled_papers}/{job.total_papers} papers crawled, "
                f"{job.failed_papers} failed"
            )

        except Exception as e:
            self.logger.error(f"Job {job_id} failed: {e}")
            job.status = JobStatus.FAILED
            job.error_message = str(e)
            job.completed_at = datetime.now()
            self.storage.save_job(job)

        return job

    def get_job_status(self, job_id: str) -> Optional[CrawlJob]:
        """Get the current status of a job.

        Args:
            job_id: Job ID

        Returns:
            CrawlJob object or None if not found
        """
        return self.storage.get_job(job_id)

    def list_all_jobs(self) -> list:
        """List all crawl jobs.

        Returns:
            List of all CrawlJob objects, sorted by creation date (newest first)
        """
        jobs = self.storage.get_all_jobs()
        return sorted(jobs, key=lambda j: j.created_at, reverse=True)

    def list_all_papers(self) -> list:
        """List all crawled papers.

        Returns:
            List of all Paper objects, sorted by crawl date (newest first)
        """
        papers = self.storage.get_all_papers()
        return sorted(papers, key=lambda p: p.crawled_at, reverse=True)

    def get_paper(self, paper_id: str) -> Optional[Paper]:
        """Get a specific paper by ID.

        Args:
            paper_id: Paper ID (DOI)

        Returns:
            Paper object or None if not found
        """
        return self.storage.get_paper(paper_id)

    def cleanup(self) -> None:
        """Cleanup resources."""
        self.selenium_scraper.close()
        self.logger.info("Crawler service cleaned up")

    def __enter__(self) -> "CrawlerService":
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        """Context manager exit."""
        self.cleanup()
