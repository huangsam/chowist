from django.test import TestCase
from django.urls import reverse

from places.models import Restaurant

# Create your tests here.

class HomeViewTestCase(TestCase):
    """HomeView test suite"""

    desired_url = '/places/'
    desired_name = 'places:home'

    def test_desired_location(self):
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse(self.desired_name)
        self.assertEquals(reverse_url, self.desired_url)


class RestaurantListViewTestCase(TestCase):
    """RestaurantListView test suite"""

    desired_url = '/places/restaurants/'
    desired_name = 'places:restaurant-list'
    desired_restaurant_count = 25

    @classmethod
    def setUpTestData(cls):
        for i in range(cls.desired_restaurant_count):
            Restaurant.objects.create(
                name='Chipotle {rid}'.format(rid=i), address='Bogus {rid}'.format(rid=i),
                latitude=0.00, longitude=0.00,
                min_party=1, max_party=6,
                yelp_link='/chipotle-bogus-{rid}'.format(rid=i))

    def test_desired_location(self):
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse(self.desired_name)
        self.assertEquals(reverse_url, self.desired_url)

    def test_desired_data(self):
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context['restaurant_list']), self.desired_restaurant_count)


class RestaurantDetailViewTestCase(TestCase):
    """RestaurantDetailView test suite"""

    desired_name = 'places:restaurant-detail'
    desired_id = 1
    desired_url = '/places/restaurants/{rid}'.format(rid=desired_id)

    undesired_id = 2
    undesired_url = '/places/restaurants/{rid}'.format(rid=undesired_id)

    @classmethod
    def setUpTestData(cls):
        Restaurant.objects.create(
            name='Chick Fil A', address='Venus',
            latitude=0.00, longitude=0.00,
            min_party=3, max_party=8,
            yelp_link='/chick-fil-a-venus')

    def test_desired_location(self):
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse(self.desired_name, args=(self.desired_id,))
        self.assertEquals(reverse_url, self.desired_url)

    def test_desired_data(self):
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)
        restaurant = resp.context['restaurant']
        self.assertTrue(type(restaurant) == Restaurant)
        self.assertEqual(restaurant.name, 'Chick Fil A')
        self.assertEqual(restaurant.min_party, 3)
        self.assertEqual(restaurant.max_party, 8)

    def test_undesired_location(self):
        resp = self.client.get(self.undesired_url)
        self.assertNotEqual(resp.status_code, 200)
        self.assertEqual(resp.status_code, 404)

    def test_undesired_name(self):
        reverse_url = reverse(self.desired_name, args=(self.undesired_id,))
        self.assertEquals(reverse_url, self.undesired_url)
