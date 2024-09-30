from django.test import TestCase

from places.models import Restaurant

_FIVE_GUYS = "Five Guys"
_IN_N_OUT = "In N Out"


class TestRestaurant(TestCase):
    """Restaurant test suite"""

    def setUp(self):
        Restaurant.objects.create(
            name=_FIVE_GUYS,
            address="Earth",
            latitude=0.00,
            longitude=0.00,
            min_party=1,
            max_party=6,
            yelp_link="/five-guys-earth",
        )
        Restaurant.objects.create(
            name=_IN_N_OUT,
            address="Mars",
            latitude=2.00,
            longitude=2.00,
            min_party=1,
            max_party=4,
            yelp_link="/in-n-out-mars",
        )

    def test_restaurants_all(self):
        restaurants = Restaurant.objects.all()
        self.assertEqual(len(restaurants), 2)

    def test_restaurant_get(self):
        restaurant = Restaurant.objects.get(name=_FIVE_GUYS)
        self.assertEqual(restaurant.min_party, 1)
        self.assertEqual(restaurant.max_party, 6)

    def test_restaurant_filter(self):
        restaurants = Restaurant.objects.filter(max_party__gt=5)
        self.assertNotEqual(restaurants, None)
        self.assertEqual(len(restaurants), 1)

    def test_restaurant_missing(self):
        self.assertRaises(Restaurant.DoesNotExist, Restaurant.objects.get, name="Bogus")

    def test_restaurant_empty(self):
        restaurants = Restaurant.objects.filter(max_party__gt=10)
        self.assertEqual(len(restaurants), 0)

    def test_restaurant_distance(self):
        five_guys = Restaurant.objects.get(name=_FIVE_GUYS)
        in_n_out = Restaurant.objects.get(name=_IN_N_OUT)
        dist_one = five_guys.get_distance_to(in_n_out)
        dist_two = in_n_out.get_distance_to(five_guys)
        self.assertEqual(dist_one, dist_two)
