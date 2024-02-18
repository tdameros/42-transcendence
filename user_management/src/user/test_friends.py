import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from user.models import Friend, User
from user_management.JWTManager import UserAccessJWTManager


class FriendsTest(TestCase):
    @patch('user.views.sign_up.post_user_stats')
    def create_user(self, body, mock_user_stats):
        mock_user_stats.return_value = (True, None)
        url = reverse('signup')
        response = self.client.post(url, json.dumps(body), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        refresh_token = response.json()['refresh_token']
        url = reverse('refresh-access-jwt')
        response = self.client.post(url, json.dumps({'refresh_token': refresh_token}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        return response.json()['access_token']

    def get_friends(self, access_token):
        url = reverse('friends')
        response = self.client.get(url, content_type='application/json', HTTP_AUTHORIZATION=f'{access_token}')
        return response

    def request_friends(self, access_token, friend_id):
        url = reverse('friends-request')
        response = self.client.post(
            url,
            json.dumps({'friend_id': friend_id}),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'{access_token}'
        )
        return response

    def accept_friends(self, access_token, friend_id):
        url = reverse('friends-accept')
        response = self.client.post(
            url,
            json.dumps({'friend_id': friend_id}),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'{access_token}'
        )
        return response

    def decline_friends(self, access_token, friend_id):
        url = reverse('friends-decline')
        response = self.client.post(
            url,
            json.dumps({'friend_id': friend_id}),
            content_type='application/json',
            HTTP_AUTHORIZATION=f'{access_token}'
        )
        return response

    def delete_friends(self, access_token, friend_id):
        url = reverse('friends')
        if friend_id is not None:
            url += f'?friend_id={friend_id}'
        response = self.client.delete(
            url,
            HTTP_AUTHORIZATION=f'{access_token}',
        )
        return response

    def get_id_from_username(self, username):
        url = reverse('username', args=[username])
        first_id_in_db = User.objects.all().first().id
        response = self.client.get(url, HTTP_AUTHORIZATION=f'{UserAccessJWTManager.generate_jwt(first_id_in_db)[1]}')
        return response.json()['id']


class FriendsRequestTest(FriendsTest):
    def test_valid(self):
        user1 = {
            'username': 'User1',
            'email': 'user1@test.com',
            'password': 'Validpass42*',
        }
        user2 = {
            'username': 'User2',
            'email': 'user2@test.com',
            'password': 'Validpass42*',
        }
        token1 = self.create_user(user1)
        self.create_user(user2)
        user_id = self.get_id_from_username('User1')
        friend_id = self.get_id_from_username('User2')
        response = self.request_friends(token1, friend_id)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['message'], 'friend request sent')
        friends = Friend.objects.filter(user_id=user_id, friend_id=friend_id)
        self.assertEqual(len(friends), 1)
        self.assertEqual(friends[0].status, Friend.PENDING)

    def test_invalid_friend_id(self):
        user1 = {
            'username': 'User1',
            'email': 'user1@test.com',
            'password': 'Validpass42*',
        }
        token1 = self.create_user(user1)
        response = self.request_friends(token1, None)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['`friend_id` field required'])
        response = self.request_friends(token1, 'test')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['`friend_id` field must be an integer'])
        response = self.request_friends(token1, 3)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['Friend not found'])

    def test_invalid_already_sent(self):
        user1 = {
            'username': 'User1',
            'email': 'user1@test.com',
            'password': 'Validpass42*',
        }
        user2 = {
            'username': 'User2',
            'email': 'user2@test.com',
            'password': 'Validpass42*',
        }
        token1 = self.create_user(user1)
        self.create_user(user2)
        user_id = self.get_id_from_username('User1')
        friend_id = self.get_id_from_username('User2')
        self.request_friends(token1, friend_id)
        response = self.request_friends(token1, friend_id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['Friend status: pending'])
        friend = Friend.objects.get(user_id=user_id, friend_id=friend_id)
        self.assertEqual(friend.status, Friend.PENDING)

    def test_invalid_already_friends(self):
        user1 = {
            'username': 'User1',
            'email': 'user1@test.com',
            'password': 'Validpass42*',
        }
        user2 = {
            'username': 'User2',
            'email': 'user2@test.com',
            'password': 'Validpass42*',
        }
        token1 = self.create_user(user1)
        token2 = self.create_user(user2)
        user_1_id = self.get_id_from_username('User1')
        user_2_id = self.get_id_from_username('User2')
        self.request_friends(token1, user_2_id)
        self.accept_friends(token2, user_1_id)
        response = self.request_friends(token1, user_2_id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['Friend status: accepted'])
        friend = Friend.objects.get(user_id=user_1_id, friend_id=user_2_id)
        self.assertEqual(friend.status, Friend.ACCEPTED)


