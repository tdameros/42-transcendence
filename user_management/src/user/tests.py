import json
import random
from datetime import datetime, timedelta

import jwt
import pyotp
from django.test import TestCase
from django.urls import reverse

from user.models import User
from user_management import settings
from user_management.JWTManager import UserAccessJWTManager


class TestsSignup(TestCase):

    def run_signup_test(self, name, username, email, password, expected_status, has_refresh_token,
                        expected_errors=None):
        data = {
            'username': username,
            'email': email,
            'password': password,
        }
        url = reverse('signup')
        result = self.client.post(url, json.dumps(data), content_type='application/json')

        if expected_status == 201 and result.status_code != 201:
            print(f'Failed test {name}')
            print(result.json())
        self.assertEqual(result.status_code, expected_status)
        if has_refresh_token:
            self.assertTrue('refresh_token' in result.json())
        else:
            self.assertTrue('errors' in result.json())
        if expected_errors:
            self.assertEqual(result.json()['errors'], expected_errors)

    def test_signup_valid_username(self):
        password = 'Validpass42*'
        has_refresh_token = True
        expected_status = 201
        name = 'Valid Username'
        long_username = 'a' * settings.USERNAME_MAX_LENGTH
        valid_usernames = [
            'Aurel', 'aurel', 'aa',
            'AA', 'aurelien', 'aurel42',
            'aurelx42', 'aurelh42', long_username
        ]
        for username in valid_usernames:
            email = 'c' + random.randint(0, 100000).__str__() + '@a.fr'
            self.run_signup_test(name,
                                 username,
                                 email,
                                 password,
                                 expected_status,
                                 has_refresh_token)

    def test_signup_invalid_username(self):
        password = 'Validpass42*'
        has_refresh_token = False
        expected_status = 400
        name = 'Invalid Username'
        long_username = 'a' * (settings.USERNAME_MAX_LENGTH + 1)
        invalid_usernames = [
            (None, 'Username empty'),
            ('', 'Username empty'),
            ('a' * (settings.USERNAME_MIN_LENGTH - 1),
             f'Username length {settings.USERNAME_MIN_LENGTH - 1} < {settings.USERNAME_MIN_LENGTH}'),
            (long_username, f'Username length {len(long_username)} > {settings.USERNAME_MAX_LENGTH}'),
        ]
        for invalid_username in invalid_usernames:
            username = invalid_username[0]
            expected_errors = [invalid_username[1]]
            email = 'b' + random.randint(0, 100000).__str__() + '@a.fr'
            self.run_signup_test(name,
                                 username,
                                 email,
                                 password,
                                 expected_status,
                                 has_refresh_token,
                                 expected_errors)

    def test_signup_valid_email(self):
        password = 'Validpass42*'
        has_refresh_token = True
        expected_status = 201
        name = 'Valid Email'
        long_email = ('a' * (settings.EMAIL_MAX_LENGTH - 5)) + '@a.fr'
        valid_emails = [
            'aurelien.levra@gmail.com',
            'a@a.fr', 'aurel@asd.fr',
            long_email
        ]
        for email in valid_emails:
            username = 'Aurel' + str(random.randint(0, 100000))  # To avoid `username already taken` error
            self.run_signup_test(name, username, email, password, expected_status, has_refresh_token)

    def test_signup_invalid_email(self):
        password = 'Validpass42*'
        has_refresh_token = False
        expected_status = 400
        name = 'Invalid Email'
        long_email = ('a' * (settings.EMAIL_MAX_LENGTH - 4)) + '@a.fr'
        invalid_emails = [
            (None, 'Email empty'),
            ('', 'Email empty'),
            (long_email, f'Email length {len(long_email)} > {settings.EMAIL_MAX_LENGTH}'),
            ('aurel$@gmail.com', 'Invalid character in email address'),
            ('aurelien.levra', 'Email missing @'),
            ('@a.fr', 'Local part length 0 < 1'),
            ('aurel@asd', 'Email missing "." character'),
            ('a@a@a.fr', 'Email contains more than one @ character'),
            ('@a.fr', f'Local part length 0 < {settings.EMAIL_LOCAL_PART_MIN_LENGTH}'),
            ('a.@a', 'Email missing TLD'),
            ('a@a.123456789ABCDEFG', f'TLD length 16 > {settings.TLD_MAX_LENGTH}'),
        ]
        for invalid_email in invalid_emails:
            email = invalid_email[0]
            expected_errors = [invalid_email[1]]
            username = 'Aurel' + str(random.randint(0, 100000))
            self.run_signup_test(name,
                                 username,
                                 email,
                                 password,
                                 expected_status,
                                 has_refresh_token,
                                 expected_errors)

    def test_signup_valid_password(self):
        has_refresh_token = True
        expected_status = 201
        name = 'Valid Password'
        valid_passwords = [
            'Validpass42*', 'a' * (settings.PASSWORD_MAX_LENGTH - 3) + 'A1*',
                            'a' * (settings.PASSWORD_MIN_LENGTH - 3) + 'A1*'
        ]
        for password in valid_passwords:
            username = 'Aurel' + str(random.randint(0, 100000))
            email = 'a' + random.randint(0, 100000).__str__() + '@a.fr'
            self.run_signup_test(name,
                                 username,
                                 email,
                                 password,
                                 expected_status,
                                 has_refresh_token)

    def test_signup_invalid_password(self):
        has_refresh_token = False
        expected_status = 400
        name = 'Invalid Password'
        email = 'alevra@student.42Lyon.fr'
        invalid_passwords = [
            (None, 'Password empty'),
            ('', 'Password empty'),
            ('a' * (settings.PASSWORD_MIN_LENGTH - 4) + 'A1*',
             f'Password length {settings.PASSWORD_MIN_LENGTH - 1} < {settings.PASSWORD_MIN_LENGTH}'),
            ('a' * (settings.PASSWORD_MAX_LENGTH - 2) + 'A1*',
             f'Password length {settings.PASSWORD_MAX_LENGTH + 1} > {settings.PASSWORD_MAX_LENGTH}'),
            ('a' * settings.PASSWORD_MIN_LENGTH + '1*', 'Password missing uppercase character'),
            ('A' * settings.PASSWORD_MIN_LENGTH + '1*', 'Password missing lowercase character'),
            ('a' * settings.PASSWORD_MIN_LENGTH + 'A*', 'Password missing digit'),
            ('a' * settings.PASSWORD_MIN_LENGTH + 'A1', 'Password missing special character'),
        ]
        for invalid_password in invalid_passwords:
            password = invalid_password[0]
            expected_errors = [invalid_password[1]]
            username = 'Aurel' + str(random.randint(0, 100000))
            self.run_signup_test(name,
                                 username,
                                 email,
                                 password,
                                 expected_status,
                                 has_refresh_token,
                                 expected_errors)

    def test_signup_not_a_json(self):
        string = 'This is not a JSON'
        url = reverse('signup')
        result = self.client.post(url, string, content_type='application/json')
        self.assertEqual(result.status_code, 400)
        self.assertTrue('errors' in result.json())


