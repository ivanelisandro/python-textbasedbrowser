from bs4 import BeautifulSoup
from dataclasses import dataclass
from storage import LocalStorage
import re
import requests


@dataclass
class Page:
    """
    Data class to represent the information of a webpage.
    """
    url: str
    shortcut: str
    content: str
    is_valid: bool


class HtmlToText:
    """
    Class to extract HTML content and transform into text for the text-based browser.
    """

    @staticmethod
    def convert(response: requests.Response):
        """
        Extracts the HTML content of a response and transforms its contents into
        pure text using BeautifulSoup library.
        Includes the title of the page and the content of the body only.
        """
        processor = BeautifulSoup(response.content, 'html.parser')
        result = processor.title.text + '\n'
        contents = processor.body.text.split('\n')
        contents = [line.strip() for line in contents if line]
        result += '\n'.join(contents)
        return result


class ContentManager:
    """
    Class to provide routines for retrieving and processing
    contents in the form of a Page
    """
    https_pattern = r"https?:\/\/"
    url_pattern = r"(https?:\/\/)?(\w+)\."
    name_pattern = r"(https:\/\/)(\w+)\."

    def __init__(self, path):
        self.storage = LocalStorage(path)

    def get(self, url) -> Page:
        """
        Gets the content for the given url as a Page.
        Invalid url format will return an error message Page.
        """
        if self.storage.exists(url):
            return Page("", url, self.storage.load_local(url), True)

        if re.match(self.url_pattern, url):
            name, content = self.process(url)
            return Page(url, name, content, True)

        return Page(url, "", "Invalid URL", False)

    def process(self, url):
        """
        Process the content for a previously unknown url.
        It will add the content to the local storage.
        """
        if not re.match(self.https_pattern, url):
            url = f"https://{url}"
        response = requests.get(url)
        if response:
            content = HtmlToText.convert(response)
            name = re.match(self.name_pattern, url).group(2)
            self.storage.store(name, content)
            return name, content
        return None, None
