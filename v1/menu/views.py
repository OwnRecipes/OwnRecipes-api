#!/usr/bin/env python
# encoding: utf-8

from rest_framework import viewsets, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count, Max

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from v1.recipe.models import Recipe
from v1.common.permissions import IsOwner
from .models import MenuItem
from .serializers import MenuItemSerializer

class MenuItemViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Menu Items.
    """
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = (IsOwner,)
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ('recipe', 'start_date', 'complete_date', 'complete')
    ordering_fields = ('start_date', 'id')

    def get_queryset(self):
        user = self.request.user
        if user and not user.is_anonymous:
            return MenuItem.objects.filter(author=user).order_by('start_date', 'id')
        return MenuItem.objects.none()


class MenuStatsViewSet(views.APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(
            Recipe.objects.annotate(
                num_menuitems=Count('menu_recipe'),
                last_made=Max('menu_recipe__complete_date')
            ).filter(
                num_menuitems__gte=1,
                menu_recipe__complete=True
            ).values(
                'slug',
                'title',
                'num_menuitems',
                'last_made',
            ).order_by(
                '-last_made',
                'num_menuitems',
            )
        )
