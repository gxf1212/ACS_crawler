"""Entry point for running the ACS Crawler web application."""

import uvicorn
from src.acs_crawler.config import setup_logging

if __name__ == "__main__":
    # Setup logging
    setup_logging()

    # Run the FastAPI application
    uvicorn.run(
        "src.acs_crawler.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
