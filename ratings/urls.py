from django.urls import path

from ratings import views

urlpatterns = [
    path('', views.home)
]