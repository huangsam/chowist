import math

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import models
from django.db.models import Avg
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
        ordering = ["name"]

    def get_average_rating(self) -> float:
        cache_key = f"restaurant_avg_rating_{self.id}"
        rating = cache.get(cache_key)
        if rating is None:
            result = self.reviews.aggregate(avg_rating=Avg("rating"))
            rating = result["avg_rating"] if result["avg_rating"] is not None else math.nan
            cache.set(cache_key, rating, 300)  # Cache for 5 minutes
        return rating

    def get_distance_to(self, other: "Restaurant") -> float:
        y_diff = self.latitude - other.latitude
        x_diff = self.longitude - other.longitude
        return math.sqrt(y_diff**2 + x_diff**2)

    def get_absolute_url(self) -> str:
        return reverse("places:restaurant-detail", kwargs={"pk": self.pk})

    def __repr__(self) -> str:
        return f"<Restaurant id={self.id} name='{self.name}'>"

    def __str__(self) -> str:
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
    place = models.ForeignKey(Restaurant, models.CASCADE, related_name="reviews")
    author = models.ForeignKey(get_user_model(), models.CASCADE, related_name="reviews")

    class Meta:
        db_table = "review"
        unique_together = ["place", "author"]
        ordering = ["rating"]

    def __repr__(self) -> str:
        return f"<Review id={self.id} rating={self.rating}>"

    def __str__(self) -> str:
        return f"User {self.author.username} reviewed {self.place.name} with a rating of {self.rating}"


class Category(models.Model):
    name = models.CharField(max_length=255)
    places = models.ManyToManyField(Restaurant, related_name="categories")

    class Meta:
        db_table = "category"
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __repr__(self) -> str:
        return f"<Category id={self.id} name='{self.name}'>"

    def __str__(self) -> str:
        return f"Category with the name of {self.name}"
