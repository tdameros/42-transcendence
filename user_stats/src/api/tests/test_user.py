import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

import api.error_message as error
from api.models import User
from user_stats import settings


class UserTest(TestCase):
    def get_user(self, user_id: int):
        url = reverse('user', kwargs={'user_id': user_id})
        response = self.client.get(url)
        return response

    def post_user(self, user_id: int, body: dict):
        url = reverse('user', kwargs={'user_id': user_id})
        response = self.client.post(url, json.dumps(body), content_type='application/json')
        return response

    def patch_user(self, user_id: int, body: dict):
        url = reverse('user', kwargs={'user_id': user_id})
        response = self.client.patch(url, json.dumps(body), content_type='application/json')
        return response

    def delete_user(self, user_id: int):
        url = reverse('user', kwargs={'user_id': user_id})
        response = self.client.delete(url)
        return response

    def post_match(self, body: dict):
        url = reverse('match')
        response = self.client.post(url, json.dumps(body), content_type='application/json')
        return response

    def get_history(self, user_id: int, page=1, page_size=10):
        url = reverse('user_history', kwargs={'user_id': user_id})
        response = self.client.get(url, {'page': page, 'page_size': page_size})
        return response

    def assert_equal_user(self, user, response):
        body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(body['id'], user.id)
        self.assertEqual(body['elo'], user.elo)
        self.assertEqual(body['matches_played'], user.matches_played)
        self.assertEqual(body['matches_won'], user.matches_won)
        self.assertEqual(body['matches_lost'], user.matches_lost)
        self.assertEqual(body['win_rate'], user.win_rate)
        self.assertEqual(body['friends'], user.friends)

    def assert_invalid_response(self, user_id, request_body, errors):
        response = self.post_user(user_id, request_body)
        body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['errors'], errors)


class GetUserTest(UserTest):

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_default(self, mock_authenticate):
        user1 = User.objects.create(id=0)
        mock_authenticate.return_value = (True, {'id': 0}, None)
        response = self.get_user(user1.id)
        self.assertEqual(response.status_code, 200)
        self.assert_equal_user(user1, response)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_custom(self, mock_authenticate):
        user2 = User.objects.create(
            id=0,
            elo=1000,
            matches_played=10,
            matches_won=5,
            matches_lost=5,
            win_rate=0.5,
            friends=5
        )
        mock_authenticate.return_value = (True, {'id': 0}, None)
        response = self.get_user(user2.id)
        self.assertEqual(response.status_code, 200)
        self.assert_equal_user(user2, response)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_invalid_user_not_found(self, mock_authenticate):
        User.objects.create(id=0)
        mock_authenticate.return_value = (True, {'id': 0}, None)
        response = self.get_user(1)
        body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], [error.USER_NOT_FOUND])


