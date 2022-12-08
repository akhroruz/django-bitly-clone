from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from apps.forms import UrlForm, CustomCreateUserForm, CustomLoginForm
from apps.models import Url


class MainFormView(FormView):
    form_class = UrlForm
    template_name = 'apps/index.html'
    success_url = reverse_lazy('form_view')

    def form_valid(self, form):
        url = form.save()
        url = f'{get_current_site(self.request)}/{url.short_name}'
        context = {
            'short_name': url
        }
        return render(self.request, 'apps/index.html', context)


class ShortView(View):
    def get(self, request, name, *args, **kwargs):
        url = Url.objects.get(short_name=name)
        return HttpResponseRedirect(url.long_name)


class SignupView(FormView):
    form_class = CustomCreateUserForm
    template_name = 'apps/sign-up.html'
    success_url = reverse_lazy('signin_view')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class SigninView(LoginView):
    form_class = CustomLoginForm
    template_name = 'apps/sign-in.html'
    success_url = reverse_lazy('form_view')

    def form_valid(self, form):
        form.get_user()
        messages.success(self.request, 'Match')
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('logout_view')
    template_name = 'apps/index.html'
