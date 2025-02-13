from firecrawl import FirecrawlApp
import streamlit as st


def search_and_scrape(query, top_k) -> str:
    """Searches using Firecrawl and scrapes markdown content.

    Returns:
        str: A string containing all the scraped markdown content concatenated,
             or an empty string if scraping fails.
    """
    app = FirecrawlApp()
    try:
        result = app.search(
            query,
            params={
                "limit": top_k,
                "scrapeOptions": {
                    "formats": ["markdown"],
                },
            },
        )
        if result and result["success"]:
            urls = [item["url"] for item in result["data"]]
            return result["data"], urls
        else:
            st.warning(
                f"Search was not successful: {result.get('error', 'Unknown error')}"
            )
            return [], []
    except Exception as e:
        st.error(f"Error during search and scraping: {e}")
        return [], []
