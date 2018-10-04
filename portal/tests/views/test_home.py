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
