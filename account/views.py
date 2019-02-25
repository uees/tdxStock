from django.contrib.auth import views
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView

from .forms import LoginForm, RegisterForm


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'account/registration_form.html'
    success_url = '/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.success_url)

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(False)
        user.avatar = ''
        user.save(True)
        url = reverse('account:login')
        return HttpResponseRedirect(url)


class LogoutView(views.LogoutView):
    next_page = '/'
    template_name = 'account/logged_out.html'


class LoginView(views.LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'
    redirect_authenticated_user = True
    success_url = '/'
