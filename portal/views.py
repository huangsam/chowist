import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView

from portal.forms import UserForm
from portal.models import Profile

logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    template_name = 'portal/home.html'


class UserFormView(FormView):
    template_name = 'portal/signup.html'
    form_class = UserForm
    success_url = reverse_lazy('portal:home')

    def form_valid(self, form):
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        logger.info('User {usr} registered to the system'.format(usr=username))
        return super().form_valid(form)


class ProfileView(LoginRequiredMixin, View):
    template_name = 'portal/profile.html'

    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        return render(request, self.template_name, {'profile': profile})
