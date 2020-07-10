from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from places.models import Restaurant


class HomeView(TemplateView):
    template_name = "places/home.html"


class RestaurantListView(ListView):
    model = Restaurant
    context_object_name = "restaurant_list"


class RestaurantDetailView(DetailView):
    model = Restaurant
    context_object_name = "restaurant"


class RestaurantUpdateView(LoginRequiredMixin, UpdateView):
    model = Restaurant
    fields = ["name", "description", "address", "min_party", "max_party", "yelp_link"]
    template_name_suffix = "_update"


class RestaurantRandomView(View):
    def get(self, request):
        restaurant = Restaurant.objects.order_by("?").first()
        target_url = reverse("places:restaurant-detail", args=(restaurant.id,))
        return HttpResponseRedirect(target_url)
