#!/usr/bin/env python
# encoding: utf-8

import os
import shutil
from pathlib import Path

from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from v1.recipe import views
from v1.recipe.models import Recipe


class RecipeSerializerTests(TestCase):
    fixtures = [
        'test/users.json',
        'course_data.json',
        'cuisine_data.json',
        'tag_data.json',
        'ing_data.json',
        'recipe_data.json'
    ]

    def setUp(self):
        self.factory = APIRequestFactory()
        self.staff = User.objects.create_user(
            username='staff', email='staff@gmail.com', password='top_secret', is_superuser=True
        )

    def test_simple_delete_recipe(self):
        """Test to make sure we have the right fields"""
        view = views.RecipeViewSet.as_view({ 'delete': 'destroy' })
        request = self.factory.delete('/api/v1/recipe/recipes/tasty-chili')
        request.user = self.staff
        response = view(request, slug='tasty-chili')

        self.assertEqual(response.status_code, 204)

    def test_simple_delete_recipe_with_photo(self):
        """Test that orphan photos are deleted"""
        PHOTO_PATH = os.path.join('upload', 'recipe_photos')
        media_path = os.path.join(settings.MEDIA_ROOT, PHOTO_PATH)
        if not os.path.exists(media_path):
            os.makedirs(os.path.dirname(media_path))

        # add photo
        recipe = Recipe.objects.get(slug='tasty-chili')
        recipe.photo = os.path.join(PHOTO_PATH, 'food.jpg')
        recipe.save()
        # copy file

        shutil.copy2('v1/fixtures/test/food.jpg', media_path)

        # photo should be saved on fs now
        my_file = Path(media_path, 'food.jpg')
        self.assertTrue(my_file.is_file(), 'File not found')

        # delete
        view = views.RecipeViewSet.as_view({ 'delete': 'destroy' })
        request = self.factory.delete('/api/v1/recipe/recipes/tasty-chili')
        request.user = self.staff
        response = view(request, slug='tasty-chili')
        self.assertEqual(response.status_code, 204)

        # photo should be deleted
        my_file = Path(media_path, '/food.jpg')
        self.assertFalse(my_file.is_file(), 'Deleting File failed')