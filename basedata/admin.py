from django.contrib import admin

from .models import Stock, Industry, Concept, Territory, Section, ReportType, AccountingSubject, Report, ReportItem


admin.site.register(Stock)
admin.site.register(Industry)
admin.site.register(Concept)
admin.site.register(Territory)
admin.site.register(Section)
admin.site.register(ReportType)
admin.site.register(AccountingSubject)
admin.site.register(Report)
admin.site.register(ReportItem)
