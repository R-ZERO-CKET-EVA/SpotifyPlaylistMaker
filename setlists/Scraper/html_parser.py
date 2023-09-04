import requests
from typing import List
from bs4 import BeautifulSoup

class HTMLParser:
    def __init__(self, url: str):
        self.url = url

    def parse_summary_urls(self) -> List[str]:
        summary_urls = []
        
        # First, parse the initial page
        summary_urls += self._parse_page(self.url)

        # Then, iterate from page 2 to 10 and parse each page
        for page_number in range(2, 10):
            page_url = f"{self.url}?page={page_number}"
            summary_urls += self._parse_page(page_url)

        return summary_urls

    def _parse_page(self, url: str) -> List[str]:
        html = self._get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        parsed_urls = []

        anchor_tags = soup.find_all("a", class_="summary url")
        if not anchor_tags:
            print(f"No summary URL class found for: {url}")

        for anchor_tag in anchor_tags:
            tempUrl = anchor_tag["href"]
            tempUrl = tempUrl.lstrip(".")
            tempUrl = "http://setlist.fm" + tempUrl
            parsed_urls.append(tempUrl)

        return parsed_urls

    def parse_song_labels(self, url: str) -> List[str]:
        html = self._get_html(url)
        soup = BeautifulSoup(html, "html.parser")
        song_labels = []

        div_tags = soup.find_all("div", class_="songPart")
        if not div_tags:
            song_labels.append("")  # Save a blank string if no songLabel class found

        for div_tag in div_tags:
            song_labels.append(div_tag.get_text(strip=True))

        return song_labels

    def _get_html(self, url: str) -> str:
        response = requests.get(url)
        response.raise_for_status()
        return response.text