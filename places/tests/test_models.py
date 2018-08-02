from django.test import TestCase

from places.models import Restaurant, Rating


class TestRestaurant(TestCase):
    """Restaurant test suite"""

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

    def test_restaurants_all(self):
        restaurants = Restaurant.objects.all()
        self.assertEquals(len(restaurants), 2)

    def test_restaurant_get(self):
        restaurant_one = Restaurant.objects.get(name='Five Guys')
        restaurant_two = Restaurant.objects.get(name='In N Out')
        self.assertEquals(restaurant_one.max_party, 6)
        self.assertEquals(restaurant_two.max_party, 4)

    def test_restaurant_filter(self):
        restaurants = Restaurant.objects.filter(max_party__gt=5)
        self.assertNotEquals(restaurants, None)
        self.assertEquals(len(restaurants), 1)

    def test_restaurant_exception(self):
        self.assertRaises(Restaurant.DoesNotExist, Restaurant.objects.get, name='Bogus')

    def test_restaurant_empty(self):
        restaurants = Restaurant.objects.filter(max_party__gt=10)
        self.assertEquals(len(restaurants), 0)


class TestRating(TestCase):
    """Rating test suite"""

    ratings = [
        ('This place is excellent', 5),
        ('This place sucks', 1),
        ('You should check this place out', 5),
        ('This place is merely okay', 3),
    ]

    def setUp(self):
        restaurant = Restaurant.objects.create(
            name='Plutos', address='Jupiter',
            latitude=0.00, longitude=0.00,
            min_party=1, max_party=6,
            yelp_link='/plutos-jupiter')

        for snippet, stars in self.ratings:
            Rating.objects.create(
                snippet=snippet,
                stars=stars,
                place=restaurant,
                author=None
            )

    def test_rating_all(self):
        ratings = Rating.objects.all()
        self.assertEquals(len(ratings), len(self.ratings))

    def test_rating_get(self):
        rating = Rating.objects.get(snippet='This place is excellent')
        self.assertEquals(rating.place.name, 'Plutos')
        self.assertEquals(rating.stars, 5)
        self.assertEquals(rating.author, None)

    def test_rating_filter(self):
        ratings = Rating.objects.filter(stars=1)
        self.assertEquals(len(ratings), 1)

    def test_rating_exception(self):
        self.assertRaises(Rating.DoesNotExist, Rating.objects.get, stars=0)
        self.assertRaises(Rating.DoesNotExist, Rating.objects.get, stars=6)

    def test_rating_empty(self):
        ratings = Rating.objects.filter(stars=0)
        self.assertEquals(len(ratings), 0)

    def test_restaurant_ratings(self):
        restaurant = Restaurant.objects.get(name='Plutos')
        ratings = restaurant.ratings.all().prefetch_related('place')
        self.assertTrue(len(ratings) == len(self.ratings))
        for rating in ratings:
            self.assertEquals(rating.place.name, 'Plutos')
