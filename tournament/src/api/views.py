from django.http import JsonResponse
from django.views import View
from api.models import Tournament
from tournament.authenticate_request import authenticate_request
from tournament import settings
import json


class Tournament(View):
    def post(self, request):
        try:
            user, authenticate_errors = authenticate_request(request)
            if user is None:
                return JsonResponse(data={'errors': authenticate_errors}, status=401)
            json_request = json.loads(request.body.decode('utf8'))
            valid_tournament, errors = Tournament.is_valid_tournament(json_request)
            if not valid_tournament:
                return JsonResponse(data={'errors': errors}, status=400)
            Tournament.objects.create(
                name=json_request['name']
            )
            return JsonResponse(data={}, status=201)
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': ['Invalid JSON format in request body']}, status=400)

    @staticmethod
    def is_valid_tournament(json_request):
        errors = []
        name = json_request.get('name')
        valid_name, name_errors = Tournament.is_valid_name(name)
        if not valid_name:
            errors.append(name_errors)
        if errors:
            return False, errors
        return True, None

    @staticmethod
    def is_valid_name(name):
        errors = []

        if name is None:
            errors.append('Missing name field')
        if len(name) < settings.MIN_TOURNAMENT_NAME_LENGTH:
            errors.append(f'Tournament name must contain at least {settings.MIN_TOURNAMENT_NAME_LENGTH} characters')
        elif len(name) > settings.MAX_TOURNAMENT_NAME_LENGTH:
            errors.append(f'Tournament name must contain less than {settings.MAX_TOURNAMENT_NAME_LENGTH} characters')
        if not name.replace(' ', '').isalnum():
            errors.append('Tournament name may only contain letters, numbers and spaces')

        if errors:
            return False, errors
        return True, None



