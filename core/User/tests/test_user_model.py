from django.test import TestCase

from ..models import User
from ..factories import UserFactory


class UserTests(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        obj = UserFactory.create()
        qs = User.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = UserFactory.create()
        obj.delete()

        qs = User.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())
