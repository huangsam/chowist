from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class TestProfileDetailView(TestCase):
    """ProfileDetailView test suite"""

    desired_url = "/profile/"
    desired_name = "portal:profile"

    def setUp(self):
        User.objects.create_user("john", "john@localhost", "john")

    def test_desired_location(self):
        self.client.login(username="john", password="john")
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_location_redirect(self):
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 302)

    def test_desired_name(self):
        reverse_url = reverse(self.desired_name)
        self.assertEquals(reverse_url, self.desired_url)


class TestProfileUpdateView(TestProfileDetailView):
    """ProfileUpdateView test suite"""

    desired_url = "/profile/update/"
    desired_name = "portal:profile_update"


class TestProfileSignupView(TestCase):
    """ProfileSignupView test suite"""

    desired_url = "/signup/"
    desired_name = "portal:signup"

    def test_desired_location(self):
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse(self.desired_name)
        self.assertEquals(reverse_url, self.desired_url)
