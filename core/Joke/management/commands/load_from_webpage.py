from django.db import transaction

from core.Joke.models import Joke
from core.Joke.webparsers.parser import WebpageParser
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load jokes from website'

    def add_arguments(self, parser):
        parser.add_argument('url',
                            type=str
                            )
        parser.add_argument('pages',
                            type=int,
                            help='Get pages of url (from 1 to N)',
                            nargs='?',
                            )

    @classmethod
    def handle_parsing(cls, url, *args, **kwargs):
        parser = WebpageParser(url, *args, **kwargs)
        content = parser.get_content()
        created_count = 0
        for item in content:
            if len(item) > Joke.MAX_LENGTH:
                continue

            joke, created = Joke.objects.get_or_create(text=item)
            if created:
                created_count += 1
                joke.assign_slug()

        print(f'[+] From web page got {len(content)} jokes and {created_count} created')

    @transaction.atomic
    def handle(self, *args, **options):
        url = options.get('url')
        pages = options.get('pages')

        if 'anekdot.ru' in url:
            # https://www.anekdot.ru/
            args = ('div',)
            kwargs = {
                'attrs': {'class': 'text'},
            }
        else:
            args = ('div',)
            kwargs = {
                'attrs': {'class': 'text'},
            }

        if pages:
            for page in range(1, pages + 1):
                self.handle_parsing(f'{url}?page={page}', *args, **kwargs)
        else:
            self.handle_parsing(url, *args, **kwargs)
