import urllib
from abc import ABC, abstractmethod
from datetime import timedelta
from hashlib import sha256

import requests
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from django.views import View

from user.models import PendingOAuth, User, UserOAuth
from user_management import settings
from user_management.JWTManager import UserRefreshJWTManager
from user_management.utils import (download_image_from_url,
                                   generate_random_string, is_valid_username,
                                   post_user_stats)


class OAuthFactory:
    @staticmethod
    def create_oauth_handler(auth_service):
        if auth_service == 'github':
            return GitHubOAuth()
        elif auth_service == '42api':
            return FtApiOAuth()
        else:
            return None


class BaseOAuth(ABC):

    @staticmethod
    def create_pending_oauth(source):
        state = generate_random_string(settings.OAUTH_STATE_MAX_LENGTH)
        hashed_state = sha256(str(state).encode('utf-8')).hexdigest()
        PendingOAuth.objects.create(hashed_state=hashed_state, source=source)
        return state

    @abstractmethod
    def handle_auth(self, request, source):
        pass


class OAuth(View):

    @staticmethod
    def get(request, auth_service):
        source = request.GET.get('source')
        if source is None:
            return JsonResponse(data={'errors': ['No source provided']}, status=400)
        if not source.endswith('/'):
            source += '/'
        oauth_handler = OAuthFactory.create_oauth_handler(auth_service)
        if oauth_handler:
            return oauth_handler.handle_auth(request, source)
        else:
            return JsonResponse(data={'errors': ['Unknown auth service']}, status=400)


class GitHubOAuth(BaseOAuth):
    def handle_auth(self, request, source):
        state = self.create_pending_oauth(source)
        authorization_url = self.get_github_authorization_url(state)
        return JsonResponse(data={'redirection_url': authorization_url}, status=200)

    @staticmethod
    def get_github_authorization_url(state):
        return (
            f'{settings.GITHUB_AUTHORIZE_URL}'
            f'?client_id={settings.GITHUB_CLIENT_ID}'
            f'&redirect_uri={urllib.parse.quote_plus(settings.GITHUB_REDIRECT_URI)}'
            f'&state={state}'
            f'&scope=user:email'
        )


