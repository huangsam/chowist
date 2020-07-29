from django.test import TestCase

from places.models import Restaurant


class TestRestaurant(TestCase):
    """Restaurant test suite"""

    def setUp(self):
        Restaurant.objects.create(
            name="Five Guys",
            address="Earth",
            latitude=0.00,
            longitude=0.00,
            min_party=1,
            max_party=6,
            yelp_link="/five-guys-earth",
        )
        Restaurant.objects.create(
            name="In N Out",
            address="Mars",
            latitude=2.00,
            longitude=2.00,
            min_party=1,
            max_party=4,
            yelp_link="/in-n-out-mars",
        )

    def test_restaurants_all(self):
        restaurants = Restaurant.objects.all()
        self.assertEquals(len(restaurants), 2)

    def test_restaurant_get(self):
        restaurant = Restaurant.objects.get(name="Five Guys")
        self.assertEquals(restaurant.min_party, 1)
        self.assertEquals(restaurant.max_party, 6)

    def test_restaurant_filter(self):
        restaurants = Restaurant.objects.filter(max_party__gt=5)
        self.assertNotEquals(restaurants, None)
        self.assertEquals(len(restaurants), 1)

    def test_restaurant_missing(self):
        self.assertRaises(Restaurant.DoesNotExist, Restaurant.objects.get, name="Bogus")

    def test_restaurant_empty(self):
        restaurants = Restaurant.objects.filter(max_party__gt=10)
        self.assertEquals(len(restaurants), 0)

    def test_restaurant_distance(self):
        five_guys = Restaurant.objects.get(name="Five Guys")
        in_n_out = Restaurant.objects.get(name="In N Out")
        dist_one = five_guys.get_distance_to(in_n_out)
        dist_two = in_n_out.get_distance_to(five_guys)
        self.assertEquals(dist_one, dist_two)
