# #!/usr/bin/env python
# # encoding: utf-8

from datetime import datetime
from django.contrib.auth.models import User
from django.test import TestCase


class RatingsSerializerTests(TestCase):
    fixtures = ['test/users.json', 'course_data.json', 'cuisine_data.json', 'recipe_data.json']

    def setUp(self):
        # create user / author
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()
        logged_in = self.client.login(username='testuser', password='12345')
        self.user_id = getattr(user, 'id')
        self.user_name = getattr(user, 'username')

    def test_create_rating(self):
        new_rating_data = {"recipe": "tasty-chili", "author": self.user_id,
                           "comment": "test_rating test_create_rating äöüÄÖÜ@€", "rating": 3}

        # rating post request
        response = self.client.post('/api/v1/rating/rating/', new_rating_data)
        self.assertEqual(response.status_code, 201)
        inserted_rating_id = response.data['id']

        # rating get request
        response = self.client.get('/api/v1/rating/rating/' + str(inserted_rating_id) + '/', {})
        self.assertEqual(response.status_code, 200)
        retrieved_rating_data = response.json()
        self.assertEquals(retrieved_rating_data['id'], inserted_rating_id)
        self.assertEquals(retrieved_rating_data['recipe'], new_rating_data['recipe'])
        self.assertEquals(retrieved_rating_data['comment'], new_rating_data['comment'])
        self.assertEquals(retrieved_rating_data['author'], new_rating_data['author'])
        self.assertEquals(retrieved_rating_data['rating'], new_rating_data['rating'])
        self.assertEquals(retrieved_rating_data['username'], self.user_name)
        now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        self.assertEquals(retrieved_rating_data['pub_date'], now)
        self.assertEquals(retrieved_rating_data['update_date'], now)
        recipe_slug = retrieved_rating_data['recipe']

        # recipe get request
        response = self.client.get('/api/v1/recipe/recipes/' + recipe_slug + "/", {})
        self.assertEqual(response.status_code, 200)
        retrieved_recipe_data = response.json()
        self.assertEquals(retrieved_recipe_data['slug'], new_rating_data['recipe'])

    def test_update_rating(self):
        new_rating_data = {"recipe": "tasty-chili", "author": self.user_id,
                           "comment": "test_rating test_update_rating äöüÄÖÜ@€", "rating": 3}

        # rating post request
        response = self.client.post('/api/v1/rating/rating/', new_rating_data)
        self.assertEqual(response.status_code, 201)
        inserted_rating_id = response.data['id']

        # rating get request
        response = self.client.get('/api/v1/rating/rating/' + str(inserted_rating_id) + '/', {})
        self.assertEqual(response.status_code, 200)
        retrieved_rating_data = response.json()
        self.assertEquals(retrieved_rating_data['id'], inserted_rating_id)
        recipe_slug = retrieved_rating_data['recipe']

        # rating put request
        update_rating_data = {"recipe": "tasty-chili", "author": self.user_id,
                              "comment": "test_rating test_update_rating äöüÄÖÜ@€ UPDATED", "rating": 4}

        response = self.client.put('/api/v1/rating/rating/' + str(inserted_rating_id) + '/',
                                   update_rating_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # rating get request
        response = self.client.get('/api/v1/rating/rating/' + str(inserted_rating_id) + '/', {})
        self.assertEqual(response.status_code, 200)
        retrieved_rating_data = response.json()
        self.assertEquals(retrieved_rating_data['id'], inserted_rating_id)
        self.assertEquals(retrieved_rating_data['recipe'], update_rating_data['recipe'])
        self.assertEquals(retrieved_rating_data['comment'], update_rating_data['comment'])
        self.assertEquals(retrieved_rating_data['author'], update_rating_data['author'])
        self.assertEquals(retrieved_rating_data['rating'], update_rating_data['rating'])

    def test_delete_rating(self):
        new_rating_data = {"recipe": "tasty-chili", "author": self.user_id,
                           "comment": "test_rating test_delete_rating äöüÄÖÜ@€", "rating": 3}

        # rating post request
        response = self.client.post('/api/v1/rating/rating/', new_rating_data)
        self.assertEqual(response.status_code, 201)
        inserted_rating_id = response.data['id']

        # rating get request
        response = self.client.get('/api/v1/rating/rating/' + str(inserted_rating_id) + '/', {})
        self.assertEqual(response.status_code, 200)
        retrieved_rating_data = response.json()
        self.assertEquals(retrieved_rating_data['id'], inserted_rating_id)
        recipe_slug = retrieved_rating_data['recipe']

        # rating delete request
        response = self.client.delete('/api/v1/rating/rating/' + str(inserted_rating_id) + '/', {})
        self.assertEqual(response.status_code, 204)

        # rating get request
        response = self.client.get('/api/v1/rating/rating/' + str(inserted_rating_id) + '/', {})
        self.assertEqual(response.status_code, 404)

        # recipe get request
        response = self.client.get('/api/v1/recipe/recipes/' + recipe_slug + "/", {})
        self.assertEqual(response.status_code, 200)
        retrieved_recipe_data = response.json()
        self.assertEquals(retrieved_recipe_data['slug'], new_rating_data['recipe'])
