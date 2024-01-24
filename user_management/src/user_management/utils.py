import secrets
import string
from io import BytesIO

import requests
from django.core.files import File
from django.core.files.base import ContentFile
from PIL import Image


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
        except Exception as e:
            return False
        return True
    else:
        return False
