import re
import requests
from bs4 import BeautifulSoup
from django.utils.html import strip_tags


class WebpageParser(object):
    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.args = args
        self.kwargs = kwargs

    @classmethod
    def parse_html_to_text(cls, row):
        row = str(row)
        row = re.sub(r'<br.>', '\n', row)
        row = re.sub(r' +', ' ', row)

        result = strip_tags(row)
        result = result.strip()
        return result

    def get_content(self):
        response = requests.get(self.url)
        html_text = response.text
        soup = BeautifulSoup(html_text, features="lxml")
        find = soup.find_all(*self.args, **self.kwargs)
        content = [self.parse_html_to_text(row) for row in find]
        return content
