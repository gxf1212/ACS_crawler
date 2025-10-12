"""SQLite-based storage implementation for papers and jobs."""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import json

from ..config import DATA_DIR, get_logger
from ..models.paper import Paper, PaperMetadata, Author, CrawlJob, JobStatus


class SQLiteStorage:
    """SQLite-based storage for papers and crawl jobs.

    This implementation uses SQLite for better performance, scalability,
    and query capabilities compared to JSON files.

    Attributes:
        db_path: Path to SQLite database file
        logger: Logger instance
    """

    def __init__(self, db_path: Optional[Path] = None) -> None:
        """Initialize SQLite storage.

        Args:
            db_path: Custom path for database file (default: data/acs_papers.db)
        """
        self.db_path = db_path or DATA_DIR / "acs_papers.db"
        self.logger = get_logger(self.__class__.__name__)
        self._init_database()

    def _init_database(self) -> None:
        """Initialize database schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Papers table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS papers (
                    paper_id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    doi TEXT NOT NULL,
                    url TEXT NOT NULL,
                    abstract TEXT,
                    publication_date TEXT,
                    journal TEXT,
                    volume TEXT,
                    issue TEXT,
                    pages TEXT,
                    is_open_access INTEGER DEFAULT 0,
                    oa_pdf_url TEXT,
                    crawled_at TEXT NOT NULL,
                    raw_html TEXT
                )
            """)

            # Authors table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS authors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    paper_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    affiliation TEXT,
                    email TEXT,
                    author_order INTEGER,
                    FOREIGN KEY (paper_id) REFERENCES papers(paper_id) ON DELETE CASCADE
                )
            """)

            # Keywords table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS keywords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    paper_id TEXT NOT NULL,
                    keyword TEXT NOT NULL,
                    FOREIGN KEY (paper_id) REFERENCES papers(paper_id) ON DELETE CASCADE
                )
            """)

            # Jobs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    journal_url TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    started_at TEXT,
                    completed_at TEXT,
                    total_papers INTEGER DEFAULT 0,
                    crawled_papers INTEGER DEFAULT 0,
                    failed_papers INTEGER DEFAULT 0,
                    error_message TEXT,
                    max_results INTEGER
                )
            """)

            # Add max_results column if it doesn't exist (for existing databases)
            try:
                cursor.execute("ALTER TABLE jobs ADD COLUMN max_results INTEGER")
                self.logger.info("Added max_results column to jobs table")
            except sqlite3.OperationalError:
                # Column already exists
                pass

            # Add is_open_access column if it doesn't exist (for existing databases)
            try:
                cursor.execute("ALTER TABLE papers ADD COLUMN is_open_access INTEGER DEFAULT 0")
                self.logger.info("Added is_open_access column to papers table")
            except sqlite3.OperationalError:
                # Column already exists
                pass

            # Add oa_pdf_url column if it doesn't exist (for existing databases)
            try:
                cursor.execute("ALTER TABLE papers ADD COLUMN oa_pdf_url TEXT")
                self.logger.info("Added oa_pdf_url column to papers table")
            except sqlite3.OperationalError:
                # Column already exists
                pass

            # Create indexes for better query performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_papers_journal ON papers(journal)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_papers_date ON papers(publication_date)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_authors_paper ON authors(paper_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status)")

            conn.commit()
            self.logger.info(f"Database initialized at {self.db_path}")

    # Paper operations

    def save_paper(self, paper: Paper) -> bool:
        """Save or update a paper.

        Args:
            paper: Paper object to save

        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                # Insert or replace paper
                cursor.execute("""
                    INSERT OR REPLACE INTO papers
                    (paper_id, title, doi, url, abstract, publication_date,
                     journal, volume, issue, pages, is_open_access, oa_pdf_url, crawled_at, raw_html)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    paper.paper_id,
                    paper.metadata.title,
                    paper.metadata.doi,
                    paper.metadata.url,
                    paper.metadata.abstract,
                    paper.metadata.publication_date,
                    paper.metadata.journal,
                    paper.metadata.volume,
                    paper.metadata.issue,
                    paper.metadata.pages,
                    1 if paper.metadata.is_open_access else 0,
                    paper.metadata.oa_pdf_url,
                    paper.crawled_at.isoformat(),
                    paper.raw_html,
                ))

                # Delete existing authors and keywords
                cursor.execute("DELETE FROM authors WHERE paper_id = ?", (paper.paper_id,))
                cursor.execute("DELETE FROM keywords WHERE paper_id = ?", (paper.paper_id,))

                # Insert authors
                for idx, author in enumerate(paper.metadata.authors):
                    cursor.execute("""
                        INSERT INTO authors (paper_id, name, affiliation, email, author_order)
                        VALUES (?, ?, ?, ?, ?)
                    """, (paper.paper_id, author.name, author.affiliation, author.email, idx))

                # Insert keywords
                for keyword in paper.metadata.keywords:
                    cursor.execute("""
                        INSERT INTO keywords (paper_id, keyword)
                        VALUES (?, ?)
                    """, (paper.paper_id, keyword))

                conn.commit()
                self.logger.info(f"Saved paper: {paper.paper_id}")
                return True

        except Exception as e:
            self.logger.error(f"Failed to save paper {paper.paper_id}: {e}")
            return False

    def get_paper(self, paper_id: str) -> Optional[Paper]:
        """Retrieve a paper by ID.

        Args:
            paper_id: Paper ID (DOI)

        Returns:
            Paper object or None if not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                # Get paper
                cursor.execute("SELECT * FROM papers WHERE paper_id = ?", (paper_id,))
                row = cursor.fetchone()

                if not row:
                    return None

                # Get authors
                cursor.execute("""
                    SELECT name, affiliation, email
                    FROM authors
                    WHERE paper_id = ?
                    ORDER BY author_order
                """, (paper_id,))
                authors = [Author(name=r['name'], affiliation=r['affiliation'], email=r['email'])
                          for r in cursor.fetchall()]

                # Get keywords
                cursor.execute("SELECT keyword FROM keywords WHERE paper_id = ?", (paper_id,))
                keywords = [r['keyword'] for r in cursor.fetchall()]

                # Build Paper object
                # Note: sqlite3.Row doesn't have .get() method, use try/except or check keys
                try:
                    is_open_access = bool(row['is_open_access'])
                except (KeyError, TypeError):
                    is_open_access = False

                try:
                    oa_pdf_url = row['oa_pdf_url']
                except (KeyError, TypeError):
                    oa_pdf_url = None

                metadata = PaperMetadata(
                    title=row['title'],
                    doi=row['doi'],
                    url=row['url'],
                    authors=authors,
                    abstract=row['abstract'],
                    publication_date=row['publication_date'],
                    journal=row['journal'],
                    volume=row['volume'],
                    issue=row['issue'],
                    pages=row['pages'],
                    keywords=keywords,
                    is_open_access=is_open_access,
                    oa_pdf_url=oa_pdf_url,
                )

                return Paper(
                    paper_id=row['paper_id'],
                    metadata=metadata,
                    crawled_at=datetime.fromisoformat(row['crawled_at']),
                    raw_html=row['raw_html'],
                )

        except Exception as e:
            self.logger.error(f"Failed to get paper {paper_id}: {e}")
            return None

    def get_all_papers(self, limit: Optional[int] = None) -> List[Paper]:
        """Retrieve all papers.

        Args:
            limit: Maximum number of papers to return (None for all)

        Returns:
            List of Paper objects
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                query = "SELECT paper_id FROM papers ORDER BY crawled_at DESC"
                if limit:
                    query += f" LIMIT {limit}"

                cursor.execute(query)
                paper_ids = [row['paper_id'] for row in cursor.fetchall()]

                return [self.get_paper(pid) for pid in paper_ids if self.get_paper(pid)]

        except Exception as e:
            self.logger.error(f"Failed to get all papers: {e}")
            return []

    def paper_exists(self, paper_id: str) -> bool:
        """Check if a paper exists.

        Args:
            paper_id: Paper ID (DOI)

        Returns:
            True if paper exists, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1 FROM papers WHERE paper_id = ?", (paper_id,))
                return cursor.fetchone() is not None
        except Exception as e:
            self.logger.error(f"Failed to check paper existence: {e}")
            return False

    def search_papers(self, query: str, limit: int = 50) -> List[Paper]:
        """Search papers by title, abstract, or authors.

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of matching Paper objects
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                search_term = f"%{query}%"
                cursor.execute("""
                    SELECT DISTINCT p.paper_id
                    FROM papers p
                    LEFT JOIN authors a ON p.paper_id = a.paper_id
                    WHERE p.title LIKE ?
                       OR p.abstract LIKE ?
                       OR a.name LIKE ?
                    ORDER BY p.crawled_at DESC
                    LIMIT ?
                """, (search_term, search_term, search_term, limit))

                paper_ids = [row['paper_id'] for row in cursor.fetchall()]
                return [self.get_paper(pid) for pid in paper_ids if self.get_paper(pid)]

        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            return []

    # Job operations

    def save_job(self, job: CrawlJob) -> bool:
        """Save or update a crawl job.

        Args:
            job: CrawlJob object to save

        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT OR REPLACE INTO jobs
                    (job_id, journal_url, status, created_at, started_at,
                     completed_at, total_papers, crawled_papers, failed_papers, error_message, max_results)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    job.job_id,
                    job.journal_url,
                    job.status.value,
                    job.created_at.isoformat(),
                    job.started_at.isoformat() if job.started_at else None,
                    job.completed_at.isoformat() if job.completed_at else None,
                    job.total_papers,
                    job.crawled_papers,
                    job.failed_papers,
                    job.error_message,
                    job.max_results,
                ))

                conn.commit()
                self.logger.info(f"Saved job: {job.job_id}")
                return True

        except Exception as e:
            self.logger.error(f"Failed to save job {job.job_id}: {e}")
            return False

    def get_job(self, job_id: str) -> Optional[CrawlJob]:
        """Retrieve a job by ID.

        Args:
            job_id: Job ID

        Returns:
            CrawlJob object or None if not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM jobs WHERE job_id = ?", (job_id,))
                row = cursor.fetchone()

                if not row:
                    return None

                return CrawlJob(
                    job_id=row['job_id'],
                    journal_url=row['journal_url'],
                    status=JobStatus(row['status']),
                    created_at=datetime.fromisoformat(row['created_at']),
                    started_at=datetime.fromisoformat(row['started_at']) if row['started_at'] else None,
                    completed_at=datetime.fromisoformat(row['completed_at']) if row['completed_at'] else None,
                    total_papers=row['total_papers'],
                    crawled_papers=row['crawled_papers'],
                    failed_papers=row['failed_papers'],
                    error_message=row['error_message'],
                    max_results=row['max_results'],
                )

        except Exception as e:
            self.logger.error(f"Failed to get job {job_id}: {e}")
            return None

    def get_all_jobs(self) -> List[CrawlJob]:
        """Retrieve all jobs.

        Returns:
            List of CrawlJob objects, sorted by creation date (newest first)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute("SELECT job_id FROM jobs ORDER BY created_at DESC")
                job_ids = [row['job_id'] for row in cursor.fetchall()]

                return [self.get_job(jid) for jid in job_ids if self.get_job(jid)]

        except Exception as e:
            self.logger.error(f"Failed to get all jobs: {e}")
            return []

    def get_jobs_by_status(self, status: JobStatus) -> List[CrawlJob]:
        """Retrieve jobs by status.

        Args:
            status: Job status to filter by

        Returns:
            List of CrawlJob objects with the specified status
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT job_id FROM jobs WHERE status = ? ORDER BY created_at DESC",
                    (status.value,)
                )
                job_ids = [row['job_id'] for row in cursor.fetchall()]

                return [self.get_job(jid) for jid in job_ids if self.get_job(jid)]

        except Exception as e:
            self.logger.error(f"Failed to get jobs by status: {e}")
            return []

    def get_statistics(self) -> dict:
        """Get database statistics.

        Returns:
            Dictionary with statistics
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()

                stats = {}

                # Total papers
                cursor.execute("SELECT COUNT(*) FROM papers")
                stats['total_papers'] = cursor.fetchone()[0]

                # Papers with abstracts
                cursor.execute("SELECT COUNT(*) FROM papers WHERE abstract IS NOT NULL AND abstract != ''")
                stats['papers_with_abstracts'] = cursor.fetchone()[0]

                # Total jobs
                cursor.execute("SELECT COUNT(*) FROM jobs")
                stats['total_jobs'] = cursor.fetchone()[0]

                # Jobs by status
                for status in JobStatus:
                    cursor.execute("SELECT COUNT(*) FROM jobs WHERE status = ?", (status.value,))
                    stats[f'jobs_{status.value}'] = cursor.fetchone()[0]

                # Papers by journal
                cursor.execute("""
                    SELECT journal, COUNT(*) as count
                    FROM papers
                    WHERE journal IS NOT NULL
                    GROUP BY journal
                    ORDER BY count DESC
                """)
                stats['papers_by_journal'] = dict(cursor.fetchall())

                return stats

        except Exception as e:
            self.logger.error(f"Failed to get statistics: {e}")
            return {}
