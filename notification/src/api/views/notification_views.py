import json
from typing import Optional

from django.http import JsonResponse, HttpRequest
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from api.models import Notification
from api import error_message as error
from notification import settings


@method_decorator(csrf_exempt, name='dispatch')
class DeleteUserNotificationView(View):
    @staticmethod
    def delete(request: HttpRequest, notification_id: int) -> JsonResponse:
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.delete()
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [error.NOTIFICATION_NOT_FOUND]}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        return JsonResponse({'message': 'Notification deleted'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UserNotificationView(View):
    @staticmethod
    def post(request: HttpRequest) -> JsonResponse:
        try:
            body = json.loads(request.body.decode('utf8'))
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': [error.BAD_JSON_FORMAT]}, status=400)

        title = body.get('title')
        type = body.get('type')
        user_list = body.get('user_list')
        data = body.get('data')

        is_valid, errors = UserNotificationView.validate_body(title, type, user_list, data)
        if not is_valid:
            return JsonResponse({'errors': errors}, status=400)

        try:
            for user_id in user_list:
                Notification.objects.create(title=title, type=type, owner_id=user_id, data=data)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        return JsonResponse({'message': 'Notification created'}, status=201)

    @staticmethod
    def validate_body(title: any, type: any, user_list: any, data: any) -> tuple[bool, Optional[list[str]]]:
        errors = []

        title_error = UserNotificationView.validate_title(title)
        type_error = UserNotificationView.validate_type(type)
        user_list_error = UserNotificationView.validate_user_list(user_list)
        data_error = UserNotificationView.validate_data(data)

        if title_error:
            errors.append(title_error)
        if type_error:
            errors.append(type_error)
        if user_list_error:
            errors.append(user_list_error)
        if data_error:
            errors.append(data_error)

        if errors:
            return False, errors
        return True, None

    @staticmethod
    def validate_title(title: any) -> Optional[str]:
        if title is None:
            return error.MISSING_TITLE
        if not isinstance(title, str):
            return error.INVALID_TITLE_FORMAT
        if len(title) > 255 or len(title) == 0:
            return error.INVALID_TITLE_LENGTH
        return None

    @staticmethod
    def validate_type(type: any) -> Optional[str]:
        if type is None:
            return error.MISSING_TYPE
        if not isinstance(type, str):
            return error.INVALID_TYPE_FORMAT
        if type not in settings.ALLOWED_USER_NOTIFICATION_TYPES:
            return error.TYPE_NOT_EXIST
        return None

    @staticmethod
    def validate_user_list(user_list: any) -> Optional[str]:
        if user_list is None:
            return error.MISSING_USER_LIST
        if not isinstance(user_list, list):
            return error.INVALID_USER_LIST_FORMAT
        for user in user_list:
            if not isinstance(user, int):
                return error.INVALID_USER_LIST_FORMAT
        return None

    @staticmethod
    def validate_data(data: any) -> Optional[str]:
        if data is not None and not isinstance(data, str):
            return error.INVALID_DATA_FORMAT
        return None
