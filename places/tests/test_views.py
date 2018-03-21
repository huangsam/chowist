from django.test import TestCase
from django.urls import reverse

from places.models import Restaurant

# Create your tests here.

class HomeViewTestCase(TestCase):
    """HomeView test suite"""

    expected_url = '/places/'
    reverse_name = 'places:home'

    def test_desired_location(self):
        resp = self.client.get(self.expected_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse(self.reverse_name)
        self.assertEquals(reverse_url, self.expected_url)


class RestaurantListViewTestCase(TestCase):
    """RestaurantListView test suite"""

    expected_url = '/places/restaurants/'
    reverse_name = 'places:restaurant-list'
    restaurant_count = 25

    @classmethod
    def setUpTestData(cls):
        for i in range(cls.restaurant_count):
            Restaurant.objects.create(
                name='Chipotle {rid}'.format(rid=i), address='Bogus {rid}'.format(rid=i),
                latitude=0.00, longitude=0.00,
                min_party=1, max_party=6,
                yelp_link='/chipotle-bogus-{rid}'.format(rid=i))

    def test_desired_location(self):
        resp = self.client.get(self.expected_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse(self.reverse_name)
        self.assertEquals(reverse_url, self.expected_url)

    def test_desired_data(self):
        resp = self.client.get(self.expected_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['restaurant_list']), self.restaurant_count)


class RestaurantDetailViewTestCase(TestCase):
    """RestaurantDetailView test suite"""

    restaurant_id = 1
    expected_url = '/places/restaurants/{rid}'.format(rid=restaurant_id)
    reverse_name = 'places:restaurant-detail'

    @classmethod
    def setUpTestData(cls):
        Restaurant.objects.create(
            name='Chick Fil A', address='Venus',
            latitude=0.00, longitude=0.00,
            min_party=3, max_party=8,
            yelp_link='/chick-fil-a-venus')

    def test_desired_location(self):
        resp = self.client.get(self.expected_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse(self.reverse_name, args=(self.restaurant_id,))
        self.assertEquals(reverse_url, self.expected_url)

    def test_desired_data(self):
        resp = self.client.get(self.expected_url)
        self.assertEqual(resp.status_code, 200)
        restaurant = resp.context['restaurant']
        self.assertTrue(type(restaurant) == Restaurant)
        self.assertEqual(restaurant.name, 'Chick Fil A')
        self.assertEqual(restaurant.min_party, 3)
        self.assertEqual(restaurant.max_party, 8)
