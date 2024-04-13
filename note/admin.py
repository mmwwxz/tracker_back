from django.contrib import admin
from .models import Notepad, TailoringComment, ReportComment


@admin.register(Notepad)
class NotepadAdmin(admin.ModelAdmin):
    list_display = ('workshop', 'created_at', 'updated_at')
    search_fields = ('workshop__title',)
    list_filter = ('created_at', 'updated_at')


@admin.register(TailoringComment)
class TailoringCommentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'workshop', 'tailoring', 'created_at', 'updated_at')
    search_fields = ('owner__first_name', 'owner__last_name', 'workshop__title')
    list_filter = ('created_at', 'updated_at', 'workshop')


@admin.register(ReportComment)
class ReportCommentAdmin(admin.ModelAdmin):
    list_display = ('owner', 'workshop', 'report', 'created_at', 'updated_at')
    search_fields = ('owner__first_name', 'owner__last_name', 'workshop__title')
    list_filter = ('created_at', 'updated_at', 'workshop')
