from django.urls import path

from portal import views

# Insert your urls here.

urlpatterns = [
    path('', views.home, name='home')
]
