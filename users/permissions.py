from rest_framework import permissions


class IsModer(permissions.BasePermission):
    message = 'Вы являетесь администратором'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moders').exists()
