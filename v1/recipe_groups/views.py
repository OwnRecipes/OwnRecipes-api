#!/usr/bin/env python
# encoding: utf-8

from django.db.models import Count
from django.db.models.functions import Floor
from rest_framework import viewsets

from v1.recipe_groups.models import Course, Cuisine, Season, Tag
from v1.recipe.models import Recipe
from v1.recipe_groups import serializers
from v1.common.permissions import IsParentRecipeOwnerOrReadOnly
from v1.common.recipe_search import get_search_results


class CourseViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Uses `slug` as the PK for any lookups.
    """
    queryset = Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = (IsParentRecipeOwnerOrReadOnly,)
    lookup_field = 'slug'

class CourseCountViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Uses `slug` as the PK for any lookups.
    """
    serializer_class = serializers.AggCourseSerializer
    permission_classes = (IsParentRecipeOwnerOrReadOnly,)
    lookup_field = 'slug'

    def get_queryset(self):
        query = Recipe.objects
        filter_set = {}

        # If user is anonymous, restrict recipes to public.
        if not self.request.user.is_authenticated:
            filter_set['public'] = True

        if 'cuisine' in self.request.query_params:
            try:
                filter_set['cuisine__in'] = Cuisine.objects.filter(
                    slug__in=self.request.query_params.get('cuisine').split(',')
                )
            except:
                return []

        if 'season' in self.request.query_params:
            try:
                filter_set['seasons__in'] = Season.objects.filter(
                    slug__in=self.request.query_params.get('season').split(',')
                )
            except:
                return []

        if 'tag' in self.request.query_params:
            try:
                filter_set['tags__in'] = Tag.objects.filter(
                    slug__in=self.request.query_params.get('tag').split(',')
                )
            except:
                return []

        if 'search' in self.request.query_params:
            query = get_search_results(
                ['title', 'ingredient_groups__ingredients__title', 'seasons__title', 'tags__title'],
                query,
                self.request.query_params.get('search')
            ).distinct()

        query = query.filter(**filter_set)
        if 'rating' in self.request.query_params:
            query = query.annotate(rating_c=Floor('rating'))
            query_ratings = self.request.query_params.get('rating').split(',')
            query = query.filter(rating_c__in = query_ratings)

        return Course.objects.filter(recipe__in=query).order_by('title').annotate(total=Count('recipe', distinct=True))


class CuisineViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Uses `slug` as the PK for any lookups.
    """
    queryset = Cuisine.objects.all()
    serializer_class = serializers.CuisineSerializer
    permission_classes = (IsParentRecipeOwnerOrReadOnly,)
    lookup_field = 'slug'

class CuisineCountViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Uses `slug` as the PK for any lookups.
    """
    serializer_class = serializers.AggCuisineSerializer
    permission_classes = (IsParentRecipeOwnerOrReadOnly,)
    lookup_field = 'slug'

    def get_queryset(self):
        query = Recipe.objects
        filter_set = {}

        # If user is anonymous, restrict recipes to public.
        if not self.request.user.is_authenticated:
            filter_set['public'] = True

        if 'course' in self.request.query_params:
            try:
                filter_set['course__in'] = Course.objects.filter(
                    slug__in=self.request.query_params.get('course').split(',')
                )
            except:
                return []

        if 'season' in self.request.query_params:
            try:
                filter_set['seasons__in'] = Season.objects.filter(
                    slug__in=self.request.query_params.get('season').split(',')
                )
            except:
                return []

        if 'tag' in self.request.query_params:
            try:
                filter_set['tags__in'] = Tag.objects.filter(
                    slug__in=self.request.query_params.get('tag').split(',')
                )
            except:
                return []

        if 'search' in self.request.query_params:
            query = get_search_results(
                ['title', 'ingredient_groups__ingredients__title', 'seasons__title', 'tags__title'],
                query,
                self.request.query_params.get('search')
            ).distinct()

        query = query.filter(**filter_set)
        if 'rating' in self.request.query_params:
            query = query.annotate(rating_c=Floor('rating'))
            query_ratings = self.request.query_params.get('rating').split(',')
            query = query.filter(rating_c__in = query_ratings)

        return Cuisine.objects.filter(recipe__in=query).order_by('title').annotate(total=Count('recipe', distinct=True))


class SeasonViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Uses `slug` as the PK for any lookups.
    """
    queryset = Season.objects.all()
    serializer_class = serializers.SeasonSerializer
    permission_classes = (IsParentRecipeOwnerOrReadOnly,)
    lookup_field = 'slug'

class SeasonCountViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Uses `title` as the PK for any lookups.
    """
    serializer_class = serializers.AggSeasonSerializer
    permission_classes = (IsParentRecipeOwnerOrReadOnly,)
    lookup_field = 'slug'

    def get_queryset(self):
        query = Recipe.objects
        filter_set = {}

        # If user is anonymous, restrict recipes to public.
        if not self.request.user.is_authenticated:
            filter_set['public'] = True

        if 'course' in self.request.query_params:
            try:
                filter_set['course__in'] = Course.objects.filter(
                    slug__in=self.request.query_params.get('course').split(',')
                )
            except:
                return []

        if 'cuisine' in self.request.query_params:
            try:
                filter_set['cuisine__in'] = Cuisine.objects.filter(
                    slug__in=self.request.query_params.get('cuisine').split(',')
                )
            except:
                return []

        if 'tag' in self.request.query_params:
            try:
                filter_set['tags__in'] = Tag.objects.filter(
                    slug__in=self.request.query_params.get('tag').split(',')
                )
            except:
                return []

        if 'search' in self.request.query_params:
            query = get_search_results(
                ['title', 'ingredient_groups__ingredients__title', 'tags__title'],
                query,
                self.request.query_params.get('search')
            ).distinct()

        query = query.filter(**filter_set)
        if 'rating' in self.request.query_params:
            query = query.annotate(rating_c=Floor('rating'))
            query_ratings = self.request.query_params.get('rating').split(',')
            query = query.filter(rating_c__in = query_ratings)

        return Season.objects.filter(recipe__in=query).order_by('title').annotate(total=Count('recipe', distinct=True))


class TagViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Uses `title` as the PK for any lookups.
    """
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = (IsParentRecipeOwnerOrReadOnly,)
    lookup_field = 'title'
    ordering_fields = ('title',)

class TagCountViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Uses `title` as the PK for any lookups.
    """
    serializer_class = serializers.AggTagSerializer
    permission_classes = (IsParentRecipeOwnerOrReadOnly,)
    lookup_field = 'slug'

    def get_queryset(self):
        query = Recipe.objects
        filter_set = {}

        # If user is anonymous, restrict recipes to public.
        if not self.request.user.is_authenticated:
            filter_set['public'] = True

        if 'course' in self.request.query_params:
            try:
                filter_set['course__in'] = Course.objects.filter(
                    slug__in=self.request.query_params.get('course').split(',')
                )
            except:
                return []

        if 'cuisine' in self.request.query_params:
            try:
                filter_set['cuisine__in'] = Cuisine.objects.filter(
                    slug__in=self.request.query_params.get('cuisine').split(',')
                )
            except:
                return []

        if 'season' in self.request.query_params:
            try:
                filter_set['seasons__in'] = Season.objects.filter(
                    slug__in=self.request.query_params.get('season').split(',')
                )
            except:
                return []

        if 'search' in self.request.query_params:
            query = get_search_results(
                ['title', 'ingredient_groups__ingredients__title', 'tags__title'],
                query,
                self.request.query_params.get('search')
            ).distinct()

        query = query.filter(**filter_set)
        if 'rating' in self.request.query_params:
            query = query.annotate(rating_c=Floor('rating'))
            query_ratings = self.request.query_params.get('rating').split(',')
            query = query.filter(rating_c__in = query_ratings)

        return Tag.objects.filter(recipe__in=query).order_by('title').annotate(total=Count('recipe', distinct=True))
