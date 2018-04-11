from django.contrib.auth import views as auth_views
from django.urls import path

from portal import views

# Insert your urls here.

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('signup/', views.UserFormView.as_view(), name='signup'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
