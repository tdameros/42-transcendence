import json
import math
from typing import Any, Optional

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api import error_message as error
from api.models import Tournament
from api.views.tournament_views import TournamentView
from common.src.jwt_managers import user_authentication
from tournament import settings
from tournament.authenticate_request import get_user_id, get_username_by_id


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['PATCH']), name='dispatch')
class StartTournamentView(View):
    @staticmethod
    def patch(request: HttpRequest, tournament_id: int) -> JsonResponse:
        user_id = get_user_id(request)

        try:
            tournament = Tournament.objects.get(id=tournament_id)
            players = tournament.players.all()
            matches = tournament.matches.all()
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [f'tournament with id `{tournament_id}` does not exist']}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        start_error = StartTournamentView.check_start_permissions(user_id, tournament, players, matches)
        if start_error is not None:
            return JsonResponse(data={'errors': [start_error]}, status=403)

        tournament.status = Tournament.IN_PROGRESS

        try:
            tournament.save()
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        return JsonResponse({'message': f'Tournament `{tournament.name}` successfully started'}, status=200)

    @staticmethod
    def check_start_permissions(user_id: int, tournament: Tournament, players, matches) -> Optional[str]:
        if tournament.status != Tournament.CREATED:
            return 'The tournament has already started'

        if tournament.admin_id != user_id:
            return 'You are not the owner of the tournament, so you cannot start it'

        if len(players) < settings.MIN_PLAYERS:
            return error.NOT_ENOUGH_PLAYERS

        if len(matches) != int(2 ** math.ceil(math.log2(len(players))) - 1):
            return error.MATCHES_NOT_GENERATED

        return None


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['GET', 'DELETE', 'PATCH']), name='dispatch')
class ManageTournamentView(View):
    @staticmethod
    def get(request: HttpRequest, tournament_id: int) -> JsonResponse:
        jwt = request.headers.get('Authorization')

        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [f'tournament with id `{tournament_id}` does not exist']}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        try:
            tournament_players = tournament.players.all()
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        try:
            tournament_data = {
                'id': tournament.id,
                'name': tournament.name,
                'max-players': tournament.max_players,
                'nb-players': len(tournament_players),
                'players': [{
                    'nickname': player.nickname,
                    'user-id': player.user_id,
                    'rank': player.rank
                } for player in tournament_players],
                'is-private': tournament.is_private,
                'status': TournamentView.status_to_string(tournament.status),
                'admin': get_username_by_id(tournament.admin_id, jwt)
            }
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        if tournament.registration_deadline is not None:
            tournament_data['registration-deadline'] = tournament.registration_deadline

        return JsonResponse(tournament_data, status=200)

    @staticmethod
    def delete(request: HttpRequest, tournament_id: int) -> JsonResponse:
        user_id = get_user_id(request)

        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [f'tournament with id `{tournament_id}` does not exist']}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        tournament_name = tournament.name
        tournament_admin = tournament.admin_id

        if tournament_admin != user_id:
            return JsonResponse({
                'errors': [f'you cannot delete `{tournament_name}` because you are not the owner of the tournament']
            }, status=403)

        try:
            tournament.delete()
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        return JsonResponse({'message': f'tournament `{tournament_name}` successfully deleted'}, status=200)

    @staticmethod
    def patch(request: HttpRequest, tournament_id: int) -> JsonResponse:
        user_id = get_user_id(request)

        try:
            body = json.loads(request.body.decode('utf8'))
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': [error.BAD_JSON_FORMAT]}, status=400)

        try:
            tournament = Tournament.objects.get(id=tournament_id)
            tournament_players = tournament.players.all()
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [f'tournament with id `{tournament_id}` does not exist']}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        manage_errors = ManageTournamentView.check_manage_permissions(user_id, tournament)
        if manage_errors is not None:
            return JsonResponse(data={'errors': manage_errors}, status=403)

        update_errors = ManageTournamentView.update_tournament_settings(body, tournament, tournament_players)
        if update_errors:
            return JsonResponse(data={'errors': update_errors}, status=400)

        try:
            tournament.save()
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        tournament_data = ManageTournamentView.get_tournament_data(tournament)
        return JsonResponse(tournament_data, status=200)

    @staticmethod
    def check_manage_permissions(user_id: int, tournament: Tournament) -> Optional[list[str]]:
        if tournament.status != Tournament.CREATED:
            return ['The tournament has already started, so you cannot update the settings']

        if tournament.admin_id != user_id:
            return ['You are not the owner of the tournament, so you cannot update the settings']

        return None

    @staticmethod
    def update_tournament_settings(body: dict, tournament: Tournament, tournament_players) -> Optional[list[str]]:
        update_errors = []

        new_name_errors = ManageTournamentView.update_tournament_name(body, tournament)
        new_max_players_error = ManageTournamentView.update_max_players(body, tournament, tournament_players)
        new_deadline_error = ManageTournamentView.update_registration_deadline(body, tournament)
        new_is_private_error = ManageTournamentView.update_is_private(body, tournament)
        new_password_error = ManageTournamentView.update_password(body, tournament)

        if new_name_errors is not None:
            update_errors.extend(new_name_errors)
        if new_max_players_error is not None:
            update_errors.append(new_max_players_error)
        if new_deadline_error is not None:
            update_errors.append(new_deadline_error)
        if new_is_private_error is not None:
            update_errors.append(new_is_private_error)
        if new_password_error is not None:
            update_errors.append(new_password_error)

        return update_errors

    @staticmethod
    def update_tournament_name(body: dict, tournament: Tournament) -> Optional[list[str]]:
        new_name = body.get('name')
        if new_name is not None:
            valid_new_name, new_name_errors = TournamentView.is_valid_name(new_name)
            if not valid_new_name:
                return new_name_errors
            else:
                tournament.name = new_name
        return None

    @staticmethod
    def update_max_players(body: dict, tournament: Tournament, tournament_players) -> Optional[str]:
        new_max_players = body.get('max-players')
        if new_max_players is not None:
            valid_new_max_players, new_max_players_error = ManageTournamentView.is_valid_max_players(
                new_max_players, tournament_players)
            if not valid_new_max_players:
                return new_max_players_error
            else:
                tournament.max_players = new_max_players
        return None

    @staticmethod
    def update_registration_deadline(body: dict, tournament: Tournament) -> Optional[str]:
        new_deadline = body.get('registration-deadline')
        if new_deadline is not None:
            valid_registration_deadline, registration_deadline_error = TournamentView.is_valid_deadline(new_deadline)
            if not valid_registration_deadline:
                return registration_deadline_error
            else:
                tournament.registration_deadline = new_deadline
        return None

    @staticmethod
    def update_is_private(body: dict, tournament: Tournament) -> Optional[str]:
        new_is_private = body.get('is-private')
        if new_is_private is not None:
            valid_is_private, is_private_error = TournamentView.is_valid_private(new_is_private)
            if not valid_is_private:
                return is_private_error
            else:
                tournament.is_private = new_is_private
        return None

    @staticmethod
    def update_password(body: dict, tournament: Tournament) -> Optional[str]:
        new_password = body.get('password')
        valid_password, password_error = TournamentView.is_valid_password(new_password)
        if tournament.is_private and (tournament.password is None or new_password is not None):
            if not valid_password:
                return password_error
            else:
                tournament.password = make_password(new_password)
        return None

    @staticmethod
    def is_valid_max_players(new_max_players: Any, tournament_players: Any) -> tuple[bool, Optional[str]]:
        valid_max_players, max_players_error = TournamentView.is_valid_max_players(new_max_players)
        if not valid_max_players:
            return False, max_players_error
        elif len(tournament_players) > new_max_players:
            return False, f'You cannot set the max players to {new_max_players} because there are already '\
                          f'{len(tournament_players)} players registered'
        return True, None

    @staticmethod
    def get_tournament_data(tournament: Tournament) -> dict[str, Any]:
        tournament_data = {
            'id': tournament.id,
            'name': tournament.name,
            'max-players': tournament.max_players,
            'is-private': tournament.is_private,
            'registration-deadline': tournament.registration_deadline,
            'status': TournamentView.status_to_string(tournament.status),
        }
        return tournament_data
