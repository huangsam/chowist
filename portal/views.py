from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View

from portal.forms import UserForm

# Create your views here.

class HomeView(TemplateView):
    template_name = 'portal/home.html'


class UserFormView(View):
    form_class = UserForm
    template_name = 'portal/signup.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('portal:home')
        return render(request, self.template_name, {'form': form})


class ProfileView(LoginRequiredMixin, View):
    template_name = 'portal/profile.html'

    def get(self, request):
        return render(request, self.template_name)
