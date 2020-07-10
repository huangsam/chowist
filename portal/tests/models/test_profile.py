from django.contrib.auth.models import User
from django.test import TestCase

from portal.models import Profile


class TestProfile(TestCase):
    """Profile test suite"""

    users = ["john", "jane"]

    def setUp(self):
        for user in self.users:
            User.objects.create_user(user, f"{user}@localhost", user)

    def test_profile_all(self):
        profiles = Profile.objects.all()
        self.assertEquals(len(profiles), len(self.users))

    def test_profile_get(self):
        user = User.objects.get(username="john")
        profile = Profile.objects.get(user=user)
        self.assertIsNotNone(profile)
