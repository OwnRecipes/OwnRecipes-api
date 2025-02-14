#!/usr/bin/env python
# encoding: utf-8

import random
from django.core.exceptions import ValidationError
from django.db.models.functions import Floor

from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from . import serializers
from .models import Recipe
from .save_recipe import SaveRecipe
from v1.common.permissions import IsOwnerOrReadOnly
from v1.recipe_groups.models import Course, Cuisine, Season, Tag


class RecipeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    lookup_field = 'slug'
    serializer_class = serializers.RecipeSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('title', 'seasons__title', 'tags__title', 'ingredient_groups__ingredients__title')
    ordering_fields = ('pub_date', 'title', 'rating')
    ordering = ('-pub_date', 'title')

    def get_queryset(self):
        query = Recipe.objects
        filter_set = {}

        # If user is anonymous, restrict recipes to public.
        if not self.request.user.is_authenticated:
            filter_set['public'] = True

        if 'course__slug' in self.request.query_params:
            filter_set['course__in'] = Course.objects.filter(
                slug__in=self.request.query_params.get('course__slug').split(',')
            )

        if 'cuisine__slug' in self.request.query_params:
            filter_set['cuisine__in'] = Cuisine.objects.filter(
                slug__in=self.request.query_params.get('cuisine__slug').split(',')
            )

        if 'season__slug' in self.request.query_params:
            filter_set['seasons__in'] = Season.objects.filter(
                slug__in=self.request.query_params.get('season__slug').split(',')
            )

        if 'tag__slug' in self.request.query_params:
            filter_set['tags__in'] = Tag.objects.filter(
                slug__in=self.request.query_params.get('tag__slug').split(',')
            )

        if 'author__username' in self.request.query_params:
            filter_set['author__username'] = self.request.query_params.get('author__username')

        if 'source' in self.request.query_params:
            filter_set['source__contains'] = self.request.query_params.get('source')

        if 'info' in self.request.query_params:
            filter_set['info__contains'] = self.request.query_params.get('info')

        if 'directions' in self.request.query_params:
            filter_set['directions__contains'] = self.request.query_params.get('directions')

        query = query.filter(**filter_set).distinct()
        if 'rating' not in self.request.query_params:
            return query

        query = query.annotate(rating_c=Floor('rating'))
        query_ratings = self.request.query_params.get('rating').split(',')

        return query.filter(rating_c__in = query_ratings)

    def create(self, request, *args, **kwargs):
        try:
            return Response(
                serializers.RecipeSerializer(
                    SaveRecipe(request.data, self.request.user).create(),
                    context={'request': request}
                ).data
            )
        except ValidationError as err:
            return Response(err.message_dict, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        try:
            return Response(
                serializers.RecipeSerializer(
                    SaveRecipe(request.data, self.request.user, partial=partial).update(self.get_object()),
                    context={'request': request}
                ).data
            )
        except ValidationError as err:
            return Response(err.message_dict, status=status.HTTP_400_BAD_REQUEST)


class MiniBrowseViewSet(viewsets.mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """
    This viewset automatically provides `list` action.
    """
    queryset = Recipe.objects.all()
    serializer_class = serializers.MiniBrowseSerializer

    def list(self, request, *args, **kwargs):
        # If user is anonymous, restrict recipes to public.
        if self.request.user.is_authenticated:
            qs = Recipe.objects.all()
        else:
            qs = Recipe.objects.filter(public=True)

        filter_set = {}
        if 'course__slug' in self.request.query_params:
            filter_set['course__in'] = Course.objects.filter(
                slug__in=self.request.query_params.get('course__slug').split(',')
            )
        if 'cuisine__slug' in self.request.query_params:
            filter_set['cuisine__in'] = Cuisine.objects.filter(
                slug__in=self.request.query_params.get('cuisine__slug').split(',')
            )
        if 'season__slug' in self.request.query_params:
            filter_set['seasons__in'] = Season.objects.filter(
                slug__in=self.request.query_params.get('season__slug').split(',')
            )
        if 'tag__slug' in self.request.query_params:
            filter_set['tags__in'] = Tag.objects.filter(
                slug__in=self.request.query_params.get('tag__slug').split(',')
            )

        qs = qs.filter(**filter_set).distinct()
        # Get the limit from the request and the count from the DB.
        # Compare to make sure you aren't accessing more than possible.
        limit = int(request.query_params.get('limit', 4))
        count = qs.count()
        if limit > count:
            limit = count

        # Get all ids from the DB.
        my_ids = [key.id for key in qs]
        # Select a random sample from the DB.
        rand_ids = random.sample(my_ids, limit)
        # set the queryset to that random sample.
        self.queryset = Recipe.objects.filter(id__in=rand_ids)

        return super(MiniBrowseViewSet, self).list(request, *args, **kwargs)
