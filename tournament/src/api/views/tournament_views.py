import json
from datetime import datetime, timezone
from typing import Any, Optional

from dateutil import parser, tz
from django.contrib.auth.hashers import make_password
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
    def get(request: HttpRequest) -> JsonResponse:
        user, authenticate_errors = authenticate_request(request)
        if user is None:
            return JsonResponse(data={'errors': authenticate_errors}, status=401)

        filter_params = TournamentView.get_filter_params(request)
        try:
            tournaments = Tournament.objects.filter(**filter_params)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        nb_tournaments = len(tournaments)

        page, page_size, nb_pages = TournamentView.get_page_params(request, nb_tournaments)

        page_tournaments = tournaments[page_size * (page - 1): page_size * page]

        tournaments_data = [{
            'id': tournament.id,
            'name': tournament.name,
            'max-players': tournament.max_players,
            'registration-deadline': tournament.registration_deadline,
            'is-private': tournament.is_private,
            'status': TournamentView.status_to_string(tournament.status),
            'admin': user['username']
        } for tournament in page_tournaments]

        response_data = {
            'page': page,
            'page-size': page_size,
            'nb-pages': nb_pages,
            'nb-tournaments': nb_tournaments,
            'tournaments': tournaments_data
        }

        return JsonResponse(response_data, status=200)

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

        is_private = json_request['is-private']
        tournament = Tournament(
            name=json_request['name'],
            is_private=is_private,
            admin_id=user['id']
        )

        if is_private:
            tournament.password = make_password(json_request['password'])

        max_players = json_request.get('max-players')
        if max_players is not None:
            tournament.max_players = max_players
        registration_deadline = json_request.get('registration-deadline')
        if json_request.get('registration-deadline') is not None:
            registration_deadline = parser.isoparse(registration_deadline)
            tournament.registration_deadline = TournamentView.convert_to_utc_datetime(registration_deadline)

        tournament.save()
        return JsonResponse(model_to_dict(tournament, exclude=['password']), status=201)

    @staticmethod
    def delete(request: HttpRequest) -> JsonResponse:
        # TODO: authorize this endpoint only for auth microservice
        user, authenticate_errors = authenticate_request(request)
        if user is None:
            return JsonResponse(data={'errors': authenticate_errors}, status=401)

        try:
            user_tournaments = Tournament.objects.filter(admin_id=user['id'], status=Tournament.CREATED)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        if user_tournaments:
            try:
                user_tournaments.delete()
            except Exception as e:
                return JsonResponse({'errors': [str(e)]}, status=500)

        return JsonResponse({'message': 'tournaments created by this user have been deleted'}, status=200)

    @staticmethod
    def is_valid_tournament(json_request: dict[str, Any]) -> tuple[bool, Optional[list[str]]]:
        errors = []
        name = json_request.get('name')
        max_players = json_request.get('max-players')
        registration_deadline = json_request.get('registration-deadline')
        is_private = json_request.get('is-private')
        password = json_request.get('password')

        valid_name, name_errors = TournamentView.is_valid_name(name)
        valid_max_players, max_players_error = TournamentView.is_valid_max_players(max_players)
        valid_deadline, deadline_error = TournamentView.is_valid_deadline(registration_deadline)
        valid_private, is_private_error = TournamentView.is_valid_private(is_private)
        valid_password, password_error = TournamentView.is_valid_password(password)

        if not valid_name:
            errors.extend(name_errors)
        if not valid_max_players:
            errors.append(max_players_error)
        if not valid_deadline:
            errors.append(deadline_error)
        if not valid_private:
            errors.append(is_private_error)
        if valid_private and is_private and not valid_password:
            errors.append(password_error)

        if errors:
            return False, errors
        return True, None

    @staticmethod
    def is_valid_name(name: Any) -> tuple[bool, Optional[list[str]]]:
        errors = []

        if name is None:
            return False, [error.NAME_MISSING]
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
            return False, error.IS_PRIVATE_MISSING
        elif not isinstance(is_private, bool):
            return False, error.IS_PRIVATE_NOT_BOOL
        return True, None

    @staticmethod
    def is_valid_password(password: Any) -> tuple[bool, Optional[str]]:
        if password is None:
            return False, error.PASSWORD_MISSING
        if not isinstance(password, str):
            return False, error.PASSWORD_NOT_STRING
        if len(password) < settings.PASSWORD_MIN_LENGTH:
            return False, error.PASSWORD_TOO_SHORT
        if len(password) > settings.PASSWORD_MAX_LENGTH:
            return False, error.PASSWORD_TOO_LONG
        return True, None

    @staticmethod
    def convert_to_utc_datetime(parsed_datetime: datetime) -> datetime:
        return parsed_datetime.astimezone(tz.tzutc())

    @staticmethod
    def get_page_params(request: HttpRequest, nb_tournaments: int) -> tuple[int, int, int]:
        page = request.GET.get('page', 1)
        page_size = request.GET.get('page-size', settings.DEFAULT_PAGE_SIZE)

        try:
            page_size = int(page_size)
            if page_size > settings.MAX_PAGE_SIZE:
                page_size = settings.MAX_PAGE_SIZE
            elif page_size <= 0:
                raise ValueError
        except ValueError:
            page_size = settings.DEFAULT_PAGE_SIZE

        last_page = nb_tournaments // page_size
        if nb_tournaments % page_size != 0:
            last_page += 1
        if nb_tournaments == 0:
            last_page = 1

        try:
            page = int(page)
            if page > last_page:
                page = last_page
            elif page <= 0:
                raise ValueError
        except ValueError:
            page = 1

        return page, page_size, last_page

    @staticmethod
    def get_filter_params(request: HttpRequest) -> dict:
        filter_params = {}

        if 'display-private' not in request.GET:
            filter_params['is_private'] = False
        if 'display-completed' not in request.GET:
            filter_params['status__in'] = [Tournament.CREATED, Tournament.IN_PROGRESS]

        return filter_params

    @staticmethod
    def status_to_string(status: int) -> str:
        status_string = ['Created', 'In progress', 'Finished']

        return status_string[status]
