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
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        self.client.login(username='testuser', password='12345')
        self.user_id = getattr(user, 'id')
        self.user_name = getattr(user, 'username')
        self.data = {
            "ingredient_groups": [
                {
                    "id": 3,
                    "title": "",
                    "ingredients": []
                },
                {
                    "id": 4,
                    "title": "Veges",
                    "ingredients": [
                        {
                            "id": 13,
                            "numerator": 1.0,
                            "denominator": 2.0,
                            "measurement": "dash",
                            "title": "black pepper"
                        },
                        {
                            "id": 14,
                            "numerator": 4.0,
                            "denominator": 1.0,
                            "measurement": "tablespoons",
                            "title": "chili powder"
                        },
                        {
                            "id": 15,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "tablespoon",
                            "title": "cumin"
                        },
                        {
                            "id": 16,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "can",
                            "title": "dark kidney beans"
                        },
                        {
                            "id": 17,
                            "numerator": 2.0,
                            "denominator": 1.0,
                            "measurement": "cans",
                            "title": "diced tomatos"
                        },
                        {
                            "id": 18,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "whole",
                            "title": "green bell pepper"
                        },
                        {
                            "id": 19,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "can",
                            "title": "light kidney beans"
                        },
                        {
                            "id": 20,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "whole",
                            "title": "serrano pepper"
                        },
                        {
                            "id": 21,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "whole",
                            "title": "white onion"
                        }
                    ]
                },
                {
                    "id": 5,
                    "title": "Beef",
                    "ingredients": [
                        {
                            "id": 22,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "pound",
                            "title": "ground pork"
                        },
                        {
                            "id": 23,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "pound",
                            "title": "ground sirloin"
                        },
                        {
                            "id": 24,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "dash",
                            "title": "kosher salt"
                        }
                    ]
                }
            ],
            "directions": '',
            "tags": [{'title': 'hi'}, {'title': 'hello'}],
            "title": "Recipe name",
            "info": "Recipe info",
            "source": "google.com",
            "prep_time": 60,
            "cook_time": 60,
            "servings": 8,
            "rating": 0,
            "cuisine": {"id": 1},
            "course": {"id": 2}
        }

    def test_simple_patch_recipe(self):
        """Test to make sure we have the right fields"""
        view = views.RecipeViewSet.as_view({'patch': 'update'})
        data = {
            "ingredient_groups": [
                {
                    "id": 3,
                    "title": "",
                    "ingredients": []
                },
                {
                    "id": 4,
                    "title": "Veges",
                    "ingredients": [
                        {
                            "id": 13,
                            "numerator": 1.0,
                            "denominator": 2.0,
                            "measurement": "dash",
                            "title": "black pepper"
                        },
                        {
                            "id": 14,
                            "numerator": 4.0,
                            "denominator": 1.0,
                            "measurement": "tablespoons",
                            "title": "chili powder"
                        },
                        {
                            "id": 15,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "tablespoon",
                            "title": "cumin"
                        },
                        {
                            "id": 16,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "can",
                            "title": "dark kidney beans"
                        },
                        {
                            "id": 17,
                            "numerator": 2.0,
                            "denominator": 1.0,
                            "measurement": "cans",
                            "title": "diced tomatos"
                        },
                        {
                            "id": 18,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "whole",
                            "title": "green bell pepper"
                        },
                        {
                            "id": 19,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "can",
                            "title": "light kidney beans"
                        },
                        {
                            "id": 20,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "whole",
                            "title": "serrano pepper"
                        },
                        {
                            "id": 21,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "whole",
                            "title": "white onion"
                        }
                    ]
                },
                {
                    "id": 5,
                    "title": "Beef",
                    "ingredients": [
                        {
                            "id": 22,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "pound",
                            "title": "ground pork"
                        },
                        {
                            "id": 23,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "pound",
                            "title": "ground sirloin"
                        },
                        {
                            "id": 24,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "dash",
                            "title": "kosher salt"
                        }
                    ]
                }
            ],
            "directions": '',
            "tags": [{'title': 'hi'}, {'title': 'hello'}],
            "title": "Recipe name",
            "info": "Recipe info",
            "source": "google.com",
            "prep_time": 60,
            "cook_time": 60,
            "servings": 8,
            "rating": 0,
            "cuisine": {"id": 1},
            "course": {"id": 2}
        }
        request = self.factory.patch('/api/v1/recipe/recipes/tasty-chili', data=data, format='json')
        request.user = self.staff
        response = view(request, slug='tasty-chili')

        self.assertTrue(response.data.get('id', True))

    def test_put_recipe(self):
        """Test to make sure we have the right fields"""
        view = views.RecipeViewSet.as_view({'put': 'update'})
        data = {
            "ingredient_groups": [
                {
                    "id": 3,
                    "title": "",
                    "ingredients": []
                },
                {
                    "id": 4,
                    "title": "Veges",
                    "ingredients": [
                        {
                            "id": 13,
                            "numerator": 1.0,
                            "denominator": 2.0,
                            "measurement": "dash",
                            "title": "black pepper"
                        },
                        {
                            "id": 14,
                            "numerator": 4.0,
                            "denominator": 1.0,
                            "measurement": "tablespoons",
                            "title": "chili powder"
                        },
                        {
                            "id": 15,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "tablespoon",
                            "title": "cumin"
                        },
                        {
                            "id": 16,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "can",
                            "title": "dark kidney beans"
                        },
                        {
                            "id": 17,
                            "numerator": 2.0,
                            "denominator": 1.0,
                            "measurement": "cans",
                            "title": "diced tomatos"
                        },
                        {
                            "id": 18,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "whole",
                            "title": "green bell pepper"
                        },
                        {
                            "id": 19,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "can",
                            "title": "light kidney beans"
                        },
                        {
                            "id": 20,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "whole",
                            "title": "serrano pepper"
                        },
                        {
                            "id": 21,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "whole",
                            "title": "white onion"
                        }
                    ]
                },
                {
                    "id": 5,
                    "title": "Beef",
                    "ingredients": [
                        {
                            "id": 22,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "pound",
                            "title": "ground pork"
                        },
                        {
                            "id": 23,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "pound",
                            "title": "ground sirloin"
                        },
                        {
                            "id": 24,
                            "numerator": 1.0,
                            "denominator": 1.0,
                            "measurement": "dash",
                            "title": "kosher salt"
                        }
                    ]
                }
            ],
            "directions": '',
            "tags": [{'title': 'hi'}, {'title': 'hello'}],
            "title": "Recipe name",
            "info": "Recipe info",
            "source": "google.com",
            "prep_time": 60,
            "cook_time": 60,
            "servings": 8,
            "rating": 0,
            "cuisine": {"id": 1},
            "course": {"id": 2}
        }
        request = self.factory.put('/api/v1/recipe/recipes/tasty-chili', data=data, format='json')
        request.user = self.staff
        response = view(request, slug='tasty-chili')

        self.assertTrue(response.data.get('id', True))

    def test_patch_recipe_with_photo(self):
        """Test that orphan photos are deleted"""
        PHOTO_PATH = os.path.join('upload', 'recipe_photos')
        media_path = os.path.join(settings.MEDIA_ROOT, PHOTO_PATH)
        if not os.path.exists(media_path):
            os.makedirs(os.path.dirname(media_path))

        view = views.RecipeViewSet.as_view({'patch': 'update'})
        data = {
            "ingredient_groups": [
                {
                    "id": 3,
                    "title": "",
                    "ingredients": []
                }
            ],
            "directions": 'test',
            "title": "Recipe name",
            "info": "Recipe info rgo",
            "source": "google.com",
            "prep_time": 60,
            "cook_time": 60,
            "servings": 8,
            "cuisine": {"id": 1},
            "course": {"id": 2},
            "photo": os.path.join(PHOTO_PATH, 'food.jpg')
        }

        data_new_file = {
            "ingredient_groups": [
                {
                    "id": 3,
                    "title": "",
                    "ingredients": []
                }
            ],
            "directions": 'test',
            "title": "Recipe name",
            "info": "Recipe info rgo",
            "source": "google.com",
            "prep_time": 60,
            "cook_time": 60,
            "servings": 8,
            "cuisine": {"id": 1},
            "course": {"id": 2},
            "photo": os.path.join(PHOTO_PATH, 'food2.jpg')
        }

        # add data with photo url
        request = self.factory.patch('/api/v1/recipe/recipes/tasty-chili', data=data, format='json')
        # print(request)
        request.user = self.staff
        response = view(request, slug='tasty-chili')
        self.assertEqual(response.data.get('info'), 'Recipe info rgo')
        self.assertTrue(response.data.get('photo').endswith(os.path.join(PHOTO_PATH, 'food.jpg')))
        # copy file
        shutil.copy2('v1/fixtures/test/food.jpg', media_path)

        # check if copying file succeeded
        my_file = Path(media_path, 'food.jpg')
        self.assertTrue(my_file.is_file(), 'File not found')

        # patch recipe and check if the file has been replaced
        request = self.factory.patch('/api/v1/recipe/recipes/tasty-chili', data=data_new_file, format='json')
        # print(request)
        request.user = self.staff
        response = view(request, slug='tasty-chili')
        self.assertEqual(response.data.get('info'), 'Recipe info rgo')
        self.assertTrue(response.data.get('photo').endswith(os.path.join(PHOTO_PATH, 'food2.jpg')))

        # photo should be deleted
        my_file = Path(media_path, 'food.jpg')
        self.assertFalse(my_file.is_file(), 'Deleting File failed')

    def test_update_recipe_too_long_name(self):
        view = views.RecipeViewSet.as_view({'put': 'update'})
        self.data['title'] = "Recipe name Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium."
        request = self.factory.put('/api/v1/recipe/recipes/tasty-chili', data=self.data, format='json')
        request.user = self.staff
        response = view(request, slug='tasty-chili')
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Ensure this value has at most 250 characters" in str(response.data))
