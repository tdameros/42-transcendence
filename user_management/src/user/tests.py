import base64
import json
import random
from datetime import datetime, timedelta
from unittest.mock import patch

import jwt
import pyotp
from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from user.models import User
from user.views.delete_inactive_users import (remove_inactive_users,
                                              remove_old_pending_accounts)
from user_management import settings
from user_management.JWTManager import (UserAccessJWTManager,
                                        UserRefreshJWTManager)


class TestsSignup(TestCase):

    def run_signup_test(self, name, username, email, password, expected_status,
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
        if expected_errors:
            self.assertEqual(result.json()['errors'], expected_errors)

    def test_signup_valid_username(self):
        password = 'Validpass42*'
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
                                 )

    def test_signup_invalid_username(self):
        password = 'Validpass42*'
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
                                 expected_errors)

    def test_signup_valid_email(self):
        password = 'Validpass42*'
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
            self.run_signup_test(name, username, email, password, expected_status)

    def test_signup_invalid_email(self):
        password = 'Validpass42*'
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
                                 expected_errors)

    def test_signup_valid_password(self):
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
                                 )

    def test_signup_invalid_password(self):
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
                                 expected_errors)

    def test_signup_not_a_json(self):
        string = 'This is not a JSON'
        url = reverse('signup')
        result = self.client.post(url, string, content_type='application/json')
        self.assertEqual(result.status_code, 400)
        self.assertTrue('errors' in result.json())


class TestsSignin(TestCase):

    def test_signin(self):
        User.objects.create(
            username='aurelien123',
            email='a@a.fr',
            password=make_password('Validpass42*'),
            emailVerified=True)
        url = reverse('signin')
        data = {
            'login': 'aurelien123',
            'password': 'Validpass42*',
        }
        result = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(result.status_code, 200)

        data_wrong_pass = {
            'login': 'aurelien123',
            'password': 'WrongValidpass42*',
        }
        url = reverse('signin')
        result = self.client.post(url, json.dumps(data_wrong_pass), content_type='application/json')
        self.assertEqual(result.status_code, 401)

        data_valid_email = {
            'login': 'a@a.fr',
            'password': 'Validpass42*',
        }
        url = reverse('signin')
        result = self.client.post(url, json.dumps(data_valid_email), content_type='application/json')
        self.assertEqual(result.status_code, 200)


