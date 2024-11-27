#!/usr/bin/env python
# encoding: utf-8

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'course-count', views.CourseCountViewSet, basename='course-count')
router.register(r'course', views.CourseViewSet, basename='course')
router.register(r'cuisine-count', views.CuisineCountViewSet, basename='cuisine-count')
router.register(r'cuisine', views.CuisineViewSet, basename='cuisine')
router.register(r'season-count', views.SeasonCountViewSet, basename='season-count')
router.register(r'season', views.SeasonViewSet, basename='season')
router.register(r'tag-count', views.TagCountViewSet, basename='tag-count')
router.register(r'tag', views.TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
