from django.contrib import admin

from .models import (AccountingSubject, Concept, Industry, Report, ReportItem,
                     ReportType, Section, Stock, Territory)


@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    list_display = ('name', 'memo')


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'memo')


@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'memo')
    list_select_related = ('parent', 'parent__parent')

    def get_queryset(self, request):
        """
        Return a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view.
        """
        qs = self.model._default_manager.get_queryset()
        # 只显示3级分类
        qs = qs.filter(parent__parent__isnull=False)
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent":
            # 只展示1·2级分类
            kwargs["queryset"] = Industry.objects.select_related(*self.list_select_related)\
                .filter(parent__parent__isnull=True)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'company_name', 'ownership_nature', 'registered_capital', 'found_date', 'listing_date')
    list_display_links = ('name', 'code', 'company_name')
    search_fields = ('name', 'code', 'company_name')
    list_filter = ('ownership_nature',)


@admin.register(ReportType)
class ReportTypeAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ('name', 'slug', 'memo')
    list_display_links = ('name',)
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


class ReportItemInline(admin.StackedInline):
    model = ReportItem


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('stock_id', 'name', 'report_type_id', 'report_date', 'is_single_quarter')
    list_display_links = ('name',)
    list_per_page = 50


admin.site.register(Territory)
