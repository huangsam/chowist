from django.test import TestCase
from places.models import Restaurant

# Create your tests here.

class RestaurantTestCase(TestCase):
    def setUp(self):
        Restaurant.objects.create(
            name='Five Guys', address='Earth',
            latitude=0.00, longitude=0.00,
            min_party=1, max_party=6,
            yelp_link='/five-guys-earth')
        Restaurant.objects.create(
            name='In N Out', address='Mars',
            latitude=0.00, longitude=0.00,
            min_party=1, max_party=4,
            yelp_link='/in-n-out-mars')

    def test_restaurant_retrieval(self):
        restaurant_one = Restaurant.objects.get(name='Five Guys')
        restaurant_two = Restaurant.objects.get(name='In N Out')
        self.assertEquals(restaurant_one.max_party, 6)
        self.assertEquals(restaurant_two.max_party, 4)

    def test_restaurant_greater_than_five(self):
        restaurants = Restaurant.objects.filter(max_party__gt=5)
        self.assertNotEquals(restaurants, None)
        self.assertEquals(len(restaurants), 1)

    def test_no_restaurants(self):
        self.assertRaises(Restaurant.DoesNotExist, Restaurant.objects.get, name='Bogus')
