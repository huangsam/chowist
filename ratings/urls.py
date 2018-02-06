from django.urls import path

from ratings import views

# Insert your urls here.

urlpatterns = [
    path('', views.home, name='home')
]
