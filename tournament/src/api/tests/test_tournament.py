import json
from unittest.mock import patch

from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from api import error_message as error
from api.models import Tournament
from tournament import settings


class GetTournamentTest(TestCase):
    def setUp(self):
        for i in range(1, 51):
            Tournament.objects.create(name=f'Test{i}', admin_id=1)
        for i in range(1, 26):
            Tournament.objects.create(name=f'PrivateTest{i}', admin_id=1, is_private=True)
        for i in range(1, 26):
            Tournament.objects.create(name=f'FinishTest{i}', admin_id=1, status=2)
        for i in range(1, 6):
            Tournament.objects.create(name=f'PrivateFinishTest{i}', admin_id=1, is_private=True, status=2)

    def get_tournaments(self, params: dict) -> tuple[HttpResponse, dict]:
        url = reverse('tournament')

        response = self.client.get(url, params)

        body = json.loads(response.content.decode('utf-8'))

        return response, body

    def test_default(self):
        response, body = self.get_tournaments({})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body['tournaments']), settings.DEFAULT_PAGE_SIZE)
        self.assertEqual(body['page'], 1)
        self.assertEqual(body['page-size'], settings.DEFAULT_PAGE_SIZE)
        self.assertEqual(body['nb-pages'], 5)
        self.assertEqual(body['nb-tournaments'], 50)

    def test_page_2(self):
        response, body = self.get_tournaments({'page': 2})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body['tournaments']), settings.DEFAULT_PAGE_SIZE)
        self.assertEqual(body['page'], 2)
        self.assertEqual(body['page-size'], settings.DEFAULT_PAGE_SIZE)
        self.assertEqual(body['nb-pages'], 5)
        self.assertEqual(body['nb-tournaments'], 50)

    def test_page_size(self):
        response, body = self.get_tournaments({'page-size': 20})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body['tournaments']), 20)
        self.assertEqual(body['page'], 1)
        self.assertEqual(body['page-size'], 20)
        self.assertEqual(body['nb-pages'], 3)
        self.assertEqual(body['nb-tournaments'], 50)

    def test_page_size_too_high(self):
        response, body = self.get_tournaments({'page-size': 100})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body['tournaments']), 50)
        self.assertEqual(body['page'], 1)
        self.assertEqual(body['page-size'], 50)
        self.assertEqual(body['nb-pages'], 1)
        self.assertEqual(body['nb-tournaments'], 50)

    def test_page_too_high(self):
        response, body = self.get_tournaments({'page': 6})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body['tournaments']), 10)
        self.assertEqual(body['page'], 5)
        self.assertEqual(body['page-size'], settings.DEFAULT_PAGE_SIZE)
        self.assertEqual(body['nb-pages'], 5)
        self.assertEqual(body['nb-tournaments'], 50)

    def test_page_size_and_page(self):
        response, body = self.get_tournaments({'page-size': 20, 'page': 3})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body['tournaments']), 10)
        self.assertEqual(body['page'], 3)
        self.assertEqual(body['page-size'], 20)
        self.assertEqual(body['nb-pages'], 3)
        self.assertEqual(body['nb-tournaments'], 50)

    def test_negative_params(self):
        response, body = self.get_tournaments({'page-size': -20, 'page': -3})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body['tournaments']), settings.DEFAULT_PAGE_SIZE)
        self.assertEqual(body['page'], 1)
        self.assertEqual(body['page-size'], settings.DEFAULT_PAGE_SIZE)
        self.assertEqual(body['nb-pages'], 5)
        self.assertEqual(body['nb-tournaments'], 50)

    def test_page_size_1(self):
        response, body = self.get_tournaments({'page-size': 1})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body['tournaments']), 1)
        self.assertEqual(body['page'], 1)
        self.assertEqual(body['page-size'], 1)
        self.assertEqual(body['nb-pages'], 50)
        self.assertEqual(body['nb-tournaments'], 50)

    def test_display_private(self):
        response, body = self.get_tournaments({'page': 8, 'display-private': True})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body['tournaments']), 5)
        self.assertEqual(body['page'], 8)
        self.assertEqual(body['page-size'], settings.DEFAULT_PAGE_SIZE)
        self.assertEqual(body['nb-pages'], 8)
        self.assertEqual(body['nb-tournaments'], 75)

    def test_display_completed(self):
        response, body = self.get_tournaments({'page': 6, 'display-completed': True})

        tournaments = Tournament.objects.filter(status=2)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body['tournaments']), settings.DEFAULT_PAGE_SIZE)
        self.assertEqual(body['page'], 6)
        self.assertEqual(body['page-size'], settings.DEFAULT_PAGE_SIZE)
        self.assertEqual(body['nb-pages'], 8)
        self.assertEqual(body['nb-tournaments'], 75)

    def test_display_private_and_completed(self):
        response, body = self.get_tournaments({'page': 11, 'display-private': True, 'display-completed': True})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(body['tournaments']), 5)
        self.assertEqual(body['page'], 11)
        self.assertEqual(body['page-size'], settings.DEFAULT_PAGE_SIZE)
        self.assertEqual(body['nb-pages'], 11)
        self.assertEqual(body['nb-tournaments'], 105)

