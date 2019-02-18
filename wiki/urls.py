from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path('<int:pk>/', views.ConceptDetailView.as_view(), name='concept-detail'),
]
