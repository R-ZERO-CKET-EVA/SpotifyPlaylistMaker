import os
import json
import logging
from typing import List, Dict
from html_parser import HTMLParser
from string_counter import StringCounter
import time
from urllib.parse import quote


class URLProcessor:
    def __init__(self, config_file: str):
        self.config_file = config_file

    def process_urls(self) -> Dict[str, Dict[str, int]]:
        urls = self._read_config_file()
        results = {}

        for url in urls:
            try:
                html_parser = HTMLParser(url)
                summary_urls = html_parser.parse_summary_urls()
                song_labels = []

                for summary_url in summary_urls:
                    time.sleep(5)  # Wait for 5 seconds between each visit
                    song_labels.extend(html_parser.parse_song_labels(summary_url))
                    print(summary_url)

                string_counter = StringCounter()
                counts = string_counter.count_strings(song_labels)

                results[url] = counts

            except Exception as e:
                logging.error(f"Error processing URL: {url}")
                log_file = self._get_log_file_name(url)
                self._save_error_log(log_file, str(e))

        return results

    def _read_config_file(self) -> List[str]:
        with open(self.config_file, "r") as f:
            urls = f.read().splitlines()
        return urls

    def _get_log_file_name(self, url: str) -> str:
        filename = quote(url, safe="")
        return f"{filename}.log"

    def _save_error_log(self, log_file: str, error_message: str):
        with open(log_file, "w") as f:
            f.write(error_message)
