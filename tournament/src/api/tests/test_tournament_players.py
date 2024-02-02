import json
from unittest.mock import patch

from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse

from api import error_message as error
from api.models import Player, Tournament
from api.tests.utils import get_fake_headers


class GetTournamentPlayers(TestCase):
    def setUp(self):
        tournament = Tournament.objects.create(id=1, name=f'tournament {1}', admin_id=1, max_players=16)
        Tournament.objects.create(id=2, name=f'tournament {1}', admin_id=1, max_players=16)
        for i in range(1, 16):
            Player.objects.create(nickname=f'player {i}', user_id=i, tournament=tournament)

    def get_tournament_players(self, tournament_id):
        url = reverse('tournament-players', args=(tournament_id,))

        response = self.client.get(url, headers=get_fake_headers(1))

        body = json.loads(response.content.decode('utf8'))

        return response, body

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_get_tournament_players(self, mock_authenticate_request):
        user = {'id': 1}
        mock_authenticate_request.return_value = (True, user, None)
        tournament_id = 1

        response, body = self.get_tournament_players(tournament_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['max-players'], 16)
        self.assertEqual(body['nb-players'], 15)
        self.assertEqual(len(body['players']), 15)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_invalid_tournament(self, mock_authenticate_request):
        user = {'id': 1}
        mock_authenticate_request.return_value = (True, user, None)
        tournament_id = 10

        response, body = self.get_tournament_players(tournament_id)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], [f'tournament with id `{tournament_id}` does not exist'])

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_no_players(self, mock_authenticate_request):
        user = {'id': 1}
        mock_authenticate_request.return_value = (True, user, None)
        tournament_id = 2

        response, body = self.get_tournament_players(tournament_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['max-players'], 16)
        self.assertEqual(body['nb-players'], 0)
        self.assertEqual(len(body['players']), 0)


