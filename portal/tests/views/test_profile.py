from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from portal.models import Profile


class TestProfileDetailView(TestCase):
    """ProfileDetailView test suite"""

    desired_url = "/profile/"
    desired_name = "portal:profile"

    UserModel = get_user_model()

    def setUp(self):
        self.UserModel.objects.create_user("john", "john@localhost", "john")

    def test_desired_location(self):
        self.client.login(username="john", password="john")
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_location_redirect(self):
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 302)

    def test_desired_name(self):
        reverse_url = reverse(self.desired_name)
        self.assertEqual(reverse_url, self.desired_url)


class TestProfileUpdateView(TestProfileDetailView):
    """ProfileUpdateView test suite"""

    desired_url = "/profile/update/"
    desired_name = "portal:profile-update"

    def test_post_valid_update(self):
        """Test successful profile update"""
        self.client.login(username="john", password="john")
        form_data = {"bio": "I love food!", "address": "123 Main St", "birth_date": "1990-01-01"}
        resp = self.client.post(self.desired_url, form_data)
        self.assertEqual(resp.status_code, 302)  # Redirect to profile
        # Check profile was updated
        user = get_user_model().objects.get(username="john")
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.bio, "I love food!")
        self.assertEqual(profile.address, "123 Main St")

    def test_post_invalid_update(self):
        """Test profile update with invalid data"""
        self.client.login(username="john", password="john")
        form_data = {
            "bio": "x" * 600,  # Too long
            "address": "Valid address",
            "birth_date": "2030-01-01",  # Future date
        }
        resp = self.client.post(self.desired_url, form_data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("form", resp.context)
        self.assertFalse(resp.context["form"].is_valid())


class TestProfileSignupView(TestCase):
    """ProfileSignupView test suite"""

    desired_url = "/signup/"
    desired_name = "portal:signup"

    def test_desired_location(self):
        resp = self.client.get(self.desired_url)
        self.assertEqual(resp.status_code, 200)

    def test_desired_name(self):
        reverse_url = reverse(self.desired_name)
        self.assertEqual(reverse_url, self.desired_url)

    def test_post_valid_signup(self):
        """Test successful user signup with profile creation"""
        form_data = {"username": "newuser", "email": "newuser@example.com", "password": "securepass123", "password_confirm": "securepass123"}
        resp = self.client.post(self.desired_url, form_data)
        self.assertEqual(resp.status_code, 302)  # Redirect to home
        # Check user was created
        UserModel = get_user_model()
        user = UserModel.objects.get(username="newuser")
        self.assertEqual(user.email, "newuser@example.com")
        # Check profile was created
        profile = Profile.objects.get(user=user)
        self.assertIsNotNone(profile)

    def test_post_invalid_signup(self):
        """Test signup with invalid data"""
        form_data = {"username": "newuser", "email": "invalid-email", "password": "weak", "password_confirm": "different"}
        resp = self.client.post(self.desired_url, form_data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("form", resp.context)
        self.assertFalse(resp.context["form"].is_valid())
