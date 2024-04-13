from django_filters import rest_framework as filters
from .models import Workshop, Tailoring, Expense, Report


class WorkshopFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    description = filters.CharFilter(lookup_expr='icontains')
    head_id = filters.NumberFilter(field_name='head__id')
    created_at = filters.DateFilter()
    created_at__gte = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = filters.DateFilter(field_name='created_at', lookup_expr='lte')
    updated_at = filters.DateFilter()
    updated_at__gte = filters.DateFilter(field_name='updated_at', lookup_expr='gte')
    updated_at__lte = filters.DateFilter(field_name='updated_at', lookup_expr='lte')

    class Meta:
        model = Workshop
        fields = ['title', 'description', 'head_id', 'created_at', 'created_at__gte', 'created_at__lte', 'updated_at', 'updated_at__gte', 'updated_at__lte']


class TailoringFilter(filters.FilterSet):
    model = filters.CharFilter(lookup_expr='icontains')
    master = filters.CharFilter(lookup_expr='icontains')
    workshop_id = filters.NumberFilter(field_name='workshop__id')
    author_id = filters.NumberFilter(field_name='author__id')
    quantity = filters.NumberFilter()
    quantity__gte = filters.NumberFilter(field_name='quantity', lookup_expr='gte')
    quantity__lte = filters.NumberFilter(field_name='quantity', lookup_expr='lte')
    master_unit_price = filters.NumberFilter()
    master_unit_price__gte = filters.NumberFilter(field_name='master_unit_price', lookup_expr='gte')
    master_unit_price__lte = filters.NumberFilter(field_name='master_unit_price', lookup_expr='lte')
    done = filters.NumberFilter()
    done__gte = filters.NumberFilter(field_name='done', lookup_expr='gte')
    done__lte = filters.NumberFilter(field_name='done', lookup_expr='lte')
    total_master_payment = filters.NumberFilter()
    total_master_payment__gte = filters.NumberFilter(field_name='total_master_payment', lookup_expr='gte')
    total_master_payment__lte = filters.NumberFilter(field_name='total_master_payment', lookup_expr='lte')
    created_at = filters.DateFilter()
    created_at__gte = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = filters.DateFilter(field_name='created_at', lookup_expr='lte')
    updated_at = filters.DateFilter()
    updated_at__gte = filters.DateFilter(field_name='updated_at', lookup_expr='gte')
    updated_at__lte = filters.DateFilter(field_name='updated_at', lookup_expr='lte')

    class Meta:
        model = Tailoring
        fields = ['model', 'master', 'workshop_id', 'author_id', 'quantity', 'quantity__gte', 'quantity__lte', 'master_unit_price', 'master_unit_price__gte', 'master_unit_price__lte', 'done', 'done__gte', 'done__lte', 'total_master_payment', 'total_master_payment__gte', 'total_master_payment__lte', 'created_at', 'created_at__gte', 'created_at__lte', 'updated_at', 'updated_at__gte', 'updated_at__lte']


class ExpenseFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    workshop_id = filters.NumberFilter(field_name='workshop__id')
    author_id = filters.NumberFilter(field_name='author__id')
    value = filters.NumberFilter()
    value__gte = filters.NumberFilter(field_name='value', lookup_expr='gte')
    value__lte = filters.NumberFilter(field_name='value', lookup_expr='lte')
    created_at = filters.DateFilter()
    created_at__gte = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = filters.DateFilter(field_name='created_at', lookup_expr='lte')
    updated_at = filters.DateFilter()
    updated_at__gte = filters.DateFilter(field_name='updated_at', lookup_expr='gte')
    updated_at__lte = filters.DateFilter(field_name='updated_at', lookup_expr='lte')

    class Meta:
        model = Expense
        fields = ['title', 'workshop_id', 'author_id', 'value', 'value__gte', 'value__lte', 'created_at', 'created_at__gte', 'created_at__lte', 'updated_at', 'updated_at__gte', 'updated_at__lte']


class ReportFilter(filters.FilterSet):
    workshop_id = filters.NumberFilter(field_name='workshop__id')
    tailoring_id = filters.NumberFilter(field_name='tailoring__id')
    author_id = filters.NumberFilter(field_name='author__id')
    expenses_total = filters.NumberFilter()
    expenses_total__gte = filters.NumberFilter(field_name='expenses_total', lookup_expr='gte')
    expenses_total__lte = filters.NumberFilter(field_name='expenses_total', lookup_expr='lte')
    production_total = filters.NumberFilter()
    production_total__gte = filters.NumberFilter(field_name='production_total', lookup_expr='gte')
    production_total__lte = filters.NumberFilter(field_name='production_total', lookup_expr='lte')
    production_unit = filters.NumberFilter()
    production_unit__gte = filters.NumberFilter(field_name='production_unit', lookup_expr='gte')
    production_unit__lte = filters.NumberFilter(field_name='production_unit', lookup_expr='lte')
    unit = filters.NumberFilter()
    unit__gte = filters.NumberFilter(field_name='unit', lookup_expr='gte')
    unit__lte = filters.NumberFilter(field_name='unit', lookup_expr='lte')
    total = filters.NumberFilter()
    total__gte = filters.NumberFilter(field_name='total', lookup_expr='gte')
    total__lte = filters.NumberFilter(field_name='total', lookup_expr='lte')
    margin = filters.NumberFilter()
    margin__gte = filters.NumberFilter(field_name='margin', lookup_expr='gte')
    margin__lte = filters.NumberFilter(field_name='margin', lookup_expr='lte')
    profit = filters.NumberFilter()
    profit__gte = filters.NumberFilter(field_name='profit', lookup_expr='gte')
    profit__lte = filters.NumberFilter(field_name='profit', lookup_expr='lte')
    created_at = filters.DateFilter()
    created_at__gte = filters.DateFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = filters.DateFilter(field_name='created_at', lookup_expr='lte')
    updated_at = filters.DateFilter()
    updated_at__gte = filters.DateFilter(field_name='updated_at', lookup_expr='gte')
    updated_at__lte = filters.DateFilter(field_name='updated_at', lookup_expr='lte')

    class Meta:
        model = Report
        fields = ['workshop_id', 'tailoring_id', 'author_id', 'expenses_total', 'expenses_total__gte', 'expenses_total__lte', 'production_total', 'production_total__gte', 'production_total__lte', 'production_unit', 'production_unit__gte', 'production_unit__lte', 'unit', 'unit__gte', 'unit__lte', 'total', 'total__gte', 'total__lte', 'margin', 'margin__gte', 'margin__lte', 'profit', 'profit__gte', 'profit__lte', 'created_at', 'created_at__gte', 'created_at__lte', 'updated_at', 'updated_at__gte', 'updated_at__lte']