class TestsUsernameExist(TestCase):

    def test_username_exist(self):
        User.objects.create(username='Burel305', email='a@a.fr', password='Validpass42*', emailVerified=True)
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
        user = User.objects.create(username='Aurel303',
                                   email='alevra@gmail.com',
                                   password='Validpass42*',
                                   emailVerified=True)
        data = {
            'refresh_token': UserRefreshJWTManager.generate_jwt(user.id)[1]
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
        User.objects.create(username='Aurel305',
                            email='a@a.fr',
                            password='Validpass42*',
                            emailVerified=True)
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
        user = User.objects.create(username='Aurel303',
                                   email='alevra@gmail.com',
                                   password='Validpass42*',
                                   emailVerified=True)
        url = reverse('user-id', args=[user.id])
        result = self.client.get(url)
        self.assertEqual(result.status_code, 401)
        result = self.client.get(url, HTTP_AUTHORIZATION=f'{UserAccessJWTManager.generate_jwt(user.id)[1]}')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(user.username, result.json()['username'])
        self.assertEqual(user.id, result.json()['id'])


class Username(TestCase):

    def test_username(self):
        user = User.objects.create(username='Aurel303',
                                   email='alevra@gmail.com',
                                   password='Validpass42*',
                                   emailVerified=True)
        url = reverse('username', args=[user.username])
        result = self.client.get(url)
        self.assertEqual(result.status_code, 401)
        result = self.client.get(url, HTTP_AUTHORIZATION=f'{UserAccessJWTManager.generate_jwt(user.id)[1]}')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(user.username, result.json()['username'])
        self.assertEqual(user.id, result.json()['id'])

    def test_invalid_username(self):
        user = User.objects.create(username='forjwt', email='a@a.fr', password='Validpass42*')
        user_id = user.id
        url = reverse('username', args=['invalid_username_123'])
        result = self.client.get(url)
        self.assertEqual(result.status_code, 401)
        result = self.client.get(url, HTTP_AUTHORIZATION=f'{UserAccessJWTManager.generate_jwt(user_id)[1]}')
        self.assertEqual(result.status_code, 404)
        self.assertTrue('errors' in result.json())


class TestsSearchUsername(TestCase):

    def test_search_username(self):
        for i in range(1, 20):
            User.objects.create(username=f'Felix{i}',
                                email=f'felix{i}@gmail.com',
                                password='Validpass42*',
                                emailVerified=True)
        data = {
            'username': 'Felix'
        }
        url = reverse('search-username')
        result = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(result.status_code, 401)
        Aurel1 = User.objects.create(username='Aurel1', email='aurel1@42.fr', password='Validpass42*')
        result = self.client.post(url, json.dumps(data), content_type='application/json',
                                  HTTP_AUTHORIZATION=f'{UserAccessJWTManager.generate_jwt(Aurel1.id)[1]}')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('users' in result.json())
        self.assertEqual(len(result.json()['users']), 10)
        data = {
            'username': 'Felix1'
        }
        url = reverse('search-username')
        result = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(result.status_code, 401)
        result = self.client.post(url, json.dumps(data), content_type='application/json',
                                  HTTP_AUTHORIZATION=f'{UserAccessJWTManager.generate_jwt(Aurel1.id)[1]}')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('users' in result.json())
        self.assertEqual(len(result.json()['users']), 10)
        data = {
            'username': 'Felix2'
        }
        url = reverse('search-username')
        result = self.client.post(url, json.dumps(data), content_type='application/json',
                                  HTTP_AUTHORIZATION=f'{UserAccessJWTManager.generate_jwt(Aurel1.id)[1]}')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('users' in result.json())
        self.assertEqual(len(result.json()['users']), 1)
        self.assertEqual(result.json()['users'][0], 'Felix2')
        data = {
            'username': 'Felix111'
        }
        url = reverse('search-username')
        result = self.client.post(url, json.dumps(data), content_type='application/json',
                                  HTTP_AUTHORIZATION=f'{UserAccessJWTManager.generate_jwt(Aurel1.id)[1]}')
        self.assertEqual(result.status_code, 200)
        self.assertTrue('users' in result.json())
        self.assertEqual(len(result.json()['users']), 0)


class TestsUserUpdateInfos(TestCase):
    """ 1) first, create a user with /user/signup
    2) get the access token of the user just created with /user/refresh-access-jwt
    3) then, update the user infos with /user/update-infos
    4) finally, check if the user infos have been updated with /user/user-id
    5) test invalid data"""

    def test_user_update_infos(self):
        # 1)
        user = User.objects.create(username='UpdateThisUser',
                                   email='updatethisuser@gmail.com',
                                   password='Validpass42*',
                                   emailVerified=True)
        refresh_token = UserRefreshJWTManager.generate_jwt(user.id)[1]
        user = User.objects.filter(username='UpdateThisUser').first()

        # 2)
        url = reverse('refresh-access-jwt')
        result = self.client.post(url, json.dumps({'refresh_token': refresh_token}), content_type='application/json')
        access_token = result.json()['access_token']

        # 3)
        data = {
            'change_list': ['username', 'email', 'password'],
            'username': 'UpdatedUser',
            'email': 'updateduser@gmail.com',
            'password': 'AnotherValidpass42*'
        }
        url = reverse('update-infos')
        result = self.client.post(url, json.dumps(data), content_type='application/json')

        # 4)
        self.assertEqual(result.status_code, 401)
        result = self.client.post(url, json.dumps(data), content_type='application/json',
                                  HTTP_AUTHORIZATION=f'{access_token}')
        self.assertEqual(result.status_code, 200)
        user = User.objects.filter(username='UpdatedUser').first()
        self.assertEqual(user.username, 'UpdatedUser')
        self.assertEqual(user.email, 'updateduser@gmail.com')

        # 5)
        data = {
            'access_token': access_token,
            'change_list': ['username', 'email', 'password'],
            'username': 'I',
            'email': 'a.fr',
            'password': 'aninvalidpassword'
        }

        url = reverse('update-infos')
        result = self.client.post(url, json.dumps(data), content_type='application/json',
                                  HTTP_AUTHORIZATION=f'{access_token}')
        self.assertEqual(result.status_code, 400)
        self.assertTrue('errors' in result.json())
        self.assertTrue(result.json()['errors'])


class TestsTwoFa(TestCase):

    def test_two_fa(self):
        user = User.objects.create(username='TestTwoFA',
                                   email='aurelien.levra@gmail.com',
                                   password='Validpass42*',
                                   emailVerified=True)
        refresh_token = UserRefreshJWTManager.generate_jwt(user.id)[1]
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
            'code': '234567'
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


class TestUserIdList(TestCase):
    def test_user_id_list(self):
        # create a user

        Aurel1 = User.objects.create(username='Aurel1', email='aurel1@42.fr', password='Validpass42*')
        User.objects.create(username='Aurel2', email='aurel2@42.fr', password='Validpass42*')
        User.objects.create(username='Aurel3', email='aurel3@42.fr', password='Validpass42*')
        User.objects.create(username='Aurel4', email='aurel4@42.fr', password='Validpass42*')

        # get the list of id of the users
        UserList = User.objects.all()
        id_list = [user.id for user in User.objects.all()]
        data = {
            'id_list': id_list
        }

        url = reverse('user-id-list')
        result = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(result.status_code, 401)
        result = self.client.post(url, json.dumps(data), content_type='application/json',
                                  HTTP_AUTHORIZATION=f'{UserAccessJWTManager.generate_jwt(Aurel1.id)[1]}')
        for user in UserList:
            self.assertEqual(result.json().get(str(user.id)), user.username)


class TestDeletedUser(TestCase):

    @patch('requests.delete')
    @patch('requests.post')
    def test_deleted_user(self, mock_post, mock_delete):
        Aurel1 = User.objects.create(username='Aurel1', email='aurel1@42.fr', password='Validpass42*')
        url = reverse('delete-account')
        access_token = UserAccessJWTManager.generate_jwt(Aurel1.id)[1]

        mock_delete.return_value.status_code = 200
        mock_post.return_value.status_code = 200
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'{access_token}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Account deleted')
        self.assertEqual(User.objects.filter(username='Aurel1').count(), 0)
        Aurel1 = User.objects.filter(id=Aurel1.id).first()
        self.assertTrue(Aurel1.account_deleted)

        refresh_token = UserRefreshJWTManager.generate_jwt(Aurel1.id)[1]
        url = reverse('refresh-access-jwt')
        data = {
            'refresh_token': refresh_token
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertNotEqual(response.status_code, 200)


class TestAvatar(TestCase):
    def test_avatar(self):
        user = User.objects.create(username='alevra', email='aurel1@42.fr', password='Validpass42*')
        access_token = UserAccessJWTManager.generate_jwt(user.id)[1]
        url = reverse('avatar')

        if settings.DEBUG:
            path = 'test_resources/avatar.png'
        else:
            path = 'user/test_resources/avatar.png'
        avatar = open(path, 'rb')
        base64_avatar = base64.b64encode(avatar.read()).decode('utf-8')
        base64_avatar = f'data:image/png;base64,{base64_avatar}'
        avatar.close()
        data = {
            'avatar': base64_avatar
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json',
                                    HTTP_AUTHORIZATION=f'{access_token}')

        self.assertEqual(response.status_code, 200)
        url = reverse('avatar', args=['alevra'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('image/png' in response['Content-Type'])

        url = reverse('avatar')
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'{access_token}')
        self.assertEqual(response.status_code, 200)

        # test with too big avatar
        if settings.DEBUG:
            path = 'test_resources/too_big_avatar.png'
        else:
            path = 'user/test_resources/too_big_avatar.png'
        avatar = open(path, 'rb')
        base64_avatar = base64.b64encode(avatar.read()).decode('utf-8')
        base64_avatar = f'data:image/png;base64,{base64_avatar}'
        avatar.close()
        data = {
            'avatar': base64_avatar
        }

        response = self.client.post(url, json.dumps(data), content_type='application/json',
                                    HTTP_AUTHORIZATION=f'{access_token}')

        self.assertEqual(response.status_code, 400)


class TestEmailVerified(TestCase):
    @patch('user.views.verify_email.post_user_stats')
    def test_email_verified(self, mock_user_stats):
        mock_user_stats.return_value = (True, None)
        username = 'testEmailVerified'
        email = 'a@a.fr'
        password = 'Validpass42*'
        data = {
            'username': username,
            'email': email,
            'password': password,
        }
        url = reverse('signup')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        user = User.objects.filter(username='testEmailVerified').first()
        self.assertTrue(user.emailVerificationToken)
        url = reverse('verify-email', args=[user.id, user.emailVerificationToken])
        response = self.client.post(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        user = User.objects.filter(username='testEmailVerified').first()
        self.assertTrue(user.emailVerified)
        self.assertEqual(user.emailVerificationToken, None)

        username = 'testBadToken'
        email = 'a2@a.fr'
        data = {
            'username': username,
            'email': email,
            'password': password,
        }
        url = reverse('signup')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        user = User.objects.filter(username='testBadToken').first()
        url = reverse('verify-email', args=[user.id, 'bad_token'])
        response = self.client.post(url, content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertTrue('errors' in response.json())
        self.assertEqual(response.json()['errors'], ['invalid verification token'])
        user = User.objects.filter(username='testBadToken').first()
        self.assertFalse(user.emailVerified)
        # test expired token

        username = 'testExpiredToken'
        email = 'a3@a.fr'
        data = {
            'username': username,
            'email': email,
            'password': password,
        }
        url = reverse('signup')
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        user = User.objects.filter(username='testExpiredToken').first()
        user.emailVerificationTokenExpiration = datetime.now(timezone.utc) - timedelta(days=1)
        user.save()
        url = reverse('verify-email', args=[user.id, user.emailVerificationToken])
        response = self.client.post(url, content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertTrue('errors' in response.json())
        self.assertEqual(response.json()['errors'], ['verification token expired'])
        user = User.objects.filter(username='testExpiredToken').first()
        self.assertFalse(user.emailVerified)
        self.assertEqual(user.emailVerificationToken, None)
        self.assertEqual(user.emailVerificationTokenExpiration, None)


class TestDeleteInactiveUsersView(TestCase):

    def test_delete_inactive_users(self):
        for i in range(0, 20):
            fake_inactive_account = User.objects.create(username=f'InactiveAccount{i}',
                                                        email=f'InactiveAccount{i}@42.fr',
                                                        password='Validpass42*')
            fake_inactive_account.last_activity = (timezone.now() -
                                                   timedelta(days=settings.MAX_INACTIVITY_DAYS_BEFORE_DELETION + 1))
            fake_inactive_account.save()
        self.assertEqual(User.objects.filter(account_deleted=False).count(), 20)
        self.assertEqual(User.objects.all().count(), 20)
        remove_inactive_users()
        self.assertEqual(User.objects.filter(account_deleted=True).count(), 0)

        for i in range(0, 20):
            fake_old_pending_accounts = User.objects.create(username=f'PendingAccount{i}',
                                                            email=f'PendingAccount{i}@42.fr',
                                                            password='Validpass42*',
                                                            emailVerified=False)
            fake_old_pending_accounts.date_joined = (
                    timezone.now() - timedelta(days=settings.MAX_DAYS_BEFORE_PENDING_ACCOUNTS_DELETION + 1))
            fake_old_pending_accounts.save()

        self.assertEqual(User.objects.filter(account_deleted=False).count(), 40)
        remove_old_pending_accounts()
        self.assertEqual(User.objects.filter(account_deleted=True).count(), 0)


class TestSendUserInfosView(TestCase):

    @patch('common.src.internal_requests.InternalRequests.get')
    def test_send_user_infos(self, mock_internal_requests_get):
        # mock handling
        mock_internal_requests_get.return_value.status_code = 200

        Aurel1 = User.objects.create(username='Aurel1', email='aurelien.levra@gmail.com', password='Validpass42*')
        access_token = UserAccessJWTManager.generate_jwt(Aurel1.id)[1]
        # avatar
        url = reverse('avatar')
        if settings.DEBUG:
            path = 'test_resources/avatar.png'
        else:
            path = 'user/test_resources/avatar.png'
        avatar = open(path, 'rb')
        base64_avatar = base64.b64encode(avatar.read()).decode('utf-8')
        base64_avatar = f'data:image/png;base64,{base64_avatar}'
        avatar.close()
        data = {
            'avatar': base64_avatar
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json',
                                    HTTP_AUTHORIZATION=f'{access_token}')
        self.assertEqual(response.status_code, 200)

        url = reverse('send-user-infos')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'{access_token}')
        self.assertEqual(response.status_code, 200)


class TestMeView(TestCase):

    def test_me(self):
        Aurel1 = User.objects.create(username='Aurel1', email='a@a.fr', password='Validpass42*')
        access_token = UserAccessJWTManager.generate_jwt(Aurel1.id)[1]
        url = reverse('me')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'{access_token}')
        self.assertEqual(response.status_code, 200)

        url = reverse('me')
        response = self.client.get(url, HTTP_AUTHORIZATION='invalid_token')
        self.assertEqual(response.status_code, 401)
