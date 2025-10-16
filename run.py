"""Entry point for running the ACS Crawler web application."""

import os
import uvicorn
from src.acs_crawler.config import setup_logging

if __name__ == "__main__":
    # Setup logging
    setup_logging()

    # Detect if running in Docker (disable reload for production)
    is_docker = os.path.exists("/.dockerenv")
    reload_enabled = not is_docker

    # Run the FastAPI application
    uvicorn.run(
        "src.acs_crawler.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=reload_enabled,
        log_level="info",
    )
