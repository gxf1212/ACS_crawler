"""Configuration module for ACS Crawler."""

import logging
import os
import sys
from pathlib import Path
from typing import Final, Optional

try:
    from dotenv import load_dotenv
    # Load .env file from project root if it exists
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        load_dotenv(env_path)
except ImportError:
    # python-dotenv not installed, skip .env loading
    pass

# Project paths
PROJECT_ROOT: Final[Path] = Path(__file__).parent.parent.parent
DATA_DIR: Final[Path] = PROJECT_ROOT / "data"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

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
# Priority: Environment variable > .env file > None (auto-download)
# Set CHROMEDRIVER_PATH environment variable or add it to .env file
# Examples:
#   Linux/Mac: /usr/local/bin/chromedriver
#   Windows: C:\Program Files\Google\Chrome\Application\chromedriver-win64\chromedriver.exe
CHROMEDRIVER_PATH: Optional[str] = os.getenv("CHROMEDRIVER_PATH")


def setup_logging(level: int = logging.INFO) -> None:
    """Configure logging for the application.

    Args:
        level: Logging level (default: logging.INFO)
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Console handler only
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(logging.Formatter(log_format))

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
