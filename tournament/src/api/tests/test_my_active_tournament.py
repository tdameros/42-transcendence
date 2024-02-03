from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from api.models import Player, Tournament
from api.tests.utils import get_fake_headers


class TestMyActiveTournamentView(TestCase):
    def setUp(self):
        tournament = Tournament.objects.create(id=1, name='Tournament 1', admin_id=1, status=0)
        Tournament.objects.create(id=2, name='Tournament 2', admin_id=2, status=2)
        Tournament.objects.create(id=3, name='Tournament 3', admin_id=2, status=0)
        Tournament.objects.create(id=4, name='Tournament 4', admin_id=2, status=0)
        Player.objects.create(nickname='nickname', user_id=1, tournament=tournament)
        Player.objects.create(nickname='nickname1', user_id=2, tournament=tournament)

    def get_my_active_tournament(self, user_id):
        url = reverse('my-active-tournament')
        response = self.client.get(url, headers=get_fake_headers(user_id))

        body = response.json()
        return response, body

    @patch('api.views.tournament_utils.get_username_by_id')
    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_get_my_active_tournament(self, mock_authenticate, mock_get_username_by_id):
        mock_authenticate.return_value = (True, {'user_id': 1}, None)
        mock_get_username_by_id.return_value = 'nickname'
        response, body = self.get_my_active_tournament(1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body, {
            'nb-active-tournaments': 1,
            'active-tournaments': [
                {
                    'id': 1,
                    'name': 'Tournament 1',
                    'max-players': 16,
                    'nb-players': 2,
                    'is-private': False,
                    'status': 'Created',
                    'admin': mock_get_username_by_id.return_value
                },
            ]
        })

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_get_my_active_tournament_no_active_tournament(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'user_id': 3}, None)
        response, body = self.get_my_active_tournament(3)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body, {
            'nb-active-tournaments': 0,
            'active-tournaments': []
        })

    @patch('api.views.tournament_utils.get_username_by_id')
    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_get_my_active_tournament_user_2(self, mock_authenticate, mock_get_username_by_id):
        mock_authenticate.return_value = (True, {'user_id': 2}, None)
        mock_get_username_by_id.return_value = 'nickname1'
        response, body = self.get_my_active_tournament(2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['nb-active-tournaments'], 3)
        self.assertEqual(len(body['active-tournaments']), 3)
        self.assertEqual(body, {
            'nb-active-tournaments': 3,
            'active-tournaments': [
                {
                    'id': 1,
                    'name': 'Tournament 1',
                    'max-players': 16,
                    'nb-players': 2,
                    'is-private': False,
                    'status': 'Created',
                    'admin': 'nickname1'
                },
                {
                    'id': 3,
                    'name': 'Tournament 3',
                    'max-players': 16,
                    'nb-players': 0,
                    'is-private': False,
                    'status': 'Created',
                    'admin': 'nickname1'
                },
                {
                    'id': 4,
                    'name': 'Tournament 4',
                    'max-players': 16,
                    'nb-players': 0,
                    'is-private': False,
                    'status': 'Created',
                    'admin': 'nickname1'
                }
            ]
        })
