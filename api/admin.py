from django.contrib import admin

from api.models import Location
from api.models import Category
from api.models import Restaurant
from api.models import Rating


admin.site.register(Location)
admin.site.register(Category)
admin.site.register(Restaurant)
admin.site.register(Rating)
