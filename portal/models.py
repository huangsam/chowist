from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(max_length=500, blank=True)
    address = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(null=True)

    class Meta:
        db_table = "profile"

    def __repr__(self):
        return f"<Profile id={self.id} username='{self.user.username}'>"

    def __str__(self):
        return f"Profile for user {self.user.username} w/ email: {self.user.email or 'N/A'}"


@receiver(post_save, sender=get_user_model())
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
