"""Configuration module for ACS Crawler."""

import logging
import sys
from pathlib import Path
from typing import Final, Optional

# Project paths
PROJECT_ROOT: Final[Path] = Path(__file__).parent.parent.parent
DATA_DIR: Final[Path] = PROJECT_ROOT / "data"
CACHE_DIR: Final[Path] = PROJECT_ROOT / "cache"
LOGS_DIR: Final[Path] = PROJECT_ROOT / "logs"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Scraper settings
USER_AGENT: Final[str] = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)
REQUEST_TIMEOUT: Final[int] = 30
MAX_RETRIES: Final[int] = 3
RETRY_DELAY: Final[float] = 1.0

# Database settings
DB_FILE: Final[Path] = DATA_DIR / "acs_papers.json"

# Selenium/ChromeDriver settings
# Set to None to auto-download, or provide path to your chromedriver executable
CHROMEDRIVER_PATH: Optional[str] = None  # e.g., "/usr/local/bin/chromedriver" or "/tmp/chromedriver-linux64/chromedriver"


def setup_logging(level: int = logging.INFO) -> None:
    """Configure logging for the application.

    Args:
        level: Logging level (default: logging.INFO)
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file = LOGS_DIR / "acs_crawler.log"

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(log_format))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter(log_format))

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
