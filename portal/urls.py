from django.urls import path
from django.contrib.auth import views as auth_views

from portal import views

# Insert your urls here.

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('register/', views.UserFormView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
