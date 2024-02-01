import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

import api.error_message as error
from api.models import User


class ProgressTest(TestCase):
    def get_progress(self, user_id, days):
        url = reverse('user_progress', kwargs={'user_id': user_id})
        if days is not None:
            response = self.client.get(url, {'days': days})
        else:
            response = self.client.get(url)

        return response

    def post_match(self, body):
        url = reverse('match')
        response = self.client.post(url, json.dumps(body), content_type='application/json')
        return response

    def assert_progress_validity(self, user_id, elo, win_rate, matches_played, days=None):
        response = self.get_progress(user_id, days)
        self.assertEqual(response.status_code, 200)
        progress = response.json()['progress']
        if elo is not None:
            self.assertEqual(progress['elo'], elo)
        if win_rate is not None:
            self.assertEqual(progress['win_rate'], win_rate)
        if matches_played is not None:
            self.assertEqual(progress['matches_played'], matches_played)
        return progress


class GetProgress(ProgressTest):
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
    def test_valid_no_matches(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)

        self.assert_progress_validity(1, 0, 0, 0)
        self.assert_progress_validity(2, 0, 0, 0)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_single_match(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        date = timezone.now() - timezone.timedelta(days=1)
        body = {
            'winner_id': 1,
            'loser_id': 2,
            'winner_score': 2,
            'loser_score': 1,
            'date': date.isoformat(),
        }
        self.post_match(body)

        progress = self.assert_progress_validity(1, None, 1, 1)
        self.assertGreater(progress['elo'], 0)

        progress = self.assert_progress_validity(2, None, 0, 1)
        self.assertLess(progress['elo'], 0)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_multiple_matches(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        date = timezone.now() - timezone.timedelta(days=3)
        body = {
            'winner_id': 1,
            'loser_id': 2,
            'winner_score': 2,
            'loser_score': 1,
            'date': date.isoformat(),
        }
        self.post_match(body)
        date = timezone.now() - timezone.timedelta(days=2)
        body['date'] = date.isoformat()
        self.post_match(body)
        date = timezone.now() - timezone.timedelta(days=1)
        body['date'] = date.isoformat()
        self.post_match(body)

        progress = self.assert_progress_validity(1, None, 1, 3)
        self.assertGreater(progress['elo'], 0)

        progress = self.assert_progress_validity(2, None, 0, 3)
        self.assertLess(progress['elo'], 0)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_single_match_no_progress(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        date = timezone.now() - timezone.timedelta(days=8)
        body = {
            'winner_id': 1,
            'loser_id': 2,
            'winner_score': 1,
            'loser_score': 2,
            'date': date.isoformat(),
        }
        self.post_match(body)

        self.assert_progress_validity(1, 0, 0, 0)
        self.assert_progress_validity(2, 0, 0, 0)
        self.assert_progress_validity(1, 0, 0, 0, 0)
        self.assert_progress_validity(2, 0, 0, 0, 0)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_multiple_matches_no_progress(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        date = timezone.now() - timezone.timedelta(days=8)
        body = {
            'winner_id': 1,
            'loser_id': 2,
            'winner_score': 1,
            'loser_score': 2,
            'date': date.isoformat(),
        }
        self.post_match(body)
        date = timezone.now() - timezone.timedelta(days=9)
        body['date'] = date.isoformat()
        self.post_match(body)
        date = timezone.now() - timezone.timedelta(days=10)
        body['date'] = date.isoformat()
        self.post_match(body)

        self.assert_progress_validity(1, 0, 0, 0)
        self.assert_progress_validity(2, 0, 0, 0)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_mixed_matches_progress(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        date = timezone.now() - timezone.timedelta(days=10)
        body = {
            'winner_id': 1,
            'loser_id': 2,
            'winner_score': 1,
            'loser_score': 2,
            'date': date.isoformat(),
        }
        self.post_match(body)
        date = timezone.now() - timezone.timedelta(days=9)
        body['date'] = date.isoformat()
        self.post_match(body)
        date = timezone.now() - timezone.timedelta(days=8)
        body['date'] = date.isoformat()
        self.post_match(body)
        date = timezone.now() - timezone.timedelta(days=3)
        body['date'] = date.isoformat()
        self.post_match(body)
        date = timezone.now() - timezone.timedelta(days=2)
        body['date'] = date.isoformat()
        self.post_match(body)
        date = timezone.now() - timezone.timedelta(days=1)
        body['date'] = date.isoformat()
        self.post_match(body)

        progress = self.assert_progress_validity(1, None, 0, 3)
        self.assertGreater(progress['elo'], 0)
        progress = self.assert_progress_validity(2, None, 0, 3)
        self.assertLess(progress['elo'], 0)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_high_day_span(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        date = timezone.now() - timezone.timedelta(days=50)
        body = {
            'winner_id': 1,
            'loser_id': 2,
            'winner_score': 1,
            'loser_score': 2,
            'date': date.isoformat(),
        }
        self.post_match(body)
        date = timezone.now() - timezone.timedelta(days=10)
        body['date'] = date.isoformat()
        self.post_match(body)
        date = timezone.now() - timezone.timedelta(days=9)
        body['date'] = date.isoformat()
        self.post_match(body)
        date = timezone.now() - timezone.timedelta(days=8)
        body['date'] = date.isoformat()
        self.post_match(body)

        progress = self.assert_progress_validity(1, None, 0, 3, 11)
        self.assertGreater(progress['elo'], 0)
        progress = self.assert_progress_validity(2, None, 0, 3, 11)
        self.assertLess(progress['elo'], 0)

        progress = self.assert_progress_validity(1, None, 1, 4, 100)
        self.assertGreater(progress['elo'], 0)
        progress = self.assert_progress_validity(2, None, 0, 4, 100)
        self.assertLess(progress['elo'], 0)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_low_day_span(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        date = timezone.now() - timezone.timedelta(days=50)
        body = {
            'winner_id': 1,
            'loser_id': 2,
            'winner_score': 1,
            'loser_score': 2,
            'date': date.isoformat(),
        }
        self.post_match(body)
        date = timezone.now() - timezone.timedelta(days=3)
        body['date'] = date.isoformat()
        self.post_match(body)
        date = timezone.now() - timezone.timedelta(days=2)
        body['date'] = date.isoformat()
        self.post_match(body)

        progress = self.assert_progress_validity(1, None, 0, 2, 5)
        self.assertGreater(progress['elo'], 0)
        progress = self.assert_progress_validity(2, None, 0, 2, 5)
        self.assertLess(progress['elo'], 0)

        self.assert_progress_validity(1, 0, 0, 0, 1)
        self.assert_progress_validity(2, 0, 0, 0, 1)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_invalid_user_id(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        response = self.get_progress(4, None)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.USER_NOT_FOUND])

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_invalid_days(self, mock_authenticate):
        mock_authenticate.return_value = (True, {'id': 1}, None)
        response = self.get_progress(1, 'a')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.DAYS_INVALID])
        response = self.get_progress(1, -1)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.DAYS_INVALID])
        response = self.get_progress(1, 1.5)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.DAYS_INVALID])
