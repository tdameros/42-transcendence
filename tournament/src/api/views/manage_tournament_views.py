import datetime
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
from common.src import settings as common_settings
from common.src.internal_requests import InternalAuthRequests
from common.src.jwt_managers import user_authentication
from tournament import settings
from tournament.get_user import get_user_id


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
        tournament.start_datetime = datetime.datetime.now(datetime.UTC)

        try:
            tournament.save()
            game_created, game_creation_error, response = StartTournamentView.create_tournament_game(tournament)
            if not game_created:
                tournament.status = Tournament.CREATED
                tournament.save()
                return JsonResponse({'errors': [game_creation_error]}, status=response.status_code)
            StartTournamentView.send_tournament_start_notification(tournament, response.json()['port'])
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

    @staticmethod
    def send_tournament_start_notification(tournament: Tournament, game_port: int) -> None:
        players = tournament.players.all()
        players_id = [player.user_id for player in players]
        notification_data = {
            'title': f'Tournament `{tournament.name}` started',
            'type': 'tournament_start',
            'user_list': players_id,
            'data': f'{game_port}'
        }

        response = InternalAuthRequests.post(
            url=settings.USER_NOTIFICATION_ENDPOINT,
            data=json.dumps(notification_data)
        )

        if response.status_code != 201:
            raise Exception(f'Failed to send tournament start notification: {response.json()}')

    @staticmethod
    def create_tournament_game(tournament: Tournament) -> tuple[bool, Optional[str], any]:
        data = {
            'request_issuer': 'tournament',
            'game_id': tournament.id,
            'players': StartTournamentView.get_players_list(tournament)
        }

        response = InternalAuthRequests.post(
            url=common_settings.GAME_CREATOR_CREATE_GAME_ENDPOINT,
            data=json.dumps(data)
        )

        if response.status_code == 409:
            players_list = StartTournamentView.get_players_already_in_game(
                tournament,
                response.json()['players_already_in_a_game']
            )
            return False, f'Some players are already in a game: {players_list}', response

        if response.status_code != 201:
            return False, f'Failed to create game: {response.json()}', response

        return True, None, response

    @staticmethod
    def get_players_list(tournament: Tournament) -> list[Optional[int]]:
        matches = tournament.matches.all()
        players = []
        nb_round = int(math.log2(len(matches) + 1))

        for i in range(0, 2 ** (nb_round - 1)):
            if matches[i].player_1 is not None:
                players.append(matches[i].player_1.user_id)
            else:
                players.append(None)
            if matches[i].player_2 is not None:
                players.append(matches[i].player_2.user_id)
            else:
                players.append(None)
        return players

    @staticmethod
    def get_players_already_in_game(tournament: Tournament, players_already_in_game: list[int]) -> list[str]:
        players_list = []
        players = tournament.players.all()

        for player in players:
            if player.user_id in players_already_in_game:
                players_list.append(player.nickname)
        return players_list


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['GET', 'DELETE', 'PATCH']), name='dispatch')
class ManageTournamentView(View):
    @staticmethod
    def get(request: HttpRequest, tournament_id: int) -> JsonResponse:
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
            'admin-id': tournament.admin_id
        }

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
        elif tournament.status == Tournament.IN_PROGRESS:
            return JsonResponse({
                'errors': [f'you cannot delete `{tournament_name}` because the tournament has already started']
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
        except Exception:
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
        new_is_private_error = ManageTournamentView.update_is_private(body, tournament)
        new_password_error = ManageTournamentView.update_password(body, tournament)

        if new_name_errors is not None:
            update_errors.extend(new_name_errors)
        if new_max_players_error is not None:
            update_errors.append(new_max_players_error)
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
            return False, f'You cannot set the max players to {new_max_players} because there are already ' \
                          f'{len(tournament_players)} players registered'
        return True, None

    @staticmethod
    def get_tournament_data(tournament: Tournament) -> dict[str, Any]:
        tournament_data = {
            'id': tournament.id,
            'name': tournament.name,
            'max-players': tournament.max_players,
            'is-private': tournament.is_private,
            'status': TournamentView.status_to_string(tournament.status),
        }
        return tournament_data
