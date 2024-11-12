#!/usr/bin/env python
# encoding: utf-8

from django.test import TestCase
from rest_framework import status

class AccountTests(TestCase):
    fixtures = ['test/users.json']

    def test_obtain_authtoken_success(self):
        """ Try and login and confirm that the login was successful """
        resp = self.client.post(
            '/api/v1/accounts/obtain-auth-token/',
            {
                'username': 'testuser1',
                'password': 'testpassword'
            }
        )

        self.assertEqual(resp.status_code, 200)
        self.assertTrue(bool(resp.json()['refresh']))

    def test_obtain_authtoken_wrong_password(self):
        """ Try and login and confirm that the login was unsuccessful """
        resp = self.client.post(
            '/api/v1/accounts/obtain-auth-token/',
            {
                'username': 'testuser1',
                'password': 'wrongpassword'
            }
        )

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
