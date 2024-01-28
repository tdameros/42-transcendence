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

    def assert_equal_user(self, user, response):
        body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(body['id'], user.id)
        self.assertEqual(body['elo'], user.elo)
        self.assertEqual(body['games_played'], user.games_played)
        self.assertEqual(body['games_won'], user.games_won)
        self.assertEqual(body['games_lost'], user.games_lost)
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
            games_played=10,
            games_won=5,
            games_lost=5,
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
        self.assertEqual(body['games_played'], settings.GAMES_PLAYED_DEFAULT)
        self.assertEqual(body['games_won'], settings.GAMES_WON_DEFAULT)
        self.assertEqual(body['games_lost'], settings.GAMES_LOST_DEFAULT)
        self.assertEqual(body['win_rate'], settings.WIN_RATE_DEFAULT)
        self.assertEqual(body['friends'], settings.FRIENDS_DEFAULT)

    def test_valid_custom(self):
        user_id = 1
        request_body = {
            'elo': 1000,
            'games_played': 10,
            'games_won': 5,
            'games_lost': 5,
            'win_rate': 0.5,
            'friends': 5
        }
        response = self.post_user(user_id, request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(response_body['elo'], request_body['elo'])
        self.assertEqual(response_body['games_played'], request_body['games_played'])
        self.assertEqual(response_body['games_won'], request_body['games_won'])
        self.assertEqual(response_body['games_lost'], request_body['games_lost'])
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
        self.assertEqual(response_body['games_played'], settings.GAMES_PLAYED_DEFAULT)
        self.assertEqual(response_body['games_won'], settings.GAMES_WON_DEFAULT)
        self.assertEqual(response_body['games_lost'], settings.GAMES_LOST_DEFAULT)
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

    def test_valid_games_played(self):
        user_id = 0
        request_body = {'games_played': 1000}
        response = self.post_user(user_id, request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(response_body['elo'], settings.ELO_DEFAULT)
        self.assertEqual(response_body['games_played'], request_body['games_played'])
        self.assertEqual(response_body['games_won'], settings.GAMES_WON_DEFAULT)
        self.assertEqual(response_body['games_lost'], settings.GAMES_LOST_DEFAULT)
        self.assertEqual(response_body['win_rate'], settings.WIN_RATE_DEFAULT)
        self.assertEqual(response_body['friends'], settings.FRIENDS_DEFAULT)

    def test_invalid_games_played(self):
        request_body = {'games_played': 'abc'}
        self.assert_invalid_response(0, request_body, [error.GAMES_PLAYED_INVALID])
        request_body = {'games_played': 1.1}
        self.assert_invalid_response(0, request_body, [error.GAMES_PLAYED_INVALID])
        request_body = {'games_played': [1]}
        self.assert_invalid_response(0, request_body, [error.GAMES_PLAYED_INVALID])
        request_body = {'games_played': {'games_played': 1}}
        self.assert_invalid_response(0, request_body, [error.GAMES_PLAYED_INVALID])
        request_body = {'games_played': -1}
        self.assert_invalid_response(0, request_body, [error.GAMES_PLAYED_INVALID])

    def test_valid_games_won(self):
        user_id = 0
        request_body = {'games_won': 1000}
        response = self.post_user(user_id, request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(response_body['elo'], settings.ELO_DEFAULT)
        self.assertEqual(response_body['games_played'], settings.GAMES_PLAYED_DEFAULT)
        self.assertEqual(response_body['games_won'], request_body['games_won'])
        self.assertEqual(response_body['games_lost'], settings.GAMES_LOST_DEFAULT)
        self.assertEqual(response_body['win_rate'], settings.WIN_RATE_DEFAULT)
        self.assertEqual(response_body['friends'], settings.FRIENDS_DEFAULT)

    def test_invalid_games_won(self):
        request_body = {'games_won': 'abc'}
        self.assert_invalid_response(0, request_body, [error.GAMES_WON_INVALID])
        request_body = {'games_won': 1.1}
        self.assert_invalid_response(0, request_body, [error.GAMES_WON_INVALID])
        request_body = {'games_won': [1]}
        self.assert_invalid_response(0, request_body, [error.GAMES_WON_INVALID])
        request_body = {'games_won': {'games_won': 1}}
        self.assert_invalid_response(0, request_body, [error.GAMES_WON_INVALID])
        request_body = {'games_won': -1}
        self.assert_invalid_response(0, request_body, [error.GAMES_WON_INVALID])

    def test_valid_games_lost(self):
        user_id = 0
        request_body = {'games_lost': 1000}
        response = self.post_user(user_id, request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(response_body['elo'], settings.ELO_DEFAULT)
        self.assertEqual(response_body['games_played'], settings.GAMES_PLAYED_DEFAULT)
        self.assertEqual(response_body['games_won'], settings.GAMES_WON_DEFAULT)
        self.assertEqual(response_body['games_lost'], request_body['games_lost'])
        self.assertEqual(response_body['win_rate'], settings.WIN_RATE_DEFAULT)
        self.assertEqual(response_body['friends'], settings.FRIENDS_DEFAULT)

    def test_invalid_games_lost(self):
        request_body = {'games_lost': 'abc'}
        self.assert_invalid_response(0, request_body, [error.GAMES_LOST_INVALID])
        request_body = {'games_lost': 1.1}
        self.assert_invalid_response(0, request_body, [error.GAMES_LOST_INVALID])
        request_body = {'games_lost': [1]}
        self.assert_invalid_response(0, request_body, [error.GAMES_LOST_INVALID])
        request_body = {'games_lost': {'games_lost': 1}}
        self.assert_invalid_response(0, request_body, [error.GAMES_LOST_INVALID])
        request_body = {'games_lost': -1}
        self.assert_invalid_response(0, request_body, [error.GAMES_LOST_INVALID])

    def test_valid_win_rate(self):
        user_id = 0
        request_body = {'win_rate': 0.5}
        response = self.post_user(user_id, request_body)
        response_body = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(response_body['elo'], settings.ELO_DEFAULT)
        self.assertEqual(response_body['games_played'], settings.GAMES_PLAYED_DEFAULT)
        self.assertEqual(response_body['games_won'], settings.GAMES_WON_DEFAULT)
        self.assertEqual(response_body['games_lost'], settings.GAMES_LOST_DEFAULT)
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
        self.assertEqual(response_body['games_played'], settings.GAMES_PLAYED_DEFAULT)
        self.assertEqual(response_body['games_won'], settings.GAMES_WON_DEFAULT)
        self.assertEqual(response_body['games_lost'], settings.GAMES_LOST_DEFAULT)
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
            'games_played': -1,
            'games_won': -1,
            'games_lost': -1,
            'win_rate': -1,
            'friends': -1
        }
        self.assert_invalid_response(0, request_body, [
            error.ELO_INVALID,
            error.GAMES_PLAYED_INVALID,
            error.GAMES_WON_INVALID,
            error.GAMES_LOST_INVALID,
            error.WIN_RATE_INVALID,
            error.FRIENDS_INVALID
        ])


class PatchUserTest(UserTest):

    def setUp(self):
        self.post_user(0, {})
        self.post_user(1, {
            'elo': 1000,
            'games_played': 10,
            'games_won': 5,
            'games_lost': 5,
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
        self.assertEqual(body['games_played'], settings.GAMES_PLAYED_DEFAULT)
        self.assertEqual(body['games_won'], settings.GAMES_WON_DEFAULT)
        self.assertEqual(body['games_lost'], settings.GAMES_LOST_DEFAULT)
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
        self.assertEqual(body['games_played'], 10)
        self.assertEqual(body['games_won'], 5)
        self.assertEqual(body['games_lost'], 5)
        self.assertEqual(body['win_rate'], 0.5)
        self.assertEqual(body['friends'], 5)

    def test_valid_custom(self):
        user_id = 0
        request_body = {
            'elo': 1000,
            'games_played': 10,
            'games_won': 5,
            'games_lost': 5,
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
        self.assertEqual(body['games_played'], 10)
        self.assertEqual(body['games_won'], 5)
        self.assertEqual(body['games_lost'], 5)
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

    def test_valid_games_played(self):
        user_id = 0
        request_body = {'games_played': 1000}
        response = self.patch_user(user_id, request_body)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content.decode('utf-8'))
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(body['games_played'], request_body['games_played'])

    def test_invalid_games_played(self):
        user_id = 0
        request_body = {'games_played': 'abc'}
        self.assert_invalid_response(user_id, request_body, [error.GAMES_PLAYED_INVALID])
        request_body = {'games_played': 1.1}
        self.assert_invalid_response(user_id, request_body, [error.GAMES_PLAYED_INVALID])
        request_body = {'games_played': [1]}
        self.assert_invalid_response(user_id, request_body, [error.GAMES_PLAYED_INVALID])
        request_body = {'games_played': {'games_played': 1}}
        self.assert_invalid_response(user_id, request_body, [error.GAMES_PLAYED_INVALID])
        request_body = {'games_played': -1}
        self.assert_invalid_response(user_id, request_body, [error.GAMES_PLAYED_INVALID])

    def test_valid_games_won(self):
        user_id = 1
        request_body = {'games_won': 1000}
        response = self.patch_user(user_id, request_body)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content.decode('utf-8'))
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(body['games_won'], request_body['games_won'])
        self.assertEqual(body['elo'], 1000)
        self.assertEqual(body['games_played'], 10)
        self.assertEqual(body['games_lost'], 5)
        self.assertEqual(body['win_rate'], 0.5)
        self.assertEqual(body['friends'], 5)

    def test_invalid_games_won(self):
        user_id = 0
        request_body = {'games_won': 'abc'}
        self.assert_invalid_response(user_id, request_body, [error.GAMES_WON_INVALID])
        request_body = {'games_won': 1.1}
        self.assert_invalid_response(user_id, request_body, [error.GAMES_WON_INVALID])
        request_body = {'games_won': [1]}
        self.assert_invalid_response(user_id, request_body, [error.GAMES_WON_INVALID])
        request_body = {'games_won': {'games_won': 1}}
        self.assert_invalid_response(user_id, request_body, [error.GAMES_WON_INVALID])
        request_body = {'games_won': -1}
        self.assert_invalid_response(user_id, request_body, [error.GAMES_WON_INVALID])

    def test_valid_games_lost(self):
        user_id = 1
        request_body = {'games_lost': 1000}
        response = self.patch_user(user_id, request_body)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content.decode('utf-8'))
        user = User.objects.get(pk=user_id)
        self.assert_equal_user(user, response)
        self.assertEqual(body['games_lost'], request_body['games_lost'])
        self.assertEqual(body['elo'], 1000)
        self.assertEqual(body['games_played'], 10)
        self.assertEqual(body['games_won'], 5)
        self.assertEqual(body['win_rate'], 0.5)
        self.assertEqual(body['friends'], 5)

    def test_invalid_games_lost(self):
        user_id = 0
        request_body = {'games_lost': 'abc'}
        self.assert_invalid_response(user_id, request_body, [error.GAMES_LOST_INVALID])
        request_body = {'games_lost': 1.1}
        self.assert_invalid_response(user_id, request_body, [error.GAMES_LOST_INVALID])
        request_body = {'games_lost': [1]}
        self.assert_invalid_response(user_id, request_body, [error.GAMES_LOST_INVALID])
        request_body = {'games_lost': {'games_lost': 1}}
        self.assert_invalid_response(user_id, request_body, [error.GAMES_LOST_INVALID])
        request_body = {'games_lost': -1}
        self.assert_invalid_response(user_id, request_body, [error.GAMES_LOST_INVALID])

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
        self.assertEqual(body['games_played'], 10)
        self.assertEqual(body['games_won'], 5)
        self.assertEqual(body['games_lost'], 5)
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
        self.assertEqual(body['games_played'], 10)
        self.assertEqual(body['games_won'], 5)
        self.assertEqual(body['games_lost'], 5)
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
            'games_played': -1,
            'games_won': -1,
            'games_lost': -1,
            'win_rate': -1,
            'friends': -1
        }
        self.assert_invalid_response(user_id, request_body, [
            error.ELO_INVALID,
            error.GAMES_PLAYED_INVALID,
            error.GAMES_WON_INVALID,
            error.GAMES_LOST_INVALID,
            error.WIN_RATE_INVALID,
            error.FRIENDS_INVALID
        ])
