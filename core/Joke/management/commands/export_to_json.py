import json
from core.Joke.models import Joke
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Export to json file'

    def add_arguments(self, parser):
        parser.add_argument('filename',
                            type=str
                            )

    def handle(self, *args, **options):
        filename = options.get('filename')
        extension = 'json'
        file_extension = filename.split('.')[-1].lower()
        if file_extension != extension:
            filename += f'.{extension}'
        filepath = f'core/Joke/fixtures/{filename}'
        qs = Joke.objects.all()
        data = []
        for counter, joke in enumerate(qs, start=1):
            joke_dict = joke.to_json()
            joke_dict.update({'counter': counter})
            data.append(joke_dict)

        with open(filepath, 'w+') as json_file:
            json.dump(data, json_file, ensure_ascii=False)

        full_path = f'{settings.BASE_DIR}{filepath}'
        self.stdout.write(f'Jokes exported {len(data)} to {full_path}', style_func=self.style.SUCCESS)
