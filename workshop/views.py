from django.http import HttpResponse
from rest_framework import viewsets, permissions
import pandas as pd
from rest_framework.decorators import action

from workshop.filters import ExpenseFilter, TailoringFilter, WorkshopFilter, ReportFilter
from workshop.models import Workshop, Tailoring, Expense, Report
from workshop.permissions import IsHead, IsHeadOrWorker
from workshop.serializers import WorkshopSerializer, TailoringSerializer, ExpenseSerializer, ReportSerializer

from urllib.parse import quote


class WorkshopViewSet(viewsets.ModelViewSet):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    filterset_class = WorkshopFilter
    permission_classes = [permissions.IsAuthenticated, IsHead]

    def get_queryset(self):
        return Workshop.objects.filter(head=self.request.user)

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        queryset = self.get_queryset()
        data = []
        for workshop in queryset:
            data.append({
                'Название': workshop.title,
                'Описание': workshop.description,
                'Руководитель': f"{workshop.head.first_name} {workshop.head.last_name}" if workshop.head else None,
                'Дата создания': workshop.created_at,
                'Дата обновления': workshop.updated_at,
            })

        df = pd.DataFrame(data)

        for column, dtype in df.dtypes.items():
            if dtype.name == 'datetime64[ns, UTC]':
                df[column] = df[column].dt.tz_convert(None)

        response = HttpResponse(content_type='application/vnd.ms-excel')

        filename = "Цех.xlsx"
        filename_ascii = quote(filename.encode('utf-8'))
        response['Content-Disposition'] = f'attachment; filename="{filename_ascii}"'

        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

        return response


class TailoringViewSet(viewsets.ModelViewSet):
    queryset = Tailoring.objects.all()
    serializer_class = TailoringSerializer
    filterset_class = TailoringFilter
    permission_classes = [permissions.IsAuthenticated, IsHeadOrWorker]

    def get_queryset(self):
        if self.request.user.account_type == 'head':
            workshops = self.request.user.head_workshops.all()
            tailoring = Tailoring.objects.filter(workshop__in=workshops)
            return tailoring

        workshops = self.request.user.workers_workshops.all()
        tailoring = Tailoring.objects.filter(workshop__in=workshops)
        return tailoring

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        queryset = self.get_queryset()

        data = []
        for tailoring in queryset:
            data.append({
                'Автор записи': tailoring.author.first_name + ' ' + tailoring.author.last_name if tailoring.author else None,
                'Цех': tailoring.workshop.title if tailoring.workshop else None,
                'Модель': tailoring.model,
                'Мастер': tailoring.master,
                'Количество': tailoring.quantity,
                'Цена за единицу работы мастера': tailoring.master_unit_price,
                'Выполнено': tailoring.done,
                'Общая оплата мастеру': tailoring.total_master_payment,
                'Дата создания': tailoring.created_at,
                'Дата обновления': tailoring.updated_at,
            })

        df = pd.DataFrame(data)

        for column, dtype in df.dtypes.items():
            if dtype.name == 'datetime64[ns, UTC]':
                df[column] = df[column].dt.tz_convert(None)

        response = HttpResponse(content_type='application/vnd.ms-excel')

        filename = "Пошив.xlsx"
        filename_ascii = quote(filename.encode('utf-8'))
        response['Content-Disposition'] = f'attachment; filename="{filename_ascii}"'

        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

        return response


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filterset_class = ExpenseFilter
    permission_classes = [permissions.IsAuthenticated, IsHeadOrWorker]

    def get_queryset(self):
        if self.request.user.account_type == 'head':
            workshops = self.request.user.head_workshops.all()
            expenses = Expense.objects.filter(workshop__in=workshops)
            return expenses

        workshops = self.request.user.workers_workshops.all()
        expenses = Expense.objects.filter(workshop__in=workshops)
        return expenses

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        queryset = self.get_queryset()

        data = []
        for expense in queryset:
            data.append({
                'Автор записи': expense.author.first_name + ' ' + expense.author.last_name if expense.author else None,
                'Цех': expense.workshop.title if expense.workshop else None,
                'Название расхода': expense.title,
                'Сумма расхода': expense.value,
                'Дата создания': expense.created_at,
                'Дата обновления': expense.updated_at,
            })

        df = pd.DataFrame(data)

        for column, dtype in df.dtypes.items():
            if dtype.name == 'datetime64[ns, UTC]':
                df[column] = df[column].dt.tz_convert(None)

        response = HttpResponse(content_type='application/vnd.ms-excel')

        filename = "Расходы.xlsx"
        filename_ascii = quote(filename.encode('utf-8'))
        response['Content-Disposition'] = f'attachment; filename="{filename_ascii}"'

        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

        return response


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    filterset_class = ReportFilter
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated, IsHeadOrWorker]

    def get_queryset(self):
        if self.request.user.account_type == 'head':
            workshops = self.request.user.head_workshops.all()
            reports = Report.objects.filter(workshop__in=workshops)
            return reports

        workshops = self.request.user.workers_workshops.all()
        reports = Report.objects.filter(workshop__in=workshops)
        return reports

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        queryset = self.get_queryset()

        data = []
        for report in queryset:
            data.append({
                'Автор записи': report.author.first_name + ' ' + report.author.last_name if report.author else None,
                'Цех': report.workshop.title if report.workshop else None,
                'Пошив': report.tailoring.model if report.tailoring else None,
                'Общая сумма расходов': report.expenses_total,
                'Общая стоимость производства': report.production_total,
                'Стоимость производства за единицу': report.production_unit,
                'Цена продажи за единицу': report.unit,
                'Общая сумма для продажи': report.total,
                'Маржа': report.margin,
                'Прибыль': report.profit,
                'Дата создания': report.created_at,
                'Дата обновления': report.updated_at,
            })

        df = pd.DataFrame(data)

        for column, dtype in df.dtypes.items():
            if dtype.name == 'datetime64[ns, UTC]':
                df[column] = df[column].dt.tz_convert(None)

        response = HttpResponse(content_type='application/vnd.ms-excel')

        filename = "Отчеты.xlsx"
        filename_ascii = quote(filename.encode('utf-8'))
        response['Content-Disposition'] = f'attachment; filename="{filename_ascii}"'

        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

        return response
