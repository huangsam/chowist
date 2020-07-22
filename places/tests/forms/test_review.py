from django.test import TestCase

from places.forms import ReviewForm


class TestReviewForm(TestCase):
    """ReviewForm test suite"""

    def test_review_form_invalid_with_empty(self):
        form = ReviewForm()
        self.assertFalse(form.is_valid())

    def test_review_form_invalid_with_partial(self):
        form_data = {"title": "Great restaurant"}
        form = ReviewForm(form_data)
        self.assertFalse(form.is_valid())

    def test_review_form_valid_with_full_fill(self):
        form_data = {
            "title": "Great restaurant",
            "body": "This restaurant is really good",
            "rating": 5,
        }
        form = ReviewForm(form_data)
        self.assertTrue(form.is_valid())
