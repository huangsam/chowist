from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    address = models.CharField(max_length=255, blank=True)
    birth_date = models.DateField(null=True)

    class Meta:
        db_table = "profile"

    def __repr__(self):
        return f"<Profile id={self.id} username={self.user.username}>"

    def __str__(self):
        return f"Profile for user {self.user.username} w/ email: {self.user.email or 'N/A'}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
