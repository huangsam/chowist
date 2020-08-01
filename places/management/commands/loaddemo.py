import json
import random
from argparse import FileType
from collections import defaultdict

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db.models import Q

from places.models import Category, Rating, Restaurant, Review


class Command(BaseCommand):
    help = "Load demo data for places app"
    UserModel = get_user_model()
    admin_user = "admin"
    normal_users = ["john", "jane"]

    def add_arguments(self, parser):
        parser.add_argument("places", help="JSON artifact", type=FileType("r"))

    @staticmethod
    def get_user_options(user):
        return {"username": user, "email": f"{user}@localhost", "password": user}

    @staticmethod
    def create_review(restaurant, reviewer):
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

    def handle(self, *args, **options):
        self.stdout.write("Delete existing data")
        self.UserModel.objects.all().delete()
        Category.objects.all().delete()
        Review.objects.all().delete()
        Restaurant.objects.all().delete()
        Group.objects.all().delete()

        self.stdout.write("Create reviewers group")
        reviewers = Group.objects.create(name="reviewers")
        is_places = Q(content_type__app_label__exact="places")
        is_portal = Q(content_type__app_label__exact="portal")
        is_valid_app = is_places | is_portal
        is_change = Q(codename__contains="change")
        is_valid_change = is_change & ~Q(codename__contains="restaurant")
        permissions = Permission.objects.filter(is_valid_app & is_valid_change)
        reviewers.permissions.set(permissions)
        add_review = Permission.objects.get(codename__exact="add_review")
        reviewers.permissions.add(add_review)

        self.stdout.write("Create users")
        admin_options = self.get_user_options(self.admin_user)
        self.UserModel.objects.create_superuser(**admin_options)
        for normal_user in self.normal_users:
            normal_options = self.get_user_options(normal_user)
            user = self.UserModel.objects.create_user(**normal_options)
            reviewers.user_set.add(user)

        self.stdout.write("Create restaurants")
        content = json.load(options["places"])
        categories_for_restaurants = defaultdict(list)
        for item in content:
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
            for category_name in item["categories"]:
                categories_for_restaurants[category_name].append(restaurant)

        self.stdout.write("Create categories")
        for category_name, restaurants in categories_for_restaurants.items():
            category = Category.objects.create(name=category_name)
            category.places.add(*restaurants)

        self.stdout.write("Create reviews")
        first_normal = self.UserModel.objects.get(username=self.normal_users[0])
        last_normal = self.UserModel.objects.get(username=self.normal_users[-1])
        for restaurant in Restaurant.objects.all():
            self.create_review(restaurant, first_normal)
            self.create_review(restaurant, last_normal)

        self.stdout.write(self.style.SUCCESS("Success"))
