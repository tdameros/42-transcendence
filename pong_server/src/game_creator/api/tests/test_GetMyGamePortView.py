import base64
import json
from unittest.mock import patch

from django.urls import reverse

from api.PlayerManager import PlayerManager
from api.tests.utils.TestCaseNoDatabase import TestCaseNoDatabase


class GetMyGamePortViewTest(TestCaseNoDatabase):
    def get_request(self, authorization: str = '') -> (dict, int):
        url = reverse('get_my_game_port')
        response = self.client.get(url, headers={'Authorization': authorization})

        response_content = response.content.decode('utf-8')
        return (json.loads(response_content) if len(response_content) > 0 else {},
                response.status_code)

    def run_test(self,
                 expected_body,
                 expected_status,
                 payload=None):
        if payload is None:
            payload = {}
        jwt = 'junk.' + base64.b64encode(json.dumps(payload).encode('utf-8')).decode('utf-8')
        body, status = self.get_request(authorization=jwt)

        self.assertEqual(status, expected_status)
        self.assertEqual(body, expected_body)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_request_player_in_game(self, mock_authenticate):
        PlayerManager.clear()
        player_id = 1
        port = 4242
        PlayerManager.add_players([player_id], port)
        payload = {'user_id': player_id}
        mock_authenticate.return_value = (True, payload, None)

        self.run_test({'port': port}, 200, payload)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_valid_request_player_not_in_game(self, mock_authenticate):
        PlayerManager.clear()
        payload = {'user_id': 1}
        mock_authenticate.return_value = (True, payload, None)

        self.run_test({'port': None}, 200, payload)

    @patch('common.src.jwt_managers.UserAccessJWTDecoder.authenticate')
    def test_bad_jwt(self, mock_authenticate):
        error_msgs = ['Invalid token type. Token must be a <class \'bytes\'>']
        mock_authenticate.return_value = (False, None, error_msgs)

        self.run_test({'errors': error_msgs}, 401)
