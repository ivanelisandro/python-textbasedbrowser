from files_processor import StoragePath, TabsProvider
import re
import sys

nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created "soft" magnets that can flow 
and change shape, and that could be a boon to medicine 
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two 
 years.

'''

bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk 
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Creedence's 
 Bad Moon Rising. The world is a very different place than 
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey 
 addressed Apple Inc. employees at the iPhone maker’s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
'''


class Startup:
    minimum_arguments = 2

    @staticmethod
    def get_path():
        if len(sys.argv) < Startup.minimum_arguments:
            return None

        return sys.argv[1]


class Browser:
    urls = {
        'bloomberg.com': bloomberg_com,
        'nytimes.com': nytimes_com
    }

    url_pattern = r"(\w+)\."

    def __init__(self, path):
        self.tabs = TabsProvider(path)

    def run(self):
        while (command := input()) != 'exit':
            print(self.handle_command(command))

    def handle_command(self, url):
        if self.tabs.is_stored(url):
            return self.tabs.load_local(url)

        if re.match(self.url_pattern, url) and url in self.urls:
            return self.get_content(url)

        return "Invalid URL"

    def get_content(self, url):
        content = self.urls[url]
        name = re.match(self.url_pattern, url).group(1)
        self.tabs.store(name, content)
        return content


if not (storage_path := Startup.get_path()):
    sys.exit(1)
if not StoragePath.validate(storage_path):
    sys.exit(1)
browser = Browser(storage_path)
browser.run()
