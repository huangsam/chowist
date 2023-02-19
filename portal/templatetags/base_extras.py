from django import template
from django.urls import reverse

register = template.Library()


class _NavigationStatus:
    ACTIVE = "active"
    INACTIVE = ""


@register.simple_tag
def nav_active(request, url):
    current_url = request.path
    reverse_url = reverse(url)
    if reverse_url == current_url:
        return _NavigationStatus.ACTIVE
    if reverse_url in current_url and reverse_url != "/":
        return _NavigationStatus.ACTIVE
    return _NavigationStatus.INACTIVE


@register.simple_tag(takes_context=True)
def updated_params(context, **kwargs):
    # https://blog.ovalerio.net/archives/1512
    # https://docs.djangoproject.com/en/4.1/ref/request-response/
    query_dict = context['request'].GET.copy()
    for k, v in kwargs.items():
        query_dict[k] = v
    return query_dict.urlencode()
