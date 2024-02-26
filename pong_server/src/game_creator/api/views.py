import base64
import json
from typing import Optional

from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api import error_messages, settings
from api.GameCreator import GameCreator
from api.JsonResponseException import JsonResponseException
from common.src import settings as common_settings
from common.src.internal_requests import InternalAuthRequests, InternalRequests
from common.src.jwt_managers import user_authentication
from shared_code import settings as shared_settings


@method_decorator(csrf_exempt, name='dispatch')
class CreateGameView(View):
    def post(self, request):
        try:
            game_id, players, request_issuer = CreateGameView._get_args(request)

            if request_issuer == settings.TOURNAMENT:
                api_name = shared_settings.TOURNAMENT
            else:
                api_name = shared_settings.USER_STATS
            port: int = GameCreator.create_game_server(game_id, players, api_name)

            return JsonResponse({'port': port},
                                status=201)

        except JsonResponseException as json_response_exception:
            return json_response_exception.to_json_response()

    @staticmethod
    def _get_args(request) -> (int, list[Optional[int]], str):
        try:
            json_body = json.loads(request.body.decode('utf-8'))
            if not isinstance(json_body, dict):
                raise Exception()
        except Exception:
            raise JsonResponseException({'errors': [error_messages.BAD_JSON_FORMAT]},
                                        status=400)

        errors = []

        request_issuer: str = CreateGameView._get_request_issuer(json_body, errors)
        game_id: int = CreateGameView._get_game_id(json_body, errors)
        players: list[Optional[int]] = CreateGameView._get_players(
            json_body, errors, request_issuer
        )

        if len(errors) > 0:
            raise JsonResponseException({'errors': errors}, status=400)

        return game_id, players, request_issuer

    @staticmethod
    def _get_game_id(json_body, errors) -> int:
        game_id = json_body.get('game_id')
        if game_id is None:
            errors.append(error_messages.GAME_ID_FIELD_MISSING)
            return -1

        if isinstance(game_id, int):
            return game_id

        try:
            return int(game_id)
        except ValueError:
            errors.append(error_messages.GAME_ID_FIELD_IS_NOT_AN_INTEGER)
            return -1

    @staticmethod
    def _get_players(json_body, errors, request_issuer: str) -> list[Optional[int]]:
        players: any = json_body.get('players')
        if players is None:
            errors.append(error_messages.PLAYERS_FIELD_MISSING)
            return []

        if not isinstance(players, list):
            errors.append(error_messages.PLAYERS_FIELD_IS_NOT_A_LIST)
            return []

        if len(players) != 2 and request_issuer == settings.MATCHMAKING:
            errors.append(error_messages.NEED_2_PLAYERS_FOR_MATCHMAKING)

        if (len(players) & (len(players) - 1) != 0) and len(players) != 0:
            errors.append(error_messages.LEN_PLAYERS_IS_NOT_A_POWER_OF_2)

        validated_players: set[int] = set()
        for i in range(0, len(players) - 1, 2):
            CreateGameView._check_player(players, i, errors, validated_players)
            CreateGameView._check_player(players, i + 1, errors, validated_players)
            if players[i] is None and players[i + 1] is None:
                errors.append(error_messages.BOTH_PLAYERS_ARE_NONE)
        if len(players) % 2 == 1:
            CreateGameView._check_player(players, len(players) - 1, errors, validated_players)
        if len(validated_players) <= 1:
            errors.append(error_messages.NEED_AT_LEAST_2_PLAYERS_THAT_ARENT_NONE)

        return players

    @staticmethod
    def _check_player(players: list[any],
                      index: int,
                      errors: list[str],
                      validated_players: set[int]):
        if players[index] is None:
            return

        try:
            if not isinstance(players[index], int):
                players[index] = int(players[index])
        except ValueError:
            errors.append(error_messages.player_is_not_an_optional_int(index))
            return

        if players[index] in validated_players:
            errors.append(error_messages.player_is_found_multiple_times(players[index]))
        else:
            validated_players.add(players[index])

    @staticmethod
    def _get_request_issuer(json_body, errors) -> str:
        request_issuer = json_body.get('request_issuer')
        if request_issuer is None:
            errors.append(error_messages.REQUEST_ISSUER_FIELD_MISSING)
            return ''

        if not isinstance(request_issuer, str):
            errors.append(error_messages.REQUEST_ISSUER_IS_NOT_A_STRING)
            return ''

        if request_issuer not in (settings.TOURNAMENT, settings.MATCHMAKING):
            errors.append(error_messages.REQUEST_ISSUER_IS_NOT_VALID)
            return ''

        return request_issuer


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['POST']), name='dispatch')
class CreatePrivateGameView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        api_name = shared_settings.PRIVATE_GAME
        user_id = self._get_user_id(request)
        players = [user_id]

        try:
            opponent_id = self._get_opponent_id(request)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=400)
        try:
            opponent_status = self._get_opponent_friend_status(
                request.headers.get('Authorization'),
                opponent_id
            )
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        if opponent_status != 'accepted':
            return JsonResponse(
                {
                    'errors': [error_messages.opponent_not_friend(opponent_id)]
                },
                status=403
            )
        players.append(opponent_id)
        try:
            port: int = GameCreator.create_game_server(0, players, api_name)
            self.send_private_notification(port, user_id, players[1])
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        return JsonResponse({'port': port}, status=201)

    @staticmethod
    def _get_user_id(request: HttpRequest) -> int:
        jwt = request.headers.get('Authorization')
        split_jwt = jwt.split('.')
        payload = base64.b64decode(split_jwt[1] + '===')

        payload_dict = json.loads(payload)
        return int(payload_dict['user_id'])

    @staticmethod
    def _get_opponent_id(request: HttpRequest) -> int:
        try:
            json_body = json.loads(request.body.decode('utf-8'))
        except Exception:
            raise Exception(error_messages.BAD_JSON_FORMAT)
        opponent_id = json_body.get('opponent_id')
        if opponent_id is None:
            raise Exception(error_messages.OPPONENT_ID_FIELD_MISSING)
        if not isinstance(opponent_id, int):
            raise Exception(error_messages.OPPONENT_ID_FIELD_IS_NOT_AN_INTEGER)
        return json_body.get('opponent_id')

    @staticmethod
    def _get_opponent_friend_status(access_token: str, opponent: int) -> str:
        try:
            response = InternalRequests.get(
                url=f'{common_settings.FRIEND_STATUS_ENDPOINT}',
                params={'friend_id': opponent},
                headers={'Authorization': access_token}
            )
        except Exception as e:
            raise Exception(f'Failed to access friends service : {e}')
        if response.status_code != 200:
            raise Exception(f'Failed to get friend request status : {response.json()}')
        return response.json()['status']

    @staticmethod
    def send_private_notification(port: int, user_id: int, opponent_id: int):
        notification_data = {
            'title': f'Invitation to a private party from {user_id}',
            'type': 'private_game',
            'user_list': [opponent_id],
            'data': f'{port}',
        }
        try:
            response = InternalAuthRequests.post(
                url=common_settings.USER_NOTIFICATION_ENDPOINT,
                data=json.dumps(notification_data)
            )
        except Exception as e:
            raise Exception(f'Failed to access notification service : {e}')
        if response.status_code != 201:
            raise Exception(f'Failed to send notification : {response.json()}')
