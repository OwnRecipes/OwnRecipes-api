#!/usr/bin/env python
# encoding: utf-8

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from v1.recipe_groups import views


class RecipeGroupsTests(TestCase):
    fixtures = [
        'test/users.json',
        'course_data.json',
        'cuisine_data.json',
        'season_data.json',
        'tag_data.json',
        'recipe_data.json'
    ]

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_course_all(self):
        view = views.CourseCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/course-count/')
        response = view(request)

        self.assertEqual(response.data.get('count'), 1)

        results = response.data.get('results')
        totals = {"entry": 31}

        for item in results:
            self.assertEqual(totals[item.get('slug')], item.get('total'))

    def test_cuisine_all(self):
        view = views.CuisineCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/cuisine-count/')
        response = view(request)

        self.assertEqual(response.data.get('count'), 1)

        results = response.data.get('results')
        totals = {"american": 31}

        for item in results:
            self.assertEqual(totals[item.get('slug')], item.get('total'))

    def test_season_all(self):
        view = views.SeasonCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/season-count/')
        response = view(request)

        self.assertEqual(response.data.get('count'), 4)

        results = response.data.get('results')
        totals = {"spring": 6, "summer": 4, "autumn": 4, "winter": 3}

        for item in results:
            self.assertEqual(totals[item.get('slug')], item.get('total'))

    def test_tag_all(self):
        view = views.TagCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/tag-count/')
        response = view(request)

        self.assertEqual(response.data.get('count'), 4)

        results = response.data.get('results')
        totals = {"easy": 4, "gluten-free": 2, "milk-free": 2, "nut-free": 1}

        for item in results:
            self.assertEqual(totals[item.get('slug')], item.get('total'))

    def test_course_with_filters(self):
        view = views.CourseCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/course-count/?cuisine=american')
        response = view(request)

        self.assertEqual(response.data.get('count'), 1)

        results = response.data.get('results')
        totals = {"entry": 31}

        for item in results:
            self.assertEqual(totals[item.get('slug')], item.get('total'))

    def test_course_with_tag_filter(self):
        view = views.CourseCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/course-count/?cuisine=american&tag=easy')
        response = view(request)

        self.assertEqual(response.data.get('count'), 1)

        results = response.data.get('results')
        totals = {"entry": 4}

        for item in results:
            self.assertEqual(totals[item.get('slug')], item.get('total'))

    def test_course_with_cuisine_filter_no_results(self):
        view = views.CourseCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/course-count/?cuisine=snack&rating=0')
        response = view(request)

        self.assertEqual(response.data.get('count'), 0)

    def test_course_with_non_existent_cuisine(self):
        view = views.CourseCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/course-count/?cuisine=non-existent')
        response = view(request)

        self.assertEqual(response.data.get('count'), 0)

    def test_cuisine_with_filters(self):
        view = views.CuisineCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/cuisine-count/?course=entry')
        response = view(request)

        self.assertEqual(response.data.get('count'), 1)

        results = response.data.get('results')
        totals = {"american": 31}

        for item in results:
            self.assertEqual(totals[item.get('slug')], item.get('total'))

    def test_cuisine_with_course_filter_no_results(self):
        view = views.CuisineCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/cuisine-count/?course=snack&rating=0')
        response = view(request)

        self.assertEqual(response.data.get('count'), 0)

    def test_cuisine_with_tag_filter(self):
        view = views.CuisineCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/cuisine-count/?course=entry&tag=easy')
        response = view(request)

        self.assertEqual(response.data.get('count'), 1)

        results = response.data.get('results')
        totals = {"american": 4}

        for item in results:
            self.assertEqual(totals[item.get('slug')], item.get('total'))

    def test_cuisine_with_non_existent_course(self):
        view = views.CuisineCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/cuisine-count/?course=non-existent')
        response = view(request)

        self.assertEqual(response.data.get('count'), 0)

    def test_cuisine_with_non_existent_tag(self):
        view = views.CuisineCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/cuisine-count/?tag=non-existent')
        response = view(request)

        self.assertEqual(response.data.get('count'), 0)

    def test_season_with_filters(self):
        view = views.SeasonCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/season-count/?cuisine=american')
        response = view(request)

        self.assertEqual(response.data.get('count'), 4)

        results = response.data.get('results')
        totals = {"spring": 6, "summer": 4, "autumn": 4, "winter": 3}

        for item in results:
            self.assertEqual(totals[item.get('slug')], item.get('total'))

    def test_season_with_tag_filter(self):
        view = views.SeasonCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/season-count/?cuisine=american&tag=easy')
        response = view(request)

        self.assertEqual(response.data.get('count'), 3)

        results = response.data.get('results')
        totals = {"spring": 3, "summer": 1, "autumn": 1}

        for item in results:
            self.assertEqual(totals[item.get('slug')], item.get('total'))

    def test_season_with_cuisine_filter_no_results(self):
        view = views.SeasonCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/season-count/?cuisine=snack&rating=0')
        response = view(request)

        self.assertEqual(response.data.get('count'), 0)

    def test_season_with_non_existent_cuisine(self):
        view = views.SeasonCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/season-count/?cuisine=non-existent')
        response = view(request)

        self.assertEqual(response.data.get('count'), 0)

    def test_tag_with_filters(self):
        view = views.TagCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/tag-count/?course=entry')
        response = view(request)

        self.assertEqual(response.data.get('count'), 4)

        results = response.data.get('results')
        totals = {"easy": 4, "gluten-free": 2, "milk-free": 2, "nut-free": 1}

        for item in results:
            self.assertEqual(totals[item.get('slug')], item.get('total'))

    def test_tag_with_course_filter_no_results(self):
        view = views.TagCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/tag-count/?course=snack&rating=0')
        response = view(request)

        self.assertEqual(response.data.get('count'), 0)

    def test_tag_with_non_existent_course(self):
        view = views.TagCountViewSet.as_view({'get': 'list'})
        request = self.factory.get('/api/v1/recipe_groups/tag-count/?course=non-existent')
        response = view(request)

        self.assertEqual(response.data.get('count'), 0)
