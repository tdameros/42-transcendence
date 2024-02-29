import base64
import json

from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from api import error_messages
from api.GameCreator import GameCreator
from common.src import settings as common_settings
from common.src.internal_requests import InternalAuthRequests, InternalRequests
from common.src.jwt_managers import user_authentication
from shared_code import settings as shared_settings


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(user_authentication(['POST']), name='dispatch')
class CreatePrivateGameView(View):
    def post(self, request: HttpRequest) -> JsonResponse:
        # TODO: if this view is not deleted, make it check if a player is already in a game
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
