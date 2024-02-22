import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from api import error_message as error
from api.models import Match, Player, Tournament
from api.tests.utils import get_fake_headers


class GenerateTournamentMatches(TestCase):
    def setUp(self):
        tournament = Tournament.objects.create(id=1, name='tournament 1', admin_id=1, max_players=8)
        tournament_not_full = Tournament.objects.create(id=2, name='tournament 2', admin_id=1, max_players=8)

        for i in range(0, 8):
            Player.objects.create(nickname=f'player {i}', user_id=i, tournament=tournament)

        for i in range(0, 5):
            Player.objects.create(nickname=f'player {i}', user_id=i, tournament=tournament_not_full)

        players = tournament.players.all()
        Match.objects.create(player_1=players[0], player_2=players[1], tournament=tournament, match_id=1)

    def generate_matches(self, tournament_id, is_random):
        url = reverse('generate-matches', args=(tournament_id,))

        response = self.client.post(
            url,
            {'random': is_random},
            content_type='application/json',
            headers=get_fake_headers(1)
        )

        body = json.loads(response.content.decode('utf8'))

        return response, body

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_full_tournament(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (True, user, None)

        tournament_id = 1

        response, body = self.generate_matches(tournament_id, True)

        matches = Match.objects.filter(tournament_id=tournament_id)

        if response.status_code != 200:
            print(body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['nb-matches'], 7)
        self.assertEqual(len(body['matches']), 7)
        self.assertEqual(len(matches), 7)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_tournament_not_full(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (True, user, None)

        tournament_id = 2

        response, body = self.generate_matches(tournament_id, True)

        if response.status_code != 200:
            print(body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['nb-matches'], 7)
        self.assertEqual(len(body['matches']), 7)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_tournament_does_not_exist(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (True, user, None)

        tournament_id = 3

        response, body = self.generate_matches(tournament_id, True)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], ['tournament with id `3` does not exist'])


class MatchesTest(TestCase):
    def setUp(self):
        tournament = Tournament.objects.create(id=1, name='tournament 1', admin_id=1, max_players=8)

        for i in range(0, 8):
            Player.objects.create(nickname=f'player {i}', user_id=i, tournament=tournament)
        players = tournament.players.all()

        for i in range(0, 4):
            Match.objects.create(player_1=players[i], player_2=players[i + 4], tournament=tournament, match_id=i + 1)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_get_matches(self, mock_authenticate):
        user = {'id': 1}
        mock_authenticate.return_value = (True, user, None)

        tournament_id = 1
        url = reverse('matches', args=(tournament_id,))
        response = self.client.get(url)
        body = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body['matches']), 4)
        self.assertEqual(body['matches'][0]['player_1']['nickname'], 'player 0')
        self.assertEqual(body['matches'][0]['player_2']['nickname'], 'player 4')
        self.assertEqual(body['matches'][1]['player_1']['nickname'], 'player 1')
        self.assertEqual(body['matches'][1]['player_2']['nickname'], 'player 5')
        self.assertEqual(body['matches'][2]['player_1']['nickname'], 'player 2')
        self.assertEqual(body['matches'][2]['player_2']['nickname'], 'player 6')
        self.assertEqual(body['matches'][3]['player_1']['nickname'], 'player 3')
        self.assertEqual(body['matches'][3]['player_2']['nickname'], 'player 7')

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_tournament_not_exist(self, mock_authenticate):
        user = {'id': 1}
        mock_authenticate.return_value = (True, user, None)

        tournament_id = 50
        url = reverse('matches', args=(tournament_id,))
        response = self.client.get(url)
        body = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], ['tournament with id `50` does not exist'])


