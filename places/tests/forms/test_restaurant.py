from django.test import TestCase

from places.forms import RestaurantForm


class TestRestaurantForm(TestCase):
    """RestaurantForm test suite"""

    def test_restaurant_form_valid_with_empty(self):
        form_data = {"category": "", "name": ""}
        form = RestaurantForm(form_data)
        self.assertTrue(form.is_valid())

    def test_restaurant_form_valid_with_partial(self):
        form_data = {"category": "Burgers", "name": ""}
        form = RestaurantForm(form_data)
        self.assertTrue(form.is_valid())

    def test_restaurant_form_invalid_with_party(self):
        form_data = {
            "category": "",
            "name": "",
            "min_party": "Hello",
            "max_party": "World",
        }
        form = RestaurantForm(form_data)
        self.assertFalse(form.is_valid())

    def test_restaurant_form_valid_with_full_blank(self):
        form_data = {
            "category": "",
            "name": "",
            "min_party": None,
            "max_party": None,
        }
        form = RestaurantForm(form_data)
        self.assertTrue(form.is_valid())

    def test_restaurant_form_valid_with_full_fill(self):
        form_data = {
            "category": "Burgers",
            "name": "Five Guys",
            "min_party": 1,
            "max_party": 10,
        }
        form = RestaurantForm(form_data)
        self.assertTrue(form.is_valid())
