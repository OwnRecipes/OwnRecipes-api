#!/usr/bin/env python
# encoding: utf-8

import json
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from v1.recipe import views


class RecipeSerializerTests(TestCase):
    fixtures = [
        'test/users.json',
        'course_data.json',
        'cuisine_data.json',
        'season_data.json',
        'tag_data.json',
        'ing_data.json',
        'recipe_data.json'
    ]

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_retrieve_view(self):
        """Try and read the view of a recipe"""
        view = views.RecipeViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get('/api/v1/recipe/recipes/tasty-chili')
        response = view(request, slug='tasty-chili')

        self.assertTrue(response.data.get('id') == 1)
        self.assertTrue(response.data.get('title') == 'Tasty Chili')
        self.assertTrue(response.data.get('prep_time') == 60)
        self.assertTrue(response.data.get('servings') == 8)

    def test_list_view(self):
        """Try and read the view of a recipe"""
        view = views.RecipeViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe/recipes/tasty-chili?course=entry&cuisine=american')
        response = view(request)

        self.assertEqual(len(response.data.get('results')), 31)

    def test_mini_browse(self):
        """Try and read the view of a recipe"""
        view = views.MiniBrowseViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe/mini-browse')
        response = view(request)
        self.assertEqual(len(response.data), 4)

        def get_mini_browse(limit):
            v = views.MiniBrowseViewSet.as_view({'get': 'list'})
            r = self.factory.get('/api/v1/recipe/mini-browse/?limit=%s' % limit)
            results = json.loads(json.dumps(v(r).data)).get('results')
            self.assertEqual(len(results), limit)
            for r in results:
                self.assertTrue(r.get('id', False))
                self.assertTrue(r.get('slug', False))
                self.assertTrue(r.get('title', False))
                self.assertTrue(r.get('pub_date', False))
                # self.assertTrue(r.get('rating', False))
                self.assertTrue(r.get('info', False))

        get_mini_browse(2)
        get_mini_browse(4)
        get_mini_browse(6)

    def test_list_view_seasons(self):
        """Try and read the list of recipes"""
        view = views.RecipeViewSet.as_view({'get': 'list'})
        # Tasty Chili 2 is summer AND autumn
        request = self.factory.get('/api/v1/recipe/recipes/?fields=id&season__slug=summer,autumn')
        response = view(request)

        resultsLen = len(response.data.get('results'))

        uniqueResults = []
        for r in response.data.get('results'):
            r_id = r.get('id')
            if r_id not in uniqueResults:
                uniqueResults.append(r_id)
        uniqueResultsLen = len(uniqueResults)

        self.assertEqual(resultsLen, uniqueResultsLen)

    def test_list_view_tags(self):
        """Try and read the list of recipes"""
        view = views.RecipeViewSet.as_view({'get': 'list'})
        # Tasty Chili 2 is easy AND gluten-free
        request = self.factory.get('/api/v1/recipe/recipes/?fields=id&tag__slug=easy,gluten-free')
        response = view(request)

        resultsLen = len(response.data.get('results'))

        uniqueResults = []
        for r in response.data.get('results'):
            r_id = r.get('id')
            if r_id not in uniqueResults:
                uniqueResults.append(r_id)
        uniqueResultsLen = len(uniqueResults)

        self.assertEqual(resultsLen, uniqueResultsLen)
