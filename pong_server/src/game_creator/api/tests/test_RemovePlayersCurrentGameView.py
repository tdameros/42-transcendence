import json
from typing import Optional

from django.urls import reverse

import api.error_messages as error_messages
from api.PlayerManager import PlayerManager
from api.tests.utils.TestCaseNoDatabase import TestCaseNoDatabase
from common.src.jwt_managers import ServiceAccessJWT


class PostRemovePlayersCurrentGameViewTest(TestCaseNoDatabase):
    def post_request(self,
                     request_body,
                     jwt: Optional[str],
                     reset_player_manager: bool) -> (dict, int):
        url = reverse('remove_players_current_game')
        if jwt is None:
            success, jwt, errors = ServiceAccessJWT.generate_jwt()
            if not success:
                raise Exception(f'Failed to generate jwt: {errors}')

        if reset_player_manager:
            PlayerManager.clear()

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
                 jwt: Optional[str] = None,
                 reset_player_manager: bool = True):
        body, status = self.post_request(request_body, jwt, reset_player_manager)

        self.assertEqual(status, expected_status)
        self.assertEqual(body, expected_body)

    def test_valid_request(self):
        PlayerManager.add_players([1], 4242)

        self.run_test({
            'players': [1, 2],
        }, {}, 204)

        self.assertEqual(PlayerManager.get_player_game_port(1), None)

    def test_valid_request_no_players_are_in_a_game(self):
        self.run_test({
            'players': [1, 2],
        }, {}, 204)

        self.assertEqual(PlayerManager.get_player_game_port(1), None)

    def test_no_jwt(self):
        self.run_test({
            'players': [1, 4],
        }, {
            'errors': ["Invalid token type. Token must be a <class 'bytes'>"]
        }, 401, jwt='')

    def test_bad_jwt(self):
        self.run_test({
            'players': [1, 4],
        }, {
            'errors': ['Not enough segments']
        }, 401, jwt='badjwt')

    def test_invalid_json(self):
        self.run_test('invalid json', {
            'errors': [error_messages.BAD_JSON_FORMAT]
        }, 400)

    def test_invalid_players_field_missing(self):
        self.run_test({}, {
            'errors': [error_messages.PLAYERS_FIELD_MISSING]
        }, 400)

    def test_invalid_players_not_a_list(self):
        self.run_test({
            'players': 4,
        }, {
            'errors': [error_messages.PLAYERS_FIELD_IS_NOT_A_LIST]
        }, 400)

    def test_invalid_players_content(self):
        self.run_test({
            'players': ['invalid', 2, 4, None],
        }, {
            'errors': [error_messages.player_is_not_an_int(0),
                       error_messages.player_is_not_an_int(3)]
        }, 400)
