from django.test import TestCase

from portal.forms import ProfileForm


class TestProfileForm(TestCase):
    """ProfileForm test suite"""

    def test_profile_form_invalid_with_empty(self):
        form = ProfileForm()
        self.assertFalse(form.is_valid())

    def test_profile_form_invalid_with_partial(self):
        form_data = {"bio": "helloworld"}
        form = ProfileForm(form_data)
        self.assertFalse(form.is_valid())

    def test_profile_form_invalid_with_birth_date(self):
        form_data = {
            "bio": "helloworld",
            "address": "123 World",
            "birth_date": "123456789",
        }
        form = ProfileForm(form_data)
        self.assertFalse(form.is_valid())

    def test_profile_form_invalid_with_full_blank(self):
        form_data = {
            "bio": "",
            "address": "",
            "birth_date": "",
        }
        form = ProfileForm(form_data)
        self.assertFalse(form.is_valid())

    def test_profile_form_valid_with_full_fill(self):
        form_data = {
            "bio": "helloworld",
            "address": "123 World",
            "birth_date": "1111-01-01",
        }
        form = ProfileForm(form_data)
        self.assertTrue(form.is_valid())
