#!/usr/bin/env python
# encoding: utf-8

from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

admin.autodiscover()

urlpatterns = [
    path('openapi', get_schema_view(
        title='OwnRecipes',
        description='OwnRecipes OpenAPI',
        version='3.1.1',
    ), name='openapi'),

    # Backend REST API
    path('api/v1/', include('v1.urls', namespace='v1')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Generic Static Home
    path('', TemplateView.as_view(template_name='index.html'), name='home'),

    # Admin
    path(settings.ADMIN_URL, admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
