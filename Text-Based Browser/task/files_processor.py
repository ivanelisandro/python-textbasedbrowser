import os


class StoragePath:
    @staticmethod
    def validate(path):
        if not os.access(path, os.F_OK):
            os.makedirs(path, os.W_OK)
        return os.access(path, os.W_OK)


class TabsProvider:
    def __init__(self, directory):
        self.directory = directory

    def store(self, name, content):
        with open(self.format_path(name), "w", encoding='utf-8') as tab:
            tab.write(content)

    def load_local(self, name):
        with open(self.format_path(name), "r", encoding='utf-8') as tab:
            return tab.read()

    def is_stored(self, name):
        return os.access(self.format_path(name), os.R_OK)

    def format_path(self, name):
        return os.path.join(self.directory, name)