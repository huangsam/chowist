from django.contrib import admin

from portal.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["username", "email_address", "birth_date"]

    @staticmethod
    def username(obj):
        return obj.user.username

    @staticmethod
    def email_address(obj):
        return obj.user.email


admin.site.register(Profile, ProfileAdmin)
