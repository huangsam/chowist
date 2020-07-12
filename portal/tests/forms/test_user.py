from django.test import TestCase

from portal.forms import UserForm


class TestUserForm(TestCase):
    """UserForm test suite"""

    def test_user_form_invalid_as_empty(self):
        form = UserForm()
        self.assertFalse(form.is_valid())

    def test_user_form_invalid_as_partial(self):
        form_data = {"username": "johndoe"}
        form = UserForm(form_data)
        self.assertFalse(form.is_valid())

    def test_user_form_valid_as_partial(self):
        form_data = {"username": "johndoe", "password": "s3cret123"}
        form = UserForm(form_data)
        self.assertTrue(form.is_valid())

    def test_user_form_valid_as_full(self):
        form_data = {
            "username": "johndoe",
            "email": "johndoe@example.org",
            "password": "s3cret123",
        }
        form = UserForm(form_data)
        self.assertTrue(form.is_valid())
