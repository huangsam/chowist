from django import template
from django.urls import NoReverseMatch, reverse

register = template.Library()


class _NavigationStatus:
    ACTIVE = "active"
    INACTIVE = ""


@register.simple_tag
def nav_active(request, url):
    # Handle case where request might be a string (during testing)
    if hasattr(request, "path"):
        current_url = request.path
    else:
        current_url = str(request)

    try:
        reverse_url = reverse(url)
        if reverse_url == current_url:
            return _NavigationStatus.ACTIVE
        if reverse_url in current_url and reverse_url != "/":
            return _NavigationStatus.ACTIVE
    except NoReverseMatch:
        pass
    return _NavigationStatus.INACTIVE
