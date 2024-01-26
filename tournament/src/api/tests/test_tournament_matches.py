import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from api.models import Match, Player, Tournament


class GenerateTournamentMatches(TestCase):
    def setUp(self):
        tournament = Tournament.objects.create(name='tournament 1', admin_id=1, max_players=8)
        tournament_not_full = Tournament.objects.create(name='tournament 2', admin_id=1, max_players=8)

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

    @patch('api.views.tournament_matches_views.authenticate_request')
    def test_full_tournament(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (user, None)

        tournament_id = 1

        response, body = self.generate_matches(tournament_id, True)

        matches = Match.objects.filter(tournament_id=tournament_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['nb-matches'], 4)
        self.assertEqual(len(body['matches']), 4)
        self.assertEqual(len(matches), 4)

    @patch('api.views.tournament_matches_views.authenticate_request')
    def test_tournament_not_full(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (user, None)

        tournament_id = 2

        response, body = self.generate_matches(tournament_id, True)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['nb-matches'], 4)
        self.assertEqual(len(body['matches']), 4)

    @patch('api.views.tournament_matches_views.authenticate_request')
    def test_tournament_does_not_exist(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (user, None)

        tournament_id = 3

        response, body = self.generate_matches(tournament_id, True)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['errors'], ['tournament with id `3` does not exist'])
