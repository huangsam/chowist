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

    def test_category_all(self):
        self.assertEqual(len(Category.objects.all()), 2)

    def test_category_get(self):
        category = Category.objects.get(name="Burgers")
        self.assertEqual(self.burger_category, category)

    def test_category_missing(self):
        self.assertRaises(Category.DoesNotExist, Category.objects.get, name="Bogus")

    def test_category_burger(self):
        burger_places = self.burger_category.places.all()
        self.assertEqual(len(burger_places), 2)

    def test_category_earthly(self):
        earthly_places = self.earthly_category.places.all()
        self.assertEqual(len(earthly_places), 1)

    def test_restaurant_five_guys(self):
        five_guys = Restaurant.objects.get(name="Five Guys")
        self.assertEqual(len(five_guys.categories.all()), 2)

    def test_restaurant_in_n_out(self):
        in_n_out = Restaurant.objects.get(name="In N Out")
        self.assertEqual(len(in_n_out.categories.all()), 1)
