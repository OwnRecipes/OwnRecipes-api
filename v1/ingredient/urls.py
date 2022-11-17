#!/usr/bin/env python
# encoding: utf-8

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'ingredient', views.IngredientViewSet)
router.register(r'ingredient-group', views.IngredientGroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
