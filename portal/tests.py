from django.test import TestCase
from portal.forms import UserForm

# Create your tests here.

class UserFormTestCase(TestCase):
    """UserForm test suite"""

    def test_userform_invalid(self):
        form = UserForm()
        self.assertEquals(form.is_valid(), False)

    def test_userform_valid(self):
        form_data = {
            'username': 'johndoe',
            'email': 'johndoe@example.org',
            'password': 's3cret123'
        }
        form = UserForm(form_data)
        self.assertEquals(form.is_valid(), True)
