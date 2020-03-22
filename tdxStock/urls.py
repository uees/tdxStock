"""tdxStock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from rest_framework import routers
from account import api
from basedata import views as basedata_views

admin.AdminSite.site_title = settings.SITE_NAME
admin.AdminSite.site_header = '%s 管理' % settings.SITE_NAME

router = routers.DefaultRouter()
router.register(r'account/users', api.UserViewSet)
router.register(r'account/groups', api.GroupViewSet)
router.register(r'stocks', basedata_views.StockViewSet)
router.register(r'industries', basedata_views.IndustryViewSet)
router.register(r'concepts', basedata_views.ConceptViewSet)
router.register(r'territories', basedata_views.TerritoryViewSet)
router.register(r'sections', basedata_views.SectionViewSet)

urlpatterns = [
    path('', RedirectView.as_view(url='/wiki/'), name='index'),
    path('wiki/', include('wiki.urls')),
    path('account/', include('account.urls')),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    import debug_toolbar

    # Server statics and uploaded media
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

    # debug_toolbar
    urlpatterns.extend([
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ])
