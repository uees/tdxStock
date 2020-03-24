from django.urls import path

from . import views

app_name = "basedata"  # noqa

urlpatterns = [
    path('reports/', views.ReportView.as_view(), name='report'),
    path('xreports/', views.XReportView.as_view(), name='xreport'),
    path('compare/', views.CompareView.as_view(), name='compare'),
]
