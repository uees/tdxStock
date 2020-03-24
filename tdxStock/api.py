from rest_framework import routers

from account import api_views as account_views
from basedata import views as basedata_views

router = routers.DefaultRouter()
router.register(r'account/users', account_views.UserViewSet)
router.register(r'account/groups', account_views.GroupViewSet)
router.register(r'stocks', basedata_views.StockViewSet)
router.register(r'industries', basedata_views.IndustryViewSet)
router.register(r'concepts', basedata_views.ConceptViewSet)
router.register(r'territories', basedata_views.TerritoryViewSet)
router.register(r'sections', basedata_views.SectionViewSet)
router.register(r'report-types', basedata_views.ReportTypeViewSet)
router.register(r'subjects', basedata_views.AccountingSubjectViewSet)
