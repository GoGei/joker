import uuid
from urllib.parse import urlparse

from django.test import TestCase
from django.test import Client
from django_hosts import reverse

from core.Joke.models import Joke
from core.User.factories import SuperuserFactory
from core.Joke.factories import JokeFactory

from .test_joke_data import joke_data


class JokeViewTestCase(TestCase):
    def setUp(self):
        password = str(uuid.uuid4())
        self.user = SuperuserFactory.create(is_staff=True, is_superuser=True, is_active=True)
        self.user.set_password(password)
        self.user.save()

        self.client = Client()
        self.client.login(username=self.user.email, password=password)

        self.joke = JokeFactory.create()
        self.data = joke_data.copy()

    def test_jokes_list_get_success(self):
        response = self.client.get(reverse('jokes-list', host='admin'), HTTP_HOST='admin', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.joke.id)

    def test_jokes_add_get_success(self):
        response = self.client.get(reverse('jokes-add', host='admin'), HTTP_HOST='admin', format='json')
        self.assertEqual(response.status_code, 200)

    def test_jokes_add_post_success(self):
        Joke.objects.all().delete()
        data = self.data.copy()
        response = self.client.post(reverse('jokes-add', host='admin'), HTTP_HOST='admin', format='json', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Joke.objects.exists())

    def test_jokes_add_post_cancel_success(self):
        data = {'_cancel': '_cancel'}
        response = self.client.post(reverse('jokes-add', host='admin'), HTTP_HOST='admin', format='json', data=data)
        self.assertEqual(response.status_code, 302)

        expected_url = urlparse(reverse('jokes-list', host='admin')).path
        self.assertRedirects(response, expected_url=expected_url)

    def test_jokes_edit_get_success(self):
        response = self.client.get(reverse('jokes-edit', host='admin', args=[self.joke.slug]), HTTP_HOST='admin',
                                   format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.joke.text)

    def test_jokes_edit_post_success(self):
        data = self.data.copy()
        response = self.client.post(reverse('jokes-edit', host='admin', args=[self.joke.slug]),
                                    HTTP_HOST='admin', data=data)
        self.assertEqual(response.status_code, 302)

    def test_jokes_edit_post_cancel_success(self):
        data = {'_cancel': '_cancel'}
        response = self.client.post(reverse('jokes-edit', host='admin', args=[self.joke.slug]),
                                    HTTP_HOST='admin', format='json', data=data)
        self.assertEqual(response.status_code, 302)

        expected_url = urlparse(reverse('jokes-list', host='admin')).path
        self.assertRedirects(response, expected_url=expected_url)

    def test_jokes_view_get_200(self):
        response = self.client.post(reverse('jokes-view', host='admin', args=[self.joke.slug]), HTTP_HOST='admin',
                                    format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.joke.pk)

    def test_jokes_archive_success(self):
        response = self.client.post(reverse('jokes-archive', host='admin', args=[self.joke.slug]), HTTP_HOST='admin',
                                    format='json')
        self.assertEqual(response.status_code, 302)
        self.joke.refresh_from_db()
        self.assertTrue(self.joke.archived_stamp)

    def test_jokes_restore_success(self):
        response = self.client.post(reverse('jokes-restore', host='admin', args=[self.joke.slug]), HTTP_HOST='admin',
                                    format='json')
        self.assertEqual(response.status_code, 302)
        self.joke.refresh_from_db()
        self.assertFalse(self.joke.archived_stamp)

    def test_jokes_delete_success(self):
        response = self.client.post(reverse('jokes-delete', host='admin', args=[self.joke.slug]), HTTP_HOST='admin',
                                    format='json')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Joke.objects.all().exists())
