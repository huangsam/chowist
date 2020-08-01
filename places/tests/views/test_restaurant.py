from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from places.models import Restaurant
from places.views import RestaurantListView


class TestRestaurantListView(TestCase):
    """RestaurantListView test suite"""

    desired_url = "/places/restaurants/"
    desired_name = "places:restaurant-list"
    desired_restaurant_count = RestaurantListView.paginate_by

    @classmethod
    def setUpTestData(cls):
        for i in range(cls.desired_restaurant_count * 2):
            Restaurant.objects.create(
                name=f"Chipotle {i}",
                address=f"Bogus {i}",
                latitude=0.00,
                longitude=0.00,
                min_party=1,
                max_party=6,
                yelp_link=f"chipotle-bogus-{i}",
            )

    def test_desired_location(self):
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse(self.desired_name)
        self.assertEquals(reverse_url, self.desired_url)

    def test_desired_data(self):
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            len(resp.context["restaurant_list"]), self.desired_restaurant_count
        )
        for restaurant in resp.context["restaurant_list"]:
            assert restaurant.name.startswith("Chipotle")
            assert restaurant.yelp_link.startswith("chipotle-bogus-")


class TestRestaurantDetailView(TestCase):
    """RestaurantDetailView test suite"""

    @classmethod
    def setUpTestData(cls):
        cls.restaurant = Restaurant.objects.create(
            name="Chick Fil A",
            address="Venus",
            latitude=0.00,
            longitude=0.00,
            min_party=3,
            max_party=8,
            yelp_link="chick-fil-a-venus",
        )

    def get_url(self, restaurant_id):
        return reverse("places:restaurant-detail", args=[restaurant_id])

    def test_desired_location(self):
        resp = self.client.get(self.get_url(self.restaurant.id))
        self.assertEqual(resp.status_code, 200)

    def test_desired_data(self):
        resp = self.client.get(self.get_url(self.restaurant.id))
        self.assertEqual(resp.status_code, 200)
        restaurant = resp.context["restaurant"]
        self.assertTrue(type(restaurant) == Restaurant)
        self.assertEqual(restaurant.name, "Chick Fil A")
        self.assertEqual(restaurant.min_party, 3)
        self.assertEqual(restaurant.max_party, 8)


class TestRestaurantUpdateView(TestCase):
    """RestaurantUpdateView test suite"""

    UserModel = get_user_model()

    @classmethod
    def setUpTestData(cls):
        cls.restaurant = Restaurant.objects.create(
            name="Chick Fil A",
            address="Venus",
            latitude=0.00,
            longitude=0.00,
            min_party=3,
            max_party=8,
            yelp_link="chick-fil-a-venus",
        )
        cls.UserModel.objects.create_superuser("john", "john@localhost", "john")

    def get_url(self, restaurant_id):
        return reverse("places:restaurant-update", args=(restaurant_id,))

    def test_desired_location(self):
        self.client.login(username="john", password="john")
        resp = self.client.get(self.get_url(self.restaurant.id))
        self.assertEqual(resp.status_code, 200)


class TestRestaurantRandomView(TestCase):
    """RestaurantRandomView test suite"""

    UserModel = get_user_model()

    @classmethod
    def setUpTestData(cls):
        cls.restaurant = Restaurant.objects.create(
            name="Chick Fil A",
            address="Venus",
            latitude=0.00,
            longitude=0.00,
            min_party=3,
            max_party=8,
            yelp_link="chick-fil-a-venus",
        )

    def get_url(self):
        return reverse("places:restaurant-random")

    def test_desired_location(self):
        resp = self.client.get(self.get_url())
        self.assertEqual(resp.status_code, 302)
