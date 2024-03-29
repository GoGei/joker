from typing import List, Dict
import celery
from slugify import slugify

from django.db import models
from django.db.models import Count, Q
from django.db.models.expressions import RawSQL
from django.utils import timezone
from django.utils.html import strip_tags
from django.conf import settings
from django.template.loader import render_to_string

from core.Utils.Mixins.models import CrmMixin, SlugifyMixin, LikeMixin, ExportableMixin
from core.Utils.Mixins.exceptions import SlugifyFieldNotSetException
from .tasks import send_joke_to_email, send_joke_to_telegram


class Joke(CrmMixin, SlugifyMixin, ExportableMixin):
    BASE_TEMPLATE = 'core_templates/joke_template_message.html'
    SLUGIFY_FIELD = 'text'
    MAX_LENGTH = 4096
    text = models.CharField(max_length=4096)

    class Meta:
        db_table = 'joke'

    @property
    def label(self):
        return str(self)

    def __str__(self):
        return self.slug

    @classmethod
    def slugify_without_html(cls, value):
        return slugify(strip_tags(value))

    @classmethod
    def is_allowed_to_assign_slug(cls, value, instance=None):
        slug = cls.slugify_without_html(value)
        qs = cls.objects.exclude(slug__isnull=True, slug__exact='').filter(slug=slug)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        return not qs.exists()

    def assign_slug(self):
        if not self.SLUGIFY_FIELD:
            raise SlugifyFieldNotSetException('Field for slugify not set!')

        slug = self.slugify_without_html(getattr(self, self.SLUGIFY_FIELD))
        self.slug = slug if len(slug) <= 255 else slug[:255]
        self.save()
        return self

    def like(self, user):
        like_status, _ = JokeLikeStatus.objects.get_or_create(joke=self, user=user)
        like_status.like()
        return self

    def dislike(self, user):
        like_status, _ = JokeLikeStatus.objects.get_or_create(joke=self, user=user)
        like_status.dislike()
        return self

    def deactivate(self, user):
        like_status, _ = JokeLikeStatus.objects.get_or_create(joke=self, user=user)
        like_status.deactivate()
        return self

    def make_seen(self, user):
        JokeSeen.objects.create(joke=self, user=user)
        return self

    @classmethod
    def annotate_qs_by_user(cls, qs, user=None):
        if not (user and user.is_authenticated):
            qs = qs.annotate(is_liked=models.Value(None, output_field=models.NullBooleanField()))
            return qs

        qs = qs.annotate(
            is_liked=RawSQL(
                'select is_liked from joke_like_status where user_id=%s AND joke_id=joke.id', (user.id,)),
            liked_order=RawSQL(
                'select id from joke_like_status where user_id=%s AND joke_id=joke.id', (user.id,))
        )

        return qs

    @property
    def prepared_html_message(self):
        base_template = self.BASE_TEMPLATE
        context = {'joke_text': self.text}

        html_message = render_to_string(base_template, context)
        return html_message

    @property
    def prepared_plain_message(self):
        html_message = self.prepared_html_message
        plain_message = strip_tags(html_message)
        return plain_message

    def send_to_email(self, target):
        async_result = send_joke_to_email.apply_async(kwargs={'joke': self, 'recipient': target})
        try:
            is_send, result = async_result.get(timeout=settings.CELERY_TASK_TIMEOUT)
        except celery.exceptions.TimeoutError:
            is_send, result = False, None
        return is_send, result

    def send_to_telegram_username(self, target):
        async_result = send_joke_to_telegram.apply_async(kwargs={'joke': self, 'recipient': target})
        try:
            is_send, result = async_result.get(timeout=settings.CELERY_TASK_TIMEOUT)
        except celery.exceptions.TimeoutError:
            is_send, result = False, None
        return is_send, result

    @classmethod
    def get_unseen_jokes(cls, user):
        queryset = cls.objects.prefetch_related('jokeseen_set', 'jokelikestatus_set')
        queryset = queryset.annotate(is_seen=models.Exists(
            JokeSeen.objects.filter(
                joke=models.OuterRef('pk'),
                user=user
            )))
        queryset = queryset.filter(is_seen=False)
        return queryset

    @classmethod
    def clear_seen_jokes(cls, user):
        user.jokeseen_set.all().delete()
        return True

    def to_json(self):
        return {
            'text': self.text,
            'slug': self.slug,
            'is_active': self.is_active(),
        }

    @classmethod
    def get_data_to_export(cls) -> List[Dict]:
        qs = JokeLikeStatus.objects.select_related('joke').filter(is_liked=True)
        liked = set(qs.values_list('joke_id', flat=True))
        qs = cls.objects.filter(id__in=liked).all()
        data = [
            {
                'text': item.text,
            } for item in qs
        ]
        return data


class JokeSeen(models.Model):
    joke = models.ForeignKey('Joke.Joke', on_delete=models.CASCADE)
    user = models.ForeignKey('User.User', on_delete=models.CASCADE)
    seen_stamp = models.DateTimeField(default=timezone.now, db_index=True)

    class Meta:
        db_table = 'joke_seen'


class JokeLikeStatus(LikeMixin):
    joke = models.ForeignKey('Joke.Joke', on_delete=models.CASCADE)

    class Meta:
        db_table = 'joke_like_status'
