import math

from django.contrib.auth import get_user_model
from django.test import TestCase

from places.models import Restaurant, Review


class TestReview(TestCase):
    """Review test suite"""

    UserModel = get_user_model()

    @classmethod
    def setUpTestData(cls):
        place_with_reviews = Restaurant.objects.create(
            name="Plutos",
            address="Jupiter",
            latitude=0.00,
            longitude=0.00,
            min_party=1,
            max_party=6,
            yelp_link="/plutos-jupiter",
        )

        cls.user = cls.UserModel.objects.create_user("john", "john@localhost", "john")
        Review.objects.create(
            title="Amazing",
            body="This place is excellent",
            rating=5,
            place=place_with_reviews,
            author=cls.user,
        )

        Restaurant.objects.create(
            name="Nowhere",
            address="Mars",
            latitude=0.00,
            longitude=0.00,
            min_party=1,
            max_party=1,
            yelp_link="/nowhere-mars",
        )

    def test_review_all(self):
        reviews = Review.objects.all()
        self.assertEqual(len(reviews), 1)

    def test_review_get(self):
        review = Review.objects.get(title="Amazing")
        self.assertEqual(review.place.name, "Plutos")
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.author, self.user)

    def test_review_filter(self):
        reviews = Review.objects.filter(rating=5)
        self.assertEqual(len(reviews), 1)

    def test_review_missing(self):
        self.assertRaises(Review.DoesNotExist, Review.objects.get, rating=0)

    def test_review_empty(self):
        reviews = Review.objects.filter(rating=0)
        self.assertEqual(len(reviews), 0)

    def test_restaurant_reviews(self):
        restaurant = Restaurant.objects.get(name="Plutos")
        review = restaurant.reviews.first()
        self.assertEqual(review.place.name, restaurant.name)

    def test_restaurant_rating_with_reviews(self):
        restaurant = Restaurant.objects.get(name="Plutos")
        self.assertEqual(restaurant.get_average_rating(), 5.0)

    def test_restaurant_rating_without_reviews(self):
        restaurant = Restaurant.objects.get(name="Nowhere")
        self.assertTrue(math.isnan(restaurant.get_average_rating()))
