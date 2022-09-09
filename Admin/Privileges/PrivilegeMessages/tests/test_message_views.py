import uuid
from urllib.parse import urlparse

from django.test import TestCase
from django.test import Client
from django_hosts import reverse

from core.User.factories import SuperuserFactory
from core.Privilege.models import PrivilegeMessage
from core.Privilege.factories import PrivilegeMessageFactory

from .test_message_data import message_data


class PrivilegeMessageViewTestCase(TestCase):
    def setUp(self):
        password = str(uuid.uuid4())
        self.user = SuperuserFactory.create(is_staff=True, is_superuser=True, is_active=True)
        self.user.set_password(password)
        self.user.save()

        self.client = Client()
        self.client.login(username=self.user.email, password=password)

        self.privilege_message = PrivilegeMessageFactory.create()
        self.privilege_user = self.privilege_message.privilege_user
        self.data = message_data.copy()
        self.data.update({'privilege_user': self.privilege_user})

    def test_privilege_message_list_get_success(self):
        response = self.client.get(reverse('privilege-message-list', args=[self.privilege_user.pk], host='admin'),
                                   HTTP_HOST='admin', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.privilege_message.pk)

    def test_privilege_message_add_get_success(self):
        response = self.client.get(reverse('privilege-message-add', args=[self.privilege_user.pk], host='admin'),
                                   HTTP_HOST='admin', format='json')
        self.assertEqual(response.status_code, 200)

    def test_privilege_message_add_post_success(self):
        PrivilegeMessage.objects.all().delete()
        data = self.data.copy()
        response = self.client.post(reverse('privilege-message-add', args=[self.privilege_user.pk], host='admin'),
                                    HTTP_HOST='admin', format='json', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(PrivilegeMessage.objects.exists())

    def test_privilege_message_add_post_cancel_success(self):
        data = {'_cancel': '_cancel'}
        response = self.client.post(reverse('privilege-message-add', args=[self.privilege_user.pk], host='admin'),
                                    HTTP_HOST='admin', format='json', data=data)
        self.assertEqual(response.status_code, 302)

        expected_url = urlparse(reverse('privilege-message-list', args=[self.privilege_user.pk], host='admin')).path
        self.assertRedirects(response, expected_url=expected_url)

    def test_privilege_message_edit_get_success(self):
        response = self.client.get(
            reverse('privilege-message-edit', host='admin', args=[self.privilege_user.pk, self.privilege_message.pk]),
            HTTP_HOST='admin', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.privilege_message.message)

    def test_privilege_message_edit_post_success(self):
        data = self.data.copy()
        response = self.client.post(
            reverse('privilege-message-edit', host='admin', args=[self.privilege_user.pk, self.privilege_message.pk]),
            HTTP_HOST='admin', data=data)
        self.assertEqual(response.status_code, 302)

    def test_privilege_message_edit_post_cancel_success(self):
        data = {'_cancel': '_cancel'}
        response = self.client.post(
            reverse('privilege-message-edit', host='admin', args=[self.privilege_user.pk, self.privilege_message.pk]),
            HTTP_HOST='admin', format='json', data=data)
        self.assertEqual(response.status_code, 302)

        expected_url = urlparse(reverse('privilege-message-list', args=[self.privilege_user.pk], host='admin')).path
        self.assertRedirects(response, expected_url=expected_url)

    def test_privilege_message_view_get_200(self):
        response = self.client.post(
            reverse('privilege-message-view', host='admin', args=[self.privilege_user.pk, self.privilege_message.pk]),
            HTTP_HOST='admin', format='json')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.privilege_message.pk)

    def test_privilege_message_delete_success(self):
        response = self.client.post(
            reverse('privilege-message-delete', host='admin', args=[self.privilege_user.pk, self.privilege_message.pk]),
            HTTP_HOST='admin', format='json')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(PrivilegeMessage.objects.all().exists())
