from django.urls import path

from portal import views

app_name = "portal"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("signup/", views.ProfileSignupView.as_view(), name="signup"),
    path("profile/", views.ProfileDetailView.as_view(), name="profile"),
    path("profile/update/", views.ProfileUpdateView.as_view(), name="profile-update"),
]
