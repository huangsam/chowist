from django.urls import path

from places import views

app_name = "places"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("restaurants/", views.RestaurantListView.as_view(), name="restaurant-list"),
    path(
        "restaurants/<int:pk>/",
        views.RestaurantDetailView.as_view(),
        name="restaurant-detail",
    ),
    path(
        "restaurants/<int:pk>/update/",
        views.RestaurantUpdateView.as_view(),
        name="restaurant-update",
    ),
    path(
        "restaurants/random/",
        views.RestaurantRandomView.as_view(),
        name="restaurant-random",
    ),
    path(
        "restaurants/<int:restaurant_id>/review/",
        views.RestaurantReviewView.as_view(),
        name="restaurant-review",
    ),
]
