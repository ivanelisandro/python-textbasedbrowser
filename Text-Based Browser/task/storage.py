import os


class LocalStorage:
    """
    Handles local storage requirements, storing previously
    navigated web-site content as text accessible from files.
    """

    def __init__(self, directory):
        self.directory = directory

    def store(self, name, content):
        """
        Stores the given content to a file with the given name
        in the local storage directory.
        """
        with open(self.format_path(name), "w", encoding='utf-8') as tab:
            tab.write(content)

    def load_local(self, name):
        """
        Retrieves the content of a file with the given name
        from the local storage directory.
        """
        with open(self.format_path(name), "r", encoding='utf-8') as tab:
            return tab.read()

    def exists(self, name):
        """
        Validates if a file with the given name exists in the
        local storage directory with reading permissions.

        Returns False if the file does not exist or if it cannot
        be read.
        """
        return os.access(self.format_path(name), os.R_OK)

    def format_path(self, name):
        """
        Formats the file name into a full file path using the
        local storage directory.
        """
        return os.path.join(self.directory, name)
