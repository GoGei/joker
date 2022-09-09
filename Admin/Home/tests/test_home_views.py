import uuid

from django.test import TestCase
from django.test import Client
from django_hosts import reverse

from core.User.factories import SuperuserFactory


class HomeViewTestCase(TestCase):
    def setUp(self):
        password = str(uuid.uuid4())
        self.user = SuperuserFactory.create(is_staff=True, is_superuser=True, is_active=True)
        self.user.set_password(password)
        self.user.save()

        self.client = Client()
        self.client.login(username=self.user.email, password=password)

    def test_home_get_success(self):
        response = self.client.get(reverse('admin-home', host='admin'), HTTP_HOST='admin', format='json')
        self.assertEqual(response.status_code, 200)
