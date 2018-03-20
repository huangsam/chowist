from django.urls import path
from django.contrib.auth import views as auth_views

from portal import views

# Insert your urls here.

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout, name='logout'),
    path('register/', views.UserFormView.as_view(), name='register'),
]
