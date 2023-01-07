import json

from django.db import transaction

from core.Joke.models import Joke
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load jokes from json'

    def add_arguments(self, parser):
        parser.add_argument('filename',
                            type=str
                            )
        parser.add_argument('--with_print',
                            type=bool
                            )
        parser.add_argument('--save_errored',
                            type=bool,
                            help='Save joke even if it creation went with error',
                            )

    @transaction.atomic
    def handle(self, *args, **options):
        filename = options.get('filename')
        save_errored = options.get('save_errored')
        filepath = f'core/Joke/fixtures/{filename}'

        with open(filepath, 'r') as file:
            data = json.load(file)

        created = 0
        synced = 0
        passed = 0
        slug_error = 0

        synced_jokes = []
        passed_jokes = []
        slug_error_jokes = []

        for item_counter, joke_data in enumerate(data, start=1):
            slug = joke_data.get('slug', None)

            joke = None
            if slug:
                joke = Joke.objects.filter(slug=slug).first()

            text = joke_data.get('text')
            if not joke:
                joke = Joke(text=text)
                created += 1
            else:
                if joke.text != text:
                    synced += 1
                    synced_jokes.append({'before': joke.text,
                                         'after': text})
                    joke.text = text
                else:
                    passed_jokes.append(joke.text)
                    passed += 1

            joke.save()

            if not joke.slug:
                if Joke.is_allowed_to_assign_slug(text):
                    joke.assign_slug()
                else:
                    counter = joke_data.get('counter', item_counter)
                    msg = '[-] Jokes with text not assigned slug because slug like this already exists!'
                    self.stdout.write(msg, style_func=self.style.ERROR)
                    self.stdout.write(f'\tText on position {counter}: "{text}"')
                    slug_error_jokes.append(joke)
                    slug_error += 1
                    created -= 1

                    if not save_errored:
                        joke.delete()
                        continue

            is_active = joke_data.get('is_active', False)
            if not is_active:
                joke.archive()

        self.stdout.write(f'[+] Jokes synced {len(data)}', style_func=self.style.SUCCESS)
        self.stdout.write(f'[+] Jokes created {created}')
        self.stdout.write(f'[+] Jokes synced {synced}')
        self.stdout.write(f'[!] Jokes passed {passed}')
        self.stdout.write(f'[-] Jokes slug errors {slug_error}')

        if options.get('with_print', False):
            self.stdout.write('Synced')
            for joke_data in synced_jokes:
                self.stdout.write(f'\t{joke_data.get("before")} -> {joke_data.get("after")}')

            self.stdout.write('Passed (already exists)')
            for joke_text in passed_jokes:
                self.stdout.write(f'\t{joke_text}', style_func=self.style.WARNING)

            self.stdout.write('Slug went error')
            for joke in slug_error_jokes:
                self.stdout.write(f'\t{joke.text}|{joke.slug}', style_func=self.style.ERROR)