class GetMatchTest(TestCase):
    def setUp(self):
        tournament = Tournament.objects.create(id=1, name='tournament 1', admin_id=1, max_players=8)

        for i in range(0, 8):
            Player.objects.create(nickname=f'player {i}', user_id=i, tournament=tournament)
        players = tournament.players.all()

        for i in range(0, 4):
            Match.objects.create(player_1=players[i], player_2=players[i + 4], tournament=tournament, match_id=i + 1)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_get_match(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (True, user, None)

        tournament_id = 1
        url = reverse('matches', args=(tournament_id,))
        response = self.client.get(url)
        body = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body['matches']), 4)
        self.assertEqual(body['matches'][0]['player_1']['nickname'], 'player 0')
        self.assertEqual(body['matches'][0]['player_2']['nickname'], 'player 4')
        self.assertEqual(body['matches'][0]['status'], 'Not played')

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_tournament_does_not_exist(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (True, user, None)

        tournament_id = 50
        url = reverse('matches', args=(tournament_id,))
        response = self.client.get(url)
        body = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], ['tournament with id `50` does not exist'])


class StartMatchTest(TestCase):
    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def setUp(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (True, user, None)
        tournament = Tournament.objects.create(id=1, name='tournament 1', admin_id=1, max_players=8)

        for i in range(0, 8):
            Player.objects.create(
                id=i,
                nickname=f'player {i}',
                user_id=i,
                tournament=tournament,
            )

        url = reverse('generate-matches', args=(1,))

        self.client.post(url, {'random': True}, content_type='application/json', headers=get_fake_headers(1))

        tournament.status = Tournament.IN_PROGRESS
        tournament.save()

    @patch('common.src.jwt_managers.ServiceAccessJWT.authenticate')
    def start_match(self, tournament_id, player1, player2, mock_authenticate):
        mock_authenticate.return_value = (True, None)
        url = reverse('start-match', args=(tournament_id,))

        response = self.client.post(
            url,
            {
                'player1': player1,
                'player2': player2
            },
            content_type='application/json'
        )

        body = json.loads(response.content.decode('utf8'))

        return response, body

    def test_start_match(self):
        tournament_id = 1

        match = Match.objects.get(match_id=0, tournament_id=tournament_id)

        response, body = self.start_match(tournament_id, match.player_1.user_id, match.player_2.user_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['player_1']['nickname'], match.player_1.nickname)
        self.assertEqual(body['player_2']['nickname'], match.player_2.nickname)
        self.assertEqual(body['status'], 'In progress')
        self.assertEqual(body['player_1_score'], 0)
        self.assertEqual(body['player_2_score'], 0)

    def test_start_match_not_found(self):
        tournament_id = 1

        response, body = self.start_match(tournament_id, 49, 50)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], ['Player does not exist'])

    def test_tournament_not_exist(self):
        tournament_id = 50

        response, body = self.start_match(tournament_id, 1, 2)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], ['Tournament with id `50` does not exist'])

    def test_invalid_body(self):
        response, body = self.start_match(1, 'test', 2)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['errors'], [error.MATCH_PLAYER_NOT_INT])


class EndMatchTest(TestCase):
    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def setUp(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (True, user, None)
        tournament = Tournament.objects.create(id=1, name='tournament 1', admin_id=1, max_players=8)

        for i in range(0, 8):
            Player.objects.create(
                id=i,
                nickname=f'player {i}',
                user_id=i,
                tournament=tournament,
            )

        url = reverse('generate-matches', args=(1,))

        response = self.client.post(url, {'random': True}, content_type='application/json', headers=get_fake_headers(1))

        json.loads(response.content.decode('utf8'))

        match = Match.objects.get(match_id=0, tournament_id=1)
        match.status = Match.IN_PROGRESS
        match.player_1_score = 5
        match.player_2_score = 3
        match.save()

        tournament.status = Tournament.IN_PROGRESS
        tournament.save()

    @patch('common.src.jwt_managers.ServiceAccessJWT.authenticate')
    def end_match(self, tournament_id, winner_id, mock_authenticate):
        mock_authenticate.return_value = (True, None)

        url = reverse('end-match', args=(tournament_id,))

        response = self.client.post(
            url,
            {
                'winner': winner_id
            },
            content_type='application/json'
        )

        body = json.loads(response.content.decode('utf8'))

        return response, body

    def test_end_match(self):
        match = Match.objects.get(match_id=0, tournament_id=1)

        response, body = self.end_match(1, match.player_1.user_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['player_1']['nickname'], match.player_1.nickname)
        self.assertEqual(body['player_2']['nickname'], match.player_2.nickname)
        self.assertEqual(body['status'], 'Finished')
        self.assertEqual(body['player_1_score'], 5)
        self.assertEqual(body['player_2_score'], 3)
        self.assertEqual(body['winner']['nickname'], match.player_1.nickname)

    def test_match_not_found(self):
        response, body = self.end_match(1, 49)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], ['Player does not exist'])

    def test_tournament_not_exist(self):
        response, body = self.end_match(50, 1)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], ['Tournament with id `50` does not exist'])

    def test_invalid_body(self):
        response, body = self.end_match(1, 'test')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['errors'], [error.MATCH_WINNER_NOT_INT])


