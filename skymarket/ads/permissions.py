# TODO здесь производится настройка пермишенов для нашего проекта
from rest_framework import permissions

from ads.models import User


# class IsOwner(permissions.BasePermission):
#     message = 'Allowed only for the owner'
#
#     def has_permission(self, request, view):
#         return request.user.id == view.get_object().owner.id


class IsAuthor(permissions.BasePermission):
    message = 'Allowed only for the author'

    def has_permission(self, request, view):
        return request.user.id == view.get_object().author.id


class IsAdmin(permissions.BasePermission):
    message = 'Allowed only for admins'

    def has_permission(self, request, view):
        return request.user.role == User.ADMIN


# not used so far
# class IsSelf(permissions.BasePermission):
#     message = "Allowed only for the record's owner"
#
#     def has_permission(self, request, view):
#         return request.user.id == view.get_object().id
