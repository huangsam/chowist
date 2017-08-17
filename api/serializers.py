from rest_framework import serializers

from api.models import Location
from api.models import Category
from api.models import Restaurant
from api.models import Rating


class LocationSerializer(serializers.Serializer):
    class Meta:
        model = Location
        fields = ('id',)


class CategorySerializer(serializers.Serializer):
    class Meta:
        model = Category
        fields = ('id',)


class RestaurantSerializer(serializers.Serializer):
    class Meta:
        model = Restaurant
        fields = ('id',)


class RatingSerializer(serializers.Serializer):
    class Meta:
        model = Rating
        fields = ('id',)
