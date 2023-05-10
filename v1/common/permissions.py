#!/usr/bin/env python
# encoding: utf-8

from rest_framework import permissions


class IsParentRecipeOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners
    of an object and admins to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the recipe.
        return request.user and (obj.recipe.author == request.user or request.user.is_superuser or request.user.is_staff)

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners
    of an object and admins to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the rating, and to admins.
        return request.user and (obj.author == request.user or request.user.is_superuser or request.user.is_staff)

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admins to edit.
    """

    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to admin users.
        return request.user and request.user.is_staff

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners
    of an object and admins to it.
    """

    def has_object_permission(self, request, view, obj):
        return request.user and (obj.author == request.user or request.user.is_superuser or request.user.is_staff)
