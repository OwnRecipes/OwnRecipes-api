#!/usr/bin/env python
# encoding: utf-8

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'mini-browse', views.MiniBrowseViewSet)
router.register(r'recipes', views.RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]
