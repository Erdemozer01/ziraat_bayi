from django.conf import settings

from django.contrib.sites.shortcuts import get_current_site
from django.views import generic
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import views

from bayi.models import SettingsSite


class LoginView(views.LoginView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            site = SettingsSite.objects.latest('created').name
        except SettingsSite.DoesNotExist:
            site = None

        context['site'] = get_current_site(self.request)
        context['site_name'] = site
        return context


class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/sign-up.html'

    def get_success_url(self):
        return settings.LOGIN_REDIRECT_URL

    def form_valid(self, form):
        messages.success(self.request, 'üye olma işlemi başarılı')
        return super(RegisterView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            site = SettingsSite.objects.latest('created').name
        except SettingsSite.DoesNotExist:
            site = None
        context['site'] = get_current_site(self.request)
        context['site_name'] = site
        return context


class LogoutView(views.LogoutView):
    template_name = 'registration/logged_out.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        site = SettingsSite.objects.latest('created')
        context['site'] = get_current_site(self.request)
        context['site_name'] = site.name
        return context


class PasswordResetView(views.PasswordResetView):
    template_name = 'registration/password_reset_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            site = SettingsSite.objects.latest('created').name
        except SettingsSite.DoesNotExist:
            site = None
        context['site'] = get_current_site(self.request)
        context['site_name'] = site
        return context


class PasswordResetConfirmView(views.PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            site = SettingsSite.objects.latest('created').name
        except SettingsSite.DoesNotExist:
            site = None
        context['site'] = get_current_site(self.request)
        context['site_name'] = site
        return context
