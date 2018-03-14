from django.urls import path

from places import views

# Insert your urls here.

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('restaurants/', views.RestaurantListView.as_view(), name='restaurant_list'),
]