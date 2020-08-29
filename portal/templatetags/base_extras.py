from django import template
from django.urls import reverse

register = template.Library()

# Module-level constants
_IS_ACTIVE = "active"
_IS_INACTIVE = ""


@register.simple_tag
def nav_active(request, url):
    current_url = request.path
    reverse_url = reverse(url)
    if reverse_url == current_url:
        return _IS_ACTIVE
    if reverse_url in current_url and reverse_url != "/":
        return _IS_ACTIVE
    return _IS_INACTIVE
