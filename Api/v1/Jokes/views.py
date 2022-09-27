from random import randint
from django.db import models
from django.db.models.expressions import RawSQL
from django.core.cache import cache
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from Api.base_views import MappedSerializerVMixin
from core.Joke import exceptions
from core.Joke.models import Joke, JokeSeen
from .serializers import JokeSerializer, JokeSeenSerializer, JokeSendToEmailSerializer, JokeSendToTelegramSerializer


class JokeViewSet(viewsets.ReadOnlyModelViewSet, MappedSerializerVMixin):
    queryset = Joke.objects.prefetch_related('jokeseen_set', 'jokelikestatus_set').ordered()
    serializer_class = JokeSerializer
    serializer_map = {
        'get_random': JokeSeenSerializer,
        'send_to_email': JokeSendToEmailSerializer,
        'send_to_telegram': JokeSendToTelegramSerializer,
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

    @action(methods=['post'], detail=True, permission_classes=(permissions.IsAuthenticated,))
    def like(self, request, pk=None):
        joke = self.get_object()
        joke.like(request.user)
        return Response({'joke %s is liked' % joke.label}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, permission_classes=(permissions.IsAuthenticated,))
    def dislike(self, request, pk=None):
        joke = self.get_object()
        joke.dislike(request.user)
        return Response({'joke %s is disliked' % joke.label}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, permission_classes=(permissions.IsAuthenticated,))
    def deactivate(self, request, pk=None):
        joke = self.get_object()
        joke.deactivate(request.user)
        return Response({'joke %s is deactivated' % joke.label}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_name='get-random', url_path='get-random')
    def get_random(self, request, *args, **kwargs):
        user = self.request.user

        def get_random_joke_from_qs(qs):
            if qs.exists():
                return queryset[randint(0, qs.count() - 1)]
            return None

        if user.is_authenticated:
            queryset = self.get_queryset()
            queryset = queryset.filter(is_seen=False)

            joke = get_random_joke_from_qs(queryset)
            if joke:
                JokeSeen.objects.create(joke=joke, user=user)
        else:
            data = {'seen_jokes': cache.get('seen_jokes', [])}

            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            seen_jokes = serializer.validated_data.get('seen_jokes')

            queryset = self.get_queryset()
            if seen_jokes:
                queryset = queryset.exclude(id__in=seen_jokes)

            joke = get_random_joke_from_qs(queryset)
            if joke:
                seen_jokes.append(joke.pk)
                cache.set('seen_jokes', seen_jokes)

        if not joke:
            # clear seen jokes
            if user.is_authenticated:
                user.jokeseen_set.all().delete()
            else:
                cache.set('seen_jokes', [])
            return Response({'text': 'There are no jokes left you have not seen',
                             'all_jokes_seen': True},
                            status=status.HTTP_200_OK)

        return Response(JokeSerializer(joke).data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, permission_classes=(permissions.AllowAny,),
            url_path='send-to-email', url_name='send-to-email')
    def send_to_email(self, request, pk=None):
        joke = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')

        try:
            is_send, result = joke.send_to_email(email)
            if not is_send:
                return Response({'non_field_errors': ['Email is not send. Please, try later!']},
                                status=status.HTTP_400_BAD_REQUEST)
        except exceptions.EmailConnectToMailException as e:
            return Response({'non_field_errors': ['Something went wrong! Please, try to send email later.']})

        return Response({'is_send': is_send, 'result': result}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, permission_classes=(permissions.AllowAny,),
            url_path='send-to-telegram', url_name='send-to-telegram')
    def send_to_telegram(self, request, pk=None):
        joke = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        nickname = serializer.validated_data.get('nickname')

        try:
            is_send, result = joke.send_to_telegram_username(nickname)
            if not is_send:
                return Response({'non_field_errors': ['Joke is not send. Please, try later!']},
                                status=status.HTTP_400_BAD_REQUEST)
        except exceptions.TelegramRecipientNotRegisteredInBotException as e:
            return Response({'non_field_errors': ['Probably you dont have conversation with our bot']},
                            status=status.HTTP_400_BAD_REQUEST)
        except exceptions.TelegramIncorrectRecipientException as e:
            return Response({'non_field_errors': ['Something went wrong! Please, try to send email later.']},
                            status=status.HTTP_400_BAD_REQUEST)
        except exceptions.TelegramConnectToBotException as e:
            return Response({'non_field_errors': ['Something went wrong! Please, try to send email later.']},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response({'is_send': is_send, 'result': result}, status=status.HTTP_200_OK)
