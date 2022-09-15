from random import randint
from django.db import models
from django.db.models.expressions import RawSQL
from drf_yasg2.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from Api.base_views import MappedSerializerVMixin
from .serializers import JokeSerializer, JokeSeenSerializer
from core.Joke.models import Joke, JokeSeen


class JokeViewSet(viewsets.ReadOnlyModelViewSet, MappedSerializerVMixin):
    queryset = Joke.objects.prefetch_related('jokeseen_set', 'jokelikestatus_set').ordered()
    serializer_class = JokeSerializer
    serializer_map = {
        'get_random': JokeSeenSerializer
    }
    empty_serializers = ('like', 'dislike', 'deactivate')
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        queryset = self.queryset
        user = self.request.user

        if user.is_authenticated:
            queryset = queryset.annotate(is_seen=models.Exists(
                JokeSeen.objects.filter(
                    joke=models.OuterRef('pk'),
                    user=user
                )))
            queryset = queryset.annotate(is_liked=RawSQL(
                'select is_liked from joke_like_status where joke_id=joke.id and user_id=%s', (user.id,)
            ))
        else:
            queryset = queryset.annotate(is_seen=models.Case(default=False, output_field=models.BooleanField()))
            queryset = queryset.annotate(is_liked=models.Case(default=None, output_field=models.BooleanField()))

        return queryset

    @action(methods=['post'], detail=True, permission_classes=(permissions.IsAuthenticated, ))
    def like(self, request, pk=None):
        joke = self.get_object()
        joke.like(request.user)
        return Response({'joke %s is liked' % joke.label}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, permission_classes=(permissions.IsAuthenticated, ))
    def dislike(self, request, pk=None):
        joke = self.get_object()
        joke.dislike(request.user)
        return Response({'joke %s is disliked' % joke.label}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, permission_classes=(permissions.IsAuthenticated, ))
    def deactivate(self, request, pk=None):
        joke = self.get_object()
        joke.deactivate(request.user)
        return Response({'joke %s is deactivated' % joke.label}, status=status.HTTP_200_OK)

    @swagger_auto_schema(query_serializer=JokeSeenSerializer)
    @action(methods=['get'], detail=False, url_name='get-random', url_path='get-random')
    def get_random(self, request, *args, **kwargs):
        user = self.request.user

        if user.is_authenticated:
            queryset = self.get_queryset()
            queryset = queryset.filter(is_seen=False)

            if not queryset.exists():
                user.jokeseen_set.all().delete()
                print('All seen removed')
        else:
            serializer = self.get_serializer(data=self.request.query_params)
            serializer.is_valid(raise_exception=True)
            seen_jokes = serializer.validated_data.get('seen_jokes')

            queryset = self.get_queryset()
            if seen_jokes:
                seen_jokes = seen_jokes.split(',')
                queryset = queryset.exclude(id__in=seen_jokes)

        if not queryset.exists():
            return Response({'text': 'There are no jokes left you have not seen',
                             'all_jokes_seen': True},
                            status=status.HTTP_200_OK)

        joke = queryset[randint(0, queryset.count() - 1)]
        if user.is_authenticated:
            JokeSeen.objects.create(joke=joke, user=user)

        serializer = JokeSerializer(joke)
        data = serializer.data.copy()
        data.update({'add_to_cache': not user.is_authenticated})
        return Response(data, status=status.HTTP_200_OK)
