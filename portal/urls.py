from django.urls import path
from django.contrib.auth import views as auth_views

from portal import views

# Insert your urls here.

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(success_url='done'), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('signup/', views.UserFormView.as_view(), name='signup'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