class TestsSignin(TestCase):

    def test_signin(self):
        data_preparation = {
            'username': 'aurelien123',
            'email': 'a@a.fr',
            'password': 'Validpass42*',
        }
        url = reverse('signup')
        self.client.post(url, json.dumps(data_preparation), content_type='application/json')
        data = {
            'username': 'aurelien123',
            'password': 'Validpass42*',
        }
        url = reverse('signin')
        result = self.client.post(url, json.dumps(data), content_type='application/json')

        self.assertEqual(result.status_code, 200)
        data_wrong_pass = {
            'username': 'aurelien123',
            'password': 'WrongValidpass42*',
        }
        url = reverse('signin')
        result = self.client.post(url, json.dumps(data_wrong_pass), content_type='application/json')
        self.assertEqual(result.status_code, 400)


class TestsUsernameExist(TestCase):

    def test_username_exist(self):
        data_preparation = {
            'username': 'Burel305',
            'email': 'a@a.fr',
            'password': 'Validpass42*',
        }
        url = reverse('signup')
        self.client.post(url, json.dumps(data_preparation), content_type='application/json')
        data_username_exist = {
            'username': 'Burel305'
        }
        url = reverse('username-exist')
        result = self.client.post(url, json.dumps(data_username_exist), content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('is_taken' in result.json())
        self.assertTrue(result.json()['is_taken'])

        data_username_not_exist = {
            'username': 'Aurel304',
        }
        url = reverse('username-exist')
        result = self.client.post(url, json.dumps(data_username_not_exist), content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('is_taken' in result.json())
        self.assertFalse(result.json()['is_taken'])


class TestsRefreshJWT(TestCase):

    def test_refresh_jwt(self):
        data_preparation = {
            'username': 'Aurel303',
            'email': 'alevra@gmail.com',
            'password': 'Validpass42*',
        }
        url = reverse('signup')
        result = self.client.post(url, json.dumps(data_preparation), content_type='application/json')
        data = {
            'refresh_token': result.json()['refresh_token']
        }
        url = reverse('refresh-access-jwt')
        result = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('access_token' in result.json())
        # 1 Refresh token not found
        valid_access_token = UserAccessJWTManager.generate_jwt(1)[1]

        # 2 Invalid token
        valid_payload = {
            'user_id': 1,
            'exp': datetime.utcnow() + timedelta(minutes=100),
            'token_type': 'refresh'
        }
        bad_signature_token = jwt.encode(valid_payload,
                                         "INVALID_KEY",
                                         'HS256')
        # 3 Empty payload
        payload = {}
        empty_payload = jwt.encode(payload, settings.REFRESH_KEY, 'HS256')

        # 4 Token expired
        payload_expired = {
            'user_id': 1,
            'exp': datetime.utcnow(),
            'token_type': 'refresh'
        }
        expired_token = jwt.encode(payload_expired, settings.REFRESH_KEY, 'HS256')

        # 5 No user_id in payload
        payload_no_user_id = {
            'exp': datetime.utcnow() + timedelta(minutes=100),
            'token_type': 'refresh'
        }
        token_no_user_id = jwt.encode(payload_no_user_id, settings.REFRESH_KEY, 'HS256')

        # 6 User does not exist
        payload_user_not_exist = {
            'user_id': 999,
            'exp': datetime.utcnow() + timedelta(minutes=100),
            'token_type': 'refresh'
        }
        token_user_not_exist = jwt.encode(payload_user_not_exist, settings.REFRESH_KEY, 'HS256')

        errors = [('Refresh token not found', {'access_token': valid_access_token}),
                  ('Signature verification failed', {'refresh_token': bad_signature_token}),
                  ('No expiration date found', {'refresh_token': empty_payload}),
                  ('Signature has expired', {'refresh_token': expired_token}),
                  ('No user_id in payload', {'refresh_token': token_no_user_id}),
                  ('User does not exist', {'refresh_token': token_user_not_exist})
                  ]

        for error in errors:
            url = reverse('refresh-access-jwt')
            try:
                result = self.client.post(url, json.dumps(error[1]), content_type='application/json')
            except Exception as e:
                print(e)
            self.assertEqual(result.status_code, 400)
            self.assertTrue('errors' in result.json())
            self.assertEqual(result.json()['errors'], [error[0]])


class TestsEmailExist(TestCase):

    def test_email_exist(self):
        data_preparation = {
            'username': 'Aurel305',
            'email': 'a@a.fr',
            'password': 'Validpass42*',
        }
        url = reverse('signup')
        self.client.post(url, json.dumps(data_preparation), content_type='application/json')
        data_email_exist = {
            'email': 'a@a.fr'
        }
        url = reverse('email-exist')
        result = self.client.post(url, json.dumps(data_email_exist), content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('is_taken' in result.json())
        self.assertTrue(result.json()['is_taken'])

        data_email_not_exist = {
            'email': 'a@afwefwe.fr'
        }
        url = reverse('email-exist')
        result = self.client.post(url, json.dumps(data_email_not_exist), content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('is_taken' in result.json())
        self.assertFalse(result.json()['is_taken'])


class UserId(TestCase):

    def test_user_id(self):
        data_preparation = {
            'username': 'Aurel303',
            'email': 'alevra@gmail.com',
            'password': 'Validpass42*',
        }
        url = reverse('signup')
        self.client.post(url, json.dumps(data_preparation), content_type='application/json')
        user = User.objects.all().first()
        url = reverse('user-id', args=[user.id])
        result = self.client.get(url)
        self.assertEqual(result.status_code, 200)
        self.assertTrue('username' in result.json())


class TestsSearchUsername(TestCase):

    def test_search_username(self):
        for i in range(1, 20):
            data_preparation = {
                'username': f'Felix{i}',
                'email': f'felix{i}@gmail.com',
                'password': 'Validpass42*',
            }
            url = reverse('signup')
            self.client.post(url, json.dumps(data_preparation), content_type='application/json')
        data = {
            'username': 'Felix'
        }
        url = reverse('search-username')
        result = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('users' in result.json())
        self.assertEqual(len(result.json()['users']), 10)
        self.assertEqual(result.json()['users'][0], 'Felix1')
        self.assertEqual(result.json()['users'][9], 'Felix10')
        data = {
            'username': 'Felix1'
        }
        url = reverse('search-username')
        result = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('users' in result.json())
        self.assertEqual(len(result.json()['users']), 10)
        self.assertEqual(result.json()['users'][0], 'Felix1')
        data = {
            'username': 'Felix2'
        }
        url = reverse('search-username')
        result = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('users' in result.json())
        self.assertEqual(len(result.json()['users']), 1)
        self.assertEqual(result.json()['users'][0], 'Felix2')
        data = {
            'username': 'Felix111'
        }
        url = reverse('search-username')
        result = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('users' in result.json())
        self.assertEqual(len(result.json()['users']), 0)


class TestsTwoFa(TestCase):

    def test_two_fa(self):
        data_preparation = {
            'username': 'TestTwoFA',
            'email': 'aurelien.levra@gmail.com',
            'password': 'Validpass42*',
        }
        url = reverse('signup')
        result = self.client.post(url, json.dumps(data_preparation), content_type='application/json')
        refresh_token = result.json()['refresh_token']
        data = {
            'refresh_token': refresh_token
        }
        url = reverse('refresh-access-jwt')
        result = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(result.status_code, 200)
        access_token = result.json()['access_token']
        url = reverse('enable-2fa')
        result = self.client.post(url, content_type='application/json', HTTP_AUTHORIZATION=f'{access_token}')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('image/png' in result['Content-Type'])
        url = reverse('verify-2fa')
        data = {
            'code': '234567'  # Invalid code but base32
        }

        result = self.client.post(url, json.dumps(data), content_type='application/json',
                                  HTTP_AUTHORIZATION=f'{access_token}')

        self.assertEqual(result.status_code, 400)
        real_code = pyotp.TOTP(User.objects.get(username='TestTwoFA').totp_secret).now()
        data = {
            'code': real_code
        }
        result = self.client.post(url, json.dumps(data), content_type='application/json',
                                  HTTP_AUTHORIZATION=f'{access_token}')
        self.assertEqual(result.status_code, 200)
        url = reverse('disable-2fa')
        result = self.client.post(url, content_type='application/json', HTTP_AUTHORIZATION=f'{access_token}')
        self.assertEqual(result.status_code, 200)
