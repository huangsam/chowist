import django_filters

from places.models import Restaurant


class RestaurantFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")
    category = django_filters.CharFilter(field_name="categories__name", lookup_expr="icontains")
    min_party = django_filters.NumberFilter(field_name="min_party", lookup_expr="gte")
    max_party = django_filters.NumberFilter(field_name="max_party", lookup_expr="lte")

    class Meta:
        model = Restaurant
        fields = ["name", "category", "min_party", "max_party"]
