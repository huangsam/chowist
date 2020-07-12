from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
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
    paginate_by = 15
    context_object_name = "restaurant_list"

    @staticmethod
    def get_composite_key(queries):
        composite = queries[0]
        for query in queries[1:]:
            composite &= query
        return composite

    def get_queryset(self):
        queries = []
        name = self.request.GET.get("name")
        if name:
            queries.append(Q(name__contains=name))
        category = self.request.GET.get("category")
        if category:
            queries.append(Q(categories__name__contains=category))
        min_party = self.request.GET.get("min_party")
        if min_party and min_party.isdigit():
            queries.append(Q(min_party__gte=min_party))
        max_party = self.request.GET.get("max_party")
        if max_party and max_party.isdigit():
            queries.append(Q(max_party__lte=max_party))
        if queries:
            composite = self.get_composite_key(queries)
            return Restaurant.objects.filter(composite)
        return Restaurant.objects.all()


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
