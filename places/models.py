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


class Rating(models.IntegerChoices):
    TERRIBLE = 1
    MEDIOCRE = 2
    AVERAGE = 3
    GOOD = 4
    GREAT = 5


class Review(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    rating = models.IntegerField(choices=Rating.choices)
    place = models.ForeignKey("Restaurant", models.CASCADE, related_name="reviews")
    author = models.ForeignKey(get_user_model(), models.CASCADE, related_name="reviews")

    class Meta:
        db_table = "review"
        unique_together = ["place", "author"]

    def __repr__(self):
        return f"<Review id={self.id} score={self.score}>"

    def __str__(self):
        return f"User {self.author.username} reviewed {self.place.name} with a rating of {self.rating}"
