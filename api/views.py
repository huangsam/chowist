from rest_framework import generics

from api.models import Location
from api.models import Category
from api.models import Restaurant
from api.models import Rating
from api.serializers import LocationSerializer
from api.serializers import CategorySerializer
from api.serializers import RestaurantSerializer
from api.serializers import RatingSerializer


class LocationList(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RestaurantList(generics.ListCreateAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class RatingList(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
