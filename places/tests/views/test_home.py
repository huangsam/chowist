from django.test import TestCase
from django.urls import reverse


class TestHomeView(TestCase):
    """HomeView test suite"""

    desired_url = "/places/"
    desired_name = "places:home"

    def test_desired_location(self):
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse(self.desired_name)
        self.assertEqual(reverse_url, self.desired_url)

    def test_get_with_valid_form_data(self):
        """Test GET request with valid form parameters redirects to restaurant list"""
        form_data = {"name": "test", "min_party": 2, "max_party": 10}
        resp = self.client.get(self.desired_url, form_data)
        self.assertEqual(resp.status_code, 302)  # Redirect
        self.assertIn("/places/restaurants/", resp.url)
        self.assertIn("name=test", resp.url)
        self.assertIn("min_party=2", resp.url)
        self.assertIn("max_party=10", resp.url)

    def test_get_with_invalid_form_data(self):
        """Test GET request with invalid form parameters still renders the form"""
        form_data = {"min_party": -1, "max_party": 5}  # Invalid: min_party < 1
        resp = self.client.get(self.desired_url, form_data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("form", resp.context)
