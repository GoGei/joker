from django.test import TestCase
from core.User.models import User
from core.User.factories import UserFactory
from ..forms import UserFilterForm
from .test_user_data import user_data, user_filter_data


class UserFilterTestCase(TestCase):
    def setUp(self):
        self.form = UserFilterForm
        self.data = user_filter_data.copy()
        self.obj = UserFactory.create(email=user_data['email'])

    def test_obj_filter_valid(self):
        form = self.form(self.data)
        self.assertTrue(form.is_valid())

    def test_obj_filter_obj_found(self):
        obj = self.obj
        data = self.data.copy()
        form = self.form(data, queryset=User.objects.all())
        self.assertTrue(form.is_valid())
        self.assertIn(obj, form.qs)

        for key, value in data.items():
            form = self.form({key: value})
            self.assertIn(obj, form.qs)

    def test_obj_filter_obj_not_found(self):
        obj = self.obj
        data = self.data.copy()
        data.update({'search': 'my-email-to-not-found'})
        form = self.form(data, queryset=User.objects.all())
        self.assertTrue(form.is_valid())
        self.assertNotIn(obj, form.qs)

    def test_obj_search_success(self):
        obj = self.obj
        search_to = (obj.email[:10],)
        for search in search_to:
            data = {'search': search}
            form = self.form(data, queryset=User.objects.all())
            self.assertIn(obj, form.qs)
