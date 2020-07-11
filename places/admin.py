from django.contrib import admin

from places.models import Category, Restaurant, Review

admin.site.register(Category)
admin.site.register(Restaurant)
admin.site.register(Review)
