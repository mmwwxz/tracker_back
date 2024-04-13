from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from note.views import ReportCommentViewSet, TailoringCommentViewSet, NotepadViewSet
from workshop.views import WorkshopViewSet, TailoringViewSet, ExpenseViewSet, ReportViewSet
from .drf_swagger import urlpatterns as doc_urls
from rest_framework import routers


router = routers.DefaultRouter()


router.register(r'api/v1/workshop', WorkshopViewSet, basename='Workshop')
router.register(r'api/v1/tailoring', TailoringViewSet, basename='Tailoring')
router.register(r'api/v1/expense', ExpenseViewSet, basename='Expense')
router.register(r'api/v1/report', ReportViewSet, basename='Report')

router.register(r'api/v1/notepad', NotepadViewSet, basename='Notepad')
router.register(r'api/v1/comment/tailoring', TailoringCommentViewSet, basename='Tailoring Comment')
router.register(r'api/v1/comment/report', ReportCommentViewSet, basename='Report Comment')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/v1/account/', include('account.urls')),
]

urlpatterns += router.urls

urlpatterns += doc_urls  # swagger docs urls

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

