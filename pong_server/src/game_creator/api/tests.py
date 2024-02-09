import json
import os
import socket
from typing import Optional

from django.urls import reverse

import api.error_messages as error_messages
from game_creator.TestCaseNoDatabase import TestCaseNoDatabase
from shared_code import error_messages as shared_error_messages


class PostCreateGameTest(TestCaseNoDatabase):
    def setUp(self):
        self._port_min: Optional[str] = os.getenv('PONG_GAME_SERVERS_MIN_PORT')
        self._port_max: Optional[str] = os.getenv('PONG_GAME_SERVERS_MAX_PORT')
        self._app_path: Optional[str] = os.getenv('GAME_SERVER_PATH')

    def tearDown(self):
        if self._port_min:
            os.environ['PONG_GAME_SERVERS_MIN_PORT'] = self._port_min
        if self._port_max:
            os.environ['PONG_GAME_SERVERS_MAX_PORT'] = self._port_max
        if self._app_path:
            os.environ['GAME_SERVER_PATH'] = self._app_path

    def post_request(self, request_body) -> (dict, int):
        url = reverse('create_game')
        response = self.client.post(url,
                                    json.dumps(request_body),
                                    content_type='application/json')

        return json.loads(response.content.decode('utf-8')), response.status_code

    def set_env_var(self,
                    min_port: int,
                    max_port: Optional[int] = None,
                    app_path: Optional[str] = None):
        if max_port is None:
            max_port = min_port
        if app_path is None:
            app_path = self._app_path

        os.environ['PONG_GAME_SERVERS_MIN_PORT'] = str(min_port)
        os.environ['PONG_GAME_SERVERS_MAX_PORT'] = str(max_port)
        os.environ['GAME_SERVER_PATH'] = app_path

    def run_test(self, request_body, expected_body, expected_status):
        body, status = self.post_request(request_body)

        self.assertEqual(body, expected_body)

        self.assertEqual(status, expected_status)

    def test_valid_matchmaking_request(self):
        port = 4242
        self.set_env_var(port)

        self.run_test({
            'game_id': 1,
            'players': [1, 2],
            'request_issuer': 'matchmaking'
        }, {
            'game_server_uri': f'http://localhost:{port}'
        }, 201)

    def test_valid_tournament_request(self):
        port = 4243
        self.set_env_var(port)

        self.run_test({
            'game_id': 1,
            'players': [1, None, None, 4],
            'request_issuer': 'tournament'
        }, {
            'game_server_uri': f'http://localhost:{port}'
        }, 201)

    def test_invalid_json(self):
        self.run_test('invalid json', {
            'errors': [error_messages.BAD_JSON_FORMAT]
        }, 400)

    def test_missing_game_id(self):
        self.run_test({
            'players': [1, 2],
            'request_issuer': 'matchmaking'
        }, {
            'errors': [error_messages.GAME_ID_FIELD_MISSING]
        }, 400)

    def test_invalid_game_id(self):
        self.run_test({
            'game_id': 'invalid',
            'players': [1, 2],
            'request_issuer': 'matchmaking'
        }, {
            'errors': [error_messages.GAME_ID_FIELD_IS_NOT_AN_INTEGER]
        }, 400)

    def test_missing_players(self):
        self.run_test({
            'game_id': 1,
            'request_issuer': 'matchmaking'
        }, {
            'errors': [error_messages.PLAYERS_FIELD_MISSING]
        }, 400)

    def test_invalid_players_not_a_list(self):
        self.run_test({
            'game_id': 1,
            'players': 4,
            'request_issuer': 'matchmaking'
        }, {
            'errors': [error_messages.PLAYERS_FIELD_IS_NOT_A_LIST]
        }, 400)

    def test_invalid_players_content(self):
        self.run_test({
            'game_id': 1,
            'players': ['invalid', 2, 4, None],
            'request_issuer': 'matchmaking'
        }, {
            'errors': [error_messages.player_is_not_an_optional_int(0)]
        }, 400)

    def test_invalid_players_duplicate_id_in_content(self):
        player_id = 2
        self.run_test({
            'game_id': 1,
            'players': [player_id, player_id, player_id + 1, None],
            'request_issuer': 'matchmaking'
        }, {
            'errors': [error_messages.player_is_found_multiple_times(player_id)]
        }, 400)

    def test_invalid_players_pair_of_none(self):
        self.run_test({
            'game_id': 1,
            'players': [1, 2, None, None],
            'request_issuer': 'tournament'
        }, {
            'errors': [error_messages.BOTH_PLAYERS_ARE_NONE]
        }, 400)

    def test_invalid_players_only_one_valid_id(self):
        self.run_test({
            'game_id': 1,
            'players': [1, None],
            'request_issuer': 'tournament'
        }, {
            'errors': [error_messages.NEED_AT_LEAST_2_PLAYERS_THAT_ARENT_NONE]
        }, 400)

    def test_invalid_players_not_enough_players(self):
        self.run_test({
            'game_id': 1,
            'players': [1],
            'request_issuer': 'tournament'
        }, {
            'errors': [error_messages.NEED_AT_LEAST_2_PLAYERS_THAT_ARENT_NONE]
        }, 400)

    def test_invalid_players_empty_list(self):
        self.run_test({
            'game_id': 1,
            'players': [],
            'request_issuer': 'tournament'
        }, {
            'errors': [error_messages.NEED_AT_LEAST_2_PLAYERS_THAT_ARENT_NONE]
        }, 400)

    def test_players_size_not_power_of_2(self):
        self.run_test({
            'game_id': 1,
            'players': [1, 2, 3],
            'request_issuer': 'tournament'
        }, {
            'errors': [error_messages.LEN_PLAYERS_IS_NOT_A_POWER_OF_2]
        }, 400)

    def test_missing_request_issuer(self):
        self.run_test({
            'game_id': 1,
            'players': [1, 2]
        }, {
            'errors': [error_messages.REQUEST_ISSUER_FIELD_MISSING]
        }, 400)

    def test_invalid_request_issuer_not_a_string(self):
        self.run_test({
            'game_id': 1,
            'players': [1, 2],
            'request_issuer': 4
        }, {
            'errors': [error_messages.REQUEST_ISSUER_IS_NOT_A_STRING]
        }, 400)

    def test_invalid_request_issuer_not_valid(self):
        self.run_test({
            'game_id': 1,
            'players': [1, 2],
            'request_issuer': 'nope'
        }, {
            'errors': [error_messages.REQUEST_ISSUER_IS_NOT_VALID]
        }, 400)

    def test_no_ports_available(self):
        port = 43523
        self.set_env_var(port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', port))

        self.run_test({
            'game_id': 1,
            'players': [1, 2],
            'request_issuer': 'tournament'
        }, {
            'errors': [error_messages.error_creating_game_server(
                shared_error_messages.NO_AVAILABLE_PORTS)]
        }, 500)

        s.close()

    def test_popen_fails(self):
        invalid_path = '/1nval1d/p@th/'
        self.set_env_var(6567, app_path=invalid_path)

        self.run_test({
            'game_id': 1,
            'players': [1, 2],
            'request_issuer': 'tournament'
        }, {
            'errors': [error_messages.popen_failed_to_run_command(
                f"[Errno 2] No such file or directory: '{invalid_path}'")]
        }, 500)
