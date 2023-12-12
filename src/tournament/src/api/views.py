from django.http import JsonResponse
from django.views import View
from api.models import Tournament
import json

class Tournament(View):
    def post(self, request):
        try:
            # TODO: Verify JWT
            json_request = json.loads(request.body.decode('utf8'))
            valid_tournament, errors = Tournament.is_valid_tournament(json_request)
            if not valid_tournament:
                return JsonResponse(data={"errors": errors}, status=400)
            Tournament.objects.create(
                name=json_request['name']
            )
            return JsonResponse(data={}, status=201)
        except json.JSONDecodeError:
            return JsonResponse(data={"errors": ["Invalid JSON format"]}, status=400)

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
        min_len = 3
        max_len = 20
        errors = []

        if len(name) < min_len:
            errors.append(f'Tournament name must contain at least {min_len} characters')
        elif len(name) > 20:
            errors.append(f'Tournament name must contain less than {max_len} characters')
        if not name.replace(' ', '').isalnum():
            errors.append('Tournament name may only contain letters, numbers and spaces')

        if errors:
            return False, errors
        return True, None



