"""Utility functions for building ACS search URLs."""

from typing import Optional
from urllib.parse import urlencode


def build_search_url(
    query: str,
    sort_by: str = "Relevance",
    start_page: int = 0,
    page_size: int = 50,
    after_year: Optional[int] = None,
    after_month: Optional[int] = None,
    before_year: Optional[int] = None,
    before_month: Optional[int] = None
) -> str:
    """Build an ACS search URL from parameters.

    Args:
        query: Search query string
        sort_by: Sort order. Options:
            - "Relevance" (default)
            - "Earliest_asc" (oldest first)
            - "Earliest_desc" (newest first)
            - "MostCited"
        start_page: Starting page number (0-based)
        page_size: Number of results per page (default 50)
        after_year: Start year for date range (e.g., 2020)
        after_month: Start month for date range (1-12)
        before_year: End year for date range (e.g., 2025)
        before_month: End month for date range (1-12)

    Returns:
        Complete ACS search URL

    Examples:
        >>> build_search_url("rdrp")
        'https://pubs.acs.org/action/doSearch?AllField=rdrp&sortBy=Relevance&startPage=0&pageSize=50'

        >>> build_search_url("CRISPR", sort_by="Earliest_asc", page_size=100)
        'https://pubs.acs.org/action/doSearch?AllField=CRISPR&sortBy=Earliest_asc&startPage=0&pageSize=100'

        >>> build_search_url("RdRp", after_year=2020, after_month=1, before_year=2025, before_month=12)
        'https://pubs.acs.org/action/doSearch?AllField=RdRp&sortBy=Relevance&startPage=0&pageSize=50&AfterYear=2020&AfterMonth=1&BeforeYear=2025&BeforeMonth=12'
    """
    base_url = "https://pubs.acs.org/action/doSearch"

    params = {
        "AllField": query,
        "sortBy": sort_by,
        "startPage": start_page,
        "pageSize": page_size
    }

    # Add date range parameters if provided
    if after_year is not None:
        params["AfterYear"] = after_year
    if after_month is not None:
        params["AfterMonth"] = after_month
    if before_year is not None:
        params["BeforeYear"] = before_year
    if before_month is not None:
        params["BeforeMonth"] = before_month

    return f"{base_url}?{urlencode(params)}"


def parse_search_url(url: str) -> dict:
    """Parse an ACS search URL to extract parameters.

    Args:
        url: ACS search URL

    Returns:
        Dictionary with query, sort_by, start_page, page_size, and date range parameters

    Examples:
        >>> url = "https://pubs.acs.org/action/doSearch?AllField=rdrp&sortBy=Earliest_asc&startPage=0&pageSize=50"
        >>> parse_search_url(url)
        {'query': 'rdrp', 'sort_by': 'Earliest_asc', 'start_page': 0, 'page_size': 50, 'after_year': None, 'after_month': None, 'before_year': None, 'before_month': None}

        >>> url = "https://pubs.acs.org/action/doSearch?AllField=test&AfterYear=2020&AfterMonth=1&BeforeYear=2025&BeforeMonth=12"
        >>> parse_search_url(url)
        {'query': 'test', 'sort_by': 'Relevance', 'start_page': 0, 'page_size': 50, 'after_year': 2020, 'after_month': 1, 'before_year': 2025, 'before_month': 12}
    """
    from urllib.parse import urlparse, parse_qs

    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)

    result = {
        "query": query_params.get("AllField", [""])[0],
        "sort_by": query_params.get("sortBy", ["Relevance"])[0],
        "start_page": int(query_params.get("startPage", ["0"])[0]),
        "page_size": int(query_params.get("pageSize", ["50"])[0])
    }

    # Add date range parameters if present
    if "AfterYear" in query_params:
        result["after_year"] = int(query_params["AfterYear"][0])
    else:
        result["after_year"] = None

    if "AfterMonth" in query_params:
        result["after_month"] = int(query_params["AfterMonth"][0])
    else:
        result["after_month"] = None

    if "BeforeYear" in query_params:
        result["before_year"] = int(query_params["BeforeYear"][0])
    else:
        result["before_year"] = None

    if "BeforeMonth" in query_params:
        result["before_month"] = int(query_params["BeforeMonth"][0])
    else:
        result["before_month"] = None

    return result


def is_search_url(url: str) -> bool:
    """Check if a URL is an ACS search URL.

    Args:
        url: URL to check

    Returns:
        True if URL is a search URL, False otherwise

    Examples:
        >>> is_search_url("https://pubs.acs.org/action/doSearch?AllField=test")
        True
        >>> is_search_url("https://pubs.acs.org/toc/jacsat/current")
        False
    """
    return "/action/doSearch" in url


def get_next_page_url(url: str) -> Optional[str]:
    """Get the URL for the next page of search results.

    Args:
        url: Current search URL

    Returns:
        URL for next page, or None if can't parse

    Examples:
        >>> url = "https://pubs.acs.org/action/doSearch?AllField=test&startPage=0"
        >>> get_next_page_url(url)
        'https://pubs.acs.org/action/doSearch?AllField=test&startPage=1'
    """
    try:
        params = parse_search_url(url)
        params["start_page"] += 1
        return build_search_url(
            query=params["query"],
            sort_by=params["sort_by"],
            start_page=params["start_page"],
            page_size=params["page_size"]
        )
    except Exception:
        return None
