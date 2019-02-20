from django.urls import path

from . import views
from .forms import LoginForm

app_name = "account"  # noqa

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login', kwargs={'authentication_form': LoginForm}),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.LogoutView.as_view(), name='logout')
]
