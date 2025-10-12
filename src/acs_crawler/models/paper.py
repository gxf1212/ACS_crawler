"""Data models for papers and crawl jobs."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List, Optional


class JobStatus(str, Enum):
    """Status of a crawl job."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class JobType(str, Enum):
    """Type of crawl job."""

    JOURNAL_ISSUE = "journal_issue"  # Crawl a specific journal issue
    SEARCH = "search"  # Search with query parameters


@dataclass
class SearchParameters:
    """Parameters for ACS search jobs.

    Attributes:
        query: Search query string (AllField parameter)
        sort_by: Sort order (e.g., 'Earliest_asc', 'Relevance', 'Earliest_desc')
        start_page: Starting page number (0-based)
        page_size: Number of results per page
        max_pages: Maximum number of pages to crawl (None for all)
        after_year: Start year for date range (e.g., 2020)
        after_month: Start month for date range (1-12)
        before_year: End year for date range (e.g., 2025)
        before_month: End month for date range (1-12)
    """

    query: str
    sort_by: str = "Relevance"
    start_page: int = 0
    page_size: int = 50
    max_pages: Optional[int] = None
    after_year: Optional[int] = None
    after_month: Optional[int] = None
    before_year: Optional[int] = None
    before_month: Optional[int] = None


@dataclass
class Author:
    """Represents a paper author.

    Attributes:
        name: Full name of the author
        affiliation: Author's institutional affiliation
        email: Author's email address (if available)
    """

    name: str
    affiliation: Optional[str] = None
    email: Optional[str] = None


@dataclass
class PaperMetadata:
    """Metadata for a scientific paper.

    Attributes:
        title: Paper title
        authors: List of paper authors
        doi: Digital Object Identifier
        abstract: Paper abstract
        publication_date: Date of publication
        journal: Journal name
        volume: Journal volume
        issue: Journal issue
        pages: Page range
        keywords: List of keywords
        url: Full URL to the paper
        is_open_access: Whether the paper is Open Access
        oa_pdf_url: Direct PDF download URL (for Open Access papers)
    """

    title: str
    doi: str
    url: str
    authors: List[Author] = field(default_factory=list)
    abstract: Optional[str] = None
    publication_date: Optional[str] = None
    journal: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    is_open_access: bool = False
    oa_pdf_url: Optional[str] = None


@dataclass
class Paper:
    """Represents a complete paper record.

    Attributes:
        paper_id: Unique identifier (DOI)
        metadata: Paper metadata
        crawled_at: Timestamp when the paper was crawled
        raw_html: Raw HTML content (optional)
    """

    paper_id: str
    metadata: PaperMetadata
    crawled_at: datetime = field(default_factory=datetime.now)
    raw_html: Optional[str] = None


@dataclass
class CrawlJob:
    """Represents a crawl job.

    Attributes:
        job_id: Unique job identifier
        journal_url: URL of the journal issue to crawl (or search URL for search jobs)
        job_type: Type of job (journal_issue or search)
        search_params: Search parameters (for search jobs only)
        status: Current job status
        created_at: Job creation timestamp
        started_at: Job start timestamp
        completed_at: Job completion timestamp
        total_papers: Total number of papers found
        crawled_papers: Number of papers successfully crawled
        failed_papers: Number of papers that failed to crawl
        error_message: Error message if job failed
        max_results: Maximum number of papers to crawl (None for unlimited)
    """

    job_id: str
    journal_url: str
    job_type: JobType = JobType.JOURNAL_ISSUE
    search_params: Optional[SearchParameters] = None
    status: JobStatus = JobStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    total_papers: int = 0
    crawled_papers: int = 0
    failed_papers: int = 0
    error_message: Optional[str] = None
    max_results: Optional[int] = None
