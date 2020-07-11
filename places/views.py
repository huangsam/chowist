from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from places.forms import ReviewForm
from places.models import Restaurant, Review


class HomeView(TemplateView):
    template_name = "places/home.html"


class RestaurantListView(ListView):
    model = Restaurant
    ordering = ["name"]
    paginate_by = 15
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
        target_url = reverse("places:restaurant-detail", args=[restaurant.id])
        return HttpResponseRedirect(target_url)


class RestaurantReviewView(LoginRequiredMixin, View):
    template_name = "places/restaurant_review.html"

    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.get(id=restaurant_id)
        try:
            review = Review.objects.get(place=restaurant, author=request.user)
            form = ReviewForm(instance=review)
        except Review.DoesNotExist:
            form = ReviewForm()
        context = {"form": form, "restaurant": restaurant}
        return render(request, self.template_name, context)

    def post(self, request, restaurant_id):
        form = ReviewForm(request.POST)
        restaurant = Restaurant.objects.get(id=restaurant_id)
        if not form.is_valid():
            context = {"form": form, "restaurant": restaurant}
            return render(request, self.template_name, context)
        try:
            review = Review.objects.get(place=restaurant, author=request.user)
            review.__dict__.update(**form.cleaned_data)
            review.save()
        except Review.DoesNotExist:
            Review.objects.create(
                place=restaurant,
                author=request.user,
                title=form.cleaned_data["title"],
                body=form.cleaned_data["body"],
                rating=form.cleaned_data["rating"],
            )
        success_url = reverse("places:restaurant-detail", args=[restaurant.id])
        return HttpResponseRedirect(success_url)
