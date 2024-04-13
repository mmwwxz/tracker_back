from bs4 import BeautifulSoup
from django.http import HttpResponse
from rest_framework import viewsets, permissions
from rest_framework.decorators import action

from note.filters import NotepadFilter, ReportCommentFilter, TailoringCommentFilter
from note.models import TailoringComment, ReportComment, Notepad
from note.permissions import IsOwner
from note.serializers import TailoringCommentSerializer, ReportCommentSerializer, NotepadSerializer
from workshop.permissions import IsHead, IsHeadOrWorker

import pandas as pd
from urllib.parse import quote


class NotepadViewSet(viewsets.ModelViewSet):
    queryset = Notepad.objects.all()
    serializer_class = NotepadSerializer
    permission_classes = [permissions.IsAuthenticated, IsHead]
    filterset_class = NotepadFilter

    def get_permissions(self):
        if self.action in ('update', 'partial_update'):
            return [IsHeadOrWorker()]
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.account_type == 'head':
            workshops = self.request.user.head_workshops.all()
            notepads = Notepad.objects.filter(workshop__in=workshops)
            return notepads

        workshops = self.request.user.workers_workshops.all()
        notepads = Notepad.objects.filter(workshop__in=workshops)
        return notepads

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        queryset = self.get_queryset()

        data = []
        for notepad in queryset:
            body_text = BeautifulSoup(notepad.body, 'html.parser').get_text() if notepad.body else None
            data.append({
                'Цех': notepad.workshop.title if notepad.workshop else None,
                'Текст блокнота': body_text,
                'Дата создания': notepad.created_at,
                'Дата обновления': notepad.updated_at,
            })

        df = pd.DataFrame(data)

        for column, dtype in df.dtypes.items():
            if dtype.name == 'datetime64[ns, UTC]':
                df[column] = df[column].dt.tz_convert(None)

        response = HttpResponse(content_type='application/vnd.ms-excel')

        filename = "Блокноты.xlsx"
        filename_ascii = quote(filename.encode('utf-8'))
        response['Content-Disposition'] = f'attachment; filename="{filename_ascii}"'

        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

        return response


class TailoringCommentViewSet(viewsets.ModelViewSet):
    queryset = TailoringComment.objects.all()
    serializer_class = TailoringCommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsHeadOrWorker]
    filterset_class = TailoringCommentFilter

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated, IsOwner()]
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.account_type == 'head':
            workshops = self.request.user.head_workshops.all()
            comments = TailoringComment.objects.filter(workshop__in=workshops)
            return comments

        workshops = self.request.user.workers_workshops.all()
        comments = TailoringComment.objects.filter(workshop__in=workshops)
        return comments

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        queryset = self.get_queryset()

        data = []
        for tailoring_comment in queryset:
            body_text = BeautifulSoup(tailoring_comment.body, 'html.parser').get_text() if tailoring_comment.body else None
            data.append({
                'Владелец комментария': tailoring_comment.owner.first_name + ' ' + tailoring_comment.owner.last_name if tailoring_comment.owner else None,
                'Цех': tailoring_comment.workshop.title if tailoring_comment.workshop else None,
                'Пошив': tailoring_comment.tailoring,
                'Текст комментария': body_text,
                'Дата создания': tailoring_comment.created_at,
                'Дата обновления': tailoring_comment.updated_at,
            })

        df = pd.DataFrame(data)

        for column, dtype in df.dtypes.items():
            if dtype.name == 'datetime64[ns, UTC]':
                df[column] = df[column].dt.tz_convert(None)

        response = HttpResponse(content_type='application/vnd.ms-excel')

        filename = "Комментарии к пошиву.xlsx"
        filename_ascii = quote(filename.encode('utf-8'))
        response['Content-Disposition'] = f'attachment; filename="{filename_ascii}"'

        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

        return response


class ReportCommentViewSet(viewsets.ModelViewSet):
    queryset = ReportComment.objects.all()
    serializer_class = ReportCommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsHeadOrWorker]
    filterset_class = ReportCommentFilter

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            return [permissions.IsAuthenticated, IsOwner()]
        return super().get_permissions()

    def get_queryset(self):
        if self.request.user.account_type == 'head':
            workshops = self.request.user.head_workshops.all()
            comments = ReportComment.objects.filter(workshop__in=workshops)
            return comments

        workshops = self.request.user.workers_workshops.all()
        comments = ReportComment.objects.filter(workshop__in=workshops)
        return comments

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        queryset = self.get_queryset()

        data = []
        for report_comment in queryset:
            body_text = BeautifulSoup(report_comment.body, 'html.parser').get_text() if report_comment.body else None
            data.append({
                'Владелец комментария': report_comment.owner.first_name + ' ' + report_comment.owner.last_name if report_comment.owner else None,
                'Цех': report_comment.workshop.title if report_comment.workshop else None,
                'Отчет': report_comment.report,
                'Текст комментария': body_text,
                'Дата создания': report_comment.created_at,
                'Дата обновления': report_comment.updated_at,
            })

        df = pd.DataFrame(data)

        for column, dtype in df.dtypes.items():
            if dtype.name == 'datetime64[ns, UTC]':
                df[column] = df[column].dt.tz_convert(None)

        response = HttpResponse(content_type='application/vnd.ms-excel')

        filename = "Комментарии к отчету.xlsx"
        filename_ascii = quote(filename.encode('utf-8'))
        response['Content-Disposition'] = f'attachment; filename="{filename_ascii}"'

        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)

        return response
