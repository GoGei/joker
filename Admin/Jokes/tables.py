import django_tables2 as tables
from core.Joke.models import Joke


class JokesTable(tables.Table):
    text_start = tables.TemplateColumn(template_name='Admin/Joke/joke_text_start.html', orderable=False)
    is_active = tables.BooleanColumn(orderable=False)
    actions = tables.TemplateColumn(template_name='Admin/Joke/joke_actions.html', orderable=False)

    class Meta:
        model = Joke
        fields = ('pk', 'text_start', 'is_active', 'actions')
        template_name = "django_tables2/bootstrap4.html"