class PostTournamentPlayers(TestCase):
    def setUp(self):
        full_tournament = Tournament.objects.create(id=1, name='tournament full', admin_id=1, max_players=16)
        tournament = Tournament.objects.create(id=2, name='tournament', admin_id=1, max_players=16)
        Tournament.objects.create(
            id=3,
            name='deadline passed',
            admin_id=1,
            max_players=16,
            registration_deadline='2021-01-01 00:00:00+00:00'
        )
        Tournament.objects.create(
            id=4,
            name='private',
            admin_id=1,
            max_players=16,
            is_private=True,
            password=make_password('pass')
        )
        for i in range(1, 17):
            Player.objects.create(nickname=f'player {i}', user_id=(i + 4), tournament=full_tournament)
        Player.objects.create(nickname='player 1', user_id=4, tournament=tournament)

    def post_tournament_players(self, tournament_id, body):
        url = reverse('tournament-players', args=(tournament_id,))

        response = self.client.post(url, body, content_type='application/json', headers=get_fake_headers(1))

        body = json.loads(response.content.decode('utf8'))

        return response, body

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_post_tournament_players(self, mock_authenticate_request):
        user = {'id': 1}
        mock_authenticate_request.return_value = (True, user, None)
        tournament_id = 2
        body = json.dumps({'nickname': 'player 4'})

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(body['nickname'], 'player 4')
        self.assertEqual(body['user_id'], 1)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_join_private_tournament(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (True, user, None)
        tournament_id = 4
        body = json.dumps({'nickname': 'player 4', 'password': 'pass'})

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(body['nickname'], 'player 4')
        self.assertEqual(body['user_id'], 1)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_post_tournament_players_full(self, mock_authenticate_request):
        user = {'id': 1}
        mock_authenticate_request.return_value = (True, user, None)
        tournament_id = 1
        body = json.dumps({'nickname': 'player'})

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(body['errors'], ['This tournament is fully booked'])

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_nickname_too_long(self, mock_authenticate_request):
        user = {'id': 1}
        mock_authenticate_request.return_value = (True, user, None)
        tournament_id = 2
        body = json.dumps({'nickname': 'a' * 17})

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['errors'], [error.NICKNAME_TOO_LONG])

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_nickname_too_short(self, mock_authenticate_request):
        user = {'id': 1}
        mock_authenticate_request.return_value = (True, user, None)
        tournament_id = 2
        body = json.dumps({'nickname': 'a'})

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['errors'], [error.NICKNAME_TOO_SHORT])

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_nickname_already_use(self, mock_authenticate_request):
        user = {'id': 1}
        mock_authenticate_request.return_value = (True, user, None)
        tournament_id = 2
        body = json.dumps({'nickname': 'player 1'})

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['errors'], ['nickname `player 1` already taken'])

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_player_already_in_tournament(self, mock_authenticate_request):
        user = {'id': 1}
        mock_authenticate_request.return_value = (True, user, None)
        tournament_id = 2
        body = json.dumps({'nickname': 'player 2'})

        Player.objects.create(nickname='player 1', user_id=1, tournament_id=tournament_id)

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(body['errors'], ['You are already registered as `player 1` for the tournament'])

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_invalid_tournament(self, mock_authenticate_request):
        user = {'id': 1}
        mock_authenticate_request.return_value = (True, user, None)
        tournament_id = 50
        body = json.dumps({'nickname': 'player 1'})

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], [f'tournament with id `{tournament_id}` does not exist'])

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_deadline_passed(self, mock_authenticate_request):
        user = {'id': 1}
        mock_authenticate_request.return_value = (True, user, None)
        tournament_id = 3
        body = json.dumps({'nickname': 'player 1'})

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(body['errors'], ['The registration phase is over'])

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_already_register_to_another_tournament(self, mock_authenticate_request):
        user = {'id': 1}
        mock_authenticate_request.return_value = (True, user, None)
        tournament_id = 2
        body = json.dumps({'nickname': 'player 4'})

        Player.objects.create(nickname='player 1', user_id=1, tournament_id=3)

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(body['errors'], ['You are already registered for another tournament'])

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_join_invalid_password(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (True, user, None)
        tournament_id = 4
        body = json.dumps({'nickname': 'player 4', 'password': 'wrong'})

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(body['errors'], [error.PASSWORD_NOT_MATCH])

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_join_private_no_password(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (True, user, None)
        tournament_id = 4
        body = json.dumps({'nickname': 'player 4'})

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['errors'], [error.PASSWORD_MISSING])


class DeleteTournamentPlayers(TestCase):
    def setUp(self):
        tournament = Tournament.objects.create(id=1, name='tournament', admin_id=1, max_players=16)
        Tournament.objects.create(id=2, name='tournament', admin_id=1, max_players=16)
        Player.objects.create(nickname='player 1', user_id=1, tournament=tournament)
        Player.objects.create(nickname='player 2', user_id=2, tournament=tournament)

        finished_tournament = Tournament.objects.create(id=3, name='tournament', admin_id=1, status=2)
        Player.objects.create(nickname='player 1', user_id=1, tournament=finished_tournament)

        in_progress_tournament = Tournament.objects.create(id=4, name='tournament', admin_id=1, status=1)
        Player.objects.create(nickname='player 1', user_id=1, tournament=in_progress_tournament)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_delete_tournament_player(self, mock_authenticate_request):
        user = {'id': 1}
        mock_authenticate_request.return_value = (True, user, None)
        tournament_id = 1

        url = reverse('tournament-players', args=(tournament_id,))
        response = self.client.delete(url, headers=get_fake_headers(1))

        body = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['message'], 'You left the tournament `tournament`')

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_delete_not_admin(self, mock_authenticate_request):
        user = {'id': 2}
        mock_authenticate_request.return_value = (True, user, None)
        tournament_id = 1

        url = reverse('tournament-players', args=(tournament_id,))
        response = self.client.delete(url, headers=get_fake_headers(2))

        body = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['message'], 'You left the tournament `tournament`')

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_delete_tournament_not_found(self, mock_authenticate_request):
        user = {'id': 1}
        mock_authenticate_request.return_value = (True, user, None)
        tournament_id = 10

        url = reverse('tournament-players', args=(tournament_id,))
        response = self.client.delete(url, headers=get_fake_headers(1))

        body = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], [f'tournament with id `{tournament_id}` does not exist'])

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_delete_not_registered(self, mock_authenticate_request):
        user = {'id': 1}
        mock_authenticate_request.return_value = (True, user, None)
        tournament_id = 2

        url = reverse('tournament-players', args=(tournament_id,))
        response = self.client.delete(url, headers=get_fake_headers(1))

        body = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], ['You are not registered for this tournament'])

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_delete_finished_tournament(self, mock_authenticate_request):
        user = {'id': 1}
        mock_authenticate_request.return_value = (True, user, None)
        tournament_id = 3

        url = reverse('tournament-players', args=(tournament_id,))
        response = self.client.delete(url, headers=get_fake_headers(1))

        body = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 403)
        self.assertEqual(body['errors'], [error.CANT_LEAVE])

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_delete_in_progress_tournament(self, mock_authenticate_request):
        user = {'id': 1}
        mock_authenticate_request.return_value = (True, user, None)
        tournament_id = 4

        url = reverse('tournament-players', args=(tournament_id,))
        response = self.client.delete(url, headers=get_fake_headers(1))

        body = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 403)
        self.assertEqual(body['errors'], [error.CANT_LEAVE])


class AnonymizePlayer(TestCase):
    def setUp(self):
        tournament = Tournament.objects.create(id=1, name='tournament', admin_id=1, max_players=16)
        second_tournament = Tournament.objects.create(id=2, name='tournament', admin_id=1, max_players=16)
        for i in range(0, 16):
            Player.objects.create(nickname=f'player {i}', user_id=(i + 1), tournament=tournament)
        for i in range(0, 16):
            Player.objects.create(nickname=f'player {i}', user_id=(i + 1), tournament=second_tournament)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_anonymize_player(self, mock_authenticate_request):
        user = {'id': 1}
        mock_authenticate_request.return_value = (True, user, None)

        url = reverse('player')
        response = self.client.post(url, headers=get_fake_headers(1))

        players = Player.objects.filter(user_id=user['id'])

        self.assertEqual(response.status_code, 200)
        for player in players:
            self.assertEqual(player.nickname, 'deleted_user')

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_no_player_to_anonymize(self, mock_authenticate_request):
        user = {'id': 50}
        mock_authenticate_request.return_value = (True, user, None)

        url = reverse('player')
        response = self.client.post(url, headers=get_fake_headers(50))

        self.assertEqual(response.status_code, 200)
