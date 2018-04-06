from django.test import TestCase

from portal.forms import UserForm, ProfileForm

# Create your tests here.

class UserFormTestCase(TestCase):
    """UserForm test suite"""

    def test_userform_invalid(self):
        form = UserForm()
        self.assertFalse(form.is_valid())

    def test_userform_valid(self):
        form_data = {
            'username': 'johndoe',
            'email': 'johndoe@example.org',
            'password': 's3cret123'
        }
        form = UserForm(form_data)
        self.assertTrue(form.is_valid())


class ProfileFormTestCase(TestCase):
    """ProfileForm test suite"""

    def test_profileform_invalid(self):
        pass

    def test_profileform_valid(self):
        pass
