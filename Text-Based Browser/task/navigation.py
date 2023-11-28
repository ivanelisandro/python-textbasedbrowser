from collections import deque
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
            content = response.text
            name = re.match(self.name_pattern, url).group(2)
            self.storage.store(name, content)
            return name, content
        return None, None


class Navigation:
    """
    Class to handle navigation history.
    """

    def __init__(self):
        self.history = deque()

    def add_history(self, command):
        """
        Adds the specified command to the history stack.
        """
        if command:
            self.history.append(command[:])

    def get_previous(self):
        """
        Retrieves the previous state in the history stack,
        removing it from the stack.
        """
        if self.history:
            return self.history.pop()
        return None


class TabsProvider:
    """
    Provides tab-like navigation routines to a text-based browser.
    """
    url_pattern = r"(\w+)\."

    def __init__(self, path):
        self.current_page = None
        self.navigation = Navigation()
        self.contents = ContentManager(path)

    def navigate(self, command):
        """
        Processes the navigation command.
        When 'back' is used, returns to the previous page.
        Otherwise, shows to content for the command.
        """
        if command == 'back':
            self.go_back()
            return
        self.show(command)

    def go_back(self):
        """
        Goes back to the previous state if it exists,
        otherwise does nothing.
        """
        if command := self.navigation.get_previous():
            self.show(command)

    def show(self, command):
        """
        Prints the page content based on a command or url.
        If the page is valid, adds it to history for future
        backwards navigation.
        """
        page = self.contents.get(command)
        print(page.content)
        if page.is_valid:
            self.navigation.add_history(self.current_page)
            self.current_page = page.shortcut
