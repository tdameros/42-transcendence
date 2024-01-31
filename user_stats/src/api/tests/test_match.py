import json

from dateutil import parser
from django.test import TestCase
from django.urls import reverse

import api.error_message as error
from api.models import Match, User


class MatchTest(TestCase):
    def post_match(self, body):
        url = reverse('match')
        response = self.client.post(url, json.dumps(body), content_type='application/json')
        return response

    def assert_match_integrity(self, body):
        winner_id = body.get('winner_id')
        loser_id = body.get('loser_id')
        winner_score = body.get('winner_score')
        loser_score = body.get('loser_score')
        date = body.get('date')
        winner_before = User.objects.get(pk=winner_id)
        loser_before = User.objects.get(pk=loser_id)
        response = self.post_match(body)
        self.assertEqual(response.status_code, 201)
        match1 = Match.objects.get(pk=response.json()['winner_match_id'])
        match2 = Match.objects.get(pk=response.json()['loser_match_id'])
        winner = User.objects.get(pk=winner_id)
        loser = User.objects.get(pk=loser_id)

        self.assertEqual(match1.user_id, winner_id)
        self.assertEqual(match1.opponent_id, loser_id)
        self.assertEqual(match1.user_score, winner_score)
        self.assertEqual(match1.opponent_score, loser_score)
        self.assertEqual(match1.result, True)
        self.assertEqual(match1.user_elo, winner.elo - match1.user_elo_delta)
        self.assertEqual(match1.user_win_rate, winner_before.win_rate)
        self.assertEqual(match1.user_matches_played, winner_before.matches_played)
        self.assertEqual(match1.date, parser.isoparse(date))

        self.assertEqual(match2.user_id, loser_id )
        self.assertEqual(match2.opponent_id, winner_id)
        self.assertEqual(match2.user_score, loser_score)
        self.assertEqual(match2.opponent_score, winner_score)
        self.assertEqual(match2.result, False)
        self.assertEqual(match2.user_elo, loser.elo - match2.user_elo_delta)
        self.assertEqual(match2.user_win_rate, loser_before.win_rate)
        self.assertEqual(match2.user_matches_played, loser_before.matches_played)
        self.assertEqual(match2.date, parser.isoparse(date))



class PostMatch(MatchTest):
    def setUp(self):
        User.objects.create(
            id=1,
            elo=1000,
            matches_played=0,
            matches_won=0,
            matches_lost=0,
            win_rate=0,
            friends=0
        )
        User.objects.create(
            id=2,
            elo=1200,
            matches_played=0,
            matches_won=0,
            matches_lost=0,
            win_rate=0,
            friends=0
        )

    def test_valid_match(self):
        body = {
            'winner_id': 1,
            'loser_id': 2,
            'winner_score': 10,
            'loser_score': 5,
            'date': '2021-01-01T00:00:00Z'
        }
        self.assert_match_integrity(body)
        body['winner_score'] = 1000
        body['loser_score'] = 999
        self.assert_match_integrity(body)
        body['date'] = '2021-01-01T00:00:01+10'
        self.assert_match_integrity(body)
        User.objects.create(
            id=3,
            elo=100,
            matches_played=50,
            matches_won=20,
            matches_lost=30,
            win_rate=0.4,
            friends=1000
        )
        body['winner_id'] = 3
        self.assert_match_integrity(body)

    def test_invalid_match_id(self):
        body = {
            'winner_id': 3,
            'loser_id': 2,
            'winner_score': 10,
            'loser_score': 5,
            'date': '2021-01-01T00:00:00Z'
        }
        response = self.post_match(body)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.USER_NOT_FOUND])

        body['winner_id'] = 1
        body['loser_id'] = 3
        response = self.post_match(body)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.USER_NOT_FOUND])

    def test_invalid_match_score(self):
        body = {
            'winner_id': 1,
            'loser_id': 2,
            'winner_score': -1,
            'loser_score': 1,
            'date': '2021-01-01T00:00:00Z'
        }

        response = self.post_match(body)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.SCORE_INVALID])

        body['winner_score'] = 0
        body['loser_score'] = -1
        response = self.post_match(body)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.SCORE_INVALID])

    def test_invalid_match_date(self):
        body = {
            'winner_id': 1,
            'loser_id': 2,
            'winner_score': 10,
            'loser_score': 5,
            'date': 'abc'
        }
        response = self.post_match(body)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.DATE_INVALID])

        body['date'] = '2021-01-01T00:00:00Zaaa'
        response = self.post_match(body)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.DATE_INVALID])

        body['date'] = '2021-01-01aa00:00:00Z'
        response = self.post_match(body)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.DATE_INVALID])

        body['date'] = '900-01-01T00:00:00Z'
        response = self.post_match(body)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.DATE_INVALID])

        body['date'] = '10000-01-01T00:00:00Z'
        response = self.post_match(body)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], [error.DATE_INVALID])

    def test_invalid_match_body(self):
        body = {
            'winner_id': 1,
            'loser_id': 2,
            'winner_score': 10,
            'loser_score': 5,
            'date': '2021-01-01T00:00:00Z'
        }
        for key in body.keys():
            body_copy = body.copy()
            del body_copy[key]
            response = self.post_match(body_copy)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json()['errors'],
                [
                    error.SCORE_REQUIRED if key == 'winner_score' or key == 'loser_score'
                    else error.USER_ID_REQUIRED if key == 'winner_id' or key == 'loser_id'
                    else error.DATE_REQUIRED
                ])

    def test_invalid_match_body_type(self):
        body = {
            'winner_id': 1,
            'loser_id': 2,
            'winner_score': 10,
            'loser_score': 5,
            'date': '2021-01-01T00:00:00Z'
        }
        for key in body.keys():
            body_copy = body.copy()
            body_copy[key] = 'abc'
            response = self.post_match(body_copy)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json()['errors'],
                [
                    error.SCORE_INVALID if key == 'winner_score' or key == 'loser_score'
                    else error.USER_ID_INVALID if key == 'winner_id' or key == 'loser_id'
                    else error.DATE_INVALID
                ])

    def test_invalid_match_body_value(self):
        body = {
            'winner_id': 1,
            'loser_id': 2,
            'winner_score': 10,
            'loser_score': 5,
            'date': '2021-01-01T00:00:00Z'
        }
        for key in body.keys():
            body_copy = body.copy()
            if key == 'winner_id' or key == 'loser_id':
                body_copy[key] = -1
            elif key == 'winner_score' or key == 'loser_score':
                body_copy[key] = -1
            else:
                body_copy[key] = '2021-01-01T00:00:00Zaaa'
            response = self.post_match(body_copy)
            self.assertEqual(response.status_code, 400)
            self.assertEqual(
                response.json()['errors'],
                [
                    error.SCORE_INVALID if key == 'winner_score' or key == 'loser_score'
                    else error.USER_ID_INVALID if key == 'winner_id' or key == 'loser_id'
                    else error.DATE_INVALID
                ])
