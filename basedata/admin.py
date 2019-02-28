from django.contrib import admin

from .models import Stock, Industry, Concept, Territory, Section, ReportType, AccountingSubject, Report, ReportItem


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'company_name', 'ownership_nature', 'registered_capital', 'found_date', 'listing_date')
    list_display_links = ('name', 'code', 'company_name')
    search_fields = ('name', 'code', 'company_name')
    list_filter = ('ownership_nature',)


@admin.register(ReportType)
class ReportTypeAdmin(admin.ModelAdmin):
    list_select_related = ('parent',)
    list_per_page = 20
    list_display = ('parent', 'name', 'slug', 'memo')
    list_display_links = ('name',)
    list_filter = ('parent',)
    search_fields = ('name', 'slug')


@admin.register(AccountingSubject)
class AccountingSubjectAdmin(admin.ModelAdmin):
    list_select_related = ('report_type', 'parent', 'parent__report_type')  # 防止 N + 1
    list_display = ('report_type', 'parent', 'name', 'slug', 'memo')  # 列表显示的字段
    list_display_links = ('name',)  # 列表显示链接字段
    list_per_page = 50
    list_filter = ('report_type',)
    search_fields = ('name', 'slug')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            kwargs["queryset"] = AccountingSubject.objects.select_related(*self.list_select_related)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Industry)
admin.site.register(Concept)
admin.site.register(Territory)
admin.site.register(Section)
admin.site.register(Report)
admin.site.register(ReportItem)
