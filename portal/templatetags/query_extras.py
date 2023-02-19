from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def updated_params(context, **kwargs):
    # https://blog.ovalerio.net/archives/1512
    # https://docs.djangoproject.com/en/4.1/ref/request-response/
    query_dict = context["request"].GET.copy()
    for k, v in kwargs.items():
        query_dict[k] = v
    return query_dict.urlencode()
