import json

from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from user.models import User
from user_management.JWTManager import UserAccessJWTManager
from user_management.utils import is_valid_username, is_valid_email, is_valid_password


class UserUpdateInfosManager:
    FIELD_VALIDATORS = {
        'username': {'validator': is_valid_username},
        'email': {'validator': is_valid_email},
        'avatar': {'validator': lambda x: True},
        'password': {'validator': is_valid_password},
    }

    @staticmethod
    def update_infos(user_id, json_request):
        errors = []

        change_list = json_request.get('change_list')
        if change_list is None:
            return False, ['change_list must be provided']

        UserUpdateInfosManager.validate_change_list(change_list, errors, json_request)
        if errors:
            return False, errors

        for field in change_list:
            value = json_request.get(field)
            success, update_errors = UserUpdateInfosManager.update_user_field(user_id, field, value)
            if not success:
                errors.append({field: update_errors})
                return False, errors

        return True, None

    @staticmethod
    def validate_change_list(change_list, errors, json_request):
        """Ensure that the requested changes are as valid as when a user signs up for the first time"""
        for field in change_list:
            if field in UserUpdateInfosManager.FIELD_VALIDATORS:
                value = json_request.get(field)
                validator = UserUpdateInfosManager.FIELD_VALIDATORS[field]['validator']

                valid, error_message = validator(value)
                if not valid:
                    errors.append({field: error_message})

    @staticmethod
    def update_user_field(user_id, field_name, new_value):
        try:
            user = User.objects.get(id=user_id)
            setattr(user, field_name, new_value)
            user.save()
            return True, None
        except Exception as e:
            return False, [f'An unexpected error occurred while updating user information: {e}']


@method_decorator(csrf_exempt, name='dispatch')
class UpdateInfos(View):
    @staticmethod
    def post(request):
        try:
            json_request = json.loads(request.body.decode('utf-8'))
            access_token = json_request.get('access_token')
            if access_token is None:
                return JsonResponse(data={'errors': ['Access token not found']}, status=400)
            success, user_id, errors = UserAccessJWTManager.authenticate(access_token)
            if success is False:
                return JsonResponse(data={'errors': errors}, status=400)
            success, errors = UserUpdateInfosManager.update_infos(user_id, json_request)
            if success is False:
                return JsonResponse(data={'errors': errors}, status=400)
            return JsonResponse(data={'ok': 'ok'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': ['Invalid JSON format in the request body']}, status=400)
        except Exception as e:
            return JsonResponse(data={'errors': [f'An unexpected error occurred : {e}']}, status=500)
