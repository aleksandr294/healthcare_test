from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


def check_auth(request):
    if isinstance(request.user, AnonymousUser):
        return False
    return True


class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if not check_auth(request):
            return False
        return request.user.is_staff


class IsPatient(permissions.BasePermission):
    def has_permission(self, request, view):
        if not check_auth(request):
            return False
        return not request.user.is_staff
