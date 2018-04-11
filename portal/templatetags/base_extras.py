from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def nav_active(request, url):
    current_url = request.path
    reverse_url = reverse(url)
    if reverse_url in current_url:
        # Handle sub-path and root-path
        if reverse_url != '/' or current_url == '/':
            return 'active'
    return ''
