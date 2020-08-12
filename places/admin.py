from django.contrib import admin

from places.models import Category, Restaurant, Review


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ["name", "address", "description"]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ["rating", "author", "place"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Review, ReviewAdmin)
