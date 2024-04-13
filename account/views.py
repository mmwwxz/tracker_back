from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from account import serializers
from account.permissions import IsUser, IsAdmin


User = get_user_model()


class UserViewSet(CreateModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action in ('update', 'partial_update'):
            return serializers.ProfileUpdateSerializer
        elif self.action in ('profile', 'list'):
            return serializers.ProfileSerializer
        return serializers.RegisterSerializer

    def get_permissions(self):
        if self.action in ('list',):
            return [IsAdmin()]
        elif self.action in ('update', 'partial_update', 'destroy', 'profile', 'retrieve', 'profile'):
            return [IsUser(), IsAuthenticated()]
        return [AllowAny()]

    @action(['GET'], detail=False)
    def profile(self, request):
        user = request.user
        serializer = serializers.ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
