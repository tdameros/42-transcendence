import json

from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from api.models import Tournament, Player
from api import error_message as error


class GetTournamentPlayers(TestCase):
    def setUp(self):
        tournament = Tournament.objects.create(name=f'tournament {1}', admin_id=1, max_players=16)
        Tournament.objects.create(name=f'tournament {1}', admin_id=1, max_players=16)
        for i in range(1, 16):
            Player.objects.create(nickname=f'player {i}', user_id=i, tournament=tournament)

    def get_tournament_players(self, tournament_id):
        url = reverse('tournament-players', args=(tournament_id,))

        response = self.client.get(url)

        body = json.loads(response.content.decode('utf8'))

        return response, body

    def test_get_tournament_players(self):
        tournament_id = 1

        response, body = self.get_tournament_players(tournament_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['max-players'], 16)
        self.assertEqual(body['nb-players'], 15)
        self.assertEqual(len(body['players']), 15)

    def test_invalid_tournament(self):
        tournament_id = 10

        response, body = self.get_tournament_players(tournament_id)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['error'], f'tournament with id `{tournament_id}` does not exist')

    def test_no_players(self):
        tournament_id = 2

        response, body = self.get_tournament_players(tournament_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['max-players'], 16)
        self.assertEqual(body['nb-players'], 0)
        self.assertEqual(len(body['players']), 0)


class PostTournamentPlayers(TestCase):
    def setUp(self):
        full_tournament = Tournament.objects.create(name=f'tournament full', admin_id=1, max_players=16)
        tournament = Tournament.objects.create(name=f'tournament', admin_id=1, max_players=16)
        Tournament.objects.create(
            name=f'deadline passed',
            admin_id=1,
            max_players=16,
            registration_deadline='2021-01-01 00:00:00+00:00')
        for i in range(1, 17):
            Player.objects.create(nickname=f'player {i}', user_id=(i + 4), tournament=full_tournament)
        Player.objects.create(nickname=f'player 1', user_id=4, tournament=tournament)

    def post_tournament_players(self, tournament_id, body):
        url = reverse('tournament-players', args=(tournament_id,))

        response = self.client.post(url, body, content_type='application/json')

        body = json.loads(response.content.decode('utf8'))

        return response, body

    def test_post_tournament_players(self):
        tournament_id = 2
        body = json.dumps({'nickname': 'player 4'})

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(body['nickname'], 'player 4')
        self.assertEqual(body['user_id'], 1)

    def test_post_tournament_players_full(self):
        tournament_id = 1
        body = json.dumps({'nickname': 'player'})

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(body['errors'], ['This tournament is fully booked'])

    def test_nickname_too_long(self):
        tournament_id = 2
        body = json.dumps({'nickname': 'a' * 17})

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['errors'], [error.NICKNAME_TOO_LONG])

    def test_nickname_too_short(self):
        tournament_id = 2
        body = json.dumps({'nickname': 'a'})

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['errors'], [error.NICKNAME_TOO_SHORT])

    def test_nickname_already_use(self):
        tournament_id = 2
        body = json.dumps({'nickname': 'player 1'})

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['errors'], ['nickname `player 1` already taken'])

    def test_player_already_in_tournament(self):
        tournament_id = 2
        body = json.dumps({'nickname': 'player 2'})

        Player.objects.create(nickname=f'player 1', user_id=1, tournament_id=tournament_id)

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(body['errors'], ['You are already registered as `player 1` for the tournament'])

    def test_invalid_tournament(self):
        tournament_id = 50
        body = json.dumps({'nickname': 'player 1'})

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], [f'tournament with id `{tournament_id}` does not exist'])

    def test_deadline_passed(self):
        tournament_id = 3
        body = json.dumps({'nickname': 'player 1'})

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(body['errors'], ['The registration phase is over'])

    def test_already_register_to_another_tournament(self):
        tournament_id = 2
        body = json.dumps({'nickname': 'player 4'})

        Player.objects.create(nickname=f'player 1', user_id=1, tournament_id=3)

        response, body = self.post_tournament_players(tournament_id, body)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(body['errors'], ['You are already registered for another tournament'])

