from django.contrib.auth import get_user_model
from django.test import TestCase

from places.models import Restaurant, Rating


class TestRating(TestCase):
    """Rating test suite"""

    UserModel = get_user_model()

    @classmethod
    def setUpTestData(cls):
        restaurant = Restaurant.objects.create(
            name="Plutos",
            address="Jupiter",
            latitude=0.00,
            longitude=0.00,
            min_party=1,
            max_party=6,
            yelp_link="/plutos-jupiter",
        )

        cls.user = cls.UserModel.objects.create_user("john", "john@localhost", "john")
        Rating.objects.create(snippet="This place is excellent", stars=5, place=restaurant, author=cls.user)

    def test_rating_all(self):
        ratings = Rating.objects.all()
        self.assertEquals(len(ratings), 1)

    def test_rating_get(self):
        rating = Rating.objects.get(snippet="This place is excellent")
        self.assertEquals(rating.place.name, "Plutos")
        self.assertEquals(rating.stars, 5)
        self.assertEquals(rating.author, self.user)

    def test_rating_filter(self):
        ratings = Rating.objects.filter(stars=5)
        self.assertEquals(len(ratings), 1)

    def test_rating_exception(self):
        self.assertRaises(Rating.DoesNotExist, Rating.objects.get, stars=0)
        self.assertRaises(Rating.DoesNotExist, Rating.objects.get, stars=6)

    def test_rating_empty(self):
        ratings = Rating.objects.filter(stars=0)
        self.assertEquals(len(ratings), 0)

    def test_restaurant_ratings(self):
        restaurant = Restaurant.objects.get(name="Plutos")
        rating = restaurant.ratings.first()
        self.assertEquals(rating.place.name, "Plutos")
