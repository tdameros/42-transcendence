import json
from typing import Any, Optional

from django.contrib.auth.hashers import make_password
from django.forms.models import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api import error_message as error
from api.models import Player, Tournament
from api.views.tournament_players_views import TournamentPlayersView
from api.views.tournament_utils import TournamentUtils
from common.src.jwt_managers import user_authentication
from tournament import settings
from tournament.get_user import get_user_id


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['GET', 'POST', 'DELETE']), name='dispatch')
class TournamentView(View):
    @staticmethod
    def get(request: HttpRequest) -> JsonResponse:
        filter_params = TournamentView.get_filter_params(request)
        try:
            tournaments = Tournament.objects.filter(**filter_params)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)
        nb_tournaments = len(tournaments)

        page, page_size, nb_pages = TournamentView.get_page_params(request, nb_tournaments)

        page_tournaments = tournaments[page_size * (page - 1): page_size * page]

        tournaments_data = TournamentUtils.tournament_to_json(page_tournaments)

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
        user_id = get_user_id(request)

        try:
            json_request = json.loads(request.body.decode('utf8'))
        except Exception:
            return JsonResponse(data={'errors': [error.BAD_JSON_FORMAT]}, status=400)

        valid_tournament, errors = TournamentView.is_valid_tournament(json_request)
        if not valid_tournament:
            return JsonResponse(data={'errors': errors}, status=400)

        is_private = json_request['is-private']
        tournament = Tournament(
            name=json_request['name'],
            is_private=is_private,
            admin_id=user_id
        )

        if is_private:
            tournament.password = make_password(json_request['password'])

        max_players = json_request.get('max-players')
        if max_players is not None:
            tournament.max_players = max_players
        try:
            tournament.save()
            register_admin_errors = TournamentView.register_admin_as_player(json_request, tournament, user_id)
            if register_admin_errors is not None:
                tournament.delete()
                return JsonResponse({'errors': register_admin_errors}, status=400)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)
        return JsonResponse(model_to_dict(tournament, exclude=['password']), status=201)

    @staticmethod
    def delete(request: HttpRequest) -> JsonResponse:
        user_id = get_user_id(request)

        try:
            user_tournaments = Tournament.objects.filter(admin_id=user_id, status=Tournament.CREATED)
            nb_tournaments = len(user_tournaments)
            if user_tournaments:
                user_tournaments.delete()

            player = Player.objects.filter(user_id=user_id, tournament__status=Tournament.CREATED)
            if player:
                player.delete()
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        if nb_tournaments == 0:
            return JsonResponse({'message': 'No tournament created by this user'}, status=200)
        return JsonResponse({'message': 'Tournaments created by this user have been deleted'}, status=200)

    @staticmethod
    def is_valid_tournament(json_request: dict[str, Any]) -> tuple[bool, Optional[list[str]]]:
        errors = []
        name = json_request.get('name')
        max_players = json_request.get('max-players')
        is_private = json_request.get('is-private')
        password = json_request.get('password')

        valid_name, name_errors = TournamentView.is_valid_name(name)
        valid_max_players, max_players_error = TournamentView.is_valid_max_players(max_players)
        valid_private, is_private_error = TournamentView.is_valid_private(is_private)
        valid_password, password_error = TournamentView.is_valid_password(password)

        if not valid_name:
            errors.extend(name_errors)
        if not valid_max_players:
            errors.append(max_players_error)
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
    def register_admin_as_player(json_request, tournament: Tournament, user_id: int) -> Optional[list[str]]:
        admin_nickname = json_request.get('nickname')
        if admin_nickname is not None:
            valid_nickname, nickname_errors = TournamentPlayersView.is_valid_nickname(admin_nickname)
            if not valid_nickname:
                return nickname_errors
            Player.objects.create(
                nickname=admin_nickname,
                user_id=user_id,
                tournament=tournament
            )
        return None

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
