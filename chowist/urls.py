"""chowist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include


def get_app_path(route, package):
    """Get application path for urlpatterns.

    https://docs.djangoproject.com/en/3.0/ref/urls/#include

    Args:
        route: Literal path.
        package: Python package name.

    Returns:
        Application path instance.
    """
    url_module = f"{package}.urls"
    return path(route, include((url_module, package), namespace=package))


# Default app
urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    get_app_path("", "portal"),
    get_app_path("places/", "places"),
]
