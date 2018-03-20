from django.urls import path

from portal import views

# Insert your urls here.

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.UserFormView.as_view(), name='register'),
]
