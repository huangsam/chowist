from django.test import TestCase

from portal.forms import ProfileForm


class TestProfileForm(TestCase):
    """ProfileForm test suite"""

    def test_profileform_invalid(self):
        form = ProfileForm()
        self.assertFalse(form.is_valid())

    def test_profileform_valid(self):
        form_data = {
            "bio": "helloworld",
            "address": "123 World",
            "birth_date": "1111-01-01",
        }
        form = ProfileForm(form_data)
        self.assertTrue(form.is_valid())