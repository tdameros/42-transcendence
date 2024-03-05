import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from api.models import User

NOW = timezone.now()


class GraphTest(TestCase):
    def get_graph(self, user_id, start, end, max_points):
        url_elo = reverse('user_graph_elo', kwargs={'user_id': user_id})
        url_win_rate = reverse('user_graph_win_rate', kwargs={'user_id': user_id})
        url_matches_played = reverse('user_graph_matches_played', kwargs={'user_id': user_id})
        query = {
            'start': start,
            'end': end,
            'max_points': max_points,
        }
        if start is None:
            del query['start']
        if end is None:
            del query['end']
        if max_points is None:
            del query['max_points']
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
    def test_valid_many_matches(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        data = {
            'winner_id': 1,
            'loser_id': 2,
            'winner_score': 2,
            'loser_score': 1,
        }
        for i in range(11):
            data['date'] = (NOW - timezone.timedelta(days=10 - i)).isoformat()
            self.post_match(data)
        response_elo, response_win_rate, response_matches_played = self.get_graph(
            1,
            NOW - timezone.timedelta(days=7),
            NOW,
            7
        )
        self.assertEqual(response_elo.status_code, 200)
        self.assertEqual(response_win_rate.status_code, 200)
        self.assertEqual(response_matches_played.status_code, 200)
        body = response_elo.json()
        last_elo = None
        for value in body['graph']:
            if last_elo is not None:
                self.assertGreaterEqual(value['value'], last_elo)
            last_elo = value['value']
        body = response_win_rate.json()
        last_value = None
        for value in body['graph']:
            if last_value is not None:
                self.assertGreaterEqual(value['value'], last_value)
            last_value = value['value']
        body = response_matches_played.json()
        for value in body['graph']:
            self.assertEqual(value['value'], 1)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_many_daily_matches(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        data = {
            'winner_id': 1,
            'loser_id': 2,
            'winner_score': 2,
            'loser_score': 1,
        }
        date = NOW - timezone.timedelta(days=2)
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        for i in range(10):
            date = date.replace(hour=i)
            data['date'] = date.isoformat()
            self.post_match(data)
        date = NOW - timezone.timedelta(days=1)
        data['date'] = date.isoformat()
        self.post_match(data)
        start = NOW - timezone.timedelta(days=2)
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timezone.timedelta(days=7)
        response_elo, response_win_rate, response_matches_played = self.get_graph(
            1,
            start,
            end,
            7
        )
        self.assertEqual(response_elo.status_code, 200)
        self.assertEqual(response_win_rate.status_code, 200)
        self.assertEqual(response_matches_played.status_code, 200)
        body = response_matches_played.json()
        self.assertEqual(body['num_points'], 7)
        self.assertEqual(len(body['graph']), 7)
        self.assertEqual(body['graph'][0]['value'], 10)

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
    def test_invalid_max_points(self, mock_authenticate):
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
    def test_invalid_start_end_max_points(self, mock_authenticate):
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
        body = response_elo.json()
        num_points = body['num_points']
        graph = body['graph']
        self.assertEqual(num_points, 1)
        self.assertEqual(len(graph), num_points)
        self.assertEqual(graph[0]['value'], 1000)
        body = response_win_rate.json()
        num_points = body['num_points']
        graph = body['graph']
        self.assertEqual(num_points, 1)
        self.assertEqual(len(graph), num_points)
        self.assertEqual(graph[0]['value'], 0)
        body = response_matches_played.json()
        num_points = body['num_points']
        graph = body['graph']
        self.assertEqual(num_points, 7)
        self.assertEqual(len(graph), num_points)
        for value in graph:
            self.assertEqual(value['value'], 0)

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
        body = response_elo.json()
        num_points = body['num_points']
        graph = body['graph']
        self.assertEqual(num_points, 1)
        self.assertEqual(len(graph), num_points)
        self.assertEqual(graph[0]['value'], 1000)

        self.assertEqual(response_win_rate.status_code, 200)
        body = response_win_rate.json()
        num_points = body['num_points']
        graph = body['graph']
        self.assertEqual(num_points, 1)
        self.assertEqual(len(graph), num_points)
        self.assertEqual(graph[0]['value'], 0)

        self.assertEqual(response_matches_played.status_code, 200)
        body = response_matches_played.json()
        num_points = body['num_points']
        graph = body['graph']
        self.assertEqual(num_points, 7)
        self.assertEqual(len(graph), num_points)
        for value in graph:
            self.assertEqual(value['value'], 0)

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
        body = response_elo.json()
        num_points = body['num_points']
        graph = body['graph']
        self.assertEqual(num_points, 1)
        self.assertEqual(len(graph), num_points)
        self.assertGreater(graph[0]['value'], 1000)

        self.assertEqual(response_win_rate.status_code, 200)
        body = response_win_rate.json()
        num_points = body['num_points']
        graph = body['graph']
        self.assertEqual(num_points, 1)
        self.assertEqual(len(graph), num_points)
        self.assertEqual(graph[0]['value'], 100)

        self.assertEqual(response_matches_played.status_code, 200)
        body = response_matches_played.json()
        num_points = body['num_points']
        graph = body['graph']
        self.assertEqual(num_points, 7)
        self.assertEqual(len(graph), num_points)
        for value in graph:
            self.assertEqual(value['value'], 0)
