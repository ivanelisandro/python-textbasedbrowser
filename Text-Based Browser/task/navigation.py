from collections import deque
from content import ContentManager


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
