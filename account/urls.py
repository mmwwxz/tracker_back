from django.urls import path, include

from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views
from .serializers import MyTokenObtainPairView


router = SimpleRouter()
router.register('', views.UserViewSet)


urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('', include(router.urls)),
]

urlpatterns += router.urls
