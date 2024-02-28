import base64
import json
import secrets
import string
from io import BytesIO

import requests
from django.core.files import File
from django.core.files.base import ContentFile
from PIL import Image

import common.src.settings as common
from common.src.internal_requests import InternalAuthRequests
from user.models import User
from user_management import settings


def generate_random_string(length):
    alphanumeric_characters = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(alphanumeric_characters) for _ in range(length))
    return random_string


def download_image_from_url(url, model_instance):
    response = requests.get(url)
    if response.status_code == 200:
        try:
            img = Image.open(BytesIO(response.content))
            img_io = BytesIO()
            img.save(img_io, format='PNG')
            img_file = ContentFile(img_io.getvalue())
            random_suffixes = generate_random_string(10)
            model_instance.avatar.delete()
            model_instance.avatar.save(f'{model_instance.id}_{random_suffixes}.png', File(img_file), save=True)
        except Exception:
            return False
        return True
    else:
        return False


def get_image_format_from_base64(base64_string):
    try:
        image_format = base64_string.split(';base64')[0].split('/')[1]
        return image_format
    except Exception:
        return None


def save_image_from_base64(base64_string, model_instance):
    if not base64_string:
        return False, 'Image not found'
    try:
        img = Image.open(BytesIO(base64.b64decode(base64_string)))
        img_io = BytesIO()
        img_format = img.format if img.format else 'PNG'
        img.save(img_io, format=img_format)
        img_file = ContentFile(img_io.getvalue())
        random_suffixes = generate_random_string(10)
        model_instance.avatar.delete()
        model_instance.avatar.save(
            f'{model_instance.id}_{random_suffixes}.{img_format.lower()}', File(img_file), save=True
        )
    except Exception as e:
        return False, str(e)
    return True, None


def is_valid_username(username):
    if username is None or username == '':
        return False, 'Username empty'
    if len(username) < settings.USERNAME_MIN_LENGTH:
        return False, f'Username length {len(username)} < {settings.USERNAME_MIN_LENGTH}'
    if len(username) > settings.USERNAME_MAX_LENGTH:
        return False, f'Username length {len(username)} > {settings.USERNAME_MAX_LENGTH}'
    if not username.isalnum():
        return False, 'Username must be alphanumeric'
    users = User.objects.filter(username=username)
    if users.exists():
        return False, f'Username {username} already taken'
    return True, None


def is_valid_email(email):
    if email is None or email == '':
        return False, 'Email empty'
    users = User.objects.filter(email=email)
    if users.exists():
        return False, f'Email {email} already taken'
    if len(email) > settings.EMAIL_MAX_LENGTH:
        return False, f'Email length {len(email)} > {settings.EMAIL_MAX_LENGTH}'
    if any(char not in f'{string.ascii_letters}{string.digits}@_-.' for char in email):
        return False, 'Invalid character in email address'
    if '@' not in email:
        return False, 'Email missing @'
    if '.' not in email:
        return False, 'Email missing "." character'
    if email.count('@') > 1:
        return False, 'Email contains more than one @ character'
    local_part, domain_and_tld = email.rsplit('@', 1)
    if len(local_part) < settings.EMAIL_LOCAL_PART_MIN_LENGTH:
        return False, f'Local part length {len(local_part)} < {settings.EMAIL_LOCAL_PART_MIN_LENGTH}'
    if domain_and_tld.count('.') == 0:
        return False, 'Email missing TLD'
    tld = domain_and_tld.rsplit('.')[-1]
    if len(tld) > settings.TLD_MAX_LENGTH:
        return False, f'TLD length {len(tld)} > {settings.TLD_MAX_LENGTH}'
    return True, None


def is_valid_password(password):
    if password is None or password == '':
        return False, 'Password empty'
    if len(password) < settings.PASSWORD_MIN_LENGTH:
        return False, f'Password length {len(password)} < {settings.PASSWORD_MIN_LENGTH}'
    if len(password) > settings.PASSWORD_MAX_LENGTH:
        return False, f'Password length {len(password)} > {settings.PASSWORD_MAX_LENGTH}'
    if not any(char.isupper() for char in password):
        return False, 'Password missing uppercase character'
    if not any(char.islower() for char in password):
        return False, 'Password missing lowercase character'
    if not any(char.isdigit() for char in password):
        return False, 'Password missing digit'
    if not any(char in '!@#$%^&*()-_+=' for char in password):
        return False, 'Password missing special character'
    return True, None


def post_user_stats(user_id: int) -> (bool, list):
    try:
        response = InternalAuthRequests.post(
            f'{common.USER_STATS_USER_ENDPOINT}{user_id}/',
            data=json.dumps({})
        )
    except requests.exceptions.RequestException:
        return False, ['Could not access user-stats']
    if not response.ok:
        return False, ['Could not create user in user-stats']
    return True, None
