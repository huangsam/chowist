from django.test import TestCase

from portal.forms import UserForm


class TestUserForm(TestCase):
    """UserForm test suite"""

    def test_user_form_invalid_with_empty(self):
        form = UserForm()
        self.assertFalse(form.is_valid())

    def test_user_form_invalid_with_partial(self):
        form_data = {"username": "johndoe"}
        form = UserForm(form_data)
        self.assertFalse(form.is_valid())

    def test_user_form_valid_with_partial(self):
        form_data = {"username": "johndoe", "password": "s3cret123"}
        form = UserForm(form_data)
        self.assertTrue(form.is_valid())

    def test_user_form_invalid_with_full_blank(self):
        form_data = {
            "username": "",
            "email": "",
            "password": "",
        }
        form = UserForm(form_data)
        self.assertFalse(form.is_valid())

    def test_user_form_valid_with_full_fill(self):
        form_data = {
            "username": "johndoe",
            "email": "johndoe@example.org",
            "password": "s3cret123",
        }
        form = UserForm(form_data)
        self.assertTrue(form.is_valid())
