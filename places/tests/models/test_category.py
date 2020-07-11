from django.test import TestCase

from places.models import Category, Restaurant


class TestRestaurant(TestCase):
    """Category test suite"""

    @classmethod
    def setUpTestData(cls):
        r1 = Restaurant.objects.create(
            name="Five Guys",
            address="Earth",
            latitude=0.00,
            longitude=0.00,
            min_party=1,
            max_party=6,
            yelp_link="/five-guys-earth",
        )
        r2 = Restaurant.objects.create(
            name="In N Out",
            address="Mars",
            latitude=0.00,
            longitude=0.00,
            min_party=1,
            max_party=4,
            yelp_link="/in-n-out-mars",
        )
        cls.burger_category = Category.objects.create(name="Burgers")
        cls.earthly_category = Category.objects.create(name="Earthly")
        cls.burger_category.places.add(r1, r2)
        cls.earthly_category.places.add(r1)

    def test_category_burger(self):
        burger_places = self.burger_category.places.all()
        self.assertEquals(len(burger_places), 2)

    def test_category_earthly(self):
        earthly_places = self.earthly_category.places.all()
        self.assertEquals(len(earthly_places), 1)
