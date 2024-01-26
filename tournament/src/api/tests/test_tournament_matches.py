import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from api.models import Match, Player, Tournament


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

        response = self.client.post(url, {'random': is_random}, content_type='application/json')

        body = json.loads(response.content.decode('utf8'))

        return response, body

    @patch('api.views.generate_matches_views.authenticate_request')
    def test_full_tournament(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (user, None)

        tournament_id = 1

        response, body = self.generate_matches(tournament_id, True)

        matches = Match.objects.filter(tournament_id=tournament_id)

        if response.status_code != 200:
            print(body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['nb-matches'], 4)
        self.assertEqual(len(body['matches']), 4)
        self.assertEqual(len(matches), 4)

    @patch('api.views.generate_matches_views.authenticate_request')
    def test_tournament_not_full(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (user, None)

        tournament_id = 2

        response, body = self.generate_matches(tournament_id, True)

        if response.status_code != 200:
            print(body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['nb-matches'], 4)
        self.assertEqual(len(body['matches']), 4)

    @patch('api.views.generate_matches_views.authenticate_request')
    def test_tournament_does_not_exist(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (user, None)

        tournament_id = 3

        response, body = self.generate_matches(tournament_id, True)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], ['tournament with id `3` does not exist'])


class MatchesTest(TestCase):
    def setUp(self):
        tournament = Tournament.objects.create(name='tournament 1', admin_id=1, max_players=8)

        for i in range(0, 8):
            Player.objects.create(nickname=f'player {i}', user_id=i, tournament=tournament)
        players = tournament.players.all()

        for i in range(0, 4):
            Match.objects.create(player_1=players[i], player_2=players[i + 4], tournament=tournament, match_id=i + 1)

    @patch('api.views.matches_views.authenticate_request')
    def test_get_matches(self, mock_authenticate):
        user = {'id': 1}
        mock_authenticate.return_value = (user, None)

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

    @patch('api.views.matches_views.authenticate_request')
    def test_tournament_not_exist(self, mock_authenticate):
        user = {'id': 1}
        mock_authenticate.return_value = (user, None)

        tournament_id = 50
        url = reverse('matches', args=(tournament_id,))
        response = self.client.get(url)
        body = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], ['tournament with id `50` does not exist'])


class GetMatchTest(TestCase):
    def setUp(self):
        tournament = Tournament.objects.create(name='tournament 1', admin_id=1, max_players=8)

        for i in range(0, 8):
            Player.objects.create(nickname=f'player {i}', user_id=i, tournament=tournament)
        players = tournament.players.all()

        for i in range(0, 4):
            Match.objects.create(player_1=players[i], player_2=players[i + 4], tournament=tournament, match_id=i + 1)

    @patch('api.views.matches_views.authenticate_request')
    def test_get_match(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (user, None)

        tournament_id = 1
        match_id = 1
        url = reverse('manage-match', args=(tournament_id, match_id))
        response = self.client.get(url)
        body = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['id'], 1)
        self.assertEqual(body['status'], 'Not played')
        self.assertEqual(body['player_1']['nickname'], 'player 0')
        self.assertEqual(body['player_2']['nickname'], 'player 4')

    @patch('api.views.matches_views.authenticate_request')
    def test_match_does_not_exist(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (user, None)

        tournament_id = 1
        match_id = 50
        url = reverse('manage-match', args=(tournament_id, match_id))
        response = self.client.get(url)
        body = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], ['match with id `50` does not exist'])

    @patch('api.views.matches_views.authenticate_request')
    def test_tournament_does_not_exist(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (user, None)

        tournament_id = 50
        match_id = 1
        url = reverse('manage-match', args=(tournament_id, match_id))
        response = self.client.get(url)
        body = json.loads(response.content.decode('utf8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], ['match with id `1` does not exist'])


class UpdateMatchTest(TestCase):
    def setUp(self):
        tournament = Tournament.objects.create(name='tournament 1', admin_id=1, max_players=8)

        for i in range(0, 8):
            Player.objects.create(nickname=f'player {i}', user_id=i, tournament=tournament)
        players = tournament.players.all()

        for i in range(0, 4):
            Match.objects.create(player_1=players[i], player_2=players[i + 4], tournament=tournament, match_id=i + 1)

    def update_match(self, tournament_id, match_id, body):
        url = reverse('manage-match', args=(tournament_id, match_id))
        response = self.client.patch(url, body, content_type='application/json')
        body = json.loads(response.content.decode('utf8'))

        return response, body

    @patch('api.views.matches_views.authenticate_request')
    def test_update_status(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (user, None)

        response, body = self.update_match(1, 1, {'status': Match.IN_PROGRESS})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['id'], 1)
        self.assertEqual(body['status'], 'In progress')
        self.assertEqual(body['player_1']['nickname'], 'player 0')
        self.assertEqual(body['player_2']['nickname'], 'player 4')

    @patch('api.views.matches_views.authenticate_request')
    def test_update_status_not_played(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (user, None)

        response, body = self.update_match(1, 1, {'status': Match.NOT_PLAYED})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['id'], 1)
        self.assertEqual(body['status'], 'Not played')
        self.assertEqual(body['player_1']['nickname'], 'player 0')
        self.assertEqual(body['player_2']['nickname'], 'player 4')

    @patch('api.views.matches_views.authenticate_request')
    def test_update_status_finished(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (user, None)

        response, body = self.update_match(1, 1, {'status': Match.FINISHED})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['id'], 1)
        self.assertEqual(body['status'], 'Finished')
        self.assertEqual(body['player_1']['nickname'], 'player 0')
        self.assertEqual(body['player_2']['nickname'], 'player 4')

    @patch('api.views.matches_views.authenticate_request')
    def test_update_player_1(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (user, None)

        response, body = self.update_match(1, 1, {'player_1': 2})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['id'], 1)
        self.assertEqual(body['status'], 'Not played')
        self.assertEqual(body['player_1']['nickname'], 'player 1')
        self.assertEqual(body['player_2']['nickname'], 'player 4')

    @patch('api.views.matches_views.authenticate_request')
    def test_update_player_2(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (user, None)

        response, body = self.update_match(1, 1, {'player_2': 6})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['id'], 1)
        self.assertEqual(body['status'], 'Not played')
        self.assertEqual(body['player_1']['nickname'], 'player 0')
        self.assertEqual(body['player_2']['nickname'], 'player 5')

    @patch('api.views.matches_views.authenticate_request')
    def test_update_both_players(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (user, None)

        response, body = self.update_match(1, 1, {'player_1': 2, 'player_2': 6})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['id'], 1)
        self.assertEqual(body['status'], 'Not played')
        self.assertEqual(body['player_1']['nickname'], 'player 1')
        self.assertEqual(body['player_2']['nickname'], 'player 5')
