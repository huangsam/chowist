from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class HomeViewTestCase(TestCase):
    """HomeView test suite"""

    expected_url = '/'

    def test_desired_location(self):
        resp = self.client.get(self.expected_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse('portal:home')
        self.assertEquals(reverse_url, self.expected_url)


class LoginViewTestCase(TestCase):
    """LoginView test suite"""

    expected_url = '/login/'

    def test_desired_location(self):
        resp = self.client.get(self.expected_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse('portal:login')
        self.assertEquals(reverse_url, self.expected_url)


class LogoutViewTestCase(TestCase):
    """LogoutView test suite"""

    expected_url = '/logout/'

    def test_desired_location(self):
        resp = self.client.get(self.expected_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse('portal:logout')
        self.assertEquals(reverse_url, self.expected_url)


class UserFormViewTestCase(TestCase):
    """UserFormView test suite"""

    expected_url = '/register/'

    def test_desired_location(self):
        resp = self.client.get(self.expected_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse('portal:register')
        self.assertEquals(reverse_url, self.expected_url)
