import json
from django.test import TestCase
from core.Privilege.models import PrivilegeUser
from core.Privilege.factories import PrivilegeUserFactory
from core.User.factories import UserFactory, SuperuserFactory
from ..forms import PrivilegeUserFilterForm, PrivilegeUserForm


class PrivilegeUserFormTestCase(TestCase):
    def setUp(self):
        self.form = PrivilegeUserForm
        self.user = UserFactory.create()
        self.superuser = SuperuserFactory.create()

    def test_obj_form_valid(self):
        data = {
            'user': self.user
        }
        form = self.form(data)
        self.assertTrue(form.is_valid())

    def test_obj_form_invalid_errors(self):
        data = {
            'user': self.superuser
        }
        form = self.form(data)
        self.assertFalse(form.is_valid())
        errors = json.dumps(form.errors)
        for key in data.keys():
            self.assertIn(key, errors)

    def test_obj_form_invalid_empty(self):
        data = {}
        form = self.form(data)
        self.assertFalse(form.is_valid())
        errors = json.dumps(form.errors)
        for key in data.keys():
            self.assertIn(key, errors)


class PrivilegeUserFilterTestCase(TestCase):
    def setUp(self):
        self.form = PrivilegeUserFilterForm
        self.obj = PrivilegeUserFactory.create()
        self.data = {
            'search': self.obj.user.email
        }

    def test_obj_filter_valid(self):
        form = self.form(self.data)
        self.assertTrue(form.is_valid())

    def test_obj_filter_obj_found(self):
        obj = self.obj
        data = self.data.copy()
        form = self.form(data, queryset=PrivilegeUser.objects.all())
        self.assertTrue(form.is_valid())
        self.assertIn(obj, form.qs)

        for key, value in data.items():
            form = self.form({key: value})
            self.assertIn(obj, form.qs)

    def test_obj_filter_obj_not_found(self):
        obj = self.obj
        data = self.data.copy()
        data.update({'search': 'my-text-to-not-found'})
        form = self.form(data, queryset=PrivilegeUser.objects.all())
        self.assertTrue(form.is_valid())
        self.assertNotIn(obj, form.qs)

    def test_obj_search_success(self):
        obj = self.obj
        search_to = (obj.user.email[:10],)
        for search in search_to:
            data = {'search': search}
            form = self.form(data, queryset=PrivilegeUser.objects.all())
            self.assertIn(obj, form.qs)
