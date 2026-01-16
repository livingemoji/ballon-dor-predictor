import requests
from bs4 import BeautifulSoup


def scrape_report_text(url):
    """
    Scrapes readable paragraph text from a match report.
    """

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.RequestException:
        return ""

    soup = BeautifulSoup(response.text, "html.parser")

    paragraphs = soup.find_all("p")
    text = " ".join(p.get_text(strip=True) for p in paragraphs)

    return text.lower()
