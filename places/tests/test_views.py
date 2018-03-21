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

    reverse_name = 'places:restaurant-detail'

    @classmethod
    def setUpTestData(cls):
        Restaurant.objects.create(
            name='Chick Fil A', address='Venus',
            latitude=0.00, longitude=0.00,
            min_party=3, max_party=8,
            yelp_link='/chick-fil-a-venus')

    def setUp(self):
        self.good_id = 1
        self.bad_id = 2
        self.good_url = '/places/restaurants/{rid}'.format(rid=self.good_id)
        self.bad_url = '/places/restaurants/{rid}'.format(rid=self.bad_id)

    def test_desired_location(self):
        resp = self.client.get(self.good_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse(self.reverse_name, args=(self.good_id,))
        self.assertEquals(reverse_url, self.good_url)

    def test_desired_data(self):
        resp = self.client.get(self.good_url)
        self.assertEqual(resp.status_code, 200)
        restaurant = resp.context['restaurant']
        self.assertTrue(type(restaurant) == Restaurant)
        self.assertEqual(restaurant.name, 'Chick Fil A')
        self.assertEqual(restaurant.min_party, 3)
        self.assertEqual(restaurant.max_party, 8)

    def test_bad_location(self):
        resp = self.client.get(self.bad_url)
        self.assertNotEqual(resp.status_code, 200)
        self.assertEqual(resp.status_code, 404)

    def test_bad_name(self):
        reverse_url = reverse(self.reverse_name, args=(self.bad_id,))
        self.assertEquals(reverse_url, self.bad_url)
