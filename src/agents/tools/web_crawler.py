import trafilatura
from langchain_core.tools import tool

def webpage_crawler(url: str):
    """
    Crawls a given URL and extracts its content in markdown format.
    This function uses the library to fetch and extract the content
    of a webpage from the provided URL. The extracted content is returned in
    markdown format, including any formatting, images, links, and tables present
    on the page.

    Args:
        url (str): The URL of the webpage to crawl.

    Returns:
        str: The extracted content in markdown format. If an error occurs during
            the crawling or extraction process, an empty string is returned.

    """
    try:
        html = trafilatura.fetch_url(url)
        content = trafilatura.extract(
            html,
            output_format="markdown",
            include_formatting=True,
            include_images=True,
            include_links=True,
            include_tables=True,
        )
    except Exception:
        content = "."
    return f"================ Hers is a content of url: {url} ================\n" + str(content)