class FriendsAcceptTest(FriendsTest):
    def test_valid(self):
        user1 = {
            'username': 'User1',
            'email': 'user1@test.com',
            'password': 'Validpass42*',
        }
        user2 = {
            'username': 'User2',
            'email': 'user2@test.com',
            'password': 'Validpass42*',
        }
        token1 = self.create_user(user1)
        token2 = self.create_user(user2)
        user_1_id = self.get_id_from_username('User1')
        user_2_id = self.get_id_from_username('User2')
        self.request_friends(token1, user_2_id)
        response = self.accept_friends(token2, user_1_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'friend request accepted')
        friend_1 = Friend.objects.get(user_id=user_1_id, friend_id=user_2_id)
        self.assertEqual(friend_1.status, Friend.ACCEPTED)
        friend_2 = Friend.objects.get(user_id=user_2_id, friend_id=user_1_id)
        self.assertEqual(friend_2.status, Friend.ACCEPTED)

    def test_invalid_friend_id(self):
        user1 = {
            'username': 'User1',
            'email': 'user1@test.com',
            'password': 'Validpass42*',
        }
        token1 = self.create_user(user1)
        response = self.accept_friends(token1, None)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['`friend_id` field required'])
        response = self.accept_friends(token1, 'test')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['`friend_id` field must be an integer'])
        response = self.accept_friends(token1, 3)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['Friend not found'])

    def test_invalid_not_requested(self):
        user1 = {
            'username': 'User1',
            'email': 'user1@test.com',
            'password': 'Validpass42*',
        }
        token = self.create_user(user1)
        user_id = self.get_id_from_username('User1')
        response = self.accept_friends(token, user_id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['Friend request not found'])

    def test_invalid_already_friends(self):
        user1 = {
            'username': 'User1',
            'email': 'user1@test.com',
            'password': 'Validpass42*',
        }
        user2 = {
            'username': 'User2',
            'email': 'user2@test.com',
            'password': 'Validpass42*',
        }
        token1 = self.create_user(user1)
        token2 = self.create_user(user2)
        user_1_id = self.get_id_from_username('User1')
        user_2_id = self.get_id_from_username('User2')
        self.request_friends(token1, user_2_id)
        self.accept_friends(token2, user_1_id)
        response = self.accept_friends(token1, user_2_id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['Friend request already accepted'])
        friend = Friend.objects.get(user_id=user_1_id, friend_id=user_2_id)
        self.assertEqual(friend.status, Friend.ACCEPTED)


class FriendsDeclineTest(FriendsTest):
    def test_valid(self):
        user1 = {
            'username': 'User1',
            'email': 'user1@test.com',
            'password': 'Validpass42*',
        }
        user2 = {
            'username': 'User2',
            'email': 'user2@test.com',
            'password': 'Validpass42*',
        }
        token1 = self.create_user(user1)
        token2 = self.create_user(user2)
        user_1_id = self.get_id_from_username('User1')
        user_2_id = self.get_id_from_username('User2')
        self.request_friends(token1, user_2_id)
        response = self.decline_friends(token2, user_1_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'friend request declined')
        friends = Friend.objects.filter(user_id=user_1_id, friend_id=user_2_id)
        self.assertEqual(len(friends), 0)
        friends = Friend.objects.filter(user_id=user_2_id, friend_id=user_1_id)
        self.assertEqual(len(friends), 0)

    def test_invalid_friend_id(self):
        user1 = {
            'username': 'User1',
            'email': 'user1@test.com',
            'password': 'Validpass42*',
        }
        token1 = self.create_user(user1)
        response = self.decline_friends(token1, None)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['`friend_id` field required'])
        response = self.decline_friends(token1, 'test')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['`friend_id` field must be an integer'])
        response = self.decline_friends(token1, 3)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['Friend not found'])

    def test_invalid_not_requested(self):
        user1 = {
            'username': 'User1',
            'email': 'user1@test.com',
            'password': 'Validpass42*',
        }
        token = self.create_user(user1)
        user_id = self.get_id_from_username('User1')
        response = self.decline_friends(token, user_id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['Friend request not found'])

    def test_invalid_already_friends(self):
        user1 = {
            'username': 'User1',
            'email': 'user1@test.com',
            'password': 'Validpass42*',
        }
        user2 = {
            'username': 'User2',
            'email': 'user2@test.com',
            'password': 'Validpass42*',
        }
        token1 = self.create_user(user1)
        token2 = self.create_user(user2)
        user_1_id = self.get_id_from_username('User1')
        user_2_id = self.get_id_from_username('User2')
        self.request_friends(token1, user_2_id)
        self.accept_friends(token2, user_1_id)
        response = self.decline_friends(token1, user_2_id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['Friend request already accepted'])
        friend = Friend.objects.get(user_id=user_1_id, friend_id=user_2_id)
        self.assertEqual(friend.status, Friend.ACCEPTED)


