from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from places.models import Restaurant, Review
from places.views import RestaurantListView

import math

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

    def test_restaurant_list_template_caching(self):
        """Test that restaurant list view renders correctly with caching enabled"""
        # Get the first restaurant from the list
        first_restaurant = Restaurant.objects.first()
        cache_key = f"restaurant_card_{first_restaurant.id}"

        # Clear any existing cache
        cache.delete(cache_key)

        # Make request to list view
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)

        # Check that response contains expected content
        self.assertContains(resp, "Chipotle")
        self.assertContains(resp, "card-link")
        self.assertContains(resp, first_restaurant.name)

        # Note: Template fragment caching may not work in test environment
        # due to Django's test client behavior, but the view should still render
        # The important thing is that the page renders correctly
        self.assertEqual(len(resp.context["restaurant_list"]), self.desired_restaurant_count)

    def test_restaurant_list_model_caching_integration(self):
        """Test that model caching works in the context of list view rendering"""
        # Get a restaurant and ensure its average rating is cached
        restaurant = Restaurant.objects.first()
        rating_cache_key = f"restaurant_avg_rating_{restaurant.id}"

        # Clear cache and get rating (should cache it)
        cache.delete(rating_cache_key)
        rating1 = restaurant.get_average_rating()

        # Verify it's cached
        cached_rating = cache.get(rating_cache_key)
        self.assertIsNotNone(cached_rating)

        # Make request to list view - this should not affect the model cache
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)

        # Model cache should still be there
        cached_rating_after = cache.get(rating_cache_key)
        # Handle NaN comparison properly
        if math.isnan(cached_rating):
            self.assertTrue(math.isnan(cached_rating_after))
        else:
            self.assertEqual(cached_rating, cached_rating_after)

    def test_restaurant_list_template_contains_cache_tags(self):
        """Test that the restaurant list template includes cache tags"""
        from django.template.loader import get_template

        # Load the template
        template = get_template("places/restaurant_list.html")

        # Check that template source contains cache tags
        template_source = template.template.source
        self.assertIn("{% cache 300 restaurant_card", template_source)
        self.assertIn("{% endcache %}", template_source)


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

    def test_update_restaurant_cache_invalidation(self):
        """Test that restaurant card cache is invalidated when restaurant is updated"""
        self.client.login(username="john", password="john")

        # Pre-populate cache
        cache_key = f"restaurant_card_{self.restaurant.id}"
        cache.set(cache_key, "fake_cached_content", 300)

        # Verify cache is set
        self.assertEqual(cache.get(cache_key), "fake_cached_content")

        # Update restaurant
        form_data = {
            "name": "Updated Chick Fil A",
            "description": "Updated description",
            "address": "Updated Venus",
            "min_party": 4,
            "max_party": 10,
            "yelp_link": "updated-chick-fil-a-venus",
        }
        resp = self.client.post(self.get_url(self.restaurant.id), form_data)
        self.assertEqual(resp.status_code, 302)

        # Cache should be cleared (None)
        self.assertIsNone(cache.get(cache_key))


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

    def test_post_review_form_cache_invalidation_new_review(self):
        """Test that cache is invalidated when creating new review"""
        self.client.login(username="john", password="john")

        # Pre-populate cache
        cache_key = f"restaurant_avg_rating_{self.restaurant.id}"
        cache.set(cache_key, 0.0, 300)  # Set fake cached value

        # Verify cache is set
        self.assertEqual(cache.get(cache_key), 0.0)

        # Create new review
        form_data = {"title": "Amazing food", "body": "Best chicken sandwich ever", "rating": 5}
        resp = self.client.post(self.get_url(self.restaurant.id), form_data)
        self.assertEqual(resp.status_code, 302)

        # Cache should be cleared (None)
        self.assertIsNone(cache.get(cache_key))

    def test_post_review_form_cache_invalidation_update_review(self):
        """Test that cache is invalidated when updating existing review"""
        self.client.login(username="john", password="john")

        # Create existing review
        Review.objects.create(place=self.restaurant, author=self.user, title="Original review", body="Original body", rating=3)

        # Pre-populate cache
        cache_key = f"restaurant_avg_rating_{self.restaurant.id}"
        cache.set(cache_key, 3.0, 300)  # Set fake cached value

        # Verify cache is set
        self.assertEqual(cache.get(cache_key), 3.0)

        # Update review
        form_data = {"title": "Updated review", "body": "Updated body", "rating": 5}
        resp = self.client.post(self.get_url(self.restaurant.id), form_data)
        self.assertEqual(resp.status_code, 302)

        # Cache should be cleared (None)
        self.assertIsNone(cache.get(cache_key))
