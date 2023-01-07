import requests
from bs4 import BeautifulSoup
from django.db import transaction
from django.utils.html import strip_tags

from core.Joke.models import Joke
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load jokes from website'

    def add_arguments(self, parser):
        parser.add_argument('url',
                            type=str
                            )

    @transaction.atomic
    def handle(self, *args, **options):
        url = options.get('url')
        response = requests.get(url)
        html_text = response.text
        soup = BeautifulSoup(html_text, features="html.parser")
        find = soup.find_all('div', attrs={'class': 'text'})

        for row in find:
            print('=====')
            print(strip_tags(row))
