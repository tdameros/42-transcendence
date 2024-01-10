import json
from datetime import datetime, timezone
from typing import Any, Optional

from dateutil import parser, tz
from django.forms.models import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api import error_message as error
from api.models import Tournament
from tournament import settings
from tournament.authenticate_request import authenticate_request


@method_decorator(csrf_exempt, name='dispatch')
class TournamentView(View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        user, authenticate_errors = authenticate_request(request)
        if user is None:
            return JsonResponse(data={'errors': authenticate_errors}, status=401)

        try:
            json_request = json.loads(request.body.decode('utf8'))
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': [error.BAD_JSON_FORMAT]}, status=400)

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

    @staticmethod
    def is_valid_tournament(json_request: dict[str, Any]) -> tuple[bool, Optional[list[str]]]:
        errors = []
        name = json_request.get('name')
        max_players = json_request.get('max-players')
        registration_deadline = json_request.get('registration-deadline')
        is_private = json_request.get('is-private')

        valid_name, name_errors = TournamentView.is_valid_name(name)
        valid_max_players, max_players_error = TournamentView.is_valid_max_players(max_players)
        valid_deadline, deadline_error = TournamentView.is_valid_deadline(registration_deadline)
        valid_private, is_private_error = TournamentView.is_valid_private(is_private)

        if not valid_name:
            errors.extend(name_errors)
        if not valid_max_players:
            errors.append(max_players_error)
        if not valid_deadline:
            errors.append(deadline_error)
        if not valid_private:
            errors.append(is_private_error)

        if errors:
            return False, errors
        return True, None

    @staticmethod
    def is_valid_name(name: Any) -> tuple[bool, Optional[list[str]]]:
        errors = []

        if name is None:
            return False, [error.MISSING_NAME]
        if len(name) < settings.MIN_TOURNAMENT_NAME_LENGTH:
            errors.append(error.NAME_TOO_SHORT)
        elif len(name) > settings.MAX_TOURNAMENT_NAME_LENGTH:
            errors.append(error.NAME_TOO_LONG)
        if len(name) and not name.replace(' ', '').isalnum():
            errors.append(error.NAME_INVALID_CHAR)

        if errors:
            return False, errors
        return True, None

    @staticmethod
    def is_valid_max_players(max_players: Any) -> tuple[bool, Optional[str]]:
        if max_players is None:
            return True, None
        if not isinstance(max_players, int):
            return False, error.PLAYERS_NOT_INT
        if max_players > settings.MAX_PLAYERS:
            return False, error.TOO_MANY_SLOTS
        if max_players < settings.MIN_PLAYERS:
            return False, error.NOT_ENOUGH_SLOTS
        return True, None

    @staticmethod
    def is_valid_deadline(registration_deadline: str) -> tuple[bool, Optional[str]]:
        if registration_deadline is None:
            return True, None

        try:
            deadline_time = parser.isoparse(registration_deadline)
        except ValueError:
            return False, error.NOT_ISO_8601

        deadline_time = TournamentView.convert_to_utc_datetime(deadline_time)
        if deadline_time < datetime.now(timezone.utc):
            return False, error.DEADLINE_PASSED
        return True, None

    @staticmethod
    def is_valid_private(is_private: Any) -> tuple[bool, Optional[str]]:
        if is_private is None:
            return False, error.MISSING_IS_PRIVATE
        elif not isinstance(is_private, bool):
            return False, error.IS_PRIVATE_NOT_BOOL
        return True, None

    @staticmethod
    def convert_to_utc_datetime(parsed_datetime: datetime) -> datetime:
        return parsed_datetime.astimezone(tz.tzutc())
