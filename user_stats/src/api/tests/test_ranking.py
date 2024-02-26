import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

import api.error_message as error
from api.models import Match, User


class RankingTest(TestCase):
    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def get_ranking(self, page, page_size, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        url = reverse('ranking')
        query = {}
        if page is not None:
            query.update({'page': page})
        if page_size is not None:
            query.update({'page_size': page_size})
        response = self.client.get(url, query)
        return response

    def create_user_range(self, nb_users: int):
        for i in range(nb_users):
            User.objects.create(
                id=i,
                elo=1000 + i,
                win_rate=50,
                matches_played=100,
            )

class GetRanking(RankingTest):
    def test_valid_single_page(self):
        self.create_user_range(10)
        response = self.get_ranking(1, 10)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(len(body['ranking']), 10)
        self.assertEqual(body['total_pages'], 1)
        elo = None
        for user in body['ranking']:
            if elo is not None:
                self.assertLessEqual(user['elo'], elo)
            elo = user['elo']
    def test_valid_multiple_pages(self):
        self.create_user_range(100)
        response = self.get_ranking(1, 10)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(len(body['ranking']), 10)
        self.assertEqual(body['total_pages'], 10)
        response = self.get_ranking(10, 10)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(len(body['ranking']), 10)
        self.assertEqual(body['total_pages'], 10)

    def test_valid_default(self):
        self.create_user_range(100)
        response = self.get_ranking(None, None)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(len(body['ranking']), 100)
        self.assertEqual(body['total_pages'], 1)

    def test_valid_page_size(self):
        self.create_user_range(100)
        response = self.get_ranking(1, 1)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(len(body['ranking']), 1)
        self.assertEqual(body['total_pages'], 100)
        response = self.get_ranking(1, 100)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(len(body['ranking']), 100)
        self.assertEqual(body['total_pages'], 1)

    def test_valid_no_user(self):
        response = self.get_ranking(None, None)
        self.assertEqual(response.status_code, 200)
        body = json.loads(response.content)
        self.assertEqual(len(body['ranking']), 0)
        self.assertEqual(body['ranking'], [])
        self.assertEqual(body['total_pages'], 1)

    def test_invalid_page(self):
        self.create_user_range(100)
        response = self.get_ranking(2, None)
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body['errors'], ['That page contains no results'])
        response = self.get_ranking(0, None)
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body['errors'], [error.PAGE_INVALID])
        response = self.get_ranking(-1, None)
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body['errors'], [error.PAGE_INVALID])
        response = self.get_ranking('a', None)
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body['errors'], [error.PAGE_INVALID])

    def test_invalid_page_size(self):
        self.create_user_range(100)
        response = self.get_ranking(None, 0)
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body['errors'], [error.PAGE_SIZE_INVALID])
        response = self.get_ranking(None, -1)
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body['errors'], [error.PAGE_SIZE_INVALID])
        response = self.get_ranking(None, 'a')
        self.assertEqual(response.status_code, 400)
        body = json.loads(response.content)
        self.assertEqual(body['errors'], [error.PAGE_SIZE_INVALID])

