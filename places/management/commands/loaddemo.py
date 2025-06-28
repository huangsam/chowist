import json
import random
from argparse import FileType
from collections import defaultdict

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.db.transaction import atomic

from places.models import Category, Rating, Restaurant, Review


class DemoBuilder:
    def __init__(self, stdout, style, places_json_file):
        self.stdout = stdout
        self.style = style
        self.places_json_file = places_json_file
        self.UserModel = get_user_model()
        self.admin_user = "admin"
        self.normal_users = ["john", "jane"]
        self.reviewers_group = None
        self.restaurants_data = None
        self.created_restaurants = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.stdout.write(self.style.ERROR(f"An error occurred: {exc_val}"))
        else:
            self.stdout.write(self.style.SUCCESS("Demo data loaded successfully!"))

    @staticmethod
    def _get_user_options(user):
        return {"username": user, "email": f"{user}@localhost", "password": user}

    @staticmethod
    def _create_review_for_restaurant(restaurant, reviewer):
        rating = random.randint(1, 5)
        rating_name = Rating(rating).name
        rating_title = f"{rating_name.title()} place"
        rating_body = f"{rating_name.title()} food, {rating_name.lower()} service."
        Review.objects.create(
            title=rating_title,
            body=rating_body,
            rating=rating,
            place=restaurant,
            author=reviewer,
        )

    @atomic
    def with_clean_data(self):
        self.stdout.write("Deleting existing data...")
        self.UserModel.objects.all().delete()
        Category.objects.all().delete()
        Review.objects.all().delete()
        Restaurant.objects.all().delete()
        Group.objects.all().delete()
        return self

    @atomic
    def with_reviewers_group(self):
        self.stdout.write("Create reviewers group")
        is_places = Q(content_type__app_label__exact="places")
        is_portal = Q(content_type__app_label__exact="portal")
        is_valid_app = is_places | is_portal
        is_change = Q(codename__contains="change")
        is_not_restaurant_change = is_change & ~Q(codename__contains="restaurant")
        is_add_review = Q(codename__exact="add_review")
        is_valid_change = is_valid_app & is_not_restaurant_change
        is_valid_add = is_places & is_add_review
        valid_permissions = Permission.objects.filter(is_valid_change | is_valid_add)
        self.reviewers_group = Group.objects.create(name="reviewers")
        self.reviewers_group.permissions.set(valid_permissions)
        return self

    @atomic
    def with_users(self):
        if not self.reviewers_group:
            raise ValueError("Reviewers group must be created before adding users.")

        self.stdout.write("Create users")
        admin_options = self._get_user_options(self.admin_user)
        self.UserModel.objects.create_superuser(**admin_options)
        for normal_user_name in self.normal_users:
            normal_options = self._get_user_options(normal_user_name)
            user = self.UserModel.objects.create_user(**normal_options)
            if self.reviewers_group:
                self.reviewers_group.user_set.add(user)
        return self

    @atomic
    def with_restaurants(self):
        self.stdout.write("Create restaurants")
        self.restaurants_data = json.load(self.places_json_file)
        for item in self.restaurants_data:
            restaurant = Restaurant.objects.create(
                name=item["name"],
                description=item["description"],
                address=item["address"],
                latitude=item["lat"],
                longitude=item["long"],
                min_party=item["minparty"],
                max_party=item["maxparty"],
                yelp_link=item["yelp"],
            )
            self.created_restaurants.append(restaurant)
        return self

    @atomic
    def with_categories(self):
        if not self.created_restaurants:
            raise ValueError("Restaurants must be created before adding categories.")

        self.stdout.write("Create categories")
        categories_for_restaurants = defaultdict(list)
        for item in self.restaurants_data:
            # We need to map the JSON items back to the created Restaurant objects
            # Assuming names are unique for simplicity here. In a real app,
            # you might store a mapping or retrieve by name/pk.
            restaurant = next((r for r in self.created_restaurants if r.name == item["name"]), None)
            if restaurant:
                for category_name in item["categories"]:
                    categories_for_restaurants[category_name].append(restaurant)

        for category_name, restaurants in categories_for_restaurants.items():
            category, _ = Category.objects.get_or_create(name=category_name)
            category.places.add(*restaurants)
        return self

    @atomic
    def with_reviews(self):
        if not self.created_restaurants:
            raise ValueError("Restaurants must be created before adding reviews.")
        if not self.normal_users:
            raise ValueError("Normal users must be created before adding reviews.")

        self.stdout.write("Creating reviews...")
        first_normal = self.UserModel.objects.get(username=self.normal_users[0])
        last_normal = self.UserModel.objects.get(username=self.normal_users[-1])

        for restaurant in self.created_restaurants:
            self._create_review_for_restaurant(restaurant, first_normal)
            self._create_review_for_restaurant(restaurant, last_normal)
        return self


class Command(BaseCommand):
    help = "Load demo data for places app"

    def add_arguments(self, parser):
        parser.add_argument("places", help="JSON artifact", type=FileType("r"))

    def handle(self, *args, **options):
        with DemoBuilder(self.stdout, self.style, options["places"]) as builder:
            builder = builder.with_clean_data()
            builder = builder.with_reviewers_group().with_users()
            builder = builder.with_restaurants().with_categories().with_reviews()
