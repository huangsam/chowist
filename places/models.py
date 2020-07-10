from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


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
        db_table = "restaurant"

    def get_absolute_url(self):
        return reverse("places:restaurant-detail", kwargs={"pk": self.pk})

    def __repr__(self):
        return f"<Restaurant id={self.id} name='{self.name}'>"

    def __str__(self):
        return f"Restaurant {self.name} located at {self.address}"


class Rating(models.Model):
    snippet = models.CharField(max_length=255)
    stars = models.IntegerField()
    place = models.ForeignKey("Restaurant", models.CASCADE, related_name="ratings")
    author = models.ForeignKey(get_user_model(), models.CASCADE, related_name="author")

    class Meta:
        db_table = "rating"
        unique_together = ["place", "author"]

    def __repr__(self):
        return f"<Rating id={self.id} stars={self.stars}>"

    def __str__(self):
        return f"Rating of {self.stars} stars for {self.place.name} by {self.author.username}"