class CreateTournamentTest(TestCase):
    def create_tournament(self, data: dict) -> tuple[HttpResponse, dict]:
        url = reverse('tournament')

        response = self.client.post(url, json.dumps(data), content_type='application/json')

        body = json.loads(response.content.decode('utf-8'))

        return response, body

    @patch('api.views.tournament_views.authenticate_request')
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

    @patch('api.views.tournament_views.authenticate_request')
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

    @patch('api.views.tournament_views.authenticate_request')
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

    @patch('api.views.tournament_views.authenticate_request')
    def test_no_body(self, mock_get):
        expected_errors = [error.BAD_JSON_FORMAT]

        self.send_tournament_bad_request(mock_get, None, expected_errors)

    @patch('api.views.tournament_views.authenticate_request')
    def test_empty_body(self, mock_get):
        expected_errors = [error.MISSING_NAME, error.MISSING_IS_PRIVATE]

        self.send_tournament_bad_request(mock_get, {}, expected_errors)

    @patch('api.views.tournament_views.authenticate_request')
    def test_invalid_type(self, mock_get):
        expected_errors = [error.PLAYERS_NOT_INT, error.IS_PRIVATE_NOT_BOOL]

        data = {
            'name': 'Test',
            'is-private': 1,
            'max-players': 'test'
        }

        self.send_tournament_bad_request(mock_get, data, expected_errors)

    @patch('api.views.tournament_views.authenticate_request')
    def test_invalid_iso_8601(self, mock_get):
        expected_errors = [error.NOT_ISO_8601]

        data = {
            'name': 'Test',
            'is-private': False,
            'registration-deadline': '2030-07-1222:30:00'
        }

        self.send_tournament_bad_request(mock_get, data, expected_errors)

    @patch('api.views.tournament_views.authenticate_request')
    def test_passed_deadline(self, mock_get):
        expected_errors = [error.DEADLINE_PASSED]

        data = {
            'name': 'Test',
            'is-private': False,
            'registration-deadline': '2022-07-12T00:00:00Z'
        }

        self.send_tournament_bad_request(mock_get, data, expected_errors)

    @patch('api.views.tournament_views.authenticate_request')
    def test_name_too_long(self, mock_get):
        expected_errors = [error.NAME_TOO_LONG]

        data = {
            'name': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
            'is-private': False,
        }

        self.send_tournament_bad_request(mock_get, data, expected_errors)

    @patch('api.views.tournament_views.authenticate_request')
    def test_name_too_short(self, mock_get):
        expected_errors = [error.NAME_TOO_SHORT]

        data = {
            'name': 'a',
            'is-private': False,
        }

        self.send_tournament_bad_request(mock_get, data, expected_errors)

    @patch('api.views.tournament_views.authenticate_request')
    def test_empty_name(self, mock_get):
        expected_errors = [error.NAME_TOO_SHORT]

        data = {
            'name': '',
            'is-private': False,
        }

        self.send_tournament_bad_request(mock_get, data, expected_errors)

    @patch('api.views.tournament_views.authenticate_request')
    def test_name_invalid_char(self, mock_get):
        expected_errors = [error.NAME_INVALID_CHAR]

        data = {
            'name': 'test!',
            'is-private': False,
        }

        self.send_tournament_bad_request(mock_get, data, expected_errors)
