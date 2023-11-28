from startup import Startup
from navigation import TabsProvider
import sys


class Browser:
    def __init__(self, path):
        self.tabs = TabsProvider(path)

    def run(self):
        """
        Runs the text-based browser until an 'exit'
        command is used.
        """
        while (command := input()) != 'exit':
            self.tabs.navigate(command)


if not Startup.can_run(sys.argv):
    sys.exit(1)
browser = Browser(Startup.get_path())
browser.run()
