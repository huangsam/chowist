from django.test import TestCase
from django.urls import reverse

# Create your tests here.

class HomeViewTestCase(TestCase):
    """HomeView test suite"""

    expected_url = '/places/'

    def test_desired_location(self):
        resp = self.client.get(self.expected_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse('places:home')
        self.assertEquals(reverse_url, self.expected_url)


class RestaurantListViewTestCase(TestCase):
    """RestaurantListView test suite"""

    expected_url = '/places/restaurants/'

    def test_desired_location(self):
        resp = self.client.get(self.expected_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse('places:restaurant-list')
        self.assertEquals(reverse_url, self.expected_url)
