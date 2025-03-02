"""Class to scrape the Dhamma talks website using beautifulsoup4."""

from dataclasses import dataclass
from time import sleep
from typing import Optional

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from scripture_search.config import Config
from scripture_search.data_collection.data_collector import DataCollector

BASE_URL = "https://www.dhammatalks.org"
DHAMMA_TALKS_DN_URL = BASE_URL + "/suttas/DN"
INDEX_PAGE_EXTENSIONS = [
    "/suttas/AN",
    "/suttas/DN",
    "/suttas/KN",
    "/suttas/MN/",
    "/suttas/SN/",
]
INDEX_PAGE_URLS = [BASE_URL + ext for ext in INDEX_PAGE_EXTENSIONS]


@dataclass
class SuttaText:
    """Class to hold relevant data for a sutta."""

    collection: str
    title: str
    paragraphs: list[str]
    url_source: str


class DhammaTalksCollector(DataCollector):
    """Class to scrape the Dhamma talks website using beautifulsoup4."""

    def __init__(self, config: Optional[Config] = None):
        if config is None:
            config = Config()
        self.config = config

        super().__init__(config.paths.dhamma_talks_suttas_data_file)

    def _collect_data(self) -> pd.DataFrame:
        """Collect data from the Dhamma talks website."""
        index_page_to_sutta_page_links = self._get_index_page_to_sutta_page_links()

        data = []
        for index_page_url, sutta_page_links in tqdm(
            index_page_to_sutta_page_links.items()
        ):
            collection = list(filter(lambda x: len(x) > 0, index_page_url.split("/")))[
                -1
            ]
            self.logger.info("Processing collection: %s", collection)
            for sutta_page_link in sutta_page_links:
                try:
                    sutta_text = self._get_sutta_text(sutta_page_link, collection)
                    data.append(sutta_text)
                    sleep(0.25)
                except Exception as e:
                    self.logger.error(
                        "Error processing %s: %s", sutta_page_link, str(e)
                    )

        self.logger.info("Collected %d suttas", len(data))
        data = pd.DataFrame(data)

        data = data.assign(
            religion="Buddhism",
            subgroup="Theravada",
            source="Dhamma Talks",
            translation_source="Thanissaro Bhikkhu",
        )
        return data

    def _get_sutta_text(self, url: str, collection: str) -> SuttaText:
        """Get the text of a sutta from the Dhamma talks website."""
        self.logger.debug("Fetching sutta from %s", url)
        sutta_page = BeautifulSoup(
            requests.get(url, timeout=self.config.data_collector_timeout).text,
            "html.parser",
        )
        sutta_body = sutta_page.find("div", id="sutta")
        if not sutta_body:
            self.logger.warning("No sutta body found at %s", url)
            return None
        sutta_title = sutta_body.find("h1").text.split("\n")[0].strip()
        sutta_paragraphs = [p.text.strip() for p in sutta_body.find_all("p")]
        return SuttaText(collection, sutta_title, sutta_paragraphs, url)

    def _get_index_page_to_sutta_page_links(self) -> dict[str, list[str]]:
        """Get a mapping of index pages to their sutta page links."""
        self.logger.info("Getting sutta page links from index pages")
        return {
            index_page_url: self._get_sutta_links_from_index_page(index_page_url)
            for index_page_url in INDEX_PAGE_URLS
        }

    def _get_sutta_links_from_index_page(self, index_page_url: str) -> list[str]:
        """Extract sutta links from a given index page."""
        self.logger.debug("Processing index page: %s", index_page_url)
        response = requests.get(
            index_page_url, timeout=self.config.data_collector_timeout
        )
        soup = BeautifulSoup(response.text, "html.parser")
        toc = soup.find("div", class_="suttatoc")

        if toc is None:
            self.logger.warning("No table of contents found at %s", index_page_url)
            return []

        links = [
            BASE_URL + anchor["href"]
            for anchor in toc.find_all("a")
            if ".html" in anchor["href"]
        ]
        self.logger.debug("Found %d links in %s", len(links), index_page_url)
        return links
