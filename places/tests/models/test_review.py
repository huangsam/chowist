from django.contrib.auth import get_user_model
from django.test import TestCase

from places.models import Restaurant, Review


class TestReview(TestCase):
    """Review test suite"""

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
        Review.objects.create(
            title="Amazing",
            body="This place is excellent",
            rating=5,
            place=restaurant,
            author=cls.user,
        )

    def test_review_all(self):
        reviews = Review.objects.all()
        self.assertEquals(len(reviews), 1)

    def test_review_get(self):
        review = Review.objects.get(title="Amazing")
        self.assertEquals(review.place.name, "Plutos")
        self.assertEquals(review.rating, 5)
        self.assertEquals(review.author, self.user)

    def test_review_filter(self):
        reviews = Review.objects.filter(rating=5)
        self.assertEquals(len(reviews), 1)

    def test_review_exception(self):
        self.assertRaises(Review.DoesNotExist, Review.objects.get, rating=0)
        self.assertRaises(Review.DoesNotExist, Review.objects.get, rating=6)

    def test_review_empty(self):
        reviews = Review.objects.filter(rating=0)
        self.assertEquals(len(reviews), 0)

    def test_restaurant_reviews(self):
        restaurant = Restaurant.objects.get(name="Plutos")
        review = restaurant.reviews.first()
        self.assertEquals(review.place.name, restaurant.name)
