#!/usr/bin/env python
# encoding: utf-8
import shutil
from pathlib import Path

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
            "directions": 'test',
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
            "directions": 'test',
            "tags": [{'title': 'hi'}, {'title': 'hello'}],
            "title": "Recipe name",
            "info": "Recipe info rgo",
            "source": "google.com",
            "prep_time": 60,
            "cook_time": 60,
            "servings": 8,
            "rating": 0,
            "cuisine": {"id": 1},
            "course": {"id": 2},
            "photo": "upload/recipe_photos/food.jpg"
        }

        data_new_file = {
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
            "directions": 'test',
            "tags": [{'title': 'hi'}, {'title': 'hello'}],
            "title": "Recipe name",
            "info": "Recipe info rgo",
            "source": "google.com",
            "prep_time": 60,
            "cook_time": 60,
            "servings": 8,
            "rating": 0,
            "cuisine": {"id": 1},
            "course": {"id": 2},
            "photo": "upload/recipe_photos/food2.jpg"
        }

        # add data with photo url
        request = self.factory.patch('/api/v1/recipe/recipes/tasty-chili', data=data, format='json')
        # print(request)
        request.user = self.staff
        response = view(request, slug='tasty-chili')
        self.assertEqual(response.data.get('info'), 'Recipe info rgo')
        self.assertTrue(response.data.get('photo').endswith("upload/recipe_photos/food.jpg"))
        # copy file
        shutil.copy2('v1/fixtures/test/food.jpg', 'site-media/upload/recipe_photos')

        # check if copying file succeeded
        my_file = Path("site-media/upload/recipe_photos/food.jpg")
        self.assertTrue(my_file.is_file(), "File not found")

        # patch recipe and check if the file has been replaced
        request = self.factory.patch('/api/v1/recipe/recipes/tasty-chili', data=data_new_file, format='json')
        # print(request)
        request.user = self.staff
        response = view(request, slug='tasty-chili')
        self.assertEqual(response.data.get('info'), 'Recipe info rgo')
        self.assertTrue(response.data.get('photo').endswith("upload/recipe_photos/food2.jpg"))

        # photo is deleted on file system?
        my_file = Path("site-media/upload/recipe_photos/food.jpg")
        self.assertFalse(my_file.is_file(), "Deleting File failed")