class PostUserTest(UserTest):

    def test_valid_default(self):
        user_id = 1
        response = self.post_user(user_id, {})
        body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(body['elo'], settings.ELO_DEFAULT)
        self.assertEqual(body['matches_played'], settings.MATCHES_PLAYED_DEFAULT)
        self.assertEqual(body['matches_won'], settings.MATCHES_WON_DEFAULT)
        self.assertEqual(body['matches_lost'], settings.MATCHES_LOST_DEFAULT)
        self.assertEqual(body['win_rate'], settings.WIN_RATE_DEFAULT)
        self.assertEqual(body['friends'], settings.FRIENDS_DEFAULT)

    def test_valid_custom(self):
        user_id = 1
        request_body = {
            'elo': 1000,
            'matches_played': 10,
            'matches_won': 5,
            'matches_lost': 5,
            'win_rate': 0.5,
            'friends': 5
        }
        response = self.post_user(user_id, request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(response_body['elo'], request_body['elo'])
        self.assertEqual(response_body['matches_played'], request_body['matches_played'])
        self.assertEqual(response_body['matches_won'], request_body['matches_won'])
        self.assertEqual(response_body['matches_lost'], request_body['matches_lost'])
        self.assertEqual(response_body['win_rate'], request_body['win_rate'])
        self.assertEqual(response_body['friends'], request_body['friends'])

    def test_invalid_user_existing(self):
        User.objects.create(id=0)
        response = self.post_user(0, {})
        body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['errors'], [error.USER_EXISTING])

    def test_valid_elo(self):
        user_id = 0
        request_body = {'elo': 1000}
        response = self.post_user(user_id, request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(response_body['elo'], request_body['elo'])
        self.assertEqual(response_body['matches_played'], settings.MATCHES_PLAYED_DEFAULT)
        self.assertEqual(response_body['matches_won'], settings.MATCHES_WON_DEFAULT)
        self.assertEqual(response_body['matches_lost'], settings.MATCHES_LOST_DEFAULT)
        self.assertEqual(response_body['win_rate'], settings.WIN_RATE_DEFAULT)
        self.assertEqual(response_body['friends'], settings.FRIENDS_DEFAULT)

    def test_invalid_elo(self):
        request_body = {'elo': 'abc'}
        self.assert_invalid_response(0, request_body, [error.ELO_INVALID])
        request_body = {'elo': 1.1}
        self.assert_invalid_response(0, request_body, [error.ELO_INVALID])
        request_body = {'elo': [1]}
        self.assert_invalid_response(0, request_body, [error.ELO_INVALID])
        request_body = {'elo': {'elo': 1}}
        self.assert_invalid_response(0, request_body, [error.ELO_INVALID])
        request_body = {'elo': -1}
        self.assert_invalid_response(0, request_body, [error.ELO_INVALID])

    def test_valid_matches_played(self):
        user_id = 0
        request_body = {'matches_played': 1000}
        response = self.post_user(user_id, request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(response_body['elo'], settings.ELO_DEFAULT)
        self.assertEqual(response_body['matches_played'], request_body['matches_played'])
        self.assertEqual(response_body['matches_won'], settings.MATCHES_WON_DEFAULT)
        self.assertEqual(response_body['matches_lost'], settings.MATCHES_LOST_DEFAULT)
        self.assertEqual(response_body['win_rate'], settings.WIN_RATE_DEFAULT)
        self.assertEqual(response_body['friends'], settings.FRIENDS_DEFAULT)

    def test_invalid_matches_played(self):
        request_body = {'matches_played': 'abc'}
        self.assert_invalid_response(0, request_body, [error.MATCHES_PLAYED_INVALID])
        request_body = {'matches_played': 1.1}
        self.assert_invalid_response(0, request_body, [error.MATCHES_PLAYED_INVALID])
        request_body = {'matches_played': [1]}
        self.assert_invalid_response(0, request_body, [error.MATCHES_PLAYED_INVALID])
        request_body = {'matches_played': {'matches_played': 1}}
        self.assert_invalid_response(0, request_body, [error.MATCHES_PLAYED_INVALID])
        request_body = {'matches_played': -1}
        self.assert_invalid_response(0, request_body, [error.MATCHES_PLAYED_INVALID])

    def test_valid_matches_won(self):
        user_id = 0
        request_body = {'matches_won': 1000}
        response = self.post_user(user_id, request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(response_body['elo'], settings.ELO_DEFAULT)
        self.assertEqual(response_body['matches_played'], settings.MATCHES_PLAYED_DEFAULT)
        self.assertEqual(response_body['matches_won'], request_body['matches_won'])
        self.assertEqual(response_body['matches_lost'], settings.MATCHES_LOST_DEFAULT)
        self.assertEqual(response_body['win_rate'], settings.WIN_RATE_DEFAULT)
        self.assertEqual(response_body['friends'], settings.FRIENDS_DEFAULT)

    def test_invalid_matches_won(self):
        request_body = {'matches_won': 'abc'}
        self.assert_invalid_response(0, request_body, [error.MATCHES_WON_INVALID])
        request_body = {'matches_won': 1.1}
        self.assert_invalid_response(0, request_body, [error.MATCHES_WON_INVALID])
        request_body = {'matches_won': [1]}
        self.assert_invalid_response(0, request_body, [error.MATCHES_WON_INVALID])
        request_body = {'matches_won': {'matches_won': 1}}
        self.assert_invalid_response(0, request_body, [error.MATCHES_WON_INVALID])
        request_body = {'matches_won': -1}
        self.assert_invalid_response(0, request_body, [error.MATCHES_WON_INVALID])

    def test_valid_matches_lost(self):
        user_id = 0
        request_body = {'matches_lost': 1000}
        response = self.post_user(user_id, request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(response_body['elo'], settings.ELO_DEFAULT)
        self.assertEqual(response_body['matches_played'], settings.MATCHES_PLAYED_DEFAULT)
        self.assertEqual(response_body['matches_won'], settings.MATCHES_WON_DEFAULT)
        self.assertEqual(response_body['matches_lost'], request_body['matches_lost'])
        self.assertEqual(response_body['win_rate'], settings.WIN_RATE_DEFAULT)
        self.assertEqual(response_body['friends'], settings.FRIENDS_DEFAULT)

    def test_invalid_matches_lost(self):
        request_body = {'matches_lost': 'abc'}
        self.assert_invalid_response(0, request_body, [error.MATCHES_LOST_INVALID])
        request_body = {'matches_lost': 1.1}
        self.assert_invalid_response(0, request_body, [error.MATCHES_LOST_INVALID])
        request_body = {'matches_lost': [1]}
        self.assert_invalid_response(0, request_body, [error.MATCHES_LOST_INVALID])
        request_body = {'matches_lost': {'matches_lost': 1}}
        self.assert_invalid_response(0, request_body, [error.MATCHES_LOST_INVALID])
        request_body = {'matches_lost': -1}
        self.assert_invalid_response(0, request_body, [error.MATCHES_LOST_INVALID])

    def test_valid_win_rate(self):
        user_id = 0
        request_body = {'win_rate': 0.5}
        response = self.post_user(user_id, request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(response_body['elo'], settings.ELO_DEFAULT)
        self.assertEqual(response_body['matches_played'], settings.MATCHES_PLAYED_DEFAULT)
        self.assertEqual(response_body['matches_won'], settings.MATCHES_WON_DEFAULT)
        self.assertEqual(response_body['matches_lost'], settings.MATCHES_LOST_DEFAULT)
        self.assertEqual(response_body['win_rate'], request_body['win_rate'])
        self.assertEqual(response_body['friends'], settings.FRIENDS_DEFAULT)

    def test_valid_win_rate_boundary(self):
        user_id = 0
        request_body = {'win_rate': 1.0}
        response = self.post_user(user_id, request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(response_body['win_rate'], request_body['win_rate'])

        user_id = 1
        request_body = {'win_rate': 0.0}
        response = self.post_user(user_id, request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(response_body['win_rate'], request_body['win_rate'])

    def test_invalid_win_rate(self):
        request_body = {'win_rate': 'abc'}
        self.assert_invalid_response(0, request_body, [error.WIN_RATE_INVALID])
        request_body = {'win_rate': 0}
        self.assert_invalid_response(0, request_body, [error.WIN_RATE_INVALID])
        request_body = {'win_rate': [1]}
        self.assert_invalid_response(0, request_body, [error.WIN_RATE_INVALID])
        request_body = {'win_rate': {'win_rate': 1}}
        self.assert_invalid_response(0, request_body, [error.WIN_RATE_INVALID])
        request_body = {'win_rate': -1}
        self.assert_invalid_response(0, request_body, [error.WIN_RATE_INVALID])
        request_body = {'win_rate': 1.1}
        self.assert_invalid_response(0, request_body, [error.WIN_RATE_INVALID])

    def test_valid_friends(self):
        user_id = 0
        request_body = {'friends': 1000}
        response = self.post_user(user_id, request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(response_body['elo'], settings.ELO_DEFAULT)
        self.assertEqual(response_body['matches_played'], settings.MATCHES_PLAYED_DEFAULT)
        self.assertEqual(response_body['matches_won'], settings.MATCHES_WON_DEFAULT)
        self.assertEqual(response_body['matches_lost'], settings.MATCHES_LOST_DEFAULT)
        self.assertEqual(response_body['win_rate'], settings.WIN_RATE_DEFAULT)
        self.assertEqual(response_body['friends'], request_body['friends'])

    def test_invalid_friends(self):
        request_body = {'friends': 'abc'}
        self.assert_invalid_response(0, request_body, [error.FRIENDS_INVALID])
        request_body = {'friends': 1.1}
        self.assert_invalid_response(0, request_body, [error.FRIENDS_INVALID])
        request_body = {'friends': [1]}
        self.assert_invalid_response(0, request_body, [error.FRIENDS_INVALID])
        request_body = {'friends': {'friends': 1}}
        self.assert_invalid_response(0, request_body, [error.FRIENDS_INVALID])
        request_body = {'friends': -1}
        self.assert_invalid_response(0, request_body, [error.FRIENDS_INVALID])

    def test_invalid_fields(self):
        request_body = {
            'elo': -1,
            'matches_played': -1,
            'matches_won': -1,
            'matches_lost': -1,
            'win_rate': -1,
            'friends': -1
        }
        self.assert_invalid_response(0, request_body, [
            error.ELO_INVALID,
            error.MATCHES_PLAYED_INVALID,
            error.MATCHES_WON_INVALID,
            error.MATCHES_LOST_INVALID,
            error.WIN_RATE_INVALID,
            error.FRIENDS_INVALID
        ])


class PatchUserTest(UserTest):

    def setUp(self):
        self.post_user(0, {})
        self.post_user(1, {
            'elo': 1000,
            'matches_played': 10,
            'matches_won': 5,
            'matches_lost': 5,
            'win_rate': 0.5,
            'friends': 5
        })

    def test_valid_empty_default(self):
        user_id = 0
        request_body = {}
        response = self.patch_user(user_id, request_body)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content.decode('utf-8'))
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(body['elo'], settings.ELO_DEFAULT)
        self.assertEqual(body['matches_played'], settings.MATCHES_PLAYED_DEFAULT)
        self.assertEqual(body['matches_won'], settings.MATCHES_WON_DEFAULT)
        self.assertEqual(body['matches_lost'], settings.MATCHES_LOST_DEFAULT)
        self.assertEqual(body['win_rate'], settings.WIN_RATE_DEFAULT)
        self.assertEqual(body['friends'], settings.FRIENDS_DEFAULT)

    def test_valid_empty_custom(self):
        user_id = 1
        request_body = {}
        response = self.patch_user(user_id, request_body)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content.decode('utf-8'))
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(body['elo'], 1000)
        self.assertEqual(body['matches_played'], 10)
        self.assertEqual(body['matches_won'], 5)
        self.assertEqual(body['matches_lost'], 5)
        self.assertEqual(body['win_rate'], 0.5)
        self.assertEqual(body['friends'], 5)

    def test_valid_custom(self):
        user_id = 0
        request_body = {
            'elo': 1000,
            'matches_played': 10,
            'matches_won': 5,
            'matches_lost': 5,
            'win_rate': 0.5,
            'friends': 5
        }
        response = self.patch_user(user_id, request_body)
        self.assertEqual(response.status_code, 200)
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)

    def test_invalid_user_not_found(self):
        user_id = 2
        request_body = {}
        response = self.patch_user(user_id, request_body)
        body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], [error.USER_NOT_FOUND])

    def test_valid_elo(self):
        user_id = 1
        request_body = {'elo': 1000}
        response = self.patch_user(user_id, request_body)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content.decode('utf-8'))
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(body['elo'], request_body['elo'])
        self.assertEqual(body['matches_played'], 10)
        self.assertEqual(body['matches_won'], 5)
        self.assertEqual(body['matches_lost'], 5)
        self.assertEqual(body['win_rate'], 0.5)
        self.assertEqual(body['friends'], 5)

    def test_invalid_elo(self):
        user_id = 0
        request_body = {'elo': 'abc'}
        self.assert_invalid_response(user_id, request_body, [error.ELO_INVALID])
        request_body = {'elo': 1.1}
        self.assert_invalid_response(user_id, request_body, [error.ELO_INVALID])
        request_body = {'elo': [1]}
        self.assert_invalid_response(user_id, request_body, [error.ELO_INVALID])
        request_body = {'elo': {'elo': 1}}
        self.assert_invalid_response(user_id, request_body, [error.ELO_INVALID])
        request_body = {'elo': -1}
        self.assert_invalid_response(user_id, request_body, [error.ELO_INVALID])

    def test_valid_matches_played(self):
        user_id = 0
        request_body = {'matches_played': 1000}
        response = self.patch_user(user_id, request_body)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content.decode('utf-8'))
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(body['matches_played'], request_body['matches_played'])

    def test_invalid_matches_played(self):
        user_id = 0
        request_body = {'matches_played': 'abc'}
        self.assert_invalid_response(user_id, request_body, [error.MATCHES_PLAYED_INVALID])
        request_body = {'matches_played': 1.1}
        self.assert_invalid_response(user_id, request_body, [error.MATCHES_PLAYED_INVALID])
        request_body = {'matches_played': [1]}
        self.assert_invalid_response(user_id, request_body, [error.MATCHES_PLAYED_INVALID])
        request_body = {'matches_played': {'matches_played': 1}}
        self.assert_invalid_response(user_id, request_body, [error.MATCHES_PLAYED_INVALID])
        request_body = {'matches_played': -1}
        self.assert_invalid_response(user_id, request_body, [error.MATCHES_PLAYED_INVALID])

    def test_valid_matches_won(self):
        user_id = 1
        request_body = {'matches_won': 1000}
        response = self.patch_user(user_id, request_body)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content.decode('utf-8'))
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(body['matches_won'], request_body['matches_won'])
        self.assertEqual(body['elo'], 1000)
        self.assertEqual(body['matches_played'], 10)
        self.assertEqual(body['matches_lost'], 5)
        self.assertEqual(body['win_rate'], 0.5)
        self.assertEqual(body['friends'], 5)

    def test_invalid_matches_won(self):
        user_id = 0
        request_body = {'matches_won': 'abc'}
        self.assert_invalid_response(user_id, request_body, [error.MATCHES_WON_INVALID])
        request_body = {'matches_won': 1.1}
        self.assert_invalid_response(user_id, request_body, [error.MATCHES_WON_INVALID])
        request_body = {'matches_won': [1]}
        self.assert_invalid_response(user_id, request_body, [error.MATCHES_WON_INVALID])
        request_body = {'matches_won': {'matches_won': 1}}
        self.assert_invalid_response(user_id, request_body, [error.MATCHES_WON_INVALID])
        request_body = {'matches_won': -1}
        self.assert_invalid_response(user_id, request_body, [error.MATCHES_WON_INVALID])

    def test_valid_matches_lost(self):
        user_id = 1
        request_body = {'matches_lost': 1000}
        response = self.patch_user(user_id, request_body)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content.decode('utf-8'))
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(body['matches_lost'], request_body['matches_lost'])
        self.assertEqual(body['elo'], 1000)
        self.assertEqual(body['matches_played'], 10)
        self.assertEqual(body['matches_won'], 5)
        self.assertEqual(body['win_rate'], 0.5)
        self.assertEqual(body['friends'], 5)

    def test_invalid_matches_lost(self):
        user_id = 0
        request_body = {'matches_lost': 'abc'}
        self.assert_invalid_response(user_id, request_body, [error.MATCHES_LOST_INVALID])
        request_body = {'matches_lost': 1.1}
        self.assert_invalid_response(user_id, request_body, [error.MATCHES_LOST_INVALID])
        request_body = {'matches_lost': [1]}
        self.assert_invalid_response(user_id, request_body, [error.MATCHES_LOST_INVALID])
        request_body = {'matches_lost': {'matches_lost': 1}}
        self.assert_invalid_response(user_id, request_body, [error.MATCHES_LOST_INVALID])
        request_body = {'matches_lost': -1}
        self.assert_invalid_response(user_id, request_body, [error.MATCHES_LOST_INVALID])

    def test_valid_win_rate(self):
        user_id = 1
        request_body = {'win_rate': 0.5}
        response = self.patch_user(user_id, request_body)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content.decode('utf-8'))
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(body['win_rate'], request_body['win_rate'])
        self.assertEqual(body['elo'], 1000)
        self.assertEqual(body['matches_played'], 10)
        self.assertEqual(body['matches_won'], 5)
        self.assertEqual(body['matches_lost'], 5)
        self.assertEqual(body['friends'], 5)

    def test_valid_win_rate_boundary(self):
        user_id = 0
        request_body = {'win_rate': 1.0}
        response = self.patch_user(user_id, request_body)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(body['win_rate'], request_body['win_rate'])

        user_id = 1
        request_body = {'win_rate': 0.0}
        response = self.patch_user(user_id, request_body)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(body['win_rate'], request_body['win_rate'])

    def test_invalid_win_rate(self):
        user_id = 0
        request_body = {'win_rate': 'abc'}
        self.assert_invalid_response(user_id, request_body, [error.WIN_RATE_INVALID])
        request_body = {'win_rate': 0}
        self.assert_invalid_response(user_id, request_body, [error.WIN_RATE_INVALID])
        request_body = {'win_rate': [1]}
        self.assert_invalid_response(user_id, request_body, [error.WIN_RATE_INVALID])
        request_body = {'win_rate': {'win_rate': 1}}
        self.assert_invalid_response(user_id, request_body, [error.WIN_RATE_INVALID])
        request_body = {'win_rate': -1}
        self.assert_invalid_response(user_id, request_body, [error.WIN_RATE_INVALID])
        request_body = {'win_rate': 1.1}
        self.assert_invalid_response(user_id, request_body, [error.WIN_RATE_INVALID])

    def test_valid_friends(self):
        user_id = 1
        request_body = {'friends': 1000}
        response = self.patch_user(user_id, request_body)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content.decode('utf-8'))
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(body['friends'], request_body['friends'])
        self.assertEqual(body['elo'], 1000)
        self.assertEqual(body['matches_played'], 10)
        self.assertEqual(body['matches_won'], 5)
        self.assertEqual(body['matches_lost'], 5)
        self.assertEqual(body['win_rate'], 0.5)

    def test_invalid_friends(self):
        user_id = 0
        request_body = {'friends': 'abc'}
        self.assert_invalid_response(user_id, request_body, [error.FRIENDS_INVALID])
        request_body = {'friends': 1.1}
        self.assert_invalid_response(user_id, request_body, [error.FRIENDS_INVALID])
        request_body = {'friends': [1]}
        self.assert_invalid_response(user_id, request_body, [error.FRIENDS_INVALID])
        request_body = {'friends': {'friends': 1}}
        self.assert_invalid_response(user_id, request_body, [error.FRIENDS_INVALID])
        request_body = {'friends': -1}
        self.assert_invalid_response(user_id, request_body, [error.FRIENDS_INVALID])

    def test_invalid_fields(self):
        user_id = 0
        request_body = {
            'elo': -1,
            'matches_played': -1,
            'matches_won': -1,
            'matches_lost': -1,
            'win_rate': -1,
            'friends': -1
        }
        self.assert_invalid_response(user_id, request_body, [
            error.ELO_INVALID,
            error.MATCHES_PLAYED_INVALID,
            error.MATCHES_WON_INVALID,
            error.MATCHES_LOST_INVALID,
            error.WIN_RATE_INVALID,
            error.FRIENDS_INVALID
        ])


class DeleteUserTest(UserTest):

    def test_valid_default(self):
        user_id = 1
        self.post_user(user_id, {})
        response = self.delete_user(user_id)
        self.assertEqual(response.status_code, 200)

    def test_invalid_user_not_found(self):
        user_id = 1
        response = self.delete_user(user_id)
        body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], [error.USER_NOT_FOUND])

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_history(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 0}, None)
        valid_user_id = 0
        deleted_user_id = 1
        self.post_user(valid_user_id, {})
        self.post_user(deleted_user_id, {})
        self.post_match({
            'winner_id': valid_user_id,
            'loser_id': deleted_user_id,
            'winner_score': 10,
            'loser_score': 0,
            'date': '2020-01-01T00:00:00Z'
        })
        response = self.delete_user(deleted_user_id)
        self.assertEqual(response.status_code, 200)
        response = self.get_history(deleted_user_id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'][0], error.USER_NOT_FOUND)
        response = self.get_history(valid_user_id)
        self.assertEqual(response.status_code, 200)
        history = response.json()['history']
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]['opponent_id'], None)
        self.assertEqual(history[0]['user_score'], 10)
        self.assertEqual(history[0]['opponent_score'], 0)
        self.assertEqual(history[0]['result'], True)
