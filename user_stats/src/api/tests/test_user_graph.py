import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from api.models import User

NOW = timezone.now()


class GraphTest(TestCase):
    def get_graph(self, user_id, start, end, num_points):
        url_elo = reverse('user_graph_elo', kwargs={'user_id': user_id})
        url_win_rate = reverse('user_graph_win_rate', kwargs={'user_id': user_id})
        url_matches_played = reverse('user_graph_matches_played', kwargs={'user_id': user_id})
        query = {
            'start': start,
            'end': end,
            'num_points': num_points,
        }
        if start is None:
            del query['start']
        if end is None:
            del query['end']
        if num_points is None:
            del query['num_points']
        response_elo = self.client.get(url_elo, query)
        response_win_rate = self.client.get(url_win_rate, query)
        response_matches_played = self.client.get(url_matches_played, query)

        return response_elo, response_win_rate, response_matches_played

    def post_match(self, body):
        url = reverse('match')
        response = self.client.post(url, json.dumps(body), content_type='application/json')
        return response

    def post_daily_matches(self):
        body = {
            'winner_id': 1,
            'loser_id': 2,
            'winner_score': 2,
            'loser_score': 1,
        }
        for i in range(7, 0, -1):
            date = NOW - timezone.timedelta(days=i)
            body['date'] = date.isoformat()
            self.post_match(body)


