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
        form_data = {"username": "johndoe", "password": "s3cret123", "password_confirm": "s3cret123"}
        form = UserForm(form_data)
        self.assertTrue(form.is_valid())

    def test_user_form_invalid_with_full_blank(self):
        form_data = {
            "username": "",
            "email": "",
            "password": "",
            "password_confirm": "",
        }
        form = UserForm(form_data)
        self.assertFalse(form.is_valid())

    def test_user_form_valid_with_full_fill(self):
        form_data = {
            "username": "johndoe",
            "email": "johndoe@example.org",
            "password": "s3cret123",
            "password_confirm": "s3cret123",
        }
        form = UserForm(form_data)
        self.assertTrue(form.is_valid())

    def test_user_form_invalid_password_mismatch(self):
        form_data = {
            "username": "johndoe",
            "email": "johndoe@example.org",
            "password": "s3cret123",
            "password_confirm": "different123",
        }
        form = UserForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Passwords do not match", str(form.errors))

    def test_user_form_invalid_password_weak(self):
        form_data = {
            "username": "johndoe",
            "email": "johndoe@example.org",
            "password": "weak",
            "password_confirm": "weak",
        }
        form = UserForm(form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Password must be at least 8 characters", str(form.errors))
