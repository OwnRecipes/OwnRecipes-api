#!/usr/bin/env python
# encoding: utf-8

from django.db.models import Count, IntegerField
from django.db.models.functions import Floor
from rest_framework import viewsets
from rest_framework.views import APIView

from rest_framework.response import Response

from .models import Rating
from .serializers import RatingSerializer
from v1.common.permissions import IsOwnerOrReadOnly

from .models import Recipe
from v1.recipe_groups.models import Course, Cuisine, Season, Tag
from v1.common.recipe_search import get_search_results


class RatingViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Ingredients.
    """
    queryset = Rating.objects.all().order_by('id')
    serializer_class = RatingSerializer
    permission_classes = (IsOwnerOrReadOnly,)
    filterset_fields = ('recipe', 'recipe__slug', 'author', 'rating', 'update_date')


class RatingCountViewSet(APIView):
    def get(self, request):
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
                filter_set['season__in'] = Season.objects.filter(
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
                ['title', 'ingredient_groups__ingredients__title', 'tags__title'],
                query,
                self.request.query_params.get('search')
            ).distinct()

        results = {
            5: 0,
            4: 0,
            3: 0,
            2: 0,
            1: 0,
            0: 0,
        }
        query = query.filter(**filter_set)
        query = query.annotate(rating_avg_c=Floor('rating', output_field=IntegerField())).values('rating_avg_c').annotate(rCount=Count('rating_avg_c')).order_by()

        query_result = list(query)
        for r in query_result:
            results[r['rating_avg_c']] = r['rCount']

        return Response({
            'results': [{"rating": k, "total": v} for k, v in results.items()]
        })
