import json
from argparse import FileType
from collections import defaultdict

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from places.models import Category, Restaurant, Review


class Command(BaseCommand):
    help = "Load data for .demo purposes"
    UserModel = get_user_model()
    admin_user = "admin"
    normal_users = ["john", "jane"]

    def add_arguments(self, parser):
        parser.add_argument("places", help="JSON artifact", type=FileType("r"))

    @staticmethod
    def get_user_options(user):
        return {"username": user, "email": f"{user}@localhost", "password": user}

    def handle(self, *args, **options):
        self.stdout.write("Delete existing data")
        self.UserModel.objects.all().delete()
        Category.objects.all().delete()
        Review.objects.all().delete()
        Restaurant.objects.all().delete()

        self.stdout.write("Create users")
        admin_options = self.get_user_options(self.admin_user)
        self.UserModel.objects.create_superuser(**admin_options)
        for normal_user in self.normal_users:
            normal_options = self.get_user_options(normal_user)
            self.UserModel.objects.create_user(**normal_options)

        self.stdout.write("Create restaurants")
        content = json.load(options["places"])
        categories_for_restaurants = defaultdict(list)
        for item in content:
            restaurant = Restaurant.objects.create(
                name=item["name"],
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
            Review.objects.create(
                title="Great place",
                body="Great food, great service",
                rating=5,
                place=restaurant,
                author=first_normal,
            )
            Review.objects.create(
                title="Worst place",
                body="Worst food, worst service",
                rating=1,
                place=restaurant,
                author=last_normal,
            )

        self.stdout.write(self.style.SUCCESS("Success"))
