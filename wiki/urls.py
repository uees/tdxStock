from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('wiki/', views.ConceptListView.as_view(), name='concept-list'),
    path('wiki/create/', views.ConceptCreateView.as_view(), name='concept-store'),
    path('wiki/<int:pk>/', views.ConceptDetailView.as_view(), name='concept-detail'),
    path('wiki/<int:pk>/edit/', views.ConceptUpdateView.as_view(), name='concept-edit'),
    path('wiki/<int:concept_id>/delete/', views.delete, name='concept-delete')
]
