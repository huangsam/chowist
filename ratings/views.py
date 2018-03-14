from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from ratings.models import Restaurant

# Create your views here.

class HomeView(TemplateView):
    template_name = 'ratings/home.html'


class RestaurantListView(ListView):
    model = Restaurant
