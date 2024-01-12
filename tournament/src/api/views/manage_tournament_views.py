import json

from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

from api.models import Tournament
from api.views.tournament_views import TournamentView
from api import error_message as error
from tournament.authenticate_request import authenticate_request


@method_decorator(csrf_exempt, name='dispatch')
class ManageTournamentView(View):
    @staticmethod
    def get(request: HttpRequest, tournament_id: int) -> JsonResponse:
        # TODO uncomment this line when jwt will be implemented
        # user, authenticate_errors = authenticate_request(request)
        # if user is None:
        #     return JsonResponse(data={'errors': authenticate_errors}, status=401)

        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'tournament with id `{tournament_id}` does not exist'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        try:
            tournament_players = tournament.players.all()
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        tournament_data = {
            'id': tournament.id,
            'name': tournament.name,
            'max-players': tournament.max_players,
            'nb-players': len(tournament_players),
            'players': [{
                'nickname': player.nickname,
                'user-id': player.user_id
            } for player in tournament_players],
            'is-private': tournament.is_private,
            'status': TournamentView.status_to_string(tournament.status),
        }
        # TODO add admin username

        if tournament.registration_deadline is not None:
            tournament_data['registration-deadline'] = tournament.registration_deadline

        return JsonResponse(tournament_data, status=200)

    @staticmethod
    def delete(request: HttpRequest, tournament_id: int) -> JsonResponse:
        # TODO uncomment this line when jwt will be implemented
        # user, authenticate_errors = authenticate_request(request)
        # if user is None:
        #     return JsonResponse(data={'errors': authenticate_errors}, status=401)
        user = {'id': 1}

        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except ObjectDoesNotExist:
            return JsonResponse({'error': f'tournament with id `{tournament_id}` does not exist'}, status=404)

        tournament_name = tournament.name
        tournament_admin = tournament.admin_id

        if tournament_admin != user['id']:
            return JsonResponse({
                'error': f'you cannot delete `{tournament_name}` because you are not the owner of the tournament'
            }, status=403)

        try:
            tournament.delete()
        except:
            return JsonResponse({'error': f'cannot delete `{tournament_name}`'}, status=500)

        return JsonResponse({'message': f'tournament `{tournament_name}` successfully deleted'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class UpdateSettingsView(View):
    @staticmethod
    def patch(request: HttpRequest, tournament_id: int) -> JsonResponse:
        # TODO uncomment this line when jwt will be implemented
        # user, authenticate_errors = authenticate_request(request)
        # if user is None:
        #     return JsonResponse(data={'errors': authenticate_errors}, status=401)
        user = {'id': 1}

        try:
            body = json.loads(request.body.decode('utf8'))
        except json.JSONDecodeError:
            return JsonResponse(data={'errors': [error.BAD_JSON_FORMAT]}, status=400)

        try:
            tournament = Tournament.objects.get(id=tournament_id)
        except ObjectDoesNotExist:
            return JsonResponse({'errors': [f'tournament with id `{tournament_id}` does not exist']}, status=404)
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        if tournament.status != Tournament.CREATED:
            return JsonResponse(
                {'errors': [f'The tournament has already started, so you cannot update the settings']},
                status=403
            )

        if tournament.admin_id != user['id']:
            return JsonResponse(
                {'errors': [f'You are not the owner of the tournament, so you cannot update the settings']},
                status=403
            )

        try:
            tournament_players = tournament.players.all()
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        new_name = body.get('name')
        if new_name is not None:
            valid_name, name_errors = TournamentView.is_valid_name(new_name)
            if not valid_name:
                return JsonResponse(data={'errors': name_errors}, status=400)
            tournament.name = new_name

        new_max_players = body.get('max-players')
        if new_max_players is not None:
            valid_max_players, max_players_error = TournamentView.is_valid_max_players(new_max_players)
            if not valid_max_players:
                return JsonResponse(data={'errors': [max_players_error]}, status=400)
            elif len(tournament_players) > new_max_players:
                return JsonResponse(
                    data={'errors': [f'You cannot set the max players to {new_max_players} because there are already '
                                     f'{len(tournament_players)} players registered']},
                    status=400
                )
            tournament.max_players = new_max_players

        new_registration_deadline = body.get('registration-deadline')
        if new_registration_deadline is not None:
            valid_registration_deadline, registration_deadline_error = TournamentView.is_valid_deadline(
                new_registration_deadline)
            if not valid_registration_deadline:
                return JsonResponse(data={'errors': [registration_deadline_error]}, status=400)
            tournament.registration_deadline = new_registration_deadline

        new_is_private = body.get('is-private')
        if new_is_private is not None:
            valid_is_private, is_private_error = TournamentView.is_valid_private(new_is_private)
            if not valid_is_private:
                return JsonResponse(data={'errors': [is_private_error]}, status=400)
            tournament.is_private = new_is_private

        try:
            tournament.save()
        except Exception as e:
            return JsonResponse({'errors': [str(e)]}, status=500)

        tournament_data = {
            'id': tournament.id,
            'name': tournament.name,
            'max-players': tournament.max_players,
            'is-private': tournament.is_private,
            'registration-deadline': tournament.registration_deadline,
            'status': TournamentView.status_to_string(tournament.status),
        }

        return JsonResponse(tournament_data, status=200)
