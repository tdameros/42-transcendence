import json
from typing import Optional

from django.urls import reverse

import api.error_messages as error_messages
from api import settings
from api.PlayerManager import PlayerManager
from api.tests.utils.TestCaseNoDatabase import TestCaseNoDatabase
from common.src.jwt_managers import ServiceAccessJWT


class PostGetPlayersGamePortViewTest(TestCaseNoDatabase):
    def post_request(self,
                     request_body,
                     jwt: Optional[str]) -> (dict, int):
        url = reverse('get_players_game_port')
        if jwt is None:
            success, jwt, errors = ServiceAccessJWT.generate_jwt()
            if not success:
                raise Exception(f'Failed to generate jwt: {errors}')

        response = self.client.post(
            url,
            json.dumps(request_body),
            content_type='application/json',
            headers={'Authorization': jwt} if len(jwt) != 0 else None
        )

        response_content = response.content.decode('utf-8')
        return (json.loads(response_content) if len(response_content) > 0 else {},
                response.status_code)

    def run_test(self,
                 request_body,
                 expected_body,
                 expected_status,
                 jwt: Optional[str] = None):
        body, status = self.post_request(request_body, jwt)

        self.assertEqual(body, expected_body)

        self.assertEqual(status, expected_status)

    def test_valid_request(self):
        PlayerManager._users = {}
        player_1_port = 4242
        player_2_port = 42322
        PlayerManager.add_players([1], player_1_port)
        PlayerManager.add_players([2], player_2_port)
        self.run_test({
            'players': [1, 2, 3, 4, 4],
        }, {
            '1': player_1_port,
            '3': None,
            '2': player_2_port,
            '4': None,
        }, 200)

    def test_no_jwt(self):
        self.run_test({
            'players': [1, None, None, 4],
        }, {
            'errors': ["Invalid token type. Token must be a <class 'bytes'>"]
        }, 401, jwt='')

    def test_bad_jwt(self):
        self.run_test({
            'players': [1, None, None, 4],
        }, {
            'errors': ['Not enough segments']
        }, 401, jwt='badjwt')

    def test_invalid_json(self):
        self.run_test('invalid json', {
            'errors': [error_messages.BAD_JSON_FORMAT]
        }, 400)

    def test_missing_players(self):
        self.run_test({
        }, {
            'errors': [error_messages.PLAYERS_FIELD_MISSING]
        }, 400)

    def test_invalid_players_not_a_list(self):
        self.run_test({
            'game_id': 1,
            'players': 4,
            'request_issuer': settings.MATCHMAKING
        }, {
            'errors': [error_messages.PLAYERS_FIELD_IS_NOT_A_LIST]
        }, 400)

    def test_invalid_players_content(self):
        self.run_test({
            'game_id': 1,
            'players': ['invalid', 2, 4, None],
            'request_issuer': settings.TOURNAMENT
        }, {
            'errors': [error_messages.player_is_not_an_int(0),
                       error_messages.player_is_not_an_int(3)]
        }, 400)
