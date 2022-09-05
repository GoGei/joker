from factory import fuzzy, faker, SubFactory, DjangoModelFactory
from django.utils import timezone
from .models import Joke, JokeSeen, JokeLikeStatus


class JokeFactory(DjangoModelFactory):
    class Meta:
        model = Joke

    text = faker.Faker('paragraph', nb_sentences=5)


class JokeSeenFactory(DjangoModelFactory):
    class Meta:
        model = JokeSeen

    joke = SubFactory(JokeFactory)
    user = SubFactory('core.User.factories.UserFactory')
    seen_stamp = fuzzy.FuzzyDateTime(start_dt=timezone.now())


class JokeLikeStatusFactory(DjangoModelFactory):
    class Meta:
        model = JokeLikeStatus

    joke = SubFactory(JokeFactory)
    user = SubFactory('core.User.factories.UserFactory')
    is_liked = fuzzy.FuzzyChoice(choices=[True, False, None])
