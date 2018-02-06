from django.contrib import admin

from ratings.models import Restaurant, Rating

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(Rating)
