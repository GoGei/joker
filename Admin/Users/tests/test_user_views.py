import uuid

from django.test import TestCase
from django.test import Client
from django_hosts import reverse

from core.User.models import User
from core.User.factories import SuperuserFactory, UserFactory


class JokeViewTestCase(TestCase):
    def setUp(self):
        password = str(uuid.uuid4())
        self.user = SuperuserFactory.create(is_staff=True, is_superuser=True, is_active=True)
        self.user.set_password(password)
        self.user.save()

        self.client = Client()
        self.client.login(username=self.user.email, password=password)

    def test_users_list_get_success(self):
        response = self.client.get(reverse('users-list', host='admin'), HTTP_HOST='admin', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.id)

    def test_users_view_get_200(self):
        response = self.client.post(reverse('users-view', host='admin', args=[self.user.id]), HTTP_HOST='admin',
                                    format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user)

    def test_jokes_delete_success(self):
        user = UserFactory.create()
        response = self.client.post(reverse('users-delete', host='admin', args=[user.id]), HTTP_HOST='admin',
                                    format='json')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(pk=user.pk).exists())
