from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from places.models import Restaurant


class HomeView(TemplateView):
    template_name = 'places/home.html'


class RestaurantListView(ListView):
    model = Restaurant
    context_object_name = 'restaurant_list'


class RestaurantDetailView(DetailView):
    model = Restaurant
    context_object_name = 'restaurant'


class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
    model = Restaurant
    fields = ['name', 'description', 'address', 'min_party', 'max_party', 'yelp_link']
    template_name_suffix = '_update'