class GetFriendsTest(FriendsTest):
    def test_valid(self):
        user1 = {
            'username': 'User1',
            'email': 'user1@test.com',
            'password': 'Validpass42*',
        }
        user2 = {
            'username': 'User2',
            'email': 'user2@test.com',
            'password': 'Validpass42*',
        }
        user3 = {
            'username': 'User3',
            'email': 'user3@test.com',
            'password': 'Validpass42*',
        }
        token1 = self.create_user(user1)
        token2 = self.create_user(user2)
        token3 = self.create_user(user3)
        user_1_id = self.get_id_from_username('User1')
        user_2_id = self.get_id_from_username('User2')
        user_3_id = self.get_id_from_username('User3')
        self.request_friends(token1, user_2_id)
        self.request_friends(token1, user_3_id)
        self.accept_friends(token2, user_1_id)

        response = self.get_friends(token1)
        self.assertEqual(response.status_code, 200)
        friends = response.json()['friends']
        self.assertEqual(len(friends), 2)
        self.assertEqual(friends[0]['id'], user_2_id)
        self.assertEqual(friends[0]['status'], 'accepted')
        self.assertEqual(friends[1]['id'], user_3_id)
        self.assertEqual(friends[1]['status'], 'pending')

        response = self.get_friends(token2)
        self.assertEqual(response.status_code, 200)
        friends = response.json()['friends']
        self.assertEqual(len(friends), 1)
        self.assertEqual(friends[0]['id'], user_1_id)
        self.assertEqual(friends[0]['status'], 'accepted')

        response = self.get_friends(token3)
        self.assertEqual(response.status_code, 200)
        friends = response.json()['friends']
        self.assertEqual(len(friends), 0)

    def test_invalid(self):
        response = self.get_friends('test')
        self.assertEqual(response.status_code, 401)


class DeleteFriendsTest(FriendsTest):
    def test_valid(self):
        user1 = {
            'username': 'User1',
            'email': 'user1@test.com',
            'password': 'Validpass42*',
        }
        user2 = {
            'username': 'User2',
            'email': 'user2@test.com',
            'password': 'Validpass42*',
        }
        token1 = self.create_user(user1)
        token2 = self.create_user(user2)
        user_1_id = self.get_id_from_username('User1')
        user_2_id = self.get_id_from_username('User2')
        self.request_friends(token1, user_2_id)
        self.accept_friends(token2, user_1_id)
        response = self.delete_friends(token1, user_2_id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'friend deleted')
        friends = Friend.objects.filter(user_id=1, friend_id=2)
        self.assertEqual(len(friends), 0)
        friends = Friend.objects.filter(user_id=2, friend_id=1)
        self.assertEqual(len(friends), 0)

    def test_invalid_pending(self):
        user1 = {
            'username': 'User1',
            'email': 'user1@test.com',
            'password': 'Validpass42*',
        }
        user2 = {
            'username': 'User2',
            'email': 'user2@test.com',
            'password': 'Validpass42*',
        }
        token1 = self.create_user(user1)
        token2 = self.create_user(user2)
        user_id = self.get_id_from_username('User1')
        friend_id = self.get_id_from_username('User2')
        self.request_friends(token1, friend_id)
        response = self.delete_friends(token1, friend_id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['Friend not found'])
        response = self.delete_friends(token2, user_id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['Friend not found'])
        friends = Friend.objects.get(user_id=1, friend_id=2)
        self.assertEqual(friends.status, Friend.PENDING)

    def test_invalid_no_friends(self):
        user1 = {
            'username': 'User1',
            'email': 'user1@test.com',
            'password': 'Validpass42*',
        }
        user2 = {
            'username': 'User2',
            'email': 'user2@test.com',
            'password': 'Validpass42*',
        }
        token1 = self.create_user(user1)
        token2 = self.create_user(user2)
        user_1_id = self.get_id_from_username('User1')
        user_2_id = self.get_id_from_username('User2')
        response = self.delete_friends(token1, user_2_id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['Friend not found'])
        response = self.delete_friends(token2, user_1_id)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['Friend not found'])

    def test_invalid_user_id(self):
        user1 = {
            'username': 'User1',
            'email': 'user1@test.com',
            'password': 'Validpass42*',
        }
        token1 = self.create_user(user1)
        response = self.delete_friends(token1, None)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['`friend_id` query parameter required'])
        response = self.delete_friends(token1, 'test')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['`friend_id` query parameter must be an integer'])
        response = self.delete_friends(token1, 3)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['errors'], ['Friend not found'])
