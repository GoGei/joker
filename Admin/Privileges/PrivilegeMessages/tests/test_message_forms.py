import json
from django.test import TestCase
from core.Privilege.factories import PrivilegeUserFactory
from ..forms import PrivilegeMessageForm
from .test_message_data import message_data, message_error_data, message_empty_data


class PrivilegeMessageFormTestCase(TestCase):
    def setUp(self):
        self.form = PrivilegeMessageForm
        self.privilege_user = PrivilegeUserFactory.create()

    def test_obj_form_valid(self):
        data = message_data.copy()
        form = self.form(data, privilege_user=self.privilege_user)
        self.assertTrue(form.is_valid())

    def test_obj_form_invalid_errors(self):
        data = message_error_data.copy()
        form = self.form(data, privilege_user=self.privilege_user)
        self.assertFalse(form.is_valid())
        errors = json.dumps(form.errors)
        for key in data.keys():
            self.assertIn(key, errors)

    def test_obj_form_invalid_empty(self):
        data = message_empty_data.copy()
        form = self.form(data, privilege_user=self.privilege_user)
        self.assertFalse(form.is_valid())
        errors = json.dumps(form.errors)
        for key in data.keys():
            self.assertIn(key, errors)
