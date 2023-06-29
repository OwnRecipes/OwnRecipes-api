#!/usr/bin/env python
# encoding: utf-8

import os
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from rest_framework.test import APIRequestFactory
from v1.recipe import views


class RecipeSerializerTests(TestCase):
    fixtures = [
        'test/users.json',
        'course_data.json',
        'cuisine_data.json',
        'tag_data.json',
    ]

    def setUp(self):
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        self.client.login(username='testuser', password='12345')
        self.user_id = getattr(user, 'id')
        self.user_name = getattr(user, 'username')
        self.factory = APIRequestFactory()
        self.staff = User.objects.create_user(
            username='staff', email='staff@gmail.com', password='top_secret', is_superuser=True
        )
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

    def test_simple_create_recipe(self):
        """Test to make sure we have the right fields"""
        view = views.RecipeViewSet.as_view({'post': 'create'})

        request = self.factory.post('/api/v1/recipe/recipes/', data=self.data, format='json')
        request.user = self.staff

        root_path = os.path.join(settings.PROJECT_PATH, 'v1', 'fixtures', 'test', 'food.jpg')
        with open(root_path, 'rb') as f:
            request.FILES['photo'] = SimpleUploadedFile(
                root_path,
                f.read(),
                content_type='multipart/form-data'
            )
        response = view(request)

        self.assertTrue(response.data.get('id', True))

    def test_create_recipe_too_long_name(self):
        self.data['title'] = "Recipe name Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium."
        response = self.client.post('/api/v1/recipe/recipes/', self.data, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertTrue("Ensure this value has at most 250 characters" in str(response.data))
