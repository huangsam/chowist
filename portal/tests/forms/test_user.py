from django.test import TestCase

from portal.forms import UserForm


class TestUserForm(TestCase):
    """UserForm test suite"""

    def test_user_form_invalid(self):
        form = UserForm()
        self.assertFalse(form.is_valid())

    def test_user_form_valid(self):
        form_data = {
            "username": "johndoe",
            "email": "johndoe@example.org",
            "password": "s3cret123",
        }
        form = UserForm(form_data)
        self.assertTrue(form.is_valid())
