from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class HomeViewTestCase(TestCase):
    """HomeView test suite"""

    desired_url = '/'
    desired_name = 'portal:home'

    def test_desired_location(self):
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse(self.desired_name)
        self.assertEquals(reverse_url, self.desired_url)


class LoginViewTestCase(TestCase):
    """LoginView test suite"""

    desired_url = '/accounts/login/'
    desired_name = 'portal:login'

    def test_desired_location(self):
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse(self.desired_name)
        self.assertEquals(reverse_url, self.desired_url)


class LogoutViewTestCase(TestCase):
    """LogoutView test suite"""

    desired_url = '/accounts/logout/'
    desired_name = 'portal:logout'

    def test_desired_location(self):
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse(self.desired_name)
        self.assertEquals(reverse_url, self.desired_url)


class UserFormViewTestCase(TestCase):
    """UserFormView test suite"""

    desired_url = '/signup/'
    desired_name = 'portal:signup'

    def test_desired_location(self):
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse(self.desired_name)
        self.assertEquals(reverse_url, self.desired_url)
