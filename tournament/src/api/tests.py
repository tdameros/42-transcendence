import json

from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
from django.http import HttpRequest, HttpResponse

from tournament import settings
from api import error_message as error


class CreateTournamentTest(TestCase):
    def create_tournament(self, data: dict) -> tuple[HttpResponse, dict]:
        url = reverse('tournament')

        response = self.client.post(url, json.dumps(data), content_type='application/json')

        body = json.loads(response.content.decode('utf-8'))

        return response, body

    @patch('api.views.authenticate_request')
    def test_tournament_creation(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (user, None)

        data = {
            'name': 'World Championship',
            'max-players': 16,
            'registration-deadline': '2027-02-17T10:53:00Z',
            'is-private': True
        }

        response, body = self.create_tournament(data)

        if response.status_code != 201:
            print(body)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(body['name'], data['name'])
        self.assertEqual(body['max_players'], data['max-players'])
        self.assertEqual(body['registration_deadline'], data['registration-deadline'])
        self.assertEqual(body['is_private'], data['is-private'])
        self.assertEqual(body['admin_id'], 1)

    @patch('api.views.authenticate_request')
    def test_tournament_different_timezone(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (user, None)

        data = {
            'name': 'World Championship',
            'max-players': 16,
            'registration-deadline': '2027-01-06T07:38:51-07:00',
            'is-private': True
        }

        response, body = self.create_tournament(data)

        if response.status_code != 201:
            print(body)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(body['name'], data['name'])
        self.assertEqual(body['max_players'], data['max-players'])
        self.assertEqual(body['registration_deadline'], '2027-01-06T14:38:51Z')
        self.assertEqual(body['is_private'], data['is-private'])
        self.assertEqual(body['admin_id'], 1)

    @patch('api.views.authenticate_request')
    def test_tournament_without_optional_info(self, mock_get):
        user = {'id': 1}
        mock_get.return_value = (user, None)

        data = {
            'name': 'World Championship',
            'is-private': True
        }

        response, body = self.create_tournament(data)

        if response.status_code != 201:
            print(body)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(body['name'], data['name'])
        self.assertEqual(body['max_players'], settings.MAX_PLAYERS)
        self.assertEqual(body['registration_deadline'], None)
        self.assertEqual(body['is_private'], data['is-private'])
        self.assertEqual(body['admin_id'], 1)


class BadRequestCreateTournament(TestCase):
    def send_tournament_bad_request(self, mock_get, data, expected_errors):
        user = {'id': 1}
        mock_get.return_value = (user, None)

        url = reverse('tournament')

        if data is None:
            response = self.client.post(url)
        else:
            response = self.client.post(url, data=data, content_type='application/json')

        body = json.loads(response.content.decode('utf-8'))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['errors'], expected_errors)

    @patch('api.views.authenticate_request')
    def test_no_body(self, mock_get):
        expected_errors = [error.BAD_JSON_FORMAT]

        self.send_tournament_bad_request(mock_get, None, expected_errors)

    @patch('api.views.authenticate_request')
    def test_empty_body(self, mock_get):
        expected_errors = [error.MISSING_NAME, error.MISSING_IS_PRIVATE]

        self.send_tournament_bad_request(mock_get, {}, expected_errors)

    @patch('api.views.authenticate_request')
    def test_invalid_type(self, mock_get):
        expected_errors = [error.PLAYERS_NOT_INT, error.IS_PRIVATE_NOT_BOOL]

        data = {
            'name': 'Test',
            'is-private': 1,
            'max-players': 'test'
        }

        self.send_tournament_bad_request(mock_get, data, expected_errors)

    @patch('api.views.authenticate_request')
    def test_invalid_iso_8601(self, mock_get):
        expected_errors = [error.NOT_ISO_8601]

        data = {
            'name': 'Test',
            'is-private': False,
            'registration-deadline': '2030-07-1222:30:00'
        }

        self.send_tournament_bad_request(mock_get, data, expected_errors)

    @patch('api.views.authenticate_request')
    def test_passed_deadline(self, mock_get):
        expected_errors = [error.DEADLINE_PASSED]

        data = {
            'name': 'Test',
            'is-private': False,
            'registration-deadline': '2022-07-12T00:00:00Z'
        }

        self.send_tournament_bad_request(mock_get, data, expected_errors)

    @patch('api.views.authenticate_request')
    def test_name_too_long(self, mock_get):
        expected_errors = [error.NAME_TOO_LONG]

        data = {
            'name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'is-private': False,
        }

        self.send_tournament_bad_request(mock_get, data, expected_errors)

    @patch('api.views.authenticate_request')
    def test_name_too_short(self, mock_get):
        expected_errors = [error.NAME_TOO_SHORT]

        data = {
            'name': 'a',
            'is-private': False,
        }

        self.send_tournament_bad_request(mock_get, data, expected_errors)

    @patch('api.views.authenticate_request')
    def test_empty_name(self, mock_get):
        expected_errors = [error.NAME_TOO_SHORT]

        data = {
            'name': '',
            'is-private': False,
        }

        self.send_tournament_bad_request(mock_get, data, expected_errors)

    @patch('api.views.authenticate_request')
    def test_name_invalid_char(self, mock_get):
        expected_errors = [error.NAME_INVALID_CHAR]

        data = {
            'name': 'test!',
            'is-private': False,
        }

        self.send_tournament_bad_request(mock_get, data, expected_errors)
