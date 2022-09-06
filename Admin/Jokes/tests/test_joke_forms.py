import json
from django.test import TestCase
from core.Joke.models import Joke
from core.Joke.factories import JokeFactory
from ..forms import JokeFilterForm, JokeForm
from .test_joke_data import joke_data, joke_empty_data, joke_error_data, joke_filter_data


class JokeFormTestCase(TestCase):
    def setUp(self):
        self.form = JokeForm

    def test_obj_form_valid(self):
        data = joke_data.copy()
        form = self.form(data)
        self.assertTrue(form.is_valid())

    def test_obj_form_invalid_errors(self):
        data = joke_empty_data.copy()
        form = self.form(data)
        self.assertFalse(form.is_valid())
        errors = json.dumps(form.errors)
        for key in data.keys():
            self.assertIn(key, errors)

    def test_obj_form_invalid_empty(self):
        data = joke_error_data.copy()
        form = self.form(data)
        self.assertFalse(form.is_valid())
        errors = json.dumps(form.errors)
        for key in data.keys():
            self.assertIn(key, errors)


class JokeFilterTestCase(TestCase):
    def setUp(self):
        self.form = JokeFilterForm
        self.data = joke_filter_data.copy()
        self.obj = JokeFactory.create(text=joke_data['text'])

    def test_obj_filter_valid(self):
        form = self.form(self.data)
        self.assertTrue(form.is_valid())

    def test_obj_filter_obj_found(self):
        obj = self.obj
        data = self.data.copy()
        form = self.form(data, queryset=Joke.objects.all())
        self.assertTrue(form.is_valid())
        self.assertIn(obj, form.qs)

        for key, value in data.items():
            form = self.form({key: value})
            self.assertIn(obj, form.qs)

    def test_obj_filter_obj_not_found(self):
        obj = self.obj
        data = self.data.copy()
        data.update({'search': 'my-text-to-not-found'})
        form = self.form(data, queryset=Joke.objects.all())
        self.assertTrue(form.is_valid())
        self.assertNotIn(obj, form.qs)

    def test_obj_search_success(self):
        obj = self.obj
        search_to = (obj.text[:10],)
        for search in search_to:
            data = {'search': search}
            form = self.form(data, queryset=Joke.objects.all())
            self.assertIn(obj, form.qs)
