from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import models
from django.db.models.expressions import RawSQL
from core.Joke.models import Joke, JokeLikeStatus, JokeSeen


def home_view(request):
    return render(request, 'Public/Home/public_home.html')


def home_all_jokes_view(request):
    jokes = Joke.objects.active().ordered()
    jokes = Joke.annotate_qs_by_user(jokes, request.user)
    return render(request, 'Public/Home/public_all_jokes.html', {'jokes': jokes})


def home_top_jokes_view(request):
    jokes = Joke.objects.active().all()
    jokes = jokes.annotate(likes=RawSQL(
        'select count(id) from joke_like_status where joke_id=joke.id AND is_liked=True', ()
    ))
    jokes = jokes.filter(~models.Q(likes=0))
    jokes = Joke.annotate_qs_by_user(jokes, request.user)
    jokes = jokes.order_by('-likes')
    return render(request, 'Public/Home/public_top_jokes.html', {'jokes': jokes})


@login_required
def home_liked_views(request):
    user = request.user
    liked = JokeLikeStatus.objects.select_related('joke', 'user').filter(user=user, is_liked=True).all()
    jokes = Joke.objects.filter(id__in=liked.values_list('joke', flat=True))
    jokes = Joke.annotate_qs_by_user(jokes, request.user)
    return render(request, 'Public/Home/public_liked_jokes.html', {'jokes': jokes})


def home_seen_views(request):
    user = request.user
    liked = JokeSeen.objects.select_related('joke', 'user').filter(user=user).order_by(
        'seen_stamp').all()
    jokes = Joke.objects.filter(id__in=liked.values_list('joke', flat=True))
    jokes = Joke.annotate_qs_by_user(jokes, request.user)
    return render(request, 'Public/Home/public_seen_jokes.html', {'jokes': jokes})
