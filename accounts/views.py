from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib import messages
from django.shortcuts import render, redirect
from bayi.forms import CustomerForm, UserForm
from .forms import CustomUserCreationForm
from django.contrib.auth import views
from accounts.models import Customer
from bayi.models import SettingsSite


class DashboardView(generic.ListView):
    model = Customer
    template_name = 'pages/dashboard.html'


def MyInformationDashBoardView(request, pk, user):
    if request.user.username == user:
        customer = Customer.objects.get(pk=pk)
        form = CustomerForm(request.POST or None, instance=customer)
        form2 = UserForm(request.POST or None, instance=request.user)
        if request.method == 'POST':
            if form.is_valid() or form2.is_valid():
                form.save(), form2.save()
                messages.success(request, 'Bilgileriniz Güncellendi')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.info(request, 'Yetkisiz işlem')
        return redirect('/')
    return render(request, 'pages/dashboard.html', {'form': form, 'form2': form2})


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
        messages.success(self.request, 'Hesabınız Başarılı şekilde oluşturuldu.')
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
