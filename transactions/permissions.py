from rest_framework.permissions import BasePermission


class CanReadTransactionPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.has_perm("transactions.view_transaction")


class CanDeleteTransactionPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("transactions.delete_transaction")


class CanUpdateTransactionPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("transactions.change_transaction")


class CanCreateTransactionPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("transactions.add_transaction")


class CanChangeTransactionStatus(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("transactions.can_change_transaction_status")
