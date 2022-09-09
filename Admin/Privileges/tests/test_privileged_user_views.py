import uuid
from urllib.parse import urlparse

from django.test import TestCase
from django.test import Client
from django_hosts import reverse

from core.Privilege.models import PrivilegeUser
from core.Privilege.factories import PrivilegeUserFactory
from core.User.factories import SuperuserFactory, UserFactory


class PrivilegeUsersViewTestCase(TestCase):
    def setUp(self):
        password = str(uuid.uuid4())
        self.user = SuperuserFactory.create(is_staff=True, is_superuser=True, is_active=True)
        self.user.set_password(password)
        self.user.save()

        self.client = Client()
        self.client.login(username=self.user.email, password=password)

        self.privileged_user = PrivilegeUserFactory.create()
        self.data = {
            'user': UserFactory.create().id
        }
        self.error_data = {
            'user': SuperuserFactory.create().id
        }

    def test_privileged_users_list_get_success(self):
        response = self.client.get(reverse('privileged-user-list', host='admin'), HTTP_HOST='admin', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.privileged_user.user.email)

    def test_privileged_users_add_get_success(self):
        response = self.client.get(reverse('privileged-user-add', host='admin'), HTTP_HOST='admin', format='json')
        self.assertEqual(response.status_code, 200)

    def test_privileged_users_add_post_success(self):
        PrivilegeUser.objects.all().delete()
        data = self.data.copy()
        response = self.client.post(reverse('privileged-user-add', host='admin'), HTTP_HOST='admin', format='json',
                                    data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PrivilegeUser.objects.exists())

        response = self.client.post(reverse('privileged-user-add', host='admin'), HTTP_HOST='admin', format='json',
                                    data=data)
        self.assertEqual(response.status_code, 200)

    def test_privileged_users_add_post_error(self):
        PrivilegeUser.objects.all().delete()
        data = self.error_data.copy()
        response = self.client.post(reverse('privileged-user-add', host='admin'), HTTP_HOST='admin', format='json',
                                    data=data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(PrivilegeUser.objects.exists())

    def test_privileged_users_add_post_cancel_success(self):
        data = {'_cancel': '_cancel'}
        response = self.client.post(reverse('privileged-user-add', host='admin'), HTTP_HOST='admin', format='json',
                                    data=data)
        self.assertEqual(response.status_code, 302)

        expected_url = urlparse(reverse('privileged-user-list', host='admin')).path
        self.assertRedirects(response, expected_url=expected_url)

    def test_privileged_users_view_get_200(self):
        response = self.client.post(reverse('privileged-user-view', host='admin', args=[self.privileged_user.id]),
                                    HTTP_HOST='admin', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.privileged_user.user.email)

    def test_privileged_users_delete_success(self):
        response = self.client.post(reverse('privileged-user-delete', host='admin', args=[self.privileged_user.id]),
                                    HTTP_HOST='admin', format='json')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(PrivilegeUser.objects.all().exists())
