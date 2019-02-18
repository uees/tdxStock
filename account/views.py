from django.conf import settings
from django.contrib import auth
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView

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


class LogoutView(RedirectView):
    url = settings.LOGIN_URL

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'
    redirect_field_name = REDIRECT_FIELD_NAME
    success_url = '/'

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if redirect_to is None:
            redirect_to = '/'
        kwargs['redirect_to'] = redirect_to

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form = AuthenticationForm(data=self.request.POST, request=self.request)

        if form.is_valid():
            auth.login(self.request, form.get_user())
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        redirect_to = self.request.POST.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, allowed_hosts=[self.request.get_host()]):
            redirect_to = self.success_url
        return redirect_to
