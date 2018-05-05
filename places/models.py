from django.conf import settings
from django.db import models


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

    def __str__(self):
        return '{id}: {name} @ {address}'.format(
            id=self.id, name=self.name, address=self.address)


class Rating(models.Model):
    snippet = models.CharField(max_length=255)
    stars = models.IntegerField()
    place = models.ForeignKey(
        'Restaurant',
        on_delete=models.CASCADE,
        related_name='ratings',
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        related_name='author',
    )

    class Meta:
        db_table = 'rating'

    def __str__(self):
        return '{id}: {address} w/ {stars} stars'.format(
            id=self.id, address=self.place.yelp_link, stars=self.stars)
