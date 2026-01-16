import requests
from bs4 import BeautifulSoup
from urllib.parse import quote


def discover_report_urls(player_name, max_results=5):
    """
    Uses DuckDuckGo HTML to discover match report URLs.
    No Google scraping.
    """

    query = quote(f"{player_name} match report crucial clearance save")
    url = f"https://duckduckgo.com/html/?q={query}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")

    links = []
    for a in soup.select("a.result__a")[:max_results]:
        href = a.get("href")
        if href:
            links.append(href)

    return links
# Example usage:
# urls = discover_report_urls("John Doe")   