from django.shortcuts import render
from django.db import models
from core.Joke.models import Joke


def home_view(request):
    return render(request, 'Public/Home/public_home.html')


def home_all_jokes_view(request):
    jokes = Joke.objects.active().ordered()
    return render(request, 'Public/Home/public_all_jokes.html', {'jokes': jokes})


def home_top_jokes_view(request):
    jokes = Joke.objects.prefetch_related('jokelikestatus_set').active().all()
    jokes = jokes.annotate(likes=models.Count('jokelikestatus'))
    jokes = jokes.filter(~models.Q(likes=0))
    jokes = jokes.order_by('likes')
    return render(request, 'Public/Home/public_top_jokes.html', {'jokes': jokes})
