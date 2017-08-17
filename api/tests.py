from django.test import TestCase

from api.models import Location
from api.models import Category
from api.models import Restaurant
from api.models import Rating


class LocationTestCase(TestCase):
    def setUp(self):
        Location.objects.create()

    def test_location_get(self):
        location = Location.objects.get(pk=1)
        assert type(location) is Location


class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create()

    def test_category_get(self):
        category = Category.objects.get(pk=1)
        assert type(category) is Category


class RestaurantTestCase(TestCase):
    def setUp(self):
        Restaurant.objects.create()

    def test_restaurant_get(self):
        restaurant = Restaurant.objects.get(pk=1)
        assert type(restaurant) is Restaurant


class RatingTestCase(TestCase):
    def setUp(self):
        Rating.objects.create()

    def test_rating_get(self):
        rating = Rating.objects.get(pk=1)
        assert type(rating) is Rating
