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
        self._port_min = os.getenv('PONG_GAME_SERVERS_MIN_PORT')
        self._port_max = os.getenv('PONG_GAME_SERVERS_MAX_PORT')
        self._app_path = os.getenv('GAME_SERVER_PATH')

    def tearDown(self):
        os.environ['PONG_GAME_SERVERS_MIN_PORT'] = self._port_min
        os.environ['PONG_GAME_SERVERS_MAX_PORT'] = self._port_max
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

    def test_valid_matchmaking_request(self):
        port = 4242
        self.set_env_var(port)

        request_body = {
            'game_id': 1,
            'players': [1, None, 45, None],
            'request_issuer': 'matchmaking'
        }
        # TODO maybe disallow None and more than 2 players for matchmaking?

        body, status = self.post_request(request_body)

        self.assertEqual(status, 201)

        self.assertEqual(len(body), 1)
        self.assertEqual(body['game_server_uri'], f'http://localhost:{port}')

    def test_valid_tournament_request(self):
        port = 4243
        self.set_env_var(port)

        request_body = {
            'game_id': 1,
            'players': [1, None, 45, None, 3],
            'request_issuer': 'tournament'
        }

        body, status = self.post_request(request_body)

        self.assertEqual(status, 201)

        self.assertEqual(len(body), 1)
        self.assertEqual(body['game_server_uri'], f'http://localhost:{port}')

    def test_invalid_json(self):
        request_body = 'invalid json'

        body, status = self.post_request(request_body)

        self.assertEqual(status, 400)

        self.assertEqual(len(body), 1)
        self.assertEqual(body['errors'], [error_messages.BAD_JSON_FORMAT])

    def test_missing_game_id(self):
        request_body = {
            'players': [1, 2],
            'request_issuer': 'matchmaking'
        }

        body, status = self.post_request(request_body)

        self.assertEqual(status, 400)

        self.assertEqual(len(body), 1)
        self.assertEqual(body['errors'], [error_messages.GAME_ID_FIELD_MISSING])

    def test_invalid_game_id(self):
        request_body = {
            'game_id': 'invalid',
            'players': [1, 2],
            'request_issuer': 'matchmaking'
        }

        body, status = self.post_request(request_body)

        self.assertEqual(status, 400)

        self.assertEqual(len(body), 1)
        self.assertEqual(body['errors'], [error_messages.GAME_ID_FIELD_IS_NOT_AN_INTEGER])

    def test_missing_players(self):
        request_body = {
            'game_id': 1,
            'request_issuer': 'matchmaking'
        }

        body, status = self.post_request(request_body)

        self.assertEqual(status, 400)

        self.assertEqual(len(body), 1)
        self.assertEqual(body['errors'], [error_messages.PLAYERS_FIELD_MISSING])

    def test_invalid_players_not_a_list(self):
        request_body = {
            'game_id': 1,
            'players': 4,
            'request_issuer': 'matchmaking'
        }

        body, status = self.post_request(request_body)

        self.assertEqual(status, 400)

        self.assertEqual(len(body), 1)
        self.assertEqual(body['errors'], [error_messages.PLAYERS_FIELD_IS_NOT_A_LIST])

    def test_invalid_players_content(self):
        request_body = {
            'game_id': 1,
            'players': ['invalid', 2],
            'request_issuer': 'matchmaking'
        }

        body, status = self.post_request(request_body)

        self.assertEqual(status, 400)

        self.assertEqual(len(body), 1)
        self.assertEqual(body['errors'], [error_messages.player_is_not_an_optional_int(0)])

    def test_invalid_players_duplicate_id_in_content(self):
        player_id = 2
        request_body = {
            'game_id': 1,
            'players': [player_id, player_id],
            'request_issuer': 'matchmaking'
        }

        body, status = self.post_request(request_body)

        self.assertEqual(status, 400)

        self.assertEqual(len(body), 1)
        self.assertEqual(body['errors'],
                         [error_messages.player_is_found_multiple_times(player_id)])

    def test_missing_request_issuer(self):
        request_body = {
            'game_id': 1,
            'players': [1, 2]
        }

        body, status = self.post_request(request_body)

        self.assertEqual(status, 400)

        self.assertEqual(len(body), 1)
        self.assertEqual(body['errors'], [error_messages.REQUEST_ISSUER_FIELD_MISSING])

    def test_invalid_request_issuer_not_a_string(self):
        request_body = {
            'game_id': 1,
            'players': [1, 2],
            'request_issuer': 4
        }

        body, status = self.post_request(request_body)

        self.assertEqual(status, 400)

        self.assertEqual(len(body), 1)
        self.assertEqual(body['errors'], [error_messages.REQUEST_ISSUER_IS_NOT_A_STRING])

    def test_invalid_request_issuer_not_valid(self):
        request_body = {
            'game_id': 1,
            'players': [1, 2],
            'request_issuer': 'nope'
        }

        body, status = self.post_request(request_body)

        self.assertEqual(status, 400)

        self.assertEqual(len(body), 1)
        self.assertEqual(body['errors'], [error_messages.REQUEST_ISSUER_IS_NOT_VALID])

    def test_no_ports_available(self):
        port = 43523
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', port))

        self.set_env_var(port)

        request_body = {
            'game_id': 1,
            'players': [1, 2],
            'request_issuer': 'tournament'
        }

        body, status = self.post_request(request_body)
        s.close()

        self.assertEqual(status, 500)

        self.assertEqual(len(body), 1)
        self.assertEqual(body['errors'],
                         [error_messages.error_creating_game_server(
                             shared_error_messages.NO_AVAILABLE_PORTS)])

    def test_popen_fails(self):
        self.set_env_var(6567, app_path='/invalid_path/ewrfewgrebds')

        request_body = {
            'game_id': 1,
            'players': [1, 2],
            'request_issuer': 'tournament'
        }

        body, status = self.post_request(request_body)

        self.assertEqual(status, 500)

        self.assertEqual(len(body), 1)
        errno = "[Errno 2] No such file or directory: '/invalid_path/ewrfewgrebds'"
        self.assertEqual(body['errors'],
                         [error_messages.popen_failed_to_run_command(errno)])
