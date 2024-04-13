from django_filters import rest_framework as filters
from .models import Notepad, TailoringComment, ReportComment


class NotepadFilter(filters.FilterSet):
    body = filters.CharFilter(lookup_expr='icontains')
    workshop_id = filters.NumberFilter(field_name='workshop__id')
    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Notepad
        fields = ['body', 'workshop_id', 'created_at', 'updated_at']


class TailoringCommentFilter(filters.FilterSet):
    body = filters.CharFilter(lookup_expr='icontains')
    owner_id = filters.NumberFilter(field_name='owner__id')
    workshop_id = filters.NumberFilter(field_name='workshop__id')
    tailoring_id = filters.NumberFilter(field_name='tailoring__id')
    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()

    class Meta:
        model = TailoringComment
        fields = ['body', 'owner_id', 'workshop_id', 'tailoring_id', 'created_at', 'updated_at']


class ReportCommentFilter(filters.FilterSet):
    body = filters.CharFilter(lookup_expr='icontains')
    owner_id = filters.NumberFilter(field_name='owner__id')
    workshop_id = filters.NumberFilter(field_name='workshop__id')
    report_id = filters.NumberFilter(field_name='report__id')
    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()

    class Meta:
        model = ReportComment
        fields = ['body', 'owner_id', 'workshop_id', 'report_id', 'created_at', 'updated_at']
