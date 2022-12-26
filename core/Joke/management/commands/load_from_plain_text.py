from django.db import transaction
from core.Joke.models import Joke
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Load jokes from plain text (joke per line)'

    def add_arguments(self, parser):
        parser.add_argument('filename',
                            type=str
                            )
        parser.add_argument('--with_print',
                            type=bool
                            )

    @transaction.atomic
    def handle(self, *args, **options):
        filename = options.get('filename')
        filepath = f'core/Joke/fixtures/{filename}'

        with open(filepath, 'r') as file:
            data = file.readlines()

        created = 0
        skipped = 0
        skipped_jokes = []
        for joke_text in data:
            text = joke_text.replace('\n', '')
            joke = Joke.objects.filter(text=text).first()
            if joke:
                skipped += 1
                skipped_jokes.append(joke_text)
                continue
            else:
                joke = Joke(text=text)

            if not joke.slug and Joke.is_allowed_to_assign_slug(joke_text):
                created += 1
                joke.assign_slug()
            else:
                skipped += 1
                skipped.append(joke_text)
                self.stdout.write('Jokes not created due to not allowed to assign slug', style_func=self.style.WARNING)
                self.stdout.write(f'{joke_text}')

        self.stdout.write(f'Jokes created {created}', style_func=self.style.SUCCESS)
        self.stdout.write(f'Jokes skipped {skipped}', style_func=self.style.WARNING)

        if options.get('with_print', False):
            self.stdout.write('Skipped', style_func=self.style.ERROR)
            for joke in skipped_jokes:
                self.stdout.write(f'\t{joke}')
