from urllib.parse import urlencode

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from places.forms import RestaurantForm, ReviewForm
from places.models import Restaurant, Review


class HomeView(View):
    template_name = "places/home.html"

    def get(self, request):
        if request.GET:
            if (form := RestaurantForm(request.GET)).is_valid():
                target_url = reverse("places:restaurant-list")
                query_params = {k: v for k, v in form.cleaned_data.items() if v}
                if target_queries := urlencode(query_params):
                    target_url = f"{target_url}?{target_queries}"
                return HttpResponseRedirect(target_url)
        else:
            form = RestaurantForm()
        return render(request, self.template_name, {"form": form})


class RestaurantListView(ListView):
    model = Restaurant
    paginate_by = 15
    context_object_name = "restaurant_list"

    @staticmethod
    def get_composite_query(queries):
        composite_query = queries[0]
        for query in queries[1:]:
            composite_query &= query
        return composite_query

    def get_queryset(self):
        queries = []
        if name := self.request.GET.get("name"):
            queries.append(Q(name__contains=name))
        if category := self.request.GET.get("category"):
            queries.append(Q(categories__name__contains=category))
        if min_party := self.request.GET.get("min_party"):
            if min_party.isdigit():
                queries.append(Q(min_party__gte=min_party))
        if max_party := self.request.GET.get("max_party"):
            if max_party.isdigit():
                queries.append(Q(max_party__lte=max_party))
        if queries:
            composite_query = self.get_composite_query(queries)
            return Restaurant.objects.filter(composite_query)
        return Restaurant.objects.all()


class RestaurantDetailView(DetailView):
    model = Restaurant
    context_object_name = "restaurant"


class RestaurantUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Restaurant
    fields = ["name", "description", "address", "min_party", "max_party", "yelp_link"]
    template_name_suffix = "_update"
    permission_required = "places.change_restaurant"


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
