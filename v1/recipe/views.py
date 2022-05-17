#!/usr/bin/env python
# encoding: utf-8

import random
from django.db.models import Avg
from django.db.models.functions import Coalesce

from rest_framework import permissions, viewsets, filters
from rest_framework.response import Response
from v1.rating.average_rating import convert_rating_to_int

from . import serializers
from .models import Recipe
from .save_recipe import SaveRecipe
from v1.recipe_groups.models import Cuisine, Course, Tag


class RecipeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    lookup_field = 'slug'
    serializer_class = serializers.RecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('title', 'tags__title', 'ingredient_groups__ingredients__title')
    ordering_fields = ('pub_date', 'title', 'rating')
    ordering = ('-pub_date', 'title')

    def get_queryset(self):
        query = Recipe.objects
        filter_set = {}

        # If user is anonymous, restrict recipes to public.
        if not self.request.user.is_authenticated:
            filter_set['public'] = True

        if 'cuisine__slug' in self.request.query_params:
            filter_set['cuisine__in'] = Cuisine.objects.filter(
                slug__in=self.request.query_params.get('cuisine__slug').split(',')
            )

        if 'course__slug' in self.request.query_params:
            filter_set['course__in'] = Course.objects.filter(
                slug__in=self.request.query_params.get('course__slug').split(',')
            )

        if 'tag__slug' in self.request.query_params:
            filter_set['tags__in'] = Tag.objects.filter(
                slug__in=self.request.query_params.get('tag__slug').split(',')
            )

        query = query.filter(**filter_set)

        query = query.annotate(rating_avg=Coalesce(Avg('rating__rating'), 0))
        if 'rating_avg' in self.request.query_params:
            query = query.filter(rating_avg=self.request.query_params['rating_avg'])
        return query

    def create(self, request, *args, **kwargs):
        return Response(
            serializers.RecipeSerializer(
                SaveRecipe(request.data, self.request.user).create(),
                context={'request': request}
            ).data
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        return Response(
            serializers.RecipeSerializer(
                SaveRecipe(request.data, self.request.user, partial=partial).update(self.get_object()),
                context={'request': request}
            ).data
        )


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
