from rest_framework import permissions


class IsHead(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.head == request.user


class IsHeadOrWorker(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.workshop.head == request.user:
            return True
        return request.user in obj.workshop.workers.all()
