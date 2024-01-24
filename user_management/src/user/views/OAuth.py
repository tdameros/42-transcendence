from datetime import timedelta
from hashlib import sha256

import requests
from django.http import JsonResponse
from django.utils import timezone
from django.views import View

from user.models import PendingOAuth, User
from user_management import settings
from user_management.JWTManager import JWTManager
from user_management.utils import (download_image_from_url,
                                   generate_random_string)


class OAuthFactory:
    @staticmethod
    def create_oauth_handler(auth_service):
        if auth_service == 'github':
            return GitHubOAuth()
        elif auth_service == '42api':
            return FtApiOAuth()
        else:
            return None


class BaseOAuth(View):
    @staticmethod
    def get(request, auth_service):
        oauth_handler = OAuthFactory.create_oauth_handler(auth_service)
        if oauth_handler:
            return oauth_handler.handle_auth(request)
        else:
            return JsonResponse(data={'errors': ['Unknown auth service']}, status=400)

    @staticmethod
    def create_pending_oauth():
        state = generate_random_string(settings.OAUTH_STATE_MAX_LENGTH)
        hashed_state = sha256(str(state).encode('utf-8')).hexdigest()
        PendingOAuth.objects.create(hashed_state=hashed_state)
        return state

    def handle_auth(self, request):
        raise NotImplementedError("Subclasses must implement this method")


class GitHubOAuth(BaseOAuth):
    def handle_auth(self, request):
        state = self.create_pending_oauth()
        authorization_url = self.get_github_authorization_url(state)
        return JsonResponse(data={'redirection_url': authorization_url}, status=200)

    @staticmethod
    def get_github_authorization_url(state):
        return (
            f"{settings.GITHUB_AUTHORIZE_URL}"
            f"?client_id={settings.GITHUB_CLIENT_ID}"
            f"&redirect_uri={settings.GITHUB_REDIRECT_URI}"
            f"&state={state}"
            f"&scope=user:email"
        )


class FtApiOAuth(BaseOAuth):
    def handle_auth(self, request):
        state = self.create_pending_oauth()
        authorization_url = self.get_ft_api_authorization_url(state)
        return JsonResponse(data={'redirection_url': authorization_url}, status=200)

    @staticmethod
    def get_ft_api_authorization_url(state):
        return (
            f"{settings.FT_API_AUTHORIZE_URL}"
            f"?client_id={settings.FT_API_CLIENT_ID}"
            f"&redirect_uri={settings.FT_API_REDIRECT_URI}"
            f"&response_type=code"
            f"&state={state}"
        )


class OAuthCallback(View):
    access_token_url = None
    client_id = None
    client_secret = None
    redirect_uri = None

    def set_params(self, auth_service):
        if auth_service == 'github':
            self.access_token_url = settings.GITHUB_ACCESS_TOKEN_URL
            self.client_id = settings.GITHUB_CLIENT_ID
            self.client_secret = settings.GITHUB_CLIENT_SECRET.replace("'", "")
            self.redirect_uri = settings.GITHUB_REDIRECT_URI
        elif auth_service == '42api':
            self.access_token_url = settings.FT_API_ACCESS_TOKEN_URL
            self.client_id = settings.FT_API_CLIENT_ID
            self.client_secret = settings.FT_API_CLIENT_SECRET.replace("'", "")
            self.redirect_uri = settings.FT_API_REDIRECT_URI

    def get(self, request, auth_service):
        code = request.GET.get('code')
        state = request.GET.get('state')
        print(f"Received code: {code}")
        print(f"Received state: {state}")
        self.set_params(auth_service)
        self.check_and_update_state(code, state)
        access_token = self.get_access_token(code, state, auth_service)
        if not access_token:
            return JsonResponse(data={'errors': ['Failed to retrieve access token']}, status=400)

        login, avatar_url, email = self.get_user_infos(access_token, auth_service)
        user = self.create_or_get_user(login, email, avatar_url)
        if not user:
            return JsonResponse(data={'errors': ['Failed to create or get user']}, status=400)

        success, refresh_token, errors = JWTManager('refresh').generate_token(user.id)
        if not success:
            return JsonResponse(data={'errors': errors}, status=400)

        return JsonResponse(data={'refresh_token': refresh_token}, status=201)

    @staticmethod
    def create_or_get_user(login, email, avatar_url):
        user = User.objects.filter(email=email).first()

        if user is None:
            user = User.objects.create(username=login, email=email, password=None)
            if not download_image_from_url(avatar_url, user):
                return None
            user.save()

        return user

    @staticmethod
    def get_user_infos(access_token, auth_service):
        if auth_service == 'github':
            github_user_profile_url = settings.GITHUB_USER_PROFILE_URL
            headers = {
                'Accept': 'application/vnd.github+json',
                'Authorization': f'Bearer {access_token}',
                'X-GitHub-Api-Version': '2022-11-28'
            }
            response = requests.get(github_user_profile_url, headers=headers)
            if response.status_code != 200:
                print(f"Error: {response.status_code}, {response.text}")
                return None
            user_profile = response.json()
            login = user_profile['login']
            avatar_url = user_profile['avatar_url']
            email_url = settings.GITHUB_USER_PROFILE_URL + '/emails'
            response = requests.get(email_url, headers=headers)
            email = response.json()[0]['email']
            return login, avatar_url, email
        if auth_service == '42api':
            ft_api_user_profile_url = settings.FT_API_USER_PROFILE_URL
            headers = {
                'Accept': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.get(ft_api_user_profile_url, headers=headers)
            if response.status_code != 200:
                print(f"Error: {response.status_code}, {response.text}")
                return None
            user_profile = response.json()
            login = user_profile['login']
            avatar_url = user_profile['image']['link']
            email = user_profile['email']
            return login, avatar_url, email

    @staticmethod
    def check_and_update_state(code, state):
        hashed_state = sha256(str(state).encode('utf-8')).hexdigest()
        pending_oauth = PendingOAuth.objects.filter(hashed_state=hashed_state).first()
        if pending_oauth is None:
            return JsonResponse(data={'errors': ['Invalid state']}, status=400)
        pending_oauth.delete()
        PendingOAuth.objects.filter(created_at__lte=timezone.now() - timedelta(minutes=5)).delete()

    def get_access_token(self, code, state, auth_service):
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code',
            'scope': 'public'
        }
        headers = {
            'Accept': 'application/json'
        }

        response = requests.post(self.access_token_url, data=payload, headers=headers)
        if response.status_code != 200:
            print(f"Error: {response.status_code}, {response.text}")
            return None
        access_token = response.json()['access_token']
        print(f"Received access token: {access_token}")

        return access_token



