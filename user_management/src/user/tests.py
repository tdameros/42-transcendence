import json
import random

from django.test import TestCase
from django.urls import reverse

from user_management import settings


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
        email = 'alevra@asdf.fr'
        valid_usernames = [
            'Aurel', 'aurel', 'aa',
            'AA', 'aurelien', 'aurel42',
            'aurel_42', 'aurel-42', long_username
        ]
        for username in valid_usernames:
            print(f'\nTesting {name} with username {username}')
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
        email = 'alevra@student.42lyon.fr'
        long_username = 'a' * (settings.USERNAME_MAX_LENGTH + 1)
        invalid_usernames = [
            (None, 'Username empty'),
            ('', 'Username empty'),
            ('a' * (settings.USERNAME_MIN_LENGTH - 1),
             f'Username length {settings.USERNAME_MIN_LENGTH - 1} < {settings.USERNAME_MIN_LENGTH}'),
            (long_username, f'Username length {len(long_username)} > {settings.USERNAME_MAX_LENGTH}'),
        ]
        print(f'\n-------------------\nTesting {name}')
        for invalid_username in invalid_usernames:
            username = invalid_username[0]
            expected_errors = [invalid_username[1]]
            print(f'\nTesting {name} with username \'{username}\'')
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
            print(f'\nTesting {name} with email {email}')
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
        print(f'\n-------------------\nTesting {name}')
        for invalid_email in invalid_emails:
            email = invalid_email[0]
            expected_errors = [invalid_email[1]]
            username = 'Aurel' + str(random.randint(0, 100000))
            print(f'\nTesting {name} with email \'{email}\'')
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
        email = 'alevra@student.42lyon.fr'
        valid_passwords = [
            'Validpass42*', 'a' * (settings.PASSWORD_MAX_LENGTH - 3) + 'A1*',
                            'a' * (settings.PASSWORD_MIN_LENGTH - 3) + 'A1*'
        ]
        for password in valid_passwords:
            username = 'Aurel' + str(random.randint(0, 100000))
            print(f'\nTesting {name} with password {password}')
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
        print(f'\n-------------------\nTesting {name}')
        for invalid_password in invalid_passwords:
            password = invalid_password[0]
            expected_errors = [invalid_password[1]]
            username = 'Aurel' + str(random.randint(0, 100000))
            print(f'\nTesting {name} with password \'{password}\'')
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
        result = self.client.post(url, json.dumps(data_preparation), content_type='application/json')
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
            'username': 'Aurel303',
            'email': 'a@a.fr',
            'password': 'Validpass42*',
        }
        url = reverse('signup')
        self.client.post(url, json.dumps(data_preparation), content_type='application/json')
        data_username_exist = {
            'username': 'Aurel303'
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
