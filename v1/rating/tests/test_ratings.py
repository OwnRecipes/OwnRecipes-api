# #!/usr/bin/env python
# # encoding: utf-8

from django.contrib.auth.models import User
from django.test import TestCase


class RatingsSerializerTests(TestCase):
    fixtures = ['test/users.json', 'course_data.json', 'cuisine_data.json', 'season_data.json', 'recipe_data.json']

    def setUp(self):
        # create user / author
        user = User.objects.create(username='testuser')
        user.set_password('12345')
        user.save()

        self.client.login(username='testuser', password='12345')
        self.user_id = getattr(user, 'id')
        self.user_name = getattr(user, 'username')

    def test_create_rating(self):
        new_rating_data = {"recipe": "tasty-chili",
                           "comment": "test_rating test_create_rating äöüÄÖÜ@€", "rating": 3}

        # rating post request
        response = self.client.post('/api/v1/rating/rating/', new_rating_data)
        self.assertEqual(response.status_code, 201)
        inserted_rating_id = response.data['id']

        # rating get request
        response = self.client.get('/api/v1/rating/rating/' + str(inserted_rating_id) + '/', {})
        self.assertEqual(response.status_code, 200)
        retrieved_rating_data = response.json()
        self.assertEqual(retrieved_rating_data['id'], inserted_rating_id)
        self.assertEqual(retrieved_rating_data['recipe'], new_rating_data['recipe'])
        self.assertEqual(retrieved_rating_data['comment'], new_rating_data['comment'])
        self.assertEqual(retrieved_rating_data['rating'], new_rating_data['rating'])
        self.assertEqual(retrieved_rating_data['author'], self.user_id)
        self.assertEqual(retrieved_rating_data['pub_username'], self.user_name)
        self.assertIsNotNone(retrieved_rating_data['pub_date'])
        self.assertIsNotNone(retrieved_rating_data['update_date'])
        recipe_slug = retrieved_rating_data['recipe']

        # recipe get request
        response = self.client.get('/api/v1/recipe/recipes/' + recipe_slug + "/", {})
        self.assertEqual(response.status_code, 200)
        retrieved_recipe_data = response.json()
        self.assertEqual(retrieved_recipe_data['slug'], new_rating_data['recipe'])

    def test_update_rating(self):
        new_rating_data = {"recipe": "tasty-chili",
                           "comment": "test_rating test_update_rating äöüÄÖÜ@€", "rating": 3}

        # rating post request
        response = self.client.post('/api/v1/rating/rating/', new_rating_data)
        self.assertEqual(response.status_code, 201)
        inserted_rating_id = response.data['id']

        # rating get request
        response = self.client.get('/api/v1/rating/rating/' + str(inserted_rating_id) + '/', {})
        self.assertEqual(response.status_code, 200)
        retrieved_rating_data = response.json()
        self.assertEqual(retrieved_rating_data['id'], inserted_rating_id)

        # rating put request
        user2 = User.objects.create(username='testuserr2', is_superuser=True, is_staff=True)
        user2.set_password('12346')
        user2.save()

        self.client.login(username='testuserr2', password='12346')
        user2_id = getattr(user2, 'id')

        update_rating_data = {"recipe": "tasty-chili",
                              "comment": "test_rating test_update_rating äöüÄÖÜ@€ UPDATED", "rating": 4}

        response = self.client.put('/api/v1/rating/rating/' + str(inserted_rating_id) + '/',
                                   update_rating_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # rating get request
        response = self.client.get('/api/v1/rating/rating/' + str(inserted_rating_id) + '/', {})
        self.assertEqual(response.status_code, 200)
        retrieved_rating_data = response.json()
        self.assertEqual(retrieved_rating_data['id'], inserted_rating_id)
        self.assertEqual(retrieved_rating_data['recipe'], update_rating_data['recipe'])
        self.assertEqual(retrieved_rating_data['comment'], update_rating_data['comment'])
        self.assertEqual(retrieved_rating_data['author'], self.user_id)
        self.assertEqual(retrieved_rating_data['update_author'], user2_id)
        self.assertEqual(retrieved_rating_data['rating'], update_rating_data['rating'])

    def test_delete_rating(self):
        new_rating_data = {"recipe": "tasty-chili",
                           "comment": "test_rating test_delete_rating äöüÄÖÜ@€", "rating": 3}

        # rating post request
        response = self.client.post('/api/v1/rating/rating/', new_rating_data)
        self.assertEqual(response.status_code, 201)
        inserted_rating_id = response.data['id']

        # rating get request
        response = self.client.get('/api/v1/rating/rating/' + str(inserted_rating_id) + '/', {})
        self.assertEqual(response.status_code, 200)
        retrieved_rating_data = response.json()
        self.assertEqual(retrieved_rating_data['id'], inserted_rating_id)
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
        self.assertEqual(retrieved_recipe_data['slug'], new_rating_data['recipe'])
