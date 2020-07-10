from django.contrib.auth import get_user_model
from django.test import TestCase

from portal.models import Profile


class TestProfile(TestCase):
    """Profile test suite"""

    users = ["john", "jane"]

    UserModel = get_user_model()

    def setUp(self):
        for user in self.users:
            self.UserModel.objects.create_user(user, f"{user}@localhost", user)

    def test_profile_all(self):
        profiles = Profile.objects.all()
        self.assertEquals(len(profiles), len(self.users))

    def test_profile_get(self):
        user = self.UserModel.objects.get(username="john")
        profile = Profile.objects.get(user=user)
        self.assertIsNotNone(profile)
