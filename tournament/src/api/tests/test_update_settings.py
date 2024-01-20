import json
from unittest.mock import patch

from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse

from api import error_message as error
from api.models import Player, Tournament


class PatchTournamentTest(TestCase):
    def setUp(self):
        Tournament.objects.create(id=1, name='Test1', admin_id=1)
        Tournament.objects.create(id=2, name='Test2', admin_id=1)
        Tournament.objects.create(id=3, name='Test3', admin_id=1, registration_deadline='2028-01-01T00:00:00Z')
        Tournament.objects.create(id=4, name='in_progress', status=Tournament.IN_PROGRESS, admin_id=1)
        Tournament.objects.create(id=5, name='finished', status=Tournament.FINISHED, admin_id=1)
        Tournament.objects.create(id=6, name='8players', max_players=14, admin_id=1)
        Tournament.objects.create(id=7, name='private', is_private=True, password=make_password('test'), admin_id=1)

        for i in range(1, 9):
            Player.objects.create(nickname=f'Player{i}', user_id=i, tournament_id=6)

    def patch_tournament(self, tournament_id: int, body: dict):
        url = reverse('manage-tournament', args=[tournament_id])
        response = self.client.patch(url, json.dumps(body), content_type='application/json')

        body = json.loads(response.content.decode('utf-8'))

        return response, body

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_patch_tournament(self, mock_authenticate_request):
        user = {'id': 1, 'username': 'admin'}
        mock_authenticate_request.return_value = (user, None)
        response, body = self.patch_tournament(1, {
                                                   'name': 'new name',
                                                   'max-players': 8,
                                                   'is-private': True,
                                                   'password': 'test'
                                                   })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['id'], 1)
        self.assertEqual(body['name'], 'new name')
        self.assertEqual(body['max-players'], 8)
        self.assertEqual(body['is-private'], True)

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_change_password(self, mock_get):
        user = {'id': 1, 'username': 'admin'}
        mock_get.return_value = (user, None)
        response, body = self.patch_tournament(7, {'password': 'test2'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['id'], 7)
        self.assertEqual(body['name'], 'private')
        self.assertEqual(body['max-players'], 16)
        self.assertEqual(body['is-private'], True)

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_private_to_public(self, mock_get):
        user = {'id': 1, 'username': 'admin'}
        mock_get.return_value = (user, None)
        response, body = self.patch_tournament(7, {'is-private': False})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['id'], 7)
        self.assertEqual(body['name'], 'private')
        self.assertEqual(body['max-players'], 16)
        self.assertEqual(body['is-private'], False)

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_patch_tournament_name(self, mock_authenticate_request):
        user = {'id': 1, 'username': 'admin'}
        mock_authenticate_request.return_value = (user, None)
        response, body = self.patch_tournament(1, {'name': 'new name'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['id'], 1)
        self.assertEqual(body['name'], 'new name')
        self.assertEqual(body['max-players'], 16)
        self.assertEqual(body['is-private'], False)
        self.assertEqual(body['status'], 'Created')

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_patch_tournament_max_players(self, mock_authenticate_request):
        user = {'id': 1, 'username': 'admin'}
        mock_authenticate_request.return_value = (user, None)
        response, body = self.patch_tournament(1, {'max-players': 8})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['id'], 1)
        self.assertEqual(body['name'], 'Test1')
        self.assertEqual(body['max-players'], 8)
        self.assertEqual(body['is-private'], False)
        self.assertEqual(body['status'], 'Created')

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_patch_max_players_too_short(self, mock_authenticate_request):
        user = {'id': 1, 'username': 'admin'}
        mock_authenticate_request.return_value = (user, None)
        response, body = self.patch_tournament(6, {'max-players': 2})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['errors'],
                         ['You cannot set the max players to 2 because there are already 8 players registered'])

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_patch_name_too_long(self, mock_authenticate_request):
        user = {'id': 1, 'username': 'admin'}
        mock_authenticate_request.return_value = (user, None)
        response, body = self.patch_tournament(1, {'name': 'a' * 40})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['errors'], [error.NAME_TOO_LONG])

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_patch_invalid_name(self, mock_authenticate_request):
        user = {'id': 1, 'username': 'admin'}
        mock_authenticate_request.return_value = (user, None)
        response, body = self.patch_tournament(1, {'name': 'a!fdasfdas'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['errors'], [error.NAME_INVALID_CHAR])

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_patch_passed_deadline(self, mock_authenticate_request):
        user = {'id': 1, 'username': 'admin'}
        mock_authenticate_request.return_value = (user, None)
        response, body = self.patch_tournament(3, {'registration-deadline': '2022-01-01T00:00:00Z'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['errors'], [error.DEADLINE_PASSED])

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_patch_deadline(self, mock_authenticate_request):
        user = {'id': 1, 'username': 'admin'}
        mock_authenticate_request.return_value = (user, None)
        response, body = self.patch_tournament(3, {'registration-deadline': '2029-01-01T00:00:00Z'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['id'], 3)
        self.assertEqual(body['name'], 'Test3')
        self.assertEqual(body['max-players'], 16)
        self.assertEqual(body['is-private'], False)
        self.assertEqual(body['status'], 'Created')
        self.assertEqual(body['registration-deadline'], '2029-01-01T00:00:00Z')

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_patch_no_password(self, mock_get):
        user = {'id': 1, 'username': 'admin'}
        mock_get.return_value = (user, None)
        response, body = self.patch_tournament(1, {'is-private': True})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['errors'], [error.PASSWORD_MISSING])

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_patch_password_too_short(self, mock_get):
        user = {'id': 1, 'username': 'admin'}
        mock_get.return_value = (user, None)
        response, body = self.patch_tournament(1, {'is-private': True, 'password': 'a'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['errors'], [error.PASSWORD_TOO_SHORT])

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_patch_password_too_long(self, mock_get):
        user = {'id': 1, 'username': 'admin'}
        mock_get.return_value = (user, None)
        response, body = self.patch_tournament(1, {'is-private': True, 'password': 'a' * 40})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['errors'], [error.PASSWORD_TOO_LONG])
