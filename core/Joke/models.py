from django.db import models
from django.utils import timezone
from core.Utils.Mixins.models import CrmMixin, SlugifyMixin, LikeMixin


class Joke(CrmMixin, SlugifyMixin):
    SLUGIFY_FIELD = 'text'
    text = models.CharField(max_length=4096)

    class Meta:
        db_table = 'joke'

    @property
    def label(self):
        return str(self)

    def __str__(self):
        return self.text


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
