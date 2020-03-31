from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path('', views.ConceptListView.as_view(), name='concept-list'),
    path('create/', views.ConceptCreateView.as_view(), name='concept-store'),
    path('<int:pk>/', views.ConceptDetailView.as_view(), name='concept-detail'),
    path('<int:pk>/edit/', views.ConceptUpdateView.as_view(), name='concept-edit'),
    path('<int:concept_id>/delete/', views.delete, name='concept-delete'),
    path('look/', views.look),
]
