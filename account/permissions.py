from rest_framework.permissions import BasePermission


class IsUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser


class IsSubscription(BasePermission):
    def has_permission(self, request, view):
        return request.user.subscription_start != None and request.user.account_type == 'head'


class IsHeadNotSubs(BasePermission):    # ?
    def has_permission(self, request, view):
        return request.user.account_type == 'head' and request.user.subscription_start == None
