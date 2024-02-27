import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

import api.error_message as error
from api.models import User


class FriendsTest(TestCase):
    @patch('common.src.jwt_managers.ServiceAccessJWT.authenticate')
    def post_friends(self, user_id, increment, mock_post):
        mock_post.return_value = (True, None)
        url = reverse('user_friends', kwargs={'user_id': user_id})
        body = {
            'increment': increment
        }
        return self.client.post(url, json.dumps(body), content_type='application/json')


class PostProgress(FriendsTest):
    def setUp(self):
        User.objects.create(
            id=1,
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_valid_increment(self):
        response = self.post_friends(1, True)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['new_entry']['count'], 1)
        user = User.objects.get(pk=1)
        self.assertEqual(user.friends, 1)
        response = self.post_friends(1, False)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['new_entry']['count'], 0)
        user = User.objects.get(pk=1)
        self.assertEqual(user.friends, 0)

    def test_invalid_negative(self):
        response = self.post_friends(1, False)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.FRIENDS_NEGATIVE])

    def test_invalid_increment(self):
        response = self.post_friends(1, None)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.INCREMENT_REQUIRED])
        response = self.post_friends(1, 'true')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.INCREMENT_INVALID])
        response = self.post_friends(1, 'false')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.INCREMENT_INVALID])
        response = self.post_friends(1, 1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.INCREMENT_INVALID])
        response = self.post_friends(1, 0)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.INCREMENT_INVALID])
        response = self.post_friends(1, '1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.INCREMENT_INVALID])
        response = self.post_friends(1, '0')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.INCREMENT_INVALID])
        response = self.post_friends(1, 'True')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.INCREMENT_INVALID])
        response = self.post_friends(1, 'False')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.INCREMENT_INVALID])
        response = self.post_friends(1, 'True')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.INCREMENT_INVALID])
        response = self.post_friends(1, 'False')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.INCREMENT_INVALID])
        response = self.post_friends(1, 'True')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.INCREMENT_INVALID])
        response = self.post_friends(1, 'False')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.INCREMENT_INVALID])
        response = self.post_friends(1, 'True')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.INCREMENT_INVALID])
        response = self.post_friends(1, 'False')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.INCREMENT_INVALID])
        response = self.post_friends(1, 'True')
        self.assertEqual(response.status_code, 400)

    def test_invalid_user_id(self):
        response = self.post_friends(2, True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.USER_NOT_FOUND])
