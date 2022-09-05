from django.test import TestCase

from ..models import PrivilegeUser, PrivilegeMessage
from ..factories import PrivilegeUserFactory, PrivilegeMessageFactory


class PrivilegeUserTests(TestCase):
    def setUp(self):
        self.obj = PrivilegeUserFactory.create()

    def test_create(self):
        obj = self.obj
        qs = PrivilegeUser.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = self.obj
        obj.delete()

        qs = PrivilegeUser.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())


class PrivilegeMessageTests(TestCase):
    def setUp(self):
        self.obj = PrivilegeMessageFactory.create()

    def test_create(self):
        obj = self.obj
        qs = PrivilegeMessage.objects.filter(pk=obj.pk)
        self.assertTrue(qs.exists())
        self.assertEqual(qs[0], obj)

    def test_delete(self):
        obj = self.obj
        obj.delete()

        qs = PrivilegeMessage.objects.filter(pk=obj.pk)
        self.assertFalse(qs.exists())