class FtApiOAuth(BaseOAuth):
    def handle_auth(self, request, source):
        state = self.create_pending_oauth(source)
        authorization_url = self.get_ft_api_authorization_url(state)
        return JsonResponse(data={'redirection_url': authorization_url}, status=200)

    @staticmethod
    def get_ft_api_authorization_url(state):
        return (
            f'{settings.FT_API_AUTHORIZE_URL}'
            f'?client_id={settings.FT_API_CLIENT_ID}'
            f'&redirect_uri={urllib.parse.quote_plus(settings.FT_API_REDIRECT_URI)}'
            f'&response_type=code'
            f'&state={state}'
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
            self.client_secret = settings.GITHUB_CLIENT_SECRET
            self.redirect_uri = settings.GITHUB_REDIRECT_URI
        elif auth_service == '42api':
            self.access_token_url = settings.FT_API_ACCESS_TOKEN_URL
            self.client_id = settings.FT_API_CLIENT_ID
            self.client_secret = settings.FT_API_CLIENT_SECRET
            self.redirect_uri = settings.FT_API_REDIRECT_URI

    def get(self, request, auth_service):
        if request.GET.get('error'):
            return redirect(f'{self.get_source_url(request.GET.get("state"))}?error='
                            f'Could not authenticate with {auth_service}')
        code = request.GET.get('code')
        state = request.GET.get('state')
        source = self.get_source_url(state)
        self.set_params(auth_service)
        if self.check_state(state) is False:
            return redirect(f'{source}?error=Invalid State')
        self.flush_pending_oauth(state)
        access_token = self.get_access_token(code)
        if not access_token:
            return redirect(f'{source}?error=Failed to retrieve access token')
        login, avatar_url, email, api_id = self.get_user_infos(access_token, auth_service)
        user, error = self.create_or_get_user(login, email, avatar_url, auth_service, api_id)
        if not user:
            return redirect(f'{source}?error={error}')
        success, refresh_token, errors = UserRefreshJWTManager.generate_jwt(user.id)
        if not success:
            return redirect(f'{source}?error=${errors}')
        response = redirect(source)
        response.set_cookie('refresh_token', refresh_token)
        return response

    @staticmethod
    def create_or_get_user(login, email, avatar_url, auth_service, api_id):
        try:
            with transaction.atomic():
                user = OAuthCallback._get_existing_user(auth_service, api_id, email)
                if user:
                    OAuthCallback._update_existing_user(user, auth_service, api_id)
                    return user, None
                login = OAuthCallback._generate_valid_username(login)
                user = OAuthCallback._create_user(login, email, avatar_url, auth_service, api_id)
                return user, None
        except Exception as e:
            return None, f'Failed to create user while executing OAuth process: {e}'

    @staticmethod
    def _get_existing_user(auth_service, api_id, email):
        user_oauth = UserOAuth.objects.filter(service=auth_service, service_id=api_id).first()
        if user_oauth:
            return user_oauth.user
        return User.objects.filter(email=email).first()

    @staticmethod
    def _update_existing_user(user, auth_service, api_id):
        user_oauth, created = UserOAuth.objects.get_or_create(user=user, service=auth_service)
        user_oauth.service_id = api_id
        user_oauth.save()
        user.last_activity = timezone.now()
        user.save()
        user.update_latest_login()

    @staticmethod
    def _generate_valid_username(login):
        if User.objects.filter(username=login).exists() or not is_valid_username(login):
            return generate_random_string(10)
        return login

    @staticmethod
    def _create_user(login, email, avatar_url, auth_service, api_id):
        try:
            user = User.objects.create(username=login, email=email, password=None)
            UserOAuth.objects.create(user=user, service=auth_service, service_id=api_id)
            success, error = post_user_stats(user.id)
            if not success:
                raise UserCreationError(f'Failed to post user stats: {error}')
            download_image_from_url(avatar_url, user)
            user.emailVerified = True
            user.save()
            return user
        except Exception:
            raise UserCreationError('Failed to create user')

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
                return None
            user_profile = response.json()
            login = user_profile['login']
            avatar_url = user_profile['avatar_url']
            id_api = user_profile['id']
            email_url = settings.GITHUB_USER_PROFILE_URL + '/emails'
            response = requests.get(email_url, headers=headers)
            email = response.json()[0]['email']
            return login, avatar_url, email, id_api
        if auth_service == '42api':
            ft_api_user_profile_url = settings.FT_API_USER_PROFILE_URL
            headers = {
                'Accept': 'application/json',
                'Authorization': f'Bearer {access_token}',
            }
            response = requests.get(ft_api_user_profile_url, headers=headers)
            if response.status_code != 200:
                return None
            user_profile = response.json()
            login = user_profile['login']
            avatar_url = user_profile['image']['link']
            email = user_profile['email']
            id_api = user_profile['id']
            return login, avatar_url, email, id_api

    @staticmethod
    def check_state(state):
        hashed_state = sha256(str(state).encode('utf-8')).hexdigest()
        pending_oauth = PendingOAuth.objects.filter(hashed_state=hashed_state).first()
        if pending_oauth is None:
            return False
        return True

    def get_access_token(self, code):
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
            return None
        access_token = response.json()['access_token']

        return access_token

    def get_source_url(self, state):
        pending_oauth = PendingOAuth.objects.filter(hashed_state=sha256(str(state).encode('utf-8')).hexdigest()).first()
        return pending_oauth.source

    def flush_pending_oauth(self, state):
        hashed_state = sha256(str(state).encode('utf-8')).hexdigest()
        PendingOAuth.objects.filter(hashed_state=hashed_state).delete()
        PendingOAuth.objects.filter(created_at__lte=timezone.now() - timedelta(minutes=5)).delete()


class UserCreationError(Exception):
    def __init__(self, message="User creation failed"):
        self.message = message
        super().__init__(self.message)
