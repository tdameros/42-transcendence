import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

import api.error_message as error
from api.models import Match, User


class HistoryTest(TestCase):
    def get_history(self, user_id, page=1, page_size=10):
        url = reverse('user_history', kwargs={'user_id': user_id})
        response = self.client.get(url, {'page': page, 'page_size': page_size})
        return response

    def post_match(self, body):
        url = reverse('match')
        response = self.client.post(url, json.dumps(body), content_type='application/json')
        return response


class GetHistory(HistoryTest):
    def setUp(self):
        User.objects.create(
            id=1,
            elo=1000,
        )
        User.objects.create(
            id=2,
            elo=1100,
        )
        User.objects.create(
            id=3,
            elo=1300,
        )
        body = {
            'winner_id': 1,
            'loser_id': 2,
            'winner_score': 10,
            'loser_score': 8,
            'date': '2020-01-01T00:00:00+00:00',
        }
        self.post_match(body)
        body['loser_id'] = 3
        body['date'] = '2020-01-02T00:00:00+00:00'
        self.post_match(body)
        body['winner_id'] = 2
        body['loser_id'] = 1
        body['date'] = '2020-01-03T00:00:00+00:00'
        self.post_match(body)
        body['loser_id'] = 3
        body['date'] = '2020-01-04T00:00:00+00:00'
        self.post_match(body)
        body['winner_id'] = 3
        body['loser_id'] = 1
        body['date'] = '2020-01-05T00:00:00+00:00'
        self.post_match(body)
        body['loser_id'] = 2
        body['date'] = '2020-01-06T00:00:00+00:00'
        self.post_match(body)

    def tearDown(self):
        Match.objects.all().delete()
        User.objects.all().delete()

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_default(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        response = self.get_history(1)
        history = response.json()['history']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(history), 4)
        response = self.get_history(2)
        history = response.json()['history']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(history), 4)
        response = self.get_history(3)
        history = response.json()['history']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(history), 4)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_page(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        response = self.get_history(1, page=1, page_size=2)
        history = response.json()['history']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(history), 2)
        response = self.get_history(1, page=2, page_size=2)
        history = response.json()['history']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(history), 2)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_no_match(self, mock_authenticate):
        Match.objects.all().delete()
        mock_authenticate.return_value = (True, {'id': 1}, None)
        response = self.get_history(1, page=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['history'], [])
        self.assertEqual(response.json()['total_pages'], 1)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_total_pages(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        response = self.get_history(1, page_size=2)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_pages'], 2)
        response = self.get_history(1, page_size=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_pages'], 4)
        body = {
            'winner_id': 1,
            'loser_id': 2,
            'winner_score': 10,
            'loser_score': 8,
            'date': '2020-01-01T00:00:00+00:00',
        }
        for i in range(20):
            self.post_match(body)
        response = self.get_history(1, page_size=10)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_pages'], 3)
        response = self.get_history(1, page_size=5)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_pages'], 5)
        response = self.get_history(1, page_size=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total_pages'], 24)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_invalid_user_id(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        response = self.get_history(4)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'][0], error.USER_NOT_FOUND)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_invalid_page(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        response = self.get_history(1, page=2)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'][0], 'That page contains no results')
        response = self.get_history(1, page=0)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'][0], 'page invalid')
        response = self.get_history(1, page=-1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'][0], 'page invalid')
        response = self.get_history(1, page='test')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'][0], 'page invalid')

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_invalid_page_size(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        response = self.get_history(1, page_size=0)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'][0], 'page_size invalid')
        response = self.get_history(1, page_size=-1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'][0], 'page_size invalid')
        response = self.get_history(1, page_size='test')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'][0], 'page_size invalid')

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_history(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        response = self.get_history(1)
        history = response.json()['history']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(history), 4)
        self.assertEqual(history[0]['opponent_id'], 3)
        self.assertEqual(history[0]['date'], '2020-01-05T00:00:00+00:00')
        self.assertEqual(history[0]['result'], False)
        self.assertEqual(history[0]['user_score'], 8)
        self.assertEqual(history[0]['opponent_score'], 10)
        self.assertEqual(history[1]['opponent_id'], 2)
        self.assertEqual(history[1]['date'], '2020-01-03T00:00:00+00:00')
        self.assertEqual(history[1]['result'], False)
        self.assertEqual(history[1]['user_score'], 8)
        self.assertEqual(history[1]['opponent_score'], 10)
        self.assertEqual(history[2]['opponent_id'], 3)
        self.assertEqual(history[2]['date'], '2020-01-02T00:00:00+00:00')
        self.assertEqual(history[2]['result'], True)
        self.assertEqual(history[2]['user_score'], 10)
        self.assertEqual(history[2]['opponent_score'], 8)
        self.assertEqual(history[3]['opponent_id'], 2)
        self.assertEqual(history[3]['date'], '2020-01-01T00:00:00+00:00')
        self.assertEqual(history[3]['result'], True)
        self.assertEqual(history[3]['user_score'], 10)
        self.assertEqual(history[3]['opponent_score'], 8)
