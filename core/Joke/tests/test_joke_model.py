from django.test import TestCase

from ..models import Joke, JokeSeen, JokeLikeStatus
from ..factories import JokeFactory, JokeSeenFactory, JokeLikeStatusFactory


class JokeTests(TestCase):
    def setUp(self):
        self.obj = JokeFactory.create()

    def test_create(self):
        obj = self.obj
        qs = Joke.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = self.obj
        obj.delete()

        qs = Joke.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())


class JokeSeenTests(TestCase):
    def setUp(self):
        self.obj = JokeSeenFactory.create()

    def test_create(self):
        obj = self.obj
        qs = JokeSeen.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = self.obj
        obj.delete()

        qs = JokeSeen.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())


class JokeLikeStatusTests(TestCase):
    def setUp(self):
        self.obj = JokeLikeStatusFactory.create()

    def test_create(self):
        obj = self.obj
        qs = JokeLikeStatus.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = self.obj
        obj.delete()

        qs = JokeLikeStatus.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())

    def test_like_obj(self):
        obj = self.obj
        obj.like()
        self.assertTrue(obj.is_liked is True)

    def test_dislike_obj(self):
        obj = self.obj
        obj.dislike()
        self.assertTrue(obj.is_liked is False)

    def test_deactivate_obj(self):
        obj = self.obj
        obj.deactivate()
        self.assertTrue(obj.is_liked is None)
