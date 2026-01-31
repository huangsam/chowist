from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from places.models import Restaurant, Review
from places.views import RestaurantListView

# Module-level constants
_CHICK_FIL_A = "Chick Fil A"
_VENUS = "Venus"


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
        self.assertEqual(reverse_url, self.desired_url)

    def test_desired_data(self):
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.context["restaurant_list"]), self.desired_restaurant_count)
        for restaurant in resp.context["restaurant_list"]:
            assert restaurant.name.startswith("Chipotle")
            assert restaurant.yelp_link.startswith("chipotle-bogus-")


class TestRestaurantDetailView(TestCase):
    """RestaurantDetailView test suite"""

    @classmethod
    def setUpTestData(cls):
        cls.restaurant = Restaurant.objects.create(
            name=_CHICK_FIL_A,
            address=_VENUS,
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
        self.assertIsInstance(restaurant, Restaurant)
        self.assertEqual(restaurant.name, _CHICK_FIL_A)
        self.assertEqual(restaurant.min_party, 3)
        self.assertEqual(restaurant.max_party, 8)


class TestRestaurantUpdateView(TestCase):
    """RestaurantUpdateView test suite"""

    UserModel = get_user_model()

    @classmethod
    def setUpTestData(cls):
        cls.restaurant = Restaurant.objects.create(
            name=_CHICK_FIL_A,
            address=_VENUS,
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
            name=_CHICK_FIL_A,
            address=_VENUS,
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


class TestRestaurantReviewView(TestCase):
    """RestaurantReviewView test suite"""

    UserModel = get_user_model()

    @classmethod
    def setUpTestData(cls):
        cls.restaurant = Restaurant.objects.create(
            name=_CHICK_FIL_A,
            address=_VENUS,
            latitude=0.00,
            longitude=0.00,
            min_party=3,
            max_party=8,
            yelp_link="chick-fil-a-venus",
        )
        cls.user = cls.UserModel.objects.create_user("john", "john@localhost", "john")

    def get_url(self, restaurant_id):
        return reverse("places:restaurant-review", args=[restaurant_id])

    def test_get_review_form_new_review(self):
        """Test GET request for new review form"""
        self.client.login(username="john", password="john")
        resp = self.client.get(self.get_url(self.restaurant.id))
        self.assertEqual(resp.status_code, 200)
        self.assertIn("form", resp.context)
        self.assertIn("restaurant", resp.context)
        self.assertEqual(resp.context["restaurant"], self.restaurant)

    def test_get_review_form_existing_review(self):
        """Test GET request when user already has a review"""
        self.client.login(username="john", password="john")
        # Create existing review
        Review.objects.create(place=self.restaurant, author=self.user, title="Great place", body="Really enjoyed it", rating=5)
        resp = self.client.get(self.get_url(self.restaurant.id))
        self.assertEqual(resp.status_code, 200)
        form = resp.context["form"]
        self.assertEqual(form.instance.title, "Great place")
        self.assertEqual(form.instance.rating, 5)

    def test_get_review_form_invalid_restaurant(self):
        """Test GET request with invalid restaurant ID"""
        self.client.login(username="john", password="john")
        resp = self.client.get(self.get_url(99999))
        self.assertEqual(resp.status_code, 404)

    def test_get_review_form_unauthenticated(self):
        """Test GET request without authentication"""
        resp = self.client.get(self.get_url(self.restaurant.id))
        self.assertEqual(resp.status_code, 302)  # Redirect to login

    def test_post_review_form_valid_new_review(self):
        """Test POST request creating new review"""
        self.client.login(username="john", password="john")
        form_data = {"title": "Amazing food", "body": "Best chicken sandwich ever", "rating": 5}
        resp = self.client.post(self.get_url(self.restaurant.id), form_data)
        self.assertEqual(resp.status_code, 302)
        # Check review was created
        review = Review.objects.get(place=self.restaurant, author=self.user)
        self.assertEqual(review.title, "Amazing food")
        self.assertEqual(review.rating, 5)

    def test_post_review_form_valid_update_review(self):
        """Test POST request updating existing review"""
        self.client.login(username="john", password="john")
        # Create existing review
        Review.objects.create(place=self.restaurant, author=self.user, title="Great place", body="Really enjoyed it", rating=4)
        form_data = {"title": "Amazing place", "body": "Even better than I thought", "rating": 5}
        resp = self.client.post(self.get_url(self.restaurant.id), form_data)
        self.assertEqual(resp.status_code, 302)
        # Check review was updated
        review = Review.objects.get(place=self.restaurant, author=self.user)
        self.assertEqual(review.title, "Amazing place")
        self.assertEqual(review.rating, 5)

    def test_post_review_form_invalid(self):
        """Test POST request with invalid form data"""
        self.client.login(username="john", password="john")
        form_data = {
            "title": "Hi",  # Too short
            "body": "Good",  # Too short
            "rating": 6,  # Invalid rating
        }
        resp = self.client.post(self.get_url(self.restaurant.id), form_data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("form", resp.context)
        self.assertFalse(resp.context["form"].is_valid())

    def test_post_review_form_invalid_restaurant(self):
        """Test POST request with invalid restaurant ID"""
        self.client.login(username="john", password="john")
        form_data = {"title": "Amazing food", "body": "Best chicken sandwich ever", "rating": 5}
        resp = self.client.post(self.get_url(99999), form_data)
        self.assertEqual(resp.status_code, 404)

    def test_post_review_form_unauthenticated(self):
        """Test POST request without authentication"""
        form_data = {"title": "Amazing food", "body": "Best chicken sandwich ever", "rating": 5}
        resp = self.client.post(self.get_url(self.restaurant.id), form_data)
        self.assertEqual(resp.status_code, 302)  # Redirect to login
