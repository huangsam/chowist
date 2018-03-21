from django.test import TestCase
from django.urls import reverse

from places.models import Restaurant

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
    restaurant_count = 25

    @classmethod
    def setUpTestData(cls):
        for i in range(cls.restaurant_count):
            Restaurant.objects.create(
                name='Five Guys {rid}'.format(rid=i), address='Bogus {rid}'.format(rid=i),
                latitude=0.00, longitude=0.00,
                min_party=1, max_party=6,
                yelp_link='/five-guys-earth-{rid}'.format(rid=i))

    def test_desired_location(self):
        resp = self.client.get(self.expected_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse('places:restaurant-list')
        self.assertEquals(reverse_url, self.expected_url)

    def test_desired_data(self):
        resp = self.client.get(self.expected_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['restaurant_list']), self.restaurant_count)
