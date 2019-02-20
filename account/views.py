from django.conf import settings
from django.contrib.auth import views
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView
from django.shortcuts import redirect

from .forms import LoginForm, RegisterForm


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'account/registration_form.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save(False)
        user.avatar = ''
        user.save(True)
        url = reverse('account:login')
        return HttpResponseRedirect(url)


class LogoutView(views.LogoutView):
    next_page = settings.LOGIN_URL
    template_name = 'account/logged_out.html'


class LoginView(views.LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)

        return super(LoginView, self).get(request, *args, **kwargs)
