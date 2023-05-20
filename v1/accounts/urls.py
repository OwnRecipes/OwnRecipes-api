#!/usr/bin/env python
# encoding: utf-8

from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView
from . import views

urlpatterns = [
    path('obtain-auth-token/', views.MyObtainTokenPairView.as_view()),
    path('refresh-auth-token/', TokenRefreshView.as_view()),
    path('revoke-auth-token/', TokenBlacklistView.as_view())
]
