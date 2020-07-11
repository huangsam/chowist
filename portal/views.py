import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView

from portal.forms import ProfileForm, UserForm
from portal.models import Profile

logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = "portal/home.html"


class ProfileSignupView(FormView):
    template_name = "portal/profile_signup.html"
    form_class = UserForm
    success_url = reverse_lazy("portal:home")

    def form_valid(self, form):
        user = form.save(commit=False)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user.set_password(password)
        user.save()
        logger.info(f"User {username} registered to the system")
        return super().form_valid(form)


class ProfileDetailView(LoginRequiredMixin, View):
    template_name = "portal/profile_detail.html"

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        return render(request, self.template_name, {"profile": profile})


class ProfileUpdateView(LoginRequiredMixin, View):
    template_name = "portal/profile_update.html"

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        form = ProfileForm(instance=profile)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = ProfileForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})
        profile = Profile.objects.get(user=request.user)
        profile.__dict__.update(**form.cleaned_data)
        profile.save()
        return HttpResponseRedirect(reverse("portal:profile"))
