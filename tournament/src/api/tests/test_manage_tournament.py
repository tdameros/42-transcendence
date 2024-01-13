import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from api.models import Player, Tournament


class GetTournamentTest(TestCase):
    def setUp(self):
        Tournament.objects.create(id=1, name='Test1', admin_id=1)
        Tournament.objects.create(id=2, name='Test2', admin_id=2)
        Tournament.objects.create(id=3, name='Test3', admin_id=3, registration_deadline='2020-01-01T00:00:00Z')
        Tournament.objects.create(id=4, name='finished', status=Tournament.FINISHED, admin_id=4)

        for i in range(1, 14):
            Player.objects.create(nickname=f'Player{i}', user_id=i, tournament_id=1)
        for i in range(1, 3):
            Player.objects.create(nickname=f'Player{i}', user_id=i, tournament_id=3)

    def get_tournament(self, tournament_id: int):
        url = reverse('manage-tournament', args=[tournament_id])
        response = self.client.get(url)

        body = json.loads(response.content.decode('utf-8'))

        return response, body

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_get_tournament(self, mock_authenticate_request):
        user = {'id': 1, 'username': 'admin'}
        mock_authenticate_request.return_value = (user, None)
        response, body = self.get_tournament(1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['id'], 1)
        self.assertEqual(body['name'], 'Test1')
        self.assertEqual(body['max-players'], 16)
        self.assertEqual(body['nb-players'], 13)
        self.assertEqual(body['is-private'], False)
        self.assertEqual(body['status'], 'Created')
        self.assertEqual(body['players'], [{
            'nickname': f'Player{i}',
            'user-id': i
        } for i in range(1, 14)])

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_get_tournament_with_deadline(self, mock_authenticate_request):
        user = {'id': 1, 'username': 'admin'}
        mock_authenticate_request.return_value = (user, None)
        response, body = self.get_tournament(3)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['id'], 3)
        self.assertEqual(body['name'], 'Test3')
        self.assertEqual(body['max-players'], 16)
        self.assertEqual(body['nb-players'], 2)
        self.assertEqual(body['is-private'], False)
        self.assertEqual(body['status'], 'Created')
        self.assertEqual(body['registration-deadline'], '2020-01-01T00:00:00Z')
        self.assertEqual(body['players'], [
            {
                'nickname': f'Player{i}',
                'user-id': i
            } for i in range(1, 3)
        ])

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_get_tournament_not_found(self, mock_authenticate_request):
        user = {'id': 1, 'username': 'admin'}
        mock_authenticate_request.return_value = (user, None)
        response, body = self.get_tournament(50)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['error'], 'tournament with id `50` does not exist')

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_get_tournament_no_player(self, mock_authenticate_request):
        user = {'id': 1, 'username': 'admin'}
        mock_authenticate_request.return_value = (user, None)
        response, body = self.get_tournament(2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['id'], 2)
        self.assertEqual(body['name'], 'Test2')
        self.assertEqual(body['max-players'], 16)
        self.assertEqual(body['nb-players'], 0)
        self.assertEqual(body['is-private'], False)
        self.assertEqual(body['status'], 'Created')
        self.assertEqual(body['players'], [])

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_get_tournament_finished(self, mock_authenticate_request):
        user = {'id': 1, 'username': 'admin'}
        mock_authenticate_request.return_value = (user, None)
        response, body = self.get_tournament(4)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['id'], 4)
        self.assertEqual(body['name'], 'finished')
        self.assertEqual(body['max-players'], 16)
        self.assertEqual(body['nb-players'], 0)
        self.assertEqual(body['is-private'], False)
        self.assertEqual(body['status'], 'Finished')
        self.assertEqual(body['players'], [])


class DeleteTournamentTest(TestCase):
    def setUp(self):
        Tournament.objects.create(id=1, name='Test1', admin_id=1)
        Tournament.objects.create(id=2, name='Test2', admin_id=2)

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_delete_tournament(self, mock_authenticate_request):
        user = {'id': 1, 'username': 'admin'}
        mock_authenticate_request.return_value = (user, None)
        url = reverse('manage-tournament', args=[1])
        response = self.client.delete(url)

        body = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tournament.objects.count(), 1)
        self.assertEqual(body['message'], 'tournament `Test1` successfully deleted')

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_delete_tournament_not_found(self, mock_authenticate_request):
        user = {'id': 1, 'username': 'admin'}
        mock_authenticate_request.return_value = (user, None)
        url = reverse('manage-tournament', args=[3])
        response = self.client.delete(url)

        body = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(Tournament.objects.count(), 2)
        self.assertEqual(body['error'], 'tournament with id `3` does not exist')

    @patch('api.views.manage_tournament_views.authenticate_request')
    def test_delete_tournament_not_owner(self, mock_authenticate_request):
        user = {'id': 1, 'username': 'admin'}
        mock_authenticate_request.return_value = (user, None)
        url = reverse('manage-tournament', args=[2])
        response = self.client.delete(url)

        body = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Tournament.objects.count(), 2)
        self.assertEqual(body['error'], 'you cannot delete `Test2` because you are not the owner of the tournament')
