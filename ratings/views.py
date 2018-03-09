from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class RatingsView(TemplateView):
    template_name = 'ratings/home.html'
