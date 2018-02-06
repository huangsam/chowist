from django.db import models

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=17, decimal_places=15)
    longitude = models.DecimalField(max_digits=18, decimal_places=15)
    min_party = models.IntegerField()
    max_party = models.IntegerField()
    yelp_link = models.CharField(max_length=255)
    notes = models.CharField(max_length=255)

    class Meta:
        db_table = 'restaurant'


class Rating(models.Model):
    snippet = models.CharField(max_length=255)
    stars = models.IntegerField()
    place = models.ForeignKey(
        'Restaurant',
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'rating'