class GetGraph(GraphTest):
    def setUp(self):
        User.objects.create(
            id=1,
            elo=1000,
        )
        User.objects.create(
            id=2,
            elo=2000,
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_daily_graph(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        self.post_daily_matches()
        response_elo, response_win_rate, response_matches_played = self.get_graph(
            1,
            NOW - timezone.timedelta(days=7),
            NOW,
            7
        )
        self.assertEqual(response_elo.status_code, 200)
        self.assertEqual(response_win_rate.status_code, 200)
        self.assertEqual(response_matches_played.status_code, 200)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_invalid_user_id(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        response_elo, response_win_rate, response_matches_played = self.get_graph(
            3,
            NOW - timezone.timedelta(days=7),
            NOW,
            7
        )
        self.assertEqual(response_elo.status_code, 400)
        self.assertEqual(response_win_rate.status_code, 400)
        self.assertEqual(response_matches_played.status_code, 400)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_invalid_start(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        response_elo, response_win_rate, response_matches_played = self.get_graph(1, None, NOW, 7)
        self.assertEqual(response_elo.status_code, 400)
        self.assertEqual(response_win_rate.status_code, 400)
        self.assertEqual(response_matches_played.status_code, 400)
        response_elo, response_win_rate, response_matches_played = self.get_graph(1, 'abc', NOW, 7)
        self.assertEqual(response_elo.status_code, 400)
        self.assertEqual(response_win_rate.status_code, 400)
        self.assertEqual(response_matches_played.status_code, 400)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_invalid_end(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        response_elo, response_win_rate, response_matches_played = self.get_graph(
            1,
            NOW - timezone.timedelta(days=7),
            None,
            7
        )
        self.assertEqual(response_elo.status_code, 400)
        self.assertEqual(response_win_rate.status_code, 400)
        self.assertEqual(response_matches_played.status_code, 400)
        response_elo, response_win_rate, response_matches_played = self.get_graph(
            1,
            NOW - timezone.timedelta(days=7),
            'abc',
            7
        )
        self.assertEqual(response_elo.status_code, 400)
        self.assertEqual(response_win_rate.status_code, 400)
        self.assertEqual(response_matches_played.status_code, 400)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_invalid_num_points(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        response_elo, response_win_rate, response_matches_played = self.get_graph(
            1,
            NOW - timezone.timedelta(days=7),
            NOW,
            None
        )
        self.assertEqual(response_elo.status_code, 400)
        self.assertEqual(response_win_rate.status_code, 400)
        self.assertEqual(response_matches_played.status_code, 400)
        response_elo, response_win_rate, response_matches_played = self.get_graph(
            1,
            NOW - timezone.timedelta(days=7),
            NOW,
            'abc'
        )
        self.assertEqual(response_elo.status_code, 400)
        self.assertEqual(response_win_rate.status_code, 400)
        self.assertEqual(response_matches_played.status_code, 400)
        response_elo, response_win_rate, response_matches_played = self.get_graph(
            1, NOW - timezone.timedelta(days=7),
            NOW,
            -1
        )
        self.assertEqual(response_elo.status_code, 400)
        self.assertEqual(response_win_rate.status_code, 400)
        self.assertEqual(response_matches_played.status_code, 400)
        response_elo, response_win_rate, response_matches_played = self.get_graph(
            1,
            NOW - timezone.timedelta(days=7),
            NOW,
            0
        )
        self.assertEqual(response_elo.status_code, 400)
        self.assertEqual(response_win_rate.status_code, 400)
        self.assertEqual(response_matches_played.status_code, 400)
        response_elo, response_win_rate, response_matches_played = self.get_graph(
            1,
            NOW - timezone.timedelta(days=7),
            NOW,
            1
        )
        self.assertEqual(response_elo.status_code, 400)
        self.assertEqual(response_win_rate.status_code, 400)
        self.assertEqual(response_matches_played.status_code, 400)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_invalid_start_end(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        response_elo, response_win_rate, response_matches_played = self.get_graph(
            1,
            NOW,
            NOW - timezone.timedelta(days=7),
            7
        )
        self.assertEqual(response_elo.status_code, 400)
        self.assertEqual(response_win_rate.status_code, 400)
        self.assertEqual(response_matches_played.status_code, 400)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_invalid_start_end_num_points(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        response_elo, response_win_rate, response_matches_played = self.get_graph(
            1,
            NOW,
            NOW - timezone.timedelta(days=7),
            None
        )
        self.assertEqual(response_elo.status_code, 400)
        self.assertEqual(response_win_rate.status_code, 400)
        self.assertEqual(response_matches_played.status_code, 400)
        response_elo, response_win_rate, response_matches_played = self.get_graph(
            1,
            NOW,
            NOW - timezone.timedelta(days=7),
            'abc'
        )
        self.assertEqual(response_elo.status_code, 400)
        self.assertEqual(response_win_rate.status_code, 400)
        self.assertEqual(response_matches_played.status_code, 400)
        response_elo, response_win_rate, response_matches_played = self.get_graph(
            1,
            NOW,
            None,
            7
        )
        self.assertEqual(response_elo.status_code, 400)
        self.assertEqual(response_win_rate.status_code, 400)
        self.assertEqual(response_matches_played.status_code, 400)
        response_elo, response_win_rate, response_matches_played = self.get_graph(1, NOW, None, None)
        self.assertEqual(response_elo.status_code, 400)
        self.assertEqual(response_win_rate.status_code, 400)
        self.assertEqual(response_matches_played.status_code, 400)
        response_elo, response_win_rate, response_matches_played = self.get_graph(1, NOW, 'abc', 7)
        self.assertEqual(response_elo.status_code, 400)
        self.assertEqual(response_win_rate.status_code, 400)
        self.assertEqual(response_matches_played.status_code, 400)
        response_elo, response_win_rate, response_matches_played = self.get_graph(1, NOW, 'abc', 'abc')
        self.assertEqual(response_elo.status_code, 400)
        self.assertEqual(response_win_rate.status_code, 400)
        self.assertEqual(response_matches_played.status_code, 400)
        response_elo, response_win_rate, response_matches_played = self.get_graph(1, NOW, None, None)
        self.assertEqual(response_elo.status_code, 400)
        self.assertEqual(response_win_rate.status_code, 400)
        self.assertEqual(response_matches_played.status_code, 400)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_no_matches(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        response_elo, response_win_rate, response_matches_played = self.get_graph(
            1,
            NOW - timezone.timedelta(days=7),
            NOW,
            7)
        self.assertEqual(response_elo.status_code, 200)
        self.assertEqual(response_win_rate.status_code, 200)
        self.assertEqual(response_matches_played.status_code, 200)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_no_progress(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        self.post_daily_matches()
        response_elo, response_win_rate, response_matches_played = self.get_graph(
            1,
            NOW - timezone.timedelta(days=20),
            NOW - timezone.timedelta(days=10),
            7)
        self.assertEqual(response_elo.status_code, 200)
        self.assertEqual(response_win_rate.status_code, 200)
        self.assertEqual(response_matches_played.status_code, 200)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_no_progress_after_matches(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        self.post_match({
            'winner_id': 1,
            'loser_id': 2,
            'winner_score': 2,
            'loser_score': 1,
            'date': (NOW - timezone.timedelta(days=20)).isoformat(),
        })
        response_elo, response_win_rate, response_matches_played = self.get_graph(
            1,
            NOW - timezone.timedelta(days=7),
            NOW,
            7
        )
        self.assertEqual(response_elo.status_code, 200)
        self.assertEqual(response_win_rate.status_code, 200)
        self.assertEqual(response_matches_played.status_code, 200)
