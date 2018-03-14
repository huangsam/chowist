import json
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from places.models import Restaurant, Rating


class Command(BaseCommand):
    help = 'Loads sample data for application'

    def add_arguments(self, parser):
        parser.add_argument('data_path', type=str)

    def handle(self, *args, **options):
        data_path = options['data_path']
        if os.path.exists(data_path) is False:
            raise CommandError('{path} does not exist'.format(path=data_path))
        with open(data_path) as f:
            places = json.loads(f.read())
        for place in places:
            restaurant = Restaurant(
                name=place['name'],
                address=place['address'],
                latitude=place['lat'],
                longitude=place['long'],
                min_party=place['minparty'],
                max_party=place['maxparty'],
                yelp_link=place['yelp'],
            )
            restaurant.save()
            rating = Rating(
                stars=int(place['rating']),
                snippet=place['snippet_text'],
                place=restaurant,
            )
            rating.save()
