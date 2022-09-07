#!/usr/bin/env python
# encoding: utf-8

from django.test import TestCase
from rest_framework.test import APIRequestFactory
from v1.recipe import views as recipe_views
from v1.rating import views as ratings_views


class RecipeSerializerTests(TestCase):
    fixtures = [
        'test/users.json',
        'course_data.json',
        'cuisine_data.json',
        'tag_data.json',
        'ing_data.json',
        'recipe_data.json',
        'rating_data.json'
    ]

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_list_view_filtered_by_rating(self):
        """Try and read the view of a recipe"""
        ratings_view = ratings_views.RatingCountViewSet.as_view()
        recipe_view = recipe_views.RecipeViewSet.as_view({'get': 'list'})

        request = self.factory.get(
            'https://fraspberry.dedyn.io/ownrecipes-api/api/v1/rating/rating-count/')
        response = ratings_view(request)
        recipe_count_dict = {}
        for item in response.data.get('results'):
            recipe_count_dict[item.get('rating')] = item.get('total')
        self.assertEqual(recipe_count_dict[0], 29)
        self.assertEqual(recipe_count_dict[1], 0)
        self.assertEqual(recipe_count_dict[2], 1)
        self.assertEqual(recipe_count_dict[3], 1)
        self.assertEqual(recipe_count_dict[4], 0)
        self.assertEqual(recipe_count_dict[5], 0)

        # unfiltered / all recipes
        request = self.factory.get(
            '/api/v1/recipe/recipes/?fields=id,slug,title,pub_date,rating,photo_thumbnail,info')
        response = recipe_view(request)
        self.assertEqual(len(response.data.get('results')), 31, "unfiltered")

        # filter by recipe = 0
        request = self.factory.get(
            '/api/v1/recipe/recipes/?fields=id,slug,title,pub_date,rating,photo_thumbnail,info&ordering=-rating&rating=0')
        response = recipe_view(request)
        self.assertEqual(len(response.data.get('results')), 29, "rating=0")

        # filter by recipe = 1
        request = self.factory.get(
            '/api/v1/recipe/recipes/?fields=id,slug,title,pub_date,rating,photo_thumbnail,info&ordering=-rating&rating=1')
        response = recipe_view(request)
        self.assertEqual(len(response.data.get('results')), 0, "rating=1")

        # filter by recipe = 2
        request = self.factory.get(
            '/api/v1/recipe/recipes/?fields=id,slug,title,pub_date,rating,photo_thumbnail,info&ordering=-rating&rating=2')
        response = recipe_view(request)
        self.assertEqual(len(response.data.get('results')), 1, "rating=2")

        # filter by recipe = 3
        request = self.factory.get(
            '/api/v1/recipe/recipes/?fields=id,slug,title,pub_date,rating,photo_thumbnail,info&ordering=-rating&rating=3')
        response = recipe_view(request)
        self.assertEqual(len(response.data.get('results')), 1, "rating=3")

        # filter by recipe = 4
        request = self.factory.get(
            '/api/v1/recipe/recipes/?fields=id,slug,title,pub_date,rating,photo_thumbnail,info&ordering=-rating&rating=4')
        response = recipe_view(request)
        self.assertEqual(len(response.data.get('results')), 0, "rating=4")

        # filter by recipe = 5
        request = self.factory.get(
            '/api/v1/recipe/recipes/?fields=id,slug,title,pub_date,rating,photo_thumbnail,info&ordering=-rating&rating=5')
        response = recipe_view(request)
        self.assertEqual(len(response.data.get('results')), 0, "rating=5")

        # filter by recipe = 2, 3 (get recipes with 0 and recipes with 3 stars)
        request = self.factory.get(
            '/api/v1/recipe/recipes/?fields=id,slug,title,pub_date,rating,photo_thumbnail,info&ordering=-rating&rating=2,3')
        response = recipe_view(request)
        self.assertEqual(len(response.data.get('results')), 2, "rating=2,3")

        # all filtered in / all recipes
        request = self.factory.get(
            '/api/v1/recipe/recipes/?fields=id,slug,title,pub_date,rating,photo_thumbnail,info&ordering=-rating&rating=0,1,2,3,4,5')
        response = recipe_view(request)
        self.assertEqual(len(response.data.get('results')), 31, "rating=0,1,2,3,4,5")