class AddPointTest(TestCase):
    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def setUp(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (True, user, None)
        tournament = Tournament.objects.create(id=1, name='tournament 1', admin_id=1, max_players=8)

        for i in range(0, 8):
            Player.objects.create(
                id=i,
                nickname=f'player {i}',
                user_id=i,
                tournament=tournament,
            )

        url = reverse('generate-matches', args=(1,))

        response = self.client.post(url, {'random': True}, content_type='application/json', headers=get_fake_headers(1))

        json.loads(response.content.decode('utf8'))

        match = Match.objects.get(match_id=0, tournament_id=1)
        match.status = Match.IN_PROGRESS
        match.player_1_score = 0
        match.player_2_score = 0
        match.save()

        tournament.status = Tournament.IN_PROGRESS
        tournament.save()

    @patch('common.src.jwt_managers.ServiceAccessJWT.authenticate')
    def add_point(self, tournament_id, player_id, mock_authenticate):
        mock_authenticate.return_value = (True, None)

        url = reverse('add-point', args=(tournament_id,))

        response = self.client.post(
            url,
            {
                'player': player_id
            },
            content_type='application/json'
        )

        body = json.loads(response.content.decode('utf8'))

        return response, body

    def test_add_point(self):
        match = Match.objects.get(match_id=0, tournament_id=1)

        response, body = self.add_point(1, match.player_1.user_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['player_1']['nickname'], match.player_1.nickname)
        self.assertEqual(body['player_2']['nickname'], match.player_2.nickname)
        self.assertEqual(body['status'], 'In progress')
        self.assertEqual(body['player_1_score'], 1)
        self.assertEqual(body['player_2_score'], 0)

    def test_add_point_second_player(self):
        match = Match.objects.get(match_id=0, tournament_id=1)

        response, body = self.add_point(1, match.player_2.user_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['player_1']['nickname'], match.player_1.nickname)
        self.assertEqual(body['player_2']['nickname'], match.player_2.nickname)
        self.assertEqual(body['status'], 'In progress')
        self.assertEqual(body['player_1_score'], 0)
        self.assertEqual(body['player_2_score'], 1)

    def test_add_many_point(self):
        match = Match.objects.get(match_id=0, tournament_id=1)

        for i in range(0, 5):
            response, body = self.add_point(1, match.player_1.user_id)
        for i in range(0, 3):
            response, body = self.add_point(1, match.player_2.user_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['player_1']['nickname'], match.player_1.nickname)
        self.assertEqual(body['player_2']['nickname'], match.player_2.nickname)
        self.assertEqual(body['status'], 'In progress')
        self.assertEqual(body['player_1_score'], 5)
        self.assertEqual(body['player_2_score'], 3)

    def test_match_not_found(self):
        response, body = self.add_point(1, 49)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], ['Player does not exist'])

    def test_tournament_not_found(self):
        response, body = self.add_point(50, 1)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], ['Tournament with id `50` does not exist'])

    def test_invalid_body(self):
        response, body = self.add_point(1, 'test')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['errors'], [error.MATCH_PLAYER_NOT_INT])
