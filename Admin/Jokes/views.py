from django.conf import settings
from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import render, redirect, reverse, get_object_or_404

from core.Utils.Access.decorators import manager_required, superuser_required
from core.Joke.models import Joke
from .forms import JokeFilterForm, JokeAddForm, JokeEditForm
from .tables import JokesTable, JokesTopTable


@manager_required
def jokes_list(request):
    jokes = Joke.objects.all().ordered()

    joke_filter = JokeFilterForm(request.GET, queryset=jokes)
    jokes = joke_filter.qs
    table_body = JokesTable(jokes)
    page = request.GET.get("page", 1)
    table_body.paginate(page=page, per_page=settings.ITEMS_PER_PAGE)

    table = {
        'pk': 'Joke Data Table',
        'body': table_body
    }
    table_filter = {
        'pk': 'Joke filter',
        'body': joke_filter,
        'action': reverse('jokes-list'),
    }

    return render(request, 'Admin/Joke/joke_list.html',
                  {'table': table,
                   'filter': table_filter})


@manager_required
def jokes_top_list(request):
    jokes = Joke.objects.annotate(
        likes=Count('jokelikestatus', filter=Q(jokelikestatus__is_liked=True))
    ).order_by('-likes').all()

    table_body = JokesTopTable(jokes)
    page = request.GET.get("page", 1)
    table_body.paginate(page=page, per_page=settings.ITEMS_PER_PAGE)

    table = {
        'pk': 'Top jokes',
        'body': table_body
    }

    return render(request, 'Admin/Joke/joke_top_list.html',
                  {'table': table})


@manager_required
def jokes_add(request):
    if '_cancel' in request.POST:
        return redirect(reverse('jokes-list'), host='admin')

    form_body = JokeAddForm(request.POST or None)

    if form_body.is_valid():
        joke = form_body.save()
        messages.success(request, f'Joke {joke.pk} added')
        return redirect(reverse('jokes-list'), host='admin')

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
        'inline_form': True
    }

    return render(request, 'Admin/Joke/joke_add.html',
                  {'form': form})


@manager_required
def jokes_edit(request, joke_slug):
    joke = get_object_or_404(Joke, slug=joke_slug)

    if '_cancel' in request.POST:
        return redirect(reverse('jokes-list'), host='admin')

    form_body = JokeEditForm(request.POST or None,
                             instance=joke)

    if form_body.is_valid():
        joke = form_body.save()
        joke.modify(request.user)
        messages.success(request, f'Joke {joke.pk} edited')
        return redirect(reverse('jokes-list'), host='admin')

    form = {
        'body': form_body,
        'buttons': {'save': True, 'cancel': True},
        'inline_form': True
    }
    return render(request, 'Admin/Joke/joke_edit.html',
                  {'form': form})


@manager_required
def jokes_view(request, joke_slug):
    joke = get_object_or_404(Joke, slug=joke_slug)
    return render(request, 'Admin/Joke/joke_view.html', {'joke': joke})


@manager_required
def jokes_archive(request, joke_slug):
    joke = get_object_or_404(Joke, slug=joke_slug)
    joke.archive(request.user)
    messages.success(request, f'Joke {joke.pk} archived')
    return redirect(reverse('jokes-list'), host='admin')


@manager_required
def jokes_restore(request, joke_slug):
    joke = get_object_or_404(Joke, slug=joke_slug)
    joke.restore(request.user)
    messages.success(request, f'Joke {joke.pk} restored')
    return redirect(reverse('jokes-list'), host='admin')


@superuser_required
def jokes_delete(request, joke_slug):
    joke = get_object_or_404(Joke, slug=joke_slug)
    messages.success(request, f'Joke {joke.pk} deleted')
    joke.delete()
    return redirect(reverse('jokes-list'), host='admin')
