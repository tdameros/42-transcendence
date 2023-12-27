from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict

from dateutil import parser, tz
from datetime import datetime, timezone
import json

from api.models import Tournament
from tournament.authenticate_request import authenticate_request
from tournament import settings


@method_decorator(csrf_exempt, name='dispatch')
class TournamentView(View):
    @staticmethod
    def post(request):
        try:
            user, authenticate_errors = authenticate_request(request)
            if user is None:
                return JsonResponse(data={'errors': authenticate_errors}, status=401)
            json_request = json.loads(request.body.decode('utf8'))
            valid_tournament, errors = TournamentView.is_valid_tournament(json_request)
            if not valid_tournament:
                return JsonResponse(data={'errors': errors}, status=400)

            tournament = Tournament(
                name=json_request['name'],
                is_private=json_request['is-private'],
                admin_id=user['id']
            )
            max_players = json_request.get('max-players')
            if max_players is not None:
                tournament.max_players = max_players
            registration_deadline = json_request.get('registration-deadline')
            if json_request.get('registration-deadline') is not None:
                registration_deadline = parser.isoparse(registration_deadline)
                tournament.registration_deadline = TournamentView.convert_to_utc_datetime(registration_deadline)
            tournament.save()
            return JsonResponse(model_to_dict(tournament), status=201)
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': ['Invalid JSON format in request body']}, status=400)

    @staticmethod
    def is_valid_tournament(json_request):
        errors = []
        name = json_request.get('name')
        max_players = json_request.get('max-players')
        registration_deadline = json_request.get('registration-deadline')
        is_private = json_request.get('is-private')

        valid_name, name_errors = TournamentView.is_valid_name(name)
        valid_max_players, max_players_error = TournamentView.is_valid_max_players(max_players)
        valid_deadline, deadline_error = TournamentView.is_valid_deadline(registration_deadline)

        if not valid_name:
            errors.append(name_errors)
        if not valid_max_players:
            errors.append(max_players_error)
        if not valid_deadline:
            errors.append(deadline_error)
        if is_private is None:
            errors.append('Missing is-private field')
        elif not isinstance(is_private, bool):
            errors.append('Is private must be a boolean')

        if errors:
            return False, errors
        return True, None

    @staticmethod
    def is_valid_name(name):
        errors = []

        if name is None:
            errors.append('Missing name field')
        if len(name) < settings.MIN_TOURNAMENT_NAME_LENGTH:
            errors.append(f'Tournament name must contain at least {settings.MIN_TOURNAMENT_NAME_LENGTH} characters')
        elif len(name) > settings.MAX_TOURNAMENT_NAME_LENGTH:
            errors.append(f'Tournament name must contain less than {settings.MAX_TOURNAMENT_NAME_LENGTH} characters')
        if not name.replace(' ', '').isalnum():
            errors.append('Tournament name may only contain letters, numbers and spaces')

        if errors:
            return False, errors
        return True, None

    @staticmethod
    def is_valid_max_players(max_players):
        if max_players is None:
            return True, None
        if not isinstance(max_players, int):
            return False, 'Max players must be an integer'
        if max_players > settings.MAX_PLAYERS:
            return False, f'Max players must contain less than {settings.MAX_PLAYERS} slots'
        if max_players < settings.MIN_PLAYERS:
            return False, f'Max players must contain at least {settings.MIN_PLAYERS} slots'
        return True, None

    @staticmethod
    def is_valid_deadline(registration_deadline):
        if registration_deadline is None:
            return True, None
        try:
            deadline_time = parser.isoparse(registration_deadline)
            deadline_time = TournamentView.convert_to_utc_datetime(deadline_time)
            current_time = datetime.now(timezone.utc)
            if deadline_time < current_time:
                return False, 'Registration deadline has passed'
            return True, None
        except ValueError:
            return False, 'Registration deadline not in ISO 8601 date and time format'

    @staticmethod
    def convert_to_utc_datetime(parsed_datetime):
        return parsed_datetime.astimezone(tz.tzutc())

