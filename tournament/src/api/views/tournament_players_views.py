import json
from datetime import datetime, timezone
from typing import Optional

from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api import error_message as error
from api.models import Player, Tournament
from tournament import settings
from tournament.authenticate_request import authenticate_request


@method_decorator(csrf_exempt, name='dispatch')
class TournamentPlayersView(View):
    @staticmethod
    def get(request: HttpRequest, tournament_id: int) -> JsonResponse:
        user, authenticate_errors = authenticate_request(request)
        if user is None:
            return JsonResponse(data={'errors': authenticate_errors}, status=401)

        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [f'tournament with id `{tournament_id}` does not exist']}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        players = tournament.players.all()

        players_data = [{
            'nickname': player.nickname,
            'user_id': player.user_id
        } for player in players]

        response_data = {
            'max-players': tournament.max_players,
            'nb-players': len(players),
            'players': players_data
        }

        return JsonResponse(response_data, status=200)

    @staticmethod
    def post(request: HttpRequest, tournament_id: int) -> JsonResponse:
        user, authenticate_errors = authenticate_request(request)
        if user is None:
            return JsonResponse(data={'errors': authenticate_errors}, status=401)

        try:
            json_request = json.loads(request.body.decode('utf8'))
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': [error.BAD_JSON_FORMAT]}, status=400)

        user_nickname = json_request.get('nickname')
        valid_nickname, nickname_errors = TournamentPlayersView.is_valid_nickname(user_nickname)
        if not valid_nickname:
            return JsonResponse(data={'errors': nickname_errors}, status=400)

        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [f'tournament with id `{tournament_id}` does not exist']}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [f'An unexpected error occurred : {e}']}, status=500)

        player = Player(nickname=user_nickname, user_id=user['id'], tournament=tournament)

        password = json_request.get('password')
        can_join, error_data = TournamentPlayersView.player_can_join_tournament(player, password, tournament)

        if not can_join:
            return JsonResponse({'errors': [error_data[0]]}, status=error_data[1])

        try:
            player.save()
        except Exception as e:
            return JsonResponse({'errors': [f'An unexpected error occurred : {e}']}, status=500)

        return JsonResponse(model_to_dict(player), status=201)

    @staticmethod
    def is_valid_nickname(nickname: str) -> tuple[bool, Optional[list[str]]]:
        errors = []

        if nickname is None:
            return False, [error.NICKNAME_MISSING]
        if len(nickname) < settings.MIN_NICKNAME_LENGTH:
            errors.append(error.NICKNAME_TOO_SHORT)
        elif len(nickname) > settings.MAX_NICKNAME_LENGTH:
            errors.append(error.NICKNAME_TOO_LONG)
        if len(nickname) and not nickname.replace(' ', '').isalnum():
            errors.append(error.NICKNAME_INVALID_CHAR)

        if errors:
            return False, errors
        return True, None

    @staticmethod
    def player_can_join_tournament(new_player: Player, password: Optional[str], tournament: Tournament)\
            -> tuple[bool, Optional[list[str | int]]]:
        try:
            tournament_players = tournament.players.all()
        except Exception as e:
            return False, [f'An unexpected error occurred : {e}', 500]

        if tournament.status != Tournament.CREATED or (
                tournament.registration_deadline is not None
                and tournament.registration_deadline < datetime.now(timezone.utc)):
            return False, ['The registration phase is over', 403]

        if tournament.is_private and password is None:
            return False, [error.PASSWORD_MISSING, 400]
        if tournament.is_private and not check_password(password, tournament.password):
            return False, [error.PASSWORD_NOT_MATCH, 403]

        for player in tournament_players:
            if player.user_id == new_player.user_id:
                return False, [f'You are already registered as `{player.nickname}` for the tournament', 403]
            elif player.nickname == new_player.nickname:
                return False, [f'nickname `{player.nickname}` already taken', 400]

        try:
            user_already_in_tournament = Tournament.objects.filter(
                players__user_id=new_player.user_id,
                status__in=[Tournament.CREATED, Tournament.IN_PROGRESS]
            ).exists()
        except Exception as e:
            return False, [f'An unexpected error occurred : {e}', 500]

        if user_already_in_tournament:
            return False, ['You are already registered for another tournament', 403]

        if tournament.max_players <= len(tournament_players):
            return False, ['This tournament is fully booked', 403]

        return True, None
