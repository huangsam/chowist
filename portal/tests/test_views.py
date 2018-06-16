from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestHomeView(TestCase):
    """HomeView test suite"""

    desired_url = '/'
    desired_name = 'portal:home'

    def test_desired_location(self):
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse(self.desired_name)
        self.assertEquals(reverse_url, self.desired_url)


class TestUserFormView(TestCase):
    """UserFormView test suite"""

    desired_url = '/signup/'
    desired_name = 'portal:signup'

    def test_desired_location(self):
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse(self.desired_name)
        self.assertEquals(reverse_url, self.desired_url)


class TestProfileFormView(TestCase):
    """ProfileFormView test suite"""

    desired_url = '/profile/'
    desired_name = 'portal:profile'

    def setUp(self):
        User.objects.create_user('john', 'john@example.org', 'secret123')

    def test_desired_location(self):
        self.client.login(username='john', password='secret123')
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)
        self.client.logout()
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 302)

    def test_desired_location_redirect(self):
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 302)

    def test_desired_name(self):
        reverse_url = reverse(self.desired_name)
        self.assertEquals(reverse_url, self.desired_url)
