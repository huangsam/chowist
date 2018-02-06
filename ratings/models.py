from django.db import models
from django.conf import settings

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, unique=True)
    latitude = models.DecimalField(max_digits=17, decimal_places=15)
    longitude = models.DecimalField(max_digits=18, decimal_places=15)
    min_party = models.IntegerField()
    max_party = models.IntegerField()
    yelp_link = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'restaurant'


class Rating(models.Model):
    snippet = models.CharField(max_length=255)
    stars = models.IntegerField()
    place = models.ForeignKey(
        'Restaurant',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
    )

    class Meta:
        db_table = 'rating'
