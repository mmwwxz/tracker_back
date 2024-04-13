from django.contrib import admin
from .models import Workshop, Tailoring, Expense, Report


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'head', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'head')
    search_fields = ('title', 'description', 'head__first_name', 'head__last_name')
    raw_id_fields = ('head',)
    filter_horizontal = ('workers',)


@admin.register(Tailoring)
class TailoringAdmin(admin.ModelAdmin):
    list_display = ('model', 'master', 'workshop', 'author', 'quantity', 'done', 'total_master_payment')
    list_filter = ('workshop', 'author', 'master')
    search_fields = ('model', 'master')
    # raw_id_fields = ('author', 'workshop')


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'workshop', 'author', 'value', 'created_at', 'updated_at')
    list_filter = ('workshop', 'author', 'created_at')
    search_fields = ('title', 'value')
    raw_id_fields = ('author', 'workshop')


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('workshop', 'author', 'tailoring', 'expenses_total', 'production_total', 'profit', 'created_at', 'updated_at')
    list_filter = ('workshop', 'author', 'created_at')
    search_fields = ('workshop__title', 'author__first_name', 'author__last_name')
    raw_id_fields = ('author', 'workshop', 'tailoring')
    filter_horizontal = ('expenses',)
