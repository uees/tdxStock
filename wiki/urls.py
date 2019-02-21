from django.urls import path

from . import views

app_name = 'wiki'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('wiki/', views.ConceptListView.as_view(), name='concept-list'),
    path('wiki/<int:pk>/', views.ConceptDetailView.as_view(), name='concept-detail'),
    path('wiki/create/', views.ConceptStoreView.as_view(), name='concept-store')
]
