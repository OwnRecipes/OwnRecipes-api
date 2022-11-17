#!/usr/bin/env python
# encoding: utf-8

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'rating', views.RatingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('rating-count/', views.RatingCountViewSet.as_view(), name='rating-count'),
]
